# Kapitel 02 — Simulate (30 Sekunden)

## Für wen ist dieses Kapitel?

Für **Entwickler, Gründer und Evaluatoren**, die Archovive nicht glauben, sondern **sehen** wollen — ohne Enterprise-Vertrag, ohne Bundle-Download, ohne Sales-Call.

---

## Was passiert bei `simulate`?

Archovive analysiert das Demo-Repository `examples/demo-fintech` — ein kleines, aber realistisches Multi-Service-Layout (API, Payments, Notifications, Shared Layer). Die Analyse läuft **lokal**, in wenigen Sekunden, und liefert:

| Phase | Was du siehst |
|-------|----------------|
| **Architecture graph** | Module, Kopplung, Schicht-Grenzverletzungen |
| **Drift matrix** | Ob eine Baseline existiert (beim ersten Lauf: `unmeasured`) |
| **Policy evaluation** | DORA / NIS2 / GLOBAL — PASS oder FAIL pro Regel |
| **Verdict** | Gesamtentscheidung + Replay-Hash |

Der OSS-Demo zeigt bewusst einen **FAIL** — so siehst du, wie ein Blocker in CI aussehen würde.

---

## Quickstart

### Option A — Einzeiler

```bash
git clone https://github.com/Archovive/Archovive.git
cd Archovive
bash dist/install.sh
```

`install.sh` installiert die OSS-CLI und startet automatisch `archovive simulate`.

### Option B — Manuell

```bash
pip install -e internal/
export PATH="$PWD/dist:$PATH"
archovive simulate
```

**Voraussetzungen:** Python 3.11+, Git empfohlen.

---

## Befehle

```bash
archovive simulate              # Menschenlesbare Ausgabe
archovive simulate --json       # Maschinenlesbar (CI, jq, Audit-Tools)
archovive simulate --repo PATH  # Anderes Repo (OSS — vereinfachte Analyse)
```

Leerer Aufruf `archovive` ohne Argumente startet ebenfalls **simulate**.

---

## Beispiel-Output (v5.0.0, gepinnt)

```
=== Archovive Simulate (OSS demo) ===
Version .............. 5.0.0
Repository ............. demo-fintech
Modules .............. 12

[1/4] Architecture graph
  graph_hash ........... fee879ce6ea2d296…
  coupling_index ....... 0.833
  boundary_crossings ... 1
  instability (pay) .... 0.667

[2/4] Drift matrix
  drift_status ......... unmeasured
  drift_score .......... None

[3/4] Policy evaluation
  [PASS] GLOBAL_BASE :: global_coupling_max (value=0.833, threshold=1.2)
  [FAIL] DORA_2026 :: dora_crossings_max (value=1, threshold=0)
  [PASS] NIS2_MINIMAL_V1 :: nis2_instability_ceiling (value=0.667, threshold=0.8)

[4/4] Verdict
  verdict .............. POLICY_VIOLATION
  replay_hash .......... 3e700b6addb40128…
  exit_code ............ 2

Detected: DORA_2026 violation — dora_crossings_max (boundary_crossings=1).
```

**Warum FAIL?** In `services/api/routes.py` importiert die API-Schicht direkt `payments.ledger` — ein verbotener Querschnitt zwischen Präsentations- und Kern-Domain.

---

## Demo-Repository im Detail

```
examples/demo-fintech/
  services/api/          ← HTTP-Schicht (sollte nicht in Ledger greifen)
  services/payments/     ← Zahlungsdomäne
  services/notifications/
  shared/                ← Querschnitts-Config & Logging
  tests/
```

Das Repo ist **Absicht**, kein Produktionscode. Es existiert, damit du Output mit Dokumentation vergleichen kannst.

---

## Simulate vs. Enterprise `run`

| | **OSS `simulate`** | **Enterprise `run`** |
|---|-------------------|----------------------|
| Zielgruppe | Evaluierung, Demos | Production CI/CD |
| Repo | Demo oder `--repo` | Beliebiges Repository |
| Tiefe | Vereinfachter Graph | Voller Hypergraph, Polyglot |
| Artefakte | Terminal / JSON | MD, JSON, Attestation, SBOM |
| Bundle nötig? | Nein | Ja |

---

**Nächstes Kapitel:** [03 — CI](../03-ci/README.md) — Simulate als Merge-Gate in GitHub Actions einbinden.
