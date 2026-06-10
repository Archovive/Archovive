# 05 — Invariants & Determinism

**Layer 1 · System behavior spec**

**Navigation:** [Decision Hub](00_decision_hub.md) · [Docs hub](README.md) · [DGPP proof](artifacts/dgpp_executive_report.md) · [← Tier Model](04_tier_model.md) · [Next: Kernel Contract →](06_kernel_contract_v1.md)

## Functional SLA

> Same commit + same policy packs → same `replay_hash` on every runner.

This is Archovive's determinism contract. It is a **functional** SLA, not a latency SLA. Runtime seconds and memory vary; hashes must not.

## Core invariants

### I1 — Replay determinism

For fixed inputs `(RepoSnapshot, PolicySet, Baseline?)`:

```
Kernel(inputs) → DecisionRecord D
Kernel(inputs) → DecisionRecord D'   ⟹   D.replay_hash = D'.replay_hash
```

Verified in OSS: consecutive `archovive simulate --json` runs produce byte-identical JSON on `demo-fintech`.

Pinned regression values (demo-fintech @ v5.0.0):

```
graph_hash:  fee879ce6ea2d29634bde4f5f2d738e37a0bf409fb200d1d52009c1cd0c734aa
replay_hash: 3e700b6addb401281165f88810f6ade7f93cc7cf9f0ff985bd0390c79d3b9736
```

Tests: `cli/tests/test_public_cli.py` · pins in `simulate/engine.py` · gate format in `simulate/format.py`.

### I2 — Surface parity

For the same kernel inputs, CLI, CI, and MCP must agree on:

- `replay_hash`
- `verdict`
- `exit_code` (semantic value — CI propagates to process, CLI funnel may not)

Cross-tier kernel truth identity (bundle E2E): personal = team = enterprise `kernel_truth_hash` on identical repo state (benchmark evidence in Archovive-core `evidence/benchmarks/REVIEW_E2E.md`).

### I3 — Kernel purity

The kernel function has:

- No filesystem writes
- No network IO
- No TTY formatting
- No tier / license checks
- No surface-specific branches

In OSS: `analyze_repo()` in `simulate/engine.py` returns `AnalysisResult` only. Formatting is strictly downstream in `simulate/format.py` and `simulate/runner.py`.

### I4 — Evidence provenance

Evidence files contain kernel fields. Surfaces and persistence layers must not:

- Invent `replay_hash` values
- Override `verdict` after kernel return
- Mix formatting strings into signed attestation payloads

`attestation.json` signs kernel-derived `H_verdict`, not CLI gate header text.

### I5 — Non-mutation

Surfaces render or enforce. No surface modifies repository state as part of governance projection. (Analysis ingest is read-only on repo snapshot.)

### I6 — Tier isolation

Tiers affect **availability** of projections and artifact writes in Repo A. Tiers do not define alternate kernel code paths for the same licensed kernel input.

## Exit code invariants

| Code | Kernel meaning | OSS demo produces? |
|------|----------------|-------------------|
| 0 | Allow | No (demo fails policy) |
| 1 | Drift violation | No — baseline absent, drift `unmeasured` |
| 2 | Policy violation | Yes — DORA boundary crossing |
| 3 | Engine error | No in demo path |
| 4 | Misuse | Yes — e.g. `archovive ci` without `check` |

Documented exit semantics: `cli/product_ux.py`. CI enforcement requires code 1/2 propagation via `ci check`, not `simulate`.

## Projection-specific rules (not kernel exceptions)

| Rule | Layer | Rationale |
|------|-------|-----------|
| `simulate` process exit always 0 on success | CLI funnel projection | Evaluation UX in OSS |
| `ci check` process exit = `exit_code` | CI enforcement projection | Merge gate semantics |
| Gate header string fixed in OSS | Format layer | Cosmetic; not signed |
| Demo hash pinning | Regression harness | Stabilizes CI for canonical fixture only |

Pinning applies when `repo_name == "demo-fintech"`. Other `--repo` paths receive computed hashes — still deterministic for that repo, unpinned.

## Determinism verification checklist

| Check | Command / test |
|-------|----------------|
| Gate format pin | `pytest cli/tests/test_public_cli.py::test_cli_matches_readme` |
| Hash pin | `test_simulate_pinned_hashes` |
| CI enforcement | `test_ci_check_exit_code` (exit 2) |
| JSON stability | Repeated `--json` SHA256 match |
| Public boundary | `make boundary` |
| README gate block | Matches `simulate/format.py` `README_EXAMPLE_LINES` |

## Failure modes (defects)

| Observation | Classification |
|-------------|----------------|
| Different `replay_hash` same commit, same packs, same runner | **Kernel or ingest defect** |
| CLI and CI disagree on `replay_hash` | **Surface parity defect** |
| MCP tool returns different verdict than CI on same commit | **Surface parity defect** |
| Attestation verify fails on unmodified artifact | **Evidence / signing defect** |
| Tier change alters `replay_hash` with identical inputs | **Tier leakage into kernel — defect** |

## Release determinism matrix (bundle)

Frozen binary E2E (django, enterprise) — Run 1 = Run 2:

| Signal | Stable across runs |
|--------|-------------------|
| `baseline_hash` | ✓ |
| `drift_matrix_hash` | ✓ |
| `decision_hash` (ask = chat = governance) | ✓ |

Source: `internal/releases/RELEASE_NOTES_v5.0.0.md`

---

[Docs hub](README.md) · [← Tier Model](04_tier_model.md)
