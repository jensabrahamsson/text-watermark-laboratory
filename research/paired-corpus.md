# Paired corpus for an unknown-key watermark

The controlled DeepMind experiments show that matched marked/unmarked generations can support a **key-free watermark indicator**.

The next step is to reproduce that design on a production system where the detector keys are genuinely unavailable.

Claude is one candidate.

## Experimental design

The cleanest corpus is a before/after pair built from the **same prompt set**.

### Before

Collect exact `(prompt, output)` pairs under a condition believed to precede marking.

Store:

- exact prompt string;
- output;
- model identifier or UI model claim;
- collection timestamp;
- surface used;
- assumed watermark state.

### After

Once the same model/family is announced as marked, rerun the **same prompts** under as similar a generation setup as possible.

### Learn the shift

Fit a surrogate from the paired corpora:

\[
\log P(\text{text}\mid\text{marked corpus})
-
\log P(\text{text}\mid\text{unmarked corpus})
\]

The model does not need the production keys. It needs a clean enough experimental contrast.

## Why same prompts matter

A pile of old Claude text and a pile of new Claude text are not automatically a watermark experiment.

Topic, model updates, style, decoding changes, and product changes can all create distribution shifts.

Using the same prompts removes one major confound. Using the same model identifier before and after retrofit would be stronger still.

The ideal comparison is:

```text
same model
same prompts
same sampling setup
one intended change: watermark off → on
```

## Current corpus

The pre-mark material lives in:

```text
experiments/claude-premark-2026-08/
```

The prompt source is:

```text
scripts/collect_claude_premark.py
```

Do not edit existing `PROMPTS` strings after collection. Add new prompts instead.

Earlier rewrite samples from 15 August are useful auxiliary Claude prose but are not clean A/B pairs for this experiment because their input was already watermarked GPT-2 text.

## Evaluation

When an "after" corpus exists:

1. hold one prompt group out;
2. fit marked/unmarked token/context statistics on the others;
3. score the held-out group;
4. rotate across prompts;
5. compare against shuffled or unmarked-vs-unmarked controls.

This is the same logic that reaches **10/12–11/12** in the controlled public-mixin experiment.

See [key-free-twins.md](key-free-twins.md).
