# 04 — Tier constraints

**Truth layer** · [README](../README.md) · [Docs](../docs/README.md) · [← attestation_schema](03_attestation_schema.md) · [Next → invariants_and_determinism](05_invariants_and_determinism.md)

---

## Tier ordering {#tier-ordering}

Read product capabilities in this order:

1. **Surfaces** — how accessed (CLI · CI · MCP)
2. **Tiers** — what is licensed (Free · Team · Enterprise)
3. **Capabilities** — what is possible (drift · evidence · policy depth · offline · attestations)

Tiers constrain projections and persistence — they do not change kernel verdict logic for a given input. MCP is a query projection over the same kernel truth as CLI/CI; CI remains the enforcement surface for merge gates.

## Definition

**Tiers are projection constraints** applied in Repo A (product / licensing layer). They gate which surfaces, artifact writes, and policy pack depths are available to the operator. **Tiers are not kernel logic** — the kernel does not branch on Free vs Team vs Enterprise.

```
Tier → { allowed surfaces, allowed artifact writes, policy pack depth, license checks }
Kernel → DecisionRecord (unchanged)
```

## Two independent axes (enterprise bundle)

| Axis | Values | Controls |
|------|--------|----------|
| **Product tier** | personal · team · enterprise | Capability depth (coordination vs authority) |
| **Pipeline tier** | core · ci · gov | Evidence artifact depth |

Environment variables (bundle):

- `ARCHOVIVE_PRODUCT` — product tier
- `ARCHOVIVE_LICENSE_TIER` — pipeline tier

Default mapping at bundle export: team → pipeline `ci`; enterprise → pipeline `gov`.

The kernel truth for a given commit is identical across product tiers; only available projections and persistence differ.

## Repo A tiers (this repository)

This public repository documents and ships **Free-tier projections** only.

| Tier | Kernel | Surfaces available | Evidence persistence | Policy depth |
|------|--------|-------------------|----------------------|--------------|
| **Free (OSS)** | Demo kernel (`simulate/engine.py`) | CLI + CI on demo fixture | stdout / JSON only | 3 simplified packs |
| **Team** | Full kernel (bundle) | CLI + CI + MCP (`run_analysis`) | `repro.json`, `drift_matrix.json` | Full packs (unsigned) |
| **Enterprise** | Full kernel (bundle) | All surfaces + gov CLI | Full gov artifacts + signed attestations | Signed packs |

Team and Enterprise require `archovive-enterprise-5.0.0` bundle — not shipped as source in this repo.

## What tiers constrain

| Constraint type | Example |
|-----------------|---------|
| Surface availability | MCP server not in OSS repo |
| Artifact write permissions | `attestation.json` requires gov pipeline tier |
| Policy pack registry | OSS: 3 rules; bundle: full registry in `internal/policy_packs/` |
| License enforcement | Enterprise: Ed25519-signed `archovive_license.json`, fail-closed |
| Command routing | OSS stubs `run`, `verify`, … with bundle install message |

## What tiers do not constrain

- Kernel verdict computation for a given input tuple (when full kernel is installed)
- `replay_hash` identity across surfaces at the same commit
- DecisionRecord field semantics
- Invariants in [05_invariants_and_determinism.md](05_invariants_and_determinism.md)

## Capability projection matrix

Projection availability by tier (not kernel capability):

| Projection | Free | Team | Enterprise |
|------------|:----:|:----:|:----------:|
| CLI execute (demo / full) | demo | full | full |
| CI enforce | demo | full | full |
| MCP query | — | partial | full |
| Drift matrix persist | — | ✓ | ✓ |
| Attestation persist | — | — | ✓ |
| Offline bundle | — | — | ✓ |

## Product tier capabilities (bundle spec)

Authoritative capability vectors live in the enterprise bundle spec (`policy_vectors.json` in Archovive-core). Summary:

- **Personal (6 caps):** local materialize, explain, timeline, mcp_read, local_cache, optional_cloud_sync
- **Team (+6):** shared_projects, decision_feed, hitl_routing_lite, team_notifications, audit_visibility, swcps_lite
- **Enterprise (+8):** ci_enforce_readonly, authoritative_store, admission, epoch_authority, trust_rotation, distributed_authority, external_audit, global_enforcement

These are **authority and coordination gates** on projections, not kernel forks.

## OSS honesty requirements

Documentation in Repo A must not imply:

- Tiers change kernel verdict logic
- Free tier is a "toy" with different truth semantics (it uses a reduced **input scope**, not a different verdict model)
- MCP or attestations exist in OSS without bundle

Pricing and procurement context (non-architecture): [pricing](../docs/evaluate/pricing.md)

