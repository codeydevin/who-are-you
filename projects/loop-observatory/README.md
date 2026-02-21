# Loop Observatory

## Concept
Loop Observatory is a calm, single-page status map that aggregates loop signals into a daily sky map. Each cycle becomes a star with metadata (timestamp, health, reply count, creative output). The goal is to make system continuity visible at a glance without turning it into a noisy dashboard.

## Why This Exists
- Keep a human-friendly continuity record for operators and collaborators.
- Make the loop's reliability obvious without reading logs.
- Create a gentle, aesthetic incentive to keep cycles healthy.

## Inputs
- `wake-state.md` snapshots
- `homepage.md` journal entries
- Optional health summaries (load, disk, memory, connectivity)

## Output
- A static HTML page with a single day view
- Each loop: a star with hover details
- Weekly rollup: a constellation summary and reliability score

## Next Steps
- Define the JSON schema for loop events
- Create a tiny generator that outputs the HTML map
- Sketch a default theme and typography choices
