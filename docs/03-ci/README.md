# Kapitel 03 — CI-Gate

## Für wen ist dieses Kapitel?

Für **Platform Engineers, DevOps und Release Manager**, die objektive Merge-Blocker wollen — Exit Codes statt Slack-Diskussionen, Drift und Policy **vor** dem Merge, nicht nach dem Incident.

---

## Das CI-Problem

Die meisten Pipelines prüfen:

- Unit Tests ✓
- Lint ✓
- SAST (Zeilen-Bugs) ✓

Was fehlt: **Architektur-Governance.**  
Niemand blockiert den Merge, wenn die API plötzlich die Payment-Ledger-Interna importiert — bis der Auditor oder ein Production-Vorfall kommt.

Archovive schließt diese Lücke mit **deterministischen Exit Codes**.

---

## Der Gate-Befehl

```bash
archovive ci check
```

| Exit Code | Bedeutung | CI-Aktion |
|-----------|-----------|-----------|
| **0** | Alle Policies bestanden | Merge erlaubt |
| **1** | Drift-Verstoß | Merge blockieren |
| **2** | Policy-/Regulierungs-Verstoß | Merge blockieren |
| **3** | Engine-Fehler | Pipeline rot, Investigation |
| **4** | Falsche Nutzung / fehlende Args | Pipeline-Konfiguration prüfen |

Auf dem **OSS-Demo-Repo** ist Exit **2** erwartet (DORA boundary crossing) — so testest du, dass deine Pipeline bei Verstößen wirklich stoppt.

---

## GitHub Actions — vollständiges Beispiel

```yaml
name: archovive-governance
on:
  pull_request:
    branches: [main]

jobs:
  architecture-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Archovive OSS
        run: pip install -e internal/

      - name: Architecture & policy gate
        run: |
          export PATH="$PWD/dist:$PATH"
          archovive ci check --repo examples/demo-fintech
        # Demo: exit 2 expected. Production: remove --repo, use enterprise bundle.

      - name: Upload evidence JSON
        if: always()
        run: |
          export PATH="$PWD/dist:$PATH"
          archovive simulate --json > archovive-evidence.json

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: archovive-evidence
          path: archovive-evidence.json
```

---

## Production CI (Enterprise-Bundle)

Mit installiertem Enterprise-Bundle auf **deinem** Repository:

```yaml
      - name: Archovive full analysis
        run: |
          source archovive.env
          archovive run
          archovive verify attestation.json
```

Artefakte (`repro.json`, `drift_matrix.json`, `attestation.json`) als Pipeline-Artifacts hochladen → Audit-Trail ohne manuellen Export.

---

## Reproducibility in CI

Archovives **funktionale SLA** (keine Latenz-SLA):

> Gleicher Commit + gleiche Policy-Packs → gleicher `replay_hash` auf jedem Runner.

Das bedeutet: CI-Ergebnisse sind **vergleichbar** zwischen Entwickler-Laptop, GitHub Actions und On-Prem-Runner — keine „works on my machine"-Governance.

---

## Übergang zu Governance

`ci check` im OSS-Modus nutzt vereinfachte Policy-Regeln auf dem Demo-Graph.  
Im Enterprise-Produkt kommen hinzu:

- Vollständige Policy Packs (DORA, NIS2, CRA, SOX) mit Ed25519-Signaturen
- Signierte Attestations
- Drift gegen gespeicherte Baseline
- Transparency Log

→ [Kapitel 04 — Governance](../04-governance/README.md)

---

**Nächstes Kapitel:** [04 — Governance](../04-governance/README.md) — Policies, Drift-Matrix und Verdicts im Detail.
