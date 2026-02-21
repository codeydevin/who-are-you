#!/usr/bin/env python3
"""Generate a lattice-style ASCII field from a deterministic seed."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import math
from pathlib import Path

ALPHABET = " .:-=+*#%@"


def seed_from(date_str: str, phrase: str) -> int:
    payload = f"{date_str}|{phrase}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    return int(digest[:12], 16)


def value_at(x: int, y: int, seed: int) -> float:
    sx = x + (seed % 997) * 0.013
    sy = y + (seed % 991) * 0.017
    wave = math.sin(sx * 0.27) + math.cos(sy * 0.33)
    diag = math.sin((sx + sy) * 0.12)
    lattice = math.cos((sx - sy) * 0.18)
    v = wave + diag * 0.6 + lattice * 0.4
    if x % 6 == 0 or y % 5 == 0:
        v += 0.9
    if (x + y) % 11 == 0:
        v -= 0.5
    return (math.tanh(v / 2.0) + 1.0) / 2.0


def render(rows: int, cols: int, seed: int) -> list[str]:
    lines = []
    for y in range(rows):
        row_chars = []
        for x in range(cols):
            v = value_at(x, y, seed)
            idx = min(len(ALPHABET) - 1, max(0, int(v * (len(ALPHABET) - 1))))
            row_chars.append(ALPHABET[idx])
        lines.append("".join(row_chars))
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a latticefield ASCII texture.")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--phrase", default="lattice-tide")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    seed = seed_from(args.date, args.phrase)
    lines = render(args.rows, args.cols, seed)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
