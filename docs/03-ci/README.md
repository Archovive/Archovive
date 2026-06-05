# 03 — In CI nutzen

## Gate-Befehl

```bash
archovive ci check
```

| Exit Code | Bedeutung |
|-----------|-----------|
| 0 | Policy bestanden |
| 2 | Policy-Verstoß (Merge blockieren) |

Auf dem Demo-Repo ist Exit **2** erwartet (DORA boundary crossing).

## GitHub Actions

```yaml
name: archovive-gate
on: [pull_request]
jobs:
  governance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e internal/
      - run: |
          export PATH="$PWD/dist:$PATH"
          archovive ci check
```

## Production CI (Enterprise)

Mit installiertem Enterprise-Bundle:

```bash
archovive run
archovive verify attestation.json
```

Exit Codes: 0 Pass · 1 Drift · 2 Policy · 3 Engine

→ [04 — Governance](../04-governance/README.md)
