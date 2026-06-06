# CLI — Archovive OSS

Public commands without the enterprise bundle:

| Command | Purpose |
|---------|---------|
| `archovive simulate` | 30s demo — graph, drift, policy, verdict |
| `archovive ci check` | CI gate (exit 2 on policy violation) |
| `archovive doctor` | Python + Git check |
| `archovive --help` | Overview |

Enterprise commands (`run`, `gate`, `verify`, …) delegate to the frozen bundle when installed.

Wrapper: `dist/archovive` · Install: `dist/install.sh`
