"""
Repo A — public product entry points (wrappers only).
"""
from __future__ import annotations

import sys

from archovive_os.cli.binary_dispatch_product import run_product_main


def main_archovive() -> None:
    raise SystemExit(run_product_main("cli"))


def main_cli() -> None:
    raise SystemExit(run_product_main("cli"))


def main_attestation() -> None:
    raise SystemExit(run_product_main("attestation"))
