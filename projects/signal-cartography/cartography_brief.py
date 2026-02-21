#!/usr/bin/env python3
"""Generate a compact brief from recent Signal Cartography entries."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

PREFIXES = ("Sense:", "Vector:", "Anchor:")


def parse_entry(path: Path) -> dict[str, str]:
    data = {"file": path.name, "Sense": "", "Vector": "", "Anchor": ""}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return data
    for line in lines:
        stripped = line.strip()
        for prefix in PREFIXES:
            if stripped.startswith(prefix):
                key = prefix[:-1]
                data[key] = stripped[len(prefix) :].strip()
    return data


def collect_entries(root: Path) -> list[dict[str, str]]:
    entries = []
    for path in sorted(root.glob("*.md")):
        if path.name.lower() in {"readme.md", "index.md"}:
            continue
        entries.append(parse_entry(path))
    return entries


def render_markdown(entries: list[dict[str, str]], limit: int) -> str:
    if not entries:
        return "# Signal Cartography Brief\n\nNo entries found."

    latest = entries[-1]
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    lines: list[str] = []
    lines.append("# Signal Cartography Brief")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append(f"Entries scanned: {len(entries)}")
    lines.append(f"Latest entry: {latest['file']}")
    lines.append("")
    lines.append("## Latest Marker")
    lines.append(f"- Sense: {latest['Sense'] or '—'}")
    lines.append(f"- Vector: {latest['Vector'] or '—'}")
    lines.append(f"- Anchor: {latest['Anchor'] or '—'}")
    lines.append("")
    lines.append("## Recent Trail")

    for entry in entries[-limit:]:
        summary = " | ".join(
            [
                entry.get("Sense", "").strip() or "—",
                entry.get("Vector", "").strip() or "—",
                entry.get("Anchor", "").strip() or "—",
            ]
        )
        lines.append(f"- {entry['file']}: {summary}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of recent entries to include in the trail.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory containing Signal Cartography entries.",
    )
    args = parser.parse_args()

    entries = collect_entries(args.root)
    print(render_markdown(entries, max(1, args.limit)))


if __name__ == "__main__":
    main()
