# Skyline Mesh

A small repo idea: capture a daily “cityline” from ambient signals (weather, energy use, transit delay, or personal mood), then render it as a simple text skyline. The output becomes a diary of shape rather than words.

## Why It’s Interesting
- Tiny inputs, rich pattern language.
- Text-only render works anywhere.
- Easy to automate as a daily cron.

## MVP
- Choose 3 to 5 public signals.
- Map them to building heights and gaps.
- Emit a 40-character skyline line per day.
- Append to a log file with the date.

## Tooling
Use `skyline_mesh.py` to turn a handful of numeric signals into a repeatable line.

```bash
./skyline_mesh.py 0.43 0.13 0.04 23.3 1 --with-date
./skyline_mesh.py 2,4,6,3 --length 50 --seed "week-08"
```

## Interactive
Open `skyline_mesh_console.html` to explore signals, density, and length with live updates.

## Possible Next Steps
- Add a “fog” layer from variance.
- Export a weekly block as a mini-poster.
- Offer custom signal packs.
