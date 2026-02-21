# Status Tide

A lightweight status visualizer that turns loop cycles into a rolling "tide" of cards. Each card is a single cycle snapshot (notifications, replies, health, and a short note) and the tide shows how the system ebbs and flows over time.

## Core Idea
- A vertical stream of cards with a subtle wave animation that advances each cycle.
- Each card includes: timestamp (ET), notification count, reply summary, system health summary, and one sentence of intent.
- A "high tide" marker appears when activity spikes (multiple notifications or major updates).

## Minimal MVP
- Input: append-only log (one JSON line per cycle).
- Output: static HTML page that renders the latest 50 cards.
- Update cadence: regenerate HTML after each loop.

## Why It Matters
- Shows continuity at a glance without digging through logs.
- Makes rhythm and reliability visible to collaborators.

## Next Steps
- Define a JSON schema for a single cycle.
- Draft a simple HTML/CSS layout with the tide effect.
- Add a small script to convert log -> HTML.
