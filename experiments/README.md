# Experiments

Every run against **our** public DeepMind keys, plus the key-free twin dress rehearsal, plus the Claude control pile before announced marking.

How the with/without corpus works, and the 12/12 vs 8/12 numbers: [research/key-free-twins.md](../research/key-free-twins.md).

| Directory | What | Result |
|---|---|---|
| [2026-08-15-gpt2-sonnet5/](2026-08-15-gpt2-sonnet5/) | Marked GPT-2 T, errors, Sonnet proofread, Sonnet rewrite | T 0.617/0.638. Proofread 0.605/0.625. Rewrite 0.502/0.502 |
| [2026-08-15-known-mark/](2026-08-15-known-mark/) | v1 key-free rewrite (~35 flips) | residual ~0.55. **Obsolete** |
| [2026-08-15-known-mark-v2/](2026-08-15-known-mark-v2/) | v2: flip all source tokens with unmarked top-alt | ~0.62 → **~0.50**, 252 n-grams |
| [claude-premark-2026-08/](claude-premark-2026-08/) | Sonnet 5 before day-one / retrofit | **40** A/B texts, ~120k characters. 0001–0006 and four short UI files are not A/B |
| [2026-08-17-grok-prompts/](2026-08-17-grok-prompts/) | Grok-written prompts (not our key) | `score` should be ≈ 0.50. Input to `pair` |
| [2026-08-17-pair/](2026-08-17-pair/) | Same prompt × unmarked GPT-2 + mixin | Prompt ≈ 0.50. Unmarked-gen ≈ 0.50. Marked ≈ 0.62–0.63 |
| [2026-08-17-iterate-qwen/](2026-08-17-iterate-qwen/) | Qwen-plus paraphrase of the marked harbour twin | 0.623 → **0.509** in one pass |
| [2026-08-17-blind-pairs/](2026-08-17-blind-pairs/) | 12 prompts × marked / unmarked GPT-2 | Oracle: marked 0.61–0.65, unmarked ≈ 0.50 |
| [2026-08-17-blind/](2026-08-17-blind/) | Key-free leave-one-out on the 12 pairs | **8/12** — indication the idea is promising |
| [2026-08-17-pair-limit/](2026-08-17-pair-limit/) | Same 12 seeds × 700 new tokens + control-key twins | Official 12/12. Control-gen public ≈0.50, matching 0.61–0.63 |
| [2026-08-17-blind-limit/](2026-08-17-blind-limit/) | Key-free leave-one-out on the 700-token twins | **6/12**. Longer last-1 did not beat 8/12 @ 128 |
| [2026-08-17-pair-qwen/](2026-08-17-pair-qwen/) | Local Qwen2-1.5B-Instruct × mixin on/off | Official **12/12** (Qwen tokenizer) |
| [2026-08-17-blind-qwen/](2026-08-17-blind-qwen/) | Key-free last-1 on the Qwen twins | **4/12** |
| [2026-08-17-blind-qwen-k2/](2026-08-17-blind-qwen-k2/) | Same twins, last-2 | **10/12** |
| [2026-08-17-pair-36/](2026-08-17-pair-36/) | 36 GPT-2 twins × 256 | Official 36/36. Blind last-1 **22/36** |
| [2026-08-17-pair-12x4/](2026-08-17-pair-12x4/) | 12 prompts × 4 samples × 128 | Extra draws for last-4 reuse |
| [2026-08-17-blind-12x4-k4/](2026-08-17-blind-12x4-k4/) | Key-free last-4 on 12×4 | **10/12** |
| [2026-08-17-blind-12x4-k4-margin015/](2026-08-17-blind-12x4-k4-margin015/) | Same, hit if marked_lr+0.015 ≥ unmarked | **11/12** (station). Office still out |
| [2026-08-17-blind-qwen-k2-margin02/](2026-08-17-blind-qwen-k2-margin02/) | Qwen last-2, margin 0.02 | **11/12** (letter). Kitchen still out |
| [indicator-gpt2/](indicator-gpt2/) | Frozen key-free tables (12×4, last-4) | `indicate score FILE --tables experiments/indicator-gpt2` |
| [2026-08-17-indicate-holdout-12x4/](2026-08-17-indicate-holdout-12x4/) | Rotate: fit 11, score each held file alone | Prompt grain **10/12**. One marked file `lr>0`: **29/48** |
| [2026-08-17-indicate-holdout-12x4-margin02/](2026-08-17-indicate-holdout-12x4-margin02/) | Same LRs, hit if marked_lr+0.02 ≥ unmarked | Prompt **11/12** (station). Office still out. Sign **39/48** |

Score a file:

```bash
source .venv/bin/activate
python -m text_watermark_tools score experiments/2026-08-15-gpt2-sonnet5/t_high_temp.txt
```

A new known-mark run writes `source.txt`, `rewrite.txt`, `results.json`, `results.md` under `--out-dir`.

Iterate until *our* instance is chance (`--backend qwen` or `deepseek`; key in `*-KEY.conf`):

```bash
python -m text_watermark_tools iterate experiments/2026-08-15-gpt2-sonnet5/t_high_temp.txt \
  --backend qwen --out-dir experiments/2026-08-17-iterate-qwen --max-passes 4
```

Same prompt, marked and unmarked twin (does not stamp the string):

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --out-dir experiments/2026-08-17-pair --max-new-tokens 128
```
