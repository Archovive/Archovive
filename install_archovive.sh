#!/usr/bin/env bash
# Archovive customer installer — unpack enterprise bundle v3.
set -euo pipefail

BUNDLE_NAME="${ARCHOVIVE_BUNDLE_ZIP:-archovive-enterprise-5.0.0.zip}"
TARGET_DIR="archovive-enterprise-5.0.0"
CLI_ROOT="$(cd "$(dirname "$0")" && pwd)"

cd "${CLI_ROOT}"

echo "==> Archovive Installer (v5.0.0 enterprise bundle v3)"
echo "==> Expected bundle: ${BUNDLE_NAME}"
echo "==> Install directory: ${CLI_ROOT}"
echo

if ! command -v unzip >/dev/null 2>&1; then
  echo "ERROR: unzip not found."
  exit 1
fi

if [[ ! -f "${BUNDLE_NAME}" ]]; then
  echo "ERROR: ${BUNDLE_NAME} not found in ${CLI_ROOT}/"
  echo "Download from GitHub Releases (Archovive-core or Archovive tag v5.0.0)"
  exit 1
fi

rm -rf "${TARGET_DIR}"
unzip -q "${BUNDLE_NAME}"

if [[ ! -x "${TARGET_DIR}/bin/archovive" ]]; then
  echo "ERROR: bundle missing ${TARGET_DIR}/bin/archovive"
  exit 1
fi

cat > "${CLI_ROOT}/archovive.env" <<EOF
export PATH="${CLI_ROOT}/${TARGET_DIR}/bin:\$PATH"
export ARCHOVIVE_BUNDLE_ROOT="${CLI_ROOT}/${TARGET_DIR}"
export ARCHOVIVE_PRODUCT=enterprise
export ARCHOVIVE_CONFIG="\${XDG_CONFIG_HOME:-\$HOME/.config}/archovive"
export ARCHOVIVE_CACHE="\${XDG_CACHE_HOME:-\$HOME/.cache}/archovive"
export ARCHOVIVE_STATE="\${XDG_DATA_HOME:-\$HOME/.local/share}/archovive"
EOF

echo "==> Installed. Source: source ${CLI_ROOT}/archovive.env"
echo "==> Verify: archovive --version && archovive doctor"
echo "==> Optional: cd ${TARGET_DIR} && ./scripts/verify_signature.sh"
