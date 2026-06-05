# Simulate — OSS Demo Engine

Dieses Modul implementiert die **30-Sekunden-Demo** ohne Enterprise-Bundle.

| Datei | Rolle |
|-------|--------|
| `engine.py` | Graph-Analyse + Policy-Auswertung |
| `runner.py` | CLI-Formatierung für `archovive simulate` |

**Demo-Fixture:** `examples/demo-fintech/` (12 Module, absichtlicher DORA-Verstoß)

**Dokumentation:** [docs/02-simulate/README.md](../docs/02-simulate/README.md)

**Gepinnte Hashes (v5.0.0):**

- `graph_hash`: `fee879ce6ea2d29634bde4f5f2d738e37a0bf409fb200d1d52009c1cd0c734aa`
- `replay_hash`: `3e700b6addb401281165f88810f6ade7f93cc7cf9f0ff985bd0390c79d3b9736`

Enterprise-Vollanalyse: `archovive run` mit frozen Bundle → [docs/07-enterprise](../docs/07-enterprise/README.md)
