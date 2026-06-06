#!/usr/bin/env bash
# Regenerate docs/assets/gifs/*.gif via VHS (preferred) or Pillow fallback.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "${ROOT}"
DEMO="${ROOT}/docs/assets/demo"
GIFS="${ROOT}/docs/assets/gifs"
TAPES="${DEMO}/tapes"

VHS="${VHS:-}"
if [[ -z "${VHS}" ]]; then
  if command -v vhs >/dev/null 2>&1; then
    VHS=vhs
  elif [[ -x "${DEMO}/.bin/vhs" ]]; then
    VHS="${DEMO}/.bin/vhs"
  fi
fi

echo "==> Archovive demo GIF build"
python3 -m pip install -q -e internal/ 2>/dev/null || \
  python3 -m pip install -q --break-system-packages -e internal/

if [[ -n "${VHS}" ]]; then
  echo "==> Using VHS: ${VHS}"
  for tape in "${TAPES}"/*.tape; do
    echo "    ${tape}"
    "${VHS}" "${tape}"
  done
  if command -v gifsicle >/dev/null 2>&1; then
    echo "==> Optimizing with gifsicle"
    for gif in "${GIFS}"/*.gif; do
      gifsicle -O3 --lossy=40 "${gif}" -o "${gif}"
    done
  fi
else
  echo "==> VHS not found — Pillow fallback (auto-crop)"
  echo "    VHS needs: vhs + ffmpeg (https://ffmpeg.org)"
  echo "    Install vhs: go install github.com/charmbracelet/vhs@latest"
  python3 "${DEMO}/build_gifs.py"
fi

echo "==> Done:"
ls -la "${GIFS}"/*.gif
