# Last-4 coverage by token window (36×4)

`--coverage` is leave-one-prompt-out: for every scored position, was
that last-k context seen on **both** training sides? Hits can only fire
there. `used_keys=false`. Unbucketed. Full 128-token sequences.

Window `0:16` shared **13.7%** (592/4320) vs **3.9%** on `16:32`. That
average is **not** extra 4-grams in the opening. Positions 1–2 use short
contexts (last-1 / last-2) that almost always hit: i=1 is **96.9%**
shared (mean support 196). Full last-4 from i=4 is **3.4%** in 4:16,
the same rate as 16:32 (**3.9%**).

The ranking footprint is those first tokens. Scoring only `0:4` already
ranks **34/36** (AUC **0.917**), matching `0:16`. Tokens 4:16 still beat
chance (29/36, AUC 0.712); 16:32 is near chance (22/36, AUC 0.549). See
[`../2026-08-31-probe-36x4-windows-opening/`](../2026-08-31-probe-36x4-windows-opening/).

| Window | Shared last-k | n | Mean support when shared |
|---|---|---|---|
| 0:16 (includes last-1/2) | **0.137** (592/4320) | 4320 | **97.4** |
| 4:16 (full last-4 only) | 0.034 (117/3456) | 3456 | 9.7 |
| 16:32 | 0.039 (181/4608) | 4608 | 12.2 |
| 32:64 | 0.035 (319/9216) | 9216 | 13.1 |
| 64:128 | 0.039 (722/18396) | 18396 | 13.6 |

The keyed mixin marks every position. The key-free reader is
front-loaded because shared **short** contexts sit at the start, not
because later 4-grams are unmarked.
