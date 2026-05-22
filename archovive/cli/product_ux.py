"""
Product CLI UX (v4.1) — help text and version display (public repo, no engine).
"""
from __future__ import annotations

import json
from pathlib import Path

from archovive._bundle import BUNDLE_DIR

CLI_VERSION = "4.1"
ENGINE_VERSION = "3.0.0 (product bundle)"

EXIT_CODES_HELP = """\
Exit codes:
  0  PASS
  1  Drift violation
  2  Regulatory/Policy violation
  3  Engine error
  4  Misuse (running inside bundle)"""

TOP_LEVEL_HELP = f"""\
Archovive v{CLI_VERSION} — deterministic architecture analysis (public CLI)

Usage:
  archovive run              Analyse repository (requires product bundle engine)
  archovive verify           Re-verify attestation (requires product bundle)
  archovive init             Initialize project baseline (requires product bundle)
  archovive doctor           Lightweight environment check (public)
  archovive diff             Compare two analysis runs (requires product bundle)
  archovive sbom             Emit SBOM (requires product bundle)
  archovive evidence         Evidence Camera — help only in this repo; data in bundle
  archovive camera evidence  Same

Options:
  --help                     Show this message
  --version                  Show version

{EXIT_CODES_HELP}

This repository is CLI + docs only. Install {BUNDLE_DIR}/ from {BUNDLE_DIR}.zip — see docs/INSTALL.md."""

RUN_HELP = f"""\
Usage:
  archovive run [options]

Description:
  Execute full analysis pipeline (Compiler → M1 → M2 → M4 → M3 → Verify → M5).
  Requires the product bundle engine (not shipped in this public repository).

Options:
  --compact, --core-view, --relax, --help

See docs/OUTPUTS.md and docs/INSTALL.md."""

VERIFY_HELP = """\
Usage:
  archovive verify [path] [--json]

Requires product bundle. See docs/INSTALL.md."""

INIT_HELP = """\
Usage:
  archovive init [path] [--wizard]

Requires product bundle. See docs/INSTALL.md."""

DOCTOR_HELP = """\
Usage:
  archovive doctor

Public repo: checks Python 3.11+ and Git only.
Full doctor (license, venv, policy packs) requires product bundle install."""

DIFF_HELP = """\
Usage:
  archovive diff <old_dir> <new_dir>

Requires product bundle."""

SBOM_HELP = """\
Usage:
  archovive sbom [--out=PATH]

Requires product bundle. See docs/SBOM.md."""

EVIDENCE_HELP = """\
Usage:
  archovive evidence [--json] [--global] [REPO]
  archovive camera evidence --repo NAME [--global] [--json]

Evidence Camera (C) runs in the product bundle / MCP server.
This repo documents the schema; see docs/CAMERAS.md and bundle benchmarks/."""

COMMAND_HELP: dict[str, str] = {
    "run": RUN_HELP,
    "verify": VERIFY_HELP,
    "init": INIT_HELP,
    "doctor": DOCTOR_HELP,
    "diff": DIFF_HELP,
    "sbom": SBOM_HELP,
    "evidence": EVIDENCE_HELP,
}


def _product_root() -> Path | None:
    import os

    if os.environ.get("ARCHOVIVE_REPO"):
        return Path(os.environ["ARCHOVIVE_REPO"]).resolve()
    cur = Path.cwd().resolve()
    for _ in range(16):
        if (cur / BUNDLE_DIR / "MANIFEST.json").is_file():
            return cur / BUNDLE_DIR
        if (cur / "MANIFEST.json").is_file() and (cur / "packages" / "archovive_os").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def read_bundle_hash() -> str | None:
    root = _product_root()
    if root is None:
        return None
    manifest = root / "MANIFEST.json"
    if not manifest.is_file():
        return None
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    value = data.get("bundle_hash")
    return str(value) if value else None


def print_version() -> None:
    bh = read_bundle_hash()
    lines = [
        f"archovive public CLI v{CLI_VERSION}",
        f"engine (bundle): {ENGINE_VERSION}",
    ]
    if bh:
        lines.append(f"bundle hash: {bh}")
    else:
        lines.append("bundle: not detected — install archovive_product_bundle_v4")
    print("\n".join(lines))


def print_top_help() -> None:
    print(TOP_LEVEL_HELP)


def print_command_help(command: str) -> None:
    text = COMMAND_HELP.get(command)
    if text:
        print(text)
    else:
        print_top_help()


def wants_help(argv: list[str]) -> bool:
    return "-h" in argv or "--help" in argv


def strip_help_flags(argv: list[str]) -> list[str]:
    return [a for a in argv if a not in ("-h", "--help")]
