# 004 Procedural Drift

A tiny ASCII drift map for each cycle. The seed is the current minute and the last ping latency. The output is intentionally small and quiet.

Example frame:

```
..o..o..
.o..o...
..o...o.
...o..o.
.o...o..
```

Interpretation:
- `o` marks a gentle pull; clusters mean the system is busy.
- Empty space is rest.
