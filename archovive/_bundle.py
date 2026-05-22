"""Product bundle pointers — no engine imports in the public repo."""
from __future__ import annotations

CORE_REPO_URL = "https://github.com/Archovive/Archovive-core"
BUNDLE_ZIP = "archovive_product_bundle_v4.zip"
BUNDLE_DIR = "archovive_product_bundle_v4"
INSTALL_DOC = "docs/INSTALL.md"

ENGINE_REQUIRED_MSG = f"""\
Archovive Engine is part of the product bundle ({BUNDLE_ZIP}), not this repository.
  Set ARCHOVIVE_ENGINE_ROOT=/path/to/{BUNDLE_DIR} and use bin/archovive from this repo, or
  extract the bundle and run ./install_archovive.sh — see {INSTALL_DOC}
  Engine / Evidence Camera / SBOM: {CORE_REPO_URL}
"""


def require_engine(command: str) -> None:
    raise SystemExit(
        f"archovive {command}: engine not available in the public CLI repository.\n"
        f"{ENGINE_REQUIRED_MSG}"
    )
