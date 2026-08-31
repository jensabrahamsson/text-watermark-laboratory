# Transfer: 12×4 twins → 24 unseen 36-topic stems

Train on all twelve 12×4 prompt families. Score stems `13`–`36` from
`experiments/2026-08-17-pair-36` (`--overlap drop-from-test`). Those 24
topics never appear in training. `used_keys=false`.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hard last-4 | 14/24 | 0.606 | 16/24 | 12/24 |
| **hits** | **24/24** | **0.986** | **24/24** | 14/24 |
| **hashpool** | **23/24** | 0.924 | 21/24 | 20/24 |
| hashvote | 14/24 | 0.537 | 14/24 | 11/24 |
| **hybrid** | **23/24** | **0.946** | 22/24 | 20/24 |
| stack LDA | 21/24 | 0.880 | 12/24 | 24/24 |

Hits ranks the 24 new marked files almost perfectly (AUC 0.986, all 24
`lr > 0`). That is **not** a calibrated detector: ten of the 24 unmarked
twins are also positive at threshold 0. Test Youden t ≈ 0.35 reaches
sens 0.92 / spec 1.00 on this split; that threshold was read from the
test scores and is not a claimed operating point.

Hashpool and hybrid are the better-calibrated readers at 0 (specificity
20/24). Four draws per training prompt give hits more shared 4-gram
support than the 36→12×4 direction.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --test-dir experiments/2026-08-17-pair-36 \
  --overlap drop-from-test \
  --out-dir experiments/2026-08-31-transfer-12x4-to-36
```
