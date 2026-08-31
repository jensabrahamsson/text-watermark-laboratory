# Key-free watermark indication from matched generations

## Result

We have built a **key-free indicator for watermark presence**.

The indicator is trained on matched marked/unmarked generations from the same prompts and then evaluated on held-out prompts. It does not use the watermark keys, `hash_iv`, g-values, or DeepMind's `detector_mean` to make the held-out decision.

Current results:

| Experiment | Result |
|---|---|
| Official public-key detector, 12 prompts | **12/12** |
| Key-free, 12 prompts × 1 draw | **8/12** |
| Key-free, 12 prompts × 4 draws, last-4 | **10/12** |
| Same LRs with 0.02 comparison margin | **11/12** |
| Key-free `hits` (shared 4-grams only) | **11/12**, AUC **0.737** |
| Key-free hashpool | **11/12**, isolated **35/48** |
| Key-free hashpool, 36 GPT-2 topics | **31/36**, AUC **0.877** |
| Key-free hashpool, Qwen 12×1 | **10/12**, isolated **11/12** |
| Key-free hits, train 24 other topics → 12×4 files | isolated **39/48**, AUC **0.769** |
| Nested hashpool Youden on that split | **33/48** marked, **34/48** unmarked |
| Key-free hits, 24×4 new stems → 12×4 | **12/12** ranking, isolated **42/48**, AUC **0.793** |
| Nested hits Youden, 4-draw train | **26/48** vs **44/48** |
| Nested hits FPR10, 12×4 → 36×4 | **83/96** vs **85/96** |
| Key-free hits, 36 topics × 4 draws LOO | **36/36**, AUC **0.934**; nested-by-stem **119/144** vs **134/144** |
| Key-free hits, first 16 tokens, 36×4 | **34/36**, AUC **0.916** |
| Key-free hits, matched 16-token fit, 36×4 | **34/36**, AUC **0.929**; unmarked ≤0 **112/144** |
| Key-free poshits (bucket=16), 36×4 | **34/36**, AUC **0.925**; t=0 spec **97/144** |
| Key-free hits, tokens 16–32 only, 36×4 | **22/36**, AUC **0.549** |
| Key-free hits, matched 16-token 24×4 → 12×4 | **11/12**, AUC **0.818**; nested-by-stem 39/48 vs 36/48 |
| Key-free poshits, 24×4 → 12×4 | **10/12**, AUC **0.811**; nested-by-stem 37/48 vs 35/48 |
| Key-free poshits, matched 16-token bucket 4, 36×4 | **34/36**, AUC **0.937**; unmarked ≤0 **114/144** |
| Key-free hits, tokens 0:4 only, 36×4 | **34/36**, AUC **0.917** (matches 0:16) |
| Key-free poshits, matched 4-token bucket 1, 36×4 | **34/36**, AUC **0.935**; t=0 **131/144 vs 132/144** |
| Same reader, 24×4 → 12×4 | **12/12**, AUC **0.873**; t=0 **39/48 vs 41/48** |
| Key-free postokhits on that OOD gate | **12/12**, isolated **16/48**, decided precision **1.000** |
| Same postokhits, 36×4 LOO | 34/36, AUC 0.912; t=0 **122/144 vs 132/144** |
| Key-free postokhits, 12 medium scenes → 12×4 | **12/12**, isolated **19/48**, decided precision **1.000** |
| Same plus 24 short one-liners | **12/12**, isolated **20/48**, decided precision **1.000** |
| Key-free postokbackoff, 12 medium scenes → 12×4 | **12/12**, isolated **21/48**, decided precision **1.000** |
| Key-free postokbackoff plus 24 short one-liners | **12/12**, isolated **22/48**, decided precision **1.000** |
| Key-free postokhits, tail-matched train → 12×4 | **12/12**, isolated **30/48**, decided precision **1.000** |
| Key-free postokbackoff, short+medium+tails → 12×4 | **12/12**, isolated **36/48**, AUC **0.888**, decided precision **1.000** |
| Key-free postokbackoff2 on that combined train | **13/48** last-2+ core (unchanged from 24 short stems) |
| Opening-overlap bound, same twins | Isolated recall = train atom overlap; two short stems already cover 13/48 |
| Unbucketed tokbackoff on that combined train | **36/48** marked, **3** unmarked FP, precision 0.923 |
| `--include-first` postokhits on that combined train | **43/48** marked, **10** unmarked FP (first-token unigram) |
| Neighborhood paraphrases, 12 scenes × 4 | Official lamp **12/12**; no Closing/Now/While/The ferry openings |
| Same plus short+medium+tails → 12×4 | postokbackoff **42/48**, last-2+ **15/48**, precision **1.000** |
| Key-free last-1, matched 4-token 24×4 → 12×4 | **12/12**, AUC **0.873**; t=0 **39/48 vs 41/48** |
| `--include-first` on that 4-token OOD gate | 9/12, AUC 0.719 |
| Qwen 12×4 first-token opening | **12/12**, AUC **0.901** |
| DistilGPT2 12×4 official / in-domain hits | **12/12** / **9/12**, AUC 0.705 |
| GPT-2 36×4 → DistilGPT2 (same BPE) | hits **5/12**, AUC **0.462** |
| Key-free tokmlp, 4-token 24×4 → 12×4 | 8/12, AUC 0.714 (does not beat poshits **0.873**) |
| Key-free hashlog on that OOD gate | 7/12, AUC 0.606 |
| GPT-2 learned scorers → Distil / Qwen | chance (charcnn Qwen AUC 0.496) |
| Key-free poshits vs control-shuffled-30, 4-token 24×4 → 12×4 | **0/48** control `lr>0`; public vs control **12/12**, AUC **0.906** |
| Key-free postokhits vs control-shuffled-30, same split | **0/48** control `lr>0`; public vs control **12/12**, AUC 0.667 |
| Key-free postokbackoff vs control-shuffled-30, same split | **0/48** control `lr>0`; public vs control **12/12**, AUC 0.667 |
| Official lamp, 12×4 control-key twins | public **0.501**; matching **0.624** |
| Key-free last-k coverage, 36×4 LOO | 0:16 shared **13.7%** (i=1–2); full last-4 from i=4 ~4% |
| Key-free poshitmass, matched 16-token bucket 4 | **34/36**, AUC **0.943**; unmarked ≤0 **114/144** |
| Key-free poshits, matched 16-token bucket 1, 36×4 | **34/36**, AUC **0.938**; t=0 **132/144 vs 132/144** |
| Same 16-token reader, 24×4 → 12×4 | **12/12**, AUC **0.873**; t=0 **39/48 vs 41/48** |
| Mixin last-5 vs last-4, 36×4 hits | **35/36**, AUC **0.912** (does not beat last-4) |
| UTF-8 surface, 12×4 leave-one-out | **10/12**, AUC **0.602** |
| Same-topic GPT-2 hits → Qwen 12×1 | **11/12** paired; isolated `lr>0` **1/12** |
| New Qwen 12×4 sample, same prompts, GPT-2 hits | **5/12** (first-draw **6/12**); does not replicate 11/12 |
| Qwen 12×4 in-domain hits, Qwen tokenizer | **8/12**, AUC **0.602** |
| New GPT-2 topics → Qwen | chance |
| New topics GPT-2 36×4 → new Qwen 12×4 | hits **6/12**, AUC 0.445 |
| Key-free hits, train 12×4 → 24 new topics | **24/24** ranking, AUC **0.986** (unmarked ≤0 only 14/24) |
| Nested freqhits Youden on the reverse split | **23/24** and **23/24** |
| 50% train-label shuffle, isolated sign | hits **19/48**, hashpool **20/48** |
| Qwen2-1.5B twins, last-2 | **10/12** |
| Single held-out marked file, hard `lr > 0` | **29/48** |

