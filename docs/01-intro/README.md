# Chapter 01 — What is Archovive?

**Navigation:** [Docs hub](../README.md) · Free Tier · [Next: Simulate →](../02-simulate/README.md)

## Who is this chapter for?

**Everyone** — one minute, no jargon.

**OSS is the Free tier product, not a toy demo.** Same gate format as production; Team and Enterprise add depth via the [enterprise bundle](../07-enterprise/README.md). Surfaces and tiers → [docs hub](../README.md#surfaces--tiers).

---

## The problem

Software teams face three gaps that neither SAST nor GRC closes alone:

### 1. Drift
The implemented architecture diverges from the target — often unnoticed until release. Code review sees files, not **structure**. Monorepos grow; boundaries blur.

### 2. Evidence
Auditors, regulators, and customers require **provable** artifacts: What was checked? Against which rules? With what outcome? Who approved when? Screenshots and Word docs are not enough.

### 3. Compliance
DORA, NIS2, CRA, and SOX require **software governance** — not just line-level security. Regulations know architecture layers. Scanners do not know regulations.

---

## The solution

**Archovive** is a **local-first governance engine**:

1. **Ingest repository** → architecture graph (modules, dependencies, layers)
2. **Evaluate graph** → drift vs baseline, policy rules (DORA, NIS2, …)
3. **Materialize result** → verdict, hashes, evidence pack

All **on-prem**. No code upload to the cloud. No telemetry.  
Same repository state → same output (**determinism**).

---

## Why not SonarQube / Vanta?

**SonarQube** finds line-level bugs. **Vanta** manages checklists.  
**Archovive** analyzes your architecture as a graph and decides deterministically: *may this state be released* — with signed evidence.

It does not replace SAST or GRC. It fills the **gap between them**: architecture + regulation + reproducible evidence.

---

## What Archovive is not

- Not a cloud SaaS scanner
- Not a replacement for line-by-line bug finding (SAST)
- Not a checklist app without code binding
- Not generic AI search — `ask`/`chat` in the enterprise product are **deterministic governance surfaces** on the same kernel

---

## 30-second demo

See the pinned gate output in the [README](../../README.md#try-it) or run `make demo`.

The demo repo is an intentionally broken fintech microservice layout — details in [examples/demo-fintech](../../examples/demo-fintech/README.md).

---

## Who benefits when?

| Role | Typical entry |
|------|---------------|
| Developer / tech lead | Chapter 02 — Simulate |
| Platform / DevOps | Chapter 03 — CI gate |
| Compliance / GRC | Chapters 04–05 — Governance & Evidence |
| CISO / enterprise | Chapter 07 — Enterprise bundle |

Surfaces and tiers → [docs hub](../README.md#capability-matrix) · [Chapter 08 — Pricing](../08-pricing/README.md)

---

**[← Docs hub](../README.md)** · **Next:** [02 — Simulate](../02-simulate/README.md)
