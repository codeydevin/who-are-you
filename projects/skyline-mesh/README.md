# Skyline Mesh

A small repo idea: capture a daily “cityline” from ambient signals (weather, energy use, transit delay, or personal mood), then render it as a simple text skyline. The output becomes a diary of shape rather than words.

## Why It’s Interesting
- Tiny inputs, rich pattern language.
- Text-only render works anywhere.
- Easy to automate as a daily cron.

## MVP
- Choose 3 to 5 public signals.
- Map them to building heights and gaps.
- Emit a 40-character skyline line per day.
- Append to a log file with the date.

## Possible Next Steps
- Add a “fog” layer from variance.
- Export a weekly block as a mini-poster.
- Offer custom signal packs.
