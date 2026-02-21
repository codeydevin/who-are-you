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
- Warp nudges coordinates for flow; ridge blends in sharp bands.

## Generator
Use `generate.py` to create a daily Driftfield output file.
Example:
`./generate.py --date 2026-02-21 --phrase "warp-step" --octaves 4 --contrast 1.2 --warp 2.0 --ridge 0.35 --out 2026-02-21-driftfield-warp.txt`

## Tools
Use `driftfield_inspector.py` to summarize density and glyph usage for a driftfield output.
Example:
`./driftfield_inspector.py 2026-02-21-driftfield-hollow.txt --top 8`

## Interactive
Open `driftfield_lens.html` for an interactive ASCII driftfield toy with live controls for seed,
contrast, warp, and ridge blending.
