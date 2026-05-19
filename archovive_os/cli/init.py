"""archovive init — workspace bootstrap."""
from __future__ import annotations

from pathlib import Path


def run_init(target: Path | None = None, *, human: bool = False) -> int:
    root = (target or Path.cwd()).resolve()
    cfg_dir = root / ".archovive"
    cfg_dir.mkdir(parents=True, exist_ok=True)

    config = cfg_dir / "config.yaml"
    if not config.exists():
        config.write_text(
            "# Archovive OS v3 workspace config\n"
            "compile_backend: runtime\n"
            "tenant_id: default\n"
            "engine_level: 3\n",
            encoding="utf-8",
        )

    gitignore = root / ".gitignore"
    marker = ".archovive/\n"
    if gitignore.exists() and marker.strip() not in gitignore.read_text(encoding="utf-8"):
        with gitignore.open("a", encoding="utf-8") as fh:
            fh.write("\n" + marker)
    elif not gitignore.exists():
        gitignore.write_text(marker, encoding="utf-8")

    if human:
        print()
        print(f"  Workspace: {root}")
        print(f"  Config:    {config}")
        print("  Defaults:  compile_backend=runtime, tenant_id=default, engine_level=3")
    else:
        print(f"Initialized Archovive OS workspace at {root}")
        print(f"  Config: {config}")
        print("  Default: compile_backend=runtime (v3 runtime-first)")
    return 0
