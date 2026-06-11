# Examples — Reference Fixtures

**Not surfaces · not tiers · not capabilities**

This directory holds **deterministic regression fixtures** — fixed repository snapshots that feed the kernel for CI pins, documentation demos, and DGPP parity proofs.

| Fixture | Role |
|---------|------|
| [`demo-fintech/`](demo-fintech/README.md) | OSS regression anchor — pinned `graph_hash` / `replay_hash` |

**Authority:** fixtures feed the kernel; they do not define product scope. NovaPay in `demo-fintech` is narrative pedagogy only.

Archovive evaluates arbitrary repositories via the [enterprise bundle](../docs/integrate/ch-07-enterprise.md). See [Reference fixtures spec](../specs/07_reference_fixtures.md).

```bash
make demo                    # CLI projection on demo-fintech
make ci-demo                 # CI enforcement (exit 2)
archovive simulate --repo examples/demo-fintech
```

[← README](../README.md) · [Try it](../README.md#try-it)
