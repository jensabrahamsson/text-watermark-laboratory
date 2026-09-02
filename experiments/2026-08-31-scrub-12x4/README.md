# 2026-08-31 — key-free argmax snap on the 12×4 marked files

Snap every token to the unmarked GPT-2 top-k argmax of the **original** prefix. The snap does not read watermark keys. Official `public-deepmind-30` scores are a reference check afterwards.

| Set | n | Official mean before | Official mean after |
|---|---:|---:|---:|
| All 48 marked twins | 48 | **0.6216** | **0.4994** |
| Unmarked control (`01-harbour-unmarked-gen.txt`) | 1 | 0.508 | 0.487 |

About 60–90 of 128 tokens flip. This is a statistical scrub, not a fluent paraphrase. The public mark dies on every marked file.

```bash
python -m text_watermark_tools scrub experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/2026-08-31-scrub-12x4
```
