# Examples — Reference Fixtures

**Not surfaces · not tiers · not capabilities**

This directory holds **deterministic regression fixtures** — fixed repository snapshots that feed the kernel for CI pins, documentation demos, and DGPP parity proofs.

| Fixture | Role |
|---------|------|
| [`demo-fintech/`](demo-fintech/README.md) | OSS regression anchor — pinned `graph_hash` / `replay_hash` |

**Authority:** fixtures feed the kernel; they do not define product scope. NovaPay in `demo-fintech` is narrative pedagogy only.

Archovive evaluates arbitrary repositories via the [enterprise bundle](../docs/07-enterprise/README.md). See [Reference Fixtures spec](../docs/reference_fixtures_model.md) and [Decision Hub](../docs/00_decision_hub.md#reference-fixtures-orthogonal).

```bash
make demo                    # CLI projection on demo-fintech
make ci-demo                 # CI enforcement (exit 2)
archovive simulate --repo examples/demo-fintech
```
