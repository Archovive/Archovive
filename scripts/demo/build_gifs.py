#!/usr/bin/env python3
"""Generate terminal-style demo GIFs for the public repo (no asciinema required)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "assets" / "gifs"
W, H, FS = 920, 520, 16
BG = (13, 17, 23)
FG = (201, 209, 217)
ACC = (88, 166, 255)
RED = (248, 81, 73)
GRN = (63, 185, 80)
YLW = (210, 153, 34)


def _font() -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, FS)
    return ImageFont.load_default()


def frame(lines: list[tuple[str, tuple[int, int, int] | None]]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = _font()
    y = 24
    for text, color in lines:
        draw.text((24, y), text, fill=color or FG, font=font)
        y += 22
    return img


def write_gif(name: str, frames: list[Image.Image], duration: int = 900) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.gif"
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=True,
    )
    return path


def gate_frames() -> list[Image.Image]:
    return [
        frame([("$ archovive simulate", ACC), ("", None)]),
        frame([
            ("$ archovive simulate", ACC),
            ("", None),
            ("ARCHOVIVE GATE — DORA Boundary Crossing", FG),
        ]),
        frame([
            ("$ archovive simulate", ACC),
            ("", None),
            ("ARCHOVIVE GATE — DORA Boundary Crossing", FG),
            ("Verdict: POLICY_VIOLATION", RED),
        ]),
        frame([
            ("ARCHOVIVE GATE — DORA Boundary Crossing", FG),
            ("Verdict: POLICY_VIOLATION", RED),
            ("graph_hash: fee879ce…c734aa", FG),
            ("replay_hash: 3e700b6a…d3b9736", FG),
            ("Exit Code: 2", YLW),
        ]),
    ]


def ci_frames() -> list[Image.Image]:
    return [
        frame([("GitHub Actions · architecture-gate", ACC), ("▶ Run archovive ci check", FG)]),
        frame([
            ("▶ Run archovive ci check", FG),
            ("ARCHOVIVE GATE — DORA Boundary Crossing", FG),
            ("Verdict: POLICY_VIOLATION", RED),
        ]),
        frame([
            ("✗ architecture-gate failed (exit 2)", RED),
            ("Verdict: POLICY_VIOLATION", RED),
            ("Merge blocked · policy violation", YLW),
        ]),
    ]


def drift_frames() -> list[Image.Image]:
    return [
        frame([("$ archovive diff baseline/ HEAD", ACC)]),
        frame([
            ("Drift matrix (compact)", FG),
            ("  structural_drift .... measured", FG),
            ("  boundary_crossing ... api→payments.ledger", RED),
            ("  drift_score ......... 0.42", YLW),
        ]),
        frame([
            ("Drift matrix (compact)", FG),
            ("  boundary_crossing ... api→payments.ledger", RED),
            ("Exit Code: 1", YLW),
            ("Not SonarQube — architecture drift.", ACC),
        ]),
    ]


def airgap_frames() -> list[Image.Image]:
    return [
        frame([("$ export ARCHOVIVE_ISOLATED=1", ACC)]),
        frame([
            ("$ archovive run", ACC),
            ("Running in isolated mode (offline bundle)", GRN),
            ("verify_signature.sh .... OK", GRN),
        ]),
        frame([
            ("ARCHOVIVE GATE — DORA Boundary Crossing", FG),
            ("Verdict: POLICY_VIOLATION", RED),
            ("Exit Code: 2", YLW),
            ("No cloud · no telemetry", ACC),
        ]),
    ]


def evidence_frames() -> list[Image.Image]:
    return [
        frame([("$ archovive audit export --bundle", ACC)]),
        frame([
            ("Writing evidence pack…", FG),
            ("  attestation.json", GRN),
            ("  sbom.json", GRN),
            ("  compliance_report.json", GRN),
        ]),
        frame([
            ("  file_hashes.json", GRN),
            ("archovive verify attestation.json .... OK", GRN),
            ("Evidence pack ready · not Vanta.", ACC),
        ]),
    ]


def graph_frames() -> list[Image.Image]:
    return [
        frame([("$ archovive run --compact", ACC)]),
        frame([
            ("[1/4] Architecture graph", FG),
            ("  boundary_crossings ... 1", RED),
            ("  coupling_index ....... 0.833", FG),
        ]),
        frame([
            ("[3/4] Policy evaluation", FG),
            ("  [FAIL] DORA_2026 :: dora_crossings_max", RED),
            ("Verdict: POLICY_VIOLATION · Exit Code: 2", YLW),
        ]),
    ]


def main() -> None:
    scenes = {
        "gate": gate_frames(),
        "ci": ci_frames(),
        "drift": drift_frames(),
        "airgap": airgap_frames(),
        "evidence": evidence_frames(),
        "graph": graph_frames(),
    }
    for name, frames in scenes.items():
        path = write_gif(name, frames)
        print(f"wrote {path} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
