"""Camera C — Evidence Lens (stub; runs in product bundle / MCP)."""
from __future__ import annotations

from cli._bundle import require_engine

EVIDENCE_HELP = """\
Camera C — Evidence Lens (audit / supply chain)

Audience: auditors, CI gates, MCP clients (Cursor, etc.).

JSON fields (benchmarks/ in pilot bundle):
  determinism.json   Reproducibility fingerprints
  drift.json         Drift score/status (null when unmeasured)
  verify.json        Verify-chain result
  sbom.json          SBOM hash + file_hashes (SHA-256 per path)
  perf.json / memory.json
  summary.json

Global: global_matrix.json, global_heatmap.json, global_ranking.json

CLI (in bundle): archovive evidence, archovive camera evidence
MCP (in bundle): archovive.evidence, archovive.global

See docs/CAMERAS.md, docs/SBOM.md, docs/DRIFT.md."""


def print_evidence_help() -> None:
    print(EVIDENCE_HELP)


def run_evidence_stub(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv or not argv or argv == ["--json"]:
        print_evidence_help()
        return 0
    require_engine("evidence")
