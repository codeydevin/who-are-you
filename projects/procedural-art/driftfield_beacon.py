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
    beams: float,
    pulse: float,
    drift: float,
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

            beam = 0.5 + 0.5 * math.sin(theta * beams + seed_phase)
            pulse_wave = 0.5 + 0.5 * math.cos(r * pulse * math.tau + seed_phase * 0.7)
            sweep = 0.5 + 0.5 * math.sin((nx - ny) * drift * math.pi + seed_phase * 1.3)

            value = 0.5 * beam + 0.3 * pulse_wave + 0.2 * sweep
            if falloff > 0.0:
                value *= max(0.0, 1.0 - r) ** falloff
            if contrast != 1.0:
                value = value ** contrast
            value = clamp(value + bias)
            row.append(map_to_glyph(value))
        lines.append("".join(row))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a beacon-style Driftfield ASCII map.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="beacon-scan", help="Seed phrase")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--beams", type=float, default=10.0, help="Angular beam count")
    parser.add_argument("--pulse", type=float, default=2.6, help="Radial pulse frequency")
    parser.add_argument("--drift", type=float, default=3.1, help="Diagonal sweep frequency")
    parser.add_argument("--falloff", type=float, default=0.8, help="Edge fade strength")
    parser.add_argument("--contrast", type=float, default=1.1, help="Gamma-style contrast")
    parser.add_argument("--bias", type=float, default=0.02, help="Value bias (-1 to 1)")
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
        args.beams,
        args.pulse,
        args.drift,
        args.falloff,
        args.contrast,
        args.bias,
    )

    header = [
        f"Driftfield Beacon {date_str}",
        f"Seed: {seed_text}",
        f"Grid: {args.rows}x{args.cols}",
        f"Alphabet: {ALPHABET}",
        f"Beams: {args.beams}",
        f"Pulse: {args.pulse}",
        f"Drift: {args.drift}",
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
