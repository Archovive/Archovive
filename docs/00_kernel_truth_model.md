# 00 — Kernel Truth Model

**Layer 1 · System behavior spec**

**Navigation:** [Decision Hub](00_decision_hub.md) · [Docs hub](README.md) · [DGPP proof](artifacts/dgpp_executive_report.md) · [Next: System Architecture →](01_system_architecture.md)

## Definition

The Archovive **governance kernel** is a pure function from bounded inputs to a **DecisionRecord**. It performs architecture graph construction, policy evaluation, and cryptographic fingerprinting. It has no side effects, no IO, and no awareness of CLI, CI, MCP, or product tiers.

```
Kernel : (RepoSnapshot, PolicySet, Baseline?) → DecisionRecord
```

## DecisionRecord

The canonical kernel output. All surfaces and evidence artifacts are projections or serializations of this structure.

| Field | Type | Semantics |
|-------|------|-----------|
| `graph_hash` | SHA-256 hex | Hash over module graph + structural metrics |
| `replay_hash` | SHA-256 hex | Hash over `graph_hash` + policy control IDs + verdict seed |
| `verdict` | enum string | Governance classification (`APPROVED`, `POLICY_VIOLATION`, …) |
| `exit_code` | int 0–4 | Action code mapped from verdict class |
| `metrics` | object | Graph metrics (module count, coupling, boundary crossings, …) |
| `policy_results` | array | Per-pack rule evaluation: metric, threshold, value, passed |
| `drift_matrix` | object | Drift taxonomy vs stored baseline; `unmeasured` when no baseline |

### Exit code mapping (kernel-derived)

| Code | Verdict class | Meaning |
|------|---------------|---------|
| 0 | allow | All policies passed |
| 1 | drift | Drift violation vs baseline |
| 2 | policy | Regulatory / policy rule violation |
| 3 | engine | Internal engine error |
| 4 | misuse | Invalid invocation |

The kernel assigns `exit_code`. Surfaces may or may not propagate it to the process (see [02_surfaces_cli_ci_mcp.md](02_surfaces_cli_ci_mcp.md)).

## Hash chain

```
RepoSnapshot
    → architecture graph + metrics
        → graph_hash
            → policy evaluation trace
                → replay_hash
```

**Invariant:** `replay_hash` is the cross-surface identity of a decision. CI runners, developer laptops, and MCP tool responses must agree on `replay_hash` for the same input tuple.

## OSS demo kernel (this repository)

File: `simulate/engine.py`

The public repository contains a **self-contained demo kernel** for `examples/demo-fintech`:

- Python AST import graph only (no polyglot IR)
- Three policy packs: `GLOBAL_BASE`, `DORA_2026`, `NIS2_MINIMAL_V1`
- Drift always reports `unmeasured` (no baseline store in OSS)
- Pinned hashes for canonical demo path (regression pins in `simulate/format.py`)

This kernel implements the same **DecisionRecord shape** as production but with reduced policy depth. It exists to validate projection formatting and determinism pins, not to replace the enterprise kernel.

## Production kernel (enterprise bundle)

The frozen bundle (`archovive-enterprise-5.0.0`) ships the full kernel:

- Polyglot hypergraph ingest
- Full policy pack registry (DORA, NIS2, CRA, SOX, …) with optional Ed25519 signatures
- Baseline capture and drift matrix computation
- Gov-tier artifact materialization (`attestation.json`, vault, transparency log)

Kernel logic lives in the bundle runtime, not in this repository. This repo documents the model; the bundle executes it.

## What the kernel is not

- Not a CLI command
- Not a CI plugin
- Not an MCP server
- Not tier-aware (tiers constrain projections in Repo A — see [04_tier_model.md](04_tier_model.md))
- Not responsible for TTY formatting, markdown reports, or process exit propagation

---

[Docs hub](README.md) · [Next: System Architecture →](01_system_architecture.md)
