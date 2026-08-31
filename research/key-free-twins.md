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
| Qwen2-1.5B twins, last-2 | **10/12** |
| Single held-out marked file, `lr > 0` | **29/48** |

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

Thirty-six different prompts at 256 tokens reach **22/36** at last-1. More topical variety also does not automatically strengthen the signal.

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
same LRs. Further scorers (Witten–Bell interpolation, coverage gating, context
hash pooling, unmarked-LM choice geometry) and a key-free argmax snap are
documented in [key-free-probe.md](key-free-probe.md). They still do not use
the detector keys.

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
