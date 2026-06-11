# Attestation & repro artifacts

**Truth layer** · [README](../README.md) · [Docs](../docs/README.md) · [← Surfaces](02_surfaces_cli_ci_mcp.md) · [Next → Tier constraints](04_tier_constraints.md)

---

Evidence means **persisted kernel artifacts only**: `repro.json` and `attestation.json`. Surfaces trigger writes; hashes and verdict originate in the kernel `DecisionRecord`.

## repro.json

Serialization of kernel decision fields for reproducibility verification.

| Field | Semantics |
|-------|-----------|
| `replay_hash` | Cross-surface decision identity |
| `graph_hash` | Architecture graph fingerprint |
| `verdict` | Kernel governance classification |
| `exit_code` | Kernel action code (0–4) |
| `policy_results` | Per-pack rule evaluation trace |
| `metrics` | Graph metrics at decision time |
| `drift_matrix` | Baseline comparison when present; `unmeasured` when no baseline |

**Verify:** same commit + same policy packs → identical `replay_hash` on laptop, CI runner, and air-gapped bundle.

JSON Schema: [`schemas/repro.json`](../schemas/repro.json). Must not contain surface-only fields (`gate_header`, `ci_runner`, `mcp_session`, …).

## attestation.json

Cryptographic certificate of a governance decision (enterprise gov tier).

| Field | Semantics |
|-------|-----------|
| `H_verdict` | Hash of governance outcome |
| `trust_surface` | Audit chain root, epoch binding, hypervisor binding |
| Signature | Ed25519 (gov pipeline tier) |
| Policy trace | Which rules fired at decision time |

Verification (`archovive verify`) checks signature and hash chain **without** re-ingesting the repository.

## Tier-gated writes

| Artifact | Free (OSS) | Team+ | Enterprise gov |
|----------|------------|-------|----------------|
| `repro.json` | — (stdout JSON only) | ✓ | ✓ |
| `attestation.json` | — | — | ✓ |

OSS emits `DecisionRecord` JSON to stdout via CLI projection; no disk writes.

## Related artifacts (bundle)

`drift_matrix.json`, `compliance_report.json`, and `risk_matrix.json` are additional kernel serializations gated by pipeline tier. Semantics for `repro.json` and `attestation.json` above are canonical for audit replay.

Procedures: [Integrate — Evidence](../docs/integrate/ch-05-evidence.md)

---

[← Surfaces](02_surfaces_cli_ci_mcp.md) · [Tier constraints →](04_tier_constraints.md)
