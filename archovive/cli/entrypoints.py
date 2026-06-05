"""
Public entry points — thin CLI router (no engine imports).
"""
from __future__ import annotations

import sys

from archovive.cli.cli_main import main


def main_archovive() -> None:
    raise SystemExit(main())


def main_cli() -> None:
    """Legacy alias — same v5 router."""
    raise SystemExit(main())


def main_attestation() -> None:
    from archovive._bundle import require_engine

    require_engine("attestation")
