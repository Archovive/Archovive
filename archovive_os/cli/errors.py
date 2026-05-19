"""
CLI error formatting — actionable, runtime-first guidance.
"""
from __future__ import annotations

from typing import Any


def format_api_error(result: dict[str, Any]) -> str:
    status = int(result.get("status", 500))
    error = str(result.get("error", "unknown_error"))
    detail = result.get("detail") or result.get("path") or ""
    base = f"[{status}] {error}"
    if detail:
        base = f"{base}: {detail}"

    hints: list[str] = []
    if "compile" in error.lower() or "runtime" in str(detail).lower():
        hints.append("Try: archovive ... --compile-backend=engine")
        hints.append("Or:  ARCHOVIVE_COMPILE=verify archovive ops run <repo>")
    if "proof" in error.lower():
        hints.append("Try: ARCHOVIVE_COMPILE=verify to compare engine vs runtime hashes")
    if "fleet" in error.lower():
        hints.append("Try: --tenant <id> and ops fleet status <repo>")
    if status >= 500:
        hints.append("Check server logs: archovive-server")

    if hints:
        return base + "\n  " + "\n  ".join(hints)
    return base
