# Chapter 06 — Air-gap & offline

> **Architecture:** Offline bundle deploys the full kernel + surfaces without changing truth semantics — [01 System Architecture](../01_system_architecture.md).

**Navigation:** [Docs hub](../README.md) · Path C · [← Evidence](../05-evidence/README.md) · [Next: Enterprise →](../07-enterprise/README.md)

## Who is this chapter for?

**Government, KRITIS operators, defense suppliers, hospital IT, and any team** that **cannot use cloud scanners** — but still needs architecture governance and audit evidence.

**Surface sold:** frozen bundle CLI · no MCP cloud dependency · CI on isolated runners · `ARCHOVIVE_ISOLATED=1` for sidecar-only writes.

---

## Why air-gap?

Cloud SCM scanners fail when:

- Code must not leave the network
- Build runners are isolated
- Contracts require on-prem only
- Regulators mandate data residency

Archovive is **local-first by design** — no telemetry, no upload, no account.

```bash
export ARCHOVIVE_ISOLATED=1
archovive run   # enterprise bundle
```

---

## Frozen bundle

The enterprise product is a **PyInstaller binary** in a ZIP — **no Python** required on the target system:

```
archovive-enterprise-5.0.0/
  bin/archovive          ← CLI + MCP wrapper
  libexec/               ← Runtime (read-only)
  share/                 ← Docs, legal, templates
  scripts/               ← install.sh, verify_signature.sh
  metadata/              ← Manifest, provenance
```

**~63 MB**, offline-capable, Linux x86_64 (glibc 2.31+, WSL2 ok).

---

## Installation (enterprise)

1. Download GitHub release **v5.0.0**: ZIP + `.sha256` + SLSA
2. Run installer (after download, next to the ZIP):

```bash
bash internal/install_archovive.sh
source archovive.env
archovive doctor
```

3. Production: `/opt/archovive` via `scripts/install.sh` in the bundle — see [Chapter 07](../07-enterprise/README.md)

---

## Verify signature

**Before** first production run:

```bash
sha256sum -c archovive-enterprise-5.0.0.zip.sha256
./archovive-enterprise-5.0.0/scripts/verify_signature.sh
```

This checks: bundle integrity, manifest signature, policy pack registry — **supply-chain trust anchor**.

---

## Isolated mode

When the analysis repository is read-only or you want **no sidecar writes in the repo**:

```bash
export ARCHOVIVE_ISOLATED=1
archovive run
```

Preview output (enterprise bundle only) is documented above; not runnable from this OSS repo.

Cache, state, and sidecar data go only to XDG:

| Variable | Default (user) | System |
|----------|----------------|--------|
| `ARCHOVIVE_CONFIG` | `~/.config/archovive` | `/etc/archovive` |
| `ARCHOVIVE_CACHE` | `~/.cache/archovive` | `/var/cache/archovive` |
| `ARCHOVIVE_STATE` | `~/.local/state/archovive` | `/var/lib/archovive` |

The **install bundle stays immutable** — no writes into `/opt`.

---

## No telemetry

Archovive sends **nothing** to vendor servers. No telemetry. No "phone home" license check over the network in offline mode (license is locally signed).

---

## Typical air-gap workflow

```
1. ZIP + hashes via sneakernet into isolated zone
2. verify_signature.sh
3. setup_license.sh --system
4. archovive run / gate on internal Git mirror
5. Evidence JSON via export medium to audit zone
6. archovive verify attestation.json (no re-analysis)
```

---

**[← Docs hub](../README.md)** · **Next:** [07 — Enterprise](../07-enterprise/README.md)
