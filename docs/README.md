# Archovive Documentation

System specification for Archovive v5.0.0 — deterministic governance kernel with three projection surfaces.

**Authoritative architecture** (read in order):

| # | Specification | Subject |
|---|---------------|---------|
| 00 | [Kernel Truth Model](00_kernel_truth_model.md) | `DecisionRecord`, hash chain, kernel purity |
| 01 | [System Architecture](01_system_architecture.md) | Layer model, repo layout, execution flow |
| 02 | [Surfaces: CLI, CI, MCP](02_surfaces_cli_ci_mcp.md) | Execution, enforcement, query projections |
| 03 | [Evidence Model](03_evidence_model.md) | Kernel output serialization |
| 04 | [Tier Model](04_tier_model.md) | Projection constraints (Repo A) |
| 05 | [Invariants & Determinism](05_invariants_and_determinism.md) |
| 06 | [Kernel Contract v1](06_kernel_contract_v1.md) |

**Validation layer:** [`schemas/`](../schemas/) · [`tests/`](../tests/test_surface_parity.py) (surface parity, determinism, evidence consistency) SLA, verification, failure modes |

---

## Architecture summary

```
Kernel (pure) → DecisionRecord { graph_hash, replay_hash, verdict, exit_code, … }
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     CLI Surface   CI Surface   MCP Surface
    (execution)  (enforcement)   (query)
```

- **Kernel** computes truth. No IO. No tiers. No formatting.
- **Surfaces** project truth. Never mutate `DecisionRecord`.
- **Evidence** persists kernel output (`repro.json`, `drift_matrix.json`, `attestation.json`).
- **Tiers** constrain which projections and writes are available in this repository — not kernel logic.

Functional SLA: **same commit + same policy packs → same `replay_hash`.**

---

## Observation (OSS demo kernel)

This repository ships Free-tier projections with a demo kernel on `examples/demo-fintech`.

```bash
make demo      # CLI execution projection
make ci-demo   # CI enforcement projection (exit 2 on demo violation)
```

Pinned demo hashes: see [05_invariants_and_determinism.md](05_invariants_and_determinism.md#i1--replay-determinism).

Full kernel + gov artifacts: [07-enterprise/README.md](07-enterprise/README.md) (bundle required).

---

## Legacy operational chapters

Narrative walkthroughs retained for onboarding. **Architecture semantics are defined by specs 00–05**, not these chapters.

| # | Chapter | Use when |
|---|---------|----------|
| 01 | [Intro](01-intro/README.md) | Problem context |
| 02 | [Simulate](02-simulate/README.md) | CLI projection quickstart |
| 03 | [CI gate](03-ci/README.md) | CI enforcement wiring |
| 04 | [Governance](04-governance/README.md) | Policy packs (bundle) |
| 05 | [Evidence](05-evidence/README.md) | Auditor walkthrough |
| 06 | [Air-gap](06-airgap/README.md) | Offline bundle install |
| 07 | [Enterprise](07-enterprise/README.md) | Bundle deployment |
| 08 | [Pricing](08-pricing/README.md) | Tier licensing (product) |
| 09 | [MCP](09-mcp/README.md) | MCP client configuration |

---

[← README](../README.md) · [Contributing](../CONTRIBUTING.md)
