# DGPP — Deterministic Governance Parity Proof

**Truth layer** · [README](../README.md) · [Docs](../docs/README.md) · [← reference_fixtures](07_reference_fixtures.md)

---

## Executive summary

> One governance decision from repository state and policy inputs — projected identically across CLI, CI, and MCP.

CLI executes, CI enforces, MCP queries. Each surface reads the same kernel `DecisionRecord`. MCP is a read/projection surface, not a parallel enforcement path.

---

## Proof summary

| Surface | graph_hash (prefix) | replay_hash (prefix) | decision_record_hash (prefix) | Status |
|---------|---------------------|----------------------|-------------------------------|--------|
| **CLI** | `fee879ce…c734aa` | `3e700b6a…d3b9736` | `13e91e40…df6d29af` | **PASS** |
| **CI** | `fee879ce…c734aa` | `3e700b6a…d3b9736` | `13e91e40…df6d29af` | **PASS** |
| **MCP** | `fee879ce…c734aa` | `3e700b6a…d3b9736` | `13e91e40…df6d29af` | **PASS** |

Full kernel hashes (demo-fintech @ v5.1.0):

```
graph_hash:              fee879ce6ea2d29634bde4f5f2d738e37a0bf409fb200d1d52009c1cd0c734aa
replay_hash:             3e700b6addb401281165f88810f6ade7f93cc7cf9f0ff985bd0390c79d3b9736
decision_record_hash:    13e91e402af6678db7c88b44339d14c811affbacf5d55f2451d45c16df6d29af
policy_results_checksum: 3063ddfce81e7298ad957dd9a01911e97089ed35c5ab10624e2c2f0c6f418b11
```

Verdict: **POLICY_VIOLATION** (DORA_2026 boundary crossing) · Exit code: **2**

---

## Core guarantee

> **CLI == CI == MCP** under identical kernel execution conditions.

For a fixed kernel job envelope (repository snapshot, policy pack set, execution mode), all three surfaces produce:

- Identical `graph_hash`
- Identical `replay_hash`
- Identical normalized `DecisionRecord` hash
- Identical `policy_results` checksum

The only documented surface divergence is **CI process exit propagation** (enforcement layer) — not kernel truth.

---

## Failure modes addressed

| Risk | Addressed by |
|------|----------------|
| **CI/CD decision drift** | Same `replay_hash` on CLI and CI for identical inputs |
| **MCP observation divergence** | MCP projection matches CLI/CI DecisionRecord hash |
| **Hidden policy interpretation** | Single kernel `policy_results` checksum across surfaces |
| **Surface-specific verdict mutation** | Normalized DecisionRecord hash parity test (hard fail on divergence) |

---

## Convergence diagram

```
                         ┌──────────────────────────┐
                         │   Governance Kernel      │
                         │   f(job) → DecisionRecord│
                         └────────────┬─────────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            │                         │                         │
            ▼                         ▼                         ▼
     ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
     │ CLI Surface │           │ CI Surface  │           │ MCP Surface │
     │  simulate   │           │  ci check   │           │run_analysis │
     └──────┬──────┘           └──────┬──────┘           └──────┬──────┘
            │                         │                         │
            └─────────────────────────┼─────────────────────────┘
                                      ▼
                         ┌──────────────────────────┐
                         │   IDENTICAL HASH OUTPUT   │
                         │  graph_hash  = fee879ce… │
                         │  replay_hash = 3e700b6a… │
                         │  decision_hash = 13e91e40…│
                         └──────────────────────────┘
```

---

## Reproduce

```bash
make dgpp
```

Expected: all DGPP tests **PASS**. Any hash divergence fails the build.

Contract: [Kernel contract v1](06_kernel_contract_v1.md)

---

[← README](../README.md) · [Docs index](../docs/README.md)
