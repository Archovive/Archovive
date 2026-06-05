# Kapitel 02 — Simulate (30 Sekunden)

## Für wen ist dieses Kapitel?

Für **Entwickler, Gründer und Evaluatoren**, die Archovive nicht glauben, sondern **sehen** wollen — ohne Enterprise-Vertrag, ohne Bundle-Download, ohne Sales-Call.

---

## Was passiert bei `simulate`?

Archovive analysiert das Demo-Repository `examples/demo-fintech` — NovaPay, eine fiktive Payments-API mit absichtlichen Schichtverstößen. Die Analyse läuft **lokal**, in wenigen Sekunden.

Standard-Ausgabe = **Produkt-Gate-Format** (identisch mit README). Mit `--verbose` siehst du Graph-Metriken, Drift und einzelne Policy-Regeln.

---

## Quickstart

### Option A — Einzeiler

```bash
git clone https://github.com/Archovive/Archovive.git
cd Archovive
bash dist/install.sh
```

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
archovive simulate              # Gate-Format (wie README)
archovive simulate --verbose    # Volle Analyse
archovive simulate --json       # Maschinenlesbar
archovive simulate --repo PATH  # Anderes Repo
```

Leerer Aufruf `archovive` ohne Argumente startet ebenfalls **simulate**.

---

## Beispiel-Output (v5.0.0, gepinnt)

Identisch mit [README](../../README.md#was-du-bekommst):

```text
$ archovive simulate

ARCHOVIVE GATE — DORA Boundary Crossing
Verdict: POLICY_VIOLATION
graph_hash: fee879ce…c734aa
replay_hash: 3e700b6a…d3b9736
Exit Code: 2
```

**Warum FAIL?** `services/api/routes.py` importiert `payments.ledger` direkt — layer boundary breach (DORA_2026).

---

## Simulate vs. Enterprise `run`

| | **OSS `simulate`** | **Enterprise `run`** |
|---|-------------------|----------------------|
| Zielgruppe | Evaluierung, Demos | Production CI/CD |
| Repo | Demo oder `--repo` | Beliebiges Repository |
| Output | Gate-Format + optional `--verbose` | Volle Artefakte + Attestation |
| Bundle nötig? | Nein | Ja |

---

**Nächstes Kapitel:** [03 — CI](../03-ci/README.md) — Simulate als Merge-Gate in GitHub Actions einbinden.
