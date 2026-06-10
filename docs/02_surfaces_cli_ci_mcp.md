# 02 — Surfaces: CLI, CI, MCP

**L1 · System behavior spec** — interprets kernel; not adoption authority.  
**Navigation:** [L0 · Decision Hub](00_decision_hub.md) · [Docs hub](README.md) · [← System Architecture](01_system_architecture.md) · [Next: Evidence Model →](03_evidence_model.md)

## Definition

A **surface** is a deterministic projection of `DecisionRecord` onto an execution context. Surfaces do not recompute verdicts. They differ only in **how** truth is rendered, enforced, or queried.

| Surface | Execution model | Primary consumer |
|---------|-----------------|------------------|
| **CLI** | Execute analysis; render TTY or JSON | Developer, operator |
| **CI** | Execute analysis; propagate `exit_code` to process | Pipeline, merge gate |
| **MCP** | Expose kernel via tool protocol | IDE agent (Cursor, Claude Code, …) |

**Parity invariant:** for the same `(RepoSnapshot, PolicySet, Baseline?)`, all surfaces must agree on `replay_hash` and `verdict`. Disagreement is a defect.

## CLI Surface (execution projection)

### Role

Execute the kernel (or invoke bundle runtime) and render output for human or script consumption.

### OSS commands (this repository)

| Invocation | Kernel call | Output projection | Process exit |
|------------|-------------|-------------------|--------------|
| `archovive` / `archovive simulate` | `analyze_repo()` | TTY gate format | **0** (funnel — exit printed, not propagated) |
| `archovive simulate --json` | `analyze_repo()` | `DecisionRecord` JSON | 0 |
| `archovive simulate --verbose` | `analyze_repo()` | 4-step TTY walkthrough | 0 |
| `archovive ci check` | `analyze_repo()` | TTY gate format | **`exit_code`** from kernel |
| `archovive doctor` | — | Environment probe | 0 / 1 |

Formatting lives in `simulate/format.py`. Kernel function `analyze_repo()` returns data only.

### TTY gate projection (canonical)

```text
ARCHOVIVE GATE — DORA Boundary Crossing
Verdict: POLICY_VIOLATION
graph_hash: fee879ce…c734aa
replay_hash: 3e700b6a…d3b9736
Exit Code: 2
```

This is a **rendering** of `DecisionRecord`, not an independent output type. Pins: `simulate/format.py` · `README.md`.

### Bundle CLI (Team / Enterprise)

Commands such as `archovive run`, `archovive gate`, `archovive diff`, `archovive verify` invoke the full kernel via bundle runtime. They produce the same `DecisionRecord` semantics with additional evidence persistence. Stubbed in OSS with bundle install instructions — no kernel execution in public repo.

## CI Surface (enforcement projection)

### Role

Bind kernel `exit_code` to pipeline control flow. A merge gate is enforcement of an already-computed decision, not a separate analysis path.

### OSS behavior

```bash
archovive ci check --repo examples/demo-fintech
# process exit = kernel exit_code (2 on demo DORA violation)
```

| Property | CLI `simulate` | CI `check` |
|----------|------------------|------------|
| Kernel input | Same | Same |
| `replay_hash` | Same | Same |
| Process exit | 0 (funnel) | = `exit_code` |

The funnel exit on `simulate` is a **projection choice** for evaluation UX. CI must not use funnel exit for merge blocking.

### Production CI

With enterprise bundle on target repository:

- Kernel runs on PR commit
- `exit_code` blocks merge
- Evidence artifacts uploaded as pipeline artifacts (kernel serialization — see [03_evidence_model.md](03_evidence_model.md))

Reference workflow: [03-ci/README.md](03-ci/README.md) (operational example; architecture semantics defined here).

## MCP Surface (query projection)

### Role

Expose kernel truth to IDE agents via Model Context Protocol. Tools return structured views of `DecisionRecord` and derived artifacts without mutating repository state.

### OSS (this repository)

No MCP server ships here. `archovive mcp` prints bundle configuration documentation only (`cli/mcp_client.py`).

### Bundle tools (Team+)

| Tool | Projection |
|------|------------|
| `archovive.run_analysis` | Full pipeline → human report + kernel hashes |
| `archovive.would_block` | Pre-merge dry-run of enforcement exit |
| `archovive.decision.*` | Read-only decision contract views |
| `get_version`, `ping` | Smoke / determinism probes |

### Bundle tools (Enterprise)

| Tool | Projection |
|------|------------|
| `archovive.evidence` | Evidence Camera JSON (determinism, drift, verify, SBOM) |
| `archovive.global` | Cross-repo matrix / heatmap / ranking |

**Parity:** MCP `run_analysis` on commit X must yield the same `replay_hash` as `archovive ci check` on commit X.

Operational MCP setup: [09-mcp/README.md](09-mcp/README.md)

## Surface comparison matrix

| Property | CLI | CI | MCP |
|----------|-----|-----|-----|
| Computes verdict | No (kernel) | No (kernel) | No (kernel) |
| Mutates truth | No | No | No |
| Propagates exit_code | Optional | Required | Via tool response |
| Format | TTY / JSON | TTY + process exit | Tool JSON |
| OSS availability | Full (demo kernel) | Full (demo kernel) | Docs only |

## Anti-patterns (documentation)

Do **not** describe CLI, CI, and MCP as separate feature modules with independent logic. Correct framing:

- ❌ "Archovive has a CI feature and an MCP feature"
- ✓ "CI and MCP are enforcement and query projections of the governance kernel"

---

[Docs hub](README.md) · [← System Architecture](01_system_architecture.md) · [Next: Evidence Model →](03_evidence_model.md)
