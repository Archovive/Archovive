"""
Shared CLI flags — runtime-first OS kernel interface.
"""
from __future__ import annotations

import argparse
from typing import Any


COMPILE_BACKEND_CHOICES = ("auto", "engine", "runtime", "verify")


def add_os_parent_flags(parser: argparse.ArgumentParser) -> None:
    """Attach global Archovive OS flags to a subcommand parser."""
    parser.add_argument(
        "--compile-backend",
        choices=COMPILE_BACKEND_CHOICES,
        default=None,
        help="Compile path: auto (runtime-first), engine, runtime, verify (default: env ARCHOVIVE_COMPILE or auto)",
    )
    parser.add_argument(
        "--tenant",
        "--tenant-id",
        dest="tenant_id",
        default="default",
        help="Tenant scope for fleet/comply/ops",
    )
    parser.add_argument(
        "--level",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Engine depth level L1/L2/L3 (default: 3)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON response (forced when stdout is not a TTY)")
    parser.add_argument("--yaml", action="store_true", help="Emit YAML response (requires PyYAML)")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Compact TTY summary (auto-enabled on interactive terminals)",
    )
    parser.add_argument(
        "--pretty",
        "--human",
        dest="human",
        action="store_true",
        help="Human/demo mode: context blocks + pretty JSON (also ARCHOVIVE_HUMAN=1)",
    )


def request_body(repo: str, args: argparse.Namespace, **extra: Any) -> dict[str, Any]:
    """Build REST request body with compile + tenant semantics."""
    body: dict[str, Any] = {
        "source_target": repo,
        "repo_path": repo,
        "tenant_id": getattr(args, "tenant_id", "default"),
        "engine_level": getattr(args, "level", 3),
        **extra,
    }
    backend = getattr(args, "compile_backend", None)
    if backend:
        body["compile_backend"] = backend
    return body


def emit_response(data: object, *, json_flag: bool, yaml_flag: bool) -> None:
    import json

    if yaml_flag:
        try:
            import yaml

            print(yaml.safe_dump(data, sort_keys=True))
            return
        except ImportError:
            print("PyYAML not installed; falling back to JSON", file=__import__("sys").stderr)
    print(json.dumps(data, indent=2, sort_keys=True))
