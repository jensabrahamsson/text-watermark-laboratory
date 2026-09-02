# Opening-grain occupancy-free hashing copies tokhits density

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Matched
`--fit-prefix 4` (first four generated tokens). Unbucketed last-4
(`position_bucket=16` on a 4-token clip is one bucket). Occupancy-free
hashed readers versus exact `hits` / `tokhits`. Still no keys.

Opening rankpath on these twins is **41/48**. This check asks whether
hashed token identity at the same grain is that dense, or whether it
stays as sparse as tokhits.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --methods hits,tokhits,hashtok,hashtok2 \
  --out-dir experiments/2026-09-01-probe-12x4-fitprefix4-hashtok
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem | precision |
|---|---|---|---|---|---|---|
| hits | 9/12 | 0.691 | 23/48 | 48/48 | 23/48 vs 48/48 | 1.000 |
| tokhits | **12/12** | 0.772 | 23/48 | 48/48 | 23/48 vs 48/48 | 1.000 |
| **hashtok** | **12/12** | 0.796 | **24/48** | 47/48 | 23/48 vs 47/48 | 0.960 |
| hashtok2 | **12/12** | 0.729 | 22/48 | 48/48 | 22/48 vs 48/48 | 1.000 |

tokhits has 25/48 marked zeros; decided 23/0 TP/FN. tokhits's 23 true
positives are a subset of hashtok. The one extra TP is **letter d3**.
hashtok's one unmarked false positive is kitchen d4. Nested Youden
throws letter d3 away (threshold ≈ 0.065). hashtok2 versus tokhits
gains letter d3 and loses kitchen d4 and rain d1.

Letter **d2 is zero** on hits, tokhits, hashtok, and hashtok2 at this
grain (not the full-file negative LR). Opening hashed readers copy
tokhits density, not opening rankpath **41/48**. Marked isolated
`lr>0` is **24/48**, below the hard last-4 headline **29/48**. Prompt
**12/12** and unmarked ≤0 **47/48** are a sparse high-spec clip, not
denser marked detection. Combined 71/96 is mostly those zeros. Do
**not** sell 24/48, 23/48, or tokhits **12/12** as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
