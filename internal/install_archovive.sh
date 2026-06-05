#!/usr/bin/env bash
set -euo pipefail
BUNDLE_NAME="${ARCHOVIVE_BUNDLE_ZIP:-archovive-enterprise-5.0.0.zip}"
TARGET_DIR="archovive-enterprise-5.0.0"
CLI_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "${CLI_ROOT}"
echo "==> Archovive Installer v5.0.0 (bundle v3)"
if ! command -v unzip >/dev/null 2>&1; then echo "ERROR: unzip required" >&2; exit 1; fi
if [[ ! -f "${BUNDLE_NAME}" ]]; then
  echo "ERROR: ${BUNDLE_NAME} not found — download GitHub Release v5.0.0" >&2
  exit 1
fi
if [[ -f "releases/${BUNDLE_NAME}.sha256" ]] && command -v sha256sum >/dev/null 2>&1; then
  (cd releases && sha256sum -c "${BUNDLE_NAME}.sha256") || { echo "WARN: sha256 mismatch" >&2; }
elif [[ -f "${BUNDLE_NAME}.sha256" ]] && command -v sha256sum >/dev/null 2>&1; then
  sha256sum -c "${BUNDLE_NAME}.sha256" || { echo "WARN: sha256 mismatch" >&2; }
fi
rm -rf "${TARGET_DIR}"
unzip -q "${BUNDLE_NAME}"
[[ -x "${TARGET_DIR}/bin/archovive" ]] || { echo "ERROR: missing ${TARGET_DIR}/bin/archovive" >&2; exit 1; }
cat > "${CLI_ROOT}/archovive.env" <<ENV
export PATH="${CLI_ROOT}/${TARGET_DIR}/bin:$PATH"
export ARCHOVIVE_BUNDLE_ROOT="${CLI_ROOT}/${TARGET_DIR}"
export ARCHOVIVE_PRODUCT=enterprise
export ARCHOVIVE_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/archovive"
export ARCHOVIVE_CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/archovive"
export ARCHOVIVE_STATE="${XDG_DATA_HOME:-$HOME/.local/share}/archovive"
ENV
echo "==> source ${CLI_ROOT}/archovive.env"
echo "==> optional: ${TARGET_DIR}/scripts/setup_license.sh && ${TARGET_DIR}/scripts/verify_signature.sh"
