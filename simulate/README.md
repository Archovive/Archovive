# Simulate — OSS Demo Engine

Canonical product output is defined in **`format.py`** — README and CLI share the same lines.

```text
ARCHOVIVE GATE — DORA Boundary Crossing
Verdict: POLICY_VIOLATION
graph_hash: fee879ce…c734aa
replay_hash: 3e700b6a…d3b9736
Exit Code: 2
```

| File | Role |
|------|------|
| `format.py` | Product gate format (single source of truth) |
| `engine.py` | Graph analysis + policy evaluation |
| `runner.py` | CLI (`--verbose` for full walkthrough) |

**Fixture:** `examples/demo-fintech/` · **Docs:** [docs/02-simulate](../docs/02-simulate/README.md)
