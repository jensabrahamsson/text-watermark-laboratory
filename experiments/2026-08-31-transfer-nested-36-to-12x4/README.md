# Nested thresholds: 24 new topics → 12×4 files

Same split as `../2026-08-31-transfer-36-to-12x4/` (drop overlapping stems
from train). Adds `freqhits`, `hitmass`, `hashmix`, and **nested** operating
points: leave-one-prompt Youden and 10% FPR on the 24 training stems, then
frozen on the 12×4 test files. `used_keys=false`.

| Method | Prompt wins | File AUC | Marked `> 0` |
|---|---|---|---|
| hard | 10/12 | 0.640 | 32/48 |
| hits | 8/12 | 0.769 | 39/48 |
| freqhits | 7/12 | 0.763 | 39/48 |
| **hitmass** | **10/12** | **0.771** | 39/48 |
| hashpool | **11/12** | 0.766 | 34/48 |
| hashmix | **11/12** | 0.681 | 33/48 |
| hybrid | 10/12 | 0.757 | 34/48 |
| stack | 10/12 | 0.754 | 27/48 |

Coverage-weighted hits (`hitmass`) recovers the prompt grain that plain
hits lost (8/12 → 10/12) without hurting file AUC.

Nested thresholds on the *test* files (train-only, no peeking):

| Method | Nested t | Test marked>t | Test unmarked≤t | sens | spec |
|---|---|---|---|---|---|
| hits Youden / FPR10 | 0.368 | 22/48 | 40/48 | 0.46 | 0.83 |
| **hashpool Youden** | **0.005** | **33/48** | **34/48** | **0.69** | **0.71** |
| hashpool FPR10 | 0.016 | 26/48 | 41/48 | 0.54 | 0.85 |
| hitmass Youden | 0.013 | 17/48 | 44/48 | 0.35 | 0.92 |

In-sample Youden on training files that entered the fit is still reported
and is still optimistic (hard collapsed to “always marked”). The nested
hashpool point is the honest isolated-file operating point on this split:
balanced, not 39/48 at threshold 0.

Frozen hashpool tables store `decision_threshold` from nested Youden:
`tables-hashpool/`. Count tables store the nested hits Youden:
`tables-counts/` (use `--score-mode hits` or `hitmass`).
