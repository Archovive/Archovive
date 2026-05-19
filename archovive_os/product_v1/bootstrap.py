"""
Sovereign bootstrap — SPEC, Health Certificate, bindings, identity stability.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from archovive_os.product_v1._core import core
from archovive_os.product_v1.spec_ref import SPEC_V4_HASH

Status = Literal["PASS", "FAIL"]

DEFAULT_BOOTSTRAP_REPO = "synthetic://sovereign-bootstrap"


@dataclass
class BootstrapResult:
    status: Status
    spec_hash: str
    spec_verified: bool
    health_verified: bool
    epoch_binding_verified: bool
    hypervisor_binding_verified: bool
    identity_hash_stability_verified: bool
    errors: list[str] = field(default_factory=list)
    pipe_release: str = core.PIPE_V4_RELEASE
    integrity_mode: str = "full"
    repo: str = DEFAULT_BOOTSTRAP_REPO

    def to_json(self) -> str:
        return json.dumps(
            {
                "status": self.status,
                "pipe_release": self.pipe_release,
                "repo": self.repo,
                "integrity_mode": self.integrity_mode,
                "spec_hash": self.spec_hash,
                "spec_verified": self.spec_verified,
                "health_verified": self.health_verified,
                "epoch_binding_verified": self.epoch_binding_verified,
                "hypervisor_binding_verified": self.hypervisor_binding_verified,
                "identity_hash_stability_verified": self.identity_hash_stability_verified,
                "errors": self.errors,
            },
            separators=(",", ":"),
        )

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.to_json())


def _load_spec_hash(spec_path: Path | None) -> tuple[str, bool, str | None]:
    reference = SPEC_V4_HASH
    if spec_path is None or not spec_path.exists():
        return reference, True, None
    try:
        doc = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return reference, False, f"SPEC file invalid: {spec_path} ({exc})"
    file_hash = core.spec_document_hash(doc)
    if file_hash != reference:
        return file_hash, False, f"SPEC hash mismatch (got {file_hash[:16]}…, expected {reference[:16]}…)"
    return file_hash, True, None


def _check_health_certificate_file(
    path: Path | None,
    *,
    reference_spec_hash: str,
    expected_cert: dict[str, Any] | None,
) -> tuple[bool, str | None]:
    if path is None or not path.exists():
        if expected_cert and expected_cert.get("status") == "VALID":
            return True, None
        return False, "Health certificate not found (run integrity or provide health_certificate_v2.json)"
    try:
        cert = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"Health certificate invalid: {path} ({exc})"
    if cert.get("certificate_version") != core.HEALTH_CERTIFICATE_VERSION:
        return False, f"Unexpected certificate_version: {cert.get('certificate_version')}"
    if cert.get("status") != "VALID":
        return False, f"Health certificate status: {cert.get('status')}"
    if cert.get("spec_hash") != reference_spec_hash:
        return False, "Health certificate spec_hash mismatch"
    if expected_cert and cert.get("integrity_hash") != expected_cert.get("integrity_hash"):
        return False, "Health certificate integrity_hash stale (re-run bootstrap)"
    return True, None


def _check_epoch_binding(integrity: dict[str, Any]) -> tuple[bool, str | None]:
    failures = integrity.get("failures") or {}
    if failures.get("invariants"):
        l2 = (integrity.get("details") or {}).get("L2", {})
        l3 = (integrity.get("details") or {}).get("L3", {})
        if "epoch_binding_hash mismatch" in str(l2.get("error", "")) + str(l3.get("error", "")):
            return False, "Epoch binding invariant failed"
    epoch_hash = integrity.get("epoch_binding_hash")
    if not epoch_hash:
        return False, "epoch_binding_hash missing from integrity report"
    levels = integrity.get("levels") or {}
    if levels.get("L2") != "PASS" or levels.get("L3") != "PASS":
        return False, f"Epoch binding levels not PASS (L2={levels.get('L2')}, L3={levels.get('L3')})"
    return True, None


def _check_hypervisor_binding(integrity: dict[str, Any]) -> tuple[bool, str | None]:
    failures = integrity.get("failures") or {}
    if failures.get("invariants"):
        l2 = (integrity.get("details") or {}).get("L2", {})
        if l2.get("error"):
            return False, f"Hypervisor/L2 invariant: {l2.get('error')}"
    binding = integrity.get("hypervisor_binding_hash")
    runtime_mode = integrity.get("runtime_mode", "synthetic")
    if runtime_mode == "synthetic" and binding:
        return True, None
    if runtime_mode == "hypervisor" and binding:
        return True, None
    if integrity.get("integrity_mode") == "full":
        golden = integrity.get("golden") or []
        hv_fixtures = [g for g in golden if "hypervisor" in str(g.get("fixture", ""))]
        if hv_fixtures and all(g.get("match") for g in hv_fixtures):
            return True, None
    if binding:
        return True, None
    return False, "hypervisor_binding_hash missing or hypervisor golden replay failed"


def _check_identity_hash_stability(integrity: dict[str, Any]) -> tuple[bool, str | None]:
    failures = integrity.get("failures") or {}
    if failures.get("replay"):
        return False, f"Golden replay mismatch: {integrity.get('replay')}"
    if failures.get("self_ingestion"):
        return False, "Self-ingestion identity hash unstable"
    if integrity.get("replay") != "bit-identical":
        return False, f"Replay status: {integrity.get('replay')}"
    if not integrity.get("self_ingestion_stable"):
        return False, "self_ingestion_stable is false"
    return True, None


def run_bootstrap(
    spec_path: Path | None = None,
    health_cert_path: Path | None = None,
    *,
    repo: str = DEFAULT_BOOTSTRAP_REPO,
    integrity_mode: str = "full",
    epoch_id: str | None = None,
) -> BootstrapResult:
    """
    Run sovereign bootstrap checks against live integrity battery + optional on-disk artifacts.
    """
    errors: list[str] = []

    spec_hash, spec_file_ok, spec_err = _load_spec_hash(spec_path)
    if spec_err:
        errors.append(spec_err)

    integrity = core.run_pipe_integrity_check(repo, epoch_id=epoch_id, integrity_mode=integrity_mode)
    reference_spec = core.spec_document_hash(core.generate_pipe_v4_spec_document())
    spec_runtime_ok = integrity.get("spec_hash") == reference_spec
    if not spec_runtime_ok:
        errors.append(
            f"Runtime SPEC hash mismatch (integrity {str(integrity.get('spec_hash', ''))[:16]}…, "
            f"expected {reference_spec[:16]}…)"
        )
    spec_ok = spec_file_ok and spec_runtime_ok

    expected_cert = integrity.get("health_certificate") or core.build_health_certificate(integrity)
    health_ok, health_err = _check_health_certificate_file(
        health_cert_path,
        reference_spec_hash=reference_spec,
        expected_cert=expected_cert,
    )
    if not health_ok and integrity.get("integrity") == "PASS" and health_cert_path is None:
        health_ok = expected_cert.get("status") == "VALID"
    if health_err and not health_ok:
        errors.append(health_err)
    if integrity.get("integrity") != "PASS":
        errors.append(f"Integrity battery: {integrity.get('exit_code_name', 'FAIL')}")

    epoch_ok, epoch_err = _check_epoch_binding(integrity)
    if epoch_err:
        errors.append(epoch_err)

    hypervisor_ok, hypervisor_err = _check_hypervisor_binding(integrity)
    if hypervisor_err:
        errors.append(hypervisor_err)

    identity_ok, identity_err = _check_identity_hash_stability(integrity)
    if identity_err:
        errors.append(identity_err)

    all_ok = spec_ok and health_ok and epoch_ok and hypervisor_ok and identity_ok
    status: Status = "PASS" if all_ok else "FAIL"

    return BootstrapResult(
        status=status,
        spec_hash=spec_hash or reference_spec,
        spec_verified=spec_ok,
        health_verified=health_ok,
        epoch_binding_verified=epoch_ok,
        hypervisor_binding_verified=hypervisor_ok,
        identity_hash_stability_verified=identity_ok,
        errors=errors,
        pipe_release=core.PIPE_V4_RELEASE,
        integrity_mode=integrity_mode,
        repo=repo,
    )


def run_sovereign_bootstrap(
    repo: str = DEFAULT_BOOTSTRAP_REPO,
    *,
    root: Path | None = None,
    integrity_mode: str = "full",
) -> dict[str, Any]:
    """
    Legacy dict-shaped bootstrap report for analyze integration.
    """
    root = root or Path(".")
    result = run_bootstrap(
        spec_path=root / "spec_v4.json",
        health_cert_path=root / "health_certificate_v2.json",
        repo=repo,
        integrity_mode=integrity_mode,
    )
    lines = format_bootstrap_tty(result)
    return {
        "product_version": "archovive_v1",
        "verified": result.status == "PASS",
        "status": result.status,
        "banner": lines,
        "bootstrap_result": result,
        "spec_hash": result.spec_hash,
        "errors": result.errors,
    }


def format_bootstrap_tty(result: BootstrapResult) -> list[str]:
    """Step-by-step TTY lines ending with BOOTSTRAP status."""
    return [
        "=== [ARCHOVIVE v1] Sovereign Bootstrap ===",
        "",
        f"[1/5] SPEC v4 Hash .................. {'OK' if result.spec_verified else 'FAIL'}",
        f"[2/5] Health Certificate v2 ......... {'OK' if result.health_verified else 'FAIL'}",
        f"[3/5] Epoch Binding ................. {'OK' if result.epoch_binding_verified else 'FAIL'}",
        f"[4/5] Hypervisor Binding ............ {'OK' if result.hypervisor_binding_verified else 'FAIL'}",
        f"[5/5] Identity Hash Stability ....... {'OK' if result.identity_hash_stability_verified else 'FAIL'}",
        "",
        f"BOOTSTRAP: {result.status}",
    ]
