# In-domain hashtok mixer-width ablation (`--n-hashes`)

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files, last-4. Occupancy-free `hashtok` while varying the
number of random mixer hashes. Same mixer as
[../2026-09-01-probe-12x4-hashtok/](../2026-09-01-probe-12x4-hashtok/)
(CLI default **n=8**). Not `hashtok2` (`min_count=2`). Still no keys.

This directory is **n=2**. Sibling runs: n=4, n=16, n=32.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 2 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-nhashes2
```

| n_hashes | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem | precision |
|---|---|---|---|---|---|---|
| **2** (this dir) | **11/12** | **0.764** | 34/48 | **31/48** | **28/48 vs 37/48** | 0.667 |
| 4 | **11/12** | 0.733 | **36/48** | 30/48 | **35/48 vs 30/48** | 0.667 |
| 8 (default) | 9/12 | 0.664 | 33/48 | 22/48 | 22/48 vs 30/48 | 0.559 |
| 16 | **11/12** | 0.662 | **36/48** | 22/48 | 29/48 vs 24/48 | 0.581 |
| 32 | 10/12 | 0.622 | 30/48 | 26/48 | 21/48 vs 38/48 | 0.577 |

Default n=8 is **not** the best width on this in-domain gate. n=2 has
the best file AUC and the best nested spec among the dense widths.
n=4 is the densest t=0 / nested recall (mean nested t ≈ 0, so nested
**35/48 vs 30/48** is almost t=0). Wider mixers dilute the mean gap:
n=16 nested spec is **24/48**; n=32 nested recall drops to **21/48**.

n=2 versus default n=8: gained station d4, letter d3, garden d1,
ferry-queue d4; lost station d2, office d4, garden d2. Unmarked false
positives drop from 26 to 17. Prompt miss: library only (n=8 missed
market, station, office). Letter d2 stays negative at n=2/4/8/32.
n=16 is the only width here with letter d2 `lr>0`; the letter *prompt*
still loses. Do not sell that as reading the official 5-gram.

None of these widths is hits nested **22/48 vs 39/48**, poshits
**39/48**, or hard last-4 **29/48**. Combined t=0 at n=2 is **65/96**,
not a calibrated isolated-file detector. The 24→12 transfer gate
keeps the CLI default at 8. Do **not** sell 36/48, 35/48, or 34/48 as
replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
