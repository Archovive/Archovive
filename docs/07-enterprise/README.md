# Kapitel 07 — Enterprise

## Für wen ist dieses Kapitel?

Für **CISO, Head of Compliance, Procurement und Platform-Leads in regulierten Unternehmen**, die Archovive auf **eigenen Repositories** produktiv einsetzen — mit signierter Lizenz, Live-Dispatch, Multi-Repo-Governance und vollständigem Audit-Trail.

---

## Wann reicht OSS nicht?

| Anforderung | OSS | Enterprise |
|-------------|-----|------------|
| Demo / Evaluierung | ✓ | ✓ |
| CI auf eigenem Code | — | ✓ |
| Polyglot-Hypergraph | — | ✓ |
| Signierte Attestations | — | ✓ |
| DORA/NIS2/CRA volle Packs | — | ✓ |
| Live-Dispatch (PagerDuty, SIEM) | — | ✓ |
| Authoritative Decision Store | — | ✓ |

OSS = **Funnel**. Enterprise = **Produktion**.

---

## Sidecar-Architektur (v5)

Das Bundle unter `/opt/archovive` ist **read-only**. Alle Writes gehen in Sidecar-Layer:

```
/opt/archovive/                    ← immutable binary + share/
/etc/archovive/                    ← Lizenz, System-Config
/var/lib/archovive/                ← State, Transparency Log, Vault
/var/cache/archovive/              ← IR-Cache, SBOM-Scratch
~/.config/archovive/               ← User-Overrides (Dev)
```

**Warum:** Immutable Install = supply-chain trust. Sidecar = operative Wiederholbarkeit ohne Bundle-Mutation.

---

## Installation (Kurz)

```bash
# 1. Release-Assets von GitHub (v5.0.0)
# 2. Installer
bash internal/install_archovive.sh
source archovive.env

# 3. Lizenz (Enterprise — signiert, Pflicht)
./archovive-enterprise-5.0.0/scripts/setup_license.sh --system

# 4. Health
archovive ops runtime doctor
```

Kontakt Engine-Zugang: **enterprise@archovive.com**

---

## Multi-Repo Governance

| Tool | Zweck |
|------|--------|
| `archovive-fleet` | Batch-Analyse mehrerer Repos (internes Tool) |
| `archovive gate` | Release-Entscheidung pro Repo |
| Matrix / CI | Deterministische Orchestrierung über Repos |
| MCP `archovive.run_analysis` | IDE-Integration (Cursor, etc.) |

Product Tiers:

| Tier | Capabilities | Typisch |
|------|-------------|---------|
| **personal** | 6 | Einzelentwickler |
| **team** | 12 | Team Feed, Decision API |
| **enterprise** | 20 | Authoritative Store, Live Dispatch |

Pipeline Tiers (Lizenz-Tiefe): **core** → **ci** → **gov**

---

## Audit Trails

Enterprise materialisiert:

- **Transparency Log** — append-only (`transparency_log.jsonl`)
- **Vault Store** — Entscheidungs-Historie
- **Decision Contract Chain** — schema → verify → RBAC → upload gate
- **SIEM Export** — JSONL/CEF, optional Real-time HEC
- **`archovive audit export --bundle`** — 6-Feld-Ledger für Revision

---

## Regulatorische Frameworks

| Framework | Policy Pack | Archovive-Beitrag |
|-----------|-------------|-------------------|
| **DORA** | `DORA_2026`, `DORA_MINIMAL_V1` | Critical-path isolation, Layer boundaries |
| **NIS2** | `NIS2_MINIMAL_V1` | Boundary crossings, Instability ceilings |
| **CRA** | `CRA_MINIMAL_V1` | Security reachability, Annex-IV-Stubs |
| **SOX** | `SOX_2026` | ITGC-Architektur-Schwellen |

Archovive **zertifiziert keine Regulierung** — es liefert **technische Evidence**, die Prüfer bewerten.

---

## Integrationen (Enterprise)

Mit Credentials **live**, ohne Credentials **dry_run**:

PagerDuty · Slack · Jira · ServiceNow · GitHub · SIEM · OIDC · K8s Admission (Kyverno)

Dispatch-Status auf stderr: `sent` · `dry_run` · `failed`

---

## Procurement-Artefakte

```bash
archovive spec procurement-pdf --out evidence/procurement/
archovive bundle export --tier enterprise --out dist/
archovive audit export --bundle
```

---

**Nächstes Kapitel:** [08 — Pricing](../08-pricing/README.md) — OSS, Team, Enterprise und Value Proposition.
