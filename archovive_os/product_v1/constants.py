"""Archovive v1 product constants (non-contract)."""
from __future__ import annotations

PRODUCT_VERSION = "archovive_v1"
PRODUCT_LABEL = "Archovive v1 — Architecture Truth System"
ATTESTATION_SCHEMA = "archovive_attestation_v1"
BUNDLE_MANIFEST_SCHEMA = "archovive_bundle_manifest_v1"
DEFAULT_COMPLIANCE_PACK = "DORA-2026"
DEFAULT_AUDIT_INPUT = (
    b'{"audit_kind":"dora_report","pack":"DORA","ics_controls":["ICS-01"],'
    b'"framework":"DORA"}'
)
