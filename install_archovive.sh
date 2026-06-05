#!/usr/bin/env bash
# Archovive Open-Core installer — unpack v5 enterprise product bundle.
set -euo pipefail

BUNDLE_NAME="${ARCHOVIVE_BUNDLE_ZIP:-archovive-enterprise-5.0.0.zip}"
TARGET_DIR="archovive"
CLI_ROOT="$(cd "$(dirname "$0")" && pwd)"

cd "${CLI_ROOT}"

echo "==> Archovive Installer (v5.0.0)"
echo "==> Expected bundle: ${BUNDLE_NAME}"
echo "==> Install directory: ${CLI_ROOT}"
echo

if ! command -v unzip >/dev/null 2>&1; then
  echo "ERROR: unzip not found."
  exit 1
fi

if [[ ! -f "${BUNDLE_NAME}" ]]; then
  echo "ERROR: ${BUNDLE_NAME} not found in ${CLI_ROOT}/"
  echo "Download from Archovive-core release or copy from dist/archovive-enterprise-5.0.0.zip"
  exit 1
fi

rm -rf "${TARGET_DIR}"
unzip -q "${BUNDLE_NAME}"

if [[ ! -x "${TARGET_DIR}/archovive" ]]; then
  echo "ERROR: bundle missing executable ${TARGET_DIR}/archovive"
  exit 1
fi

export PATH="${CLI_ROOT}/${TARGET_DIR}:${PATH}"
cat > "${CLI_ROOT}/archovive.env" <<EOF
export PATH="${CLI_ROOT}/${TARGET_DIR}:\$PATH"
export ARCHOVIVE_PRODUCT=enterprise
export ARCHOVIVE_BUNDLE_ROOT="${CLI_ROOT}/${TARGET_DIR}"
EOF

echo "==> Installed. Source: source ${CLI_ROOT}/archovive.env"
echo "==> Verify: archovive --version && archovive doctor"
