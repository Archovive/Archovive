"""Public CLI smoke tests (no engine)."""
from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout

from archovive.cli.cli_main import main


def test_help(capsys=None):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(["--help"])
    assert code == 0
    assert "archovive run" in buf.getvalue()


def test_run_requires_bundle():
    try:
        main(["run"])
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code != 0
