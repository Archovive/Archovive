# Enterprise

**Integrate** · [README](../../README.md) · [Docs](../README.md) · [Evaluate](../evaluate/decision-hub.md) · [← 06-airgap](ch-06-airgap.md) · [Next → 09-mcp](ch-09-mcp.md)

---

## Who is this chapter for?

**CISO, head of compliance, procurement, and platform leads in regulated companies** deploying Archovive on **their own repositories** — with signed license, live dispatch, multi-repo governance, and full audit trail.

---

## When OSS is not enough

| Requirement | OSS | Enterprise |
|-------------|-----|------------|
| Demo / evaluation | ✓ | ✓ |
| CI on your code | — | ✓ |
| Polyglot hypergraph | — | ✓ |
| Signed attestations | — | ✓ |
| Full DORA/NIS2/CRA packs | — | ✓ |
| Live dispatch (PagerDuty, SIEM) | — | ✓ |
| Authoritative decision store | — | ✓ |

**Free tier (OSS)** = evaluate determinism on the pinned regression fixture. **Production** = enterprise bundle on **your** repository.

→ [Enterprise evaluation — OSS vs bundle](../evaluate/decision-hub.md#oss-vs-bundle-readiness)

```bash
archovive run --compact   # enterprise bundle
```

---

## Sidecar architecture (v5)

The bundle under `/opt/archovive` is **read-only**. All writes go to sidecar layers:

```
/opt/archovive/                    ← immutable binary + share/
/etc/archovive/                    ← license, system config
/var/lib/archovive/                ← state, transparency log, vault
/var/cache/archovive/              ← IR cache, SBOM scratch
~/.config/archovive/               ← user overrides (dev)
```

**Why:** immutable install = supply-chain trust. Sidecar = operational repeatability without bundle mutation.

---

## Installation (short)

```bash
# 1. Release assets from GitHub (v5.0.0)
# 2. Installer
bash internal/install_archovive.sh
source archovive.env

# 3. License (enterprise — signed, required)
./archovive-enterprise-5.0.0/scripts/setup_license.sh --system

# 4. Health
archovive ops runtime doctor
```

Engine access: **enterprise@archovive.com**

---

## Multi-repo governance

| Tool | Purpose | Surface |
|------|---------|---------|
| `archovive-fleet` | Batch analysis across repos | CLI |
| `archovive gate` | Release decision per repo | CLI + CI |
| Matrix / CI | Deterministic orchestration | CI |
| MCP `run_analysis` | IDE integration (Cursor, etc.) | MCP (enterprise bundle) |
| MCP `archovive.evidence` | Auditor view in IDE | MCP |

Full MCP setup → [MCP](../integrate/ch-09-mcp.md).

Tier depth → [04 Tier constraints](../../specs/04_tier_constraints.md) · [Enterprise evaluation](../evaluate/decision-hub.md) · [08 — Pricing](../evaluate/pricing.md).

---

## Audit trails

Enterprise materializes:

- **Transparency log** — append-only (`transparency_log.jsonl`)
- **Vault store** — decision history
- **Decision contract chain** — schema → verify → RBAC → upload gate
- **SIEM export** — JSONL/CEF, optional real-time HEC
- **`archovive audit export --bundle`** — 6-field ledger for revision

---

## Regulatory frameworks

| Framework | Policy pack | Archovive contribution |
|-----------|-------------|------------------------|
| **DORA** | `DORA_2026`, `DORA_MINIMAL_V1` | Critical-path isolation, layer boundaries |
| **NIS2** | `NIS2_MINIMAL_V1` | Boundary crossings, instability ceilings |
| **CRA** | `CRA_MINIMAL_V1` | Security reachability, Annex IV stubs |
| **SOX** | `SOX_2026` | ITGC architecture thresholds |

Archovive **does not certify regulation** — it delivers **technical evidence** auditors evaluate.

---

## Integrations (enterprise)

With credentials **live**, without credentials **dry_run**:

PagerDuty · Slack · Jira · ServiceNow · GitHub · SIEM · OIDC · K8s admission (Kyverno)

Dispatch status on stderr: `sent` · `dry_run` · `failed`

---

## Procurement artifacts

```bash
archovive spec procurement-pdf --out evidence/procurement/
archovive bundle export --tier enterprise --out dist/
archovive audit export --bundle
```

---
