"""CLI for `archovive bootstrap` — sovereign integrity gate."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from archovive_os.product_v1.bootstrap import (
    DEFAULT_BOOTSTRAP_REPO,
    format_bootstrap_tty,
    run_bootstrap,
)


def run_bootstrap_cli(
    *,
    json_out: bool = False,
    root: Path | None = None,
    repo: str | None = None,
    integrity_mode: str = "full",
    epoch_id: str | None = None,
) -> int:
    root_path = (root or Path(os.environ.get("ARCHOVIVE_ROOT", "."))).resolve()
    spec_path = root_path / "spec_v4.json"
    health_path = root_path / "health_certificate_v2.json"
    bootstrap_repo = repo or os.environ.get("ARCHOVIVE_BOOTSTRAP_REPO", DEFAULT_BOOTSTRAP_REPO)

    result = run_bootstrap(
        spec_path if spec_path.exists() else None,
        health_path if health_path.exists() else None,
        repo=bootstrap_repo,
        integrity_mode=integrity_mode,
        epoch_id=epoch_id,
    )

    if json_out:
        print(result.to_json())
        return 0 if result.status == "PASS" else 1

    for line in format_bootstrap_tty(result):
        print(line)
    if result.status == "FAIL" and result.errors:
        print("\nDetails:")
        for err in result.errors:
            print(f"  - {err}")

    return 0 if result.status == "PASS" else 1
