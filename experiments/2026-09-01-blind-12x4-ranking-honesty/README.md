# Blind leave-one-prompt-out now reports ranking vs isolated sign

Not a new scorer. Same last-4 count tables as
`2026-09-01-blind-12x4-recount-last4/`. That historical JSON stays
stem-mean only. This run stores per-file LRs.

```bash
python -m text_watermark_tools blind experiments/2026-08-17-pair-12x4 \
  --context-len 4 \
  --out-dir experiments/2026-09-01-blind-12x4-ranking-honesty
```

`used_keys=false`. Stem-mean ranking is still **9/12**. Isolated marked
`lr>0` is still **25**. Garden ranks with **0/4** marked files above 0.
Station, office, and ferry-queue lose ranking but hold **5** of those
25 isolated TPs (ferry-queue 3/4). Do not rewrite **9/12** or **25/48**.
