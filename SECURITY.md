# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 5.0.x   | Yes       |
| 4.x     | End of life |

## Reporting

Report vulnerabilities to **security@archovive.com**. Do not open public issues for security findings.

## Supply chain

Enterprise releases ship:

- `archovive-enterprise-5.0.0.zip` with `metadata/sha256.txt`
- `archovive.slsa.provenance.json` (SLSA provenance)
- Optional cosign signatures on the frozen CLI binary

Verify before install:

```bash
sha256sum -c archovive-enterprise-5.0.0.zip.sha256
cd archovive-enterprise-5.0.0 && ./scripts/verify_signature.sh
```

## Trust boundaries

| Layer | Writable |
|-------|----------|
| Install root (`ARCHOVIVE_BUNDLE_ROOT`) | No |
| Config (`$XDG_CONFIG_HOME/archovive`) | Yes |
| Cache / state (XDG) | Yes |

See bundle `share/docs/SECURITY.md` after install.
