# Tutorial 03 — Enterprise live

**Goal:** Signed license, production stack, honest dispatch expectations.

## What “live” means

| Outcome | When |
|---------|------|
| `Dispatch: sent to …` | Vendor credentials configured **and** live enforcement enabled |
| `Dispatch: dry_run` | Enterprise tier but missing/incomplete vendor keys |
| `Dispatch failed: …` | Adapter error (shown on stderr; not silent) |

**Demo only (not production):** `ARCHOVIVE_STAGING_DEMO_LIVE=1` simulates `sent` without vendor calls.

Integration details: [../ENTERPRISE.md](../ENTERPRISE.md)

## Steps

```bash
archovive setup --enterprise
# enter PagerDuty, Slack, Jira, GitHub keys when prompted (optional per vendor)
archovive gate
# stderr: Dispatch: sent … | dry_run … | failed …
archovive audit export --bundle
```

Deploy:

```bash
cp deploy/profiles/.env.enterprise.example .env
# set ARCHOVIVE_API_TOKEN, POSTGRES_PASSWORD, ARCHOVIVE_SIGNING_KEY_PATH
# optional: ARCHOVIVE_OIDC_ISSUER=https://your-idp
docker compose -f deploy/profiles/enterprise.yml up -d
```

Server requires non-default `ARCHOVIVE_API_TOKEN` for enterprise/production (startup fail-closed).

## Verify

```bash
archovive ops runtime doctor
# Tier: enterprise
# Pipeline tier: gov
# License signature: OK
# Vendor keys: OK (N/N configured) or WARN
```

SIEM export (requires API auth): `GET /v1/product/ciso/siem-export` with `Authorization: Bearer $ARCHOVIVE_API_TOKEN`

Procurement:

```bash
archovive spec procurement-pdf --out evidence/procurement/
archovive bundle export --tier enterprise --out dist
```

## Vendor reality check

| Vendor | Adapter in product | Default deal-blocker E2E |
|--------|-------------------|--------------------------|
| PagerDuty | Yes | Manual with creds |
| Slack | Yes | Manual with creds |
| Jira | Yes | Manual with creds |
| ServiceNow | Yes | Manual with creds |

Do not assume all four show `sent` immediately after setup — configure keys and re-run `archovive gate`.
