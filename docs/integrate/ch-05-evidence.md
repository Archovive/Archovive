# Evidence — export, verify, upload

**Integrate** · [README](../../README.md) · [Docs](../README.md) · [Evaluate](../evaluate/decision-hub.md) · [← 04-governance](ch-04-governance.md) · [Next → 06-airgap](ch-06-airgap.md)

Artifact definitions → [specs/03_attestation_schema.md](../../specs/03_attestation_schema.md) (`repro.json`, `attestation.json`)

---

## Export evidence bundle (enterprise)

```bash
archovive audit export --bundle   # gov tier
```

Writes kernel artifacts to the analysis directory. Tier gates which files are emitted — see attestation spec.

---

## Verify attestation (enterprise)

```bash
archovive verify attestation.json
```

Third parties verify signature and hash chain without re-scanning the repository.

---

## CI artifact upload

Capture CLI stdout or bundle-written files as pipeline artifacts:

```yaml
- run: archovive ci check --repo .
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: archovive-repro
    path: path/to/repro.json
```

Use `ci check`, not `simulate`, so process exit reflects the gate decision.

---

## MCP evidence tools (enterprise)

```bash
archovive evidence
archovive camera evidence
```

MCP: `archovive.evidence`, `archovive.global` — see [ch-09 MCP](ch-09-mcp.md).

---

## Release integrity (bundle install)

Before installing the enterprise bundle:

```bash
sha256sum -c internal/releases/archovive-enterprise-5.0.0.zip.sha256
./archovive-enterprise-5.0.0/scripts/verify_signature.sh
```

Release pins live in `internal/releases/`.

---
