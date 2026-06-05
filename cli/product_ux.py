"""
Product CLI UX (v5.0.0) — OSS funnel + bundle router.
"""
from __future__ import annotations

import json
from pathlib import Path

from cli._bundle import BUNDLE_DIR, BUNDLE_ZIP

CLI_VERSION = "5.0.0"
ENGINE_VERSION = "5.0.0 (enterprise bundle)"

EXIT_CODES_HELP = """\
Exit codes:
  0  PASS
  1  Drift violation
  2  Policy / regulatory violation
  3  Engine error
  4  Misuse"""

TOP_LEVEL_HELP = f"""\
Archovive v{CLI_VERSION} — local-first architecture governance

Try it now (no bundle required):
  archovive simulate          30s demo — drift + policy verdict
  archovive ci check            CI gate on demo repo (exit 2 on violation)

Production (your repositories):
  archovive run                 Full analysis (enterprise bundle)
  archovive gate                Release decision
  archovive verify              Attestation verify

Options:
  --help, --version

{EXIT_CODES_HELP}

Docs: docs/01-intro/ · Enterprise bundle: {BUNDLE_ZIP} — docs/07-enterprise/"""

SIMULATE_HELP = """\
Usage:
  archovive simulate [--json] [--repo PATH]

Runs the OSS demo on examples/demo-fintech (intentional DORA violation).
Shows graph metrics, drift matrix, policy verdict, replay hash.

  archovive simulate --json     Machine-readable output"""

CI_HELP = """\
Usage:
  archovive ci check [--repo PATH] [--json]

CI gate for the demo repository. Exit 2 on policy violation (same as production gate).
Wire into GitHub Actions — see docs/03-ci/"""

RUN_HELP = f"""\
Usage:
  archovive run [options]

Full deterministic pipeline on your repository.
Requires enterprise bundle ({BUNDLE_DIR}/). See docs/07-enterprise/."""

VERIFY_HELP = """\
Usage:
  archovive verify [path] [--json]

Requires enterprise bundle. See docs/04-governance/."""

INIT_HELP = """\
Usage:
  archovive init [path]

Requires enterprise bundle."""

DOCTOR_HELP = """\
Usage:
  archovive doctor

Checks Python 3.11+ and git. Full doctor requires enterprise bundle."""

DIFF_HELP = """\
Usage:
  archovive diff <old> <new>

Requires enterprise bundle."""

SBOM_HELP = """\
Usage:
  archovive sbom

Requires enterprise bundle. See docs/04-governance/."""

EVIDENCE_HELP = """\
Usage:
  archovive evidence [--help]

Evidence Camera — full output in enterprise bundle. See docs/04-governance/."""


def print_top_help() -> None:
    print(TOP_LEVEL_HELP)


def print_command_help(command: str) -> None:
    mapping = {
        "run": RUN_HELP,
        "verify": VERIFY_HELP,
        "init": INIT_HELP,
        "doctor": DOCTOR_HELP,
        "diff": DIFF_HELP,
        "sbom": SBOM_HELP,
        "evidence": EVIDENCE_HELP,
        "simulate": SIMULATE_HELP,
        "ci": CI_HELP,
    }
    print(mapping.get(command, TOP_LEVEL_HELP))


def print_version() -> None:
    bundle_root = Path(BUNDLE_DIR)
    detected = bundle_root.is_dir() or bool(
        __import__("os").environ.get("ARCHOVIVE_BUNDLE_ROOT")
    )
    print(f"archovive OSS CLI v{CLI_VERSION}")
    print(f"engine: {ENGINE_VERSION if detected else 'simulate demo (OSS)'}")
    if detected:
        print(f"bundle: {BUNDLE_DIR}")
    else:
        print("bundle: not installed — run dist/install.sh or archovive simulate")


def wants_help(argv: list[str]) -> bool:
    return "-h" in argv or "--help" in argv


def strip_help_flags(argv: list[str]) -> list[str]:
    return [a for a in argv if a not in ("-h", "--help")]
