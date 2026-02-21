#!/usr/bin/env python3
"""traceweaver: a tiny CLI to generate directional ASCII textiles.

Usage:
  python3 2026-02-21-traceweaver.py --width 80 --height 24 --seed 42
  python3 2026-02-21-traceweaver.py --width 120 --height 36 --palette weave
"""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass

PALETTES = {
    "weave": ".:+*#%@",
    "fog": " .:-=+*",
    "ember": " .,:;ox%#",
    "wire": " .|/\\-",
}


@dataclass
class Params:
    width: int
    height: int
    seed: int
    palette: str
    density: float
    twist: float
    drift: float


def parse_args() -> Params:
    parser = argparse.ArgumentParser(description="Generate ASCII textile fields.")
    parser.add_argument("--width", type=int, default=80)
    parser.add_argument("--height", type=int, default=24)
    parser.add_argument("--seed", type=int, default=21)
    parser.add_argument("--palette", choices=sorted(PALETTES.keys()), default="weave")
    parser.add_argument("--density", type=float, default=0.62)
    parser.add_argument("--twist", type=float, default=1.7)
    parser.add_argument("--drift", type=float, default=0.35)
    args = parser.parse_args()
    return Params(
        width=max(10, args.width),
        height=max(6, args.height),
        seed=args.seed,
        palette=args.palette,
        density=max(0.1, min(0.95, args.density)),
        twist=max(0.1, args.twist),
        drift=max(0.0, min(1.0, args.drift)),
    )


def blend(a: float, b: float, t: float) -> float:
    return a * (1 - t) + b * t


def field_value(x: int, y: int, params: Params, rng: random.Random) -> float:
    nx = x / max(1, params.width - 1)
    ny = y / max(1, params.height - 1)
    wave = math.sin((nx * 6.1 + ny * params.twist) * math.pi)
    cross = math.cos((ny * 5.3 - nx * 2.7) * math.pi)
    jitter = rng.random() * params.drift
    ridge = math.sin((nx * 12.0 - ny * 3.7) * math.pi)
    core = blend(wave, cross, 0.45) + ridge * 0.3
    return core * params.density + jitter


def render(params: Params) -> str:
    rng = random.Random(params.seed)
    palette = PALETTES[params.palette]
    rows = []
    for y in range(params.height):
        row = []
        for x in range(params.width):
            value = field_value(x, y, params, rng)
            idx = int((value + 1) / 2 * (len(palette) - 1))
            idx = max(0, min(len(palette) - 1, idx))
            row.append(palette[idx])
        rows.append("".join(row))
    return "\n".join(rows)


def main() -> None:
    params = parse_args()
    print(render(params))


if __name__ == "__main__":
    main()
