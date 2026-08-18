# Corpus with and without the mark (no key)

Official `score` needs the same keys that were used at sampling. This page is the other lamp: **same prompt, mark on vs mark off**, then ask whether a held-out text looks like the marked pile — without `keys`, `hash_iv`, or g-values.

We ran this on 17 August 2026 against DeepMind’s public mixin. That is a dress rehearsal for a key we do *not* have (Claude). It is not a Claude detector and not key recovery. See [invertibility.md](invertibility.md).

## Why twins

SynthID-Text does not write hidden characters into a string. The mark is *which next token the sampler chose*. You cannot stamp an existing paragraph and then “see the stamp”.

So a pile of “marked-looking prose” is not a corpus. You need the **same input twice**, with the only intended difference being the mixin:

| File | How it was made |
|---|---|
| `*-prompt.txt` | Seed. Not generated under the mixin. `score` ≈ 0.50 |
| `*-unmarked-gen.txt` | New tokens from that prompt, GPT-2, mixin **off** |
| `*-marked.txt` | New tokens from the **same** prompt, GPT-2, mixin **on** |

Ground truth for the key-free question is how the file was **created**, not the official mean.

A single text with no twin only lets you run `score` *if you already have the keys*. Without keys, one essay is not enough — more tokens plus the wrong key is just a more confident 0.50.

## Protocol

```text
prompts
   │
   ├─ generate, mixin off  →  unmarked pile
   └─ generate, mixin on   →  marked pile
                              │
              ┌───────────────┴───────────────┐
              │                               │
     score (public keys)              blind (no keys)
     sanity: the mark is real         leave one prompt out
                                      fit two next-token tables
                                      from the other pairs
                                      LR = log P_marked − log P_unmarked
```

`pair` writes the twins and the official scores. `blind` never calls `detector_mean`. Fit flags `used_keys` / `used_hash_iv` / `used_g_values` stay false.

The context window in `blind` is a **fit knob** (default last-1 token), not watermark `ngram_len=5`. Last-2+ is too sparse on 12 × 128 tokens.

## What we ran

Twelve short English seeds in [`experiments/2026-08-17-grok-prompts/`](../experiments/2026-08-17-grok-prompts/) (Grok-written, not our mark). Then:

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --out-dir experiments/2026-08-17-blind-pairs --max-new-tokens 128

python -m text_watermark_tools score experiments/2026-08-17-blind-pairs

python -m text_watermark_tools blind experiments/2026-08-17-blind-pairs \
  --out-dir experiments/2026-08-17-blind
