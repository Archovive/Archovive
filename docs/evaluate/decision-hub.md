# Enterprise evaluation

**Evaluate** · [README](../../README.md) · [Docs index](../README.md)

Adoption risks, compliance fit, checklist, and pilot planning.

---

## Integration risks

### Reduced when kernel contract and DGPP parity hold

| Risk | Mechanism |
|------|-----------|
| CI vs local decision drift | Same `replay_hash` on CLI and CI ([DGPP](../../specs/08_dgpp_parity_proof.md)) |
| MCP observation divergence | MCP query projection matches CI `DecisionRecord` hash |
| Hidden policy interpretation | Single kernel `policy_results` trace |
| Non-reproducible audit claims | `repro.json` + hash chain (Team+) |

### Remaining scope boundaries

| Risk | Mitigation |
|------|------------|
| Policy pack correctness | Signed packs (Enterprise), registry review |
| Baseline staleness | Drift matrix vs captured baseline (Team+) |
| Repository ingest coverage | Full polyglot ingest in enterprise bundle |
| Bundle supply chain | SLSA provenance, cosign, `build_manifest.json` |
| Process gaps | Archovive gates merge; does not replace human approval workflows |

Archovive complements SAST and GRC — it does not replace line-level scanning or checklist programs.

---

## Compliance mapping

Archovive delivers **technical evidence** for architecture-level controls. It does not certify regulatory compliance.

| Regulation | Policy pack (bundle) | Contribution |
|------------|----------------------|--------------|
| **DORA** | `DORA_2026`, `DORA_MINIMAL_V1` | Critical-path isolation, layer boundaries |
| **NIS2** | `NIS2_MINIMAL_V1` | Boundary crossings, instability ceilings |
| **CRA** | `CRA_MINIMAL_V1` | Security reachability, Annex IV stubs |
| **SOX** | `SOX_2026` | ITGC architecture thresholds |

OSS demo evaluates three simplified rules on a pinned fixture. Full packs require the [enterprise bundle](../integrate/ch-07-enterprise.md).

Artifacts: [`repro.json`](../../specs/03_attestation_schema.md) · [`attestation.json`](../../specs/03_attestation_schema.md) · procedures → [ch-05 Evidence](../integrate/ch-05-evidence.md)

---

## OSS vs bundle readiness

### Surfaces

| Surface | OSS demonstrates | Production requires |
|---------|------------------|---------------------|
| **CLI** | Gate format, `--json` output | Full pipeline on **your** repository |
| **CI** | Exit-code enforcement pattern | Merge gate on **your** repository |
| **MCP** | Parity via [DGPP](../../specs/08_dgpp_parity_proof.md) | Live MCP server (Team+) |

### Tiers

| Tier | OSS repo | Bundle adds |
|------|----------|-------------|
| **Free** | Demo kernel + CLI/CI on fixture | — |
| **Team** | — | Drift, `run_analysis`, multi-repo CI |
| **Enterprise** | — | Signed `attestation.json`, air-gap bundle |

### Capabilities

| Capability | Free | Team+ | Enterprise |
|------------|------|-------|------------|
| Policy depth | 3 rules | Full packs | Signed |
| Drift | unmeasured | Baseline | Baseline |
| `repro.json` | stdout only | ✓ | ✓ |
| `attestation.json` | — | — | ✓ |
| Offline bundle | — | — | ✓ |

**Threshold:** OSS proves determinism on a fixture. Production = bundle + **your** repository + gov artifacts.

Tier semantics → [specs/04_tier_constraints.md](../../specs/04_tier_constraints.md) · Pricing → [pricing.md](pricing.md)

---

## Adoption checklist

All items should be **YES** before production merge-gate deployment.

| # | Criterion | YES if… |
|---|-----------|---------|
| 1 | **Determinism** | You need reproducible governance decisions, not opinion-based review |
| 2 | **Architecture policy** | Rules apply to module/layer structure (DORA, NIS2, …), not only line bugs |
| 3 | **CI integration** | Pipeline can run a CLI step and fail on non-zero exit |
| 4 | **Local-first** | Analysis runs on your infrastructure without mandatory cloud egress |
| 5 | **Evidence** | Auditors need `replay_hash`-bound `repro.json` / `attestation.json` (Team+ for full set) |
| 6 | **Surface parity** | IDE agents (MCP) must match CI verdict |
| 7 | **Tier fit** | Free = evaluate · Team = multi-repo CI + drift · Enterprise = signed gov |

**Defer if:**

- You only need line-level SAST → Archovive complements, not replaces
- You cannot enforce CI exit codes on merge → no enforcement surface
- You require cloud-only SaaS with no local analysis → conflicts with local-first model

---

## Pilot path

| Step | Action |
|------|--------|
| 1 | [Try the demo](../../README.md#try-it) · inspect gate output |
| 2 | `make ci-demo` · confirm exit code 2 |
| 3 | Wire `archovive ci check` → [ch-03 CI](../integrate/ch-03-ci.md) |
| 4 | `make dgpp` · verify cross-surface parity |
| 5 | Request enterprise bundle · run on **your** repository |
| 6 | Capture baseline · enable drift matrix (Team+) |
| 7 | Enable MCP in IDE · confirm `replay_hash` matches CI (Team+) |
| 8 | Gov `attestation.json` cycle (Enterprise) |

Contact: [pilot@archovive.com](mailto:pilot@archovive.com) · [enterprise@archovive.com](mailto:enterprise@archovive.com)

---

## Related

| Topic | Document |
|-------|----------|
| Wire CI | [ch-03 CI](../integrate/ch-03-ci.md) |
| Enterprise install | [ch-07 Enterprise](../integrate/ch-07-enterprise.md) |
| Attestation semantics | [specs/03_attestation_schema.md](../../specs/03_attestation_schema.md) |
| DGPP parity | [specs/08_dgpp_parity_proof.md](../../specs/08_dgpp_parity_proof.md) |

---

[← README](../../README.md) · [Docs index](../README.md)
