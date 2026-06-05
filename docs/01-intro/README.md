# Kapitel 01 — Was ist Archovive?

## Für wen ist dieses Kapitel?

Für **alle**, die in unter einer Minute verstehen wollen, was Archovive leistet — ohne Installationsanleitung, ohne Engine-Details, ohne Compliance-Fachjargon.

---

## Das Problem

Software-Teams stehen vor drei Lücken, die weder SAST noch GRC allein schließen:

### 1. Drift
Die implementierte Architektur weicht vom Soll ab — oft unbemerkt bis kurz vor dem Release. Code-Reviews sehen Dateien, nicht **Struktur**. Monorepos wachsen, Grenzen verschwimmen.

### 2. Evidence
Auditoren, Regulatoren und Kunden verlangen **nachweisbare** Artefakte: Was wurde geprüft? Gegen welche Regeln? Mit welchem Ergebnis? Wer hat wann zugestimmt? Screenshots und Word-Dokumente reichen nicht.

### 3. Compliance
DORA, NIS2, CRA und SOX verlangen **Software-Governance** — nicht nur IT-Sicherheit auf Einzelzeilen-Ebene. Gesetze kennen Architektur-Schichten. Scanner kennen Gesetze nicht.

---

## Die Lösung

**Archovive** ist eine **local-first Governance Engine**:

1. **Repository einlesen** → Architektur-Graph (Module, Abhängigkeiten, Schichten)
2. **Graph auswerten** → Drift gegen Baseline, Policy-Regeln (DORA, NIS2, …)
3. **Ergebnis materialisieren** → Verdict, Hashes, Evidence-Paket

Alles **on-prem**. Kein Code-Upload in die Cloud. Kein Telemetry.  
Gleicher Repository-Stand → gleicher Output (**Determinismus**).

---

## Warum nicht SonarQube / Vanta?

**SonarQube** findet Zeilen-Bugs. **Vanta** verwaltet Checklisten.  
**Archovive** analysiert deine Architektur als Graph und entscheidet deterministisch: *darf dieser Stand released werden* — mit signierten Beweisen.

Das ist keine Ersetzung für SAST oder GRC-Tools. Es ist die **Lücke dazwischen**: Architektur + Regulierung + reproduzierbares Evidence.

---

## Was Archovive nicht ist

- Kein Cloud-SaaS-Scanner
- Kein Ersatz für Zeile-für-Zeile-Bugfinding (SAST)
- Keine Checklisten-App ohne Code-Anbindung
- Keine generische KI-Suche — `ask`/`chat` im Enterprise-Produkt sind **deterministische Governance-Oberflächen** auf demselben Kernel

---

## 30-Sekunden-Demo (Beispiel-Output)

```text
$ archovive simulate

ARCHOVIVE GATE — DORA Boundary Crossing
Verdict: POLICY_VIOLATION
graph_hash: fee879ce…c734aa
replay_hash: 3e700b6a…d3b9736
Exit Code: 2
```

Das Demo-Repo ist eine absichtlich fehlerhafte Fintech-Microservice-Struktur — Details in [examples/demo-fintech](../../examples/demo-fintech/README.md).

---

## Wer profitiert wann?

| Rolle | Typischer Einstieg |
|-------|-------------------|
| Entwickler / Tech Lead | Kapitel 02 — Simulate |
| Platform / DevOps | Kapitel 03 — CI-Gate |
| Compliance / GRC | Kapitel 04–05 — Governance & Evidence |
| CISO / Enterprise | Kapitel 07 — Enterprise-Bundle |

---

**Nächstes Kapitel:** [02 — Simulate](../02-simulate/README.md) — Demo in 30 Sekunden auf deinem Rechner ausführen.
