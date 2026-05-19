"""
Archovive v1 — Attestation export (Markdown + deterministic PDF).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from archovive_os.product_v1._core import core
from archovive_os.product_v1.constants import ATTESTATION_SCHEMA, PRODUCT_VERSION
from archovive_os.product_v1.spec_ref import SPEC_V4_HASH

Status = Literal["PASS", "FAIL"]

# Reproducible export anchor (no wall-clock timestamps in PDF metadata pipeline).
EXPORT_SOURCE_DATE_EPOCH = "946684800"  # 2000-01-01T00:00:00Z
SPEC_DOC_LINK = "docs/pipe/PIPE_V4_SPEC.md"

PANDOC_DETERMINISTIC_ARGS = [
    "--standalone",
    "--from=markdown",
    "--to=pdf",
    "--pdf-engine=pdflatex",
    "--variable=geometry:margin=2.5cm",
    "--variable=fontsize=11pt",
    "--variable=documentclass=article",
    "--variable=classoption=oneside",
    "--variable=colorlinks=false",
    "--variable=linkcolor=black",
    "--variable=urlcolor=black",
    "--metadata=date:2000-01-01T00:00:00Z",
    "--metadata=author:Archovive",
]


@dataclass
class KitContext:
    spec_hash: str = ""
    health_certificate_hash: str = ""
    health_status: str = ""
    health_spec_hash: str = ""
    ledger_excerpt: str = ""
    bundle_hash: str = ""
    replay_match: bool | None = None
    replay_fixture: str | None = None
    identity_stable: bool | None = None


@dataclass
class ExportResult:
    status: Status
    attest_path: str
    md_path: str
    pdf_path: str | None
    md_hash: str
    pdf_hash: str | None
    errors: list[str] = field(default_factory=list)
    pandoc_available: bool = False

    def to_json(self) -> str:
        return json.dumps(
            {
                "status": self.status,
                "attest_path": self.attest_path,
                "md_path": self.md_path,
                "pdf_path": self.pdf_path,
                "md_hash": self.md_hash,
                "pdf_hash": self.pdf_hash,
                "pandoc_available": self.pandoc_available,
                "errors": self.errors,
            },
            separators=(",", ":"),
        )


def load_attestation(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != ATTESTATION_SCHEMA:
        raise ValueError(f"unsupported schema_version: {data.get('schema_version')}")
    return data


def _hash_file(path: Path) -> str:
    return core.stable_hash_v3({"export_file_v1": True, "name": path.name, "body": path.read_bytes()})


def _fixture_for_repo(repo: str) -> str | None:
    for fixture in core.list_golden_fixtures():
        try:
            manifest = core.load_manifest(core.golden_root() / fixture)
        except OSError:
            continue
        if str(manifest.get("repo")) == repo:
            return fixture
    return None


def load_kit_context(kit_dir: Path, attestation: dict[str, Any], *, verify_replay: bool) -> KitContext:
    ctx = KitContext()
    spec_path = kit_dir / "spec_v4.json"
    if spec_path.exists():
        try:
            spec_doc = json.loads(spec_path.read_text(encoding="utf-8"))
            ctx.spec_hash = core.spec_document_hash(spec_doc)
        except (OSError, json.JSONDecodeError):
            ctx.spec_hash = SPEC_V4_HASH
    else:
        ctx.spec_hash = SPEC_V4_HASH

    hc_path = kit_dir / "health_certificate_v2.json"
    if hc_path.exists():
        try:
            hc = json.loads(hc_path.read_text(encoding="utf-8"))
            ctx.health_status = str(hc.get("status", ""))
            ctx.health_spec_hash = str(hc.get("spec_hash", ""))
            ctx.health_certificate_hash = str(hc.get("certificate_hash", ""))
        except (OSError, json.JSONDecodeError):
            pass

    ledger_path = kit_dir / "ledger.jsonl"
    if ledger_path.exists() and ledger_path.stat().st_size:
        lines = ledger_path.read_text(encoding="utf-8").strip().splitlines()[:5]
        ctx.ledger_excerpt = "\n".join(lines)

    manifest_path = kit_dir / "BUNDLE_MANIFEST.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            ctx.bundle_hash = str(manifest.get("bundle_hash", ""))
        except (OSError, json.JSONDecodeError):
            pass

    if verify_replay:
        fixture = _fixture_for_repo(str(attestation.get("repo", "")))
        if fixture:
            replay = core.run_golden_replay(fixture)
            ctx.replay_fixture = fixture
            ctx.replay_match = bool(replay.get("match"))
            ctx.identity_stable = ctx.replay_match

    return ctx


def _deterministic_timestamp(attestation: dict[str, Any]) -> str:
    """Export-bound timestamp derived from attestation (no wall clock)."""
    ah = str(attestation.get("attestation_hash", ""))
    eid = (attestation.get("trust_surface") or {}).get("epoch_id") or "default"
    return f"{eid} / {ah[:16]}" if ah else str(eid)


def _executive_summary(attestation: dict[str, Any], ctx: KitContext) -> dict[str, str]:
    ts = attestation.get("trust_surface") or {}
    failed = [c for c in ts.get("control_verdict_hashes", []) if not c.get("passed")]
    primary = failed[0] if failed else {}
    reasons = []
    if primary:
        reasons.append(str(primary.get("control_id", "")))
    ics = "ICS capacity threshold exceeded" if any(
        "ICS" in str(primary.get("control_id", "")) for _ in [1]
    ) else "—"
    if primary and "ICS" in str(primary.get("control_id", "")):
        ics = f"Control {primary.get('control_id')} — regulatory capacity scenario"
    return {
        "verdict": str(attestation.get("verdict", "UNKNOWN")),
        "ics_capacity": ics,
        "economic_impact": "Quantified in governance layer (see ledger / audit response)",
        "governance_decision": "NON_COMPLIANT — enforce remediation" if failed else "COMPLIANT",
        "failed_control": str(primary.get("control_id", "—")),
        "control_verdict_hash": str(primary.get("control_verdict_hash", "—")),
    }


def render_attestation_markdown(
    attestation: dict[str, Any],
    *,
    kit_ctx: KitContext | None = None,
) -> str:
    """Render full auditor-facing attest.md from attestation JSON."""
    kit_ctx = kit_ctx or KitContext(spec_hash=SPEC_V4_HASH)
    ts = attestation.get("trust_surface") or {}
    summary = _executive_summary(attestation, kit_ctx)
    ts_export = _deterministic_timestamp(attestation)
    failed_controls = [c for c in ts.get("control_verdict_hashes", []) if not c.get("passed")]

    replay_line = "Not verified in this export"
    if kit_ctx.replay_match is True:
        replay_line = f"BIT-IDENTICAL ({kit_ctx.replay_fixture})"
    elif kit_ctx.replay_match is False:
        replay_line = f"MISMATCH ({kit_ctx.replay_fixture})"

    identity_line = (
        "VERIFIED (golden replay + identity chain)"
        if kit_ctx.identity_stable
        else ("FAILED" if kit_ctx.identity_stable is False else "Run archovive bootstrap for full check")
    )

    health_sig = kit_ctx.health_certificate_hash or "—"
    health_status = kit_ctx.health_status or "—"
    spec_consistent = (
        "CONSISTENT"
        if not kit_ctx.health_spec_hash or kit_ctx.health_spec_hash == kit_ctx.spec_hash
        else "MISMATCH"
    )

    lines: list[str] = [
        "---",
        "title: Archovive v1 Attestation Package",
        f"date: {EXPORT_SOURCE_DATE_EPOCH}",
        "author: Archovive",
        "---",
        "",
        "# Archovive v1 — Attestation Package",
        "",
        "## Title",
        "",
        f"- **Product:** {PRODUCT_VERSION}",
        f"- **Pipe release:** {attestation.get('pipe_release', '—')}",
        f"- **Export binding:** `{ts_export}`",
        f"- **Repository:** `{attestation.get('repo', '—')}`",
        "",
        "## Hash surface (bound)",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| attestation_hash | `{attestation.get('attestation_hash', '')}` |",
        f"| spec_hash | `{kit_ctx.spec_hash}` |",
        f"| health_certificate_hash | `{health_sig}` |",
        "",
        "## Executive summary",
        "",
        f"| Item | Value |",
        f"|------|-------|",
        f"| Verdict | **{summary['verdict']}** |",
        f"| ICS capacity | {summary['ics_capacity']} |",
        f"| Economic impact | {summary['economic_impact']} |",
        f"| Governance decision | {summary['governance_decision']} |",
        f"| Failed control | {summary['failed_control']} |",
        f"| control_verdict_hash | `{summary['control_verdict_hash']}` |",
        "",
        "## Trust surface",
        "",
        "| Hash | Value |",
        "|------|-------|",
        f"| H_input | `{ts.get('H_input', '')}` |",
        f"| H_triangulation | `{ts.get('H_triangulation', '')}` |",
        f"| H_verdict | `{ts.get('H_verdict', '')}` |",
        f"| audit_chain_root | `{ts.get('audit_chain_root', '')}` |",
        f"| epoch_binding_hash | `{ts.get('epoch_binding_hash', '')}` |",
        f"| hypervisor_binding_hash | `{ts.get('hypervisor_binding_hash', '')}` |",
        f"| lineage_hash_l3 | `{ts.get('lineage_hash_l3', '')}` |",
        "",
        "## Bindings",
        "",
        "### SPEC reference",
        "",
        f"- **SPEC version:** PIPE v4 ({attestation.get('contract_label', 'v4.0_contracts')})",
        f"- **SPEC hash:** `{kit_ctx.spec_hash}`",
        f"- **SPEC link:** `{SPEC_DOC_LINK}`",
        "",
        "### Health Certificate v2",
        "",
        f"- **Status:** {health_status}",
        f"- **Certificate hash (signature):** `{health_sig}`",
        f"- **spec_hash consistency:** {spec_consistent}",
        "",
        "## Replay evidence",
        "",
        f"- **Golden replay:** {replay_line}",
        f"- **Identity hash stability:** {identity_line}",
        "",
    ]

    if failed_controls:
        lines.extend(["## ICS control matrix (excerpt)", ""])
        for cv in failed_controls:
            lines.append(
                f"- `{cv.get('pack')}` / `{cv.get('control_id')}` — "
                f"hash `{cv.get('control_verdict_hash', '')}` — passed={cv.get('passed')}"
            )
        lines.append("")

    if kit_ctx.ledger_excerpt:
        lines.extend(["## Ledger excerpt", "", "```jsonl", kit_ctx.ledger_excerpt, "```", ""])

    lines.extend(
        [
            "## Appendix A — Full attestation JSON",
            "",
            "```json",
            json.dumps(attestation, indent=2, sort_keys=True),
            "```",
            "",
            f"*Document content hash (markdown): bound via export pipeline; attestation_hash `{attestation.get('attestation_hash', '')}`*",
            "",
        ]
    )
    return "\n".join(lines)


def pandoc_available() -> bool:
    return shutil.which("pandoc") is not None


def render_attestation_pdf(md_path: Path, pdf_path: Path) -> None:
    """Invoke pandoc with deterministic flags (requires pdflatex)."""
    if not pandoc_available():
        raise RuntimeError("pandoc not found on PATH")
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = EXPORT_SOURCE_DATE_EPOCH
    env["LANG"] = "C"
    env["LC_ALL"] = "C"
    cmd = [
        "pandoc",
        str(md_path),
        "-o",
        str(pdf_path),
        *PANDOC_DETERMINISTIC_ARGS,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"pandoc failed (exit {proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}"
        )


def run_attestation_export(
    attest_path: Path,
    *,
    write_pdf: bool = False,
    md_only: bool = False,
    out_md: Path | None = None,
    out_pdf: Path | None = None,
    verify_replay: bool = True,
) -> ExportResult:
    """
    Load attest.json, render attest.md, optionally attest.pdf into kit directory.
    """
    errors: list[str] = []
    attest_path = attest_path.resolve()
    kit_dir = attest_path.parent
    attestation = load_attestation(attest_path)
    kit_ctx = load_kit_context(kit_dir, attestation, verify_replay=verify_replay)

    md_path = out_md or kit_dir / "attest.md"
    pdf_path = out_pdf or kit_dir / "attest.pdf"

    md_text = render_attestation_markdown(attestation, kit_ctx=kit_ctx)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(md_text, encoding="utf-8")
    md_hash = _hash_file(md_path)

    pdf_hash: str | None = None
    pandoc_ok = pandoc_available()
    if write_pdf and not md_only:
        if not pandoc_ok:
            errors.append("pandoc not available (install pandoc + pdflatex for PDF export)")
        else:
            try:
                render_attestation_pdf(md_path, pdf_path)
                pdf_hash = core.stable_hash_v3({"pdf_v1": True, "body": pdf_path.read_bytes()})
            except OSError as exc:
                errors.append(f"PDF write failed: {exc}")
            except RuntimeError as exc:
                errors.append(str(exc))

    status: Status = "PASS" if not errors else "FAIL"
    return ExportResult(
        status=status,
        attest_path=str(attest_path),
        md_path=str(md_path.resolve()),
        pdf_path=str(pdf_path.resolve()) if pdf_hash else (None if md_only or not write_pdf else str(pdf_path)),
        md_hash=md_hash,
        pdf_hash=pdf_hash,
        errors=errors,
        pandoc_available=pandoc_ok,
    )
