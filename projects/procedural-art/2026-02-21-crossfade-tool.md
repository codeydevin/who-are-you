# Driftfield Crossfade Tool

A small utility for blending two driftfield seeds across a single axis. The blend can be
linear or eased, which makes it useful for creating transition panels and route banners.

## Usage
`./driftfield_crossfade.py --date 2026-02-21 --phrase-a "relay-silt" --phrase-b "torchline" --rows 8 --cols 40 --axis x --curve ease --out 2026-02-21-driftfield-crossfade.txt`

## Sample (8x40)
```
Driftfield Crossfade 2026-02-21
Seed A: 2026-02-21::relay-silt
Seed B: 2026-02-21::torchline
Grid: 8x40
Blend axis: x
Blend curve: ease
Alphabet: .,:;~^*+=?%$#@
Octaves: 3 (persistence 0.55, lacunarity 2.0)
Contrast: 1.1
Warp: 0.5
Ridge: 0.15
Bias: 0.0
Tilt X: 0.0
Tilt Y: 0.0

*^^*+*+++*+*+*++++*+++***+***+++++++**++
*^^*+*+++*+*++++++*+*+***+++++++++***+++
*^*+++++++++++++***+++++++++++++*+**^*^^
***+*^^*+++++++*++++++++++++++**^*^****^
+++++^^*++++++**+++++++++++++**^^*++**^^
*++*^^^+*+++*^^*+++++++++++**^^^**++**^^
*+**^**+*+**^^++++++***++++*^~*++++***^~
***^~***^+*^~~*+==++++*+=++*^~^+++^^^^~;
```
