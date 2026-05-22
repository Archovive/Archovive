"""Camera B — Machine Lens (stub; engine in product bundle)."""
from __future__ import annotations

from archovive._bundle import require_engine

MACHINE_HELP = """\
Camera B — Machine Lens (IR, anchors, replay)

Audience: CI systems, replay tools, integrators.

Primary artefacts:
  repro.json           Replay metadata and graph hashes
  drift_matrix.json    Structural / behavioural drift taxonomy
  attestation.json     Signed anchors, pipeline identity (gov tier)

Requires product bundle engine. See docs/CAMERAS.md."""


def print_machine_help() -> None:
    print(MACHINE_HELP)


def run_machine_stub(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv:
        print_machine_help()
        return 0
    require_engine("camera machine")
