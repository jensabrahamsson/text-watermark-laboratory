# Transfer: 24 new 36-topic stems → 12×4 files

Train on `experiments/2026-08-17-pair-36` after dropping the twelve overlapping
prompt stems (`01-harbour` … `12-ferry-queue`). Score every file in
`experiments/2026-08-17-pair-12x4`. No test prompt family enters the fit.
`used_keys=false`.

This is the out-of-family single-file test: the 12×4 harbour/night-bus/… texts
are scored by tables that never saw those prompts.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hard last-4 | 10/12 | 0.640 | 32/48 | 27/48 |
| **hits** | 8/12 | **0.769** | **39/48** | 28/48 |
| **hashpool** | **11/12** | 0.766 | 34/48 | 30/48 |
| hashvote | 5/12 | 0.535 | 28/48 | 25/48 |
| hybrid | 10/12 | 0.757 | 34/48 | 31/48 |
| stack LDA | 10/12 | 0.754 | 27/48 | 35/48 |

Hits at threshold 0 is the strongest isolated *sign* here (39/48, binomial
p ≈ 8×10⁻⁶). Prompt-mean comparison is weaker (8/12) because some unmarked
twins also score slightly positive. Hashpool keeps the 11/12 prompt grain.

In-sample Youden on the 24 training files did not yield a better frozen
threshold than 0 for hits/hashpool (hard’s train Youden collapsed to “always
marked”). Ranking (AUC) is the fair isolated-file summary; the sign at 0 is
reported because that is the old 29/48 headline.

Frozen hashpool tables for `indicate score`: `tables-hashpool/`.
Count tables for `--score-mode hits`: `tables-counts/`.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-36 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --overlap drop-from-train \
  --out-dir experiments/2026-08-31-transfer-36-to-12x4
```
