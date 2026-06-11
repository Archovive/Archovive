# Reference Fixtures Model

**Truth layer** · [README](../README.md) · [Docs](../docs/README.md) · [← kernel_contract_v1](06_kernel_contract_v1.md) · [Next → dgpp_parity_proof](08_dgpp_parity_proof.md)

---

## Definition

A **reference fixture** is a deterministic repository snapshot used as kernel input for regression pins, CI gates, and DGPP parity proofs.

Reference fixtures are **orthogonal** to Surfaces, Tiers, and Capabilities:

- **Not** a surface (CLI/CI/MCP access path)
- **Not** a tier (Free/Team/Enterprise licensing)
- **Not** a capability (drift, evidence, policy depth, …)

Fixtures **feed** the kernel. They do not define product scope or domain applicability.

## Input categories

| Category | OSS (this repo) | Enterprise bundle |
|----------|-----------------|-------------------|
| **Regression fixture** | `examples/demo-fintech` | `share/examples/*` in bundle |
| **Cross-repo benchmarks** | Not shipped (see Archovive-core `evidence/benchmarks/`) | django/flask E2E harness |
| **Customer repository** | `archovive simulate --repo <path>` (unpinned hashes) | `archovive run` on target repo |

## OSS regression anchor: `demo-fintech`

| Property | Value |
|----------|-------|
| Path | `examples/demo-fintech/` |
| Purpose | CI hash pins, README gate block, DGPP parity fixture |
| Narrative | NovaPay fiction — **pedagogy only**, not domain scope |
| Pins | `simulate/format.py`, `simulate/engine.py` when `repo_name == "demo-fintech"` |

Other `--repo` paths receive computed hashes — still deterministic for that repo, but not pinned in CI.

## What fixtures are not

- Not proof that Archovive applies only to fintech
- Not a tier or licensing boundary
- Not a substitute for running on **your** repository in production evaluation

Enterprise deployment evaluates the bundle against customer repositories. `demo-fintech` proves determinism and surface parity on a **fixed** input — not single-domain applicability.

