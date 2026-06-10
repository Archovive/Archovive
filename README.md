# Archovive v5.1.0 — Deterministic Governance Kernel

[![Repository Standard](https://img.shields.io/badge/repo-standard-blue)](CONTRIBUTING.md#repository-standard)
[![DGPP](https://img.shields.io/badge/DGPP-governance%20parity%20proof-green)](docs/artifacts/dgpp_executive_report.md)

## System Overview

Archovive is a deterministic governance kernel: `f(repo, policy) → DecisionRecord`. CLI, CI, and MCP are projection surfaces over that single truth — not separate products.

**Functional SLA:** same commit + same policy packs → same `replay_hash`.

**Kernel model:** [docs/00_kernel_truth_model.md](docs/00_kernel_truth_model.md)

---

## Decision Hub

**Primary entry point for CTO, CISO, and senior engineers evaluating integration.**

→ **[docs/00_decision_hub.md](docs/00_decision_hub.md)**

Includes: integration model · operational characteristics · risk model · pilot path · adoption checklist.

---

## Executive Proof (DGPP)

> **PROOF ARTIFACT — not product documentation**  
> Formally testable guarantee: CLI ≡ CI ≡ MCP on `graph_hash`, `replay_hash`, and normalized DecisionRecord hash for a fixed kernel job.

→ **[docs/artifacts/dgpp_executive_report.md](docs/artifacts/dgpp_executive_report.md)** · Reproduce: `make dgpp`

---

## System Specs

Full documentation: [docs/README.md](docs/README.md)

<details>
<summary><strong>Layer 1 — System behavior specifications</strong></summary>

| Spec | Subject |
|------|---------|
| [00_kernel_truth_model](docs/00_kernel_truth_model.md) | DecisionRecord, hash chain |
| [01_system_architecture](docs/01_system_architecture.md) | Layer model, execution flow |
| [02_surfaces_cli_ci_mcp](docs/02_surfaces_cli_ci_mcp.md) | CLI / CI / MCP projections |
| [03_evidence_model](docs/03_evidence_model.md) | Kernel output serialization |
| [04_tier_model](docs/04_tier_model.md) | Projection constraints |
| [05_invariants_and_determinism](docs/05_invariants_and_determinism.md) | SLA, verification |
| [06_kernel_contract_v1](docs/06_kernel_contract_v1.md) | Formal `f(job)` contract |

**Operational reference (legacy surface docs):** [01-intro](docs/01-intro/README.md) · [02-simulate](docs/02-simulate/README.md) · [03-ci](docs/03-ci/README.md) · [04-governance](docs/04-governance/README.md) · [05-evidence](docs/05-evidence/README.md) · [06-airgap](docs/06-airgap/README.md) · [07-enterprise](docs/07-enterprise/README.md) · [08-pricing](docs/08-pricing/README.md) · [09-mcp](docs/09-mcp/README.md)

**Schemas & tests:** [`schemas/`](schemas/) · `make test` · `make dgpp`

</details>

---

## Quick Observation (OSS demo)

```bash
git clone https://github.com/Archovive/Archovive.git && cd Archovive && make demo
```

```text
ARCHOVIVE GATE — DORA Boundary Crossing
Verdict: POLICY_VIOLATION
graph_hash: fee879ce…c734aa
replay_hash: 3e700b6a…d3b9736
Exit Code: 2
```

CI enforcement: `make ci-demo` (process exit **2**).

---

MIT [LICENSE](LICENSE) · [Contributing](CONTRIBUTING.md)
