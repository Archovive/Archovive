"""v5 CLI — OSS simulate funnel + enterprise bundle router."""
from __future__ import annotations

import shutil
import sys

from cli._bundle import require_engine
from cli.camera_evidence_stub import run_evidence_stub
from cli.camera_operator import print_operator_help
from cli.mcp_client import print_mcp_help
from cli.product_ux import (
    print_command_help,
    print_top_help,
    print_version,
    strip_help_flags,
    wants_help,
)
from simulate.runner import run_simulate_cli


def _apply_run_flags(argv: list[str]) -> list[str]:
    import os

    rest: list[str] = []
    for arg in argv:
        if arg in ("--compact", "--core-view"):
            os.environ["ARCHOVIVE_COMPACT"] = "1"
        elif arg == "--relax":
            os.environ["ARCHOVIVE_RELAX"] = "1"
        else:
            rest.append(arg)
    return rest


def _dispatch_help(argv: list[str]) -> bool:
    if not argv:
        return False
    if wants_help(argv) and (len(argv) == 1 or argv[0] in ("-h", "--help")):
        print_top_help()
        return True
    cmd = argv[0]
    if cmd in ("run", "verify", "init", "doctor", "diff", "sbom", "evidence", "mcp", "simulate", "ci") and wants_help(
        argv
    ):
        if cmd == "mcp":
            print_mcp_help()
        elif cmd == "evidence":
            run_evidence_stub(["--help"])
        elif cmd == "ci":
            print_command_help("ci")
        else:
            print_command_help(cmd)
        return True
    if cmd == "camera" and len(argv) > 1:
        sub = argv[1]
        if sub in ("operator", "machine", "evidence") and wants_help(argv):
            if sub == "operator":
                print_operator_help()
            elif sub == "evidence":
                run_evidence_stub(["--help"])
            else:
                from cli.camera_machine_stub import print_machine_help

                print_machine_help()
            return True
    return False


def run_doctor_public(argv: list[str]) -> int:
    import sys as _sys

    ok = True
    if _sys.version_info < (3, 11):
        print("archovive doctor: Python 3.11+ required", file=_sys.stderr)
        ok = False
    else:
        print(f"archovive doctor: Python {_sys.version.split()[0]} OK")
    if shutil.which("git"):
        print("archovive doctor: git OK")
    else:
        print("archovive doctor: git not found (recommended)", file=_sys.stderr)
    print("archovive doctor: try `archovive simulate` — full checks need enterprise bundle")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    argv = _apply_run_flags(list(argv if argv is not None else sys.argv[1:]))

    if "--version" in argv or "-V" in argv:
        print_version()
        return 0

    if _dispatch_help(argv):
        return 0

    argv = strip_help_flags(argv)

    if not argv:
        return run_simulate_cli([])

    if argv[0] == "simulate":
        return run_simulate_cli(argv[1:])

    if argv[0] == "ci":
        if len(argv) < 2 or argv[1] != "check":
            print("Usage: archovive ci check [--repo PATH] [--json]", file=sys.stderr)
            return 4
        return run_simulate_cli(argv[2:], ci_mode=True)

    if argv[0] in ("run",):
        require_engine("run")
    if argv[0] == "verify":
        require_engine("verify")
    if argv[0] == "init":
        require_engine("init")
    if argv[0] == "doctor":
        return run_doctor_public(argv[1:])
    if argv[0] == "diff":
        require_engine("diff")
    if argv[0] == "sbom":
        require_engine("sbom")
    if argv[0] == "evidence":
        return run_evidence_stub(argv[1:])
    if argv[0] == "mcp":
        if argv[1:] and not wants_help(argv[1:]):
            require_engine("mcp")
        print_mcp_help()
        return 0
    if argv[0] == "camera":
        if len(argv) < 2:
            print("Usage: archovive camera {operator|machine|evidence} …", file=sys.stderr)
            return 2
        sub = argv[1]
        rest = argv[2:]
        if sub == "operator":
            if wants_help(rest) or not rest:
                print_operator_help()
                return 0
            require_engine("camera operator")
        if sub == "machine":
            from cli.camera_machine_stub import run_machine_stub

            return run_machine_stub(rest)
        if sub == "evidence":
            return run_evidence_stub(rest)
        print(f"unknown camera: {sub}", file=sys.stderr)
        return 2

    print_top_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