The 10/12 last-4 count table is unchanged. Stronger readers of the same twins, out-of-family transfer, and a key-free argmax snap are in [key-free-probe.md](key-free-probe.md). Instance contrast against `control-shuffled-30` is in [key-free-contrast.md](key-free-contrast.md). Occupancy Laplace versus observed next tokens, tokbackoff, and the opening-overlap bound are in [key-free-tokhits.md](key-free-tokhits.md). Opening-only unmarked-LM geometry and coverage-then-pivot ABSTAIN are in [key-free-cascade.md](key-free-cascade.md).

That is enough to establish a useful statistical signal under the tested conditions. It is not enough to treat every isolated paragraph as reliably classifiable.

## Why matched twins

SynthID-Text does not append a hidden tag to a finished string. It biases token selection during generation.

To separate watermark effects from topic and style, we generate the **same prompt twice**:

| File | Generation |
|---|---|
| `*-prompt.txt` | original seed |
| `*-unmarked-gen.txt` | GPT-2, watermark mixin off |
| `*-marked.txt` | GPT-2, same prompt, watermark mixin on |

The generation path gives us ground truth. The public detector is then used only as a reference check that the marked pile really is marked.

## Protocol

```text
same prompts
   │
   ├── mixin off ──→ unmarked texts
   │
   └── mixin on  ──→ marked texts
                         │
              ┌──────────┴──────────┐
              │                     │
       public-key score       key-free indicator
       reference check        leave one prompt out
                              fit token/context tables
                              LR = log P(marked) - log P(unmarked)
```

For each held-out prompt:

1. remove all samples for that prompt from training;
2. fit marked and unmarked token/context tables on the remaining prompts;
3. score the held-out marked and unmarked samples;
4. compare their likelihood ratios;
5. rotate until every prompt has been held out.

