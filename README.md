# Archovive — Local-First Architecture Governance

**In 30 Sekunden verstehen. In CI nutzen. On-prem skalieren.**

Archovive beantwortet eine Frage — mit reproduzierbarem Beweis:

> **Darf dieser Code-Stand released werden — und warum (oder warum nicht)?**

Nicht als Meinung. Nicht als Chat-Antwort. Sondern als **Verdict**, **Drift-Matrix** und **Evidence-Paket**, das Auditoren und CI gleichermaßen akzeptieren können.

---

## In 30 Sekunden testen

```bash
git clone https://github.com/Archovive/Archovive.git
cd Archovive
bash dist/install.sh
archovive simulate
```

Du siehst sofort: Architektur-Metriken → Drift-Status → Policy-Verdict → Replay-Hash.  
**Kein Enterprise-Bundle nötig** — das OSS-Demo läuft auf `examples/demo-fintech`.

---

## Dokumentation (in dieser Reihenfolge lesen)

| # | Kapitel | Für wen |
|---|---------|---------|
| 1 | [Was ist Archovive?](docs/01-intro/README.md) | Alle — Einstieg |
| 2 | [Simulate](docs/02-simulate/README.md) | Jeder, der sofort ein Ergebnis will |
| 3 | [CI-Gate](docs/03-ci/README.md) | Platform Engineering, DevOps |
| 4 | [Governance](docs/04-governance/README.md) | Tech Leads, Compliance Engineers |
| 5 | [Evidence](docs/05-evidence/README.md) | Auditoren, CRA/NIS2-Verantwortliche |
| 6 | [Air-gap](docs/06-airgap/README.md) | Behörden, KRITIS, Offline-Umgebungen |
| 7 | [Enterprise](docs/07-enterprise/README.md) | CISO, Procurement, Regulierte |
| 8 | [Pricing](docs/08-pricing/README.md) | Einkauf, Budget-Entscheider |

---

## Was du in diesem Repo siehst

| Pfad | Zweck |
|------|--------|
| `cli/` | OSS-Befehle: `simulate`, `ci check`, Router zum Enterprise-Bundle |
| `simulate/` | Demo-Engine — 30-Sekunden-Analyse ohne Cloud |
| `examples/demo-fintech/` | Beispiel-Repository mit absichtlichem Policy-Verstoß |
| `dist/` | `install.sh` und CLI-Wrapper |
| `docs/` | Produkt-Story, Kapitel 01–08 |

Build-Artefakte, Policy Packs, Release-Manifests und Enterprise-Installer liegen in **`internal/`** — nicht für Endnutzer.

---

## Enterprise (eigene Repositories)

Für Analyse **deiner** Codebases: frozen Offline-Bundle `archovive-enterprise-5.0.0.zip`  
→ [Kapitel 07 — Enterprise](docs/07-enterprise/README.md)

Sicherheitsmeldungen: `internal/SECURITY.md` · **security@archovive.com**

---

MIT [LICENSE](LICENSE)
