# Loop Tools

Small, sturdy utilities that keep the loop legible.

## Token Count Log
`token_count_log.py` appends a CSV row with estimated token counts, plus bytes and lines, for the files you care about.

Usage:

```bash
python token_count_log.py --out token-count.csv homepage.md wake-state.md
```

Defaults:
- If you pass no paths, it logs `homepage.md` and `wake-state.md`.
- If the output CSV does not exist, it writes a header row first.

CSV columns:
`timestamp_utc`, `method`, `total_tokens`, `total_bytes`, `total_lines`, `file_count`, `files`

Token estimate:
- `chars4` (default): tokens ≈ ceil(characters / 4)
- `whitespace`: tokens ≈ number of whitespace-delimited words
