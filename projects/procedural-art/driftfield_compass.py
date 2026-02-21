#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone

from generate import ALPHABET, generate, stable_seed

COMPASS_GRID = [
    ["NW", "N", "NE"],
    ["W", "C", "E"],
    ["SW", "S", "SE"],
]


def center_label(label: str, width: int) -> str:
    if len(label) >= width:
        return label[:width]
    pad = width - len(label)
    left = pad // 2
    right = pad - left
    return " " * left + label + " " * right


def build_tiles(
    date_str: str,
    phrase: str,
    rows: int,
    cols: int,
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
) -> dict[str, list[str]]:
    tiles: dict[str, list[str]] = {}
    for row in COMPASS_GRID:
        for direction in row:
            seed_text = f"{date_str}::{phrase}::{direction}"
            seed = stable_seed(seed_text)
            tiles[direction] = generate(
                rows,
                cols,
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
    return tiles


def assemble_compass(tiles: dict[str, list[str]], cols: int, gap: int) -> list[str]:
    lines: list[str] = []
    gap_str = " " * gap
    for row in COMPASS_GRID:
        label_line = gap_str.join(center_label(direction, cols) for direction in row)
        lines.append(label_line)
        for idx in range(len(next(iter(tiles.values())))):
            line = gap_str.join(tiles[direction][idx] for direction in row)
            lines.append(line)
        lines.append("")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Driftfield compass mosaic.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="driftfield-compass", help="Seed phrase")
    parser.add_argument("--rows", type=int, default=12)
    parser.add_argument("--cols", type=int, default=26)
    parser.add_argument("--gap", type=int, default=3, help="Spaces between tiles")
    parser.add_argument("--smooth", type=int, default=1, help="Smoothing passes")
    parser.add_argument("--octaves", type=int, default=3, help="Layered noise passes")
    parser.add_argument("--persistence", type=float, default=0.55, help="Amplitude decay")
    parser.add_argument("--lacunarity", type=float, default=2.0, help="Frequency growth")
    parser.add_argument("--contrast", type=float, default=1.0, help="Gamma-style contrast")
    parser.add_argument("--warp", type=float, default=0.1, help="Domain warp strength")
    parser.add_argument("--ridge", type=float, default=0.15, help="Ridge blend (0-1)")
    parser.add_argument("--bias", type=float, default=0.0, help="Value bias (-1 to 1)")
    parser.add_argument("--tilt-x", type=float, default=0.0, help="Linear gradient across columns")
    parser.add_argument("--tilt-y", type=float, default=0.0, help="Linear gradient across rows")
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    tiles = build_tiles(
        date_str,
        args.phrase,
        args.rows,
        args.cols,
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
        f"Driftfield Compass {date_str}",
        f"Seed: {date_str}::{args.phrase}::{{direction}}",
        f"Tile: {args.rows}x{args.cols} | Gap: {args.gap}",
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

    compass = assemble_compass(tiles, args.cols, args.gap)
    content = "\n".join(header + compass) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
