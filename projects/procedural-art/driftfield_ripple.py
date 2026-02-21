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


def parse_centers(raw: str) -> list[tuple[float, float]]:
    centers = []
    for chunk in raw.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(",")
        if len(parts) != 2:
            raise ValueError(f"Invalid center '{chunk}', expected x,y")
        x, y = (float(parts[0]), float(parts[1]))
        centers.append((x, y))
    if not centers:
        raise ValueError("At least one center is required")
    return centers


def generate(
    rows: int,
    cols: int,
    seed: float,
    centers: list[tuple[float, float]],
    frequency: float,
    phase: float,
    interference: float,
    drift: float,
    contrast: float,
    bias: float,
) -> list[str]:
    lines = []
    for y in range(rows):
        row = []
        ny = y / (rows - 1) if rows > 1 else 0.0
        for x in range(cols):
            nx = x / (cols - 1) if cols > 1 else 0.0
            value = 0.0
            for cx, cy in centers:
                dx = nx - cx
                dy = ny - cy
                dist = math.hypot(dx, dy)
                ripple = 0.5 + 0.5 * math.sin(dist * frequency * math.tau + seed * phase)
                value += ripple
            value /= len(centers)
            interference_wave = 0.5 + 0.5 * math.sin((nx + ny + seed) * interference * math.pi)
            drift_wave = 0.5 + 0.5 * math.sin((nx * 2.8 - ny * 1.7 + seed) * drift * math.pi)
            value = 0.68 * value + 0.2 * interference_wave + 0.12 * drift_wave
            if contrast != 1.0:
                value = value ** contrast
            value = clamp(value + bias)
            row.append(map_to_glyph(value))
        lines.append("".join(row))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a ripple-interference Driftfield map.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="ripple-lantern", help="Seed phrase")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument(
        "--centers",
        default="0.3,0.4;0.7,0.6",
        help="Semicolon-separated center points (x,y) in 0..1",
    )
    parser.add_argument("--frequency", type=float, default=10.2, help="Ripple frequency")
    parser.add_argument("--phase", type=float, default=6.2, help="Phase multiplier")
    parser.add_argument("--interference", type=float, default=4.6, help="Interference wave strength")
    parser.add_argument("--drift", type=float, default=2.4, help="Drift wave strength")
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
    centers = parse_centers(args.centers)

    lines = generate(
        args.rows,
        args.cols,
        seed,
        centers,
        args.frequency,
        args.phase,
        args.interference,
        args.drift,
        args.contrast,
        args.bias,
    )

    header = [
        f"Driftfield Ripple {date_str}",
        f"Seed: {seed_text}",
        f"Grid: {args.rows}x{args.cols}",
        f"Alphabet: {ALPHABET}",
        f"Centers: {args.centers}",
        f"Frequency: {args.frequency}",
        f"Phase: {args.phase}",
        f"Interference: {args.interference}",
        f"Drift: {args.drift}",
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
