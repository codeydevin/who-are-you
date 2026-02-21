# Driftfield Quilt Tool

A utility for stitching multiple Driftfield tiles into a single quilt. Each tile is
seeded independently (by tile coordinates), and optional bias/warp steps let you
push the grid from calm to turbulent across the quilt.

## Usage
`./driftfield_quilt.py --date 2026-02-21 --phrase "quilt-loom" --tiles-y 3 --tiles-x 4 --tile-rows 6 --tile-cols 12 --warp 0.15 --warp-step 0.03 --bias-step 0.02 --ridge 0.2 --flip x --out 2026-02-21-driftfield-quilt.txt`

## Sample (18x48)
```
Driftfield Quilt 2026-02-21
Seed: 2026-02-21::quilt-loom::tile-{y}-{x}
Grid: 18x48 | Tile: 6x12
Tiles: 3x4 | Flip: x
Alphabet: .,:;~^*+=?%$#@
Octaves: 3 (persistence 0.55, lacunarity 2.0)
Contrast: 1.0
Warp: 0.15 (step 0.03)
Ridge: 0.2
Bias: 0.0 (step 0.02)
Tilt X: 0.0
Tilt Y: 0.0

*+^+***+==========+===+*+=====?====+=+=*++=+*+==
+++=++*+=+====+===+===+*+++=+========+=++==++===
*++=++*+++++==+====+++++++*+======++=+==+===++==
*+===++++++==+*===+++===++^++=+===+++======?====
**+++=++*++==++====+*+====++==+++==========??=++
~*+++==+*+========++*=+===++==+++=====+==????=+*
```
