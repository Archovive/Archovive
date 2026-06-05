"""Public CLI + OSS simulate tests."""
from __future__ import annotations

import io
from contextlib import redirect_stdout
from pathlib import Path

from cli.cli_main import main
from simulate.engine import PINNED_GRAPH_HASH, PINNED_REPLAY_HASH, analyze_repo
from simulate.format import GATE_HEADER, README_EXAMPLE_LINES
from simulate.runner import format_tty

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_help():
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(["--help"])
    assert code == 0
    assert "simulate" in buf.getvalue()


def test_default_is_simulate():
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main([])
    assert code == 0
    assert "POLICY_VIOLATION" in buf.getvalue()


def test_cli_matches_readme():
    demo = REPO_ROOT / "examples" / "demo-fintech"
    result = analyze_repo(demo, repo_name="demo-fintech")
    cli_lines = format_tty(result)
    assert cli_lines == README_EXAMPLE_LINES
    assert cli_lines[0] == GATE_HEADER
    assert cli_lines[1] == "Verdict: POLICY_VIOLATION"
    assert cli_lines[4] == "Exit Code: 2"


def test_simulate_pinned_hashes():
    demo = REPO_ROOT / "examples" / "demo-fintech"
    result = analyze_repo(demo, repo_name="demo-fintech")
    assert result.verdict == "POLICY_VIOLATION"
    assert result.graph_hash == PINNED_GRAPH_HASH
    assert result.replay_hash == PINNED_REPLAY_HASH


def test_ci_check_exit_code():
    code = main(["ci", "check"])
    assert code == 2


def test_run_requires_bundle():
    try:
        main(["run"])
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code != 0
