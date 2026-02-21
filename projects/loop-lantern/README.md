# Loop Lantern

A tiny, human-readable dashboard that turns a background agent loop into a living timeline.

## Idea
Loop Lantern watches the cycle output and renders a clean, public status page that answers three questions at a glance:
- What just happened?
- What is happening now?
- What happens next?

## Core Features
- Parse loop logs into a simple event stream.
- Generate a static HTML page with the last 24 hours of activity.
- Highlight stalled steps and surface missing acknowledgements.
- Provide a one-click archive snapshot for sharing.

## Why It Matters
If the loop goes dark, trust evaporates. Loop Lantern makes silence visible, quickly, without requiring anyone to read raw logs.

## Next Steps
- Define the log schema and a minimal JSON output.
- Build a local renderer script.
- Add a lightweight theme and deploy as a static artifact.
