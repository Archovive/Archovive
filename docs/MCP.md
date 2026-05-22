# MCP integration

The MCP **server** ships in `archovive_product_bundle_v4`, not in this public repository.

## Tools (product bundle)

| Tool | Purpose |
|------|---------|
| `archovive.run_analysis` | Full pipeline → `ARCHOVIVE_OUTPUT.md` |
| `archovive.evidence` | Evidence Camera JSON for a repo or benchmark name |
| `archovive.global` | `global_matrix`, `global_heatmap`, `global_ranking` |
| `get_version`, `ping` | Deterministic smoke probes |

## Configuration (example)

```json
{
  "mcpServers": {
    "archovive": {
      "command": "/path/to/archovive_product_bundle_v4/.venv/bin/python3",
      "args": ["-m", "archovive_os.mcp.server"],
      "env": {
        "ARCHOVIVE_REPO": "/path/to/archovive_product_bundle_v4",
        "ARCHOVIVE_COMPILE": "runtime"
      }
    }
  }
}
```

Install the bundle first: `docs/INSTALL.md`.

## This repo

```bash
archovive mcp --help
```

Documents the contract only.
