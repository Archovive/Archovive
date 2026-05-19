"""
Archovive v1 Truth Simulator — guided DORA violation walkthrough.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Literal

from archovive_os.product_v1._core import core
from archovive_os.product_v1.analyze import build_attestation

Status = Literal["PASS", "FAIL"]
DEFAULT_FIXTURE = "pipe_l3_dora_violation"
PauseFn = Callable[[str], None] | None


@dataclass
class SimulateStep:
    phase: str
    title: str
    ok: bool
    lines: list[str] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulateResult:
    status: Status
    fixture: str
    verdict: str
    expected_verdict: str
    replay_match: bool
    trust_surface: dict[str, Any]
    attestation_hash: str
    steps: list[SimulateStep]
    errors: list[str] = field(default_factory=list)
    pipe_release: str = core.PIPE_V4_RELEASE
    violation_context: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(
            {
                "status": self.status,
                "pipe_release": self.pipe_release,
                "fixture": self.fixture,
                "verdict": self.verdict,
                "expected_verdict": self.expected_verdict,
                "replay_match": self.replay_match,
                "attestation_hash": self.attestation_hash,
                "trust_surface": self.trust_surface,
                "violation_context": self.violation_context,
                "steps": [
                    {
                        "phase": s.phase,
                        "title": s.title,
                        "ok": s.ok,
                        "lines": s.lines,
                        "data": s.data,
                    }
                    for s in self.steps
                ],
                "errors": self.errors,
            },
            separators=(",", ":"),
        )


def _short(value: str | None, width: int = 16) -> str:
    if not value:
        return "—"
    s = str(value)
    return f"{s[:width]}…" if len(s) > width else s


def _load_fixture(fixture: str) -> tuple[Path, dict[str, Any], dict[str, Any], bytes]:
    fixture_dir = core.golden_root() / fixture
    if not fixture_dir.is_dir():
        raise FileNotFoundError(f"golden fixture not found: {fixture}")
    manifest = core.load_manifest(fixture_dir)
    context_path = fixture_dir / "dora_violation_context.json"
    context: dict[str, Any] = {}
    if context_path.exists():
        context = json.loads(context_path.read_text(encoding="utf-8"))
    input_bytes = (fixture_dir / manifest.get("input_file", "input.json")).read_bytes()
    return fixture_dir, manifest, context, input_bytes


def run_simulate(
    fixture: str = DEFAULT_FIXTURE,
    *,
    epoch_id: str | None = None,
    pause: PauseFn = None,
) -> SimulateResult:
    """
    Run guided Ingestion → Runtime → Governance → Attestation → Replay sequence.
    """
    errors: list[str] = []
    steps: list[SimulateStep] = []

    _fixture_dir, manifest, context, input_bytes = _load_fixture(fixture)  # noqa: F841
    repo = str(manifest["repo"])
    tenant = str(manifest["tenant_id"])
    pack = str(manifest.get("compliance_pack", "DORA-2026"))
    pack_key = pack.split("-")[0]
    active = manifest.get("active_packs")
    active_packs = tuple(active) if isinstance(active, list) else None
    expected_verdict = str(manifest.get("expected_verdict", context.get("verdict_expected", "NON_COMPLIANT")))
    eid = core.resolve_epoch_id(epoch_id or manifest.get("epoch_id"))

    def _pause(phase: str) -> None:
        if pause:
            pause(phase)

    # --- [1/5] Ingestion (L1) ---
    l1 = core.run_pipe(repo, input_bytes, tenant_id=tenant, canonical=False, epoch_id=eid)
    pv7_l1 = l1.get("proof_v7") or {}
    step1 = SimulateStep(
        phase="ingestion",
        title="INGESTION (L1 — Hermetic Truth)",
        ok=True,
        lines=[
            f"H_input .............. {_short(pv7_l1.get('H_input'))}",
            f"H_triangulation ...... {_short(pv7_l1.get('H_triangulation'))}",
            f"H_verdict ............ {_short(pv7_l1.get('H_verdict'))}",
            f"lineage_hash ......... {_short(pv7_l1.get('lineage_hash'))}",
        ],
        data={
            "H_input": pv7_l1.get("H_input"),
            "H_triangulation": pv7_l1.get("H_triangulation"),
            "H_verdict": pv7_l1.get("H_verdict"),
            "lineage_hash": pv7_l1.get("lineage_hash"),
        },
    )
    steps.append(step1)
    _pause("ingestion")

    # --- [2/5] Runtime (L2) ---
    core.reset_runtime_ledger(repo, tenant)
    l2 = core.run_runtime_pipe(repo, input_bytes, tenant_id=tenant, compliance_pack=pack, epoch_id=eid)
    pv7_l2 = l2.get("proof_v7") or {}
    hv = l2.get("hypervisor_state") or {}
    step2 = SimulateStep(
        phase="runtime",
        title="RUNTIME (L2 — Operational Truth)",
        ok=True,
        lines=[
            f"runtime_record_hash .. {_short((l2.get('runtime_record') or {}).get('runtime_record_hash'))}",
            f"ledger_binding_hash .. {_short((l2.get('ledger') or {}).get('ledger_binding_hash'))}",
            f"epoch_binding_hash ... {_short(pv7_l2.get('epoch_binding_hash'))}",
            f"hypervisor_binding ... {_short(hv.get('binding_hash'))}",
            f"ZKAP ................. {'present' if l2.get('zkap') else '—'}",
        ],
        data={
            "ledger_binding_hash": (l2.get("ledger") or {}).get("ledger_binding_hash"),
            "epoch_binding_hash": pv7_l2.get("epoch_binding_hash"),
            "hypervisor_binding_hash": hv.get("binding_hash"),
            "lineage_hash_l2": pv7_l2.get("lineage_hash"),
        },
    )
    steps.append(step2)
    _pause("runtime")

    # --- [3/5] Governance (L3) ---
    core.reset_runtime_ledger(repo, tenant)
    core.reset_audit_ledger(repo, tenant, pack_key)
    l3 = core.run_audit_pipe(
        repo,
        input_bytes,
        tenant_id=tenant,
        compliance_pack=pack,
        active_packs=active_packs,
        epoch_id=eid,
    )
    verdict = str(l3.get("verdict", "UNKNOWN"))
    verdict_ok = verdict == expected_verdict
    if not verdict_ok:
        errors.append(f"verdict: expected {expected_verdict}, got {verdict}")

    reg = next(
        (s for s in (l3.get("audit_validation") or {}).get("stages", []) if s.get("stage") == "regulatory"),
        {},
    )
    failed = [v for v in reg.get("control_verdicts", []) if not v.get("passed")]
    primary = failed[0] if failed else {}
    economics = l3.get("audit_economics") or {}

    gov_lines = [
        f"Verdict .............. {verdict}",
        f"Regulation ........... {context.get('regulation', 'DORA')}",
        f"Article .............. {context.get('article', '—')}",
    ]
    if primary:
        gov_lines.extend(
            [
                f"Failed control ....... {primary.get('control_id')} ({', '.join(primary.get('reasons', []))})",
                f"control_verdict_hash . {_short(primary.get('control_verdict_hash'))}",
            ]
        )
    if economics.get("total_exposure"):
        gov_lines.append(f"Economic exposure .... {economics.get('total_exposure')}")

    step3 = SimulateStep(
        phase="governance",
        title="GOVERNANCE (L3 — Regulatory Truth)",
        ok=verdict_ok,
        lines=gov_lines,
        data={
            "verdict": verdict,
            "failed_controls": failed,
            "audit_chain_root": (l3.get("proof_v8") or {}).get("audit_chain_root"),
        },
    )
    steps.append(step3)
    _pause("governance")

    # --- [4/5] Attestation ---
    att = build_attestation(l3, repo=repo, bootstrap=None)
    ts = att.get("trust_surface") or {}
    step4 = SimulateStep(
        phase="attestation",
        title="ATTESTATION (Sovereign Proof Package)",
        ok=True,
        lines=[
            f"attestation_hash ..... {_short(att.get('attestation_hash'))}",
            f"audit_chain_root ..... {_short(ts.get('audit_chain_root'))}",
            f"epoch_binding_hash ... {_short(ts.get('epoch_binding_hash'))}",
            f"hypervisor_binding ... {_short(ts.get('hypervisor_binding_hash'))}",
        ],
        data={"attestation": att},
    )
    steps.append(step4)
    _pause("attestation")

    # --- [5/5] Replay ---
    replay = core.run_golden_replay(fixture, epoch_id=eid)
    replay_ok = bool(replay.get("match"))
    if not replay_ok:
        errors.extend(replay.get("errors") or ["golden replay mismatch"])
    step5 = SimulateStep(
        phase="replay",
        title="REPLAY (Golden Reproducibility)",
        ok=replay_ok,
        lines=[
            f"fixture .............. {fixture}",
            f"replay ............... {'BIT-IDENTICAL' if replay_ok else 'MISMATCH'}",
            f"audit_chain_root ..... {_short(replay.get('actual', {}).get('audit_chain_root'))}",
        ],
        data={
            "match": replay_ok,
            "errors": replay.get("errors"),
            "expected": replay.get("expected"),
            "actual": replay.get("actual"),
        },
    )
    steps.append(step5)
    _pause("replay")

    all_ok = verdict_ok and replay_ok and all(s.ok for s in steps)
    status: Status = "PASS" if all_ok else "FAIL"

    return SimulateResult(
        status=status,
        fixture=fixture,
        verdict=verdict,
        expected_verdict=expected_verdict,
        replay_match=replay_ok,
        trust_surface=ts,
        attestation_hash=str(att.get("attestation_hash", "")),
        steps=steps,
        errors=errors,
        violation_context=context,
    )


def format_simulate_tty(result: SimulateResult) -> list[str]:
    """Render full simulator transcript for terminal."""
    ctx = result.violation_context
    lines = [
        "=== [ARCHOVIVE v1] Truth Simulator ===",
        "",
        f"Scenario: DORA violation — {result.fixture}",
    ]
    if ctx.get("regulation"):
        lines.append(f"Regulation: {ctx['regulation']} — Article {ctx.get('article', '—')}")
    if ctx.get("description"):
        lines.append(f"Context: {ctx['description']}")
    lines.append("")

    for idx, step in enumerate(result.steps, start=1):
        lines.append(f"[{idx}/5] {step.title}")
        for detail in step.lines:
            lines.append(f"  {detail}")
        lines.append("")

    lines.append(f"SIMULATE: {result.status}")
    if result.status == "PASS":
        lines.append("")
        lines.append(
            "This is not a scanner. Archovive detected a DORA violation, quantified it, "
            "and produced a reproducible proof chain."
        )
    return lines
