#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone

import generate

ALPHABET = " .:-=+*#%@"


def grid_values(
    rows: int,
    cols: int,
    seed: float,
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
) -> list[list[float]]:
    x_denom = cols - 1 if cols > 1 else 1
    y_denom = rows - 1 if rows > 1 else 1
    grid = [
        [
            generate.octave_noise(
                *generate.warp_coords(x, y, seed, warp),
                seed,
                octaves,
                persistence,
                lacunarity,
            )
            + tilt_x * ((x / x_denom) - 0.5)
            + tilt_y * ((y / y_denom) - 0.5)
            for x in range(cols)
        ]
        for y in range(rows)
    ]

    for _ in range(smooth_passes):
        grid = generate.smooth(grid)

    if ridge > 0.0:
        grid = [[generate.ridgeify(v, ridge) for v in row] for row in grid]
    if contrast != 1.0:
        grid = [[min(1.0, max(0.0, v**contrast)) for v in row] for row in grid]
    if bias != 0.0:
        grid = [[min(1.0, max(0.0, v + bias)) for v in row] for row in grid]

    return grid


def map_delta(value: float) -> str:
    idx = int(value * (len(ALPHABET) - 1))
    return ALPHABET[idx]


def format_delta(delta: list[list[float]]) -> list[str]:
    lines = []
    for row in delta:
        lines.append("".join(map_delta(v) for v in row))
    return lines


def summarize(delta: list[list[float]]) -> dict:
    flat = [v for row in delta for v in row]
    if not flat:
        return {"min": 0.0, "max": 0.0, "avg": 0.0}
    return {
        "min": min(flat),
        "max": max(flat),
        "avg": sum(flat) / len(flat),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare two Driftfield seeds and output a delta map.")
    parser.add_argument("--date-a", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--date-b", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase-a", default="driftfield", help="Seed phrase A")
    parser.add_argument("--phrase-b", default="driftfield", help="Seed phrase B")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--smooth", type=int, default=1, help="Smoothing passes")
    parser.add_argument("--octaves", type=int, default=3, help="Layered noise passes")
    parser.add_argument("--persistence", type=float, default=0.55, help="Amplitude decay")
    parser.add_argument("--lacunarity", type=float, default=2.0, help="Frequency growth")
    parser.add_argument("--contrast", type=float, default=1.0, help="Gamma-style contrast")
    parser.add_argument("--warp", type=float, default=0.0, help="Domain warp strength")
    parser.add_argument("--ridge", type=float, default=0.0, help="Ridge blend (0-1)")
    parser.add_argument("--bias", type=float, default=0.0, help="Value bias (-1 to 1)")
    parser.add_argument("--tilt-x", type=float, default=0.0, help="Linear gradient across columns")
    parser.add_argument("--tilt-y", type=float, default=0.0, help="Linear gradient across rows")
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    date_a = args.date_a or today
    date_b = args.date_b or today

    seed_text_a = f"{date_a}::{args.phrase_a}"
    seed_text_b = f"{date_b}::{args.phrase_b}"
    seed_a = generate.stable_seed(seed_text_a)
    seed_b = generate.stable_seed(seed_text_b)

    grid_a = grid_values(
        args.rows,
        args.cols,
        seed_a,
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

    grid_b = grid_values(
        args.rows,
        args.cols,
        seed_b,
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

    delta = [
        [min(1.0, max(0.0, abs(a - b))) for a, b in zip(row_a, row_b)]
        for row_a, row_b in zip(grid_a, grid_b)
    ]

    stats = summarize(delta)

    header = [
        f"Driftfield Delta {today}",
        f"Seed A: {seed_text_a}",
        f"Seed B: {seed_text_b}",
        f"Grid: {args.rows}x{args.cols}",
        f"Alphabet: {ALPHABET}",
        f"Octaves: {args.octaves} (persistence {args.persistence}, lacunarity {args.lacunarity})",
        f"Contrast: {args.contrast}",
        f"Warp: {args.warp}",
        f"Ridge: {args.ridge}",
        f"Bias: {args.bias}",
        f"Tilt X: {args.tilt_x}",
        f"Tilt Y: {args.tilt_y}",
        f"Delta min: {stats['min']:.3f}",
        f"Delta max: {stats['max']:.3f}",
        f"Delta avg: {stats['avg']:.3f}",
        "",
    ]

    content = "\n".join(header + format_delta(delta)) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
