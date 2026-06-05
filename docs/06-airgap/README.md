# 06 — Air-gapped & Offline

## Frozen Bundle

`archovive-enterprise-5.0.0.zip` — PyInstaller-Binary, **kein Python**, kein Netzwerk.

```bash
bash internal/install_archovive.sh   # nach Download von GitHub Release
source archovive.env
archovive doctor
```

## Verify vor Nutzung

```bash
./archovive-enterprise-5.0.0/scripts/verify_signature.sh
sha256sum -c releases/archovive-enterprise-5.0.0.zip.sha256
```

Hashes & Provenance: `internal/releases/` (Build-Pin).

## Isolated Mode

```bash
export ARCHOVIVE_ISOLATED=1
```

Schreibt nur in XDG-Pfade — Bundle bleibt read-only.

## Kein Telemetry

Keine Cloud-Anbindung. Keine Telemetrie. Local-first by design.

→ [07 — Enterprise](../07-enterprise/README.md)
