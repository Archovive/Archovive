"""Canonical product output — README and CLI must match byte-for-byte (structure)."""
from __future__ import annotations

from simulate.engine import PINNED_GRAPH_HASH, PINNED_REPLAY_HASH

GATE_HEADER = "ARCHOVIVE GATE — DORA Boundary Crossing"


def format_hash(value: str, *, suffix_len: int = 7) -> str:
    """8-char prefix … suffix (e.g. 3e700b6a…d3b9736)."""
    if len(value) <= 8 + suffix_len:
        return value
    return f"{value[:8]}…{value[-suffix_len:]}"


def format_product_lines(*, verdict: str, exit_code: int, replay_hash: str, graph_hash: str) -> list[str]:
    """Header → Verdict → Hashes → Exit Code."""
    return [
        GATE_HEADER,
        f"Verdict: {verdict}",
        f"graph_hash: {format_hash(graph_hash, suffix_len=6)}",
        f"replay_hash: {format_hash(replay_hash)}",
        f"Exit Code: {exit_code}",
    ]


def format_verbose_lines(result) -> list[str]:
    """Detailed OSS walkthrough (--verbose)."""
    failed = [r for r in result.policy_results if not r["passed"]]
    lines = [
        GATE_HEADER,
        "",
        f"Repository ............. {result.repo}",
        f"Modules .............. {result.metrics['module_count']}",
        "",
        "[1/4] Architecture graph",
        f"  graph_hash: {format_hash(result.graph_hash)}",
        f"  coupling_index ....... {result.metrics['coupling_index']}",
        f"  boundary_crossings ... {result.metrics['boundary_crossings']}",
        "",
        "[2/4] Drift matrix",
        f"  drift_status ......... {result.drift_matrix['drift_status']}",
        "",
        "[3/4] Policy evaluation",
    ]
    for rule in result.policy_results:
        mark = "PASS" if rule["passed"] else "FAIL"
        lines.append(f"  [{mark}] {rule['pack_id']} :: {rule['rule_id']}")
    lines.extend(
        [
            "",
            "[4/4] Verdict",
            f"Verdict: {result.verdict}",
            f"graph_hash: {format_hash(result.graph_hash)}",
            f"replay_hash: {format_hash(result.replay_hash)}",
            f"Exit Code: {result.exit_code}",
        ]
    )
    if failed:
        primary = failed[0]
        lines.append("")
        lines.append(f"Finding: {primary['pack_id']} — {primary['rule_id']}")
    return lines


# README / CI pin (demo-fintech v5.0.0)
README_EXAMPLE_LINES = format_product_lines(
    verdict="POLICY_VIOLATION",
    exit_code=2,
    replay_hash=PINNED_REPLAY_HASH,
    graph_hash=PINNED_GRAPH_HASH,
)
