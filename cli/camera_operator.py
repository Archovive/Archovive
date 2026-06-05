"""Camera A — Operator Lens (documentation only in public repo)."""
from __future__ import annotations

OPERATOR_HELP = """\
Camera A — Operator Lens (human-facing)

Audience: engineers, tech leads, compliance owners.

Primary artefacts (written to the analysed repository):
  ARCHOVIVE_OUTPUT.md     Canonical report (may be compact)
  compliance_report.json  Policy pack results (gov tier)
  risk_matrix.json        Risk rows (gov tier)

This public repository documents the lens. Execution requires the product bundle.
See docs/CAMERAS.md and docs/OUTPUTS.md."""


def print_operator_help() -> None:
    print(OPERATOR_HELP)
