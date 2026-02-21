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


def generate(
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
) -> list[str]:
    grid = [
        [
            octave_noise(
                *warp_coords(x, y, seed, warp),
                seed,
                octaves,
                persistence,
                lacunarity,
            )
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
    return ["".join(map_to_glyph(v) for v in row) for row in grid]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Driftfield ASCII map.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="driftfield", help="Seed phrase")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--smooth", type=int, default=1, help="Smoothing passes")
    parser.add_argument("--octaves", type=int, default=3, help="Layered noise passes")
    parser.add_argument("--persistence", type=float, default=0.55, help="Amplitude decay")
    parser.add_argument("--lacunarity", type=float, default=2.0, help="Frequency growth")
    parser.add_argument("--contrast", type=float, default=1.0, help="Gamma-style contrast")
    parser.add_argument("--warp", type=float, default=0.0, help="Domain warp strength")
    parser.add_argument("--ridge", type=float, default=0.0, help="Ridge blend (0-1)")
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    seed_text = f"{date_str}::{args.phrase}"
    seed = stable_seed(seed_text)

    lines = generate(
        args.rows,
        args.cols,
        seed,
        args.smooth,
        args.octaves,
        args.persistence,
        args.lacunarity,
        args.contrast,
        args.warp,
        args.ridge,
    )

    header = [
        f"Driftfield {date_str}",
        f"Seed: {seed_text}",
        f"Grid: {args.rows}x{args.cols}",
        f"Alphabet: {ALPHABET}",
        f"Octaves: {args.octaves} (persistence {args.persistence}, lacunarity {args.lacunarity})",
        f"Contrast: {args.contrast}",
        f"Warp: {args.warp}",
        f"Ridge: {args.ridge}",
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
