# Kapitel 08 — Pricing & Tiers

## Für wen ist dieses Kapitel?

Für **Budget-Entscheider, Einkauf und Gründer**, die verstehen wollen, was kostenlos ist, was skaliert und **warum** Enterprise mehr kostet als ein Scanner-Abo.

*Indikativ — nicht vertraglich. Verbindliche Angebote: **enterprise@archovive.com***

---

## Value Proposition

Archovive liefert **deterministische, offline-fähige Architektur-Evidence** — ohne Code zu ändern, ohne Daten in die Cloud zu senden.

| Outcome | Nutzen |
|---------|--------|
| **CI-Gates** | Objektive Exit Codes statt Meinungs-Diskussionen |
| **Audit-Evidence** | Signierte Attestations statt manueller Reviews |
| **Regulatory Bridge** | DORA/NIS2/CRA-Regeln auf Graph-Ebene — nicht nur Checklisten |

**Moat:** Regulatorische Policy Packs → Graph-Invarianten. SAST kennt keine Gesetze. GRC kompiliert kein Repository.

---

## OSS (dieses Repository)

| | |
|---|---|
| **Preis** | **Kostenlos** (MIT) |
| **Enthält** | `simulate`, `ci check`, Demo-Repo, Story-Docs |
| **Limit** | Vereinfachte Analyse, kein voller Hypergraph, keine Attestations |
| **Ideal für** | Evaluierung, Developer Adoption, CI-Pattern lernen |

```bash
bash dist/install.sh && archovive simulate
```

---

## Team / CI

| | |
|---|---|
| **Preis** | **Kostenlos** für Open Source; **€49 / Dev / Monat** kommerziell (KMU) |
| **Enthält** | `repro.json`, `drift_matrix.json`, CI Exit Codes |
| **Ideal für** | Platform Engineering, Scale-ups, Monorepo-Teams |
| **Schmerz** | „Wir wissen nicht, ob die Architektur noch stimmt" |

Kein CISO nötig. Ein DevOps-Lead reicht als Champion.

---

## Enterprise / Gov

| | |
|---|---|
| **Preis** | **€2.500 / zertifiziertes Repository / Jahr** (unbegrenzte Attestations) |
| **Enthält** | Attestations, Compliance Reports, Vault, Transparency Log, Live-Dispatch |
| **Ideal für** | Regulierte Unternehmen, Banken, Audit-Kanäle |
| **Schmerz** | DORA/NIS2/CRA-Deadline, Audit-Vorbereitung, Release-Governance |

Pricing-Dimensionen (Enterprise-Verhandlung): Repo-Anzahl, CI-Seats, Support-SLA, Signing Key Ceremony.

---

## SLA

| | OSS | Enterprise |
|---|-----|------------|
| **Latenz** | Keine Garantie | Keine Latenz-SLA |
| **Determinismus** | Demo-gepinnt | **Funktionale SLA:** gleicher Stand → gleicher `replay_hash` |
| **Support** | Community / Docs | enterprise@archovive.com |

---

## Segment-Matrix

| Segment | Tier | Einstiegs-Kapitel |
|---------|------|-------------------|
| Developer / Evaluator | OSS | 01, 02 |
| Platform Engineering | Team/CI | 03 |
| CRA/NIS2 Vendor | Gov | 04, 05 |
| Air-gap / Behörde | Enterprise | 06, 07 |
| Bank / DORA | Enterprise | 07 |
| Audit-Boutique | Gov (pro Mandant) | 05, 07 |

---

## Pilotphase

**Läuft bis Ende 2026** — erste **5 Monate kostenlos** für qualifizierte Piloten (regulierte Industrie, Platform-Teams mit CI-Mandat, Audit-Kanäle).

Was du bekommst:

- Enterprise-Bundle auf **deinem** Repository (nicht nur Demo)
- Begleitung beim CI-Gate-Setup
- Evidence-Packs für interne oder externe Auditoren

**Interesse?** → **pilot@archovive.com**  
Betreff: `Pilot` + Branche + ungefähre Repo-Größe. Antwort innerhalb von 2 Werktagen.

Allgemeine Enterprise-Anfragen: enterprise@archovive.com

---

## Nächste Schritte

1. **Noch unsicher?** → [02 — Simulate](../02-simulate/README.md)
2. **CI einbinden?** → [03 — CI](../03-ci/README.md)
3. **Enterprise ohne Pilot?** → enterprise@archovive.com

---

**Nächstes Kapitel:** [01 — Intro](../01-intro/README.md) — zurück zum Einstieg (oder Demo starten: `archovive simulate`).
