# Chapter 05 — Evidence

> **Operational Reference (Legacy Surface Docs)**  
> This document describes operational behavior.  
> For system architecture and decision-making context see: [Decision Hub](../00_decision_hub.md)  
> Evidence spec: [03 Evidence Model](../03_evidence_model.md)

**Navigation:** [Decision Hub](../00_decision_hub.md) · [Docs hub](../README.md) · [← Governance](../04-governance/README.md) · [Next: Air-gap →](../06-airgap/README.md)

## Who is this chapter for?

**Auditors, IT compliance, CRA/NIS2 owners, and SIEM operators** who need **verifiable artifacts** — not screenshots, not verbal confirmations, but signed, replayable evidence packs.

**Surface sold:** CLI `verify`, `audit export` · MCP `archovive.evidence`, `archovive.global` · CI artifact upload (gov tier).

---

## What is an evidence pack?

An evidence pack is a **coherent bundle** of analysis results you can hand to auditors, regulators, or internal revision:

| File | Content | Pipeline tier |
|------|---------|---------------|
| `ARCHOVIVE_OUTPUT.md` | Human report | core+ |
| `repro.json` | Replay metadata, graph hashes | ci+ |
| `drift_matrix.json` | Drift taxonomy | ci+ |
| `compliance_report.json` | Policy pack matrices | gov |
| `attestation.json` | Signed verdict certificate | gov |
| `risk_matrix.json` | Risk rows from analysis | gov |

OSS demo delivers terminal/JSON. Enterprise bundle writes the full set to the analysis directory.

```bash
archovive audit export --bundle   # enterprise / gov
```

---

## Attestations

`attestation.json` is the **core artifact for auditors**:

- `H_verdict` — hash of the decision
- `trust_surface` — chain: audit_chain_root, epoch_binding, hypervisor_binding
- Ed25519 signature (gov tier)
- Decision trace — which policy rules fired

**Verify without re-analysis:**

```bash
archovive verify attestation.json
```

Trustless: third parties can verify the certificate without re-scanning your repository.

---

## SBOM & supply chain

Archovive produces SBOM data with **`file_hashes`** — SHA-256 per file path in analysis scope. Relevant for:

- **CRA** — software transparency for digital products
- **NIS2** — supply chain evidence
- **DORA** — ICT risk management
- **SLSA** — build provenance

Empty `file_hashes` in gov tier = bug, not a feature.

---

## SLSA & build provenance

The enterprise release ships:

| Artifact | Purpose |
|----------|---------|
| `archovive.slsa.provenance.json` | SLSA v1 — who, when, how built |
| `build_manifest.json` | SHA-256 of every file in bundle (~940 paths) |
| `archovive-enterprise-5.0.0.zip.sha256` | Release pin |
| cosign signatures | Keyless signing of CLI binary |

Verify before install:

```bash
sha256sum -c internal/releases/archovive-enterprise-5.0.0.zip.sha256
./archovive-enterprise-5.0.0/scripts/verify_signature.sh
```

*(Hashes live in `internal/releases/` — build pin, not end-user documentation.)*

---

## Signatures

| What | Algorithm | Where |
|------|-----------|-------|
| Policy packs | Ed25519 (`.json.sig`) | Enterprise bundle |
| Enterprise license | Ed25519 | `archovive_license.json` |
| Attestation | Ed25519 | `attestation.json` |
| CLI binary | cosign (keyless) | GitHub release |

Enterprise **fail-closed**: without valid license signature, no gov tier, no live dispatch.

---

## Evidence camera (enterprise)

```bash
archovive evidence
archovive camera evidence
```

MCP equivalents: `archovive.evidence`, `archovive.global`

Benchmark JSON (Flask, FastAPI, Django) in the bundle for global comparison matrices — `global_matrix.json`, `global_ranking.json`.

---

## Audit channel

Auditors and GRC boutiques can archive evidence packs **per repository / per release** — deterministic, repeatable, without re-analysis cost.

Indicative enterprise price: **€2,500 / certified repository / year** → [Chapter 08](../08-pricing/README.md)

---

**[← Docs hub](../README.md)** · **Next:** [06 — Air-gap](../06-airgap/README.md)
