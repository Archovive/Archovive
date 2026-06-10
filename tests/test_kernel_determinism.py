"""Kernel determinism: f(job) must be pure — identical outputs on repeated execution."""
from __future__ import annotations

import json

from tests._contract_helpers import (
    decision_record_from_result,
    execute_kernel_job,
    normalize_decision_record,
)


def test_kernel_ten_runs_identical_replay_hash(demo_job):
    hashes = [execute_kernel_job(demo_job).replay_hash for _ in range(10)]
    assert len(set(hashes)) == 1


def test_kernel_ten_runs_identical_graph_hash(demo_job):
    hashes = [execute_kernel_job(demo_job).graph_hash for _ in range(10)]
    assert len(set(hashes)) == 1


def test_kernel_ten_runs_byte_identical_json(demo_job):
    payloads = [execute_kernel_job(demo_job).to_json() for _ in range(10)]
    assert len(set(payloads)) == 1


def test_kernel_ten_runs_normalized_decision_record_identical(demo_job):
    records = [
        normalize_decision_record(decision_record_from_result(execute_kernel_job(demo_job)))
        for _ in range(10)
    ]
    assert records[0] == records[1] == records[-1]


def test_no_nondeterministic_fields_in_output(demo_job):
    """DecisionRecord must not contain timestamps, UUIDs, or runtime noise."""
    record = normalize_decision_record(decision_record_from_result(execute_kernel_job(demo_job)))
    blob = json.dumps(record, sort_keys=True)

    forbidden_substrings = ("timestamp", "uuid", "nanosecond", "random", "now()")
    for token in forbidden_substrings:
        assert token not in blob.lower()

    # Stable key set across runs
    keys_runs = [
        set(normalize_decision_record(decision_record_from_result(execute_kernel_job(demo_job))).keys())
        for _ in range(3)
    ]
    assert keys_runs[0] == keys_runs[1] == keys_runs[2]
