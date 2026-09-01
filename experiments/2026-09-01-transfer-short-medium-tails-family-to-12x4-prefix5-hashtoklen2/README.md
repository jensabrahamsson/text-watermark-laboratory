# 60-stem prefix-5 occupancy-free min_count=2 → 12×4

Same train as prefix-5 `hashtoklen`. `hashtoklen2` / `hashskip2` reuse
those exact-length and drop-one tables, but a hash votes only when
`c_m + c_u ≥ 2`. Singleton collisions are skipped at **score time**.
Not a new mixer. Still no keys. Instance `key-free-hashtoklen2` /
`key-free-hashskip2`.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --extra-train experiments/2026-08-31-pair-family12x4 \
  --fit-prefix 5 --pos-bucket 0 \
  --methods hashtoklen,hashtoklen2,hashskip,hashskip2 \
  --out-dir experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashtoklen | 12/12† | 0.701 | **21/48** | 45/48 | **21/48 vs 45/48** | 0.875 |
| **hashtoklen2** | 12/12† | 0.604 | **10/48** | **48/48** | **10/48 vs 48/48** | **1.000** |
| hashskip | 8/12 | 0.663 | **25/48** | 35/48 | **16/48 vs 41/48** | 0.658 |
| **hashskip2** | 8/12 | 0.641 | **22/48** | 39/48 | **15/48 vs 41/48** | 0.710 |

† Ranking of marked zeros plus decided files. Not isolated-file density.

**11 of 21** hashtoklen TPs are singleton hash collisions
(`c_m + c_u == 1`). min_count=2 is the robust occupancy-free 5-gram
core: precision 1.0, 0 unmarked FPs, nested Youden matching t=0.

Harbour d2 `The ferry was over ,` **survives** (same lr=+0.618): the
colliding hash has c_m=11. Letter d2 still abstains. Lost at min=2:
night-bus d3, market ×4, kitchen d2, station d1/d3, rain d2, garden
d1/d4. Leftover eight stay zeros.

hashskip2 kills letter d2's unmarked singleton votes (lr=0, not
−0.847) but still has 9 unmarked FPs. t=0 extras versus hashtoklen
remain harbour d3/d4, night-bus d2/d4, workshop d4. Nested leftover
fill-in **0/8**. Coverage-then-hashskip on saved holdouts is worse
than hashtoklen alone (26/48 vs 35/48; combined 61/96 vs 66/96). Do
not add hashskip as a cascade fallback.

Do **not** sell 10/48, 22/48, or 15/48 as beating poshits **39/48**
or replacing **29/48**. Persist the same mixers as `tables-hashtoklen/`
and `tables-hashskip/`. Score with `--score-mode hashtoklen2` or
`hashskip2`.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
