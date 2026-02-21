#!/usr/bin/env python3
"""Generate a banded Driftfield texture by weaving multiple seeds."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from generate import ALPHABET, generate, stable_seed


def build_weft(
    date_str: str,
    phrase: str,
    rows: int,
    cols: int,
    band_width: int,
    smooth: int,
    octaves: int,
    persistence: float,
    lacunarity: float,
    contrast: float,
    warp: float,
    ridge: float,
    bias: float,
    tilt_x: float,
    tilt_y: float,
) -> list[str]:
    if band_width <= 0:
        raise ValueError("band_width must be positive")
    bands: list[list[str]] = []
    band_count = (cols + band_width - 1) // band_width
    for idx in range(band_count):
        width = min(band_width, cols - idx * band_width)
        seed_text = f"{date_str}::{phrase}::band-{idx}"
        seed = stable_seed(seed_text)
        bands.append(
            generate(
                rows,
                width,
                seed,
                smooth,
                octaves,
                persistence,
                lacunarity,
                contrast,
                warp,
                ridge,
                bias,
                tilt_x,
                tilt_y,
            )
        )

    lines: list[str] = []
    for row_idx in range(rows):
        row_parts = [band[row_idx] for band in bands]
        lines.append("".join(row_parts))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a banded Driftfield weave.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="driftfield-weft", help="Seed phrase")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--band-width", type=int, default=8)
    parser.add_argument("--smooth", type=int, default=1, help="Smoothing passes")
    parser.add_argument("--octaves", type=int, default=3, help="Layered noise passes")
    parser.add_argument("--persistence", type=float, default=0.55, help="Amplitude decay")
    parser.add_argument("--lacunarity", type=float, default=2.0, help="Frequency growth")
    parser.add_argument("--contrast", type=float, default=1.0, help="Gamma-style contrast")
    parser.add_argument("--warp", type=float, default=0.1, help="Domain warp strength")
    parser.add_argument("--ridge", type=float, default=0.2, help="Ridge blend (0-1)")
    parser.add_argument("--bias", type=float, default=0.0, help="Value bias (-1 to 1)")
    parser.add_argument("--tilt-x", type=float, default=0.0, help="Linear gradient across columns")
    parser.add_argument("--tilt-y", type=float, default=0.0, help="Linear gradient across rows")
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = build_weft(
        date_str,
        args.phrase,
        args.rows,
        args.cols,
        args.band_width,
        args.smooth,
        args.octaves,
        args.persistence,
        args.lacunarity,
        args.contrast,
        args.warp,
        args.ridge,
        args.bias,
        args.tilt_x,
        args.tilt_y,
    )

    header = [
        f"Driftfield Weft {date_str}",
        f"Seed: {date_str}::{args.phrase}::band-{{index}}",
        f"Grid: {args.rows}x{args.cols} | Band width: {args.band_width}",
        f"Alphabet: {ALPHABET}",
        f"Octaves: {args.octaves} (persistence {args.persistence}, lacunarity {args.lacunarity})",
        f"Contrast: {args.contrast}",
        f"Warp: {args.warp}",
        f"Ridge: {args.ridge}",
        f"Bias: {args.bias}",
        f"Tilt X: {args.tilt_x}",
        f"Tilt Y: {args.tilt_y}",
        "",
    ]

    content = "\n".join(header + lines) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
