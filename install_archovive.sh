#!/usr/bin/env bash
# Archovive Open-Core — validates policy packs & docs; engine is a separate licensed install.
set -euo pipefail
CLI_ROOT="$(cd "$(dirname "$0")" && pwd)"

die() { echo "error: $*" >&2; exit 1; }

echo "Archovive CLI (Open Core)"
echo "  root: ${CLI_ROOT}"
echo "  engine: NOT included — set ARCHOVIVE_ENGINE_ROOT to licensed bundle"

command -v python3 >/dev/null 2>&1 || die "python3 required"
[[ -d "${CLI_ROOT}/policy_packs" ]] || die "missing policy_packs/"
[[ -f "${CLI_ROOT}/docs/COMPILER_SPEC_V1.md" ]] || die "missing docs/COMPILER_SPEC_V1.md"

unsigned=0
for f in "${CLI_ROOT}"/policy_packs/*.json; do
  [[ "$(basename "$f")" == "registry.json" ]] && continue
  [[ -f "${f}.sig" ]] || { echo "warn: unsigned $(basename "$f")"; unsigned=$((unsigned+1)); }
done
echo "==> policy packs ok (${unsigned} unsigned)"

if [[ -n "${ARCHOVIVE_ENGINE_ROOT:-}" && -x "${ARCHOVIVE_ENGINE_ROOT}/install_archovive.sh" ]]; then
  echo "==> Installing licensed engine at ${ARCHOVIVE_ENGINE_ROOT}"
  (cd "${ARCHOVIVE_ENGINE_ROOT}" && ./install_archovive.sh "$@")
  echo "export ARCHOVIVE_ENGINE_ROOT=${ARCHOVIVE_ENGINE_ROOT}" > "${CLI_ROOT}/archovive.env"
  echo "Ready: ${CLI_ROOT}/bin/archovive run  (delegates to engine)"
else
  cat > "${CLI_ROOT}/archovive.env" <<EOF
# Open-Core — point to your licensed product bundle (not in public git)
# export ARCHOVIVE_ENGINE_ROOT=/path/to/archovive_product_bundle_v3
EOF
  echo "==> Engine not configured. Add to archovive.env:"
  echo "    export ARCHOVIVE_ENGINE_ROOT=/path/to/archovive_product_bundle_v3"
fi
