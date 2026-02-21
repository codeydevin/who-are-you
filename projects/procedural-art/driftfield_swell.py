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


def rotate(x: float, y: float, angle: float) -> tuple[float, float]:
    ca = math.cos(angle)
    sa = math.sin(angle)
    return x * ca - y * sa, x * sa + y * ca


def map_to_glyph(value: float) -> str:
    idx = int(value * (len(ALPHABET) - 1))
    return ALPHABET[idx]


def generate(
    rows: int,
    cols: int,
    seed: float,
    wave_x: float,
    wave_y: float,
    phase: float,
    noise_mix: float,
    eddy: float,
    contrast: float,
    bias: float,
) -> list[str]:
    x_denom = cols - 1 if cols > 1 else 1
    y_denom = rows - 1 if rows > 1 else 1
    lines = []
    for y in range(rows):
        row = []
        y_norm = (y / y_denom) - 0.5
        for x in range(cols):
            x_norm = (x / x_denom) - 0.5
            if eddy > 0.0:
                angle = (base_noise(x_norm * 1.7, y_norm * 1.7, seed + 11.1) - 0.5) * eddy
                x_rot, y_rot = rotate(x_norm, y_norm, angle)
            else:
                x_rot, y_rot = x_norm, y_norm
            wave = math.sin((x_rot * wave_x + y_rot * wave_y + phase) * math.tau)
            wave = wave * 0.5 + 0.5
            noise = base_noise(x_rot * 3.1, y_rot * 3.1, seed + 3.7)
            value = wave * (1.0 - noise_mix) + noise * noise_mix
            if contrast != 1.0:
                value = min(1.0, max(0.0, value**contrast))
            if bias != 0.0:
                value = min(1.0, max(0.0, value + bias))
            row.append(map_to_glyph(value))
        lines.append("".join(row))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a swell-style Driftfield ASCII map.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="swell", help="Seed phrase")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--wave-x", type=float, default=2.6, help="Wave frequency along X")
    parser.add_argument("--wave-y", type=float, default=1.8, help="Wave frequency along Y")
    parser.add_argument("--phase", type=float, default=0.15, help="Phase offset (radians)")
    parser.add_argument("--noise", type=float, default=0.28, help="Noise blend (0-1)")
    parser.add_argument("--eddy", type=float, default=0.9, help="Rotation eddy strength")
    parser.add_argument("--contrast", type=float, default=1.0, help="Gamma-style contrast")
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
        args.wave_x,
        args.wave_y,
        args.phase,
        args.noise,
        args.eddy,
        args.contrast,
        args.bias,
    )

    header = [
        f"Driftfield Swell {date_str}",
        f"Seed: {seed_text}",
        f"Grid: {args.rows}x{args.cols}",
        f"Alphabet: {ALPHABET}",
        f"Wave X: {args.wave_x}",
        f"Wave Y: {args.wave_y}",
        f"Phase: {args.phase}",
        f"Noise Mix: {args.noise}",
        f"Eddy: {args.eddy}",
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
