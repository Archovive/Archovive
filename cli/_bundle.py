"""Product bundle pointers — no engine imports in the public repo."""
from __future__ import annotations

CORE_REPO_URL = "https://github.com/Archovive/Archovive-core"
BUNDLE_ZIP = "archovive-enterprise-5.0.0.zip"
BUNDLE_DIR = "archovive-enterprise-5.0.0"
INSTALL_DOC = "docs/integrate/ch-07-enterprise.md"

ENGINE_REQUIRED_MSG = f"""\
Archovive runtime ships in the enterprise product bundle ({BUNDLE_ZIP}), not this repository.
  1. Download release assets (tag v5.0.0): {BUNDLE_ZIP}, .sha256, archovive.slsa.provenance.json
  2. Place the zip beside install_archovive.sh and run ./install_archovive.sh
  3. source ./archovive.env
  Bundle layout: {BUNDLE_DIR}/bin/archovive (frozen binary, no Python venv)
  Engine source / build: {CORE_REPO_URL}
"""


def require_engine(command: str) -> None:
    raise SystemExit(
        f"archovive {command}: full runtime not available in the public CLI repository.\n"
        f"{ENGINE_REQUIRED_MSG}"
    )
