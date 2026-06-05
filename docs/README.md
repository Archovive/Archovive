# Archovive — Technical README

Decision substrate for release governance. One install, three tiers (`personal` | `team` | `enterprise`).

## Install

```bash
pip install archovive
# or editable monorepo:
pip install -e packages/archovive_engine -e "packages/archovive_runtime[store,auth,trust,mcp]" -e packages/archovive_evidence
pip install -e .
```

Enterprise Postgres requires the `store` extra: `pip install "archovive-os[store]"`.

## 60-second path

```bash
archovive setup              # tier + signing key + license
archovive onboard            # first decision (runs gate)
archovive trace <decision-id>
```

Discover docs programmatically:

```bash
archovive onboard --docs-only   # JSON: lexikon_path, tutorial_paths, tier
archovive spec link Terminology
```

## Enterprise

```bash
archovive setup --enterprise
archovive gate               # Dispatch line on stderr (sent / dry_run / failed)
archovive ops runtime doctor # Product tier, Pipeline tier, license, vendors
```

See [ENTERPRISE.md](ENTERPRISE.md) for integration matrix, guarantees, and production checklist.

## Environment

| Variable | Purpose |
|----------|---------|
| `ARCHOVIVE_PRODUCT` | `personal` (default), `team`, `enterprise` |
| `ARCHOVIVE_LICENSE_TIER` | Pipeline depth: `core`, `ci`, `gov` |
| `ARCHOVIVE_SIGNING_KEY_PATH` | Ed25519 key for signatures |
| `ARCHOVIVE_OIDC_ISSUER` | OIDC issuer URL (alias: `ARCHOVIVE_OIDC_ENDPOINT`) |
| `ARCHOVIVE_REPO` | Monorepo / analysis root override |
| `ARCHOVIVE_REPO_ALLOWLIST` | Comma-separated allowed repo paths (server/MCP) |

License file: `archovive_license.json` (enterprise requires valid Ed25519 signature).

## Spec CLI

```bash
archovive spec validate
archovive spec link Terminology
archovive spec procurement-pdf --out evidence/procurement/
```

## Exit codes (gate / onboard)

| Code | Meaning |
|------|---------|
| 0 | allow |
| 1 | block |
| 2 | warning / hold |
| 3 | engine error |
| 4 | misuse |

## Deploy profiles

| Tier | Profile |
|------|---------|
| personal | CLI only — `deploy/profiles/personal.yml` is a stub |
| team | `deploy/profiles/team.yml` |
| enterprise | `deploy/profiles/enterprise.yml` |

## Distribution

| Channel | Command |
|---------|---------|
| pip | `pip install archovive` |
| Offline bundle | `archovive bundle export --tier enterprise --out dist/` |
| Standalone binary | Roadmap — see `story/docs/ARCHOVIVE_BINARY_SUITE.md` |

## Docs in this package

- [LEXIKON.md](LEXIKON.md) — terminology (DE)
- [ENTERPRISE.md](ENTERPRISE.md) — honest enterprise contract
- [tutorials/](tutorials/) — personal / team / enterprise tracks

Spec spine: `archovive spec link Terminology`

## Finaler Nutzer-POV-E2E-Test

Nach `deploy/installers/build.sh` (Binaries unter `deploy/installers/dist/archovive/`):

```bash
bash scripts/run_final_user_pov_e2e.sh
```

- Führt alle Nutzeraktionen (CLI + MCP ping) aus
- Pro Tier zwei Läufe (Performance + Deterministik)
- Dumps: `dist/final_user_pov/` — `personal_run_1.txt`, `personal_run_2.txt`, `team_run_1.txt`, `team_run_2.txt`, `enterprise_run_1.txt`, `enterprise_run_2.txt`
