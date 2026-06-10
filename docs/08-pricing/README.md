# Chapter 08 — Pricing & tiers

> **Operational Reference (Legacy Surface Docs)**  
> This document describes operational behavior.  
> For system architecture and decision-making context see: [Decision Hub](../00_decision_hub.md)  
> Tier spec: [04 Tier Model](../04_tier_model.md)

**Navigation:** [Decision Hub](../00_decision_hub.md) · [Docs hub](../README.md) · [← Enterprise](../07-enterprise/README.md)

## Who is this chapter for?

**Budget owners, procurement, and founders** who need to know what's free, what scales, **who buys which surface** (CLI, MCP, CI), and why enterprise costs more than a scanner subscription.

*Indicative — not contractual. Binding quotes: **enterprise@archovive.com***

---

## Surfaces & Tiers

**Surfaces:**  
CLI — local-first simulate, graph, policy  
CI — deterministic merge gate  
MCP — machine interface for AI coding tools  

**Tiers:**  
Free (OSS) — simulate, ci check, local governance  
Team — multi-repo CI, shared baselines, drift history  
Enterprise — offline bundle, MCP, evidence, signed policy packs  

This repository ships the **Free** tier. Team and Enterprise require the [enterprise bundle](../07-enterprise/README.md).

Full capability matrix → [docs hub](../README.md#capability-matrix).

---

## Value proposition

Archovive delivers **deterministic, offline-capable architecture evidence** — without changing code, without sending data to the cloud.

| Outcome | Benefit |
|---------|---------|
| **CI gates** | Objective exit codes instead of opinion debates |
| **Audit evidence** | Signed attestations instead of manual reviews |
| **Regulatory bridge** | DORA/NIS2/CRA rules at graph level — not checklists only |

**Moat:** regulatory policy packs → graph invariants. SAST does not know laws. GRC does not compile repositories.

---

## Who buys what

See the [hub capability matrix](../README.md#capability-matrix) for CLI, CI, and MCP by tier. MCP detail → [Chapter 09](../09-mcp/README.md).

---

## OSS (this repository)

| | |
|---|---|
| **Price** | **Free** (MIT) |
| **Includes** | `simulate`, `ci check`, demo repo, story docs |
| **Surfaces** | CLI only · CI pattern on demo repo · no MCP server |
| **Limit** | Demo engine only — simplified graph, three policy rules, no attestations |
| **Ideal for** | Evaluation, developer adoption, learning CI patterns |

```bash
bash dist/install.sh && archovive simulate
```

---

## Team / CI

| | |
|---|---|
| **Price** | **Free** for open source; **€49 / dev / month** commercial (SMB) |
| **Includes** | `repro.json`, `drift_matrix.json`, CI exit codes |
| **Surfaces** | CLI `run`, `diff`, `gate` · MCP `run_analysis` · CI merge gate |
| **Ideal for** | Platform engineering, scale-ups, monorepo teams |
| **Pain** | "We don't know if architecture still matches intent" |

Requires enterprise bundle. No CISO required — one DevOps lead is enough as champion.

---

## Enterprise / Gov

| | |
|---|---|
| **Price** | **€2,500 / certified repository / year** (unlimited attestations) |
| **Includes** | Attestations, compliance reports, vault, transparency log, live dispatch |
| **Surfaces** | Full CLI · full MCP · gov CI artifacts + SIEM |
| **Ideal for** | Regulated companies, banks, audit channels |
| **Pain** | DORA/NIS2/CRA deadline, audit prep, release governance |

Enterprise negotiation dimensions: repo count, CI seats, support SLA, signing key ceremony.

---

## SLA

| | OSS | Enterprise |
|---|-----|------------|
| **Latency** | No guarantee | No latency SLA |
| **Determinism** | Demo-pinned hashes | **Functional SLA:** same commit + packs → same `replay_hash` |
| **Support** | Community / docs | enterprise@archovive.com |

---

## Segment matrix

| Segment | Tier | Entry chapter |
|---------|------|---------------|
| Developer / evaluator | OSS | 01, 02 |
| Platform engineering | Team/CI | 03 |
| CRA/NIS2 vendor | Gov | 04, 05 |
| Air-gap / government | Enterprise | 06, 07 |
| Bank / DORA | Enterprise | 07 |
| Audit boutique | Gov (per client) | 05, 07 |

---

## Pilot program

**Runs through end of 2026** — first **5 months free** for qualified pilots (regulated industry, platform teams with CI mandate, audit channels).

What you get:

- Enterprise bundle on **your** repository (not demo only)
- Help wiring the CI gate
- Evidence packs for internal or external auditors

**Interested?** → **pilot@archovive.com**  
Subject: `Pilot` + industry + approximate repo size. Reply within 2 business days.

General enterprise: enterprise@archovive.com

---

## Next steps

- **Try it:** `make demo` · [Docs hub](../README.md)
- **CI:** [03 — CI](../03-ci/README.md)
- **Enterprise:** **enterprise@archovive.com**

---

**[← Docs hub](../README.md)** · **Start:** [01 — Intro](../01-intro/README.md)
