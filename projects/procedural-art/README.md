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

Use `driftfield_sampler.py` to batch-generate several named variants from the recipe set.
Example:
`./driftfield_sampler.py --date 2026-02-21 --out-dir .`

Use `driftfield_delta.py` to compare two driftfield seeds and render a delta map of how they diverge.
Example:
`./driftfield_delta.py --date-a 2026-02-21 --phrase-a "warp-step" --date-b 2026-02-21 --phrase-b "tide-memory" --warp 1.4 --ridge 0.25 --out 2026-02-21-driftfield-delta.txt`

Use `driftfield_compass.py` to generate a 3x3 compass mosaic of driftfield tiles.
Example:
`./driftfield_compass.py --date 2026-02-21 --phrase "driftfield-compass" --out 2026-02-21-driftfield-compass.txt`

Use `driftfield_route.py` to generate a sequential route (stacked tiles) that drifts parameters
step by step.
Example:
`./driftfield_route.py --date 2026-02-21 --phrase "route-harbor" --steps 5 --out 2026-02-21-driftfield-route.txt`

Use `driftfield_crossfade.py` to blend two seeds across an axis to create transition panels.
Example:
`./driftfield_crossfade.py --date 2026-02-21 --phrase-a "relay-silt" --phrase-b "torchline" --axis x --curve ease --out 2026-02-21-driftfield-crossfade.txt`

Use `driftfield_echo.py` to layer a shifted echo seed on top of a base driftfield.
Example:
`./driftfield_echo.py --date 2026-02-21 --phrase "echo-braid" --echo-phrase "ember-skein" --echo-x 4 --echo-y 2 --echo-strength 0.45 --out 2026-02-21-driftfield-echo.txt`

Use `driftfield_stitch.py` to weave multiple tiles into a stitched panel.
Example:
`./driftfield_stitch.py --date 2026-02-21 --phrases "stitchline,tidal-rift,ember-loom,glass-weir" --tiles-x 2 --tiles-y 2 --tile-rows 10 --tile-cols 30 --out 2026-02-21-driftfield-stitch.txt`

Use `driftfield_orbit.py` to generate an orbital driftfield with radial rings and angular spin.
Example:
`./driftfield_orbit.py --date 2026-02-21 --phrase "orbit-floe" --rings 5.7 --spin 2.2 --ripples 3.9 --out 2026-02-21-driftfield-orbit.txt`

Use `driftfield_ripple.py` to generate a ripple-interference driftfield with multiple centers.
Example:
`./driftfield_ripple.py --date 2026-02-21 --phrase "ripple-cairn" --centers "0.3,0.4;0.7,0.6" --out 2026-02-21-driftfield-ripple.txt`

Use `driftfield_beacon.py` to generate a beacon-style driftfield with angular beams and pulsing rings.
Example:
`./driftfield_beacon.py --date 2026-02-21 --phrase "beacon-scan" --beams 11.2 --pulse 2.8 --drift 3.4 --out 2026-02-21-driftfield-beacon.txt`

Use `driftfield_swell.py` to generate a swell-style driftfield built from wave vectors and eddies.
Example:
`./driftfield_swell.py --date 2026-02-21 --phrase "swell-harbor" --wave-x 2.4 --wave-y 1.6 --phase 0.22 --noise 0.32 --eddy 1.1 --contrast 1.1 --out 2026-02-21-driftfield-swell.txt`

## Latticefield
Use `latticefield.py` to generate a lattice-weighted ASCII texture with grid accents.
Example:
`./latticefield.py --date 2026-02-21 --phrase "lattice-tide" --rows 20 --cols 60 --out 2026-02-21-latticefield.txt`

## Interactive
Open `driftfield_lens.html` for an interactive ASCII driftfield toy with live controls for seed,
contrast, warp, and ridge blending.

Open `driftfield_atlas.html` for an atlas-style driftfield generator with glyph usage telemetry
and a tide phase control.

Open `aster-loom.html` for a canvas-based orbital weaving study with palette, wobble, and spin
controls.

Open `moire-weave.html` for layered moire wavefields with seeded SVG line stacks.

Open `driftfield_prism.html` for a prism-themed ASCII driftfield lab with seed, warp,
bloom, and contrast controls.

Open `driftfield_rift.html` for a rift-themed ASCII field with shear, focus, and warp controls.

Open `driftfield_mosaic.html` for a tiled mosaic builder that weaves multiple ASCII fields into
one exportable map.

Open `2026-02-21-copper-loom.html` for an interactive warp/weft canvas with pointer pull,
thread density, and glow controls.

Open `2026-02-21-gyre-chorus.html` for a flow-field particle chorus that responds to
pointer pulls and adjustable spin/drag/glow controls.
