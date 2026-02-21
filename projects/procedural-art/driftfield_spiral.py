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


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def map_to_glyph(value: float) -> str:
    idx = int(clamp(value) * (len(ALPHABET) - 1))
    return ALPHABET[idx]


def generate(
    rows: int,
    cols: int,
    seed: float,
    arms: float,
    twist: float,
    ripples: float,
    falloff: float,
    contrast: float,
    bias: float,
) -> list[str]:
    lines = []
    seed_phase = seed * math.tau
    for y in range(rows):
        row = []
        for x in range(cols):
            nx = (x / (cols - 1)) * 2.0 - 1.0 if cols > 1 else 0.0
            ny = (y / (rows - 1)) * 2.0 - 1.0 if rows > 1 else 0.0
            r = math.hypot(nx, ny)
            theta = math.atan2(ny, nx)

            spiral = math.sin(r * arms * math.tau + theta * twist + seed_phase)
            coil = math.sin((1.0 - r) * (twist * 0.85) * math.tau + theta * arms * 0.7 + seed_phase * 0.6)
            ripple = math.sin((nx * ripples + ny * ripples * 0.65) * math.pi + seed_phase * 1.7)

            value = 0.55 * (0.5 + 0.5 * spiral) + 0.25 * (0.5 + 0.5 * coil) + 0.2 * (0.5 + 0.5 * ripple)
            if falloff > 0.0:
                value *= max(0.0, 1.0 - r) ** falloff
            if contrast != 1.0:
                value = value ** contrast
            value = clamp(value + bias)
            row.append(map_to_glyph(value))
        lines.append("".join(row))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a spiral Driftfield ASCII map.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="spiral-cairn", help="Seed phrase")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--arms", type=float, default=4.2, help="Radial arm frequency")
    parser.add_argument("--twist", type=float, default=3.1, help="Angular twist multiplier")
    parser.add_argument("--ripples", type=float, default=3.4, help="Diagonal ripple frequency")
    parser.add_argument("--falloff", type=float, default=0.95, help="Edge fade strength")
    parser.add_argument("--contrast", type=float, default=1.06, help="Gamma-style contrast")
    parser.add_argument("--bias", type=float, default=0.0, help="Value bias (-1 to 1)")
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
        args.arms,
        args.twist,
        args.ripples,
        args.falloff,
        args.contrast,
        args.bias,
    )

    header = [
        f"Driftfield Spiral {date_str}",
        f"Seed: {seed_text}",
        f"Grid: {args.rows}x{args.cols}",
        f"Alphabet: {ALPHABET}",
        f"Arms: {args.arms}",
        f"Twist: {args.twist}",
        f"Ripples: {args.ripples}",
        f"Falloff: {args.falloff}",
        f"Contrast: {args.contrast}",
        f"Bias: {args.bias}",
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
