"""
Deterministic Governance Parity Proof (DGPP) — executive-grade cross-surface proof.

Proves CLI, CI, and MCP projections yield identical kernel truth for a canonical
deterministic job envelope. Does not modify runtime behavior.
"""
from __future__ import annotations

import io
import json
from contextlib import redirect_stdout

import pytest

from simulate.runner import run_simulate_cli

from tests._contract_helpers import (
    assert_dgpp_pinned_hashes,
    ci_projection_json,
    cli_projection_json,
    extract_dgpp_artifacts,
    mcp_projection_json,
)


def _cli_surface_artifacts(dgpp_job, repo_root) -> dict[str, str]:
    """CLI simulate — programmatic invocation with --json capture."""
    demo_rel = "examples/demo-fintech"
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = run_simulate_cli(["--json", "--repo", demo_rel], ci_mode=False)
    assert code == 0
    record = json.loads(buf.getvalue())
    return extract_dgpp_artifacts(record)


def _ci_surface_artifacts(dgpp_job, repo_root) -> dict[str, str]:
    """CI check — same kernel path; enforcement projection with --json capture."""
    demo_rel = "examples/demo-fintech"
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = run_simulate_cli(["--json", "--repo", demo_rel], ci_mode=True)
    assert code == 2
    record = json.loads(buf.getvalue())
    return extract_dgpp_artifacts(record)


def _mcp_surface_artifacts(dgpp_job) -> dict[str, str]:
    """MCP run_analysis — query projection (kernel-equivalent tool JSON in OSS)."""
    record = mcp_projection_json(dgpp_job)
    return extract_dgpp_artifacts(record)


def _fail_dgpp_divergence(baseline: str, name: str, field: str, expected: str, actual: str) -> None:
    pytest.fail(
        f"\nDGPP GOVERNANCE PARITY VIOLATION\n"
        f"  Surface: {name}\n"
        f"  Field:   {field}\n"
        f"  Baseline ({baseline}): {expected}\n"
        f"  Actual:   {actual}\n"
        f"CLI == CI == MCP invariant broken.\n"
    )


def test_dgpp_governance_parity_proof(dgpp_job, repo_root):
    """
    Flagship DGPP proof: identical kernel hashes across CLI, CI, and MCP surfaces.

    Canonical job: fixed commit_ref fixture, demo-fintech graph, DORA_2026 policy pack set.
    """
    surfaces = {
        "CLI": _cli_surface_artifacts(dgpp_job, repo_root),
        "CI": _ci_surface_artifacts(dgpp_job, repo_root),
        "MCP": _mcp_surface_artifacts(dgpp_job),
    }

    baseline_name = "CLI"
    baseline = surfaces[baseline_name]

    assert_dgpp_pinned_hashes(baseline)

    parity_fields = (
        "graph_hash",
        "replay_hash",
        "decision_record_hash",
        "policy_results_checksum",
    )

    for name, artifacts in surfaces.items():
        for field in parity_fields:
            if artifacts[field] != baseline[field]:
                _fail_dgpp_divergence(baseline_name, name, field, baseline[field], artifacts[field])

    # Internal projection paths must agree with subprocess-captured CLI/CI outputs.
    internal_cli = extract_dgpp_artifacts(cli_projection_json(dgpp_job))
    internal_ci = extract_dgpp_artifacts(ci_projection_json(dgpp_job))
    for label, internal in (("CLI-internal", internal_cli), ("CI-internal", internal_ci)):
        for field in parity_fields:
            if internal[field] != baseline[field]:
                _fail_dgpp_divergence(baseline_name, label, field, baseline[field], internal[field])


def test_dgpp_all_surfaces_pass_status(dgpp_job, repo_root):
    """Executive status gate: all surfaces PASS when parity holds."""
    artifacts = {
        "CLI": _cli_surface_artifacts(dgpp_job, repo_root),
        "CI": _ci_surface_artifacts(dgpp_job, repo_root),
        "MCP": _mcp_surface_artifacts(dgpp_job),
    }
    ref = artifacts["CLI"]["replay_hash"]
    for name, art in artifacts.items():
        assert art["replay_hash"] == ref, f"DGPP FAIL: {name}"


# Pinned executive readout values (demo-fintech @ v5.1.0) — must match specs/08_dgpp_parity_proof.md
DGPP_PINNED_DECISION_RECORD_HASH = "13e91e402af6678db7c88b44339d14c811affbacf5d55f2451d45c16df6d29af"
DGPP_PINNED_POLICY_CHECKSUM = "3063ddfce81e7298ad957dd9a01911e97089ed35c5ab10624e2c2f0c6f418b11"


def test_dgpp_executive_report_hash_pins(dgpp_job, repo_root):
    """Keep executive artifact synchronized with computed DGPP proof values."""
    cli = _cli_surface_artifacts(dgpp_job, repo_root)
    assert cli["decision_record_hash"] == DGPP_PINNED_DECISION_RECORD_HASH
    assert cli["policy_results_checksum"] == DGPP_PINNED_POLICY_CHECKSUM
