# In-domain 12×4 full-file occupancy-free hashing

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full 128-token
files, last-4. Unbucketed hashpool (`instance=key-free-hashpool`); the
CLI `pos_bucket=16` default applies to poshits, not this mixer. Still
no keys. Occupancy-free `hashtok` / `hashtoklen` on the same twins.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashpool,hashtok,hashtoklen,hits,postokhits \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| hits | 11/12 | 0.737 | 28/48 | 30/48 | **22/48 vs 39/48** |
| hashpool | 11/12 | 0.716 | **35/48** | **29/48** | 23/48 vs 36/48 |
| postokhits | 12/12 | 0.763 | 24/48 | 45/48 | 22/48 vs 45/48 |
| **hashtok** | 9/12 | 0.664 | **33/48** | **22/48** | **22/48 vs 30/48** |
| hashtoklen | 8/12 | 0.592 | 33/48 | 23/48 | 30/48 vs 20/48 |

Hashpool matches the published in-domain 35/48. Occupancy-free hashing
is denser at t=0 than the headline hard last-4 **29/48**, but it spends
26 unmarked FPs. Nested-by-stem spec is worse than hits.

Occupancy and occupancy-free disagree on six files: hashpool-only
night-bus d3, library d2, market d1, ferry-queue d4; hashtok-only
night-bus d4, market d3. Letter d2 stays negative on hashpool, hashtok,
and the original indicate. Do **not** sell 33/48 or 35/48 as replacing
**29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
