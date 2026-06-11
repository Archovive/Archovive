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
| Product docs | **Entry:** `README.md` · **Index:** `docs/README.md` · **Evaluate:** `docs/evaluate/decision-hub.md` · **Specs:** `specs/00_kernel_truth_model.md` … `specs/06_kernel_contract_v1.md` · **Integrate:** `docs/integrate/ch-*.md` · **DGPP:** `specs/08_dgpp_parity_proof.md` |
| Kernel contract schemas | `schemas/` |
| Contract tests | `tests/test_surface_parity.py`, `tests/test_kernel_determinism.py`, `tests/test_evidence_consistency.py`, `tests/test_dgpp_governance_parity.py` |
| DGPP executive readout | `specs/08_dgpp_parity_proof.md` · `make dgpp` |
| Install | `dist/install.sh` |
| Build / releases | `internal/` only |

CI enforces this: `make boundary` → `internal/scripts/verify_public_boundary.sh`

---

## Setup

```bash
make demo      # install + archovive simulate
make ci-demo   # ci check on demo (exit 2)
make test      # pytest
make dgpp      # Deterministic Governance Parity Proof (executive gate)
make boundary  # layout check
```

Gate output pins live in [`simulate/format.py`](simulate/format.py) — README and CLI must match.

Kernel contract: [`specs/06_kernel_contract_v1.md`](specs/06_kernel_contract_v1.md) · run `make test` (includes parity + determinism tests).

---

## Pull requests

1. Scope changes to the product surface unless moving tooling into `internal/`
2. Run `make test` and `make boundary`
3. Update docs if CLI output changes

Security: `internal/SECURITY.md` · **security@archovive.com**
