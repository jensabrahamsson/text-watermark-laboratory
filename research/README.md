# Research notes

This directory contains the reasoning behind the experiments in the root [README](../README.md).

The main result is the **key-free watermark indicator** described in [key-free-twins.md](key-free-twins.md): matched marked/unmarked generations contain enough statistical structure to classify most held-out prompt groups without using the detector keys.

| File | Focus |
|---|---|
| [LOGBOOK.md](LOGBOOK.md) | Dated lab notes. Append after every Claude sample or measurement |
| [key-free-twins.md](key-free-twins.md) | Key-free watermark indication from matched generations; original last-4 **10/12**; `hits` **11/12** |
| [key-free-probe.md](key-free-probe.md) | Transfer scorers, hash pooling, unmarked-LM choice geometry, argmax snap |
| [key-free-learn.md](key-free-learn.md) | Tiny hashed logistic / token MLP / char CNN; they do not beat poshits |
| [key-free-contrast.md](key-free-contrast.md) | Public vs control-shuffled-30: 4-token poshits is instance-specific (**0/48**); prefix-4 rankpath control **6/48** |
| [key-free-tokhits.md](key-free-tokhits.md) | Occupancy Laplace vs observed next tokens: 39/48 includes The-ferry; postokhits **16/48** precision 1.0; opening-overlap last-2+ core **13/48** |
| [key-free-cascade.md](key-free-cascade.md) | Coverage-then-fallback: ABSTAIN at n_used=0; opening geometry, not full-file |
| [key-free-rankpath.md](key-free-rankpath.md) | Rank-symbol tables: opening 41/48; prefix-4 OOD 11/12 25/48 vs 43/48; control **6/48** |
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
**occupancy vs observed next token → `tokhits` / `postokhits`**  
**opening-overlap bound / last-2 floor → `openings` / `postokbackoff2`**  
**rank-symbol tables / leftover fill-in → `rankpath` / `--cascade-rankpath-end`**  
**key-free removal attempt → `scrub` (official `score` only as a reference check)**
