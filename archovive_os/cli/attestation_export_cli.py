"""CLI for `archovive attestation export`."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from archovive_os.product_v1.attestation_export import run_attestation_export


def run_attestation_export_cli(
    attest_path: str,
    *,
    write_pdf: bool = False,
    md_only: bool = False,
    out_path: str | None = None,
    json_out: bool = False,
    verify_replay: bool = True,
) -> int:
    path = Path(attest_path)
    out_pdf = Path(out_path) if out_path and write_pdf else None
    out_md = None
    if out_path and md_only:
        out_md = Path(out_path)
    elif out_path and not write_pdf:
        out_md = Path(out_path)

    if not json_out and sys.stdout.isatty():
        print("=== [ARCHOVIVE v1] Attestation Export ===\n")
        print(f"[1/3] Loading ............... {path}")
        print("[2/3] Rendering attest.md .")

    try:
        result = run_attestation_export(
            path,
            write_pdf=write_pdf,
            md_only=md_only,
            out_md=out_md,
            out_pdf=out_pdf,
            verify_replay=verify_replay,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        if json_out:
            print(
                json.dumps(
                    {"status": "FAIL", "errors": [str(exc)]},
                    separators=(",", ":"),
                )
            )
        else:
            print(f"EXPORT: FAIL\n  - {exc}", file=sys.stderr)
        return 1

    if json_out:
        print(result.to_json())
        return 0 if result.status == "PASS" else 1

    if write_pdf and result.pdf_path:
        print(f"[3/3] PDF ................... {result.pdf_path}")
    elif md_only:
        print(f"[3/3] Markdown only ......... {result.md_path}")
    else:
        print(f"[3/3] Done .................. {result.md_path}")

    print(f"\n  md_hash:  {result.md_hash[:32]}…")
    if result.pdf_hash:
        print(f"  pdf_hash: {result.pdf_hash[:32]}…")
    print(f"\nEXPORT: {result.status}")
    if result.errors:
        print("\nDetails:")
        for err in result.errors:
            print(f"  - {err}")

    return 0 if result.status == "PASS" else 1
