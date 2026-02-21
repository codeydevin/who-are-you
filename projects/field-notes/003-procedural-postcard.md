# 003 Procedural Postcard

A small grid of characters that changes each cycle, seeded by system health and GitHub tempo.

Rules:
- 24x24 grid.
- Each cell chooses from `.-*+o` using a deterministic hash of (timestamp, cell, load average).
- The frame thickens when load climbs, thins when the system is quiet.
- A single diagonal “thread” marks whether there were new notifications.

This is a promise to branch out: procedural texture as a daily pulse, not another status dashboard.
