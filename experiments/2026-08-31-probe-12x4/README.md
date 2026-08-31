# 2026-08-31 — key-free probe on the 12×4 GPT-2 twins

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. No keys, no `hash_iv`, no g-values. Official `score` is not used to decide.

The published hard last-4 count LR is reproduced as **10/12** (AUC **0.626**, isolated `lr > 0` **29/48**).

Better key-free readers of the same twins:

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | perm p |
|---|---|---|---|---|---|
| unigram | **11/12** | 0.592 | 26/48 | 24/48 | 0.031 |
| hard (published) | 10/12 | 0.626 | 29/48 | 23/48 | 0.0075 |
| backoff | 7/12 | 0.521 | 29/48 | 21/48 | 0.28 |
| interpolate | 7/12 | 0.524 | 24/48 | 24/48 | 0.36 |
| **hits** (shared 4-grams) | **11/12** | **0.737** | 28/48 | 30/48 | 0.00050 |
| gated (count ≥ 2) | 10/12 | 0.717 | 27/48 | 31/48 | 0.00050 |
| shrinkage | **11/12** | 0.734 | 28/48 | 30/48 | 0.00050 |
| mix last-1+4 | 6/12 | 0.520 | 25/48 | 21/48 | 0.33 |
| **hashpool** | **11/12** | 0.716 | **35/48** | 29/48 | 0.00050 |
| pivot-lda | 10/12 | 0.599 | 17/48 | 31/48 | 0.016 |
| pivot-rank | 8/12 | 0.609 | 26/48 | 27/48 | 0.045 |

Prompt-level misses (mean LR):

| Method | Miss |
|---|---|
| hard | station, office |
| unigram | office |
| hits / shrinkage | night-bus |
| hashpool | letter |

`hits` and `hashpool` fail **different** prompts. That is a note, not a 12/12 ensemble claim.

JSON: `results.json` plus one `holdout.json` per method. Pivot holdouts were copied from `../2026-08-31-probe-pivot/`.

Reproduce:

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/2026-08-31-probe-12x4
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods unigram --skip-hashpool --pivot \
  --out-dir experiments/2026-08-31-probe-pivot
```
