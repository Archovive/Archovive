# Contributing to Archovive (public repo)

Thank you for improving the OSS product surface. Read [docs/00-repository-standard](docs/00-repository-standard/README.md) first — it defines where everything belongs.

## Repository layout

| Change type | Location |
|-------------|----------|
| OSS CLI commands | `cli/` |
| Demo engine (`simulate`) | `simulate/` |
| Demo repositories | `examples/` |
| Product docs (English) | `docs/01-intro/` … `docs/08-pricing/` |
| Demo GIFs (committed) | `docs/assets/gifs/` |
| GIF regen scripts + VHS tapes | `docs/assets/demo/` |
| Install entrypoint | `dist/install.sh` |
| Build, releases, policy packs | `internal/` only |

**Do not add** top-level `scripts/`, `tools/`, `releases/`, `policy_packs/`, or root `pyproject.toml`.

## Development setup

```bash
git clone https://github.com/Archovive/Archovive.git
cd Archovive
pip install -e internal/
export PATH="$PWD/dist:$PATH"
archovive simulate
```

## Tests

```bash
python -m pytest cli/tests -q
bash internal/scripts/verify_public_boundary.sh
```

## Regenerating demo GIFs

GIFs are committed artifacts. Regenerate locally before doc commits:

```bash
# install VHS once
go install github.com/charmbracelet/vhs@latest

# regenerate all GIFs
bash docs/assets/demo/build_gifs.sh
```

Fallback (no VHS): `python3 docs/assets/demo/build_gifs.py`

See [docs/assets/gifs/README.md](docs/assets/gifs/README.md).

## Documentation

- Product story chapters: English, “Who is this chapter for?” / “Next chapter:”
- OSS vs enterprise bundle: be precise — do not claim bundle commands work without the bundle
- Gate output must match [`simulate/format.py`](simulate/format.py) pins

## Pull requests

1. Keep changes scoped to the product surface unless moving build tooling into `internal/`
2. Run `pytest cli/tests -q` and `verify_public_boundary.sh`
3. Update docs if CLI output or layout changes

Security: `internal/SECURITY.md` · **security@archovive.com**
