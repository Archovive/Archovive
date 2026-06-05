# Installation — Archovive Enterprise v5

Customer install for the frozen offline bundle (`archovive_product_bundle_v3` layout).

## Requirements

| Requirement | Detail |
|-------------|--------|
| OS | Linux x86_64 (glibc 2.31+), WSL2 |
| Python | **Not required** (frozen binaries) |
| Tools | `unzip`, `sha256sum` (recommended) |
| Disk | ~200 MB extract + XDG config/cache |

## Quick install (this repository)

```bash
git clone https://github.com/Archovive/Archovive.git
cd Archovive

# From GitHub Release v5.0.0 — place beside install_archovive.sh:
#   archovive-enterprise-5.0.0.zip
#   archovive-enterprise-5.0.0.zip.sha256
#   archovive.slsa.provenance.json

sha256sum -c archovive-enterprise-5.0.0.zip.sha256   # optional
./install_archovive.sh
source ./archovive.env

archovive --version
archovive doctor
./archovive-enterprise-5.0.0/scripts/setup_license.sh   # copies license to XDG
archovive ask "why blocked?"
```

## Bundle layout (v3)

```text
archovive-enterprise-5.0.0/
├── bin/           archovive, archovive-mcp (wrappers)
├── libexec/       PyInstaller runtime (read-only)
├── share/         docs, legal, examples, templates
├── scripts/       install.sh, verify_signature.sh, setup_license.sh
└── metadata/      build_manifest.json, sha256.txt, provenance
```

## Production install (`/opt`)

```bash
unzip archovive-enterprise-5.0.0.zip
cd archovive-enterprise-5.0.0
sudo ./scripts/install.sh                    # default: /opt/archovive-enterprise-5.0.0
sudo ./scripts/verify_signature.sh
source /etc/archovive/archovive.env
archovive doctor
```

## Environment (XDG-separated)

| Variable | Purpose |
|----------|---------|
| `ARCHOVIVE_BUNDLE_ROOT` | Immutable install (set by wrappers) |
| `ARCHOVIVE_CONFIG` | `$XDG_CONFIG_HOME/archovive` |
| `ARCHOVIVE_CACHE` | `$XDG_CACHE_HOME/archovive` |
| `ARCHOVIVE_STATE` | `$XDG_DATA_HOME/archovive` |
| `ARCHOVIVE_REPO` | Target repository under analysis |

## MCP (IDE)

```json
{
  "mcpServers": {
    "archovive": {
      "command": "/opt/archovive-enterprise-5.0.0/bin/archovive-mcp",
      "env": { "ARCHOVIVE_REPO": "/path/to/your-repo" }
    }
  }
}
```

## Troubleshooting

See `docs/TROUBLESHOOTING.md` (in repo) or `share/docs/TROUBLESHOOTING.md` (inside bundle).

## Breaking changes (v4 → v5)

- Zip: `archovive_product_bundle_v4.zip` → `archovive-enterprise-5.0.0.zip`
- No Python venv — frozen `bin/archovive`
- `ARCHOVIVE_ENGINE_ROOT` → `ARCHOVIVE_BUNDLE_ROOT`
- License: `share/legal/archovive_license.json` + `setup_license.sh`
