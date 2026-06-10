"""Surface parity: CLI, CI, and MCP projections must expose identical kernel truth."""
from __future__ import annotations

import io
import json
from contextlib import redirect_stdout

from simulate.runner import run_simulate_cli

from tests._contract_helpers import (
    ci_projection_json,
    cli_projection_json,
    decision_record_from_result,
    execute_kernel_job,
    mcp_projection_json,
    normalize_decision_record,
    validate_decision_record,
)


def test_cli_ci_mcp_replay_hash_parity(demo_job):
    cli = normalize_decision_record(cli_projection_json(demo_job))
    ci = normalize_decision_record(ci_projection_json(demo_job))
    mcp = normalize_decision_record(mcp_projection_json(demo_job))

    assert cli["replay_hash"] == ci["replay_hash"] == mcp["replay_hash"]
    assert cli["graph_hash"] == ci["graph_hash"] == mcp["graph_hash"]


def test_cli_ci_mcp_decision_record_equivalence(demo_job):
    cli = normalize_decision_record(cli_projection_json(demo_job))
    ci = normalize_decision_record(ci_projection_json(demo_job))
    mcp = normalize_decision_record(mcp_projection_json(demo_job))

    assert cli == ci == mcp


def test_kernel_direct_matches_all_projections(demo_job):
    result = execute_kernel_job(demo_job)
    kernel = normalize_decision_record(decision_record_from_result(result))

    for projection in (cli_projection_json, ci_projection_json, mcp_projection_json):
        surface = normalize_decision_record(projection(demo_job))
        assert surface == kernel


def test_cli_json_stdout_matches_kernel(demo_job, repo_root):
    """CLI --json path must not enrich DecisionRecord beyond kernel output."""
    demo_rel = "examples/demo-fintech"
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = run_simulate_cli(["--json", "--repo", demo_rel], ci_mode=False)
    assert code == 0

    cli_stdout = normalize_decision_record(json.loads(buf.getvalue()))
    kernel = normalize_decision_record(decision_record_from_result(execute_kernel_job(demo_job)))

    assert cli_stdout == kernel


def test_ci_json_stdout_matches_kernel(demo_job, repo_root):
    """CI path kernel JSON identical to CLI; only process exit differs."""
    demo_rel = "examples/demo-fintech"
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = run_simulate_cli(["--json", "--repo", demo_rel], ci_mode=True)
    assert code == 2  # kernel exit_code propagated in CI mode

    ci_stdout = normalize_decision_record(json.loads(buf.getvalue()))
    kernel = normalize_decision_record(decision_record_from_result(execute_kernel_job(demo_job)))

    assert ci_stdout == kernel


def test_decision_record_validates_against_contract(demo_job):
    record = decision_record_from_result(execute_kernel_job(demo_job))
    validate_decision_record(record)


def test_surface_only_difference_is_ci_process_exit(demo_job, repo_root):
    """Parity exception: CI propagates exit_code to process; CLI funnel returns 0."""
    demo_rel = "examples/demo-fintech"
    with redirect_stdout(io.StringIO()):
        cli_code = run_simulate_cli(["--repo", demo_rel], ci_mode=False)
        ci_code = run_simulate_cli(["--repo", demo_rel], ci_mode=True)

    assert cli_code == 0
    assert ci_code == 2
    # DecisionRecord.exit_code identical on both paths (verified above); only process exit differs.
