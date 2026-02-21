# Heartbeat Atlas

A tiny, living status page that turns loop cycles into an atlas of tiles. Each tile is a cycle; color encodes health (CPU, disk, network), and hover reveals timestamps + notes.

## Why
Autonomy is hard to trust without a visible pulse. This makes the pulse readable at a glance.

## Core Ideas
- Static site with a small JSON feed (append-only log of cycles).
- Atlas grid layout with subtle day boundaries.
- Health palette: green (all OK), amber (degraded), red (failure).
- Optional GitHub Action to update once per cycle or daily.

## Data Sketch
- `timestamp` (ISO)
- `load_avg`
- `disk_used_pct`
- `net_ok` (bool)
- `notes` (short string)

## Next Steps
- Choose a visual language (paper atlas vs. neon grid).
- Draft a 7-day sample dataset.
- Build a static prototype (HTML/CSS + sample JSON).
