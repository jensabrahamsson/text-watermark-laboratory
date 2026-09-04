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

That progression produced the repository's key result: a **key-free indicator for watermark presence**. After correcting truncated-context overcount, hard last-4 ranks held-out prompt groups **9/12** times, or **10/12** under the documented 0.02 comparison margin. Isolated hard sign is **25/48**. Occupancy-free hashing on this corpus is closed (width, seed, last-k). The pre-fix **10/12** / **29/48** stay in historical JSON; they overweighted openings. Frozen lock A on 100 new GPT-2 families is **99/100**; that does not replace **25/48**. In-family nested-by-stem Youden on that corpus is **322/400 vs 338/400** (lock A) and **392/400 vs 382/400** (lock B, occupancy). Out-of-family isolated transfer: [../research/PROTOCOL-isolated.md](../research/PROTOCOL-isolated.md) (lock A nested Youden **23/48** does not beat **25/48**; occupancy-free **16/48**; opening-overlap **18/48** covered on the original 12). Register-matched Grok-length train is [../research/PROTOCOL-isolated-register.md](../research/PROTOCOL-isolated-register.md) (lock A nested **16/48 vs 41/48**, does not beat **25/48**). Headlines vs ablations: [../research/results-ledger.md](../research/results-ledger.md). Next corpus Phase B: [../research/PROTOCOL-next.md](../research/PROTOCOL-next.md). Longer-context two-grain lock: [../research/PROTOCOL-next-longctx.md](../research/PROTOCOL-next-longctx.md) (`ngram_len=13`; Phase B interpolate **76/100** does not replace **25/48**). DistilGPT2 Hw=12 12-LOO: [../research/PROTOCOL-next-longctx-distil.md](../research/PROTOCOL-next-longctx-distil.md) (interpolate **9/12** / **49/96**; does not replace **25/48**). Qwen2-1.5B Hw=12 12-LOO: [../research/PROTOCOL-next-longctx-qwen.md](../research/PROTOCOL-next-longctx-qwen.md) (interpolate **4/12** / **41/96**; official first-draw **11/12**; does not replace **25/48**). DistilGPT2 Hw=12 100-family: [../research/PROTOCOL-next-longctx-distil-100.md](../research/PROTOCOL-next-longctx-distil-100.md) (interpolate **88/100** / **557/800**; does not replace **25/48**). DistilGPT2 Aaronson 12-LOO: [../research/PROTOCOL-next-aaronson-distil.md](../research/PROTOCOL-next-aaronson-distil.md) (interpolate **7/12** / isolated **0/48**; does not replace **25/48**). DistilGPT2 Aaronson 100-family: [../research/PROTOCOL-next-aaronson-distil-100.md](../research/PROTOCOL-next-aaronson-distil-100.md) (interpolate **96/100** / **601/800**; does not replace **25/48**). Qwen2-1.5B Aaronson 12-LOO: [../research/PROTOCOL-next-aaronson-qwen.md](../research/PROTOCOL-next-aaronson-qwen.md) (interpolate **12/12** / isolated **12/48**; does not replace **25/48**). Kirchenbauer mixin freeze: [../research/PROTOCOL-next-kgw.md](../research/PROTOCOL-next-kgw.md) (`--mixin kgw`; original-12 interpolate **12/12** / **85/96**; 100-family interpolate **100/100** / **747/800**; does not replace **25/48**).

## Main runs

