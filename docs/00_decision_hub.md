# Decision Hub — Archovive v5.1

**Layer 0 · Primary entry point for adoption decisions**

**Audience:** CTO · CISO · Senior Platform / Security Engineering  
**Navigation:** [Docs hub](README.md) · [Executive proof (DGPP)](artifacts/dgpp_executive_report.md) · [System specs →](README.md#layer-1--system-behavior)

---

## 1. System Summary

Archovive is a **deterministic governance kernel** that evaluates repository architecture against policy rules and materializes a single `DecisionRecord` (verdict, hashes, policy trace).

CLI, CI, and MCP are **projection surfaces** — they execute, enforce, or query the same kernel output. They do not compute independent verdicts.

**Functional SLA:** same commit + same policy packs → same `replay_hash` on every runner.

This repository (Free tier) ships a demo kernel and CLI/CI projections. Team and Enterprise tiers add full kernel, evidence persistence, and MCP server via the [enterprise bundle](07-enterprise/README.md).

---

## 2. Integration Model

Archovive integrates as a **CI merge gate** and optional **IDE query surface** (MCP). It does not replace SAST, dependency scanning, or GRC checklists — it closes the gap between code structure and regulatory policy at the architecture graph level.

```
Developer / Agent          Platform CI              Audit / GRC
      │                         │                        │
      ▼                         ▼                        ▼
 CLI Surface              CI Surface               Evidence artifacts
 (local execute)          (exit code gate)         (repro.json, attestation)
      │                         │                        │
      └─────────────┬───────────┴────────────────────────┘
                    ▼
            Governance Kernel
            f(repo, policy) → DecisionRecord
```

**Minimal CI integration (OSS pattern):**

```yaml
- run: archovive ci check --repo .
# exit 0 = allow merge · exit 2 = policy violation · exit 1 = drift (with baseline)
```

**IDE integration (Team+ bundle):** MCP `run_analysis` returns the same `replay_hash` as CI on the same commit — verified by [DGPP](artifacts/dgpp_executive_report.md).

Detail: [02 Surfaces spec](02_surfaces_cli_ci_mcp.md) · [03 CI operational reference](03-ci/README.md)

---

## 3. Operational Characteristics

| Property | Behavior |
|----------|----------|
| **Execution model** | Pure kernel function `f(job) → DecisionRecord`; surfaces project result |
| **State** | Stateless per invocation; no daemon required for gate execution |
| **Persistence** | Optional — evidence files are kernel serializations written on demand (Team+) |
| **Determinism** | Identical inputs → identical `replay_hash` (functional SLA, not latency SLA) |
| **Resource model** | Single-process analysis; bounded to repository scan scope |
| **CI compatibility** | Process exit code = kernel `exit_code` via `ci check` |
| **Network** | Local-first; no cloud upload required for gate execution |
| **Tier coupling** | Tiers constrain available projections — not kernel verdict logic |

No standing runtime service is required for merge-gate operation. Enterprise deployments may add optional sidecar storage (vault, transparency log) for authoritative decision history.

---

## 4. Operational Footprint

| Deployment | Components | Persistent state |
|------------|------------|------------------|
| **OSS (this repo)** | Python CLI, demo kernel | None (stdout only) |
| **Team bundle** | CLI + CI artifacts | Optional baseline store |
| **Enterprise bundle** | Full kernel + MCP + gov artifacts | Vault, transparency log, signed attestations |

Air-gap: frozen bundle under `/opt/archovive` — [06 Air-gap reference](06-airgap/README.md).

---

## 5. Risk Model

### Eliminated (when DGPP + kernel contract hold)

| Risk | Mechanism |
|------|-----------|
| CI vs local decision drift | Same `replay_hash` across CLI and CI ([DGPP](artifacts/dgpp_executive_report.md)) |
| MCP observation divergence | MCP query projection ≡ CI DecisionRecord hash |
| Hidden policy interpretation | Single kernel `policy_results` trace; no surface-authored verdict fields |
| Non-reproducible audit claims | `repro.json` + pinned hash chain |

### Remaining (explicit scope boundaries)

| Risk | Mitigation path |
|------|-----------------|
| Policy pack correctness | Signed packs (Enterprise), registry review |
| Baseline staleness | Drift matrix vs captured baseline (Team+) |
| Repository ingest coverage | Kernel scope = analyzed languages/paths (polyglot in full bundle) |
| Supply chain of bundle binary | SLSA provenance, cosign, `build_manifest.json` |
| Org process gaps | Archovive gates merge; does not replace human approval workflows |

Proof artifact (not documentation): [DGPP executive report](artifacts/dgpp_executive_report.md) · Reproduce: `make dgpp`

---

## 6. Pilot Feasibility Path

| Step | Action | Tier |
|------|--------|------|
| 1 | Clone repo · `make demo` · inspect gate output | Free |
| 2 | `make ci-demo` · confirm exit code 2 on demo violation | Free |
| 3 | Wire `archovive ci check` into one pipeline (pattern from [03-ci](03-ci/README.md)) | Free |
| 4 | `make dgpp` · verify cross-surface parity in your environment | Free |
| 5 | Request enterprise bundle · run on **your** repository | Team / Enterprise |
| 6 | Capture baseline · enable drift matrix | Team+ |
| 7 | Enable MCP in IDE · confirm `replay_hash` matches CI | Team+ |
| 8 | Gov artifacts for audit cycle | Enterprise |

Pilot contact: [pilot@archovive.com](mailto:pilot@archovive.com) · Enterprise: [07-enterprise](07-enterprise/README.md) · [08-pricing](08-pricing/README.md)

---

## 7. Decision Checklist

Use this checklist before adoption. All items should be **YES** for production merge-gate deployment.

| # | Criterion | YES if… |
|---|-----------|---------|
| 1 | **Determinism requirement** | You need reproducible governance decisions, not opinion-based review |
| 2 | **Architecture-level policy** | Rules apply to module/layer structure (DORA, NIS2, …), not only line bugs |
| 3 | **CI integration feasible** | Pipeline can run a CLI step and fail on non-zero exit |
| 4 | **Local-first acceptable** | Analysis runs on your infrastructure without mandatory cloud egress |
| 5 | **Evidence requirement** | Auditors need `replay_hash`-bound artifacts (Team+ for full set) |
| 6 | **Surface parity matters** | IDE agents (MCP) must not diverge from CI verdict |
| 7 | **Tier fit** | Free = evaluate · Team = multi-repo CI + drift · Enterprise = signed gov |

**Stop / defer if:**

- You only need line-level SAST (SonarQube-class) → Archovive complements, not replaces
- You cannot enforce CI exit codes on merge → gate has no enforcement surface
- You require cloud SaaS-only deployment with no local analysis → conflicts with local-first model

---

## 8. Where to Go Next

| Need | Document |
|------|----------|
| Adoption decision (you are here) | **Decision Hub** (this file) |
| Proof of CLI ≡ CI ≡ MCP | [DGPP executive report](artifacts/dgpp_executive_report.md) |
| Kernel / contract specs | [Docs hub — Layer 1](README.md#layer-1--system-behavior) |
| Wire CI gate | [03-ci operational reference](03-ci/README.md) |
| Enterprise deployment | [07-enterprise](07-enterprise/README.md) |
| Tier / licensing | [08-pricing](08-pricing/README.md) |

---

[Docs hub](README.md) · [DGPP proof](artifacts/dgpp_executive_report.md) · [Kernel Truth Model →](00_kernel_truth_model.md)
