"""Test-only kernel contract helpers — not imported by runtime paths."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from simulate.engine import AnalysisResult, analyze_repo

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"

FORBIDDEN_KERNEL_JOB_KEYS = frozenset(
    {
        "tier",
        "surface",
        "cli_format",
        "tty",
        "process_exit",
        "mcp_tool",
        "license_tier",
        "product_tier",
    }
)

FORBIDDEN_DECISION_RECORD_KEYS = frozenset(
    {
        "gate_header",
        "tty_lines",
        "tier",
        "surface",
        "mcp_tool",
        "process_exit_override",
    }
)


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def canonical_demo_job(repo_root: Path) -> dict[str, Any]:
    demo = repo_root / "examples" / "demo-fintech"
    return {
        "schema_id": "archovive_kernel_job_v1",
        "repo_path": str(demo.resolve()),
        "repo_name": "demo-fintech",
        "commit_ref": None,
        "policy_pack_ids": ["GLOBAL_BASE", "DORA_2026", "NIS2_MINIMAL_V1"],
        "mode": "analyze",
        "baseline_ref": None,
    }


def validate_kernel_job(envelope: dict[str, Any]) -> None:
    schema = load_schema("kernel_job.json")
    assert envelope.get("schema_id") == schema["properties"]["schema_id"]["const"]
    for key in schema["required"]:
        assert key in envelope, f"missing required kernel job field: {key}"
    for forbidden in FORBIDDEN_KERNEL_JOB_KEYS:
        assert forbidden not in envelope, f"forbidden kernel job field: {forbidden}"
    assert envelope["mode"] == "analyze"


def execute_kernel_job(envelope: dict[str, Any]) -> AnalysisResult:
    """Pure kernel invocation f(job) — mirrors analyze_repo entry, no surface logic."""
    validate_kernel_job(envelope)
    return analyze_repo(
        Path(envelope["repo_path"]).resolve(),
        repo_name=envelope["repo_name"],
    )


def decision_record_from_result(result: AnalysisResult) -> dict[str, Any]:
    """Normalize AnalysisResult to contract DecisionRecord (kernel fields only)."""
    record = json.loads(result.to_json())
    record["schema_id"] = "archovive_decision_record_v1"
    return record


def normalize_decision_record(record: dict[str, Any]) -> dict[str, Any]:
    """Stable comparison view — excludes surface-only and contract-validation keys."""
    record = {k: v for k, v in record.items() if k != "schema_id"}
    allowed = {
        "archovive_version",
        "repo",
        "verdict",
        "exit_code",
        "graph_hash",
        "replay_hash",
        "metrics",
        "policy_results",
        "drift_matrix",
    }
    out = {k: record[k] for k in sorted(record) if k in allowed}
    for forbidden in FORBIDDEN_DECISION_RECORD_KEYS:
        assert forbidden not in record
    return out


def validate_decision_record(record: dict[str, Any]) -> None:
    schema = load_schema("decision_record.json")
    assert record.get("schema_id") == schema["properties"]["schema_id"]["const"]
    for key in schema["required"]:
        assert key in record, f"missing DecisionRecord field: {key}"
    for forbidden in FORBIDDEN_DECISION_RECORD_KEYS:
        assert forbidden not in record
    assert len(record["graph_hash"]) == 64
    assert len(record["replay_hash"]) == 64


def repro_from_decision_record(record: dict[str, Any]) -> dict[str, Any]:
    """Build repro.json as pure kernel-field serialization (no enrichment)."""
    repro = {
        "schema_id": "archovive_repro_v1",
        "replay_hash": record["replay_hash"],
        "graph_hash": record["graph_hash"],
        "verdict": record["verdict"],
        "exit_code": record["exit_code"],
        "repo": record["repo"],
        "commit_ref": None,
        "archovive_version": record["archovive_version"],
        "policy_results": record["policy_results"],
        "metrics": record["metrics"],
        "drift_matrix": record["drift_matrix"],
    }
    validate_repro(repro)
    return repro


def validate_repro(repro: dict[str, Any]) -> None:
    schema = load_schema("repro.json")
    assert repro.get("schema_id") == schema["properties"]["schema_id"]["const"]
    for key in schema["required"]:
        assert key in repro, f"missing repro field: {key}"
    forbidden = {"gate_header", "tty_lines", "ci_runner", "mcp_session", "tier", "attestation_signature"}
    for key in forbidden:
        assert key not in repro


def drift_matrix_from_decision_record(record: dict[str, Any]) -> dict[str, Any]:
    """drift_matrix.json is the kernel drift_matrix object — no derivation layer."""
    return dict(record["drift_matrix"])


def attestation_from_decision_record(record: dict[str, Any]) -> dict[str, Any]:
    """Minimal attestation view derived ONLY from DecisionRecord kernel fields."""
    return {
        "schema_id": "archovive_attestation_v1_test",
        "H_verdict": record["replay_hash"],
        "graph_hash": record["graph_hash"],
        "verdict": record["verdict"],
        "exit_code": record["exit_code"],
        "policy_results": record["policy_results"],
    }


def cli_projection_json(job: dict[str, Any]) -> dict[str, Any]:
    """CLI --json projection: kernel execute + to_json (execution surface)."""
    result = execute_kernel_job(job)
    return json.loads(result.to_json())


def ci_projection_json(job: dict[str, Any]) -> dict[str, Any]:
    """CI surface uses identical kernel invocation; differs only in process exit propagation."""
    result = execute_kernel_job(job)
    return json.loads(result.to_json())


def mcp_projection_json(job: dict[str, Any]) -> dict[str, Any]:
    """MCP run_analysis projection: kernel DecisionRecord as tool JSON (query surface)."""
    result = execute_kernel_job(job)
    return json.loads(result.to_json())
