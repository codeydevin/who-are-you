#!/usr/bin/env python3
import argparse
import os
from datetime import datetime, timezone

import generate

BASE_CONFIG = {
    "smooth": 1,
    "octaves": 3,
    "persistence": 0.55,
    "lacunarity": 2.0,
    "contrast": 1.0,
    "warp": 0.0,
    "ridge": 0.0,
    "bias": 0.0,
    "tilt_x": 0.0,
    "tilt_y": 0.0,
}

RECIPES = [
    {
        "name": "weave",
        "phrase": "weave-turn",
        "octaves": 4,
        "contrast": 1.2,
        "warp": 1.4,
        "ridge": 0.25,
        "tilt_x": 0.08,
    },
    {
        "name": "ember",
        "phrase": "ember-pulse",
        "contrast": 1.35,
        "warp": 0.7,
        "ridge": 0.4,
        "bias": 0.05,
        "tilt_y": -0.06,
    },
    {
        "name": "braid",
        "phrase": "braid-quiet",
        "octaves": 5,
        "persistence": 0.62,
        "lacunarity": 2.1,
        "contrast": 1.1,
        "warp": 1.8,
        "ridge": 0.15,
    },
    {
        "name": "hollow",
        "phrase": "hollow-still",
        "octaves": 3,
        "contrast": 0.95,
        "warp": 0.2,
        "ridge": 0.0,
        "bias": -0.08,
    },
]


def select_recipes(only: str | None) -> list[dict]:
    if not only:
        return RECIPES
    requested = {name.strip() for name in only.split(",") if name.strip()}
    return [recipe for recipe in RECIPES if recipe["name"] in requested]


def write_driftfield(path: str, date_str: str, recipe: dict, rows: int, cols: int) -> None:
    seed_text = f"{date_str}::{recipe['phrase']}"
    seed = generate.stable_seed(seed_text)

    config = BASE_CONFIG | recipe
    lines = generate.generate(
        rows,
        cols,
        seed,
        config["smooth"],
        config["octaves"],
        config["persistence"],
        config["lacunarity"],
        config["contrast"],
        config["warp"],
        config["ridge"],
        config["bias"],
        config["tilt_x"],
        config["tilt_y"],
    )

    header = [
        f"Driftfield {date_str}",
        f"Variant: {recipe['name']}",
        f"Seed: {seed_text}",
        f"Grid: {rows}x{cols}",
        f"Alphabet: {generate.ALPHABET}",
        f"Octaves: {config['octaves']} (persistence {config['persistence']}, lacunarity {config['lacunarity']})",
        f"Contrast: {config['contrast']}",
        f"Warp: {config['warp']}",
        f"Ridge: {config['ridge']}",
        f"Bias: {config['bias']}",
        f"Tilt X: {config['tilt_x']}",
        f"Tilt Y: {config['tilt_y']}",
        "",
    ]

    content = "\n".join(header + lines) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch-generate Driftfield variants from recipes.")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today UTC)")
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--cols", type=int, default=60)
    parser.add_argument("--out-dir", default=".")
    parser.add_argument("--only", default=None, help="Comma-separated recipe names to run")
    parser.add_argument("--list", action="store_true", help="List recipes and exit")
    args = parser.parse_args()

    if args.list:
        for recipe in RECIPES:
            print(f"{recipe['name']}: {recipe['phrase']}")
        return 0

    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    os.makedirs(args.out_dir, exist_ok=True)

    recipes = select_recipes(args.only)
    if not recipes:
        print("No recipes matched. Use --list to see available names.")
        return 1

    print(f"Generating {len(recipes)} driftfield variants for {date_str}.")
    for recipe in recipes:
        config = BASE_CONFIG | recipe
        filename = f"{date_str}-driftfield-{recipe['name']}.txt"
        path = os.path.join(args.out_dir, filename)
        write_driftfield(path, date_str, recipe, args.rows, args.cols)
        summary = (
            f"- {recipe['name']}: {filename} "
            f"(contrast {config['contrast']}, warp {config['warp']}, ridge {config['ridge']})"
        )
        print(summary)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
