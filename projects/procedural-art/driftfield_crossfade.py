#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone

from generate import (
    ALPHABET,
    map_to_glyph,
    octave_noise,
    ridgeify,
    smooth,
    stable_seed,
    warp_coords,
)


def clamp(value: float) -> float:
    return min(1.0, max(0.0, value))


def ease_curve(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)


def blend_field(
    rows: int,
    cols: int,
    seed_a: float,
    seed_b: float,
    axis: str,
    curve: str,
    smooth_passes: int,
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
    x_denom = cols - 1 if cols > 1 else 1
    y_denom = rows - 1 if rows > 1 else 1
    grid: list[list[float]] = []
    for y in range(rows):
        row: list[float] = []
        for x in range(cols):
            t = x / x_denom if axis == "x" else y / y_denom
            if curve == "ease":
                t = ease_curve(t)
            tilt = tilt_x * ((x / x_denom) - 0.5) + tilt_y * ((y / y_denom) - 0.5)
            val_a = (
                octave_noise(
                    *warp_coords(x, y, seed_a, warp),
                    seed_a,
                    octaves,
                    persistence,
                    lacunarity,
                )
                + tilt
            )
            val_b = (
                octave_noise(
                    *warp_coords(x, y, seed_b, warp),
                    seed_b,
                    octaves,
                    persistence,
                    lacunarity,
                )
                + tilt
            )
            row.append((1.0 - t) * val_a + t * val_b)
        grid.append(row)

    for _ in range(smooth_passes):
        grid = smooth(grid)

    if ridge > 0.0:
        grid = [[ridgeify(v, ridge) for v in row] for row in grid]

    if contrast != 1.0:
        grid = [[clamp(v**contrast) for v in row] for row in grid]

    if bias != 0.0:
        grid = [[clamp(v + bias) for v in row] for row in grid]

    return ["".join(map_to_glyph(clamp(v)) for v in row) for row in grid]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a driftfield that crossfades between two seeds."
    )
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase-a", default="crossfade-origin", help="Seed phrase A")
    parser.add_argument("--phrase-b", default="crossfade-drift", help="Seed phrase B")
    parser.add_argument("--rows", type=int, default=18)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument(
        "--axis",
        choices=("x", "y"),
        default="x",
        help="Blend direction: x (columns) or y (rows)",
    )
    parser.add_argument(
        "--curve",
        choices=("linear", "ease"),
        default="linear",
        help="Blend curve: linear or ease",
    )
    parser.add_argument("--smooth", type=int, default=1, help="Smoothing passes")
    parser.add_argument("--octaves", type=int, default=3, help="Layered noise passes")
    parser.add_argument("--persistence", type=float, default=0.55)
    parser.add_argument("--lacunarity", type=float, default=2.0)
    parser.add_argument("--contrast", type=float, default=1.05)
    parser.add_argument("--warp", type=float, default=0.4)
    parser.add_argument("--ridge", type=float, default=0.12)
    parser.add_argument("--bias", type=float, default=0.0)
    parser.add_argument("--tilt-x", type=float, default=0.0)
    parser.add_argument("--tilt-y", type=float, default=0.0)
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    seed_text_a = f"{date_str}::{args.phrase_a}"
    seed_text_b = f"{date_str}::{args.phrase_b}"
    seed_a = stable_seed(seed_text_a)
    seed_b = stable_seed(seed_text_b)

    lines = blend_field(
        args.rows,
        args.cols,
        seed_a,
        seed_b,
        args.axis,
        args.curve,
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
        f"Driftfield Crossfade {date_str}",
        f"Seed A: {seed_text_a}",
        f"Seed B: {seed_text_b}",
        f"Grid: {args.rows}x{args.cols}",
        f"Blend axis: {args.axis}",
        f"Blend curve: {args.curve}",
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
