# Loop Orchard

Loop Orchard is a lightweight orchard of status “seeds” that grow into daily artifacts.
Each seed is a small, structured note derived from the loop (notifications, health checks,
creative moves). The goal is to let progress accumulate like rings in a tree: tiny, durable,
and easy to inspect.

## Concept
- Inputs: GitHub notifications, health metrics, short status note
- Output: one Markdown seed per cycle, aggregated into a weekly orchard page
- Promise: a quiet, reliable record that makes drift visible early

## First Slice
- Create `seeds/YYYY-MM-DD/HHMM.md` with a tiny front matter block
- Build `orchard.md` that indexes recent seeds and links back to `homepage.md`
- Keep it pure Markdown, no dependencies

## Notes
This is intentionally small. If it helps, it can evolve into a real repo with a minimal CLI.
