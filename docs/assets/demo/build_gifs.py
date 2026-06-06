#!/usr/bin/env python3
"""Pillow fallback for demo GIFs — auto-crops to content (no 920×520 void)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs" / "assets" / "gifs"
FS = 18
PAD = 20
LINE = 24
BG = (30, 30, 46)
FG = (205, 214, 244)
ACC = (137, 180, 250)
RED = (243, 139, 168)
GRN = (166, 227, 161)
YLW = (249, 226, 175)


def _font() -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
    ):
        if Path(path).is_file():
            return ImageFont.truetype(path, FS)
    return ImageFont.load_default()


def _text_bbox(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int, int, int]:
    if not text:
        return (0, 0, 0, LINE)
    return draw.textbbox((0, 0), text, font=font)


def frame(lines: list[tuple[str, tuple[int, int, int] | None]]) -> Image.Image:
    font = _font()
    probe = Image.new("RGB", (1, 1), BG)
    draw = ImageDraw.Draw(probe)
    max_w = 0
    height = PAD
    for text, _ in lines:
        if not text:
            height += LINE // 2
            continue
        bbox = _text_bbox(draw, text, font)
        max_w = max(max_w, bbox[2] - bbox[0])
        height += LINE
    width = max(480, max_w + PAD * 2)
    height = max(120, height + PAD)

    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    y = PAD
    for text, color in lines:
        if not text:
            y += LINE // 2
            continue
        draw.text((PAD, y), text, fill=color or FG, font=font)
        y += LINE
    return img


def _normalize(frames: list[Image.Image]) -> list[Image.Image]:
    w = max(im.size[0] for im in frames)
    h = max(im.size[1] for im in frames)
    out: list[Image.Image] = []
    for im in frames:
        if im.size == (w, h):
            out.append(im)
            continue
        canvas = Image.new("RGB", (w, h), BG)
        canvas.paste(im, (0, 0))
        out.append(canvas)
    return out


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
        frame([("$ archovive simulate", ACC)]),
        frame([
            ("$ archovive simulate", ACC),
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
        frame([("▶ Run archovive ci check", ACC)]),
        frame([
            ("ARCHOVIVE GATE — DORA Boundary Crossing", FG),
            ("Verdict: POLICY_VIOLATION", RED),
            ("Exit Code: 2", YLW),
        ]),
        frame([
            ("✗ architecture-gate failed (exit 2)", RED),
            ("Merge blocked · policy violation", YLW),
        ]),
    ]


def drift_frames() -> list[Image.Image]:
    return [
        frame([("$ archovive diff baseline/ HEAD", ACC)]),
        frame([
            ("Drift matrix (compact)", FG),
            ("  boundary_crossing ... api→payments.ledger", RED),
            ("  drift_score ......... 0.42", YLW),
            ("Exit Code: 1", YLW),
        ]),
    ]


def airgap_frames() -> list[Image.Image]:
    return [
        frame([("$ export ARCHOVIVE_ISOLATED=1", ACC), ("$ archovive run", ACC)]),
        frame([
            ("Running in isolated mode (offline bundle)", GRN),
            ("verify_signature.sh .... OK", GRN),
            ("Verdict: POLICY_VIOLATION", RED),
            ("Exit Code: 2", YLW),
        ]),
    ]


def evidence_frames() -> list[Image.Image]:
    return [
        frame([("$ archovive audit export --bundle", ACC)]),
        frame([
            ("  attestation.json", GRN),
            ("  sbom.json", GRN),
            ("  compliance_report.json", GRN),
            ("  file_hashes.json", GRN),
        ]),
        frame([("archovive verify attestation.json .... OK", GRN)]),
    ]


def graph_frames() -> list[Image.Image]:
    return [
        frame([("$ archovive run --compact", ACC)]),
        frame([
            ("  boundary_crossings ... 1", RED),
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
    for name, raw in scenes.items():
        frames = _normalize(raw)
        path = write_gif(name, frames)
        print(f"wrote {path} ({len(frames)} frames, {frames[0].size[0]}x{frames[0].size[1]})")


if __name__ == "__main__":
    main()
