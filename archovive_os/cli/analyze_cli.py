"""CLI for `archovive analyze` — Archovive v1 product surface."""
from __future__ import annotations

import sys

from archovive_os.product_v1.analyze import run_analyze
from archovive_os.product_v1.bootstrap import format_bootstrap_tty


def run_analyze_cli(
    target: str,
    *,
    out: str,
    package_dir: str | None = None,
    tenant_id: str = "default",
    compliance_pack: str = "DORA-2026",
    epoch_id: str | None = None,
    human: bool = True,
    skip_bootstrap: bool = False,
) -> int:
    result = run_analyze(
        target,
        out_path=out,
        package_dir=package_dir,
        tenant_id=tenant_id,
        compliance_pack=compliance_pack,
        epoch_id=epoch_id,
        skip_bootstrap=skip_bootstrap,
    )
    boot = result.get("bootstrap") or {}
    if human and sys.stdout.isatty() and not skip_bootstrap:
        br = boot.get("bootstrap_result")
        lines = format_bootstrap_tty(br) if br else boot.get("banner", [])
        for line in lines:
            print(line)
        if boot and not boot.get("verified"):
            print("Bootstrap failed — analyze completed with recorded bootstrap state.", file=sys.stderr)
    att = result["attestation"]
    if human:
        ts = att.get("trust_surface", {})
        print("")
        print("=== [ARCHOVIVE v1] Attestation complete ===")
        print(f"Verdict: {att.get('verdict')}")
        print(f"Output: {result.get('attest_path', out)}")
        if package_dir:
            print(f"Package: {result.get('package_dir')}")
            print(f"bundle_hash: {str((result.get('bundle_manifest') or {}).get('bundle_hash', ''))[:32]}…")
        print("")
        print("Trust surface (prefixes):")
        for key in (
            "H_input",
            "H_triangulation",
            "H_verdict",
            "audit_chain_root",
            "epoch_binding_hash",
            "hypervisor_binding_hash",
        ):
            val = str(ts.get(key, ""))
            print(f"  {key}: {val[:32]}…" if val else f"  {key}: (none)")
        failed = [c for c in ts.get("control_verdict_hashes", []) if not c.get("passed")]
        if failed:
            print(f"  control_verdict_hash (failed): {failed[0].get('control_verdict_hash', '')[:32]}…")
    return 0 if att.get("success") is not False else 1
