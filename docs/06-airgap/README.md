# Kapitel 06 — Air-gap & Offline

## Für wen ist dieses Kapitel?

Für **Behörden, KRITIS-Betreiber, Defense-Zulieferer, Krankenhaus-IT und jedes Team**, das **keine Cloud-Scanner** einsetzen darf — aber trotzdem Architektur-Governance und Audit-Evidence braucht.

---

## Warum Air-gap?

Cloud-SCM-Scanner scheitern, wenn:

- Code das Netzwerk nicht verlassen darf
- Build-Runner isoliert sind
- Verträge „on-prem only" vorschreiben
- Regulatoren Data-Residency verlangen

Archovive ist **local-first by design** — kein Telemetry, kein Upload, kein Account.

---

## Frozen Bundle

Das Enterprise-Produkt ist ein **PyInstaller-Binary** in einer ZIP — **kein Python** auf dem Zielsystem nötig:

```
archovive-enterprise-5.0.0/
  bin/archovive          ← CLI + MCP-Wrapper
  libexec/               ← Runtime (read-only)
  share/                 ← Docs, Legal, Templates
  scripts/               ← install.sh, verify_signature.sh
  metadata/              ← Manifest, Provenance
```

**~63 MB**, offline-fähig, Linux x86_64 (glibc 2.31+, WSL2 ok).

---

## Installation (Enterprise)

1. GitHub Release **v5.0.0** herunterladen: ZIP + `.sha256` + SLSA
2. Installer ausführen (liegt nach Download neben der ZIP):

```bash
bash internal/install_archovive.sh
source archovive.env
archovive doctor
```

3. Produktion: `/opt/archovive` via `scripts/install.sh` im Bundle — siehe [Kapitel 07](../07-enterprise/README.md)

---

## Verify Signature

**Vor** dem ersten Produktiv-Lauf:

```bash
sha256sum -c archovive-enterprise-5.0.0.zip.sha256
./archovive-enterprise-5.0.0/scripts/verify_signature.sh
```

Damit prüfst du: Bundle-Integrität, Manifest-Signatur, Policy-Pack-Registry — **supply-chain trust anchor**.

---

## Isolated Mode

Wenn das Analyse-Repository read-only ist oder du **keine Sidecar-Writes** im Repo willst:

```bash
export ARCHOVIVE_ISOLATED=1
```

Cache, State und Sidecar-Daten gehen ausschließlich nach XDG:

| Variable | Default (User) | System |
|----------|----------------|--------|
| `ARCHOVIVE_CONFIG` | `~/.config/archovive` | `/etc/archovive` |
| `ARCHOVIVE_CACHE` | `~/.cache/archovive` | `/var/cache/archovive` |
| `ARCHOVIVE_STATE` | `~/.local/state/archovive` | `/var/lib/archovive` |

Das **Install-Bundle bleibt immutable** — keine Writes ins `/opt`-Verzeichnis.

---

## Kein Telemetry

Archovive sendet **nichts** an Vendor-Server. Keine Telemetrie. Keine „Phone Home"-Lizenzprüfung im Offline-Modus über das Netz (Lizenz ist lokal signiert).

---

## Typischer Air-gap-Workflow

```
1. ZIP + Hashes per Sneakernet in isolierte Zone
2. verify_signature.sh
3. setup_license.sh --system
4. archovive run / gate auf internem Git-Mirror
5. Evidence-JSON per Export-Medium an Audit-Zone
6. archovive verify attestation.json (ohne Re-Analyse)
```

---

**Nächstes Kapitel:** [07 — Enterprise](../07-enterprise/README.md) — Sidecar, Multi-Repo, DORA/NIS2/CRA im Vollbetrieb.
