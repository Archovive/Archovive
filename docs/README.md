# Archovive — Customer Guide (v5)

Enterprise governance CLI — frozen offline install, no Python venv.

## Install

1. Clone [Archovive/Archovive](https://github.com/Archovive/Archovive)
2. Download **Release v5.0.0** assets beside `install_archovive.sh`
3. Run `./install_archovive.sh` and `source ./archovive.env`

Details: [INSTALL.md](INSTALL.md) | Release notes: [RELEASE_NOTES_v5.0.0.md](RELEASE_NOTES_v5.0.0.md)

## First commands

```bash
archovive --version
archovive doctor
archovive ask "why blocked?"
archovive governance decide --json
```

## Tiers

| Tier | `ARCHOVIVE_PRODUCT` |
|------|---------------------|
| Personal | `personal` |
| Team | `team` |
| Enterprise | `enterprise` (default in bundle) |

Profiles: `deploy/profiles/`

## Docs

| Doc | Topic |
|-----|-------|
| [LEXIKON.md](LEXIKON.md) | Terminology |
| [ENTERPRISE.md](ENTERPRISE.md) | Enterprise integration |
| [INSTALL.md](INSTALL.md) | Install & MCP |
| tutorials/ | Step-by-step |

Engine source and binary builds: **Archovive-core** (private).
