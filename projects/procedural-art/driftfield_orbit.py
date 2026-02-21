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
    rings: float,
    spin: float,
    ripples: float,
    falloff: float,
    contrast: float,
    bias: float,
) -> list[str]:
    lines = []
    for y in range(rows):
        row = []
        for x in range(cols):
            nx = (x / (cols - 1)) * 2.0 - 1.0 if cols > 1 else 0.0
            ny = (y / (rows - 1)) * 2.0 - 1.0 if rows > 1 else 0.0
            r = math.hypot(nx, ny)
            theta = math.atan2(ny, nx) + seed * math.tau
            orbit = 0.5 + 0.5 * math.sin(r * rings * math.pi + theta * spin)
            ripple = 0.5 + 0.5 * math.sin((nx + ny) * ripples * math.pi + seed * 6.13)
            value = 0.65 * orbit + 0.35 * ripple
            if falloff > 0.0:
                value *= max(0.0, 1.0 - r) ** falloff
            if contrast != 1.0:
                value = value ** contrast
            value = clamp(value + bias)
            row.append(map_to_glyph(value))
        lines.append("".join(row))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an orbital Driftfield ASCII map.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="orbit-drift", help="Seed phrase")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--rings", type=float, default=5.2, help="Radial band frequency")
    parser.add_argument("--spin", type=float, default=2.4, help="Angular spin multiplier")
    parser.add_argument("--ripples", type=float, default=3.6, help="Diagonal ripple frequency")
    parser.add_argument("--falloff", type=float, default=1.1, help="Edge fade strength")
    parser.add_argument("--contrast", type=float, default=1.05, help="Gamma-style contrast")
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
        args.rings,
        args.spin,
        args.ripples,
        args.falloff,
        args.contrast,
        args.bias,
    )

    header = [
        f"Driftfield Orbit {date_str}",
        f"Seed: {seed_text}",
        f"Grid: {args.rows}x{args.cols}",
        f"Alphabet: {ALPHABET}",
        f"Rings: {args.rings}",
        f"Spin: {args.spin}",
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
