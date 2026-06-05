"""CLI entry for `archovive simulate` and `archovive ci check`."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from simulate.engine import DEFAULT_REPO, DEMO_VERSION, analyze_repo


def _default_demo_path() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "examples" / DEFAULT_REPO
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("examples/demo-fintech not found — run from Archovive repo root")


def format_tty(result) -> list[str]:
    failed = [r for r in result.policy_results if not r["passed"]]
    lines = [
        "=== Archovive Simulate (OSS demo) ===",
        f"Version .............. {DEMO_VERSION}",
        f"Repository ............. {result.repo}",
        f"Modules .............. {result.metrics['module_count']}",
        "",
        "[1/4] Architecture graph",
        f"  graph_hash ........... {result.graph_hash[:16]}…",
        f"  coupling_index ....... {result.metrics['coupling_index']}",
        f"  boundary_crossings ... {result.metrics['boundary_crossings']}",
        f"  instability (pay) .... {result.metrics['instability_payments']}",
        "",
        "[2/4] Drift matrix",
        f"  drift_status ......... {result.drift_matrix['drift_status']}",
        f"  drift_score .......... {result.drift_matrix['drift_score']}",
        "",
        "[3/4] Policy evaluation",
    ]
    for rule in result.policy_results:
        mark = "PASS" if rule["passed"] else "FAIL"
        lines.append(
            f"  [{mark}] {rule['pack_id']} :: {rule['rule_id']} "
            f"(value={rule['value']}, threshold={rule['threshold']})"
        )
    lines.extend(
        [
            "",
            "[4/4] Verdict",
            f"  verdict .............. {result.verdict}",
            f"  replay_hash .......... {result.replay_hash[:16]}…",
            f"  exit_code ............ {result.exit_code}",
            "",
        ]
    )
    if failed:
        primary = failed[0]
        lines.append(
            f"Detected: {primary['pack_id']} violation — "
            f"{primary['rule_id']} ({primary['metric']}={primary['value']})."
        )
        lines.append(
            "This demo shows what Archovive does on every run: graph → drift → policy → verdict."
        )
        lines.append("Install the enterprise bundle for your own repositories (see docs/07-enterprise).")
    else:
        lines.append("All policy checks passed on this demo repository.")
    return lines


def run_simulate_cli(argv: list[str] | None = None, *, ci_mode: bool = False) -> int:
    argv = list(argv or [])
    json_out = "--json" in argv
    repo_arg: Path | None = None
    for i, arg in enumerate(argv):
        if arg in ("--repo", "-r") and i + 1 < len(argv):
            repo_arg = Path(argv[i + 1])
        if arg.startswith("--repo="):
            repo_arg = Path(arg.split("=", 1)[1])

    repo_path = repo_arg or _default_demo_path()
    if not repo_path.is_dir():
        msg = f"demo repo not found: {repo_path}"
        if json_out:
            print(json.dumps({"status": "FAIL", "errors": [msg]}))
        else:
            print(f"simulate: {msg}", file=sys.stderr)
        return 1

    result = analyze_repo(repo_path.resolve(), repo_name=repo_path.name)

    if json_out:
        print(result.to_json())
    else:
        for line in format_tty(result):
            print(line)

    if ci_mode:
        return result.exit_code
    # Educational simulate: success when demo ran (even if verdict is POLICY_VIOLATION).
    return 0
