"""
Archovive v1 — public product CLI (Repo A surface only).

Core pipe commands live in archovive-core (Repo B).
"""
from __future__ import annotations

import argparse
from pathlib import Path

from archovive_os.cli.attestation_export_cli import run_attestation_export_cli
from archovive_os.cli.analyze_cli import run_analyze_cli
from archovive_os.cli.bootstrap_cli import run_bootstrap_cli
from archovive_os.cli.doctor import run_doctor
from archovive_os.cli.flags import add_os_parent_flags
from archovive_os.cli.init import run_init
from archovive_os.cli.output import print_human_banner
from archovive_os.cli.simulate_cli import run_simulate_cli


def build_product_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="archovive",
        description="Archovive v1 — Architecture Truth System",
        epilog=(
            "Examples:\n"
            "  archovive bootstrap\n"
            "  archovive simulate\n"
            "  archovive analyze . --out attest.json\n"
            "  archovive attestation export attest.json --pdf\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    analyze_p = sub.add_parser("analyze", help="L1+L2+L3 truth → attestation package")
    analyze_p.add_argument("target", help="Repo path, synthetic:// URI, or audit .json")
    analyze_p.add_argument("--out", required=True)
    analyze_p.add_argument("--package-dir", default=None)
    analyze_p.add_argument("--pack", default="DORA-2026")
    analyze_p.add_argument("--epoch", dest="epoch_id", default=None)
    analyze_p.add_argument("--no-bootstrap", action="store_true")
    add_os_parent_flags(analyze_p)

    boot_p = sub.add_parser("bootstrap", help="Sovereign bootstrap gate")
    boot_p.add_argument("--json", action="store_true")
    boot_p.add_argument("--root", default=None)
    boot_p.add_argument("--repo", default=None)
    boot_p.add_argument("--mode", dest="integrity_mode", default="full", choices=("synthetic", "hypervisor", "full"))
    boot_p.add_argument("--epoch", dest="epoch_id", default=None)

    sim_p = sub.add_parser("simulate", help="Truth Simulator walkthrough")
    sim_p.add_argument("--fixture", default="pipe_l3_dora_violation")
    sim_p.add_argument("--json", action="store_true")
    sim_p.add_argument("--pause", action="store_true")
    sim_p.add_argument("--epoch", dest="epoch_id", default=None)

    att_p = sub.add_parser("attestation", help="Attestation export")
    att_sub = att_p.add_subparsers(dest="attestation_command", required=True)
    export_p = att_sub.add_parser("export")
    export_p.add_argument("attest_json")
    export_p.add_argument("--pdf", action="store_true")
    export_p.add_argument("--md-only", action="store_true")
    export_p.add_argument("--out", default=None)
    export_p.add_argument("--json", action="store_true")
    export_p.add_argument("--no-verify-replay", action="store_true")

    sub.add_parser("doctor", help="Environment diagnostics")
    init_p = sub.add_parser("init", help="Initialize workspace")
    init_p.add_argument("path", nargs="?", default=".")
    return parser


def dispatch_product(args: argparse.Namespace) -> int:
    if args.command == "bootstrap":
        root = Path(args.root) if getattr(args, "root", None) else None
        return run_bootstrap_cli(
            json_out=getattr(args, "json", False),
            root=root,
            repo=getattr(args, "repo", None),
            integrity_mode=getattr(args, "integrity_mode", "full"),
            epoch_id=getattr(args, "epoch_id", None),
        )
    if args.command == "attestation" and args.attestation_command == "export":
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
    if args.command == "simulate":
        return run_simulate_cli(
            fixture=getattr(args, "fixture", "pipe_l3_dora_violation"),
            json_out=getattr(args, "json", False),
            pause=getattr(args, "pause", False),
            epoch_id=getattr(args, "epoch_id", None),
        )
    if args.command == "analyze":
        return run_analyze_cli(
            args.target,
            out=args.out,
            package_dir=getattr(args, "package_dir", None),
            tenant_id=getattr(args, "tenant_id", "default"),
            compliance_pack=getattr(args, "pack", "DORA-2026"),
            epoch_id=getattr(args, "epoch_id", None),
            human=not getattr(args, "json", False),
            skip_bootstrap=getattr(args, "no_bootstrap", False),
        )
    if args.command == "doctor":
        print_human_banner("Environment diagnostics")
        return run_doctor(human=True)
    if args.command == "init":
        print_human_banner("Workspace bootstrap")
        return run_init(Path(args.path), human=True)
    return 2