```

(There is also a 3-prompt smoke run in `experiments/2026-08-17-pair/`.)

### Lamp 1 — we have the public keys

Every marked twin lights up. Every unmarked twin sits at chance. **12/12**.

| Stem | Prompt mean | Unmarked-gen mean | Marked mean |
|---|---|---|---|
| 01-harbour | 0.500 | 0.508 | **0.621** |
| 02-night-bus | 0.498 | 0.496 | **0.633** |
| 03-library | 0.493 | 0.499 | **0.633** |
| 04-market | 0.479 | 0.505 | **0.630** |
| 05-kitchen | 0.509 | 0.506 | **0.614** |
| 06-station | 0.520 | 0.498 | **0.627** |
| 07-rain | 0.515 | 0.491 | **0.617** |
| 08-letter | 0.513 | 0.507 | **0.622** |
| 09-workshop | 0.498 | 0.491 | **0.605** |
| 10-office | 0.518 | 0.506 | **0.647** |
| 11-garden | 0.484 | 0.502 | **0.629** |
| 12-ferry-queue | 0.524 | 0.499 | **0.616** |

Full table: [`experiments/2026-08-17-blind-pairs/results.md`](../experiments/2026-08-17-blind-pairs/results.md).

One harbour line, so the files are concrete: prompt `01-harbour-prompt.txt` is unmarked seed; `01-harbour-unmarked-gen.txt` is new GPT-2; `01-harbour-marked.txt` is new GPT-2 + mixin. Same prompt string. Different sampler.

### Lamp 2 — we throw the keys away

Leave-one-prompt-out. Train on 11 marked + 11 unmarked sequences (token counts only). Score the held-out pair. “Win” = the held-out *marked* text has a higher likelihood ratio than the held-out *unmarked* text.

| context_len | Marked higher |
|---|---|
| **1** | **8/12** |
| 2 | 4/12 |
| 3 | 4/12 |

Eight of twelve held-out prompts: the marked twin looked more like the marked pile. Misses: harbour, office, garden, ferry-queue. Last-2 and last-3 flip the other way — too few counts per context.

A later CPU-limit rerun on the same 12 seeds at **700** new tokens (`experiments/2026-08-17-blind-limit/`) is **6/12** at last-1. Last-3 on that pile is 8/12 again.

Local Qwen2-1.5B twins (`experiments/2026-08-17-pair-qwen/`): last-1 is **4/12**; last-2 is **10/12** (`experiments/2026-08-17-blind-qwen-k2/`).

Twelve prompts × **four** GPT-2 draws (`experiments/2026-08-17-pair-12x4/`): last-4 is **10/12** (`experiments/2026-08-17-blind-12x4-k4/`). Last-2 and last-3 match that. Last-1 is 1/12. Thirty-six *different* prompts at 256 tokens only reached 22/36 at last-1.

The same 12×4 pile, scored as **one file at a time** (`indicate holdout --rotate`, `experiments/2026-08-17-indicate-holdout-12x4/`): prompt-mean grain is still **10/12** (station and office miss). A single marked file with `lr>0` is only **29/48**. Unmarked files sit on the sign of zero (**23/48** `lr≤0`). Mean marked LR +0.033, unmarked −0.003.

`--margin 0.02` on those same LRs (`experiments/2026-08-17-indicate-holdout-12x4-margin02/`): **11/12** prompts (station). Office still misses by 0.066. One-file sign becomes 39/48 if the bar is `lr > −0.02`. That is a lower bar, not a stronger model. 12/12 would count office.

The tournament is not a unigram. Last-4 needs reuse. Extra samples of the same prompt did that. Extra topics did not. One new paragraph against frozen tables is not the same measurement as comparing twins.

Per-prompt (context_len=1): [`experiments/2026-08-17-blind/results.md`](../experiments/2026-08-17-blind/results.md).

## What those numbers mean

- The **twins work**. With the public keys the two piles do not overlap.
- Without the key, **8/12 is an indication the idea is promising**. Eight held-out prompts lean the right way; four miss. Last-4 on 12×4 is **10/12**. `indicate` is a **possible / weak indicator**. Leave-one-out (`indicate holdout --rotate`) is the test: train on all twin prompts except one, score that held-out text alone. One new file is weaker (29/48 marked files have `lr>0`). Not a lamp you point at one new paragraph. Do not treat `indicate` as official `score`.
- Light word-choice polish (“sounds better”) is the **control** on `iterate --via polish`. Substantial paraphrase is the default. `iterate --stop-on indicate` can stop when the single-file LR goes dark; official mean / weighted mean are still recorded. That loop is **not a remover**. Indicator-dark is not “this instance went to 0.50”.
- The tournament lives in keyed 5-grams. Last-1 counts are a blunt instrument. More pairs and longer generations come next.
- This is still the right *question* when the key is unknown: not “is this AI?”, but “does this text look like the marked twin pile?”

Known-mark v2 ([`experiments/2026-08-15-known-mark-v2/`](../experiments/2026-08-15-known-mark-v2/)) is a different key-free object: a surrogate used to *rewrite*, then official `score` again. It is not this classifier.

## Claude

Same protocol, different ground truth. Save `(prompt, output)` now ([`paired-corpus.md`](paired-corpus.md), `experiments/claude-premark-2026-08/`). After they *say* the mark is on, rerun the same prompts. Fit the shift. Our `score` on Claude text is the **wrong instance** even then.

Do not train that classifier on the pre-mark pile alone. There is no unmarked/marked twin yet. Claude leave-one-out waits for same-prompt marked reruns.
