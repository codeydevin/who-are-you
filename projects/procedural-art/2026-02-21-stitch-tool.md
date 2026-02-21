# Driftfield Stitch Tool

A small utility for weaving multiple driftfield tiles into a stitched panel. It generates
several deterministic tiles and joins them with seam markers so you can compare how different
seed phrases behave side-by-side.

## Intent
- Provide a quick grid view of multiple seeds without manual merging.
- Keep results reproducible from date + phrase + tile index.
- Make a printable, single-file ASCII panel.

## Usage
```bash
./driftfield_stitch.py --date 2026-02-21 --phrases "stitchline,tidal-rift,ember-loom,glass-weir" \
  --tiles-x 2 --tiles-y 2 --tile-rows 10 --tile-cols 30 --warp 1.1 --ridge 0.25 \
  --out 2026-02-21-driftfield-stitch.txt
```

## Notes
- Seam markers use `|` and `-` with `+` intersections.
- If you omit `--tiles-x` and `--tiles-y`, the tool infers a reasonable grid from phrase count.
- Use `--no-seam` for a single continuous texture.
