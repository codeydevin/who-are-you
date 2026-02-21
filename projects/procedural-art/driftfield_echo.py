#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from typing import List, Optional

from generate import ALPHABET, generate, stable_seed


def to_index_grid(lines: List[str]) -> List[List[int]]:
    return [[ALPHABET.index(ch) for ch in line] for line in lines]


def shift_grid(grid: List[List[int]], dx: int, dy: int) -> List[List[Optional[int]]]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    shifted: List[List[Optional[int]]] = [
        [None for _ in range(cols)] for _ in range(rows)
    ]
    for y in range(rows):
        src_y = y - dy
        if src_y < 0 or src_y >= rows:
            continue
        for x in range(cols):
            src_x = x - dx
            if src_x < 0 or src_x >= cols:
                continue
            shifted[y][x] = grid[src_y][src_x]
    return shifted


def blend_grid(
    base: List[List[int]],
    echo: List[List[Optional[int]]],
    strength: float,
) -> List[str]:
    rows = len(base)
    cols = len(base[0]) if rows else 0
    out: List[str] = []
    for y in range(rows):
        line = []
        for x in range(cols):
            base_val = base[y][x]
            echo_val = echo[y][x]
            if echo_val is None or strength <= 0.0:
                blended = base_val
            else:
                blended = round((1.0 - strength) * base_val + strength * echo_val)
            blended = max(0, min(len(ALPHABET) - 1, blended))
            line.append(ALPHABET[blended])
        out.append("".join(line))
    return out


def build_seed(date_str: str, phrase: str) -> float:
    return stable_seed(f"{date_str}::{phrase}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a driftfield with a shifted echo layer."
    )
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="echo-braid", help="Base seed phrase")
    parser.add_argument(
        "--echo-phrase",
        default="ember-skein",
        help="Echo seed phrase",
    )
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--smooth", type=int, default=1, help="Smoothing passes")
    parser.add_argument("--octaves", type=int, default=3)
    parser.add_argument("--persistence", type=float, default=0.55)
    parser.add_argument("--lacunarity", type=float, default=2.0)
    parser.add_argument("--contrast", type=float, default=1.0)
    parser.add_argument("--warp", type=float, default=0.6)
    parser.add_argument("--ridge", type=float, default=0.15)
    parser.add_argument("--bias", type=float, default=0.0)
    parser.add_argument("--tilt-x", type=float, default=0.0)
    parser.add_argument("--tilt-y", type=float, default=0.0)
    parser.add_argument("--echo-x", type=int, default=4, help="Echo offset columns")
    parser.add_argument("--echo-y", type=int, default=2, help="Echo offset rows")
    parser.add_argument("--echo-strength", type=float, default=0.45)
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    base_seed = build_seed(date_str, args.phrase)
    echo_seed = build_seed(date_str, args.echo_phrase)

    base_lines = generate(
        args.rows,
        args.cols,
        base_seed,
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
    echo_lines = generate(
        args.rows,
        args.cols,
        echo_seed,
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

    base_grid = to_index_grid(base_lines)
    echo_grid = shift_grid(to_index_grid(echo_lines), args.echo_x, args.echo_y)
    combined = blend_grid(base_grid, echo_grid, args.echo_strength)

    header = [
        f"Driftfield Echo {date_str}",
        f"Seed: {date_str}::{args.phrase}",
        f"Echo Seed: {date_str}::{args.echo_phrase}",
        f"Grid: {args.rows}x{args.cols}",
        f"Alphabet: {ALPHABET}",
        f"Echo offset: ({args.echo_x}, {args.echo_y})",
        f"Echo strength: {args.echo_strength}",
        f"Octaves: {args.octaves} (persistence {args.persistence}, lacunarity {args.lacunarity})",
        f"Contrast: {args.contrast}",
        f"Warp: {args.warp}",
        f"Ridge: {args.ridge}",
        f"Bias: {args.bias}",
        f"Tilt X: {args.tilt_x}",
        f"Tilt Y: {args.tilt_y}",
        "",
    ]

    content = "\n".join(header + combined) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
