# Research notes

This directory contains the reasoning behind the experiments in the root [README](../README.md).

The main result is the **key-free watermark indicator** described in [key-free-twins.md](key-free-twins.md): matched marked/unmarked generations contain enough statistical structure to classify most held-out prompt groups without using the detector keys.

Citations in these notes are author–year ([CITING.md](CITING.md)). Do not invent papers. A future research report should compile [references.bib](references.bib); do not write `thesis/` until isolated-file research is finished.

| File | Focus |
|---|---|
| [LOGBOOK.md](LOGBOOK.md) | Dated lab notes. Append after every Claude sample or measurement |
| [key-free-twins.md](key-free-twins.md) | Key-free watermark indication from matched generations; original last-4 **10/12**; `hits` **11/12** |
| [key-free-probe.md](key-free-probe.md) | Transfer scorers, hash pooling, unmarked-LM choice geometry, argmax snap |
| [key-free-learn.md](key-free-learn.md) | Tiny hashed logistic / token MLP / char CNN; they do not beat poshits |
| [key-free-contrast.md](key-free-contrast.md) | Public vs control-shuffled-30: 4-token poshits is instance-specific (**0/48**); prefix-4 rankpath control **6/48** |
| [key-free-tokhits.md](key-free-tokhits.md) | Occupancy Laplace vs observed next tokens: 39/48 includes The-ferry; postokhits **16/48** precision 1.0; opening-overlap last-2+ core **13/48** |
| [key-free-hashtok.md](key-free-hashtok.md) | Occupancy-free hashpool: prefix-5 hashtok **30/48**; hashtoklen **21/48** with harbour d2 the one collision extra; hashtoklen2 **10/48 vs 48/48** (11/21 TPs were singletons); hashskip nested **16/48**; hashmask nested **19/48 vs 45/48** (worse than hashtoklen); hashtoklen2+rankpath cascade copies rankpath **28/48**; in-domain full-file hashtok **33/48 vs 22/48**; `--n-hashes 2` **34/48 vs 31/48** nested **28/48 vs 37/48** (AUC **0.764**); `--n-hashes 4` **36/48 vs 30/48** nested **35/48 vs 30/48**; `--n-hashes 16` 36/48 nested spec **24/48**; `--n-hashes 32` hurts **30/48** nested **21/48 vs 38/48**; default n=8 is not the best in-domain width at seed 20260831; that n=2 win is seed-confounded (spec **21–31/48**); 24→12 nested Youden prefers n=8 **17/48 vs 46/48** (keep CLI default); do not sell 36/48 or 31/48; OR with indicate **39/48 vs 12/48** combined 51/96 (not a detector); tokhybrid copies that 33/48 (prompt 11/12); poshashtok nested **14/48 vs 38/48**; hashtokgap **27/48 vs 21/48** (strict subset of hashtok; nested **17/48 vs 31/48**); hashtok2 **34/48 vs 21/48** (sign reshuffle, nested **19/48 vs 35/48**); opening-grain `--fit-prefix 4` hashtok **24/48 vs 47/48** (tokhits ⊂ hashtok; extra TP letter d3; nested **23/48 vs 47/48**; marked recall below **29/48**), not rankpath **41/48**; Distil transfer AUC **0.571** |
| [related-work.md](related-work.md) | Narrative related work, author–year |
| [annotated-bibliography.md](annotated-bibliography.md) | Critical annotations (what each source is, and is not, for this lab) |
| [references.bib](references.bib) | Canonical BibTeX |
| [CITING.md](CITING.md) | Author–year convention for a future report |
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
