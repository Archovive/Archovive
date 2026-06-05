"""CLI entry for `archovive simulate` and `archovive ci check`."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from simulate.engine import DEFAULT_REPO, analyze_repo
from simulate.format import format_product_lines, format_verbose_lines


def _default_demo_path() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "examples" / DEFAULT_REPO
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("examples/demo-fintech not found — run from Archovive repo root")


def format_tty(result, *, verbose: bool = False) -> list[str]:
    if verbose:
        return format_verbose_lines(result)
    return format_product_lines(
        verdict=result.verdict,
        exit_code=result.exit_code,
        replay_hash=result.replay_hash,
        graph_hash=result.graph_hash,
    )


def run_simulate_cli(argv: list[str] | None = None, *, ci_mode: bool = False) -> int:
    argv = list(argv or [])
    json_out = "--json" in argv
    verbose = "--verbose" in argv
    argv = [a for a in argv if a not in ("--json", "--verbose")]
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
        for line in format_tty(result, verbose=verbose):
            print(line)

    if ci_mode:
        return result.exit_code
    return 0
