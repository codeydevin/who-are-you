#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from typing import List

from generate import ALPHABET, generate, stable_seed


def build_seed(date_str: str, phrase: str) -> float:
    return stable_seed(f"{date_str}::{phrase}")


def parse_phrases(base: str, steps: int, phrases: List[str]) -> List[str]:
    if phrases:
        return phrases
    return [f"{base}-{idx + 1}" for idx in range(steps)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a sequential driftfield route (stacked tiles)."
    )
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--phrase", default="route-harbor", help="Base seed phrase")
    parser.add_argument(
        "--phrase-step",
        action="append",
        default=[],
        help="Explicit step phrase (repeat to add multiple)",
    )
    parser.add_argument("--steps", type=int, default=5, help="Number of steps")
    parser.add_argument("--rows", type=int, default=12)
    parser.add_argument("--cols", type=int, default=28)
    parser.add_argument("--octaves", type=int, default=3)
    parser.add_argument("--contrast", type=float, default=1.1)
    parser.add_argument("--warp", type=float, default=0.6)
    parser.add_argument("--ridge", type=float, default=0.15)
    parser.add_argument("--warp-step", type=float, default=0.2)
    parser.add_argument("--ridge-step", type=float, default=0.07)
    parser.add_argument("--out", default=None, help="Output file path")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    phrases = parse_phrases(args.phrase, args.steps, args.phrase_step)
    steps = min(args.steps, len(phrases))

    header = [
        f"Driftfield Route {date_str}",
        f"Base phrase: {args.phrase}",
        f"Steps: {steps}",
        f"Tile: {args.rows}x{args.cols}",
        f"Alphabet: {ALPHABET}",
        f"Octaves: {args.octaves}",
        f"Contrast: {args.contrast}",
        f"Warp start: {args.warp} (step +{args.warp_step})",
        f"Ridge start: {args.ridge} (step +{args.ridge_step})",
        "",
    ]

    sections: List[str] = []
    for idx in range(steps):
        phrase = phrases[idx]
        warp = args.warp + idx * args.warp_step
        ridge = args.ridge + idx * args.ridge_step
        seed = build_seed(date_str, phrase)
        lines = generate(
            args.rows,
            args.cols,
            seed,
            smooth_passes=1,
            octaves=args.octaves,
            persistence=0.55,
            lacunarity=2.0,
            contrast=args.contrast,
            warp=warp,
            ridge=ridge,
            bias=0.0,
            tilt_x=0.0,
            tilt_y=0.0,
        )
        sections.append(
            "\n".join(
                [
                    f"Step {idx + 1}: {phrase}",
                    f"Seed: {date_str}::{phrase}",
                    f"Warp: {warp}",
                    f"Ridge: {ridge}",
                    "",
                ]
                + lines
            )
        )

    content = "\n".join(header + ["\n\n".join(sections)]) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
