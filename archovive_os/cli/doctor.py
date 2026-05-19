"""archovive doctor — environment and runtime diagnostics."""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Any


def run_doctor(*, human: bool = False) -> int:
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append((name, ok, detail))

    check("python", sys.version_info >= (3, 11), sys.version)
    check("archovive_os", _try_import("archovive_os"), "bridge + server")
    check("archovive_engine", _try_import("archovive_engine"), "reference spec oracle")
    check("gov_runtime", _try_import("archovive.event_runtime.runtime"), "EventRuntimeV4")
    check("hypervisor", _try_import("archovive.hypervisor_v5.wrapper"), "HypervisorV5")

    compile_mode = os.environ.get("ARCHOVIVE_COMPILE", "runtime")
    check("compile_default", compile_mode == "runtime", f"ARCHOVIVE_COMPILE={compile_mode}")

    git = shutil.which("git")
    check("git", git is not None, git or "not found")

    config = Path.home() / ".archovive" / "config.yaml"
    check("config", config.exists() or True, str(config) if config.exists() else "optional (run archovive init)")

    failed = 0
    if human:
        print()
    for name, ok, detail in checks:
        mark = "OK" if ok else "FAIL"
        if human:
            from archovive_os.cli.output import decision_color

            status = decision_color("PASS" if ok else "FAIL")
            print(f"  {name}: {status}")
            print(f"    {detail}")
        else:
            print(f"  [{mark}] {name}: {detail}")
        if not ok:
            failed += 1

    if failed:
        print(f"\n{failed} check(s) failed. Try: pip install -e archovive_engine -e archovive_os -e gov")
        return 1
    print("\nAll checks passed. Runtime-first Archovive OS v3 is ready.")
    return 0


def _try_import(module: str) -> bool:
    try:
        __import__(module)
        return True
    except ImportError:
        return False
