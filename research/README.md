# Research notes

This directory contains the reasoning behind the experiments in the root [README](../README.md).

The locked abstract is the **shop window** ([abstract.md](abstract.md)): what is new, first. Report author line: Jens Abrahamsson, Master of Science. Do not write `thesis/`. The main result is the **key-free watermark indicator** described in [key-free-twins.md](key-free-twins.md): matched marked/unmarked generations contain enough statistical structure to classify most held-out prompt groups without using the detector keys.

Citations in these notes are author–year ([CITING.md](CITING.md)). Do not invent papers. A future research report should compile [references.bib](references.bib); do not write `thesis/` until isolated-file research is finished.

| File | Focus |
|---|---|
| [abstract.md](abstract.md) | Shop window: key-free prompt-group indicator first; isolated **25/48** in the same pane; not a theorem refutation |
| [threat-model.md](threat-model.md) | Auditor access: key-free ≠ reference-free; two grains; not field-defining; not a finished conference paper |
| [LOGBOOK.md](LOGBOOK.md) | Dated lab notes. Append after every Claude sample or measurement |
| [PROTOCOL-next.md](PROTOCOL-next.md) | Frozen confirmatory 100×4 protocol; lock A **99/100**; Distil H3 |
| [PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md) | Frozen GPT-2 Hw=12; original-12 interpolate **6/12**; 100-family interpolate **76/100**; not **25/48** |
| [PROTOCOL-next-longctx-distil.md](PROTOCOL-next-longctx-distil.md) | Frozen DistilGPT2 Hw=12 12-LOO; interpolate **9/12**, isolated **49/96**; not **25/48** |
| [PROTOCOL-next-longctx-qwen.md](PROTOCOL-next-longctx-qwen.md) | Frozen Qwen2-1.5B Hw=12 12-LOO; interpolate **4/12**, isolated **41/96**; official first-draw **11/12**; not **25/48** |
| [PROTOCOL-next-aaronson.md](PROTOCOL-next-aaronson.md) | Frozen Aaronson–Kirchner exponential-minimum; 12-LOO interpolate **11/12** isolated **56/96**; 100-family interpolate **100/100** isolated **608/800**; not **25/48** |
| [PROTOCOL-next-aaronson-distil.md](PROTOCOL-next-aaronson-distil.md) | Frozen DistilGPT2 Aaronson 12-LOO; interpolate **7/12**, isolated **0/48 vs 48/48**; not **25/48** |
| [PROTOCOL-isolated.md](PROTOCOL-isolated.md) | Frozen out-of-family isolated-file transfer of those same readers |
| [PROTOCOL-isolated-register.md](PROTOCOL-isolated-register.md) | Grok-length train → original 12; lock A nested **16/48 vs 41/48** |
| [PROTOCOL-isolated-xreg.md](PROTOCOL-isolated-xreg.md) | Reverse: 100 one-liners → Grok-register 12; lock A nested **22/48 vs 41/48** |
| [PROTOCOL-isolated-windows.md](PROTOCOL-isolated-windows.md) | 100→Grok lock A is not front-loaded (tail **9/12**; 0:4 **7/12**); reindexed; keep |
| [PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md) | Absolute-history remasure: grok12 0:4 **7/12**; 32:64 **10/12** (rose vs reindexed **9/12**); original 12 0:4 **9/12** vs 16:32 **6/12**; do not sell **10/12**; do not overwrite the reindexed dumps |
| [PROTOCOL-isolated-scale.md](PROTOCOL-isolated-scale.md) | 36 Grok-length train; grok12 occupancy-free **39/48** = coverage; original-12 nested **26/48** ≠ occupancy-free **10/48** |
| [PROTOCOL-isolated-pool.md](PROTOCOL-isolated-pool.md) | Pooled 100+grok36 mix; coverage union **28/48**; t=0 **26/48**; interpolate nested **27/48**; not **25/48** |
| [PROTOCOL-isolated-leftover.md](PROTOCOL-isolated-leftover.md) | Mixed opening rankpath leftover **12/20 vs 14/20**; do not sell full **35/48** |
| [PROTOCOL-isolated-split.md](PROTOCOL-isolated-split.md) | In-domain 25/48 = leftover **10/20 vs 11/20** + covered **15/28**; leftover chance; not **25/48** |
| [narrative.md](narrative.md) | Two-grain story lock; rejects a “key-free detection fails” title; did not refute Christ/Zhang; not `thesis/` |
| [PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md) | 12-LOO hard 0:4 **5/12**; tails **9/12**; interpolate front-loaded; not **25/48** |
| [PROTOCOL-isolated-mask-split.md](PROTOCOL-isolated-mask-split.md) | Hard 4:128 leftover **11/20 vs 11/20**, covered **16/28**; tail 9/12 not leftover recall; not **25/48** |
| [PROTOCOL-isolated-leftover-bound.md](PROTOCOL-isolated-leftover-bound.md) | Leftover-20 official **20/20** at prefix-128; leftover 0:4 atoms unseen **99 vs 21**; interpolate **13/20**; not **25/48** |
| [PROTOCOL-isolated-leftover-union.md](PROTOCOL-isolated-leftover-union.md) | Union **30/48** equals SMT; leftover **18**; last-4 **10/18 vs 10/18**; not **25/48** |
| [PROTOCOL-isolated-occupancy-closed.md](PROTOCOL-isolated-occupancy-closed.md) | Occupancy-free leftover-18 closed; official **18/18** by subset; do not add unrelated occupancy-free trains |
| [PROTOCOL-isolated-leftover-18.md](PROTOCOL-isolated-leftover-18.md) | Leftover-18 rankpath **12/18 vs 13/18**; interpolate **12/18 vs 12/18**; 0:4 unseen **89 vs 19**; not **25/48** |
| [PROTOCOL-isolated-leftover-18-closed.md](PROTOCOL-isolated-leftover-18-closed.md) | Leftover-18 published key-free readers exhausted; do not re-slice more leftover-18 holdouts |
| [PROTOCOL-isolated-xgen.md](PROTOCOL-isolated-xgen.md) | Distil occupancy-free leftover-18 **3/18** (office); Distil postokhits **22/48** beats GPT-2 occupancy-free **16/48**, not **25/48** |
| [PROTOCOL-isolated-dgen.md](PROTOCOL-isolated-dgen.md) | Distil 100×4 → Distil 12×4 occupancy-free **16/48** = coverage; not leftover-18; not **25/48** |
| [PROTOCOL-isolated-qgen.md](PROTOCOL-isolated-qgen.md) | Qwen 100×4 → Qwen 12×4 occupancy-free **31/48 vs 48/48**; coverage **37/48**; not leftover-18; not **25/48** |
| [PROTOCOL-isolated-dsmt.md](PROTOCOL-isolated-dsmt.md) | Distil ∪ SMT openings union **33/48**; leftover **15**; last-4 **9/15 vs 8/15**; not **25/48** |
| [PROTOCOL-isolated-leftover-15-closed.md](PROTOCOL-isolated-leftover-15-closed.md) | Leftover-15 occupancy-free closed; official **15/15** at prefix-5 (keys); last-4 **9/15 vs 8/15**; not **25/48** |
| [PROTOCOL-isolated-mgen.md](PROTOCOL-isolated-mgen.md) | gpt2-medium 100×4 occupancy-free leftover-15 analog; leftover **0/15**; t=0 **16/48**; not **25/48** |
| [PROTOCOL-isolated-m12.md](PROTOCOL-isolated-m12.md) | gpt2-medium 100×4 → gpt2-medium 12×4 occupancy-free **10/48** (coverage **13/48**); not leftover-15; not **25/48** |
| [PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md) | Distil→gpt2-medium occupancy-free **20/48** (coverage **22/48**); gpt2-medium→Distil **3/48** (coverage **5/48**); not leftover-15; not **25/48** |
| [PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md) | Absolute-history H2: 0:4 **99/100** vs 16:32 **87/100**; paired McNemar **86/13/1/0**; **25/48** CI includes ½; not **25/48** |
| [PROTOCOL-isolated-xkey.md](PROTOCOL-isolated-xkey.md) | Second-key in-domain lock A: interpolate **7/12**, isolated **30/48 vs 25/48**; H-xkey-iso fails as a raw count; not **25/48** |
| [key-free-twins.md](key-free-twins.md) | Key-free watermark indication from matched generations; recounted last-4 **9/12**; isolated **25/48** |
| [key-free-probe.md](key-free-probe.md) | Transfer scorers, hash pooling, unmarked-LM choice geometry, argmax snap |
| [key-free-learn.md](key-free-learn.md) | Tiny hashed logistic / token MLP / char CNN; they do not beat poshits |
| [key-free-contrast.md](key-free-contrast.md) | Public vs control-shuffled-30: 4-token poshits is instance-specific (**0/48**); prefix-4 rankpath control **6/48** |
| [key-free-tokhits.md](key-free-tokhits.md) | Occupancy Laplace vs observed next tokens: 39/48 includes The-ferry; postokhits **16/48** precision 1.0; opening-overlap last-2+ core **13/48** |
| [key-free-hashtok.md](key-free-hashtok.md) | Occupancy-free hashpool: prefix-5 hashtok **30/48**; hashtoklen **21/48** with harbour d2 the one collision extra; hashtoklen2 **10/48 vs 48/48** (11/21 TPs were singletons); hashskip nested **16/48**; hashmask nested **19/48 vs 45/48** (worse than hashtoklen); hashtoklen2+rankpath cascade copies rankpath **28/48**; in-domain full-file hashtok **33/48 vs 22/48**; `--n-hashes 2` **34/48 vs 31/48** nested **28/48 vs 37/48** (AUC **0.764**); `--n-hashes 4` **36/48 vs 30/48** nested **35/48 vs 30/48**; `--n-hashes 16` 36/48 nested spec **24/48**; `--n-hashes 32` hurts **30/48** nested **21/48 vs 38/48**; default n=8 is not the best in-domain width at seed 20260831; that n=2 win is seed-confounded (spec **21–31/48**); 24→12 nested Youden prefers n=8 **17/48 vs 46/48** at seed 20260831 (keep frozen protocol; n=2 seed 7 nested **19/47**; do not fish a seed); do not sell 36/48 or 31/48; OR with indicate **39/48 vs 12/48** combined 51/96 (not a detector); tokhybrid copies that 33/48 (prompt 11/12); poshashtok nested **14/48 vs 38/48**; hashtokgap **27/48 vs 21/48** (strict subset of hashtok; nested **17/48 vs 31/48**); hashtok2 **34/48 vs 21/48** (sign reshuffle, nested **19/48 vs 35/48**); opening-grain `--fit-prefix 4` hashtok **24/48 vs 47/48** (tokhits ⊂ hashtok; extra TP letter d3; nested **23/48 vs 47/48**; marked recall below **29/48**), not rankpath **41/48**; Distil transfer AUC **0.571** |
| [related-work.md](related-work.md) | Narrative related work; no theorem refutation of Christ/Zhang; author–year |
| [annotated-bibliography.md](annotated-bibliography.md) | Critical annotations (what each source is, and is not, for this lab) |
| [references.bib](references.bib) | Canonical BibTeX |
| [CITING.md](CITING.md) | Author–year convention; measurements vs indications vs theorems |
| [key-free-cascade.md](key-free-cascade.md) | Coverage-then-fallback: ABSTAIN at n_used=0; `--cascade-when positive` 40/48 vs 40/48; leftover 8 officially marked; letter d2 5-gram isolated-rank invisible; prefix-8 extra TPs are last-1 |
| [key-free-rankpath.md](key-free-rankpath.md) | Rank-symbol tables: GPT-2 opening 41/48; Distil native **8/12** chance; Qwen opening rankpath **8/12** |
| [key-free-snaprate.md](key-free-snaprate.md) | Table-free leave/upset/miss: opening `snapupset` chance **7/12**; `snapmiss` **10/12** / **21/48** |
| [how-synthid-works.md](how-synthid-works.md) | How the public SynthID-Text reference implementation hashes, samples, and scores |
| [invertibility.md](invertibility.md) | Why the key-free result is not key recovery |
| [claude.md](claude.md) | Anthropic's announced text marking and what can actually be measured |
| [paired-corpus.md](paired-corpus.md) | Before/after protocol for a future real-world key-free test |
| [dipper-local.md](dipper-local.md) | Why the official 11B DIPPER checkpoint is not part of the current setup |
| [HOW-TO.md](../HOW-TO.md) | Installation and practical commands |

The conceptual split is simple:

**known keys → `score`**  
**unknown keys + paired evidence → `blind` / `indicate` / `probe`**  
**public vs other instance, still key-free → `contrast`**  
**occupancy vs observed next token → `tokhits` / `postokhits` / `hashtok` / `hashtok2` / `hashtokbackoff` / `hashtoklen`**  
**opening-overlap bound / last-2 floor → `openings` / `postokbackoff2` / `hashtokbackoff2`**  
**rank-symbol tables / leftover fill-in → `rankpath` / `--cascade-rankpath-end` / `--cascade-when`**  
**table-free unmarked-LM snap-rate → `--snaprate` (`snapupset` is chance)**  
**key-free removal attempt → `scrub` (official `score` only as a reference check)**
