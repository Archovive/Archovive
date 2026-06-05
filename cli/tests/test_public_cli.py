"""Public CLI + OSS simulate tests."""
from __future__ import annotations

import io
from contextlib import redirect_stdout
from pathlib import Path

from cli.cli_main import main
from simulate.engine import PINNED_GRAPH_HASH, PINNED_REPLAY_HASH, analyze_repo

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
