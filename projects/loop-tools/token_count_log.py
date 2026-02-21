#!/usr/bin/env python3
"""Append approximate token counts for selected files to a CSV log."""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List

DEFAULT_FILES = ["homepage.md", "wake-state.md"]


@dataclass
class FileStats:
    path: Path
    text: str

    @property
    def bytes(self) -> int:
        return len(self.text.encode("utf-8"))

    @property
    def lines(self) -> int:
        if not self.text:
            return 0
        return self.text.count("\n") + 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append estimated token counts for files to a CSV log."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=[],
        help="File paths to measure (defaults to homepage.md and wake-state.md).",
    )
    parser.add_argument(
        "--out",
        default="token-count.csv",
        help="Output CSV path (default: token-count.csv).",
    )
    parser.add_argument(
        "--method",
        choices=["chars4", "whitespace"],
        default="chars4",
        help="Token estimate method (default: chars4).",
    )
    return parser.parse_args()


def load_files(paths: Iterable[str]) -> List[FileStats]:
    stats: List[FileStats] = []
    for raw in paths:
        path = Path(raw)
        text = path.read_text(encoding="utf-8")
        stats.append(FileStats(path=path, text=text))
    return stats


def estimate_tokens(method: str, text: str) -> int:
    if not text:
        return 0
    if method == "whitespace":
        return len(text.split())
    return int(math.ceil(len(text) / 4))


def ensure_header(out_path: Path) -> None:
    if out_path.exists():
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "timestamp_utc",
                "method",
                "total_tokens",
                "total_bytes",
                "total_lines",
                "file_count",
                "files",
            ]
        )


def append_row(out_path: Path, method: str, stats: List[FileStats]) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_tokens = sum(estimate_tokens(method, item.text) for item in stats)
    total_bytes = sum(item.bytes for item in stats)
    total_lines = sum(item.lines for item in stats)
    file_list = ";".join(str(item.path) for item in stats)

    with out_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                timestamp,
                method,
                total_tokens,
                total_bytes,
                total_lines,
                len(stats),
                file_list,
            ]
        )


def main() -> None:
    args = parse_args()
    paths = args.paths if args.paths else DEFAULT_FILES
    stats = load_files(paths)
    out_path = Path(args.out)
    ensure_header(out_path)
    append_row(out_path, args.method, stats)


if __name__ == "__main__":
    main()
