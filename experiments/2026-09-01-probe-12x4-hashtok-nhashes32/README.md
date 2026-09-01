# In-domain hashtok `--n-hashes 32`

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files, last-4. Occupancy-free `hashtok` with 32 mixer
hashes. Comparison table:
[../2026-09-01-probe-12x4-hashtok-nhashes2/](../2026-09-01-probe-12x4-hashtok-nhashes2/).

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 32 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-nhashes32
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| **hashtok n=32** | 10/12 | 0.622 | 30/48 | 26/48 | **21/48 vs 38/48** |

Widening past the default **hurts** this in-domain gate: file AUC
**0.622** is the lowest in the sweep; t=0 marked **30/48** is below
default n=8 **33/48**; nested recall **21/48** is below n=8 **22/48**.
Nested spec **38/48** is close to hits **39/48** only because recall
collapsed. Prompt misses: letter, ferry-queue. Letter d2 stays
negative. Do **not** sell 30/48, 21/48, or nested spec 38/48 as
replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
