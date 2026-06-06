# Documentation

Surfaces, tiers, and paths — pick one and go. Each chapter links back here.

---

## Surfaces & Tiers

**Surfaces:**  
CLI — local-first simulate, graph, policy  
CI — deterministic merge gate  
MCP — machine interface for AI coding tools  

**Tiers:**  
Free (OSS) — simulate, ci check, local governance  
Team — multi-repo CI, shared baselines, drift history  
Enterprise — offline bundle, MCP, evidence, signed policy packs  

This repository ships the **Free** tier. Team and Enterprise require the [enterprise bundle](07-enterprise/README.md).

---

## Paths by tier

| Tier | Path | Commands |
|------|------|----------|
| **Free (OSS)** | [01 Intro](01-intro/README.md) → [02 Simulate](02-simulate/README.md) | `make demo`, `ci check` |
| **Team** | [03 CI](03-ci/README.md) → [04 Governance](04-governance/README.md) → [08 Pricing (Team)](08-pricing/README.md#team--ci) | `run`, `diff`, drift matrix |
| **Enterprise** | [07 Enterprise](07-enterprise/README.md) → [05 Evidence](05-evidence/README.md) → [06 Air-gap](06-airgap/README.md) | bundle, MCP, attestations |

---

## Paths by surface

| Surface | Start here |
|---------|------------|
| **CLI** | [02 Simulate](02-simulate/README.md) |
| **CI** | [03 CI gate](03-ci/README.md) |
| **MCP** | [09 MCP](09-mcp/README.md) |

---

## Capability matrix

| Capability | Free | Team | Enterprise | Doc |
|------------|:----:|:----:|:------------:|-----|
| CLI simulate / graph / policy | ✓ | ✓ | ✓ | 02 |
| CI merge gate | ✓ | ✓ | ✓ | 03 |
| Drift matrix | — | ✓ | ✓ | 04 |
| Policy packs | 3 rules | full | signed | 04 |
| Evidence | — | partial | ✓ | 05 |
| Offline bundle | — | — | ✓ | 06 |
| MCP | — | run_analysis | full | 09 |

---

## Full sequence (reference)

| # | Chapter |
|---|---------|
| 1 | [Intro](01-intro/README.md) |
| 2 | [Simulate](02-simulate/README.md) |
| 3 | [CI gate](03-ci/README.md) |
| 4 | [Governance](04-governance/README.md) |
| 5 | [Evidence](05-evidence/README.md) |
| 6 | [Air-gap](06-airgap/README.md) |
| 7 | [Enterprise](07-enterprise/README.md) |
| 8 | [Pricing](08-pricing/README.md) |
| 9 | [MCP](09-mcp/README.md) |

---

[← Back to README](../README.md) · [Contributing](../CONTRIBUTING.md)
