#!/usr/bin/env python3
"""Merge two driftfield text grids into a new hybrid field."""
import argparse
import math
from datetime import datetime, timezone
from pathlib import Path


def parse_grid(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return []

    if "" in lines:
        blank_index = lines.index("")
        grid = lines[blank_index + 1 :]
    else:
        grid = lines[:]

    grid = [line.rstrip("\n") for line in grid if line.strip() != ""]
    return grid


def normalize_grid(grid: list[str], rows: int, cols: int) -> list[str]:
    padded = []
    for r in range(rows):
        if r < len(grid):
            line = grid[r]
        else:
            line = ""
        if len(line) < cols:
            line = line + " " * (cols - len(line))
        padded.append(line[:cols])
    return padded


def choose_from_a(r: int, c: int, pattern: str, stripe: int, phase: int) -> bool:
    if pattern == "checker":
        return (r + c + phase) % 2 == 0
    if pattern == "diagonal":
        return c - r + phase >= 0
    if pattern == "stripe-x":
        return (c // max(1, stripe)) % 2 == 0
    if pattern == "stripe-y":
        return (r // max(1, stripe)) % 2 == 0
    if pattern == "wave":
        wave = math.sin((c + phase) / 5.0 + r * 0.35)
        return wave >= 0
    return True


def merge_grids(
    grid_a: list[str],
    grid_b: list[str],
    pattern: str,
    stripe: int,
    phase: int,
    invert: bool,
) -> list[str]:
    rows = max(len(grid_a), len(grid_b))
    cols = max((len(line) for line in grid_a), default=0)
    cols = max(cols, max((len(line) for line in grid_b), default=0))

    norm_a = normalize_grid(grid_a, rows, cols)
    norm_b = normalize_grid(grid_b, rows, cols)

    merged = []
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            take_a = choose_from_a(r, c, pattern, stripe, phase)
            if invert:
                take_a = not take_a
            row_chars.append(norm_a[r][c] if take_a else norm_b[r][c])
        merged.append("".join(row_chars).rstrip())
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge two driftfield text grids into a hybrid field."
    )
    parser.add_argument("--input-a", required=True, help="Path to driftfield text A")
    parser.add_argument("--input-b", required=True, help="Path to driftfield text B")
    parser.add_argument(
        "--pattern",
        choices=("checker", "diagonal", "stripe-x", "stripe-y", "wave"),
        default="checker",
    )
    parser.add_argument("--stripe", type=int, default=4, help="Stripe width")
    parser.add_argument("--phase", type=int, default=0, help="Pattern phase offset")
    parser.add_argument("--invert", action="store_true", help="Invert pattern choice")
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    path_a = Path(args.input_a)
    path_b = Path(args.input_b)

    grid_a = parse_grid(path_a)
    grid_b = parse_grid(path_b)

    merged = merge_grids(grid_a, grid_b, args.pattern, args.stripe, args.phase, args.invert)

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    header = [
        f"Driftfield Merge {date_str}",
        f"Input A: {path_a}",
        f"Input B: {path_b}",
        f"Pattern: {args.pattern}",
        f"Stripe: {args.stripe}",
        f"Phase: {args.phase}",
        f"Invert: {args.invert}",
        "",
    ]

    content = "\n".join(header + merged) + "\n"

    if args.out:
        Path(args.out).write_text(content, encoding="utf-8")
    else:
        print(content, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
