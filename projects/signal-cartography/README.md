# Signal Cartography

Signal Cartography maps small, recurring signals into simple coordinates.
Each entry is a three-line marker:
- Sense: what is observable right now
- Vector: where the energy is moving
- Anchor: the thing to return to when drift begins

Goal: one marker per day, clipped and legible, so future me can find the path back.

## Tooling
Use `cartography_tool.py` to generate a marker from a seed (defaults to today).

```bash
./cartography_tool.py
./cartography_tool.py --seed 2026-02-21
./cartography_tool.py --sense "fan hum" --vector "steadying" --anchor "window light"
```

Use `cartography_digest.py` to summarize recent markers and count vectors.

```bash
./cartography_digest.py --path . --limit 10
```

Use `cartography_brief.py` to generate a compact handoff brief for the latest markers.

```bash
./cartography_brief.py --limit 5
```

Use `cartography_compass.py` to build a four-point compass from the latest markers.

```bash
./cartography_compass.py --date 2026-02-21 --out 2026-02-21-compass.md
```
