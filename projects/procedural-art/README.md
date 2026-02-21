# Procedural Art: Driftfield

A small, non-status-monitoring creative thread. Goal: generate a simple daily ASCII drift field
from a deterministic seed (date + short phrase) and log a 20x60 glyph map. Each run should
produce a different texture but stay reproducible from the seed.

## First Experiment
- Grid: 20 rows x 60 columns
- Alphabet: .,:;~^*+=?%$#@ (low to high density)
- Field: value(x, y) = fract(sin(dot([x, y], [12.9898, 78.233])) * 43758.5453 + seed)
- Mapping: scale value to alphabet index

## Notes
- Keep outputs in plain text. No images required.
- If it looks too noisy, increase smoothing or reduce octaves.
- Contrast lets you push density toward heavier or lighter glyphs.

## Generator
Use `generate.py` to create a daily Driftfield output file.
Example:
`./generate.py --date 2026-02-21 --phrase "third voice" --octaves 4 --contrast 1.2 --out 2026-02-21-driftfield-2.txt`
