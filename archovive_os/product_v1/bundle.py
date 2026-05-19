"""
Sovereign Kit — BUNDLE_MANIFEST.json and attestation package layout.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from archovive_os.product_v1._core import core

from archovive_os.product_v1.attestation_export import (
    load_kit_context,
    render_attestation_markdown,
    run_attestation_export,
)
from archovive_os.product_v1.constants import BUNDLE_MANIFEST_SCHEMA, PRODUCT_VERSION


def _file_hash(path: Path) -> str:
    return core.stable_hash_v3({"file_v1": True, "path": path.name, "body": path.read_text(encoding="utf-8")})


def build_bundle_manifest(
    root: Path,
    *,
    file_hashes: dict[str, str],
    attestation_hash: str,
) -> dict[str, Any]:
    components = {
        "archovive-cli": "console: archovive-cli — full product surface",
        "archovive-core": "console: archovive-core — L1 hermetic truth",
        "archovive-runtime": "console: archovive-runtime — L2 operational truth",
        "archovive-audit": "console: archovive-audit — L3 governance truth",
        "archovive-health": "console: archovive-health — Health Certificate v2",
        "archovive-spec": "console: archovive-spec — PIPE v4 SPEC utility",
        "archovive-attestation": "console: archovive-attestation — attest export",
    }
    manifest: dict[str, Any] = {
        "schema_version": BUNDLE_MANIFEST_SCHEMA,
        "product_version": PRODUCT_VERSION,
        "components": components,
        "artifacts": sorted(file_hashes.keys()),
        "artifact_hashes": file_hashes,
        "attestation_hash": attestation_hash,
    }
    manifest["bundle_hash"] = core.stable_hash_v3(
        {k: v for k, v in manifest.items() if k != "bundle_hash"}
    )
    return manifest


def write_sovereign_kit(
    out_dir: Path,
    *,
    attestation: dict[str, Any],
    audit_result: dict[str, Any],
    health_certificate: dict[str, Any],
    spec_doc: dict[str, Any],
) -> dict[str, Any]:
    """Write full sovereign kit directory; returns manifest + paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    file_hashes: dict[str, str] = {}

    attest_path = out_dir / "attest.json"
    attest_path.write_text(json.dumps(attestation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    file_hashes["attest.json"] = _file_hash(attest_path)

    hc_path = out_dir / "health_certificate_v2.json"
    hc_path.write_text(json.dumps(health_certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    file_hashes["health_certificate_v2.json"] = _file_hash(hc_path)

    spec_path = out_dir / "spec_v4.json"
    spec_path.write_text(json.dumps(spec_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    file_hashes["spec_v4.json"] = _file_hash(spec_path)

    ledger_src = audit_result.get("audit_ledger", {}).get("ledger_path")
    ledger_path = out_dir / "ledger.jsonl"
    if ledger_src and Path(ledger_src).exists():
        shutil.copy2(ledger_src, ledger_path)
    else:
        ledger_path.write_text("", encoding="utf-8")
    if ledger_path.exists() and ledger_path.stat().st_size:
        file_hashes["ledger.jsonl"] = core.stable_hash_v3({"ledger": ledger_path.read_text(encoding="utf-8")})

    zkap = (audit_result.get("level2") or {}).get("zkap") or {}
    zkap_path = out_dir / "zkap_attestation.json"
    zkap_path.write_text(json.dumps(zkap, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    file_hashes["zkap_attestation.json"] = _file_hash(zkap_path)

    kit_ctx = load_kit_context(out_dir, attestation, verify_replay=True)
    summary_md = out_dir / "attest.md"
    summary_md.write_text(render_attestation_markdown(attestation, kit_ctx=kit_ctx), encoding="utf-8")
    file_hashes["attest.md"] = _file_hash(summary_md)

    export = run_attestation_export(
        attest_path,
        write_pdf=True,
        md_only=False,
        verify_replay=False,
    )
    if export.pdf_hash:
        file_hashes["attest.pdf"] = export.pdf_hash

    manifest = build_bundle_manifest(
        out_dir,
        file_hashes=file_hashes,
        attestation_hash=str(attestation.get("attestation_hash", "")),
    )
    manifest_path = out_dir / "BUNDLE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for name, desc in manifest["components"].items():
        comp_dir = out_dir / name
        comp_dir.mkdir(exist_ok=True)
        (comp_dir / "README.txt").write_text(f"{desc}\n", encoding="utf-8")

    return {"manifest": manifest, "manifest_path": str(manifest_path), "artifacts": file_hashes}
