"""MCP client documentation — server ships in product bundle only."""
from __future__ import annotations

MCP_HELP = """\
Archovive MCP (product bundle)

The MCP server is not started from this public repository.
After installing archovive_product_bundle_v4, configure your MCP client, e.g.:

  command: <bundle>/.venv/bin/python3
  module:  archovive_os.mcp.server
  env:     ARCHOVIVE_REPO=<absolute bundle path>

Tools (bundle):
  archovive.run_analysis   Full pipeline → ARCHOVIVE_OUTPUT.md
  archovive.evidence       Evidence Camera JSON
  archovive.global         global_matrix / heatmap / ranking
  get_version, ping        Smoke probes

See docs/MCP.md"""


def print_mcp_help() -> None:
    print(MCP_HELP)
