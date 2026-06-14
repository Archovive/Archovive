# MCP (Model Context Protocol)

**Integrate** · [README](../../README.md) · [Docs](../README.md) · [Evaluate](../evaluate/decision-hub.md) · [← 07-enterprise](ch-07-enterprise.md) · [Next → 10-hardware-ki](ch-10-hardware-ki.md)

---

## One-liner

**MCP is a read/projection surface over the same kernel truth as CLI/CI** — verdict, `graph_hash`, `replay_hash` — inside your IDE agent loop. **Not** an execution authority parallel to CI enforcement.

---

## Why MCP matters

Copy-paste from a terminal breaks the coding flow. MCP puts **governance in the loop**:

- Pre-merge checks from Cursor, Claude Code, or any MCP client
- Same deterministic output as `archovive ci check` — no shadow tooling
- Audit-friendly: agent calls are tool invocations, not ad-hoc prompts

---

## Tools (enterprise bundle)

| Tool | Purpose | Tier |
|------|---------|------|
| `archovive.run_analysis` | Full pipeline → `ARCHOVIVE_OUTPUT.md` | Team+ |
| `archovive.evidence` | Evidence Camera JSON | Enterprise |
| `archovive.global` | global_matrix / heatmap / ranking | Enterprise |
| `get_version` | Version probe | All (bundle) |
| `ping` | Smoke test | All (bundle) |

**Free (OSS):** `archovive mcp --help` documents the surface; no MCP server ships in this repo.

---

## Cursor config

Add to `.cursor/mcp.json` (or Cursor MCP settings):

```json
{
  "mcpServers": {
    "archovive": {
      "command": "/opt/archovive/bin/archovive-mcp",
      "env": {
        "ARCHOVIVE_REPO": "/path/to/your/repo"
      }
    }
  }
}
```

Replace paths with your enterprise bundle install and repository root.

---

## Claude Code / agent example

**User prompt:** “Why is this PR blocked?”

**Agent flow:**

1. Call `archovive.run_analysis` with `ARCHOVIVE_REPO` set to the PR workspace
2. Read verdict + hashes from tool output
3. Reply: *“Blocked: POLICY_VIOLATION — DORA boundary crossing. graph_hash: fee879ce… replay_hash: 3e700b6a…”*

Same `replay_hash` as CI on the same commit — no drift between IDE and pipeline.

---

## Tier depth

| Tier | MCP |
|------|-----|
| **Free (OSS)** | Docs only — `archovive mcp --help` |
| **Team** | `run_analysis` in IDE |
| **Enterprise** | Full surface — `evidence`, `global`, offline bundle |

Requires [enterprise bundle](../integrate/ch-07-enterprise.md). Readiness → [Enterprise evaluation](../evaluate/decision-hub.md#oss-vs-bundle-readiness). Hardware-KI appliance → [ch-10 Hardware-KI](../integrate/ch-10-hardware-ki.md).

---
