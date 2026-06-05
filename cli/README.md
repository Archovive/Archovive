# CLI — Archovive OSS

Öffentliche Befehle ohne Enterprise-Bundle:

| Befehl | Funktion |
|--------|----------|
| `archovive simulate` | 30s-Demo — Graph, Drift, Policy, Verdict |
| `archovive ci check` | CI-Gate (Exit 2 bei Policy-Verstoß) |
| `archovive doctor` | Python + Git Check |
| `archovive --help` | Übersicht |

Enterprise-Befehle (`run`, `gate`, `verify`, …) delegieren an das frozen Bundle, wenn installiert.

Wrapper: `dist/archovive` · Install: `dist/install.sh`
