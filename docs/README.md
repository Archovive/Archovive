# Archovive Documentation

Three-layer documentation architecture for Archovive v5.1.

---

## Layer 0 — Decision

**Single entry point for adoption decisions.**

| Document | Audience |
|----------|----------|
| **[00 Decision Hub](00_decision_hub.md)** | CTO · CISO · Senior Engineering |

Includes operational characteristics, integration model, risk model, pilot path, adoption checklist.

---

## Layer 1 — System Behavior

Specifications define kernel semantics, surfaces, evidence, and tiers. **Authoritative for architecture meaning.**

### Kernel / truth

| Spec | Subject |
|------|---------|
| [00 Kernel Truth Model](00_kernel_truth_model.md) | `DecisionRecord`, hash chain, kernel purity |
| [05 Invariants & Determinism](05_invariants_and_determinism.md) | SLA, verification, failure modes |
| [06 Kernel Contract v1](06_kernel_contract_v1.md) | Formal `f(job) → DecisionRecord` |

### Architecture

| Spec | Subject |
|------|---------|
| [01 System Architecture](01_system_architecture.md) | Layer model, repo layout, execution flow |

### Surfaces

| Spec | Operational reference |
|------|----------------------|
| [02 Surfaces: CLI, CI, MCP](02_surfaces_cli_ci_mcp.md) | [02 Simulate](02-simulate/README.md) · [03 CI gate](03-ci/README.md) · [09 MCP](09-mcp/README.md) |

### Evidence

| Spec | Operational reference |
|------|----------------------|
| [03 Evidence Model](03_evidence_model.md) | [05 Evidence](05-evidence/README.md) |

### Tiers

| Spec | Operational reference |
|------|----------------------|
| [04 Tier Model](04_tier_model.md) | [08 Pricing](08-pricing/README.md) |

### Enterprise / air-gap

| Operational reference |
|----------------------|
| [07 Enterprise](07-enterprise/README.md) · [06 Air-gap](06-airgap/README.md) |

Context chapter: [01 Intro](01-intro/README.md)

---

## Layer 2 — Proof / Executive Artifacts

**Not documentation. Not feature description. Test-gated proof outputs.**

| Artifact | Reproduce |
|----------|-----------|
| **[DGPP Executive Report](artifacts/dgpp_executive_report.md)** | `make dgpp` |

Validation: [`schemas/`](../schemas/) · [`tests/`](../tests/test_dgpp_governance_parity.py)

---

## Architecture summary

```
Kernel (pure) → DecisionRecord
       ├─► CLI Surface   (execution)
       ├─► CI Surface   (enforcement)
       └─► MCP Surface  (query)
```

Functional SLA: **same commit + same policy packs → same `replay_hash`.**

---

## OSS demo

```bash
make demo      # CLI projection
make ci-demo   # CI projection (exit 2 on demo)
make dgpp      # cross-surface parity proof
```

---

[← README](../README.md) · [Decision Hub →](00_decision_hub.md) · [Contributing](../CONTRIBUTING.md)
