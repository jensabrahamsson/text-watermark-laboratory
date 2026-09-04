# Exploratory holdouts for the three proven width ideas

JSON-only copies of the `/tmp/kgw-lab` probes that back
[lovande-idéer-260903.md](../../lovande-idéer-260903.md) (GitHub PR **#7**).
The markdown catalog stays on that PR. This directory is the dump so a
later agent does not re-run 100-family last-1 / last-2 hashing.

`used_keys=false` on every `holdout.json`. Isolated counts come from
`n_marked_lr_positive` / `n_prompts_marked_above` on the window
holdout, not nested-by-stem columns in `results.md`. File-level LRs stay
in each `holdout.json` so leftover re-slices can reuse
`summarize_leftover_holdouts` without inventing a scorer.

This is not a new `probe --methods` name. It does not replace **25/48**.
Last-2 does not fix leftover-20. Do not leftover-target. Do not sell
Qwen Aaronson last-2 hashtok2 32:64 **320/400**, Kirchenbauer last-2
hashpool 32:64 **100/100**, or Distil public SynthID last-2 hashpool
32:64 **75/100**. Isolated-file detection is still not finished. Do not
write `thesis/`.

Pair dumps already on `main`:

| Mixin | GPT-2 100 | Distil 100 | Qwen 100 |
|---|---|---|---|
| Kirchenbauer | `experiments/2026-09-03-pair-100x4-kgw` | `experiments/2026-09-03-pair-distil-100x4-kgw` | in-flight; do not invent counts |
| Aaronson–Kirchner | `experiments/2026-09-04-pair-100x4-aaronson` | `experiments/2026-09-04-pair-distil-100x4-aaronson` | `experiments/2026-09-04-pair-qwen-100x4-aaronson` |
| Public SynthID | `experiments/2026-09-01-pair-100x4` | `experiments/2026-09-01-pair-distil-100x4` | `experiments/2026-09-01-pair-qwen-100x4` |

Reproduce (CPU JAX; do **not** pass `--skip-hashpool` for `hashtok` /
`hashtok2`):

```bash
export PYTHONPATH=src JAX_PLATFORMS=cpu
python3 -m text_watermark_tools probe PAIR \
  --methods hashtok2 --context-len 2 --skip-nested --windows 32:64 \
  --out-dir /tmp/kgw-lab/example
```

Qwen probes must pass `--model Qwen/Qwen2-1.5B-Instruct`. Distil 100
Kirchenbauer / public SynthID probes in these dumps used `--model gpt2`
(same BPE). Index: [index.json](index.json). Tests:
`tests/test_lovande_holdouts.py`.
