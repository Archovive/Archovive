"""
CLI output modes — SUMMARY (TTY), HUMAN (demos), JSON (CI/machines).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Literal

OutputMode = Literal["json", "summary", "human", "yaml"]

_RESET = "\033[0m"
_GREEN = "\033[32m"
_RED = "\033[31m"
_YELLOW = "\033[33m"
_CYAN = "\033[36m"
_DIM = "\033[2m"


def _color_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def _c(text: str, code: str) -> str:
    if not _color_enabled():
        return text
    return f"{code}{text}{_RESET}"


def decision_color(decision: str) -> str:
    d = (decision or "").upper()
    if d == "PASS":
        return _c(d, _GREEN)
    if d in ("FAIL", "BLOCK", "REJECT"):
        return _c(d, _RED)
    if d in ("WARN", "WARNING", "ADVISORY"):
        return _c(d, _YELLOW)
    return d


def resolve_output_mode(args: argparse.Namespace) -> OutputMode:
    """Pick output mode: CI/pipes → JSON; explicit flags override TTY default."""
    if getattr(args, "yaml", False):
        return "yaml"
    if getattr(args, "json", False):
        return "json"
    if not sys.stdout.isatty():
        return "json"
    if getattr(args, "human", False) or os.environ.get("ARCHOVIVE_HUMAN") == "1":
        return "human"
    if getattr(args, "summary", False):
        return "summary"
    return "summary"


def _short_hash(value: str | None, *, width: int = 12) -> str:
    if not value:
        return "—"
    s = str(value)
    if len(s) <= width:
        return s
    return f"{s[:width]}..."


def _data_blob(result: dict[str, Any]) -> dict[str, Any]:
    data = result.get("data")
    if isinstance(data, dict):
        return data
    return {}


def extract_summary_fields(
    result: dict[str, Any],
    *,
    target: str,
    elapsed_sec: float | None,
    tenant: str = "default",
) -> dict[str, Any]:
    """Flatten API response into summary-line fields."""
    data = _data_blob(result)
    proof = data.get("proof_v6") or data.get("proof") or data.get("proof_lineage") or {}
    if not isinstance(proof, dict):
        proof = {}

    decision = (
        data.get("decision")
        or data.get("fleet_status")
        or ("PASS" if data.get("passed") else None)
        or ("PASS" if int(result.get("status", 500)) < 400 else "FAIL")
    )

    violations = data.get("violation_count")
    if violations is None:
        raw_v = data.get("violations")
        if isinstance(raw_v, list):
            violations = len(raw_v)
        elif isinstance(raw_v, int):
            violations = raw_v
        else:
            violations = 0

    backend = (
        data.get("compile_backend")
        or proof.get("compile_backend")
        or os.environ.get("ARCHOVIVE_COMPILE", "runtime")
    )

    graph_id = data.get("graph_id") or proof.get("graph_id") or data.get("unification_hash")
    lineage = (
        proof.get("lineage_hash")
        or data.get("lineage_hash")
        or proof.get("unification_hash")
        or data.get("unification_hash")
    )

    return {
        "target": target,
        "decision": str(decision or "UNKNOWN"),
        "backend": str(backend),
        "violations": int(violations),
        "graph_id": _short_hash(graph_id),
        "lineage": _short_hash(lineage),
        "tenant": tenant,
        "elapsed_sec": elapsed_sec,
    }


def format_summary_lines(fields: dict[str, Any]) -> list[str]:
    """At most 8 lines — compact human digest."""
    decision = fields["decision"]
    backend = fields["backend"]
    elapsed = fields.get("elapsed_sec")
    time_s = f"{elapsed:.1f}s" if elapsed is not None else "—"

    lines = [
        "ARCHOVIVE OS v3 — SUMMARY MODE",
        f"Target: {fields['target']}",
        f"Decision: {decision_color(decision)}   ({backend})",
        f"Violations: {fields['violations']}",
        f"Graph ID: {fields['graph_id']}",
        f"Lineage: {fields['lineage']}",
        f"Tenant: {fields['tenant']}",
        f"Time: {time_s}",
    ]
    return lines[:8]


def print_summary(
    result: dict[str, Any],
    *,
    target: str,
    elapsed_sec: float | None = None,
    tenant: str = "default",
) -> None:
    fields = extract_summary_fields(
        result, target=target, elapsed_sec=elapsed_sec, tenant=tenant
    )
    for line in format_summary_lines(fields):
        print(line)


def print_human(
    result: dict[str, Any],
    *,
    target: str,
    elapsed_sec: float | None = None,
    tenant: str = "default",
) -> None:
    """Pretty context blocks + indented JSON payload."""
    data = _data_blob(result)
    proof = data.get("proof_v6") or data.get("proof") or {}
    if not isinstance(proof, dict):
        proof = {}

    decision = data.get("decision") or ("PASS" if data.get("passed") else "FAIL")
    backend = data.get("compile_backend") or proof.get("compile_backend") or "runtime"
    graph_id = data.get("graph_id") or proof.get("graph_id")
    nodes = data.get("node_count") or data.get("nodes")
    edges = data.get("edge_count") or data.get("edges")
    lineage = proof.get("lineage_hash") or data.get("lineage_hash")
    schema = proof.get("schema_version") or data.get("schema_version") or "archovive_os_3.0.0"
    elapsed = f"{elapsed_sec:.1f}s" if elapsed_sec is not None else "—"

    sep = "─" * 46
    print(_c("ARCHOVIVE OS v3 — HUMAN MODE", _CYAN))
    print(sep)
    print()
    print(_c("Target Repository:", _CYAN))
    print(f"  {target}")
    print()
    print(_c("Compile Backend:", _CYAN))
    print(f"  {backend}")
    print()
    print(_c("Decision:", _CYAN))
    print(f"  {decision_color(str(decision))}")
    print()
    print(_c("Graph:", _CYAN))
    print(f"  graph_id: {_short_hash(graph_id)}")
    if nodes is not None:
        print(f"  nodes: {nodes}")
    if edges is not None:
        print(f"  edges: {edges}")
    print()
    print(_c("Proof:", _CYAN))
    print(f"  lineage_hash: {_short_hash(lineage)}")
    print(f"  schema_version: {schema}")
    print()
    print(_c("Tenant:", _CYAN))
    print(f"  {tenant}")
    print()
    print(_c("Execution Time:", _CYAN))
    print(f"  {elapsed}")
    print()
    print(sep)
    print(_dim("Full JSON (pretty-printed):"))
    payload = data if data else result
    print(json.dumps(payload, indent=2, sort_keys=True))


def _dim(text: str) -> str:
    return _c(text, _DIM) if _color_enabled() else text


def emit_cli_result(
    result: dict[str, Any],
    args: argparse.Namespace,
    *,
    target: str = ".",
    elapsed_sec: float | None = None,
) -> None:
    """Route REST envelope to the resolved output mode."""
    from archovive_os.cli.flags import emit_response

    mode = resolve_output_mode(args)
    tenant = getattr(args, "tenant_id", "default")
    is_error = int(result.get("status", 500)) >= 400

    if mode == "yaml" or mode == "json":
        emit_response(result, json_flag=True, yaml_flag=mode == "yaml")
        return

    if mode == "human":
        print_human(result, target=target, elapsed_sec=elapsed_sec, tenant=tenant)
        return

    # SUMMARY mode
    print_summary(result, target=target, elapsed_sec=elapsed_sec, tenant=tenant)
    if is_error:
        print(json.dumps(result, indent=2, sort_keys=True), file=sys.stderr)


def human_mode_enabled() -> bool:
    return os.environ.get("ARCHOVIVE_HUMAN") == "1"


def print_human_banner(title: str) -> None:
    if human_mode_enabled():
        print(_c(f"ARCHOVIVE OS v3 — HUMAN MODE\n{title}", _CYAN))
        print("─" * 46)
