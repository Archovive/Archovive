# Troubleshooting — Archovive Enterprise v5

## Install is read-only (v5.0.0-PRO)

The bundle under `/opt/archovive-enterprise-*` must **never** be modified.
There is no `config/` directory inside the bundle — only templates under `share/templates/`.

| Writable layer | Env | System path | User path |
|----------------|-----|-------------|-----------|
| Config + license | `ARCHOVIVE_CONFIG` | `/etc/archovive` | `~/.config/archovive` |
| Cache (IR, SBOM scratch) | `ARCHOVIVE_CACHE` | `/var/cache/archovive` | `~/.cache/archovive` |
| State (governance sidecar) | `ARCHOVIVE_STATE` | `/var/lib/archovive` | `~/.local/share/archovive` |

```bash
sudo ./scripts/install.sh                    # → /opt, /usr/local/bin, /etc/archovive
sudo ./scripts/setup_license.sh --system     # license → /etc/archovive (not the bundle)
source /etc/archovive/archovive.env
archovive doctor
```

Read-only cwd / air-gapped analysis: `export ARCHOVIVE_ISOLATED=1` (sidecar under `ARCHOVIVE_STATE` only).

## ask / chat / governance disagree

All surfaces must use the same analysis root:

```bash
export ARCHOVIVE_REPO=/path/to/target-repo
archovive ask "why blocked?"
archovive chat "why blocked?"
archovive governance decide --json "$ARCHOVIVE_REPO"
```

If hashes differ, check `ARCHOVIVE_REPO` and cwd — not the install directory.

## Policy packs missing (doctor exit 1)

Copy templates from `share/templates/policy_packs/` into `$ARCHOVIVE_CONFIG/policy_packs/`  
or run `scripts/setup_license.sh` then `archovive setup --enterprise`.

## MCP server

```bash
archovive-mcp   # stdio — see share/templates/systemd/archovive-mcp.service
```

## Verify integrity

```bash
./scripts/verify_signature.sh
```

Compares `metadata/sha256.txt` against installed files.
