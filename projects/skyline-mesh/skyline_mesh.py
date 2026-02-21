#!/usr/bin/env python3
"""Generate a one-line skyline mesh from a handful of numeric signals."""

from __future__ import annotations

import argparse
import datetime as dt
import random
from typing import List


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def parse_signals(values: List[str]) -> List[float]:
    signals: List[float] = []
    for raw in values:
        if "," in raw:
            parts = [p.strip() for p in raw.split(",") if p.strip()]
        else:
            parts = [raw]
        for part in parts:
            signals.append(float(part))
    return signals


def density_from_signals(signals: List[float]) -> float:
    if not signals:
        return 0.35
    max_val = max(abs(s) for s in signals) or 1.0
    avg_val = sum(abs(s) for s in signals) / len(signals)
    return clamp(avg_val / max_val * 0.7 + 0.15, 0.1, 0.85)


def seed_from_signals(signals: List[float], seed: str | None) -> str:
    if seed:
        return seed
    if signals:
        return "-".join(f"{s:.4f}" for s in signals)
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")


def render_skyline(length: int, density: float, seed: str) -> str:
    rng = random.Random(seed)
    line = []
    for _ in range(length):
        line.append("|" if rng.random() < density else ".")
    return "".join(line)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("signals", nargs="*", help="Signal numbers (space or comma separated)")
    parser.add_argument("--length", type=int, default=40, help="Output length")
    parser.add_argument("--density", type=float, help="Override density 0-1")
    parser.add_argument("--seed", help="Seed string for repeatability")
    parser.add_argument("--with-date", action="store_true", help="Prefix with YYYY-MM-DD |")
    args = parser.parse_args()

    signals = parse_signals(args.signals)
    density = clamp(args.density, 0.05, 0.95) if args.density is not None else density_from_signals(signals)
    seed = seed_from_signals(signals, args.seed)

    line = render_skyline(args.length, density, seed)
    if args.with_date:
        date_str = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
        print(f"{date_str} | {line}")
    else:
        print(line)


if __name__ == "__main__":
    main()
