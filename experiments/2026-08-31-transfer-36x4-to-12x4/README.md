# Transfer: 24 new 36×4 stems → original 12×4 files

Train on `experiments/2026-08-31-pair-36x4` after dropping overlapping stems
`01-harbour` … `12-ferry-queue`. Score every file in
`experiments/2026-08-17-pair-12x4`. Four training draws per new topic.
`used_keys=false`. Nested Youden / 10% FPR from leave-one-prompt-out on the
24 training stems, then frozen on the 12×4 test files.

Compare with the 1-draw train split
[../2026-08-31-transfer-36-to-12x4/](../2026-08-31-transfer-36-to-12x4/)
(hits 8/12, isolated 39/48, nested hashpool Youden 33/48 vs 34/48).

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hard | 8/12 | 0.607 | 29/48 | 29/48 |
| **hits** | **12/12** | **0.793** | **42/48** | 24/48 |
| freqhits | 9/12 | 0.740 | 37/48 | 27/48 |
| hitmass | 11/12 | 0.784 | 42/48 | 24/48 |
| hashpool | 11/12 | 0.733 | 30/48 | 36/48 |
| **logit** | **12/12** | **0.812** | 21/48 | **45/48** |

**12/12 is ranking of prompt-mean LRs**, not isolated-file accuracy. Extra
training draws lifted prompt grain from 8/12 (1-draw hits) to 12/12 and
isolated hits at t=0 from 39/48 to 42/48. Unmarked specificity at 0 fell to
24/48. Logit at 0 is a specificity knob (21/48 vs 45/48), not a 12/12
ensemble of isolated files. Hard last-4 stayed weak (8/12, 29/48).

Nested operating points (train-only, no peeking at the 12×4 files):

| Method | Nested t | Test marked>t | Test unmarked≤t | sens | spec |
|---|---|---|---|---|---|
| **hits Youden** | 0.535 | 26/48 | 44/48 | 0.54 | 0.92 |
| hits FPR10 | 0.590 | 21/48 | 45/48 | 0.44 | 0.94 |
| hashpool Youden | 0.043 | 16/48 | 47/48 | 0.33 | 0.98 |
| logit Youden | 0.239 | 19/48 | 45/48 | 0.40 | 0.94 |
| logit FPR10 | −0.501 | 30/48 | 38/48 | 0.62 | 0.79 |

Four training draws made nested Youden *more conservative* than 1-draw
nested hashpool (33/48 vs 34/48): higher threshold, more specificity, less
recall. Ranking improved; a universal t=0 did not become a detector.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --overlap drop-from-train \
  --methods hard,hits,freqhits,hitmass,hashpool,logit \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4
```
