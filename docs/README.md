# Archovive Documentation

**SECONDARY entry** — system overview and navigation only.  
**PRIMARY entry for adoption decisions:** [L0 · Decision Hub](00_decision_hub.md)

Three-layer documentation architecture for Archovive v5.1.

---

## Truth Hierarchy

| Rank | Layer | Location | Authority |
|------|-------|----------|-----------|
| 1 | **Kernel** (runtime) | `simulate/engine.py` · enterprise bundle | **Only source of governance truth** |
| 2 | **System documentation** | L1 specs (`00_kernel_*` … `06_*`) · ch. `01–09/` | Behavioral interpretation — no verdict authority |
| 3 | **Decision Hub** | [L0 · `00_decision_hub.md`](00_decision_hub.md) | Adoption judgment — no technical authority |
| 4 | **DGPP** | [L2 · `artifacts/dgpp_executive_report.md`](artifacts/dgpp_executive_report.md) | Verification-only — non-authoritative |

**Rules:** Kernel → System → Decision → Proof. No bidirectional influence. DGPP never affects kernel output.

**Naming:** `00_decision_hub.md` (L0) and `00_kernel_truth_model.md` (L1) share a `00_` prefix but different layers — always use **L0 / L1 / L2** labels in enterprise docs.

**Cognitive model:** Decision → System → Proof — not Feature → Feature → Feature.

---

## Primary Interpretation Rule

Read product documentation in this order:

1. **Surfaces** — CLI · CI · MCP (how accessed)
2. **Tiers** — Free · Team · Enterprise (what enabled)
3. **Capabilities** — drift · evidence · policy · offline · attestations (what possible)

Capabilities never define surfaces. Tiers never redefine kernel behavior. Surfaces never change execution semantics.

**Use cases** are derived from the three axes — not authoritative. **MCP** is a read/projection surface over the same kernel truth as CLI/CI — not execution authority parallel to CI.

**Reference fixtures** (`examples/demo-fintech`) are orthogonal — not surface, tier, or capability. → [Reference Fixtures spec](reference_fixtures_model.md)

Full rule and enterprise readiness: [L0 · Decision Hub](00_decision_hub.md#primary-interpretation-rule)

---

## Entry Priority

| Priority | Document | Role |
|----------|----------|------|
| **PRIMARY** | [L0 · Decision Hub](00_decision_hub.md) | Adoption · integration · risk · checklist |
| **SECONDARY** | [Docs hub](README.md) (this file) | System overview · spec index · navigation |
| **SECONDARY** | [Repository README](../README.md) | Repo routing · demo observation · links |

README at repository root is **not** a decision document.

---

## Layer 0 — Decision

| Document | Audience |
|----------|----------|
| **[L0 · Decision Hub](00_decision_hub.md)** | CTO · CISO · Senior Engineering |

---

## Layer 1 — System Behavior

Specifications define kernel semantics. **Authoritative for architecture meaning** — not for adoption decisions (see L0).

### L1 kernel / truth specs (flat files)

| Spec | Subject |
|------|---------|
| [L1 · Kernel Truth Model](00_kernel_truth_model.md) | `DecisionRecord`, hash chain |
| [05 Invariants & Determinism](05_invariants_and_determinism.md) | SLA, verification |
| [06 Kernel Contract v1](06_kernel_contract_v1.md) | Formal `f(job)` contract |
| [01 System Architecture](01_system_architecture.md) | Layer model, execution |
| [02 Surfaces: CLI, CI, MCP](02_surfaces_cli_ci_mcp.md) | Projections |
| [03 Evidence Model](03_evidence_model.md) | Kernel serialization |
| [04 Tier Model](04_tier_model.md) | Projection constraints |
| [Reference Fixtures](reference_fixtures_model.md) | Regression inputs (orthogonal to surfaces/tiers) |

### L1 operational references (folders — system behavior, not decision context)

Organized by surface/workflow for operators — **conceptually grouped under L1**, not a separate authority layer.

| Area | References |
|------|------------|
| Surfaces | [02 Simulate](02-simulate/README.md) · [03 CI](03-ci/README.md) · [09 MCP](09-mcp/README.md) |
| Evidence / governance | [04 Governance](04-governance/README.md) · [05 Evidence](05-evidence/README.md) |
| Enterprise | [07 Enterprise](07-enterprise/README.md) · [06 Air-gap](06-airgap/README.md) · [08 Pricing](08-pricing/README.md) |
| Context | [01 Intro](01-intro/README.md) |

---

## Layer 2 — Proof

**Not documentation. Verification-only. Non-authoritative.**

| Artifact | Reproduce |
|----------|-----------|
| **[L2 · DGPP Executive Report](artifacts/dgpp_executive_report.md)** | `make dgpp` |

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
make dgpp      # L2 proof (optional audit gate)
```

---

[← README (secondary)](../README.md) · **[L0 · Decision Hub →](00_decision_hub.md)** · [Contributing](../CONTRIBUTING.md)
