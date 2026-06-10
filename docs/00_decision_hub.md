# Decision Hub — Archovive v5.1

**L0 · Primary entry point for adoption decisions**  
**File:** `00_decision_hub.md` (Layer 0 — not to be confused with L1 kernel specs also prefixed `00_`)

**Audience:** CTO · CISO · Senior Platform / Security Engineering  

**Entry priority:** This document is the **PRIMARY** documentation entry. [README](../README.md) is **SECONDARY** routing only — not a decision document.

**Navigation:** [Docs hub (secondary)](README.md) · [DGPP proof](artifacts/dgpp_executive_report.md) · [System specs →](README.md#layer-1--system-behavior)

---

## Truth Hierarchy

Authority flows in one direction only. Lower layers never override the kernel.

| Rank | Layer | Role | Authority |
|------|-------|------|-----------|
| **1** | **Kernel** (runtime) | Deterministic execution truth — `f(job) → DecisionRecord` | **ONLY source of governance truth** |
| **2** | **System documentation** (L1 specs + ch. 01–09) | Behavioral interpretation — architecture, surfaces, evidence, tiers | Describes kernel; does not define verdicts |
| **3** | **Decision Hub** (L0 — this file) | Adoption / integration judgment — risks, pilot, checklist | **No technical authority** over kernel output |
| **4** | **DGPP** (L2 proof artifact) | External verification output — cross-surface parity readout | **Non-authoritative**; verification-only |

**Rules:**

- Kernel is the **only** source of truth for verdicts, hashes, and policy evaluation.
- System docs **interpret** kernel behavior; they do not compete with kernel output.
- Decision Hub supports **human adoption decisions**; it does not alter or override kernel semantics.
- DGPP **verifies** parity claims; it is **not** required for execution and **does not** influence kernel decisions.

**Cognitive model:** Decision → System → Proof — not Feature → Feature → Feature.

---

## Primary Interpretation Rule

All product documentation is read in this order:

1. **Surfaces** — how the system is accessed (CLI · CI · MCP)
2. **Tiers** — what capabilities are licensed/enabled (Free · Team · Enterprise)
3. **Capabilities** — what is technically possible (drift · evidence · policy · offline · attestations)

**Constraints:**

- Capabilities **never** define surfaces
- Tiers **never** redefine kernel behavior
- Surfaces **never** change execution semantics (kernel truth is identical; only projection differs)

**Use cases:** derived from Surfaces + Tiers + Capabilities — **not authoritative**. Do not present Surface, Tier, and Capability as equal-weight navigation columns.

**MCP:** read/projection surface over the same kernel truth as CLI/CI — **not** an execution authority parallel to CI enforcement.

---

## Reference Fixtures (orthogonal)

**Reference fixtures** (e.g. `examples/demo-fintech`) are **not** surfaces, **not** tiers, and **not** capabilities. They are deterministic regression inputs that feed the kernel for CI pins and DGPP.

| Property | Definition |
|----------|------------|
| What they are | Fixed repo snapshots for CI, hash pins, DGPP |
| What they are not | Domain scope, tier, surface, capability, or production constraint |
| Authority | Fixtures **feed** the kernel; they do not **define** product scope |
| OSS fixture | `demo-fintech` — NovaPay narrative is **pedagogy only** |

Archovive runs on arbitrary repositories via the enterprise bundle; `demo-fintech` is the OSS **regression anchor**, not proof of single-domain applicability.

→ [Reference Fixtures spec](reference_fixtures_model.md) · [examples/README.md](../examples/README.md)

---

## Documentation Index (naming)

Two doc systems coexist by design. Use **layer prefix**, not filename alone:

| Label | File / path | Layer |
|-------|-------------|-------|
| **L0 · Decision Hub** | `00_decision_hub.md` | Adoption entry |
| **L1 · Kernel Truth Model** | `00_kernel_truth_model.md` | System spec (kernel semantics) |
| **L1 · System specs** | `01_system_architecture.md` … `06_kernel_contract_v1.md` | System spec (flat files) |
| **L1 · Operational refs** | `01-intro/` … `09-mcp/` | System behavior walkthroughs |
| **L2 · DGPP** | `artifacts/dgpp_executive_report.md` | Proof artifact |

The duplicate `00_` prefix marks **different layers**: L0 decision vs L1 kernel spec. Always cite the **L0 / L1 / L2** label in enterprise communication.

---

## 1. System Summary

Archovive is a **deterministic governance kernel** that evaluates repository architecture against policy rules and materializes a single `DecisionRecord` (verdict, hashes, policy trace).

CLI, CI, and MCP are **projection surfaces** — they execute, enforce, or query the same kernel output. They do not compute independent verdicts.

**Functional SLA:** same commit + same policy packs → same `replay_hash` on every runner.

This repository (Free tier) ships a demo kernel and CLI/CI projections. Team and Enterprise tiers add full kernel, evidence persistence, and MCP server via the [enterprise bundle](07-enterprise/README.md).

---

## 2. Integration Model

Archovive integrates primarily as a **CI merge gate** (enforcement surface). Optional **IDE query** (MCP) projects the same kernel truth — it does not replace CI enforcement. Archovive does not replace SAST, dependency scanning, or GRC checklists — it closes the gap between code structure and regulatory policy at the architecture graph level.

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

**IDE integration (Team+ bundle):** MCP `run_analysis` is a **query projection** — same `replay_hash` as CI on the same commit, not a parallel enforcement path. Verified by [DGPP](artifacts/dgpp_executive_report.md).

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

## 5a. Proof Artifact (DGPP)

DGPP is positioned **after** adoption context — as external validation, not system input.

| Property | Definition |
|----------|------------|
| **Part of runtime?** | **No** — DGPP is a test-gated proof output, not a kernel or surface component |
| **Required for execution?** | **No** — `archovive simulate` / `ci check` run without DGPP |
| **Purpose** | Validation output for external audit — demonstrates CLI ≡ CI ≡ MCP hash parity |
| **Influences kernel?** | **No** — DGPP reads kernel projections; kernel never reads DGPP |
| **Decision authority?** | **No** — non-authoritative; verification-only |

**Decision flow:** Evaluate adoption (this hub) → implement using system docs → optionally attach DGPP readout for audit evidence.

→ [DGPP executive report](artifacts/dgpp_executive_report.md) · `make dgpp`

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

## 8. Enterprise Readiness — What OSS Proves vs Bundle

Read in interpretation order (Surfaces → Tiers → Capabilities). This is **not** equal-weight navigation across axes.

### 8.1 Surfaces (what OSS demonstrates)

| Surface | OSS proves | Bundle required for |
|---------|------------|---------------------|
| **CLI** | Gate format, `--json` DecisionRecord | Full pipeline on **your** repository |
| **CI** | Exit-code enforcement pattern | Production merge gate on **your** repository |
| **MCP** | Parity proof via DGPP projection | Live MCP server + IDE integration |

### 8.2 Tiers (what each enables)

| Tier | OSS repo ships | Requires bundle |
|------|----------------|-----------------|
| **Free** | Demo kernel + CLI/CI on fixture | — |
| **Team** | — | drift, `run_analysis`, multi-repo CI |
| **Enterprise** | — | attestations, signed packs, air-gap bundle |

### 8.3 Capabilities (derived — under tiers)

| Capability | Free | Team+ | Enterprise |
|------------|------|-------|------------|
| Policy depth | 3 rules | full packs | signed |
| Drift | unmeasured | baseline | baseline |
| Evidence | stdout | repro.json | attestations |
| Offline | — | — | bundle |

**Threshold:** OSS = evaluation + determinism-on-fixture. Enterprise-worthy deployment = bundle + **your** repository + gov artifacts. DGPP-on-fixture ≠ production certification.

Detail: [04 Tier Model](04_tier_model.md) · [07 Enterprise](07-enterprise/README.md)

---

## 9. Where to Go Next

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
