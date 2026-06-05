# Archovive — Local-First Architecture Governance

**In 30 Sekunden verstehen, in CI nutzen, on-prem skalieren.**

Archovive beantwortet eine Frage mit reproduzierbarem Beweis:

> *Darf dieser Code-Stand released werden — und warum?*

---

## Sofort testen

```bash
git clone https://github.com/Archovive/Archovive.git
cd Archovive
bash dist/install.sh
archovive simulate
```

Du siehst: Architektur-Graph → Drift-Matrix → Policy-Verdict → Replay-Hash.  
Kein Enterprise-Bundle nötig.

---

## Dokumentation (Story, nicht Technik-Handbuch)

| Kapitel | Inhalt |
|---------|--------|
| [01 — Intro](docs/01-intro/README.md) | Problem & Lösung |
| [02 — Simulate](docs/02-simulate/README.md) | 30-Sekunden-Demo |
| [03 — CI](docs/03-ci/README.md) | `archovive ci check` in Pipeline |
| [04 — Governance](docs/04-governance/README.md) | Evidence, Attestations, SLSA |
| [05 — Architecture](docs/05-architecture/README.md) | Hypergraph, Drift, Monorepos |
| [06 — Air-gap](docs/06-airgap/README.md) | Offline, signiertes Bundle |
| [07 — Enterprise](docs/07-enterprise/README.md) | DORA, NIS2, CRA, Multi-Repo |
| [08 — Pricing](docs/08-pricing/README.md) | OSS, Team, Enterprise |

---

## Was dieses Repo ist — und was nicht

**Produkt (sichtbar):** `archovive/` CLI + Simulate, `examples/`, `docs/`, `dist/`  
**Intern (Build):** `internal/` — Releases, Policy Packs, Deploy, Manifests

Engine & frozen Binary: **Archovive-core** (Commercial).  
Enterprise-Install: [docs/07-enterprise](docs/07-enterprise/README.md)

[SECURITY.md](SECURITY.md) · MIT [LICENSE](LICENSE)
