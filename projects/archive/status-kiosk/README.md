# Status Kiosk

Status Kiosk is a small, static dashboard that rotates through the last 24 hours of loop signals like a kiosk screen. It favors clarity and rhythm over deep analytics.

## Concept
- Generate a single HTML page from a tiny JSON file.
- Show a rotating set of cards: notifications, replies, system health, and creative bets.
- Make it safe to host on GitHub Pages with no backend.

## Inputs
- GitHub notifications summary.
- Recent replies or status comments.
- Health snapshot (load, disk, memory, connectivity).
- One creative action taken during the cycle.

## Output
- Static HTML + CSS.
- Optional SVG timeline strip.
- Small JSON feed for reuse.

## Next Steps
- Draft a JSON schema and sample payload.
- Sketch a minimal HTML layout with a rotating card animation.
- Add a CLI script that reads wake-state.md and emits the JSON.
