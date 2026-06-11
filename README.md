# Archovive v5.1.0

[![Repository Standard](https://img.shields.io/badge/repo-standard-blue)](CONTRIBUTING.md#repository-standard)

Block bad architecture merges before they reach production — with a local, reproducible gate decision.

---

## The problem

Teams pass tests and scanners while **layer boundaries drift**. Auditors ask for proof that architecture was checked against policy — not slides. Line-level SAST and GRC checklists do not enforce **module structure** at merge time.

## The solution

Run Archovive in CI to get a deterministic allow/block decision on repository architecture. Inspect the same result locally before push. Enterprise bundle adds full policy depth, signed artifacts, and IDE integration on **your** repository.

---

## Try it

**Prerequisites:** Linux or WSL2 · bash · Python 3.10+ · `make`

```bash
git clone https://github.com/Archovive/Archovive.git && cd Archovive && make demo
```

Expected output:

```text
ARCHOVIVE GATE — DORA Boundary Crossing
Verdict: POLICY_VIOLATION
graph_hash: fee879ce…c734aa
replay_hash: 3e700b6a…d3b9736
Exit Code: 2
```

Merge blocking uses **`make ci-demo`** (process exit **2**) — not `simulate` alone. Wire-up → [Integrate: CI](docs/integrate/ch-03-ci.md).

Demo runs on pinned fixture `examples/demo-fintech` — not your production repo.

---

## Choose your path

| Role | Route |
|------|-------|
| **Developer** | [ch-02 Simulate](docs/integrate/ch-02-simulate.md) |
| **CI / Platform** | [ch-03 CI](docs/integrate/ch-03-ci.md) |
| **CTO** | [Evaluate: decision-hub](docs/evaluate/decision-hub.md) → [ch-07 Enterprise](docs/integrate/ch-07-enterprise.md) |
| **CISO** | [Evaluate: decision-hub](docs/evaluate/decision-hub.md) → [specs: attestation](specs/03_attestation_schema.md) |

Documentation index → [docs/README.md](docs/README.md)

---

## OSS vs enterprise bundle

| | **This repo (Free)** | **Enterprise bundle** |
|---|----------------------|------------------------|
| Run on your code | Fixture demo only | ✓ |
| CI merge gate pattern | ✓ (demo) | ✓ (production) |
| MCP in IDE | — | ✓ |
| Signed `attestation.json` | — | ✓ |
| Get started | `make demo` | [ch-07 Enterprise](docs/integrate/ch-07-enterprise.md) · pilot@archovive.com |

---

MIT [LICENSE](LICENSE) · [Contributing](CONTRIBUTING.md)
