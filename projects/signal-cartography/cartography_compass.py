#!/usr/bin/env python3
"""Build a compass-style summary from recent Signal Cartography markers."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DIRECTIONS = ("North", "East", "South", "West")


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
        if "compass" in path.stem:
            continue
        marker = parse_marker(path)
        if marker:
            markers.append(marker)
    return markers


def select_markers(markers: list[Marker], limit: int) -> list[Marker]:
    if limit <= 0:
        return []
    return markers[-limit:]


def build_center(anchors: Iterable[str]) -> str:
    unique: list[str] = []
    for anchor in anchors:
        anchor = anchor.strip()
        if anchor and anchor not in unique:
            unique.append(anchor)
    if not unique:
        return "Hold the axis."
    if len(unique) == 1:
        return unique[0]
    if len(unique) == 2:
        return f"{unique[0]} / {unique[1]}"
    return "; ".join(unique)


def render_compass(markers: list[Marker], date_str: str) -> str:
    title = f"Signal Cartography Compass {date_str}"
    lines = [f"# {title}", "", "A four-point compass built from recent markers.", ""]
    for direction, marker in zip(DIRECTIONS, markers, strict=False):
        lines.append(f"## {direction}")
        lines.append(f"Sense: {marker.sense or '(missing)'}")
        lines.append(f"Vector: {marker.vector or '(missing)'}")
        lines.append(f"Anchor: {marker.anchor or '(missing)'}")
        lines.append("")
    center = build_center(marker.anchor for marker in markers)
    lines.append("## Center")
    lines.append(f"Return: {center}")
    lines.append("")
    lines.append("Sources: " + ", ".join(marker.filename for marker in markers))
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a compass-style summary from recent Signal Cartography markers."
    )
    parser.add_argument("--path", default=".", help="Directory containing marker files.")
    parser.add_argument("--date", required=True, help="Date string for the compass title.")
    parser.add_argument(
        "--limit",
        type=int,
        default=4,
        help="Number of latest markers to include (default 4).",
    )
    parser.add_argument("--out", help="Optional output file path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    directory = Path(args.path).expanduser().resolve()
    markers = collect_markers(directory)
    if len(markers) < 1:
        raise SystemExit("No markers found.")
    selection = select_markers(markers, min(args.limit, len(markers)))
    output = render_compass(selection, args.date)
    if args.out:
        out_path = Path(args.out)
        out_path.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
