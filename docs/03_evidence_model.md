# 03 — Evidence Model

**L1 · System behavior spec** — interprets kernel; not adoption authority.  
**Navigation:** [L0 · Decision Hub](00_decision_hub.md) · [Docs hub](README.md) · [← Surfaces](02_surfaces_cli_ci_mcp.md) · [Next: Tier Model →](04_tier_model.md)

## Definition

**Evidence** is the persisted serialization of kernel outputs. Evidence files are not product features — they are artifacts materialized from `DecisionRecord` and pipeline metadata.

```
DecisionRecord + pipeline_metadata → evidence artifacts on disk
```

Surfaces trigger persistence; the kernel authors the semantic content (hashes, verdict, policy trace).

## Artifact taxonomy

| Artifact | Kernel content | Pipeline tier | Schema role |
|----------|----------------|---------------|-------------|
| `ARCHOVIVE_OUTPUT.md` | Human-readable projection of decision | core+ | Report view |
| `repro.json` | `replay_hash`, graph hashes, replay metadata | ci+ | Reproducibility proof |
| `drift_matrix.json` | Drift taxonomy vs baseline | ci+ | Structural/semantic drift |
| `compliance_report.json` | Policy pack evaluation matrices | gov | Regulatory evidence |
| `attestation.json` | Signed verdict certificate (`H_verdict`, trust surface) | gov | Auditor verify-without-rescan |
| `risk_matrix.json` | Risk rows from analysis | gov | Risk posture |

Tier gates **which artifacts may be written**, not what the kernel computes internally.

## repro.json

Primary reproducibility artifact. Contains:

- `replay_hash` — cross-surface decision identity
- `graph_hash` — architecture graph fingerprint
- Compiler / pipeline identity (bundle)
- Policy pack versions applied

**Verify:** same commit + same packs → identical `replay_hash` on laptop, CI runner, air-gapped bundle.

## drift_matrix.json

Kernel output when a baseline exists. Fields include:

- `drift_status` — measured classification (vs `unmeasured` in OSS demo)
- `drift_score` — numeric drift when baseline present
- Structural / semantic / topological drift classes

OSS demo kernel always emits `drift_status: "unmeasured"` because no baseline store exists in the public repository. This is honest kernel output for the input tuple `(repo, policies, baseline=∅)`.

## attestation.json (gov tier)

Cryptographic certificate of a decision:

- `H_verdict` — hash of governance outcome
- Ed25519 signature (gov pipeline tier)
- Trust surface chain (audit root, epoch binding)
- Policy rule trace

Verification (`archovive verify`) replays signature check **without** re-ingesting the repository — trustless third-party audit.

## OSS evidence behavior

In this repository, evidence is **stdout-only**:

| Command | Evidence behavior |
|---------|-------------------|
| `archovive simulate --json` | Full `DecisionRecord` JSON to stdout |
| `archovive simulate` | TTY gate projection (subset of fields) |
| `archovive ci check` | Same kernel output; CI may capture stdout as artifact |

No files are written to disk. JSON shape matches production field names for projection compatibility.

### OSS JSON example (kernel serialization via CLI projection)

```json
{
  "archovive_version": "5.0.0",
  "repo": "demo-fintech",
  "verdict": "POLICY_VIOLATION",
  "exit_code": 2,
  "graph_hash": "fee879ce6ea2d29634bde4f5f2d738e37a0bf409fb200d1d52009c1cd0c734aa",
  "replay_hash": "3e700b6addb401281165f88810f6ade7f93cc7cf9f0ff985bd0390c79d3b9736",
  "metrics": { "module_count": 12, "boundary_crossings": 1 },
  "policy_results": [ "..." ],
  "drift_matrix": { "drift_status": "unmeasured" }
}
```

## Supply-chain evidence (bundle release)

Separate from runtime kernel output — release integrity artifacts:

| File | Purpose |
|------|---------|
| `build_manifest.json` | SHA-256 of every bundle file |
| `archovive.slsa.provenance.json` | SLSA build provenance |
| `archovive-enterprise-5.0.0.zip.sha256` | Release pin |

Location: `internal/releases/` (not runtime evidence).

## SBOM

SBOM data (`file_hashes` per path in analysis scope) is kernel-derived supply-chain evidence. Empty `file_hashes` at gov tier indicates a defect, not an optional feature.

## Anti-patterns (documentation)

- ❌ "Evidence is an Enterprise feature you can buy"
- ✓ "Evidence artifacts are kernel serializations; Enterprise tier enables gov-tier persistence and signing"

Operational detail: [05-evidence/README.md](05-evidence/README.md) (legacy walkthrough; this spec is authoritative for semantics).

---

[Docs hub](README.md) · [← Surfaces](02_surfaces_cli_ci_mcp.md) · [Next: Tier Model →](04_tier_model.md)
