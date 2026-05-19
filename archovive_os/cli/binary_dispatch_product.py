"""
Repo A — product binary dispatch (cli, attestation).
"""
from __future__ import annotations

import argparse
import sys

from archovive_os.cli.analyze_cli import run_analyze_cli
from archovive_os.cli.attestation_export_cli import run_attestation_export_cli
from archovive_os.cli.binary_kit import (
    BinaryModeName,
    IDENTITIES,
    emit_version,
    print_binary_banner,
)
from archovive_os.cli.bootstrap_cli import run_bootstrap_cli
from archovive_os.cli.simulate_cli import run_simulate_cli

PRODUCT_MODES = frozenset({"cli", "attestation"})


def build_product_mode_parser(mode: BinaryModeName) -> argparse.ArgumentParser:
    if mode == "cli":
        from archovive_os.cli.main_product import build_product_parser

        return build_product_parser()
    if mode == "attestation":
        ident = IDENTITIES[mode]
        parser = argparse.ArgumentParser(prog=ident.prog, description=ident.tagline)
        parser.add_argument("--version", action="store_true")
        parser.add_argument("--json", action="store_true")
        sub = parser.add_subparsers(dest="command", required=True)
        export = sub.add_parser("export")
        export.add_argument("attest_json")
        export.add_argument("--pdf", action="store_true")
        export.add_argument("--md-only", action="store_true")
        export.add_argument("--out", default=None)
        export.add_argument("--json", action="store_true")
        export.add_argument("--no-verify-replay", action="store_true")
        return parser
    raise ValueError(f"not a product mode: {mode}")


def dispatch_product_mode(mode: BinaryModeName, args: argparse.Namespace) -> int:
    if getattr(args, "version", False):
        return emit_version(mode, json_out=getattr(args, "json", False))
    if not getattr(args, "json", False) and sys.stdout.isatty():
        print_binary_banner(mode)

    if mode == "cli":
        from archovive_os.cli.main_product import dispatch_product

        return dispatch_product(args)

    if mode == "attestation" and args.command == "export":
        write_pdf = getattr(args, "pdf", False)
        md_only = getattr(args, "md_only", False)
        if not write_pdf and not md_only:
            md_only = True
        return run_attestation_export_cli(
            args.attest_json,
            write_pdf=write_pdf,
            md_only=md_only and not write_pdf,
            out_path=getattr(args, "out", None),
            json_out=getattr(args, "json", False),
            verify_replay=not getattr(args, "no_verify_replay", False),
        )
    return 2


def run_product_main(mode: BinaryModeName, argv: list[str] | None = None) -> int:
    parser = build_product_mode_parser(mode)
    argv = argv if argv is not None else sys.argv[1:]
    if mode == "cli" and not argv:
        parser.print_help()
        return 0
    if not argv:
        parser.print_help()
        return 0
    args = parser.parse_args(argv)
    if mode == "cli" and getattr(args, "version", False):
        return emit_version("cli", json_out=getattr(args, "json", False))
    if mode == "cli" and not getattr(args, "json", False) and sys.stdout.isatty():
        print_binary_banner("cli")
    return dispatch_product_mode(mode, args)
