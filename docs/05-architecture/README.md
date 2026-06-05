# 05 — Architecture Intelligence

## Hypergraph

Archovive kompiliert Polyglot-Repositories in einen **einheitlichen Architektur-Graphen** — Module, Kanten, Schichten.

Im OSS-Demo siehst du vereinfachte Metriken:

- `coupling_index` — Kanten pro Modul
- `boundary_crossings` — verbotene Schicht-Übergänge
- `instability_payments` — Domain-Instabilität

## Drift-Taxonomie

| Status | Bedeutung |
|--------|-----------|
| `unmeasured` | Erster Lauf — **kein Risiko-Signal** |
| gemessen | Abweichung gegen gespeicherte Baseline |

Erst nach `archovive init` / Baseline-Speicherung werden Drift-Scores meaningful.

## Monorepos

Compact Mode ab 500+ Dateien. Gleiche Determinismus-Garantie.

Production: `archovive diff old/ new/` vergleicht zwei Läufe.

→ [07 — Enterprise](../07-enterprise/README.md)
