# Tutorial 02 — Team coordination

**Goal:** Enable team surface and optional shared decision API.

## Steps

```bash
archovive setup --tier team
export ARCHOVIVE_PRODUCT=team   # or set in archovive_license.json
archovive team --help
archovive setup --ci --write --tier team
```

Optional API stack:

```bash
cp deploy/profiles/.env.team.example .env
docker compose -f deploy/profiles/team.yml up -d
```

## Expected

- `archovive ops runtime doctor` shows `Tier: team`, `12 enabled, 8 locked`
- CI workflow at `.github/workflows/archovive.yml`
