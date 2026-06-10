# 01 — System Architecture

**Layer 1 · System behavior spec**

**Navigation:** [Decision Hub](00_decision_hub.md) · [Docs hub](README.md) · [← Kernel Truth Model](00_kernel_truth_model.md) · [Next: Surfaces →](02_surfaces_cli_ci_mcp.md)

## Layered model

Archovive separates four concerns. Only the kernel computes truth.

```
┌─────────────────────────────────────────────────────────────┐
│ Tier constraints (Repo A product layer — not kernel logic)  │
│  Free · Team · Enterprise — license + projection gates      │
└────────────────────────────┬────────────────────────────────┘
                             │ constrains availability
┌────────────────────────────▼────────────────────────────────┐
│ Surfaces (projection + execution)                           │
│  CLI — execute, render TTY/JSON                             │
│  CI  — enforce via process exit                             │
│  MCP — query via tool protocol                              │
└────────────────────────────┬────────────────────────────────┘
                             │ reads DecisionRecord
┌────────────────────────────▼────────────────────────────────┐
│ Evidence (persistence)                                      │
│  repro.json · drift_matrix.json · attestation.json          │
│  = serialized kernel outputs                                │
└────────────────────────────┬────────────────────────────────┘
                             │ materialized by
┌────────────────────────────▼────────────────────────────────┐
│ Kernel (pure)                                               │
│  RepoSnapshot + PolicySet + Baseline? → DecisionRecord      │
└─────────────────────────────────────────────────────────────┘
```

## Repository layout (Repo A — public OSS)

| Path | Layer | Role |
|------|-------|------|
| `simulate/engine.py` | Kernel (demo) | Pure analysis → `AnalysisResult` ≡ DecisionRecord shape |
| `simulate/format.py` | CLI projection | TTY gate line formatting — **not kernel** |
| `simulate/runner.py` | Surface routing | `simulate` vs `ci check` exit propagation |
| `cli/cli_main.py` | Surface router | Command dispatch to projections |
| `cli/product_ux.py` | Surface help | User-facing command documentation |
| `cli/mcp_client.py` | MCP projection stub | Documents bundle MCP; no server in OSS |
| `examples/demo-fintech/` | Fixture | Canonical `RepoSnapshot` for pins |
| `internal/` | Build / bundle | Enterprise bundle assets (not kernel source in public tree) |

**Boundary rule:** public tree must not contain full engine source (`make boundary`).

## Execution model

1. **Ingest** — kernel walks repository state into an architecture graph.
2. **Evaluate** — policy packs apply rules to graph metrics.
3. **Materialize** — kernel produces `DecisionRecord` with hashes and verdict.
4. **Project** — surface renders (CLI TTY), enforces (CI exit), or exposes (MCP tool).
5. **Persist** (optional) — evidence layer writes kernel serialization to disk.

Steps 1–3 are kernel-only. Steps 4–5 are surface/evidence layers.

## OSS vs bundle deployment

| Deployment | Kernel | Surfaces | Evidence writes |
|------------|--------|----------|-------------------|
| OSS repo (`make demo`) | Demo kernel in `simulate/` | CLI + CI on demo repo | JSON to stdout only |
| Team bundle | Full kernel | CLI + CI + MCP (`run_analysis`) | `repro.json`, `drift_matrix.json` |
| Enterprise bundle | Full kernel | All surfaces + gov CLI | Full artifact set + attestations |

Same kernel truth model; tier constraints limit which projections and persistence steps are licensed.

## Demo kernel data flow

```
examples/demo-fintech/
        │
        ▼
 simulate/engine.py :: analyze_repo()
        │
        ▼
 AnalysisResult { graph_hash, replay_hash, verdict, exit_code, … }
        │
        ├─► simulate/format.py :: format_product_lines()  → TTY gate
        ├─► AnalysisResult.to_json()                    → JSON projection
        └─► runner.py exit policy:
              simulate  → process exit 0 (funnel)
              ci check  → process exit = exit_code (enforcement)
```

Formatting is explicitly outside `analyze_repo()`. This preserves kernel purity in the OSS demo even though production separates engine and runtime packages differently.

## Related specifications

- Truth model: [00_kernel_truth_model.md](00_kernel_truth_model.md)
- Surface execution: [02_surfaces_cli_ci_mcp.md](02_surfaces_cli_ci_mcp.md)
- Evidence serialization: [03_evidence_model.md](03_evidence_model.md)
- Tier constraints: [04_tier_model.md](04_tier_model.md)

---

[Docs hub](README.md) · [← Kernel Truth Model](00_kernel_truth_model.md) · [Next: Surfaces →](02_surfaces_cli_ci_mcp.md)
