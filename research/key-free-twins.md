# Key-free watermark indication from matched generations

## Result

We have built a **key-free indicator for watermark presence**.

The indicator is trained on matched marked/unmarked generations from the same prompts and then evaluated on held-out prompts. It does not use the watermark keys, `hash_iv`, g-values, or DeepMind's `detector_mean` to make the held-out decision.

Current results (truncated-context recount; pre-fix **10/12** / **29/48**
stay in historical JSON):

| Experiment | Result |
|---|---|
| Official public-key detector, 12 prompts | **12/12** |
| Key-free, 12 prompts × 1 draw | **8/12** |
| Key-free, 12 prompts × 4 draws, last-4 | **9/12** |
| Same LRs with 0.02 comparison margin | **10/12** |
| Key-free `hits` (shared 4-grams only) | **10/12**, AUC **0.718** |
| Key-free hashpool | **11/12**, isolated **35/48** |
| Key-free hashpool, 36 GPT-2 topics | **31/36**, AUC **0.877** |
| Key-free hashpool, Qwen 12×1 | **10/12**, isolated **11/12** |
| Key-free hits, train 24 other topics → 12×4 files | isolated **39/48**, AUC **0.769** |
| Nested hashpool Youden on that split | **33/48** marked, **34/48** unmarked |
| Key-free hits, 24×4 new stems → 12×4 | **12/12** ranking, isolated **42/48**, AUC **0.793** |
| Nested hits Youden, 4-draw train | **26/48** vs **44/48** |
| Nested hits FPR10, 12×4 → 36×4 | **83/96** vs **85/96** |
| Key-free hits, 36 topics × 4 draws LOO | **36/36**, AUC **0.930** |
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
| Single held-out marked file, hard `lr > 0` | **25/48** |
| Opening poshits `--fit-prefix 4 --pos-bucket 1` (recount) | **9/12**, isolated **23/48 vs 48/48** |
| Opening rankpath, 12×4 LOO 4-token (recount) | **11/12**, isolated **41/48 vs 35/48** |
| Opening occupancy-free hashtok, `--fit-prefix 4` | **12/12**, isolated **24/48 vs 47/48** (tokhits **23/48**; marked recall below **25/48**; not rankpath **41/48**) |
| In-domain full-file hashtok | **9/12**, isolated **33/48 vs 22/48**, nested **22/48 vs 30/48** |
| In-domain hashtok `--n-hashes` | n=2 **11/12** / **34/48 vs 31/48** nested **28/48 vs 37/48** at seed 20260831; n=4 **36/48 vs 30/48**; n=32 hurts **30/48** |
| In-domain hashtok n=2 seed sweep | n=2 spec **21–31/48**; default seed is a lucky mixer; not a width law |
| Transfer hashtok `--n-hashes`, 24→12 | n=8 **11/12** / nested **17/48 vs 46/48** at seed 20260831; n=2 seed 7 nested **19/47**; keep frozen protocol; do not fish a seed |
| In-domain hashtok last-k | last-1 chance **5/12**; last-3 **11/12** / **24/48 vs 36/48** nested **22/40**; keep last-4 |
| Transfer hashtok last-k, 24→12 | last-4 **11/12** nested FPR10 **17/46**; last-2 AUC **0.738** nested **15/45**; last-1 nested **18/45** prompt **7/12** |

The recounted last-4 count table is **9/12** (isolated **25/48**). Pre-fix **10/12** / **29/48** stay in historical JSON. Stronger readers of the same twins, out-of-family transfer, and a key-free argmax snap are in [key-free-probe.md](key-free-probe.md). Instance contrast against `control-shuffled-30` is in [key-free-contrast.md](key-free-contrast.md). Occupancy Laplace versus observed next tokens, tokbackoff, and the opening-overlap bound are in [key-free-tokhits.md](key-free-tokhits.md). Occupancy-free hashing is in [key-free-hashtok.md](key-free-hashtok.md). Opening-only unmarked-LM geometry and coverage-then-pivot ABSTAIN are in [key-free-cascade.md](key-free-cascade.md). Rank-symbol tables that score novel openings without token identity are in [key-free-rankpath.md](key-free-rankpath.md). Neighbours of this measurement, with author–year citations, are in [related-work.md](related-work.md) ([CITING.md](CITING.md)).

