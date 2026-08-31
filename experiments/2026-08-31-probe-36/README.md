# 2026-08-31 — key-free probe on 36 GPT-2 topics (one draw each)

Leave-one-prompt-out on `experiments/2026-08-17-pair-36`. No keys.

The original last-1 blind on this corpus was **22/36**. Hard last-4 here is **20/36** (AUC 0.549): more topics still do not help the published scorer.

Coverage gating and hash pooling do:

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | perm p |
|---|---|---|---|---|---|
| unigram | 22/36 | 0.590 | 18/36 | 21/36 | 0.067 |
| hard | 20/36 | 0.549 | 20/36 | 18/36 | 0.16 |
| backoff | 22/36 | 0.623 | 26/36 | 20/36 | 0.068 |
| interpolate | **29/36** | 0.796 | 26/36 | 26/36 | 0.00050 |
| **hits** | **30/36** | **0.886** | 33/36 | 16/36 | 0.00050 |
| gated | **31/36** | 0.856 | 32/36 | 16/36 | 0.00050 |
| shrinkage | **31/36** | 0.875 | 33/36 | 18/36 | 0.00050 |
| mix | 22/36 | 0.628 | 19/36 | 22/36 | 0.043 |
| **hashpool** | **31/36** | 0.877 | 32/36 | 22/36 | 0.00050 |

`hits` at threshold 0 is sensitive (33/36) but not specific (16/36 unmarked ≤ 0). Youden t ≈ 0.39 gives sens 0.83 / spec 0.89. Hashpool’s Youden t ≈ 0.022 gives spec 0.97.

This revises the earlier lesson that “more topics alone do not help”. They help once unseen 4-grams are not scored as unigrams.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-36 \
  --out-dir experiments/2026-08-31-probe-36
```
