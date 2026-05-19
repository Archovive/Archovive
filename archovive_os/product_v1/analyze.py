"""
Archovive v1 analyze — L1 + L2 + L3 → sovereign attestation package.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from archovive_os.product_v1._core import core
from archovive_os.product_v1.bootstrap import run_sovereign_bootstrap
from archovive_os.product_v1.bundle import write_sovereign_kit
from archovive_os.product_v1.constants import (
    ATTESTATION_SCHEMA,
    DEFAULT_AUDIT_INPUT,
    DEFAULT_COMPLIANCE_PACK,
    PRODUCT_VERSION,
)


def resolve_target(target: str, *, stdin_bytes: bytes | None = None) -> tuple[str, bytes]:
    """
    Resolve CLI target to (repo, input_stream).

    - Path ending in .json → file as audit input; repo synthetic://analyze-<hash>
    - Directory or synthetic:// → repo target; input from file or default/stdin
    """
    p = Path(target)
    if p.is_file() and p.suffix.lower() == ".json":
        data = p.read_bytes()
        repo = f"synthetic://analyze-{core.stable_hash_v3({'file': str(p.resolve())})[:16]}"
        return repo, data
    repo = target if str(target).startswith("synthetic://") else str(p.resolve())
    if stdin_bytes:
        return repo, stdin_bytes
    if p.is_dir():
        candidate = p / "audit_input.json"
        if candidate.exists():
            return repo, candidate.read_bytes()
    return repo, DEFAULT_AUDIT_INPUT


def build_attestation(
    audit_result: dict[str, Any],
    *,
    repo: str,
    bootstrap: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compose v1 attestation JSON from L3 response (includes L2 + L1)."""
    l1 = audit_result.get("level2", {}).get("level1", {})
    l2 = audit_result.get("level2", {})
    proof_v7 = l1.get("proof_v7") or l2.get("proof_v7") or {}
    proof_v8 = audit_result.get("proof_v8") or {}
    trust = audit_result.get("trust_metadata") or {}
    reg = next(
        (s for s in (audit_result.get("audit_validation") or {}).get("stages", []) if s.get("stage") == "regulatory"),
        {},
    )
    control_hashes = [
        {
            "pack": v.get("pack"),
            "control_id": v.get("control_id"),
            "passed": v.get("passed"),
            "control_verdict_hash": v.get("control_verdict_hash"),
        }
        for v in reg.get("control_verdicts", [])
    ]
    attestation: dict[str, Any] = {
        "schema_version": ATTESTATION_SCHEMA,
        "product_version": PRODUCT_VERSION,
        "pipe_release": core.PIPE_V4_RELEASE,
        "contract_label": core.CONTRACT_LABEL,
        "repo": repo,
        "verdict": audit_result.get("verdict"),
        "success": audit_result.get("success"),
        "trust_surface": {
            "H_input": proof_v7.get("H_input"),
            "H_triangulation": proof_v7.get("H_triangulation"),
            "H_verdict": proof_v7.get("H_verdict"),
            "lineage_hash_l1": proof_v7.get("lineage_hash"),
            "lineage_hash_l3": proof_v8.get("lineage_hash"),
            "record_hash": (l1.get("ingestion_record") or {}).get("record_hash"),
            "audit_chain_root": proof_v8.get("audit_chain_root"),
            "audit_record_hash": (audit_result.get("audit_record") or {}).get("audit_record_hash"),
            "ledger_binding_hash": proof_v7.get("ledger_binding_hash"),
            "epoch_binding_hash": proof_v8.get("epoch_binding_hash") or trust.get("epoch_binding_hash"),
            "hypervisor_binding_hash": trust.get("hypervisor_binding_hash")
            or (l2.get("hypervisor_state") or {}).get("binding_hash"),
            "epoch_id": trust.get("epoch_id"),
            "determinism_scope": trust.get("determinism_scope"),
            "control_verdict_hashes": control_hashes,
        },
        "compat_metadata": l1.get("compat_metadata"),
        "bootstrap_verified": bool((bootstrap or {}).get("verified"))
        or ((bootstrap or {}).get("status") == "PASS"),
    }
    attestation["attestation_hash"] = core.stable_hash_v3(
        {k: v for k, v in attestation.items() if k != "attestation_hash"}
    )
    return attestation


def run_analyze(
    target: str,
    *,
    out_path: str | Path | None = None,
    package_dir: str | Path | None = None,
    tenant_id: str = "default",
    compliance_pack: str = DEFAULT_COMPLIANCE_PACK,
    epoch_id: str | None = None,
    stdin_bytes: bytes | None = None,
    skip_bootstrap: bool = False,
    bootstrap_root: Path | None = None,
) -> dict[str, Any]:
    """
    Run full L1→L2→L3 truth stack and emit attestation (+ optional sovereign kit directory).
    """
    repo, input_bytes = resolve_target(target, stdin_bytes=stdin_bytes)
    eid = core.resolve_epoch_id(epoch_id)
    pack_key = compliance_pack.split("-")[0] if compliance_pack else "DORA"

    bootstrap = None if skip_bootstrap else run_sovereign_bootstrap(repo, root=bootstrap_root)

    core.reset_runtime_ledger(repo, tenant_id)
    core.reset_audit_ledger(repo, tenant_id, pack_key)
    audit_result = core.run_audit_pipe(
        repo,
        input_bytes,
        tenant_id=tenant_id,
        compliance_pack=compliance_pack,
        canonical=True,
        epoch_id=eid,
    )
    attestation = build_attestation(audit_result, repo=repo, bootstrap=bootstrap)

    spec_doc = core.generate_pipe_v4_spec_document()
    integrity = core.run_pipe_integrity_check(repo, epoch_id=eid, integrity_mode="synthetic")
    health = core.build_health_certificate(integrity)

    result: dict[str, Any] = {
        "attestation": attestation,
        "audit_response": audit_result,
        "bootstrap": bootstrap,
        "health_certificate": health,
        "spec": {"spec_hash": core.spec_document_hash(spec_doc), "document": spec_doc},
    }

    if out_path:
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(attestation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        result["attest_path"] = str(path.resolve())

    if package_dir:
        kit = write_sovereign_kit(
            Path(package_dir),
            attestation=attestation,
            audit_result=audit_result,
            health_certificate=health,
            spec_doc=spec_doc,
        )
        result["package_dir"] = str(Path(package_dir).resolve())
        result["bundle_manifest"] = kit["manifest"]

    return result
