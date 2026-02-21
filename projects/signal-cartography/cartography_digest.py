#!/usr/bin/env python3
"""Signal Cartography digest utility.

Scans recent marker files and prints a compact digest plus vector counts.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Marker:
    filename: str
    sense: str
    vector: str
    anchor: str


def parse_marker(path: Path) -> Marker | None:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return None
    sense = ""
    vector = ""
    anchor = ""
    for line in text.splitlines():
        lower = line.lower().strip()
        if lower.startswith("sense:"):
            sense = line.split(":", 1)[1].strip()
        elif lower.startswith("vector:"):
            vector = line.split(":", 1)[1].strip()
        elif lower.startswith("anchor:"):
            anchor = line.split(":", 1)[1].strip()
    if not (sense or vector or anchor):
        return None
    return Marker(path.name, sense, vector, anchor)


def collect_markers(directory: Path) -> list[Marker]:
    markers: list[Marker] = []
    for path in sorted(directory.glob("20*.md")):
        if path.name.lower().startswith("readme"):
            continue
        marker = parse_marker(path)
        if marker:
            markers.append(marker)
    return markers


def build_digest(markers: list[Marker], limit: int | None) -> tuple[list[Marker], Counter[str]]:
    selection = markers[-limit:] if limit else markers
    counts = Counter(m.vector.lower() for m in selection if m.vector)
    return selection, counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize Signal Cartography markers.")
    parser.add_argument("--path", default=".", help="Directory containing marker files.")
    parser.add_argument("--limit", type=int, default=10, help="Number of latest markers to include.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    directory = Path(args.path).expanduser().resolve()
    markers = collect_markers(directory)
    if not markers:
        print("No markers found.")
        return
    selection, counts = build_digest(markers, args.limit)
    print(f"Signal Cartography Digest ({len(selection)} entries)")
    print("-" * 40)
    for marker in selection:
        sense = marker.sense or "(missing)"
        vector = marker.vector or "(missing)"
        anchor = marker.anchor or "(missing)"
        print(f"{marker.filename}: {sense} | {vector} | {anchor}")
    print("\nVector counts")
    print("-" * 40)
    for vector, count in counts.most_common():
        print(f"{vector}: {count}")


if __name__ == "__main__":
    main()
