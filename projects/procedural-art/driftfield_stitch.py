#!/usr/bin/env python3
import argparse
import math
from datetime import datetime, timezone

ALPHABET = ".,:;~^*+=?%$#@"


def stable_seed(text: str) -> float:
    h = 0
    for ch in text:
        h = (h * 31 + ord(ch)) % 1000000
    return h / 1000000.0


def base_noise(x: float, y: float, seed: float) -> float:
    v = math.sin(x * 12.9898 + y * 78.233 + seed) * 43758.5453
    return v - math.floor(v)


def octave_noise(
    x: float,
    y: float,
    seed: float,
    octaves: int,
    persistence: float,
    lacunarity: float,
) -> float:
    value = 0.0
    amplitude = 1.0
    frequency = 1.0
    norm = 0.0
    for i in range(octaves):
        value += base_noise(x * frequency, y * frequency, seed + i * 19.19) * amplitude
        norm += amplitude
        amplitude *= persistence
        frequency *= lacunarity
    return value / norm if norm else 0.0


def smooth(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    out = [[0.0 for _ in range(cols)] for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            acc = 0.0
            count = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny = y + dy
                    nx = x + dx
                    if 0 <= ny < rows and 0 <= nx < cols:
                        acc += grid[ny][nx]
                        count += 1
            out[y][x] = acc / count if count else grid[y][x]
    return out


def map_to_glyph(value: float) -> str:
    idx = int(value * (len(ALPHABET) - 1))
    return ALPHABET[idx]


def ridgeify(value: float, strength: float) -> float:
    if strength <= 0.0:
        return value
    ridge = 1.0 - abs(2.0 * value - 1.0)
    return (1.0 - strength) * value + strength * ridge


def warp_coords(x: float, y: float, seed: float, strength: float) -> tuple[float, float]:
    if strength <= 0.0:
        return x, y
    low_freq = 0.15
    dx = (base_noise(x * low_freq, y * low_freq, seed + 13.7) - 0.5) * strength
    dy = (base_noise(x * low_freq, y * low_freq, seed + 42.1) - 0.5) * strength
    return x + dx, y + dy


def generate_tile(
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
) -> list[str]:
    x_denom = cols - 1 if cols > 1 else 1
    y_denom = rows - 1 if rows > 1 else 1
    grid = [
        [
            octave_noise(
                *warp_coords(x, y, seed, warp),
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
        grid = smooth(grid)
    if ridge > 0.0:
        grid = [[ridgeify(v, ridge) for v in row] for row in grid]
    if contrast != 1.0:
        grid = [[min(1.0, max(0.0, v**contrast)) for v in row] for row in grid]
    if bias != 0.0:
        grid = [[min(1.0, max(0.0, v + bias)) for v in row] for row in grid]
    return ["".join(map_to_glyph(v) for v in row) for row in grid]


def stitch_tiles(tiles: list[list[str]], tiles_x: int, tiles_y: int, seam: bool) -> list[str]:
    if not tiles:
        return []
    tile_rows = len(tiles[0])
    tile_cols = len(tiles[0][0]) if tile_rows else 0

    stitched = []
    for ty in range(tiles_y):
        row_tiles = tiles[ty * tiles_x : (ty + 1) * tiles_x]
        for r in range(tile_rows):
            parts = []
            for tile in row_tiles:
                parts.append(tile[r])
            if seam:
                stitched.append("|".join(parts))
            else:
                stitched.append("".join(parts))
        if seam and ty < tiles_y - 1:
            line = "-" * tile_cols
            stitched.append("+".join([line] * tiles_x))
    return stitched


def main() -> int:
    parser = argparse.ArgumentParser(description="Stitch multiple Driftfield tiles into a panel.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrases", default="stitchline", help="Comma-separated seed phrases")
    parser.add_argument("--tiles-x", type=int, default=None, help="Number of tiles across")
    parser.add_argument("--tiles-y", type=int, default=None, help="Number of tiles down")
    parser.add_argument("--tile-rows", type=int, default=10)
    parser.add_argument("--tile-cols", type=int, default=30)
    parser.add_argument("--smooth", type=int, default=1)
    parser.add_argument("--octaves", type=int, default=3)
    parser.add_argument("--persistence", type=float, default=0.55)
    parser.add_argument("--lacunarity", type=float, default=2.0)
    parser.add_argument("--contrast", type=float, default=1.0)
    parser.add_argument("--warp", type=float, default=0.7)
    parser.add_argument("--ridge", type=float, default=0.2)
    parser.add_argument("--bias", type=float, default=0.0)
    parser.add_argument("--tilt-x", type=float, default=0.0)
    parser.add_argument("--tilt-y", type=float, default=0.0)
    parser.add_argument("--no-seam", action="store_true", help="Disable seam markers")
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    phrase_list = [p.strip() for p in args.phrases.split(",") if p.strip()]
    if not phrase_list:
        phrase_list = ["stitchline"]

    tiles_x = args.tiles_x
    tiles_y = args.tiles_y
    if tiles_x is None and tiles_y is None:
        tiles_x = min(3, len(phrase_list))
        tiles_y = math.ceil(len(phrase_list) / tiles_x)
    elif tiles_x is None:
        tiles_y = max(1, tiles_y)
        tiles_x = math.ceil(len(phrase_list) / tiles_y)
    elif tiles_y is None:
        tiles_x = max(1, tiles_x)
        tiles_y = math.ceil(len(phrase_list) / tiles_x)

    tile_count = tiles_x * tiles_y
    tiles = []
    for idx in range(tile_count):
        phrase = phrase_list[idx % len(phrase_list)]
        seed_text = f"{date_str}::{phrase}::{idx}"
        seed = stable_seed(seed_text)
        tile = generate_tile(
            args.tile_rows,
            args.tile_cols,
            seed,
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
        tiles.append(tile)

    stitched = stitch_tiles(tiles, tiles_x, tiles_y, not args.no_seam)

    header = [
        f"Driftfield Stitch {date_str}",
        f"Tiles: {tiles_x}x{tiles_y} ({args.tile_rows}x{args.tile_cols} each)",
        f"Phrases: {', '.join(phrase_list)}",
        f"Alphabet: {ALPHABET}",
        f"Octaves: {args.octaves} (persistence {args.persistence}, lacunarity {args.lacunarity})",
        f"Contrast: {args.contrast}",
        f"Warp: {args.warp}",
        f"Ridge: {args.ridge}",
        f"Bias: {args.bias}",
        f"Tilt X: {args.tilt_x}",
        f"Tilt Y: {args.tilt_y}",
        f"Seams: {'off' if args.no_seam else 'on'}",
        "",
    ]

    content = "\n".join(header + stitched) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
