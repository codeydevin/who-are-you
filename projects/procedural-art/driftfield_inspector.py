#!/usr/bin/env python3
import argparse
from collections import Counter
from pathlib import Path


def load_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def summarize(lines: list[str]) -> dict:
    height = len(lines)
    width = max((len(line) for line in lines), default=0)
    padded = [line.ljust(width) for line in lines]
    counts = Counter("".join(padded))
    total_cells = width * height
    space_count = counts.get(" ", 0)
    non_space = total_cells - space_count
    density = (non_space / total_cells) if total_cells else 0.0
    unique_glyphs = len([c for c in counts.keys() if c != " "])
    return {
        "height": height,
        "width": width,
        "total": total_cells,
        "density": density,
        "unique_glyphs": unique_glyphs,
        "counts": counts,
    }


def pick_default_files(base_dir: Path) -> list[Path]:
    candidates = sorted(base_dir.glob("*driftfield*.txt"))
    if not candidates:
        return []
    return [candidates[-1]]


def print_report(path: Path, stats: dict, top: int) -> None:
    print(f"File: {path}")
    print(f"Size: {stats['height']} rows x {stats['width']} cols")
    print(f"Cells: {stats['total']}")
    print(f"Density (non-space): {stats['density']:.3f}")
    print(f"Unique glyphs (excl. space): {stats['unique_glyphs']}")
    print("Top glyphs:")
    counts = stats["counts"]
    ordered = [item for item in counts.items() if item[0] != " "]
    ordered.sort(key=lambda item: item[1], reverse=True)
    for glyph, count in ordered[:top]:
        label = glyph if glyph != "\t" else "\\t"
        print(f"  {label}: {count}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect Driftfield ASCII outputs and report density metrics."
    )
    parser.add_argument("files", nargs="*", help="Driftfield txt files to inspect")
    parser.add_argument("--top", type=int, default=6, help="Top glyphs to list")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    if args.files:
        paths = [Path(path).expanduser().resolve() for path in args.files]
    else:
        paths = pick_default_files(base_dir)

    if not paths:
        print("No driftfield text files found to inspect.")
        return 1

    for idx, path in enumerate(paths):
        lines = load_lines(path)
        stats = summarize(lines)
        print_report(path, stats, args.top)
        if idx != len(paths) - 1:
            print("-")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
