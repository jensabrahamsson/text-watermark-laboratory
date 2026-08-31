# Opening-overlap bound (short + medium + tails → 12×4)

Isolated observed-token recall equals train opening-atom overlap.
`--fit-prefix 4 --pos-bucket 1`. Not keys.

Train groups added in order: 24 short one-liners (36×4 minus the 12×4
stems), 12 medium scenes, 12 tail-transplants.

| upto | postokhits | postokbackoff | postokbackoff2 | last-1 later |
|---|---|---|---|---|
| 24 short | **16/48** | **16/48** | **13/48** | 0 |
| +12 medium | **20/48** | **22/48** | **13/48** | 2 |
| +12 tails | **30/48** | **36/48** | **13/48** | 6 |

`postokbackoff2` (min last-2) stays **13/48** while last-1 backoff
carries 16→36. Those six last-1-later files are library `' is' → ' the'`
and harbour `' was' → ' in'`. Precision **1.000** among decided.
Unbucketed last-1 copies 36/48 but adds 3 unmarked FPs. `--include-first`
on postokhits is a first-token unigram (**43/48**, 10 FP); tokbackoff
refuses empty last-k so it stays 36/48.

Do not sell 36/48 as beating 39/48. Do not replace 10/12, 29/48, 36/36.
Not a universal detector.
