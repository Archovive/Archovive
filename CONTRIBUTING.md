# Contributing

## Repository standard

Product-first layout: **everything at the repo root is OSS product**; **everything internal is under `internal/`**.

```
cli/ simulate/ examples/ docs/ dist/   ← product (users)
internal/                              ← build, releases, enterprise (not documented for users)
```

**Forbidden at root:** `scripts/`, `tools/`, `releases/`, `policy_packs/`, `pyproject.toml`, legacy `archovive/` folders.

| Change | Location |
|--------|----------|
| OSS CLI | `cli/` |
| Demo engine | `simulate/` |
| Demo repos | `examples/` |
| Product docs | `docs/01-intro/` … `docs/09-mcp/` |
| Install | `dist/install.sh` |
| Build / releases | `internal/` only |

CI enforces this: `make boundary` → `internal/scripts/verify_public_boundary.sh`

---

## Setup

```bash
make demo      # install + archovive simulate
make ci-demo   # ci check on demo (exit 2)
make test      # pytest
make boundary  # layout check
```

Gate output pins live in [`simulate/format.py`](simulate/format.py) — README and CLI must match.

---

## Pull requests

1. Scope changes to the product surface unless moving tooling into `internal/`
2. Run `make test` and `make boundary`
3. Update docs if CLI output changes

Security: `internal/SECURITY.md` · **security@archovive.com**
