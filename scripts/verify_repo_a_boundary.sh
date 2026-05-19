#!/usr/bin/env bash
# Verify Repo A tree has no forbidden sovereign-core imports.
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"

PKG=""
if [[ -d "$ROOT/archovive_os/product_v1" ]]; then
  PKG="$ROOT/archovive_os"
elif [[ -d "$ROOT/archovive_os/archovive_os/product_v1" ]]; then
  PKG="$ROOT/archovive_os/archovive_os"
else
  echo "cannot find archovive_os product_v1 under $ROOT" >&2
  exit 1
fi

FORBIDDEN=(
  'archovive_os\.pipe'
  'archovive_os\.runtime_pipe'
  'archovive_os\.audit_pipe'
  'archovive_os\.bridge'
  'archovive_os\.contracts'
  'archovive_engine'
  'golden/'
  'pipe_spec\.py'
  'pipe_integrity_cli'
  'health_certificate\.py'
)

echo "== Repo A boundary check: $PKG"
FAIL=0
SEARCH() {
  if command -v rg >/dev/null 2>&1; then
    rg -n "$@" 2>/dev/null
  else
    grep -Rn "$@" 2>/dev/null
  fi
}

CLI_FILES=(
  "$PKG/cli/entrypoints.py"
  "$PKG/cli/binary_kit.py"
  "$PKG/cli/binary_dispatch_product.py"
  "$PKG/cli/main_product.py"
  "$PKG/cli/analyze_cli.py"
  "$PKG/cli/bootstrap_cli.py"
  "$PKG/cli/simulate_cli.py"
  "$PKG/cli/attestation_export_cli.py"
  "$PKG/cli/flags.py"
  "$PKG/cli/output.py"
  "$PKG/cli/init.py"
  "$PKG/cli/errors.py"
)

for pattern in "${FORBIDDEN[@]}"; do
  if SEARCH "$pattern" "$PKG/product_v1" "${CLI_FILES[@]}"; then
    echo "FORBIDDEN pattern in Repo A: $pattern" >&2
    FAIL=1
  fi
done

if ! SEARCH "archovive_core" "$PKG/product_v1" >/dev/null; then
  echo "product_v1 must import via archovive_core.api / _core" >&2
  FAIL=1
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "BOUNDARY: PASS"
else
  echo "BOUNDARY: FAIL"
  exit 1
fi