| Directory | Experiment | Result |
|---|---|---|
| `2026-09-03-pair-12x4-kgw/` | Hugging Face Kirchenbauer defaults, original 12 | official z>3 **48/48** marked; Hub SHA pinned |
| `2026-09-03-probe-12x4-kgw-hard-last4/` | 12-LOO hard/interpolate on those twins | interpolate and hard **12/12**; isolated interpolate **85/96** |
| `2026-09-03-atoms-12x4-kgw/` | 12-LOO interpolate occupancy, Kirchenbauer | **114** seen vs **12071** unseen; LRs match interpolate holdout |
| `2026-09-03-pair-100x4-kgw/` | Same mixin, 100 one-liners | official first-draw z>3 **100/100** |
| `2026-09-03-probe-100x4-kgw-hard-last4/` | 100-LOO hard/interpolate | interpolate **100/100** (isolated **747/800**); hard **62/100** |
| `2026-09-03-atoms-100x4-kgw/` | 100-LOO interpolate occupancy, Kirchenbauer | **4557** seen vs **96991** unseen |
| `claude-sample-2026-09-03/` | Same 40 PROMPTS on claude.ai | 40 long texts; vs pre-mark last-4 **35/40**; not a Claude detector |
| `2026-09-03-pair-distil-12x4-kgw/` | DistilGPT2 Kirchenbauer, original 12 | official z>3 **12/12** |
| `2026-09-03-probe-distil-12x4-kgw-hard-last4/` | 12-LOO on those twins | interpolate **12/12** / **85/96**; hard **11/12** |
| `2026-09-03-atoms-distil-12x4-kgw/` | Distil Kirchenbauer occupancy | **130** seen vs **11972** unseen |
| `2026-09-03-pair-distil-100x4-kgw/` | DistilGPT2 Kirchenbauer, 100 one-liners | official first-draw z>3 **100/100** |
| `2026-09-03-probe-distil-100x4-kgw-hard-last4/` | Distil 100-LOO hard/interpolate | interpolate **100/100** / **683/800**; hard **82/100** |
| `2026-09-03-atoms-distil-100x4-kgw/` | Distil Kirchenbauer 100-family occupancy | **16170** seen vs **71541** unseen |
| `2026-09-03-pair-qwen-12x4-kgw/` | Qwen2-1.5B Kirchenbauer, original 12 | official z>3 **12/12** |
| `2026-09-03-probe-qwen-12x4-kgw-hard-last4/` | 12-LOO on those twins | interpolate **12/12** / **68/96**; hard **8/12** |
| `2026-09-03-atoms-qwen-12x4-kgw/` | Qwen Kirchenbauer occupancy | **84** seen vs **12108** unseen |
| `2026-09-04-pair-qwen-100x4-kgw/` | Qwen2-1.5B Kirchenbauer, 100 one-liners | freeze SHA `ed9fb20`; named before generation |
| `2026-09-03-probe-12x4-headline-windows-absolute/` | Absolute-history 12-LOO mask-*k* | prefixes equal reindexed; hard tails **9/12**; interpolate 8:128 rose 3→4 |
| `2026-09-03-pair-12x4-ngram13/` | Public keys, `ngram_len=13`, original 12 | official **48/48** marked above 0.55 |
| `2026-09-03-probe-12x4-ngram13-hard-last4/` | 12-LOO hard/interpolate on those twins | interpolate and hard **6/12**; isolated hard **52/96** |
| `2026-09-03-atoms-12x4-ngram13/` | 12-LOO interpolate occupancy, Hw=12 | **160** seen vs **12026** unseen; LRs match interpolate holdout |
| `2026-09-03-atoms-12x4-public-loo/` | 12-LOO interpolate occupancy, public Hw=4 | **269** seen vs **11912** unseen; every window above Hw=12 |
| `2026-09-03-pair-100x4-ngram13/` | Same mixin, 100 one-liners | official **400/400** marked above 0.55 |
| `2026-09-03-probe-100x4-ngram13-hard-last4/` | 100-LOO hard/interpolate | interpolate **76/100** (below lock A **99/100**); isolated **489/800** |
| `2026-09-04-probe-100x4-ngram13-windows/` | Hw=12 interpolate/hard/hits windows | interpolate 0:4 **86/100**; 64:128 **50/100**, AUC **0.501** |
| `2026-09-04-probe-100x4-public-w64-128/` | Public Hw=4 interpolate 64:128 | **93/100**, AUC **0.726**; full-file still **99/100** |
| `2026-09-03-atoms-100x4-ngram13/` | 100-LOO interpolate occupancy, Hw=12 | **5878** seen vs **95624** unseen; LRs match interpolate holdout |
| `2026-09-03-atoms-100x4-public-loo/` | 100-LOO interpolate occupancy, public Hw=4 | **10158** seen vs **91353** unseen; every window above Hw=12 |
| `2026-09-04-pair-distil-12x4-ngram13/` | DistilGPT2, public keys, `ngram_len=13`, original 12 | official first-draw **12/12** above 0.55 |
| `2026-09-04-probe-distil-12x4-ngram13-hard-last4/` | Distil Hw=12 12-LOO hard/interpolate | interpolate **9/12** / **49/96**; hard **6/12** |
| `2026-09-04-atoms-distil-12x4-ngram13/` | Distil Hw=12 interpolate occupancy | **175** seen vs **11994** unseen |
| `2026-09-04-pair-distil-100x4-ngram13/` | DistilGPT2, public keys, `ngram_len=13`, 100 one-liners | official first-draw **98/100** above 0.55 |
| `2026-09-04-probe-distil-100x4-ngram13-hard-last4/` | Distil Hw=12 100-LOO hard/interpolate | interpolate **88/100** / **557/800**; hard **89/100** |
| `2026-09-04-atoms-distil-100x4-ngram13/` | Distil Hw=12 100-family occupancy | **11182** seen vs **85493** unseen |
| `2026-09-04-pair-qwen-12x4-ngram13/` | Qwen2-1.5B, public keys, `ngram_len=13`, original 12 | official first-draw **11/12** above 0.55 |
| `2026-09-04-probe-qwen-12x4-ngram13-hard-last4/` | Qwen Hw=12 12-LOO hard/interpolate | interpolate **4/12** / **41/96**; hard **4/12** |
| `2026-09-04-atoms-qwen-12x4-ngram13/` | Qwen Hw=12 interpolate occupancy | **65** seen vs **12127** unseen |
| `2026-09-04-pair-qwen-100x4-ngram13/` | Qwen2-1.5B, public keys, `ngram_len=13`, 100 one-liners | official first-draw **91/100** above 0.55 |
| `2026-09-04-probe-qwen-100x4-ngram13-hard-last4/` | Qwen Hw=12 100-LOO hard/interpolate | interpolate **76/100** / **474/800**; hard **74/100** |
| `2026-09-04-atoms-qwen-100x4-ngram13/` | Qwen Hw=12 100-family occupancy | **3535** seen vs **98064** unseen |
| `2026-09-04-pair-distil-12x4-aaronson/` | DistilGPT2 Aaronson, original 12 | official first-draw z>3 **12/12** |
| `2026-09-04-probe-distil-12x4-aaronson-hard-last4/` | Distil Aaronson 12-LOO hard/interpolate | interpolate **7/12** / **0/48**; hard **7/12** / **56/96** |
| `2026-09-04-atoms-distil-12x4-aaronson/` | Distil Aaronson interpolate occupancy | **196** seen vs **11996** unseen |
| `2026-09-04-pair-distil-100x4-aaronson/` | DistilGPT2 Aaronson, 100 one-liners | official first-draw z>3 **71/100** |
| `2026-09-04-probe-distil-100x4-aaronson-hard-last4/` | Distil Aaronson 100-LOO hard/interpolate | interpolate **96/100** / **601/800**; hard **91/100** |
| `2026-09-04-atoms-distil-100x4-aaronson/` | Distil Aaronson 100-family occupancy | **28824** seen vs **61305** unseen |
| `2026-09-04-pair-qwen-12x4-aaronson/` | Qwen2-1.5B Aaronson, original 12 | official first-draw z>3 **12/12** |
| `2026-09-04-probe-qwen-12x4-aaronson-hard-last4/` | Qwen Aaronson 12-LOO hard/interpolate | interpolate **12/12** / **60/96**; hard **12/12** / **72/96** |
| `2026-09-04-atoms-qwen-12x4-aaronson/` | Qwen Aaronson interpolate occupancy | **457** seen vs **11735** unseen |
| `2026-09-04-pair-qwen-100x4-aaronson/` | Qwen2-1.5B Aaronson, 100 one-liners | official first-draw z>3 **99/100** |
| `2026-09-04-probe-qwen-100x4-aaronson-hard-last4/` | Qwen Aaronson 100-LOO hard/interpolate | interpolate **100/100** / **616/800**; hard **97/100** |
| `2026-09-04-atoms-qwen-100x4-aaronson/` | Qwen Aaronson 100-family occupancy | **8750** seen vs **92842** unseen |
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
| `2026-09-01-blind-12x4-recount-last4/` | Truncated-context recount, last-4 | **9/12** (station, office, ferry-queue miss) |
| `2026-09-01-blind-12x4-recount-last4-margin/` | Same LRs, 0.02 margin | **10/12** (ferry-queue flips) |
| `2026-09-01-probe-12x4-recount-hard-last4/` | Rechecked hard last-4 + interpolate | hard **9/12**, isolated **25/48 vs 22/48**, AUC **0.590**; interpolate still **7/12** |
| `2026-09-01-probe-12x4-recount-hits/` | Rechecked hits | **10/12**, AUC **0.718**, **28/48 vs 31/48** |
| `2026-09-01-probe-12x4-recount-opening-poshits/` | Opening poshits after recount | **9/12**, **23/48 vs 48/48** |
| `2026-09-01-probe-12x4-recount-opening-rankpath/` | Opening rankpath + first symbol | **11/12**, isolated **41/48 vs 35/48** |
| `2026-09-01-probe-36x4-recount-hits/` | Rechecked 36×4 hits | still **36/36**, AUC **0.930** |
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
| `2026-09-01-probe-12x4-fitprefix4-hashtok/` | In-domain `--fit-prefix 4` occupancy-free hashing | tokhits **23/48 vs 48/48** (prompt **12/12**); hashtok **24/48 vs 47/48** (letter d3 extra; nested **23/48 vs 47/48**); hashtok2 **22/48 vs 48/48**; marked recall below recounted hard **25/48**; sparse like tokhits, not rankpath **41/48** |
| `2026-09-01-probe-12x4-hashtok-nhashes2/` | In-domain hashtok `--n-hashes 2` | **11/12**, **34/48 vs 31/48**, nested **28/48 vs 37/48**, AUC **0.764**; best nested spec among dense widths; not 29/48 |
| `2026-09-01-probe-12x4-hashtok-nhashes4/` | In-domain hashtok `--n-hashes 4` | **11/12**, **36/48 vs 30/48**, nested **35/48 vs 30/48**; densest t=0; do not sell 36/48 |
| `2026-09-01-probe-12x4-hashtok-nhashes16/` | In-domain hashtok `--n-hashes 16` | **11/12**, **36/48 vs 22/48**, nested **29/48 vs 24/48**; letter d2 `lr>0` here only; letter prompt still loses |
| `2026-09-01-probe-12x4-hashtok-nhashes32/` | In-domain hashtok `--n-hashes 32` | **10/12**, **30/48 vs 26/48**, nested **21/48 vs 38/48**; wider than default hurts |
| `2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes2/` | 24 new topics → 12×4 hashtok n=2 | **10/12**, **29/48 vs 32/48**, nested Youden **17/48 vs 44/48**; in-domain n=2 win does not transfer |
| `2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes4/` | 24 new topics → 12×4 hashtok n=4 | **9/12**, **31/48 vs 30/48**, nested Youden **19/48 vs 41/48**; densest OOD t=0, worst nested spec |
| `2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/` | 24 new topics → 12×4 hashtok n=8 | **11/12**, **29/48 vs 35/48**, nested Youden **17/48 vs 46/48**; default wins OOD; keep CLI n=8 |
| `2026-09-01-probe-12x4-hashtok-nhashes2-seeds/` | In-domain hashtok n=2/8 mixer-seed sweep | n=2 spec **21–31/48**; default seed 20260831 is a lucky n=2 mixer; n=8 seed 7 nested **28/48 vs 37/48**; not a width law |
| `2026-09-01-transfer-36x4-to-12x4-hashtok-seeds/` | 24→12 hashtok mixer-seed sweep | n=8 default **11/12** nested **17/48 vs 46/48** is a lucky mixer; n=2 seed 7 nested **19/48 vs 47/48**; do not fish a seed |
| `2026-09-01-probe-12x4-hashtok-k1/` | In-domain hashtok last-1 | **5/12**, AUC **0.507**, **22/48 vs 22/48**, nested **9/48 vs 42/48**; chance |
| `2026-09-01-probe-12x4-hashtok-k2/` | In-domain hashtok last-2 | **9/12**, AUC **0.585**, **27/48 vs 28/48**, nested **19/48 vs 32/48**; ranking not a 5% test |
| `2026-09-01-probe-12x4-hashtok-k3/` | In-domain hashtok last-3 | **11/12**, **24/48 vs 36/48**, nested **22/48 vs 40/48**; sparser than last-4 **33/48** and below recounted hard **25/48** |
| `2026-09-01-transfer-36x4-to-12x4-hashtok-k1/` | 24 new topics → 12×4 hashtok last-1 | **7/12**, nested Youden **18/48 vs 45/48**, nested FPR10 **8/48 vs 46/48**; not last-4 |
| `2026-09-01-transfer-36x4-to-12x4-hashtok-k2/` | 24 new topics → 12×4 hashtok last-2 | **10/12**, AUC **0.738**, **29/48 vs 36/48**, nested Youden **15/48 vs 45/48**; ranking is not isolated classification |
| `2026-09-01-prompts-100/` | Confirmatory 100 one-line scenes | Committed before `pair`; disjoint from 36-topic seeds; see PROTOCOL-next.md |
| `2026-09-01-pair-100x4/` | GPT-2 twins, 100 prompts × 4 draws × 128 tokens | Official first-draw **100/100**; key-free analysis frozen in PROTOCOL-next.md |
| `2026-09-01-probe-100x4-hard-last4/` | Lock A interpolate last-4 | **99/100**, AUC **0.898**, isolated 352/400 vs 290/400 (miss stem 088) |
| `2026-09-01-probe-100x4-opening-poshits/` | Lock B opening poshits | **100/100**, AUC **0.980**, isolated 393/400 vs 344/400 |
| `2026-09-01-probe-100x4-opening-rankpath/` | Lock C opening rankpath | **96/100**, AUC **0.822**, isolated 314/400 vs 302/400 |
| `2026-09-01-probe-100x4-hard-windows/` | Lock A interpolate windows | reindexed 0:4 **99/100** AUC **0.885**; reindexed 16:32 **89/100** AUC **0.689** |
| `2026-09-01-probe-100x4-hard-windows-absolute/` | Absolute-history H2 remasure | 0:4 **99/100** AUC **0.885**; 16:32 **87/100** AUC **0.695**; paired McNemar **86/13/1/0**; not **25/48** |
| `2026-09-02-pair-12x4-control-as-marked/` | Constructed second-key twins (control-gen as marked) | Seeds 20260931 vs 0; not a matched `pair()` run |
| `2026-09-02-probe-12x4-control-as-marked-hard-last4/` | Second-key lock A interpolate last-4 | **7/12**, isolated **30/48 vs 25/48**, AUC **0.590**; H-xkey-iso fails as a raw count; not **25/48** |
| `2026-09-01-pair-distil-100x4/` | DistilGPT2 twins, same 100 prompts | Official first-draw **70/100** (weaker lamp than GPT-2 **100/100**) |
| `2026-09-01-probe-distil-100x4-opening-poshits/` | Distil lock B | persist **89/100**; strict `>` recount **88 wins + 1 tie**, AUC **0.713**, isolated 216/400 vs 247/400 |
| `2026-09-01-probe-distil-100x4-opening-rankpath/` | Distil lock C | persist **69/100**; strict `>` recount **68 wins + 1 tie**, AUC **0.598**, isolated 164/400 vs 270/400 |
| `2026-09-01-pair-qwen-100x4/` | Qwen2-1.5B twins, same 100 prompts | Official first-draw **100/100** (local HF; mixin on) |
| `2026-09-01-probe-qwen-100x4-opening-poshits/` | Qwen lock B | **95/100**, AUC **0.873**, isolated 333/400 vs 308/400 |
| `2026-09-01-probe-qwen-100x4-opening-rankpath/` | Qwen lock C | **84/100**, AUC **0.706**, isolated 275/400 vs 259/400 |
| `2026-09-01-transfer-100x4-to-12x4-hard-last4/` | 100 families → original 12×4 lock A | **8/12**, nested Youden **23/48 vs 38/48** (does not beat **25/48**) |
| `2026-09-01-transfer-100x4-to-12x4-opening-poshits/` | 100 families → original 12×4 lock B | **11/12**, nested Youden **36/48 vs 42/48**; occupancy-free **16/48 vs 48/48** |
| `2026-09-01-transfer-100x4-to-36x4-hard-last4/` | 100 families → 36×4 lock A | **36/36**, nested Youden **109/144 vs 122/144** |
| `2026-09-01-transfer-100x4-to-36x4-opening-poshits/` | 100 families → 36×4 lock B | **35/36**, nested Youden **134/144 vs 129/144**; occupancy-free **114/144 vs 139/144** |
| `2026-09-01-openings-100x4-to-12x4/` | Opening-overlap bound, 100→12 | postokhits covered **18/48**, exact **14/48**, decided 16/0 |
| `2026-09-01-openings-100x4-to-36x4/` | Opening-overlap bound, 100→36 | postokhits covered **117/144**, exact **103/144**, decided 114/5 |
| `2026-09-01-transfer-100x4-to-12x4-opening-rankpath/` | 100 families → original 12×4 lock C | **10/12**, nested Youden **24/48 vs 41/48**; losses letter/garden; 3 ranking wins have 0 isolated TPs |
| `2026-09-01-transfer-100x4-to-36x4-opening-rankpath/` | 100 families → 36×4 lock C | **35/36**, nested Youden **109/144 vs 117/144**; only miss library |
| `2026-09-01-ranking-isolated-honesty/` | Ranking vs isolated TP on frozen holdouts | 12-LOO hard: garden ranks with 0 TP; 5/25 TPs on ranking losses |
| `2026-09-01-blind-12x4-ranking-honesty/` | Same 9/12 producer, per-file LRs | **9/12**, garden 0/4, isolated **25**; historical recount JSON unchanged |
| `2026-09-01-prompts-grok12/` | Grok-register isolated-train prompts | Frozen before `pair`; [PROTOCOL-isolated-register.md](../research/PROTOCOL-isolated-register.md) |
| `2026-09-01-pair-grok12x4/` | Those seeds × 4 draws × 128 tokens | official first-draw **12/12** |
| `2026-09-01-transfer-grok12x4-to-12x4-hard-last4/` | Grok-register → original 12×4 lock A | **5/12**, nested **16/48 vs 41/48**; H-reg-A fails |
| `2026-09-01-transfer-grok12x4-to-12x4-opening-poshits/` | Same train, lock B | **7/12**, nested **6/48 vs 47/48** |
| `2026-09-01-transfer-grok12x4-to-12x4-opening-rankpath/` | Same train, lock C | **10/12**, t=0 **22/48**; nested 45/48 vs 22/48 is not a detector |
| `2026-09-01-transfer-grok12x4-to-12x4-occupancy-free/` | Same tables, postokhits | t=0 **5/48 vs 47/48**; 9 occupancy-free 0=0 ties (not ranking wins) |
| `2026-09-01-openings-grok12x4-to-12x4/` | Opening-overlap, Grok-register → 12 | covered **5/48**, exact **0/48** |
| `2026-09-01-probe-grok12x4-hard-last4/` | In-family interpolate on new 12 | **11/12**, nested-by-stem **24/48 vs 40/48** |
| `2026-09-01-transfer-grok12x4-to-36x4-hard-last4/` | Grok-register → 36×4 lock A | **24/36**, nested **50/144 vs 115/144** |
| `2026-09-01-transfer-100x4-to-grok12x4-hard-last4/` | 100 one-liners → Grok-register lock A | **11/12**, nested **22/48 vs 41/48**; H-xreg-A holds vs 16/48; not **25/48** |
| `2026-09-01-transfer-100x4-to-grok12x4-opening-poshits/` | Same train, lock B | **10/12**, nested **36/48 vs 44/48** (occupancy) |
| `2026-09-01-transfer-100x4-to-grok12x4-opening-rankpath/` | Same train, lock C | **8/12**, nested **10/48 vs 41/48** |
| `2026-09-01-transfer-100x4-to-grok12x4-occupancy-free/` | Same tables, postokhits | t=0 **0/48 vs 48/48**; 4 ranking wins with 0 TP, 6 occupancy 0=0 ties |
| `2026-09-01-openings-100x4-to-grok12x4/` | Opening-overlap, 100→Grok-register | covered **5/48**, exact **0/48**; t=0 is 0/48 |
| `2026-09-01-transfer-100x4-to-grok12x4-hard-windows/` | Same interpolate, token windows | 0:4 **7/12**; tail 32:64 and 64:128 **9/12**; reindexed; not **25/48** |
| `2026-09-01-transfer-100x4-to-12x4-hard-windows/` | 100→original 12 interpolate windows | 0:4 **9/12**; 16:32 **6/12**; front-loaded on that split; reindexed |
| `2026-09-02-transfer-100x4-to-grok12x4-hard-windows-absolute/` | Same interpolate, absolute history | 0:4 **7/12**; 32:64 **10/12** (rose vs **9/12**); 64:128 **9/12**; not **25/48** |
| `2026-09-02-transfer-100x4-to-12x4-hard-windows-absolute/` | 100→original 12 absolute windows | 0:4 **9/12**; 16:32 **6/12**; 64:128 fell 8→6; not **25/48** |
| `2026-09-01-atoms-100x4-to-grok12x4-interpolate/` | Decode lock A interpolate atoms | backoff mass; `'The'→' car'` n=19; occupancy-free **0/48**; not **25/48** |
| `2026-09-01-prompts-grok36/` | 36 Grok-length scene seeds | Frozen before `pair`; see PROTOCOL-isolated-scale |
| `2026-09-01-pair-grok36x4/` | GPT-2 twins, 36 Grok-length × 4 | Official first-draw **36/36** |
| `2026-09-01-transfer-grok36x4-to-grok12x4-hard-last4/` | 36 Grok-length → grok12 lock A | **12/12**, nested **36/48 vs 39/48**; not **25/48** |
| `2026-09-01-transfer-grok36x4-to-grok12x4-occupancy-free/` | Same tables, postokhits | t=0 **39/48 vs 45/48** = coverage **39/48** |
| `2026-09-01-openings-grok36x4-to-grok12x4/` | Opening-overlap, 36 Grok → grok12 | covered **39/48**, exact **21/48**; 3 FP |
| `2026-09-01-transfer-grok36x4-to-12x4-hard-last4/` | 36 Grok-length → original 12 lock A | **10/12**, nested **26/48 vs 33/48**; occupancy-free **10/48**; not **25/48** |
| `2026-09-01-atoms-grok36x4-to-12x4-interpolate/` | Decode those interpolate atoms | backoff; `'Cl'→'osing'` n=4 unbucketed; nested **26/48** ≠ occupancy-free **10/48** |
| `2026-09-01-atoms-grok36x4-to-grok12x4-interpolate/` | Decode grok36→grok12 interpolate atoms | 0:4 `'The'→' car'` n=19 = occupancy-free **39/48**; tail backoff |
| `2026-09-01-openings-union-100-and-grok36-to-12x4/` | Published-zero coverage union | disjoint **28/48**; leftover 20; not mixed tables |
| `2026-09-01-openings-100plusgrok36-to-12x4/` | Mixed extra-train openings | coverage **28/48** = union; leftover 20 |
| `2026-09-01-transfer-100plusgrok36-to-12x4-occupancy-free/` | Mixed postokhits | t=0 **26/48 vs 47/48**; two covered letter files negative |
| `2026-09-01-transfer-100plusgrok36-to-12x4-hard-last4/` | Mixed interpolate | nested **27/48 vs 39/48**; not **25/48** |
| `2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath/` | Mixed lock C on leftover 20 | leftover **12/20 vs 14/20**; full **35/48** not leftover; not **25/48** |
| `2026-09-01-isolated-split-25-leftover-vs-covered/` | Decode 25/48 on leftover vs covered | leftover **10/20 vs 11/20**, covered **15/28**; leftover chance; not **25/48** |
| `2026-09-01-probe-12x4-headline-windows/` | 12-LOO hard/interpolate mask-*k* | hard 0:4 **5/12**, tails **9/12**; interpolate tails **5/12** then **3/12**; not **25/48** |
| `2026-09-01-isolated-split-windows-leftover-vs-covered/` | Leftover vs covered on mask-*k* hard | 4:128 leftover **11/20 vs 11/20**, covered **16/28**; leftover chance; not **25/48** |
| `2026-09-01-isolated-leftover-bound/` | Occupancy leftover-20 official+atoms | official **20/20** at 128; leftover 0:4 unseen 99 vs 21; interpolate **13/20**; not **25/48** |
| `2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4/` | Leftover-20 ∪ SMT openings | union **30/48** equals SMT; leftover **18**; last-4 **10/18 vs 10/18**; not **25/48** |
| `2026-09-01-openings-union-distil100x4-and-smt-to-12x4/` | Distil ∪ SMT openings | union **33/48**; leftover **15**; last-4 **9/15 vs 8/15**; Distil-only office; not **25/48** |
| `2026-09-01-pair-gpt2-medium-100x4/` | gpt2-medium twins, same 100 prompts | official first-draw **100/100**; [PROTOCOL-isolated-mgen.md](../research/PROTOCOL-isolated-mgen.md) |
| `2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits/` | gpt2-medium → original 12 occupancy-free | postokhits t=0 **16/48 vs 48/48**; prompt **7/12** (5 ties); not **25/48** |
| `2026-09-01-openings-gpt2-medium-100x4-to-12x4/` | Opening-overlap, gpt2-medium → 12 | covered **16/48** (exact 14/48); leftover-15 **0/15**; not **25/48** |
| `2026-09-01-isolated-mgen-leftover-15/` | Leftover-15 gpt2-medium slice | leftover coverage **0/15**; leftover sign **0/15 vs 15/15**; not **25/48** |
| `2026-09-01-pair-gpt2-medium-12x4/` | gpt2-medium original-12 twins | official first-draw **12/12**; [PROTOCOL-isolated-m12.md](../research/PROTOCOL-isolated-m12.md) |
| `2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits/` | gpt2-medium 100×4 → gpt2-medium 12×4 occupancy-free | postokhits t=0 **10/48 vs 48/48**; prompt **8/12** (3 ties); not **25/48** |
| `2026-09-01-openings-gpt2-medium-100x4-to-medium12x4/` | Opening-overlap, gpt2-medium → medium 12 | covered **13/48** (exact 10/48); t=0 **10/48**; not **25/48** |
| `2026-09-01-transfer-distil100x4-to-medium12x4-opening-poshits/` | Distil 100×4 → gpt2-medium 12×4 occupancy-free | postokhits t=0 **20/48 vs 48/48**; prompt **11/12** (1 tie); not **25/48** |
| `2026-09-01-openings-distil100x4-to-medium12x4/` | Opening-overlap, Distil → medium 12 | covered **22/48** (exact 4/48); t=0 **20/48**; not **25/48** |
| `2026-09-01-transfer-gpt2-medium-100x4-to-distil12x4-opening-poshits/` | gpt2-medium 100×4 → Distil 12×4 occupancy-free | postokhits t=0 **3/48 vs 47/48**; prompt **6/12** (6 ties); not **25/48** |
| `2026-09-01-openings-gpt2-medium-100x4-to-distil12x4/` | Opening-overlap, gpt2-medium → Distil 12 | covered **5/48** (exact 2/48); t=0 **3/48**; not **25/48** |
| `2026-09-01-isolated-leftover-18-readers/` | Leftover-18 remaining readers | rankpath **12/18 vs 13/18**; interpolate **12/18 vs 12/18**; 0:4 unseen 89 vs 19; not **25/48** |
| `2026-09-01-isolated-xgen-leftover-18/` | Distil occupancy-free leftover-18 | leftover **3/18** (office); Distil postokhits **22/48 vs 43/48**; not **25/48** |
| `2026-09-01-transfer-distil100x4-to-distil12x4-opening-poshits/` | Distil 100×4 → Distil 12×4 occupancy-free | postokhits **16/48 vs 39/48**; poshits **25/48 vs 25/48**; not **25/48** |
| `2026-09-01-openings-distil100x4-to-distil12x4/` | Distil→Distil opening overlap | covered **16/48** (exact 9/48); equals t=0; not **25/48** |
| `2026-09-01-transfer-qwen100x4-to-qwen12x4-opening-poshits/` | Qwen 100×4 → Qwen 12×4 occupancy-free | postokhits **31/48 vs 48/48**; poshits **33/48 vs 37/48**; not **25/48** |
| `2026-09-01-openings-qwen100x4-to-qwen12x4/` | Qwen→Qwen opening overlap | covered **37/48** (exact 12/48); t=0 **31/48**; not **25/48** |
| `2026-09-01-probe-grok36x4-hard-last4/` | In-family interpolate on new 36 | **35/36**, nested-by-stem **93/144 vs 110/144** |

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
- Opening-only unmarked-LM geometry (generated tokens 1–3) beats the published 128-token pivot in-domain (**27/48** vs **17/48**) but **does not transfer** (OOD LDA 15/48, AUC 0.422). Rank-path tables on the same openings transfer: in-domain **11/12 / 41/48 vs 35/48** after the truncated-context recount (pre-fix 12/12 / 41/48), OOD **10/12 / 28/48** (15 unmarked FPs). Unbucketed full-file rank-path is chance (8/12, AUC 0.559); window 16:32 is chance, as with hits. A matched prefix of four rank symbols transfers **11/12** with isolated **25/48 vs 43/48** (5 unmarked FPs). 60-stem prefix-4 as a standalone reader is **10/12**, **28/48 vs 40/48** (same 68/96 combined). Native Distil opening rankpath is chance (**8/12**, AUC **0.579**) despite official 12/12; Qwen opening rankpath is **8/12** against first-token **12/12**. Coverage-then-pivot cascade is an honest two-channel report: in-domain 36/48 with unmarked FPs; combined 60-stem train covers **42/48** of which **34/48** have `lr>0` (precision 1.0 among decided); cascade 39/48 spends 15 unmarked FPs. Full-file rankpath fallback on that train is 38/48 with 17 unmarked FPs. `--cascade-when positive` on the prefix-4 leftover rows is **40/48 vs 40/48** (5 of 8 covered-negative ferry openings plus 1 leftover zero; 8 unmarked FPs; combined 80/96 vs count 82/96). Do not sell cascade 39/48, rankpath 41/48, or prefix-4 25/48 as beating poshits 39/48 or replacing 25/48. Isolated prefix-5 rankpath is weaker (**11/12**, 30/48) and still misses letter d2: the official 5-gram `Now in the second I` has isolated GPT-2 rank 41 and prompt rank 11. 60-stem prefix-5 `hashpool` signs that file via Laplace (0/8 hashes saw `I`); `hashtok` abstains. `indicate score` prints **ABSTAIN** at `n_used=0`. Prefix-5 `hashtokbackoff` t=0 is **38/48 vs 35/48**, but nested Youden stays **30/48**; letter d2's official `I` is last-1 unmarked (δ=−1.10), and hashtokbackoff2's 0.694 is tokens 1–2. On the published prefix-4 opening, hashed backoff **hurts** versus hashtok (**31/48** vs **35/48**). Do not sell 38/48, 36/48, or 35/48 as beating poshits 39/48. Mixed backoff library ×4 extras are 3-token prefixes hashed into the order-4 mixer (`order > i`). `hashtoklen` / `hashtoklenbackoff` hash only exact last-k: prefix-5 hashtoklen **21/48** (official 5-gram slot); exact backoff nested Youden **33/48 vs 42/48**; letter d2 backoff2 is last-2 `'Now in' → ' the'`, not `I`. Occupancy-free drop-one skip-grams (`hashskip`) are denser at t=0 (**25/48 vs 35/48**) and **worse** nested (**16/48 vs 41/48**): letter d2's official `I` is seen unmarked-only. `hashtoklen2` skips singleton hash collisions: **10/48 vs 48/48**, precision 1.0, nested matching t=0; 11 of 21 hashtoklen TPs were singletons; harbour d2 survives (c_m=11). Count-weighting hashes by `c_m+c_u` keeps that uniform 21/48 (rain d1 mixes n=7 with n=8; no singleton+dense mix). Rebound hashtoklen2 onto prefix-4 rankpath is **28/48 vs 40/48** (same as standalone rankpath). Occupancy-free MASK replace (`hashmask`) is **21/48 vs 42/48** at t=0 and nested Youden **19/48 vs 45/48**, worse than hashtoklen; letter d2's official `I` is two opposing singletons (lr=+0.240). In-domain full-file `hashtok` is **33/48 vs 22/48**, nested-by-stem **22/48 vs 30/48** (hashpool stays **35/48**). OR with hard last-4 indicate is **39/48 vs 12/48**, combined **51/96** (worse than indicate 52/96); nested LDA **21/48 vs 37/48**. `tokhybrid` copies that isolated 33/48 (prompt 11/12). `poshashtok` nested **14/48 vs 38/48**. `hashtokgap` is **27/48 vs 21/48**, nested **17/48 vs 31/48** (strict subset of hashtok). `hashtok2` is **34/48 vs 21/48**, nested **19/48 vs 35/48** (sign reshuffle, not a singleton core). In-domain `--fit-prefix 4` occupancy-free hashing copies tokhits density: tokhits **23/48 vs 48/48** (prompt **12/12**); hashtok **24/48 vs 47/48** (nested **23/48 vs 47/48**, extra TP letter d3); hashtok2 **22/48 vs 48/48**. Letter d2 is zero at that grain. Marked isolated recall **24/48** is below recounted hard last-4 **25/48**. Not opening rankpath **41/48**. In-domain full-file `--n-hashes` on hashtok: n=2 is **34/48 vs 31/48**, nested **28/48 vs 37/48**, AUC **0.764**; n=4 is **36/48 vs 30/48**, nested **35/48 vs 30/48**; n=16 copies 36/48 with nested spec **24/48**; n=32 hurts (**30/48**, nested **21/48 vs 38/48**). Default n=8 (**33/48 vs 22/48**) is not the best width on that in-domain gate at seed 20260831, and that n=2 win is seed-confounded (spec 21–31/48); 24→12 nested Youden prefers n=8 (**11/12**, **29/48 vs 35/48**, nested **17/48 vs 46/48**). Occupancy-free last-k at that frozen mixer: in-domain last-1 is chance (**5/12**, AUC **0.507**); last-3 prompt **11/12** has t=0 **24/48** (below recounted hard **25/48**) and nested spec **40/48**; 24→12 last-4 still wins prompt ranking and nested FPR10 (**17/48 vs 46/48**); last-2 file AUC **0.738** is ranking (nested **15/48**); last-1 nested **18/48** has prompt **7/12**. Keep `--context-len 4`. Do not sell 39/48, 36/48, 35/48, 34/48, 33/48, 31/48, 28/48, 27/48, 25/48, 24/48, 23/48, 22/48, 21/48, 19/48, 18/48, 17/48, 16/48, 11/48, or 10/48 as beating poshits 39/48 or replacing 25/48.

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
