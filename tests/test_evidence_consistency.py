"""Evidence artifacts must be pure kernel serializations — no surface enrichment."""
from __future__ import annotations

from tests._contract_helpers import (
    attestation_from_decision_record,
    decision_record_from_result,
    drift_matrix_from_decision_record,
    execute_kernel_job,
    repro_from_decision_record,
    validate_repro,
)


def _kernel_record(demo_job):
    return decision_record_from_result(execute_kernel_job(demo_job))


def test_repro_is_pure_kernel_serialization(demo_job):
    record = _kernel_record(demo_job)
    repro = repro_from_decision_record(record)

    assert repro["replay_hash"] == record["replay_hash"]
    assert repro["graph_hash"] == record["graph_hash"]
    assert repro["verdict"] == record["verdict"]
    assert repro["exit_code"] == record["exit_code"]
    assert repro["policy_results"] == record["policy_results"]
    assert repro["metrics"] == record["metrics"]
    assert repro["drift_matrix"] == record["drift_matrix"]


def test_repro_has_no_enrichment_fields(demo_job):
    repro = repro_from_decision_record(_kernel_record(demo_job))
    forbidden = {"gate_header", "tty_lines", "ci_runner", "mcp_session", "tier", "attestation_signature"}
    assert forbidden.isdisjoint(repro.keys())


def test_drift_matrix_is_kernel_object_only(demo_job):
    record = _kernel_record(demo_job)
    drift = drift_matrix_from_decision_record(record)

    assert drift == record["drift_matrix"]
    assert drift["schema_version"] == "drift_matrix_v1"


def test_drift_matrix_not_independently_computed(demo_job):
    """drift_matrix.json must equal DecisionRecord.drift_matrix — no external derivation."""
    record = _kernel_record(demo_job)
    drift_a = drift_matrix_from_decision_record(record)
    drift_b = dict(record["drift_matrix"])
    assert drift_a == drift_b


def test_attestation_derived_only_from_decision_record(demo_job):
    record = _kernel_record(demo_job)
    attestation = attestation_from_decision_record(record)

    assert attestation["H_verdict"] == record["replay_hash"]
    assert attestation["graph_hash"] == record["graph_hash"]
    assert attestation["verdict"] == record["verdict"]
    assert attestation["policy_results"] == record["policy_results"]

    # No fields outside kernel-derived set (except schema_id test marker)
    allowed = {"schema_id", "H_verdict", "graph_hash", "verdict", "exit_code", "policy_results"}
    assert set(attestation.keys()) <= allowed


def test_repro_validates_against_schema(demo_job):
    repro = repro_from_decision_record(_kernel_record(demo_job))
    validate_repro(repro)