No detector keys are needed in steps 2–4.

## Public-key reference

The 12 original GPT-2 prompt pairs separate completely under the public reference detector:

| Stem | Prompt | Unmarked | Marked |
|---|---:|---:|---:|
| harbour | 0.500 | 0.508 | **0.621** |
| night-bus | 0.498 | 0.496 | **0.633** |
| library | 0.493 | 0.499 | **0.633** |
| market | 0.479 | 0.505 | **0.630** |
| kitchen | 0.509 | 0.506 | **0.614** |
| station | 0.520 | 0.498 | **0.627** |
| rain | 0.515 | 0.491 | **0.617** |
| letter | 0.513 | 0.507 | **0.622** |
| workshop | 0.498 | 0.491 | **0.605** |
| office | 0.518 | 0.506 | **0.647** |
| garden | 0.484 | 0.502 | **0.629** |
| ferry-queue | 0.524 | 0.499 | **0.616** |

The public detector therefore gives **12/12** clean reference separations.

## Key-free runs

### One sample per prompt

With 12 prompts × 128 tokens and last-1 token counts, the marked twin ranks higher on **8/12** held-out prompts.

Increasing context immediately makes this tiny corpus sparse: last-2 and last-3 both fall to 4/12.

### More tokens alone

At 700 new tokens per prompt, last-1 gives **6/12**. Longer text by itself does not solve the problem.

### More topics alone

Thirty-six different prompts at 256 tokens reach **22/36** at last-1. Hard last-4 on the same corpus is **20/36**. More topical variety does not automatically strengthen the **hard** scorer.

Coverage-gated and hash-pool readers of those same 36 twins reach **30–31/36** (AUC 0.88). The topics were carrying signal; unigram fallback was burying it. See [key-free-probe.md](key-free-probe.md).

### Repeated draws from the same prompts

This is where the result improves.

With 12 prompts × 4 GPT-2 generations and a last-4 context, the held-out prompt result reaches **10/12**. Last-2 and last-3 reach the same result.

The two misses are *station* and *office*.

A 0.02 comparison margin moves *station* into the correct side, giving **11/12**. *Office* remains a clear miss.

The important empirical lesson is therefore not "more text is better". **Repeated evidence from the same prompt creates the context reuse that the higher-order indicator needs.**

### Different generator

With local Qwen2-1.5B twins, last-2 reaches **10/12**. This matters because the effect is not confined to one exact GPT-2 run.

## From twin comparison to one-file `indicate`

`blind` compares held-out marked and unmarked twins. `indicate` turns the same idea into a score for one file.

Fit on 11 prompt groups, then score each file from the held-out group:

```bash
python -m text_watermark_tools indicate holdout \
  experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4
```

At prompt-mean grain the result remains **10/12**.

At individual-file grain, however:

- marked files with `lr > 0`: **29/48**
- unmarked files with `lr <= 0`: **23/48**
- mean marked LR: **+0.033**
- mean unmarked LR: **−0.003**

The distributions overlap. That makes the one-file LR a useful **indicator**, but not yet a reliable binary detector.

## What the result establishes

The result is stronger than "watermarks leave traces".

Under controlled matched generation, those traces are systematic enough to build a model that **predicts watermark presence on held-out data without the detector keys**.

The result is also narrower than "we can detect any watermark in any text".

What works best today is:

- matched marked/unmarked training data;
- repeated samples;
- prompt-level aggregation;
- a generator and sampling setup sufficiently similar to the learned corpus.

What remains difficult is one arbitrary isolated text with no matched context.

`indicate holdout` now prints a single-file AUC and a permutation test on the
same LRs. Further scorers (coverage gating, hash pooling, unmarked-LM choice
geometry) and a key-free argmax snap are measured in
[key-free-probe.md](key-free-probe.md). `hits` reaches **11/12** and AUC
**0.737**; hashpool reaches **11/12** and isolated **35/48**. They still do
not use the detector keys.

## Why this matters for unknown production keys

The public DeepMind instance is the laboratory control because we know the ground truth and can verify it independently.

The interesting application is a system where the keys are *not* public. If we can collect clean before/after or marked/unmarked pairs, we can ask the same statistical question without pretending to reproduce the vendor's official detector.

That is the purpose of the Claude paired-corpus plan in [paired-corpus.md](paired-corpus.md).

## Reproduce

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --out-dir experiments/2026-08-17-blind-pairs \
  --max-new-tokens 128

python -m text_watermark_tools blind \
  experiments/2026-08-17-blind-pairs \
  --out-dir experiments/2026-08-17-blind

python -m text_watermark_tools indicate holdout \
  experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4
```

Experiment index: [../experiments/README.md](../experiments/README.md).
