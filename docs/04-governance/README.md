# Kapitel 04 — Governance

## Für wen ist dieses Kapitel?

Für **Tech Leads, Compliance Engineers und Architekten**, die verstehen müssen, wie Archovive von „Code-Graph" zu **regulatorischem Verdict** kommt — und was in `attestation.json` und `compliance_report.json` steckt.

---

## Governance in einem Satz

Archovive übersetzt **Architektur-Zustand** in **regulatorische Aussagen** — mit Regeln, die reproduzierbar, versioniert und signierbar sind.

---

## Policy Packs

Policy Packs sind **keine Checklisten in Excel**. Sie sind maschinenlesbare Regelsets, die auf Graph-Metriken operieren:

| Pack | Framework | Beispiel-Regel |
|------|-----------|----------------|
| `GLOBAL_BASE` | Architektur-Baseline | Kopplung ≤ Schwellwert |
| `DORA_2026` | DORA | Schicht-Grenzüberschreitungen = 0 |
| `NIS2_MINIMAL_V1` | NIS2 | Instabilität kritischer Domains |
| `CRA_MINIMAL_V1` | CRA | Security-Reachability, SBOM-Stubs |
| `SOX_2026` | SOX ITGC | Coupling / Boundary für Finanz-IT |

Im OSS-Demo werden drei Regeln live ausgewertet. Im Enterprise-Bundle: alle Packs inkl. Ed25519-`.json.sig`-Signaturen.

**Warum das der Moat ist:** SAST-Tools kennen keine DORA-Artikel. GRC-Tools kompilieren kein Repository in einen Graph. Archovive verbindet beides.

---

## Drift-Matrix

Die Drift-Matrix beschreibt **Abweichung gegen eine gespeicherte Baseline**:

| Feld | Bedeutung |
|------|-----------|
| `drift_status: unmeasured` | Erster Lauf — **kein Risiko-Signal**, nur neutral |
| `drift_status: measured` | Baseline vorhanden — Abweichung berechnet |
| `drift_score: null` | Kein numerischer Score ohne Baseline |
| `drift_score: 0.0–1.0` | Nur mit Baseline — höher = mehr strukturelle Abweichung |

**Wichtig:** `unmeasured` oder `null` bedeutet **nicht** „mittleres Risiko". Erst nach `archovive init` / Baseline-Speicherung werden Drift-Scores meaningful.

Strukturelle Klassen (Enterprise): topologisch, semantisch, verhaltensbasiert — in `drift_matrix.json`.

---

## Verdicts

| Verdict | Bedeutung | Typische CI-Reaktion |
|---------|-----------|---------------------|
| `APPROVED` | Alle Policies bestanden | Merge / Release freigeben |
| `POLICY_VIOLATION` | Regulatorische Regel verletzt | Exit 2 — blockieren |
| `DRIFT_VIOLATION` | Architektur weicht von Baseline ab | Exit 1 — blockieren |
| `OVERRIDE_REQUIRED` | Menschliche Entscheidung nötig | Workflow / Ticket |

Im Enterprise-Produkt materialisiert `archovive gate` den Verdict als **Decision Contract** — signiertes JSON mit `decision_id`, `lookup_key`, Zeitstempel.

---

## Evidence-Modell (Überblick)

Governance erzeugt ein **Evidence-Set** — maschinenlesbar, verknüpft, hash-verkettet:

```
Repository
    → Graph (graph_hash)
    → Policy Results (compliance_report.json)
    → Verdict (attestation.json)
    → Replay Pin (repro.json / replay_hash)
```

Die drei **Kameras** (Perspektiven auf dasselbe Ergebnis):

| Kamera | Zielgruppe | Haupt-Artefakt |
|--------|------------|----------------|
| **Operator** | Menschen | `ARCHOVIVE_OUTPUT.md` |
| **Machine** | CI/CD | `repro.json`, `drift_matrix.json` |
| **Evidence** | Auditoren | `attestation.json`, SBOM, Verify-Chain |

Details → [Kapitel 05 — Evidence](../05-evidence/README.md)

---

## Truth Surfaces (Enterprise)

Diese drei Befehle **müssen identische Antworten** liefern — Paritäts-Garantie:

```bash
archovive ask "why blocked?"
archovive chat "why blocked?"
archovive governance decide --json
```

Kein separates „Chat-Wissen". Eine Kernel-Wahrheit, mehrere Oberflächen.

---

**Nächstes Kapitel:** [05 — Evidence](../05-evidence/README.md) — Attestations, SLSA und Signaturen für Auditoren.
