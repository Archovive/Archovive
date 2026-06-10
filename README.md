# Archovive v5.0.0 — Deterministic Governance Kernel

[![Repository Standard](https://img.shields.io/badge/repo-standard-blue)](CONTRIBUTING.md#repository-standard)

Archovive is a **deterministic governance kernel** that materializes a single decision from repository state and policy inputs. CLI, CI, and MCP are **projection surfaces** — they execute, enforce, or query the same kernel truth. They do not compute independent verdicts.

**Functional SLA:** same commit + same policy packs → same `replay_hash` on every runner.

System specification: [docs/README.md](docs/README.md)

---

## Kernel Truth Model

The kernel accepts a bounded input tuple:

```
(repo_state, policy_packs, baseline?) → DecisionRecord
```

`DecisionRecord` is pure data — no IO, no formatting:

| Field | Role |
|-------|------|
| `graph_hash` | Fingerprint of the architecture graph |
| `replay_hash` | Fingerprint of graph + policy evaluation + verdict seed |
| `verdict` | Governance outcome (`APPROVED`, `POLICY_VIOLATION`, …) |
| `exit_code` | Machine action code (0–4) derived from verdict class |
| `policy_results` | Per-rule evaluation trace |
| `drift_matrix` | Structural/semantic drift vs baseline (when baseline present) |

Evidence artifacts (`repro.json`, `drift_matrix.json`, `attestation.json`) are **serialized kernel outputs**, not separate product features. Surfaces render or persist them; they do not author them.

---

## System Diagram

```
                    ┌─────────────────────────┐
                    │   Governance Kernel     │
                    │  (pure, tier-agnostic)  │
                    │                         │
                    │  graph → policy →       │
                    │  DecisionRecord         │
                    └───────────┬─────────────┘
                                │
              same replay_hash  │  same verdict
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
  │ CLI Surface │      │ CI Surface  │      │ MCP Surface │
  │ execution   │      │ enforcement │      │ query       │
  │ projection  │      │ projection  │      │ projection  │
  └─────────────┘      └─────────────┘      └─────────────┘
         │                      │                      │
         ▼                      ▼                      ▼
   TTY / JSON            process exit            tool JSON
   (format layer)        = gate exit             (IDE agent)
```

Surfaces **never modify truth**. Formatting (gate lines, markdown reports) lives in projection layers only.

Details: [docs/01_system_architecture.md](docs/01_system_architecture.md) · [docs/02_surfaces_cli_ci_mcp.md](docs/02_surfaces_cli_ci_mcp.md)

---

## Invariants

These hold across all surfaces and tiers (where the full kernel is installed):

1. **Replay determinism** — identical inputs → identical `replay_hash`.
2. **Surface parity** — CLI, CI, and MCP expose the same decision for the same commit (CI uses process exit; CLI may use funnel exit in demo mode — see surface spec).
3. **Kernel purity** — no IO, no formatting, no tier logic inside the kernel.
4. **Evidence provenance** — artifacts are kernel serializations; surfaces do not invent verdict fields.
5. **Non-mutation** — surfaces render or enforce; they do not rewrite `DecisionRecord`.
6. **Tier isolation** — tiers constrain which projections and artifacts are **available in this repository**; they are not kernel branches.

Full specification: [docs/05_invariants_and_determinism.md](docs/05_invariants_and_determinism.md)

---

## Architecture Layers

| Layer | Responsibility | Location (this repo) |
|-------|----------------|----------------------|
| **Kernel** | Graph ingest, policy evaluation, hash materialization | `simulate/engine.py` (OSS demo kernel); full kernel in enterprise bundle |
| **Surfaces** | CLI / CI / MCP projection and execution model | `cli/`, `simulate/runner.py`, `cli/mcp_client.py` |
| **Evidence** | Persistence of `DecisionRecord` and derived artifacts | Documented in [docs/03_evidence_model.md](docs/03_evidence_model.md); full serialization in bundle |
| **Tiers** | Product projection constraints (Repo A only) | [docs/04_tier_model.md](docs/04_tier_model.md) |

Tiers gate **which surfaces and artifact writes are licensed**, not how the kernel computes truth.

---

## Observation (OSS demo kernel)

This repository ships a **Free-tier projection** with a self-contained demo kernel on `examples/demo-fintech`. It proves the gate format and hash pins; it is not the full production kernel.

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

CI enforcement projection on the same kernel output: `make ci-demo` (process exit **2**).

Pinned hashes (demo-fintech @ v5.0.0):

```
graph_hash:  fee879ce6ea2d29634bde4f5f2d738e37a0bf409fb200d1d52009c1cd0c734aa
replay_hash: 3e700b6addb401281165f88810f6ade7f93cc7cf9f0ff985bd0390c79d3b9736
```

---

## Documentation Index

| # | Specification |
|---|---------------|
| 00 | [Kernel Truth Model](docs/00_kernel_truth_model.md) |
| 01 | [System Architecture](docs/01_system_architecture.md) |
| 02 | [Surfaces: CLI, CI, MCP](docs/02_surfaces_cli_ci_mcp.md) |
| 03 | [Evidence Model](docs/03_evidence_model.md) |
| 04 | [Tier Model](docs/04_tier_model.md) |
| 05 | [Invariants & Determinism](docs/05_invariants_and_determinism.md) |
| 06 | [Kernel Contract v1](docs/06_kernel_contract_v1.md) |

Legacy narrative chapters (01–09) remain for operational walkthroughs; the specifications above are authoritative for architecture semantics.

---

## Kernel Contract Layer

Archovive exposes a **formal execution boundary** between the governance kernel and its projection surfaces.

| Component | Role |
|-----------|------|
| [`schemas/`](schemas/) | JSON schemas for kernel input (`kernel_job`), output (`decision_record`), and evidence (`repro`) |
| [`docs/06_kernel_contract_v1.md`](docs/06_kernel_contract_v1.md) | Non-executable specification: `f(job) → DecisionRecord`, hash definitions, strict invariants |
| [`tests/test_surface_parity.py`](tests/test_surface_parity.py) | CLI ≡ CI ≡ MCP DecisionRecord parity |
| [`tests/test_kernel_determinism.py`](tests/test_kernel_determinism.py) | Repeated execution → identical hashes |
| [`tests/test_evidence_consistency.py`](tests/test_evidence_consistency.py) | Evidence artifacts ⊆ kernel serialization |

System invariants are **testable properties**, not documentation claims:

- Same input envelope → same `replay_hash`
- Kernel is a pure function with no tier or surface awareness
- Surfaces project truth; they do not author verdict fields

Enterprise bundle (full kernel + gov artifacts): [docs/07-enterprise/README.md](docs/07-enterprise/README.md)

---

MIT [LICENSE](LICENSE) · [Contributing](CONTRIBUTING.md)
