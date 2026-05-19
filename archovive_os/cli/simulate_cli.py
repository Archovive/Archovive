"""CLI for `archovive simulate` — guided Truth Simulator."""
from __future__ import annotations

import sys

from archovive_os.product_v1.simulate import (
    DEFAULT_FIXTURE,
    format_simulate_tty,
    run_simulate,
)


def run_simulate_cli(
    *,
    fixture: str = DEFAULT_FIXTURE,
    json_out: bool = False,
    pause: bool = False,
    epoch_id: str | None = None,
) -> int:
    def _pause(phase: str) -> None:
        if pause and sys.stdin.isatty():
            try:
                input(f"\n  → [{phase}] Press Enter to continue… ")
            except EOFError:
                pass

    try:
        result = run_simulate(fixture, epoch_id=epoch_id, pause=_pause if pause else None)
    except FileNotFoundError as exc:
        if json_out:
            import json

            print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, separators=(",", ":")))
        else:
            print(f"SIMULATE: FAIL\n  - {exc}", file=sys.stderr)
        return 1

    if json_out:
        print(result.to_json())
        return 0 if result.status == "PASS" else 1

    for line in format_simulate_tty(result):
        print(line)
    if result.errors:
        print("\nDetails:")
        for err in result.errors:
            print(f"  - {err}")

    return 0 if result.status == "PASS" else 1
