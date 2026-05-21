# Functional SLA (Open Core documentation)

Archovive does not publish a public **latency** SLA for the open-core CLI layer.

## Functional determinism SLA (gov tier, licensed engine)

For a fixed repository state, license tier, and engine version:

- `repro.json` `replay_hash` is stable across hosts (excluding documented volatile fields).
- Policy pack versions are recorded in `repro.json` (`policy_pack_versions`).
- Exit codes follow `MANIFEST.json`: 0 PASS, 1 drift, 2 regulatory, 3 engine, 4 misuse.

## Support tiers

| Tier | Coverage |
|------|----------|
| Open Core (this repo) | Best-effort community / docs issues on policy packs & specs |
| Commercial engine | Contractual support per pilot agreement |

See `PRICING.md` for indicative commercial tiers.
