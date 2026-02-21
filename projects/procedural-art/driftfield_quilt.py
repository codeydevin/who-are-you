#!/usr/bin/env python3
"""Generate a tiled Driftfield quilt with per-tile seed variation."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from generate import ALPHABET, generate, stable_seed


FLIP_OPTIONS = {"none", "x", "y", "both"}


def flip_tile(lines: list[str], flip: str) -> list[str]:
    if flip == "none":
        return lines
    flipped = lines
    if flip in {"y", "both"}:
        flipped = list(reversed(flipped))
    if flip in {"x", "both"}:
        flipped = [line[::-1] for line in flipped]
    return flipped


def build_quilt(
    date_str: str,
    phrase: str,
    tiles_y: int,
    tiles_x: int,
    tile_rows: int,
    tile_cols: int,
    smooth: int,
    octaves: int,
    persistence: float,
    lacunarity: float,
    contrast: float,
    warp: float,
    ridge: float,
    bias: float,
    bias_step: float,
    warp_step: float,
    tilt_x: float,
    tilt_y: float,
    flip: str,
) -> list[str]:
    if tiles_y <= 0 or tiles_x <= 0:
        raise ValueError("tiles must be positive")
    if tile_rows <= 0 or tile_cols <= 0:
        raise ValueError("tile size must be positive")
    if flip not in FLIP_OPTIONS:
        raise ValueError(f"flip must be one of: {', '.join(sorted(FLIP_OPTIONS))}")

    tile_grid: list[list[list[str]]] = []
    for ty in range(tiles_y):
        row_tiles: list[list[str]] = []
        for tx in range(tiles_x):
            seed_text = f"{date_str}::{phrase}::tile-{ty}-{tx}"
            seed = stable_seed(seed_text)
            tile_bias = bias + (ty + tx) * bias_step
            tile_warp = warp + (ty + tx) * warp_step
            tile = generate(
                tile_rows,
                tile_cols,
                seed,
                smooth,
                octaves,
                persistence,
                lacunarity,
                contrast,
                tile_warp,
                ridge,
                tile_bias,
                tilt_x,
                tilt_y,
            )
            if flip != "none" and (ty + tx) % 2 == 1:
                tile = flip_tile(tile, flip)
            row_tiles.append(tile)
        tile_grid.append(row_tiles)

    lines: list[str] = []
    for ty in range(tiles_y):
        for row_idx in range(tile_rows):
            row_parts = [tile_grid[ty][tx][row_idx] for tx in range(tiles_x)]
            lines.append("".join(row_parts))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a tiled Driftfield quilt.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="driftfield-quilt", help="Seed phrase")
    parser.add_argument("--tiles-y", type=int, default=3, help="Tiles down")
    parser.add_argument("--tiles-x", type=int, default=4, help="Tiles across")
    parser.add_argument("--tile-rows", type=int, default=8, help="Rows per tile")
    parser.add_argument("--tile-cols", type=int, default=12, help="Cols per tile")
    parser.add_argument("--smooth", type=int, default=1, help="Smoothing passes")
    parser.add_argument("--octaves", type=int, default=3, help="Layered noise passes")
    parser.add_argument("--persistence", type=float, default=0.55, help="Amplitude decay")
    parser.add_argument("--lacunarity", type=float, default=2.0, help="Frequency growth")
    parser.add_argument("--contrast", type=float, default=1.0, help="Gamma-style contrast")
    parser.add_argument("--warp", type=float, default=0.1, help="Domain warp strength")
    parser.add_argument("--ridge", type=float, default=0.2, help="Ridge blend (0-1)")
    parser.add_argument("--bias", type=float, default=0.0, help="Value bias (-1 to 1)")
    parser.add_argument("--bias-step", type=float, default=0.02, help="Bias shift per tile")
    parser.add_argument("--warp-step", type=float, default=0.02, help="Warp shift per tile")
    parser.add_argument("--tilt-x", type=float, default=0.0, help="Linear gradient across columns")
    parser.add_argument("--tilt-y", type=float, default=0.0, help="Linear gradient across rows")
    parser.add_argument(
        "--flip",
        default="x",
        choices=sorted(FLIP_OPTIONS),
        help="Flip alternating tiles",
    )
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = build_quilt(
        date_str,
        args.phrase,
        args.tiles_y,
        args.tiles_x,
        args.tile_rows,
        args.tile_cols,
        args.smooth,
        args.octaves,
        args.persistence,
        args.lacunarity,
        args.contrast,
        args.warp,
        args.ridge,
        args.bias,
        args.bias_step,
        args.warp_step,
        args.tilt_x,
        args.tilt_y,
        args.flip,
    )

    total_rows = args.tiles_y * args.tile_rows
    total_cols = args.tiles_x * args.tile_cols

    header = [
        f"Driftfield Quilt {date_str}",
        f"Seed: {date_str}::{args.phrase}::tile-{{y}}-{{x}}",
        f"Grid: {total_rows}x{total_cols} | Tile: {args.tile_rows}x{args.tile_cols}",
        f"Tiles: {args.tiles_y}x{args.tiles_x} | Flip: {args.flip}",
        f"Alphabet: {ALPHABET}",
        f"Octaves: {args.octaves} (persistence {args.persistence}, lacunarity {args.lacunarity})",
        f"Contrast: {args.contrast}",
        f"Warp: {args.warp} (step {args.warp_step})",
        f"Ridge: {args.ridge}",
        f"Bias: {args.bias} (step {args.bias_step})",
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
