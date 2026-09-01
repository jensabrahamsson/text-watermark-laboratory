# Experiments

This directory contains the runs behind the results in the root [README](../README.md).

The central sequence is:

```text
known public mark
      ↓
verify with official score
      ↓
generate matched marked/unmarked twins
      ↓
throw the keys away
      ↓
fit key-free token/context statistics
      ↓
evaluate held-out prompts
```

That progression produced the repository's key result: a **key-free indicator for watermark presence**, reaching **10/12** held-out prompts on the 12×4 GPT-2 corpus and **11/12** under the documented 0.02 comparison margin.

## Main runs

| Directory | Experiment | Result |
|---|---|---|
| `2026-08-15-gpt2-sonnet5/` | Known public mark before/after Sonnet edits | marked 0.617/0.638; proofread 0.605/0.625; rewrite 0.502/0.502 |
| `2026-08-15-known-mark-v2/` | Key-free rewrite surrogate, then official measurement | ~0.62 → ~0.50 |
| `claude-premark-2026-08/` | Control corpus collected before announced marking condition | 40 A/B texts plus auxiliary files |
| `claude-mark-2026-08-19/` | Same prompts on claude.ai after a rumored live mark | **37/40**; usage limit; `assumed_watermark=rumored` |
| `2026-08-19-claude-rumor-twins/` | Premark vs 19a, 37 prompts | last-1 **28/37**; last-4 **24/37** |
| `claude-sample-2026-08-19b/` | Same-day second pass | **40/40** |
| `2026-08-19-claude-sameday-twins/` | 19a vs 19b | last-1 **19/38**; last-4 **19/38** |
| `2026-08-17-grok-prompts/` | Seed prompts | reference input |
| `2026-08-17-blind-pairs/` | 12 GPT-2 marked/unmarked prompt pairs | official detector: **12/12** |
| `2026-08-17-blind/` | First key-free leave-one-out run | **8/12** |
| `2026-08-17-blind-limit/` | Same seeds, longer generations | **6/12** |
| `2026-08-17-pair-qwen/` | Qwen2-1.5B matched twins | official **12/12** |
| `2026-08-17-blind-qwen-k2/` | Key-free Qwen, last-2 | **10/12** |
| `2026-08-17-pair-36/` | More topics | official 36/36; blind 22/36 |
| `2026-08-17-pair-12x4/` | 12 prompts × 4 GPT-2 samples | corpus for higher-context indicator |
| `2026-08-17-blind-12x4-k4/` | Key-free last-4 | **10/12** |
| `2026-08-17-indicate-holdout-12x4/` | Rotate, fit 11 prompts, score held-out files | prompt grain **10/12**, single marked file **29/48** |
| `2026-08-17-indicate-holdout-12x4-margin02/` | Same LRs, 0.02 comparison margin | prompt grain **11/12** |
| `2026-08-31-probe-12x4/` | Key-free scorer comparison on the same 12×4 twins | `hits` **11/12** AUC **0.737**; hashpool **11/12** isolated **35/48** |
| `2026-08-31-probe-36/` | Same scorers on 36 GPT-2 topics × 1 | hashpool **31/36** AUC **0.877**; hard last-4 **20/36** |
| `2026-08-31-probe-qwen/` | Qwen2-1.5B 12×1, Qwen tokenizer | hashpool **10/12** AUC **0.750**; hits AUC **0.417** |
| `2026-08-31-scrub-12x4/` | Key-free argmax snap, official `score` as reference | **0.622 → 0.499** on 48 marked files |
| `2026-08-31-transfer-36-to-12x4/` | Train 24 new topics, score 12×4 files | hits isolated **39/48** AUC **0.769**; hashpool **11/12** |
| `2026-08-31-transfer-12x4-to-36/` | Train 12×4, score stems 13–36 | hits **24/24** AUC **0.986**; hashpool **23/24** |
| `2026-08-31-transfer-nested-36-to-12x4/` | Same split, nested Youden / FPR10 | hashpool **33/48** + **34/48**; hitmass **10/12** |
| `2026-08-31-transfer-nested-12x4-to-36/` | Reverse split, nested thresholds | freqhits **23/24** + **23/24** |
| `2026-08-31-transfer-shuffle-36-to-12x4/` | 50% train-label shuffle | isolated 19–20/48; not a detector |
| `2026-08-31-probe-surface-12x4/` | UTF-8 surface + logit on 12×4 LOO | surface **10/12** AUC 0.602 |
| `2026-08-31-transfer-surface-36-to-12x4/` | OOD surface/logit nested | surface 9/12; nested hashpool still 33/48 vs 34/48 |
| `2026-08-31-probe-surface-qwen/` | Qwen byte hashpool LOO | surface **9/12** AUC 0.674 |
| `2026-08-31-transfer-gpt2-to-qwen/` | Same-topic GPT-2 → Qwen | hits **11/12** paired; isolated 1/12 |
| `2026-08-31-transfer-36-to-qwen/` | New GPT-2 topics → Qwen | chance |
| `2026-08-31-pair-36x4/` | 36 GPT-2 prompts × 4 draws × 128 tokens | official first-draw **36/36** |
| `2026-08-31-probe-36x4/` | LOO on that corpus | hits **36/36** AUC **0.934**; nested-by-stem **119/144** vs **134/144** |
| `2026-08-31-probe-36x4-draws1/` | `--max-draws 1` ablation | hits **30/36** AUC 0.845 |
| `2026-08-31-probe-36x4-draws2/` | `--max-draws 2` ablation | hits **33/36** AUC 0.875 |
| `2026-08-31-transfer-36x4-to-12x4/` | 24×4 new stems → 12×4 | hits **12/12**, isolated **42/48**; nested Youden 26/48 vs 44/48 |
| `2026-08-31-transfer-12x4-to-36x4/` | 12×4 → 96 new-topic files | hits **24/24**; nested FPR10 **83/96** vs **85/96** |
| `2026-08-31-pair-qwen-12x4/` | Qwen 12×4 new sample | official first-draw **12/12** |
| `2026-08-31-probe-qwen-12x4/` | Qwen tokenizer LOO | hits **8/12** AUC 0.602; extra draws do not close the gap |
| `2026-08-31-transfer-gpt2-to-qwen-12x4/` | GPT-2 tables → new Qwen sample | hits **5/12**; 11/12 did not replicate |
| `2026-08-31-stack-12x4/` | LOO LDA of hits+hashpool file scores | **11/12**, AUC 0.732, unmarked ≤0 **44/48** |
| `2026-08-31-probe-36x4-prefixes/` | Token prefixes on 36×4 LOO | 16-token hits **34/36** AUC **0.916**; 128 matches 36/36 |
| `2026-08-31-transfer-36x4-to-12x4-prefixes/` | New-topic prefix curve | 16-token hits **11/12** AUC 0.752; nested-by-stem 25/48 vs 29/48 |
| `2026-08-31-probe-36x4-windows/` | Disjoint token windows, 36×4 LOO | 0:16 hits **34/36** AUC 0.916; 16:32 near chance (22/36, 0.549) |
| `2026-08-31-transfer-36x4-to-12x4-windows/` | New-topic windows | 0:16 hits **11/12**; 16:32 chance (8/12, AUC 0.512) |
| `2026-08-31-probe-36x4-k5/` | `context_len=5` on 36×4 | hits **35/36** AUC 0.912; does not beat last-4 |
| `2026-08-31-transfer-36x4-to-qwen-12x4/` | 24×4 GPT-2 → new Qwen | chance (hits **6/12**, AUC 0.445) |
| `2026-08-31-transfer-gpt2-surface-to-qwen-12x4/` | Same-topic byte table → new Qwen | **7/12**, AUC 0.525, isolated 5/48 |
| `2026-08-31-probe-36x4-fitprefix16/` | Matched 16-token fit, 36×4 LOO | hits **34/36** AUC **0.929**; unmarked ≤0 **112/144** |
| `2026-08-31-probe-36x4-posbucket/` | Position-bucketed last-4, 36×4 LOO | poshits **34/36**; t=0 spec **97/144** (hits 76/144) |
| `2026-08-31-probe-12x4-posbucket/` | Position-bucketed last-4, 12×4 LOO | poshits 10/12; specificity knob 24/48 vs 37/48 |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix16/` | New-topic matched 16-token fit | hits **11/12** AUC **0.818**; nested-by-stem 39/48 vs 36/48 |
| `2026-08-31-transfer-36x4-to-12x4-posbucket/` | New-topic poshits | **10/12** AUC **0.811**; nested-by-stem 37/48 vs 35/48 |
| `2026-08-31-probe-36x4-fitprefix16-pos4/` | Matched 16-token poshits, bucket 4 | **34/36** AUC **0.937**; unmarked ≤0 **114/144** |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos4/` | New-topic matched 16-token poshits bucket 4 | **11/12** AUC **0.820**; nested-by-stem 39/48 vs 38/48 |
| `2026-08-31-probe-36x4-coverage/` | Shared last-k by window, 36×4 LOO | 0:16 **13.7%** (i=1–2); full last-4 from i=4 ~4% |
| `2026-08-31-probe-12x4-coverage/` | Same on 12×4 | 0:16 **6.5%** vs 16:32 **1.0%** |
| `2026-08-31-probe-36x4-windows-opening/` | Hits windows 0:4 vs 4:16 | **0:4 = 0:16** at **34/36** / **0.917** |
| `2026-08-31-transfer-36x4-to-12x4-windows-opening/` | New-topic 0:4 vs 4:16 | **0:4 = 0:16** at **11/12** / **0.752** |
| `2026-08-31-probe-36x4-fitprefix4-pos1/` | Matched 4-token poshits bucket 1 | **34/36** AUC **0.935**; t=0 **131/144 vs 132/144** |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix4-pos1/` | New-topic matched 4-token poshits | **12/12** AUC **0.873**; nested Youden **39/48 vs 41/48** |
| `2026-08-31-probe-36x4-fitprefix16-pos-sweep/` | Buckets 1/2/4/8 on 16-token poshits | bucket 1 t=0 **132/144 vs 132/144** |
| `2026-08-31-probe-36x4-fitprefix16-poshitmass/` | Matched 16-token poshitmass bucket 4 | **34/36** AUC **0.943** |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix16-poshitmass/` | New-topic poshitmass bucket 4 | **11/12** AUC **0.831**; nested FPR10 39/48 vs 38/48 |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos1/` | New-topic 16-token poshits bucket 1 | **12/12** AUC **0.873**; t=0 **39/48 vs 41/48** |
| `2026-08-31-probe-12x4-fitprefix16-pos1/` | 12×4 LOO, 16-token bucket 1 | 9/12; 23/48 (not 29/48) |
| `2026-08-31-transfer-36x4-to-qwen-fitprefix16-pos1/` | GPT-2 → Qwen, 16-token bucket 1 | chance (8/12, AUC 0.516) |
| `2026-08-31-probe-36x4-fitprefix4-k1-pos1/` | Matched 4-token last-1 poshits | **34/36** AUC **0.940** |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix4-k1-pos1/` | New-topic last-1 poshits | **12/12** AUC **0.873**; t=0 **39/48 vs 41/48** |
| `2026-08-31-probe-36x4-fitprefix4-include-first/` | 4-token include-first | in-domain **35/36**; OOD hurts |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix4-include-first/` | New-topic include-first | 9/12, AUC 0.719 |
| `2026-08-31-probe-36x4-fitprefix4-prompt-context/` | Mixin-aligned prompt last-k | 34/36, AUC 0.784 |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix4-prompt-context/` | New-topic prompt last-k | **12/12** ranking, isolated 13/48 |
| `2026-08-31-probe-qwen-12x4-fitprefix4-pos1/` | Qwen opening; token 0 via `first` | **first 12/12** AUC **0.901**; hits 7/12 |
| `2026-08-31-probe-qwen-12x4-fitprefix4-include-first/` | Qwen opening include-first | hits=first **12/12** AUC **0.901** |
| `2026-08-31-transfer-36x4-to-qwen-fitprefix4-include-first/` | GPT-2 → Qwen first-token | chance |
| `2026-08-31-pair-distilgpt2-12x4/` | DistilGPT2 12×4 twins | official **12/12** |
| `2026-08-31-probe-distilgpt2-12x4/` | Distil in-domain last-4 | hits **9/12** AUC 0.705 |
| `2026-08-31-transfer-36x4-to-distilgpt2-12x4/` | GPT-2 → Distil, same tokenizer | hits **5/12** AUC **0.462** |
| `2026-08-31-learn-36x4-to-12x4-fitprefix4/` | Tiny nets on the 4-token OOD gate | tokmlp 8/12 AUC 0.714; does **not** beat poshits **0.873** |
| `2026-08-31-learn-36x4-fitprefix4/` | 36×4 LOO learned scorers | hashlog 34/36 AUC 0.864 (poshits 0.935) |
| `2026-08-31-learn-12x4-fitprefix4/` | 12×4 LOO learned scorers | hashlog 11/12 in-family; OOD is 7/12 |
| `2026-08-31-probe-12x4-fitprefix4-pos1/` | 12×4 LOO 4-token poshits | **9/12**, 23/48 vs 48/48 |
| `2026-08-31-learn-36x4-to-distil-fitprefix4/` | GPT-2 nets → Distil | chance (tokmlp 8/12, AUC 0.559) |
| `2026-08-31-learn-36x4-to-qwen-fitprefix4/` | GPT-2 nets → Qwen | chance (charcnn AUC 0.496) |
| `2026-08-31-learn-qwen-12x4-fitprefix4-include-first/` | Qwen in-domain include-first | hashlog **12/12**, AUC 0.826 (below `first` 0.901) |
| `2026-08-31-learn-36x4-to-12x4-shuffle/` | 50% train-stem shuffle | tokmlp 5/12; hashlog/charcnn do not collapse |
| `2026-08-31-pair-12x4-controlkeys/` | GPT-2 12×4 `control-shuffled-30` only | official public **0.501**; matching **0.624** |
| `2026-08-31-contrast-36x4-to-12x4-fitprefix4/` | 4-token poshits vs other instance | control `lr>0` **0/48**; public vs control **12/12**, AUC **0.906** |
| `2026-08-31-contrast-36x4-to-12x4-full/` | Full 128-token contrast | poshits still **0/48**; unbucketed hits control **29/48** `lr>0` |
| `2026-08-31-contrast-36x4-to-limit-fitprefix4/` | 4-token contrast on 12×1×700 | poshits control **0/12** `lr>0`; public vs control **12/12** |
| `2026-08-31-contrast-36x4-to-limit-full/` | Full 700-token contrast | hits public vs control AUC **1.000**; control vs unmarked 0.556 |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits/` | Occupancy vs observed next token | poshits **39/48**; postokhits **16/48** precision **1.000** |
| `2026-08-31-probe-36x4-fitprefix4-postokhits/` | 36×4 LOO postokhits | 34/36, **122/144 vs 132/144** (9 of 131 TPs were occupancy) |
| `2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokhits/` | postokhits vs control-shuffled-30 | control `lr>0` **0/48** |
| `2026-08-31-prompts-long12/` | Twelve ~41–51 word new-topic pair seeds | not copies of the original 12; not Claude |
| `2026-08-31-pair-long12x4/` | Those seeds × 4 draws × 128 tokens | official first-draw **12/12**; token 0 is only `"` / `The` |
| `2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokhits/` | Medium new topics → 12×4 | postokhits **12/12**, isolated **19/48**, precision **1.000**; poshits 8/12 (The-Laplace flips) |
| `2026-08-31-transfer-short24-plus-long12-to-12x4-fitprefix4-tokhits/` | 24 short + 12 medium → 12×4 | postokhits **12/12**, isolated **20/48**, precision **1.000**; nine zeros remain |
| `2026-08-31-pair-24short-plus-long12/` | Hardlink train dir (README only in git) | rebuild from `pair-36x4` stems 13–36 + `pair-long12x4` |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokbackoff/` | tokbackoff on short-train OOD gate | copies postokhits **16/48** |
| `2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokbackoff/` | tokbackoff, medium → 12×4 | **21/48**, +2 harbour via `' was' → ' in'` |
| `2026-08-31-transfer-short24-plus-long12-to-12x4-fitprefix4-tokbackoff/` | tokbackoff, short+medium → 12×4 | **22/48**, same two harbour files |
| `2026-08-31-probe-36x4-fitprefix4-postokbackoff/` | 36×4 LOO tokbackoff | 122/144 marked; one extra unmarked FP vs postokhits |
| `2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokbackoff/` | tokbackoff vs control-shuffled-30 | control `lr>0` **0/48** |
| `2026-08-31-prompts-tails12/` | Tail-transplant seeds (new bodies, 12×4 last paragraphs) | not copies of the original 12 as wholes |
| `2026-08-31-pair-tails12x4/` | Those seeds × 4 draws | official **12/12**; token 0 mostly `The`; no Closing |
| `2026-08-31-transfer-tails12x4-to-12x4-fitprefix4-tokbackoff/` | Tail train → 12×4 | postokhits **10/48**; postokbackoff **23/48**; precision **1.000** |
| `2026-08-31-transfer-short-medium-tails-to-12x4-fitprefix4-tokbackoff/` | short+medium+tails → 12×4 | postokhits **30/48**; postokbackoff **36/48**, AUC **0.888**; precision **1.000** |
| `2026-08-31-pair-short-medium-tails/` | Hardlink train dir (README only in git) | rebuild from 36x4 13–36 + long12 + tails12 |
| `2026-08-31-probe-12x4-fitprefix4-cascade-isolated/` | Opening pivot + cascade, 12×4 LOO | opening LDA **10/12** **27/48**; cascade 36/48 not calibrated |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix4-cascade-isolated/` | Opening pivot/cascade, short → 12×4 | postokbackoff **16/48** precision **1.0**; LDA AUC **0.422** |
| `2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-isolated/` | 60-stem train → 12×4 cascade | **42 covered / 34 `lr>0`**; cascade 39/48 precision 0.722 |
| `2026-08-31-probe-12x4-fitprefix4-rankpath-isolated/` | Rank-path opening, 12×4 LOO | **12/12**, **41/48**, AUC **0.797** |
| `2026-08-31-transfer-36x4-to-12x4-fitprefix4-rankpath-isolated/` | Rank-path, short → 12×4 | **10/12**, **28/48**; LDA 4/12 |
| `2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-rankpath-isolated/` | 60-stem rank-path → 12×4 | rankpath **12/12**; rankuni 37/48 (17 FP) |
| `2026-08-31-probe-12x4-rankpath-full-isolated/` | Unbucketed full-file rank-path, 12×4 LOO | full **8/12** AUC 0.559; prefix-4 **10/12** / 0.718; 16:32 chance |
| `2026-08-31-transfer-36x4-to-12x4-rankpath-full-isolated/` | Same slices, short → 12×4 | full 6/12; prefix-4 **11/12**, **25/48 vs 43/48** |
| `2026-08-31-transfer-short-medium-tails-family-to-12x4-rankpath-full-cascade/` | 60-stem count + full rankpath fallback | 42/34 count; cascade 38/48 (4/6 leftover zeros, 17 FP) |
| `2026-08-31-contrast-36x4-to-12x4-fitprefix4-rankpath/` | Opening rankpath vs control-shuffled-30 | rankpath control AUC **0.498**, **17/48** `lr>0`; rankuni **30/48** |
| `2026-08-31-contrast-36x4-to-12x4-prefix4-rankpath/` | Unbucketed prefix-4 rankpath vs control | public **11/12** **25/48 vs 43/48**; control AUC **0.511**, **6/48** |
| `2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/` | 60-stem count + prefix-4 rankpath fallback | 42/34 count; leftover **1/6**; cascade **35/48 vs 43/48** |
| `2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4-when-positive/` | Same rows, `--cascade-when positive` | **40/48 vs 40/48** (5 of 8 covered-negatives; 8 FP) |
| `2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath/` | Distil native opening rankpath | **8/12**, AUC **0.579** (chance; official 12/12) |
| `2026-08-31-probe-distilgpt2-12x4-prefix4-rankpath/` | Distil native prefix-4 rankpath | **7/12**, AUC 0.563 |
| `2026-08-31-transfer-36x4-to-distilgpt2-fitprefix4-rankpath/` | GPT-2 rankpath → Distil, GPT-2 LM | **9/12**, AUC 0.636, isolated **21/48** |
| `2026-08-31-probe-qwen-12x4-fitprefix4-rankpath/` | Qwen native opening rankpath | **8/12**, AUC **0.590** (first-token stays 12/12) |
| `2026-08-31-probe-qwen-12x4-prefix4-rankpath/` | Qwen native prefix-4 rankpath | **9/12**, AUC **0.662**, isolated 25/48 |
| `2026-08-31-transfer-short-medium-tails-family-to-12x4-prefix4-rankpath/` | 60-stem prefix-4 standalone → 12×4 | **10/12**, **28/48 vs 40/48** (same 68/96 as 24-short) |
| `2026-09-01-probe-12x4-fitprefix4-snaprate/` | Table-free opening snap-rate | `snapupset` chance **7/12** AUC **0.501**; `snapmiss` **10/12** **21/48** |
| `2026-09-01-probe-12x4-prefix4-snaprate/` | Table-free prefix-4 snap-rate | `snapupset` chance **6/12**; `snapmiss` t=0 is 2/48 |
| `2026-09-01-official-prefix-leftover/` | Official means on leftover 8 (keys, reference) | prefix-16 leftover **8/8 >0.55**, mean 0.627 |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-rankpath/` | 60-stem prefix-8 → 12×4 | postokbackoff **38/48 vs 40/48**; 20/38 TPs last-1 only |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-backoff2/` | Same train, last-2+ only | postokbackoff2 **18/48 vs 46/48**; four "rescues" abstain |
| `2026-09-01-letter-d2-first-ngram/` | Official 5-gram vs isolated/prompt ranks (keys on official) | letter d2 isolated rank **41**, prompt **11**, official **0.733** |
| `2026-09-01-probe-12x4-fitprefix5-rankpath/` | In-domain prefix-5 rankpath + token-4 window | **11/12**, **30/48 vs 36/48**; fifth-token rankuni **4/12** |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtok/` | 60-stem prefix-5 hashpool vs hashtok | hashpool **34/48** occupancy; hashtok **30/48** equals postokhits; letter d2 `n_used=0` |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtokbackoff/` | 60-stem prefix-5 per-order hashed backoff | hashtokbackoff **38/48 vs 35/48**; nested Youden **30/48**; letter d2 fifth is last-1 unmarked |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtokbackoff/` | 60-stem prefix-4 hashed backoff | hashtok **35/48 vs 39/48**; backoff **hurts** (**31/48 vs 33/48**) |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen/` | 60-stem prefix-5 exact-length hashed backoff | hashtoklen **21/48** (harbour d2 collision extra); hashtoklenbackoff nested Youden **33/48**; letter d2 backoff2 is last-2 not `I` |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen-cascade-rankpath/` | Occupancy-free hashed 5-gram + prefix-4 rankpath cascade | **33/48 vs 37/48**; leftover eight still miss |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtoklen/` | 60-stem prefix-4 exact-length hashed backoff | hashtoklen **0/48** (no last-4); exact backoff **35/48** (mixed had hurt: 31/48) |
| `2026-09-01-probe-12x4-fitprefix5-hashtoklen/` | In-domain 12×4 LOO prefix-5 hashtoklen | **7/48 vs 48/48**; harbour d2 already a TP; letter d2 zero |
| `2026-09-01-probe-distilgpt2-12x4-fitprefix5-hashtoklen/` | Native Distil prefix-5 hashtoklen | **7/48 vs 48/48**; official Distil still **12/12** |
| `2026-09-01-transfer-short-medium-tails-family-to-distil-prefix5-hashtoklen/` | GPT-2 60-stem hashtoklen → Distil 12×4 | hashtoklen **10/48**, AUC **0.571**; backoff chance |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashskip/` | 60-stem prefix-5 occupancy-free drop-one skip-grams | hashskip t=0 **25/48 vs 35/48**; nested Youden **16/48 vs 41/48**; letter d2 sees `I` unmarked |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2/` | 60-stem prefix-5 occupancy-free min_count=2 | hashtoklen2 **10/48 vs 48/48** (11/21 TPs were singletons); hashskip2 nested **15/48 vs 41/48** |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2-cascade-rankpath/` | hashtoklen2 + saved prefix-4 rankpath | coverage **28/48 vs 40/48** (copies rankpath; leftover 0/8) |
| `2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashmask/` | 60-stem prefix-5 occupancy-free MASK replace | hashmask t=0 **21/48 vs 42/48**; nested Youden **19/48 vs 45/48** (worse than hashtoklen); letter d2 official slot is two opposing singletons |
| `2026-09-01-probe-12x4-hashtok/` | In-domain 12×4 full-file occupancy-free hashing | hashtok **33/48 vs 22/48**; nested-by-stem **22/48 vs 30/48**; hashpool stays **35/48 vs 29/48** |
| `2026-09-01-probe-12x4-hashtok-indicate-or/` | Saved-holdout OR / coverage / nested LDA of indicate × hashtok | OR **39/48 vs 12/48** combined **51/96** (worse than indicate 52/96); nested LDA **21/48 vs 37/48**; do not sell 39/48 |
| `2026-09-01-probe-12x4-tokhybrid-poshashtok/` | In-domain tokhybrid / poshashtok | tokhybrid copies hashtok **33/48 vs 22/48** (prompt **11/12**); poshashtok nested **14/48 vs 38/48** |
| `2026-09-01-probe-12x4-hashtokgap/` | In-domain hashtok residual of unseen n-grams | hashtokgap **27/48 vs 21/48**, nested **17/48 vs 31/48**; strict subset of hashtok 33 (lost 6, gained 0) |
| `2026-09-01-probe-12x4-hashtok2/` | In-domain unbucketed min_count=2 | hashtok2 **34/48 vs 21/48**, nested **19/48 vs 35/48**; sign reshuffle (lost 3, gained 4), not a singleton core |
| `2026-09-01-probe-12x4-fitprefix4-hashtok/` | In-domain `--fit-prefix 4` occupancy-free hashing | tokhits **23/48 vs 48/48** (prompt **12/12**); hashtok **24/48 vs 47/48** (letter d3 extra; nested **23/48 vs 47/48**); hashtok2 **22/48 vs 48/48**; sparse like tokhits, not rankpath **41/48** |

## What changed across the runs

The early 8/12 result showed that token-level structure was present.

The later runs clarified what strengthens it:

- simply making generations longer did not help the hard scorer;
- simply adding more topics did not help the **hard** last-1/last-4 scorer (22/36, 20/36);
- **repeated draws from the same prompts did help** that scorer, because they create reusable higher-order contexts;
- coverage-gated and hash-pool readers later showed that extra topics *do* help once unseen 4-grams are not scored as unigrams (30–31/36);
- the effect also appears with a different local generator (Qwen2-1.5B), where hashpool matches the published **10/12**.
- training on **other** prompt families is a fairer isolated-file test than leave-one-of-12-out: hits then marks **39/48** of the 12×4 files, and ranks **24/24** new 36-topic stems (specificity at 0 is still incomplete);
- nested Youden on the training stems only is the honest isolated-file gate (OOD hashpool **33/48** vs **34/48**; reverse freqhits **23/24** vs **23/24**; 4-draw reverse nested hits FPR10 **83/96** vs **85/96**);
- four extra draws at 128 tokens lift in-domain hits from **30/36** to **36/36** (nested-by-stem **119/144** vs **134/144**);
- a 16-token prefix already ranks **34/36** in-domain (AUC 0.916); tokens 16–32 scored alone are near chance (22/36, AUC 0.549);
- matching mixin `ngram_len=5` does not beat last-4;
- extra GPT-2 draws do not create a Qwen detector (36×4 → new Qwen hits 6/12);
- matching the train window to those first 16 tokens lifts unmarked ≤0 to **112/144** in-domain and OOD file AUC to **0.818**;
- position-bucketed last-4 keeps 134/144 marked at t=0 on 36×4 with unmarked ≤0 **97/144**, and raises OOD file AUC to **0.811**;
- finer buckets (4) on that 16-token window reach in-domain poshits AUC **0.937** with unmarked ≤0 **114/144**;
- shared last-k coverage on 36×4 is **13.7%** in 0:16 vs **3.9%** in 16:32, but that gap is last-1/last-2 at i=1–2;
- scoring **0:4** already ranks **34/36** (AUC **0.917**), matching 0:16;
- a matched 4-token fit with bucket 1 balances in-domain t=0 at **131/144 vs 132/144**, and OOD ranks **12/12** (AUC **0.873**, **39/48 vs 41/48**, nested Youden matching t=0);
- that isolated-file gate needs the extra topics (12×4 LOO is 9/12) and does not transfer to Qwen;
- last-1 on those four tokens copies the OOD 12/12 / 0.873 / 39 vs 41 gate, so last-4 at the opening was already truncated;
- mixing generated token 0 into hits (`--include-first`) hurts that OOD gate (9/12, AUC 0.719);
- Qwen's in-domain opening signal **is token 0** (first **12/12**, AUC **0.901**); hits without it is 7/12;
- DistilGPT2 is officially 12/12; GPT-2 36×4 hits do not transfer across the shared tokenizer (5/12, AUC 0.462);
- native Distil unmarked-LM rankpath is chance (**8/12**, AUC **0.579**) despite that working mixin; GPT-2 rankpath on Distil tokens is **9/12** / 0.636, not a Distil reader;
- Qwen native opening rankpath is **8/12** (AUC 0.590); Qwen's in-domain opening signal remains token 0 (**12/12**, AUC **0.901**);
- tiny learned scorers (hashlog / tokmlp / charcnn) do **not** beat 4-token poshits on the new-topic gate (tokmlp 8/12, AUC 0.714 vs **0.873**) and do not transfer to Distil or Qwen;
- shuffling half the training labels drops isolated sign at 0 to chance;
- a public-trained 4-token poshits table is **instance-specific** on this mixin: `control-shuffled-30` openings get `lr>0` on **0/48** files, while public vs control ranks **12/12** (AUC **0.906**). Unbucketed hits on full files is not that check (29/48 control `lr>0`). Not key recovery.
- **39/48 poshits is not 39 token preferences.** Shared `'The'` plus unequal occupancy gives every novel continuation the same δ = 0.330 (23 of 39 TPs and all 7 FPs). `postokhits` keeps observed next tokens only: **16/48**, precision 1.0 among decided, still **12/12**, and control stays **0/48**. In-domain, only 9 of 131 TPs were occupancy (122/144).
- twelve medium-length new topics lift that observed-token isolated recall to **19/48** (20/48 with the short one-liners too); the nine After / Closing / Now / While zeros stay, and The-Laplace **flips sign** on the medium train (poshits 8/12). `postokbackoff` adds two harbour files on that train (**21/48**, combined **22/48**) via last-1 `' was' → ' in'`; it copies **16/48** on the short one-liner gate. Transplanting last paragraphs from the zero-producing 12×4 seeds is **not** new-topic OOD: combined short+medium+tails postokhits **30/48**, postokbackoff **36/48** (AUC **0.888**), precision 1.0 among decided. Library still has no Closing opening in train; backoff scores those four files via `' is' → ' the'`. Letter stays zero. Do not sell 16/48–36/48 as beating 39/48.
- Opening-only unmarked-LM geometry (generated tokens 1–3) beats the published 128-token pivot in-domain (**27/48** vs **17/48**) but **does not transfer** (OOD LDA 15/48, AUC 0.422). Rank-path tables on the same openings transfer: in-domain **12/12 / 41/48**, OOD **10/12 / 28/48** (15 unmarked FPs). Unbucketed full-file rank-path is chance (8/12, AUC 0.559); window 16:32 is chance, as with hits. A matched prefix of four rank symbols transfers **11/12** with isolated **25/48 vs 43/48** (5 unmarked FPs). 60-stem prefix-4 as a standalone reader is **10/12**, **28/48 vs 40/48** (same 68/96 combined). Native Distil opening rankpath is chance (**8/12**, AUC **0.579**) despite official 12/12; Qwen opening rankpath is **8/12** against first-token **12/12**. Coverage-then-pivot cascade is an honest two-channel report: in-domain 36/48 with unmarked FPs; combined 60-stem train covers **42/48** of which **34/48** have `lr>0` (precision 1.0 among decided); cascade 39/48 spends 15 unmarked FPs. Full-file rankpath fallback on that train is 38/48 with 17 unmarked FPs. `--cascade-when positive` on the prefix-4 leftover rows is **40/48 vs 40/48** (5 of 8 covered-negative ferry openings plus 1 leftover zero; 8 unmarked FPs; combined 80/96 vs count 82/96). Do not sell cascade 39/48, rankpath 41/48, or prefix-4 25/48 as beating poshits 39/48 or replacing 29/48. Isolated prefix-5 rankpath is weaker (**11/12**, 30/48) and still misses letter d2: the official 5-gram `Now in the second I` has isolated GPT-2 rank 41 and prompt rank 11. 60-stem prefix-5 `hashpool` signs that file via Laplace (0/8 hashes saw `I`); `hashtok` abstains. `indicate score` prints **ABSTAIN** at `n_used=0`. Prefix-5 `hashtokbackoff` t=0 is **38/48 vs 35/48**, but nested Youden stays **30/48**; letter d2's official `I` is last-1 unmarked (δ=−1.10), and hashtokbackoff2's 0.694 is tokens 1–2. On the published prefix-4 opening, hashed backoff **hurts** versus hashtok (**31/48** vs **35/48**). Do not sell 38/48, 36/48, or 35/48 as beating poshits 39/48. Mixed backoff library ×4 extras are 3-token prefixes hashed into the order-4 mixer (`order > i`). `hashtoklen` / `hashtoklenbackoff` hash only exact last-k: prefix-5 hashtoklen **21/48** (official 5-gram slot); exact backoff nested Youden **33/48 vs 42/48**; letter d2 backoff2 is last-2 `'Now in' → ' the'`, not `I`. Occupancy-free drop-one skip-grams (`hashskip`) are denser at t=0 (**25/48 vs 35/48**) and **worse** nested (**16/48 vs 41/48**): letter d2's official `I` is seen unmarked-only. `hashtoklen2` skips singleton hash collisions: **10/48 vs 48/48**, precision 1.0, nested matching t=0; 11 of 21 hashtoklen TPs were singletons; harbour d2 survives (c_m=11). Count-weighting hashes by `c_m+c_u` keeps that uniform 21/48 (rain d1 mixes n=7 with n=8; no singleton+dense mix). Rebound hashtoklen2 onto prefix-4 rankpath is **28/48 vs 40/48** (same as standalone rankpath). Occupancy-free MASK replace (`hashmask`) is **21/48 vs 42/48** at t=0 and nested Youden **19/48 vs 45/48**, worse than hashtoklen; letter d2's official `I` is two opposing singletons (lr=+0.240). In-domain full-file `hashtok` is **33/48 vs 22/48**, nested-by-stem **22/48 vs 30/48** (hashpool stays **35/48**). OR with hard last-4 indicate is **39/48 vs 12/48**, combined **51/96** (worse than indicate 52/96); nested LDA **21/48 vs 37/48**. `tokhybrid` copies that isolated 33/48 (prompt 11/12). `poshashtok` nested **14/48 vs 38/48**. `hashtokgap` is **27/48 vs 21/48**, nested **17/48 vs 31/48** (strict subset of hashtok). `hashtok2` is **34/48 vs 21/48**, nested **19/48 vs 35/48** (sign reshuffle, not a singleton core). In-domain `--fit-prefix 4` occupancy-free hashing copies tokhits density: tokhits **23/48 vs 48/48** (prompt **12/12**); hashtok **24/48 vs 47/48** (nested **23/48 vs 47/48**, extra TP letter d3); hashtok2 **22/48 vs 48/48**. Letter d2 is zero at that grain. Not opening rankpath **41/48**. Do not sell 39/48, 34/48, 33/48, 28/48, 27/48, 25/48, 24/48, 23/48, 22/48, 21/48, 19/48, 16/48, or 10/48 as beating poshits 39/48 or replacing 29/48.

This is why the current result should be described as a working experimental indicator rather than merely a "promising idea".

## Reference score

```bash
source .venv/bin/activate
python -m text_watermark_tools score \
  experiments/2026-08-15-gpt2-sonnet5/t_high_temp.txt
```

## Generate twins

```bash
python -m text_watermark_tools pair \
  experiments/2026-08-17-grok-prompts \
  --out-dir experiments/2026-08-17-pair \
  --max-new-tokens 128
```

## Run the key-free indicator experiment

```bash
python -m text_watermark_tools indicate holdout \
  experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4
```

For interpretation and methodology, see [research/key-free-twins.md](../research/key-free-twins.md).

`results.md` files inside individual run directories are experiment artifacts. They should be treated as recorded output, not editorial documentation.
