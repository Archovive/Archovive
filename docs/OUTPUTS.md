# Output artefacts

Paths are relative to the **analysis root** (Git top-level unless overridden).

## Canonical markdown

| File | Tiers | Description |
|------|-------|-------------|
| `ARCHOVIVE_OUTPUT.md` | core, ci, gov | Human-readable report; may be compact on very small or large repos |

## JSON artefacts

| File | Tiers | Description |
|------|-------|-------------|
| `repro.json` | ci, gov | Replay metadata, graph hashes, exit code, performance fields |
| `drift_matrix.json` | ci, gov | Structural and behavioural drift taxonomy |
| `attestation.json` | gov | Signed attestation (`H_verdict`, decision trace) |
| `risk_matrix.json` | gov | Risk rows from analysis |
| `compliance_report.json` | gov | Policy pack evaluation matrices |

## MCP-only

| File | When |
|------|------|
| `repair_context_v1.json` | `archovive.run_analysis` with `intent=generate_repair_context` |

## Tenant and cache (gov)

| Path | Description |
|------|-------------|
| `.archovive/transparency_log.jsonl` | Append-only audit log |
| `.archovive/vault_store.jsonl` | Vault store |
| `.archovive/vault_v3_delta.jsonl` | Vault delta log |
| `.archovive/cache/*.json` | Per-run cache (polyglot IR, drift taxonomy, predicates) |
| `.archovive/tenant.json` | Created by `archovive init` |

## Tier summary

| Tier | Artefacts |
|------|-----------|
| **core** | `ARCHOVIVE_OUTPUT.md` |
| **ci** | above + `repro.json`, `drift_matrix.json` |
| **gov** | above + attestation, risk, compliance, `.archovive/*` |

Set tier in `archovive_license.json` at the **bundle root**, or via `ARCHOVIVE_LICENSE_TIER`.

## Compact reports

Enabled automatically when:

- File count &lt; 5 or &gt; 500, or
- Report exceeds 5,000 lines

Override: `ARCHOVIVE_COMPACT=1` or `ARCHOVIVE_COMPACT=0`.

## Verify (gov)

```bash
archovive verify attestation.json
archovive-verify attestation.json
```

`archovive-verify` requires Python 3.11+ only (no full `archovive_os` install).

Recorded pilot outputs per tier: `test_nachweise/`.

## Drift semantics

When **no baseline** exists for a repository (first analysis, no stored baseline graph), structural/semantic/topological drift classes are `unmeasured`.

| Field | Meaning |
|-------|---------|
| `drift_status: unmeasured` | No baseline — drift cannot be computed |
| `drift_score: null` | Neutral placeholder, **not** a risk indicator |
| `drift_score: 0.0–1.0` | Only when drift taxonomy is measured against a baseline |

Do not interpret `null` or `unmeasured` as “medium risk”. Use `drift_matrix.json` and `drift_reasons` for detail when a baseline exists.

## Cameras overview

Archovive presents the same analysis data in three deterministic perspectives:

| Camera | Lens | Audience | Contents |
|--------|------|----------|----------|
| **A — Operator** | Human decisions | Engineers, leads | `ARCHOVIVE_OUTPUT.md`, risk/compliance summaries |
| **B — Machine** | IR & anchors | CI, replay tools | `repro.json`, `drift_matrix.json`, attestation anchors |
| **C — Evidence** | Audit & supply chain | Auditors, MCP, CI gates | determinism, verify, SBOM `file_hashes`, vault/rule/compiler hashes, perf/memory |

All three cameras use the same pipeline run. CLI: `archovive evidence` / `archovive camera evidence`. MCP: `archovive.evidence`, `archovive.global`.

## SBOM file hashes

Benchmark and `archovive sbom` SBOM evidence includes `file_hashes`: map of repo-relative path → SHA-256 of file content (from polyglot IR). Empty hashes indicate a serialization bug — not a first-run or baseline effect.
