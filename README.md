# Archovive — Local-First Architecture Governance

[![Repository Standard](https://img.shields.io/badge/repo-standard-blue)](CONTRIBUTING.md#repository-standard)

> **May this codebase be released — and why (or why not)?**

Local-first architecture governance — deterministic gate, no cloud, no account.

## Try it

```bash
git clone https://github.com/Archovive/Archovive.git && cd Archovive && make demo
```

*Free tier — same gate format as production.*

```text
ARCHOVIVE GATE — DORA Boundary Crossing
Verdict: POLICY_VIOLATION
graph_hash: fee879ce…c734aa
replay_hash: 3e700b6a…d3b9736
Exit Code: 2
```

CI merge blocker on the demo: `make ci-demo` (exit **2**).

---

## Documentation

Full index: [docs/README.md](docs/README.md)

## Surfaces & Tiers

**Surfaces:**  
CLI — local-first simulate, graph, policy  
CI — deterministic merge gate  
MCP — machine interface for AI coding tools  

**Tiers:**  
Free (OSS) — simulate, ci check, local governance  
Team — multi-repo CI, shared baselines, drift history  
Enterprise — offline bundle, MCP, evidence, signed policy packs  

This repository ships the **Free** tier. Team and Enterprise require the [enterprise bundle](docs/07-enterprise/README.md).

| Tier | Start here |
|------|------------|
| **Free (OSS)** | [Intro](docs/01-intro/README.md) → [Simulate](docs/02-simulate/README.md) |
| **Team** | [CI gate](docs/03-ci/README.md) → [Governance](docs/04-governance/README.md) |
| **Enterprise** | [Enterprise](docs/07-enterprise/README.md) → [Pricing](docs/08-pricing/README.md) |

---

Enterprise bundle & pilot → [docs/07-enterprise](docs/07-enterprise/README.md) · [pilot@archovive.com](mailto:pilot@archovive.com)

MIT [LICENSE](LICENSE) · [Contributing](CONTRIBUTING.md)
