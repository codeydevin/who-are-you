#!/usr/bin/env python3
"""Signal Cartography marker generator.

Creates a three-line marker (Sense, Vector, Anchor) with optional overrides.
"""

from __future__ import annotations

import argparse
import datetime as dt
import random
from typing import Iterable

SENSE_WORDS = [
    "low hum",
    "edge-glow",
    "soft static",
    "paper rustle",
    "quiet pulse",
    "wind shift",
    "glass-bright",
    "warm click",
    "far echo",
    "dry heat",
    "thin rain",
    "blue silence",
]

VECTOR_WORDS = [
    "northward",
    "tightening",
    "widening",
    "settling",
    "lifting",
    "looping",
    "clearing",
    "slowing",
    "accelerating",
    "spiraling",
    "drifting",
    "anchoring",
]

ANCHOR_WORDS = [
    "breath count",
    "water line",
    "desk lamp",
    "heartbeat",
    "window light",
    "stone weight",
    "walking pace",
    "coffee warmth",
    "page margin",
    "thread line",
    "midnight note",
    "pulse check",
]


def pick(rng: random.Random, options: Iterable[str]) -> str:
    choices = list(options)
    return rng.choice(choices)


def build_marker(seed: str, sense: str | None, vector: str | None, anchor: str | None) -> list[str]:
    rng = random.Random(seed)
    return [
        f"Sense: {sense or pick(rng, SENSE_WORDS)}",
        f"Vector: {vector or pick(rng, VECTOR_WORDS)}",
        f"Anchor: {anchor or pick(rng, ANCHOR_WORDS)}",
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Signal Cartography marker.")
    parser.add_argument("--seed", help="Seed string for deterministic output (default: YYYY-MM-DD).")
    parser.add_argument("--sense", help="Override the Sense line.")
    parser.add_argument("--vector", help="Override the Vector line.")
    parser.add_argument("--anchor", help="Override the Anchor line.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    seed = args.seed or dt.date.today().isoformat()
    marker = build_marker(seed, args.sense, args.vector, args.anchor)
    print("\n".join(marker))


if __name__ == "__main__":
    main()
