# Tutorial 01 — First decision (Personal)

**Goal:** Materialize your first release decision in under 60 seconds.

## Prerequisites

- Python 3.11+
- Git repository at cwd

## Steps

```bash
archovive setup
archovive onboard
archovive trace <decision-id-from-output>
```

Optional interactive demo:

```bash
archovive simulate --pause
archovive gate
```

## Expected artifacts

- `.archovive/config.toml` — tier and signing key
- `archovive_license.json` — product entitlements
- Local decision contract in `.archovive/`

## Troubleshooting

- `archovive ops runtime doctor`
- See [../README.md](../README.md)
