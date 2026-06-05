#!/usr/bin/env bash
# Enterprise bundle installer — paths under internal/releases/
set -euo pipefail
BUNDLE_NAME="${ARCHOVIVE_BUNDLE_ZIP:-archovive-enterprise-5.0.0.zip}"
TARGET_DIR="archovive-enterprise-5.0.0"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"
echo "==> Archovive Enterprise Installer v5.0.0"
if ! command -v unzip >/dev/null 2>&1; then echo "ERROR: unzip required" >&2; exit 1; fi
ZIP_PATH="${REPO_ROOT}/${BUNDLE_NAME}"
[[ -f "${ZIP_PATH}" ]] || ZIP_PATH="${REPO_ROOT}/internal/releases/${BUNDLE_NAME}"
if [[ ! -f "${ZIP_PATH}" ]]; then
  echo "ERROR: ${BUNDLE_NAME} not found — download GitHub Release v5.0.0" >&2
  exit 1
fi
if [[ -f "internal/releases/${BUNDLE_NAME}.sha256" ]] && command -v sha256sum >/dev/null 2>&1; then
  (cd internal/releases && sha256sum -c "${BUNDLE_NAME}.sha256") || { echo "WARN: sha256 mismatch" >&2; }
fi
rm -rf "${TARGET_DIR}"
unzip -q "${ZIP_PATH}"
[[ -x "${TARGET_DIR}/bin/archovive" ]] || { echo "ERROR: missing ${TARGET_DIR}/bin/archovive" >&2; exit 1; }
cat > "${REPO_ROOT}/archovive.env" <<ENV
export PATH="${REPO_ROOT}/${TARGET_DIR}/bin:$PATH"
export ARCHOVIVE_BUNDLE_ROOT="${REPO_ROOT}/${TARGET_DIR}"
export ARCHOVIVE_PRODUCT=enterprise
export ARCHOVIVE_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/archovive"
export ARCHOVIVE_CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/archovive"
export ARCHOVIVE_STATE="${XDG_DATA_HOME:-$HOME/.local/share}/archovive"
ENV
echo "==> source ${REPO_ROOT}/archovive.env"
echo "==> optional: ${TARGET_DIR}/scripts/setup_license.sh && ${TARGET_DIR}/scripts/verify_signature.sh"
