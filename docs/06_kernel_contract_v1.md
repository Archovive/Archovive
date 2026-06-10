# 06 — Kernel Contract v1

**Navigation:** [Docs hub](README.md) · [← Invariants](05_invariants_and_determinism.md)

Formal execution boundary for Archovive v5.0.0. This document is **non-executable specification**. Enforcement lives in `schemas/` and `tests/`.

```
f : KernelJob → DecisionRecord
```

Surfaces translate invocation context into `KernelJob`, call `f`, then project `DecisionRecord`. Surfaces must not alter truth.

---

## Kernel Input Contract

### Kernel Execution Envelope

Schema: [`schemas/kernel_job.json`](../schemas/kernel_job.json)

| Field | Required | Type | Semantics |
|-------|:--------:|------|-----------|
| `schema_id` | yes | const `archovive_kernel_job_v1` | Contract version |
| `repo_path` | yes | string | Repository snapshot root |
| `repo_name` | yes | string | Logical repo id → `DecisionRecord.repo` |
| `policy_pack_ids` | yes | string[] | Ordered packs applied by kernel |
| `mode` | yes | enum `analyze` | Kernel mode (analysis only) |
| `commit_ref` | no | string \| null | Optional VCS binding |
| `baseline_ref` | no | string \| null | Optional baseline for drift |

### Forbidden input fields

The kernel must not receive surface, tier, or formatting semantics:

| Forbidden | Reason |
|-----------|--------|
| `tier`, `product_tier`, `license_tier` | Tier is Repo A projection constraint |
| `surface`, `mcp_tool` | Surface is post-kernel projection |
| `cli_format`, `tty`, `process_exit` | Formatting / enforcement is surface layer |
| Any IO handle, network endpoint | Kernel is pure |

**Invariant K1:** `f(job)` is defined solely on envelope fields + snapshot at `repo_path`.

---

## Kernel Output Contract

### DecisionRecord

Schema: [`schemas/decision_record.json`](../schemas/decision_record.json)

| Field | Required | Type | Semantics |
|-------|:--------:|------|-----------|
| `schema_id` | yes | const `archovive_decision_record_v1` | Contract version (added at validation layer) |
| `archovive_version` | yes | semver string | Engine version stamp |
| `repo` | yes | string | From `repo_name` |
| `verdict` | yes | enum | Governance classification |
| `exit_code` | yes | int 0–4 | Action code from verdict class |
| `graph_hash` | yes | hex64 | Architecture graph fingerprint |
| `replay_hash` | yes | hex64 | Decision identity fingerprint |
| `metrics` | yes | object | Graph metrics |
| `policy_results` | yes | array | Rule evaluation trace |
| `drift_matrix` | yes | object | Drift state (may be `unmeasured`) |

### Forbidden output fields

| Forbidden | Reason |
|-----------|--------|
| `gate_header`, `tty_lines` | CLI format layer |
| `tier`, `surface`, `mcp_tool` | Projection metadata |
| `process_exit_override` | CI funnel semantics |

---

## Hash definitions

### graph_hash

```
graph_payload = { modules: [{path, layer}, …], metrics: {…} }
graph_hash    = SHA256(JSON_canonical(graph_payload))
```

Canonical JSON: sorted keys, compact separators (`,` `:`).

OSS demo: pinned when `repo_name == demo-fintech` for regression stability.

### replay_hash

```
replay_payload = {
  graph_hash: <graph_hash>,
  policy: [<control_id>, …],
  verdict_seed: <primary_failed_control_id | "PASS">
}
replay_hash = SHA256(JSON_canonical(replay_payload))
```

**Cross-surface identity:** `replay_hash` is the parity key. CLI `--json`, CI check JSON, and MCP tool JSON must expose the same value for the same envelope.

---

## Invariants (strict)

| ID | Invariant | Test |
|----|-----------|------|
| **K1** | Same envelope → same `replay_hash` | `tests/test_kernel_determinism.py` |
| **K2** | Kernel is pure: `f(job)` → `DecisionRecord`, no IO | Architecture + determinism tests |
| **K3** | No tier awareness in kernel | Envelope schema forbids tier fields |
| **K4** | No surface awareness in kernel | Envelope schema forbids surface fields |
| **K5** | CLI ≡ CI ≡ MCP on DecisionRecord | `tests/test_surface_parity.py` |
| **K6** | Evidence ⊆ kernel serialization | `tests/test_evidence_consistency.py` |

### Surface parity exception (documented, not a kernel defect)

CI enforcement projection propagates `exit_code` to **process exit**. CLI demo funnel returns process exit **0** while still printing kernel `exit_code`. DecisionRecord is unchanged.

---

## Evidence contract mapping

| Artifact | Schema | Derivation |
|----------|--------|------------|
| `repro.json` | [`schemas/repro.json`](../schemas/repro.json) | Subset copy of DecisionRecord fields |
| `drift_matrix.json` | (kernel object) | `DecisionRecord.drift_matrix` — no external derivation |
| `attestation.json` | gov bundle | `H_verdict` ← kernel `replay_hash`; no surface fields |

---

## OSS demo kernel binding

This repository implements contract v1 for the demo kernel:

| Contract element | OSS location |
|------------------|--------------|
| `f(job)` | `simulate/engine.py :: analyze_repo()` |
| CLI projection | `simulate/runner.py`, `simulate/format.py` |
| CI projection | `simulate/runner.py` (`ci_mode=True`) |
| MCP projection | Documented; full tool server in enterprise bundle |
| Contract tests | `tests/test_*.py` |

Full production kernel in `archovive-enterprise-5.0.0` must satisfy the same contract semantics.

---

## Validation layer

```
schemas/kernel_job.json      → input shape
schemas/decision_record.json → output shape
schemas/repro.json           → evidence serialization shape

tests/test_surface_parity.py       → K5
tests/test_kernel_determinism.py     → K1, K2
tests/test_evidence_consistency.py   → K6
```

Run: `make test`

---

[Docs hub](README.md) · [← Invariants](05_invariants_and_determinism.md)
