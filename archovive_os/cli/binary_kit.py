"""
Archovive v1 — Multi-Binary Kit mode registry and branding.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Literal

import archovive_core.api as core
from archovive_os.product_v1.constants import PRODUCT_VERSION

BinaryModeName = Literal[
    "cli",
    "core",
    "runtime",
    "audit",
    "health",
    "spec",
    "attestation",
]


@dataclass(frozen=True)
class BinaryIdentity:
    prog: str
    banner: str
    tagline: str


IDENTITIES: dict[BinaryModeName, BinaryIdentity] = {
    "cli": BinaryIdentity(
        prog="archovive-cli",
        banner="[ARCHOVIVE CLI] Sovereign Architecture Truth System v1",
        tagline="Full product surface — bootstrap, simulate, analyze, attestation",
    ),
    "core": BinaryIdentity(
        prog="archovive-core",
        banner="[ARCHOVIVE CORE] Hermetic Truth Engine v1",
        tagline="L1 ingestion — deterministic architecture truth",
    ),
    "runtime": BinaryIdentity(
        prog="archovive-runtime",
        banner="[ARCHOVIVE RUNTIME] Sovereign Runtime Engine v1",
        tagline="L2 operational truth — ledger, hypervisor, ZKAP",
    ),
    "audit": BinaryIdentity(
        prog="archovive-audit",
        banner="[ARCHOVIVE AUDIT] Governance Layer v1",
        tagline="L3 regulatory truth — proof bundles, control verdicts",
    ),
    "health": BinaryIdentity(
        prog="archovive-health",
        banner="[ARCHOVIVE HEALTH] Health Certificate v2",
        tagline="TÜV seal — integrity and certificate verification",
    ),
    "spec": BinaryIdentity(
        prog="archovive-spec",
        banner="[ARCHOVIVE SPEC] SPEC v4 Hash Utility",
        tagline="Normative constitution — PIPE v4 specification",
    ),
    "attestation": BinaryIdentity(
        prog="archovive-attestation",
        banner="[ARCHOVIVE ATTESTATION] Sovereign Attestation Export v1",
        tagline="Auditor-facing attest.md / attest.pdf packages",
    ),
}


def print_binary_banner(mode: BinaryModeName, *, force: bool = False) -> None:
    if not force and not sys.stdout.isatty():
        return
    ident = IDENTITIES[mode]
    print(ident.banner)
    print(ident.tagline)
    print(f"pipe_release={core.PIPE_V4_RELEASE} contract={core.CONTRACT_LABEL}")
    print()


def version_payload(mode: BinaryModeName) -> dict[str, str]:
    return {
        "binary": IDENTITIES[mode].prog,
        "product_version": PRODUCT_VERSION,
        "pipe_release": core.PIPE_V4_RELEASE,
        "contract_label": core.CONTRACT_LABEL,
        "engine_version": core.ENGINE_CONTRACT_VERSION,
        "runtime_version": core.RUNTIME_PIPE_VERSION,
        "audit_version": core.AUDIT_PIPE_VERSION,
        "layer": {
            "cli": "product",
            "core": "L1",
            "runtime": "L2",
            "audit": "L3",
            "health": "health_certificate_v2",
            "spec": "PIPE_V4_SPEC",
            "attestation": "attestation_export",
        }.get(mode, mode),
    }


def emit_version(mode: BinaryModeName, *, json_out: bool = False) -> int:
    payload = version_payload(mode)
    if json_out:
        print(json.dumps(payload, separators=(",", ":")))
    else:
        print_binary_banner(mode, force=True)
        for key, val in payload.items():
            if key != "layer":
                print(f"  {key}: {val}")
    return 0
