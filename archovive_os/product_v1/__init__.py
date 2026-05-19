"""
Archovive v1 — Sovereign Architecture Truth System (product surface).

Wraps frozen Pipe v4.0 L1/L2/L3 without altering identity hashes or proof semantics.
"""
from archovive_os.product_v1.analyze import build_attestation, run_analyze
from archovive_os.product_v1.bootstrap import (
    BootstrapResult,
    run_bootstrap,
    run_sovereign_bootstrap,
)
from archovive_os.product_v1.attestation_export import ExportResult, run_attestation_export
from archovive_os.product_v1.simulate import SimulateResult, run_simulate
from archovive_os.product_v1.spec_ref import SPEC_V4_HASH

__all__ = [
    "BootstrapResult",
    "ExportResult",
    "SimulateResult",
    "SPEC_V4_HASH",
    "build_attestation",
    "run_analyze",
    "run_bootstrap",
    "run_attestation_export",
    "run_simulate",
    "run_sovereign_bootstrap",
]