That is enough to establish a useful statistical signal under the tested conditions. It is not enough to treat every isolated paragraph as reliably classifiable. Occupancy-free hashing on these twins is closed; prompt-grain confirmation is [PROTOCOL-next.md](PROTOCOL-next.md); out-of-family isolated-file transfer is [PROTOCOL-isolated.md](PROTOCOL-isolated.md) (100→12 lock A nested Youden **23/48 vs 38/48**, does not beat **25/48**; occupancy-free lock B **16/48**; lock C **24/48 vs 41/48**, losses letter/garden; opening-overlap bound **18/48** covered; 100→36 lock A **109/144 vs 122/144**). Register-matched Grok-length train is [PROTOCOL-isolated-register.md](PROTOCOL-isolated-register.md) (lock A nested **16/48 vs 41/48**, does not beat **25/48**; occupancy-free coverage **5/48**). Reverse 100 one-liners → Grok-register 12 is [PROTOCOL-isolated-xreg.md](PROTOCOL-isolated-xreg.md) (lock A nested **22/48 vs 41/48**; occupancy-free **0/48**, coverage **5/48**; original 12 are not uniquely cursed). Window readout is [PROTOCOL-isolated-windows.md](PROTOCOL-isolated-windows.md): that 11/12 rank is not front-loaded (0:4 **7/12**; tail **9/12**). The `atoms` decode of those tables is almost all Witten–Bell backoff; occupancy-free openings stay **0/48**; observed-token hits are `'The' → ' car'` and GPT-2 dialogue templates (`experiments/2026-09-01-atoms-100x4-to-grok12x4-interpolate/`). Do not sell `The car`. Thirty-six Grok-length families are [PROTOCOL-isolated-scale.md](PROTOCOL-isolated-scale.md): grok12 occupancy-free **39/48** equals coverage; original-12 lock A nested **26/48 vs 33/48**; occupancy-free **10/48**. The `atoms` decode of those interpolate tables is still mostly Witten–Bell backoff (`experiments/2026-09-01-atoms-grok36x4-to-12x4-interpolate/`, `experiments/2026-09-01-atoms-grok36x4-to-grok12x4-interpolate/`). Original-12 nested **26/48** is not occupancy-free **10/48** (library `'Cl' → 'osing'` is an unbucketed body copy). Grok12 0:4 is opening overlap (`'The' → ' car'` n=19). Do not sell `Closing` or `The car`. Isolated observed-token recall is still opening-atom overlap. Published occupancy-free zeros of 100 one-liners and grok36 on the original 12 are disjoint (union **28/48**); mixed extra-train coverage equals that union and occupancy-free t=0 is **26/48** ([PROTOCOL-isolated-pool.md](PROTOCOL-isolated-pool.md)). Mixed leftover rankpath is leftover **12/20 vs 14/20** ([PROTOCOL-isolated-leftover.md](PROTOCOL-isolated-leftover.md)). In-domain **25/48** splits leftover **10/20 vs 11/20** and occupancy-covered **15/28 vs 11/28** ([PROTOCOL-isolated-split.md](PROTOCOL-isolated-split.md)); leftover last-4 is chance. Do not sell 39/48, 26/48, 28/48, 10/20, or 15/28. Ranking and isolated sign disagree on stems of the 12-LOO hard headline: garden ranks with 0 isolated TPs; ferry-queue, station, and office lose ranking with 5 of 25 TPs ([ranking-isolated-honesty](../experiments/2026-09-01-ranking-isolated-honesty/)). `blind` leave-one-prompt-out now prints that split; historical recount JSON stays stem-mean only. Live JSON: `experiments/2026-09-01-blind-12x4-ranking-honesty/`. Headlines vs ablations: [results-ledger.md](results-ledger.md). Truncated-context recount JSON: `experiments/2026-09-01-blind-12x4-recount-last4/`.

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

With 12 prompts × 4 GPT-2 generations and a last-4 context, the held-out prompt result reaches **9/12** after storing each real suffix once.

The three misses are *station*, *office*, and *ferry-queue*.

A 0.02 comparison margin moves *ferry-queue* onto the correct side, giving **10/12**. *Station* and *office* remain misses. The pre-fix JSON still reads **10/12** / margin **11/12**; those runs overcounted truncated openings.

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

At prompt-mean grain the result is **9/12**.

At individual-file grain, however:

- marked files with `lr > 0`: **25/48**
- unmarked files with `lr <= 0`: **22/48**
- mean marked LR: **+0.023**
- mean unmarked LR: **−0.002**
- file AUC **0.590**, permutation p **0.040**; binomial P(≥25) ≈ 0.44

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
[key-free-probe.md](key-free-probe.md). After the truncated-context recount,
`hits` is **10/12** and AUC **0.718**. Hashpool does not use `_add_sequence`
and stays **11/12**, isolated **35/48**, on the 2026-08-31 JSON. They still do
not use the detector keys. The 2026-08-17 holdout files stay as collected.

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

Experiment index: [../experiments/README.md](../experiments/README.md). Those
commands now store each real suffix once. Rechecked JSON:
`experiments/2026-09-01-blind-12x4-recount-last4/` and
`experiments/2026-09-01-probe-12x4-recount-hard-last4/`. The 2026-08-17
holdout files stay as collected. New `blind` persists also store per-file
LRs and `ranking_without_isolated_tp`. The recount JSON stays stem-mean
only. On that 9/12 grain, garden ranks with no isolated TP; station,
office, and ferry-queue lose ranking but hold 5 of 25 isolated TPs.
