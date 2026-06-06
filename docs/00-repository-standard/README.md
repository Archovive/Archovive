# Chapter 00 — Repository standard

## Who is this chapter for?

**Contributors, maintainers, and anyone asking “why is this repo laid out this way?”**  
End users can skip this — start at [Chapter 01 — Intro](../01-intro/README.md).

---

## Summary

Archovive uses a **simplified, product-first repository layout**. Everything visible at the root is part of the OSS product. Everything internal lives under `internal/`. This keeps the repository clean, predictable, and easy to adopt.

---

## Goals

| Goal | How the layout achieves it |
|------|------------------------------|
| Users see only the product | Public tree = CLI, simulate, examples, docs, dist, README, LICENSE |
| Internals strictly isolated | Build, release, enterprise artifacts → `internal/` only |
| Easy to understand / navigate / install / document / maintain | Linear docs 01–08, one install path, no root clutter |
| OSS adoption | No build-artifact dump at top level |

---

## 1. Public product surface (visible to users)

```
cli/              # Open-Core CLI (OSS)
simulate/         # Demo engine (OSS)
examples/         # Story-based demo repos
docs/             # Product story (English)
  00-repository-standard/
  01-intro … 08-pricing
  assets/
    gifs/         # committed demo GIFs
    demo/         # GIF regen scripts + VHS tapes
dist/             # install.sh + thin wrapper
README.md         # product landing
LICENSE           # MIT
.github/          # CI workflows (allowed at root)
```

**Rule:** Everything here is product. Everything here is for users. Everything here is part of the story.

---

## 2. Internal area (not for users)

```
internal/
    releases/         # enterprise bundle artifacts
    policy_packs/     # golden packs
    deploy/           # deploy profiles
    scripts/          # boundary checks, registry verify
    tools/            # internal utilities
    pyproject.toml    # pip install -e internal/
    MANIFEST.json     # build metadata
    RELEASE.lock.json # deterministic bundle lock
```

**Rule:** Not part of the OSS product. Not end-user documented. For build, release, enterprise.

---

## 3. Forbidden at repository root

| Forbidden | Action |
|-----------|--------|
| `archovive/` legacy folders | Delete or move to `internal/` |
| `releases/`, `policy_packs/` | → `internal/` |
| `scripts/`, `tools/` | → `internal/scripts/` or `docs/assets/demo/` (product media only) |
| Build artifacts, `*.egg-info/` | → `.gitignore` |
| `pyproject.toml`, `setup.cfg` at root | → `internal/` only |
| Old / duplicate docs | Delete |

**Rule:** If it is not product → `internal/`. If it is no longer needed → delete.

Demo GIF tooling lives under **`docs/assets/demo/`** — it produces user-visible product media and runs OSS commands only.

---

## 4. Why this layout improves Archovive

**A) OSS funnel maximally clear** — CLI, simulate, examples, docs, `install.sh`; zero distraction.

**B) Enterprise bundle isolated** — open-core done right.

**C) Docs linear, English, GIF-backed** — 01→08 product story; chapter 00 defines the repo itself.

**D) CI & release deterministic** — `internal/releases/` + `RELEASE.lock.json` + `MANIFEST.json` → reproducible bundles, simulate outputs, GIFs.

**E) Product, not monorepo waste** — a developer product, not a GitHub project dump.

---

## 5. Enforcement

CI runs [`internal/scripts/verify_public_boundary.sh`](../../internal/scripts/verify_public_boundary.sh) on every push — forbidden top-level paths fail the build.

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for where to put changes.

---

**Next chapter:** [01 — Intro](../01-intro/README.md) — what Archovive does in one minute.
