# text-watermark-laboratory

**text-watermark-laboratory** explores a practical question about statistical text watermarks:

> **Can we tell whether text carries a watermark even when we do not have the detector keys?**

For the experimental setup in this repository, the answer is **yes — to a useful but still limited degree**.

Using Google DeepMind's public SynthID-Text implementation as a controlled reference, we generate matched marked and unmarked text from the same prompts. From those pairs we have built a **key-free watermark indicator**: a model that can score previously unseen text by how strongly its token statistics resemble the marked rather than the unmarked class, without using the watermark keys, `hash_iv`, or g-values.

The clean headline for the original last-4 count tables is **10/12 held-out prompt groups**: after training on the other eleven prompt families, the marked side of the twelfth ranks above its unmarked twin group. That is **relative discrimination**, not “here is one unknown file; marked yes/no?”. A 0.02 comparison margin lifts *that same scorer* to 11/12; that is a robustness check, not the main result.

Scoring only 4-grams seen on both training sides (`hits`) reaches **11/12** with no margin and file-level AUC **0.737**. Feature-hashing those contexts (`hashpool`) reaches **11/12** and **35/48** isolated marked files with `lr > 0` (binomial p ≈ 0.001). The original hard sign at 0 remains weak under leave-one-of-12-out: **29/48**. Train the same hits reader on 24 *other* GPT-2 topics and the 12×4 files score **39/48** (AUC **0.769**). Train on 12×4 and score 24 new topics: hits ranks **24/24** (AUC **0.986**), with unmarked specificity at 0 only 14/24. There is a transferable held-out signal. It is not a magic detector, and this lab did not invent key-free watermark detection.

This repository also contains the ordinary key-based reference scorer, matched-pair generation, rewrite/degradation experiments, and a pre-mark Claude corpus for future before/after comparison.

Install and run your first measurement: **[HOW-TO.md](HOW-TO.md)**  
Research notes: **[research/](research/)**  
Coding-agent instructions: **[AGENTS.md](AGENTS.md)**

---

## What we found

The key result is not merely that watermarked text leaves “some statistical trace”. Tournament sampling leaves a **secondary, learnable footprint** in next-token counts. A very simple model — context/token tables plus a likelihood ratio, no keys, no `hash_iv`, no g-values — can pick that footprint up. The code enforces the claim: `BlindModel` carries `used_keys`, `used_hash_iv`, and `used_g_values`, the held-out decision never consults `detector_mean`, and `indicate` refuses to persist a table that says those flags are true.

That still leaves two different tasks.

**Relative discrimination (the 10/12 number).** Leave one prompt family out. Fit marked and unmarked count tables on the rest. Score the held-out marked generations and the held-out unmarked generations. Count a hit if the marked group’s mean LR is higher than the unmarked group’s. Four draws and last-4 context with the original hard scorer: **10/12**. `--margin 0.02` lets the unmarked side win by up to 0.02 and still count as a marked win; that is how one **11/12** appears. Quote **10/12** for that scorer. Treat the 0.02-margin 11/12 as a tolerance note.

A different reader of the same tables — score only 4-grams seen on both training sides (`hits`) — reaches **11/12** with no margin, file-level AUC **0.737**. Feature-hashing those 4-grams (`hashpool`) is also **11/12**. Those 11/12 figures are new methods, not the 0.02 fudge.

**Single-text classification (the 29/48 number).** Same leave-one-out tables, but decide from the sign of one file’s LR against 0, with no twin. Hard last-4 marked `lr > 0`: **29/48**. Unmarked `lr ≤ 0`: **23/48**. The two distributions overlap (mean marked LR +0.033, unmarked −0.003). Binomial P(≥29 | n=48, p=0.5) = 0.097, so that sign is not a 5% test. Ranking of the same LRs is (AUC 0.626, permutation p = 0.0075). Hashpool’s isolated sign is **35/48** (p ≈ 0.001), with unmarked specificity still 29/48.

When the tables are trained on **other prompt families** (24 stems from the 36-topic corpus, none of harbour/night-bus/…), hits on the 12×4 files is **39/48** marked `lr > 0` (AUC **0.769**). Four training draws per new topic lift that ranking to **12/12** prompt groups and **42/48** isolated files at threshold 0 (AUC **0.793**); nested Youden then becomes conservative (26/48 vs 44/48). The reverse — train 12×4, test 24 new topics — ranks every marked file above its unmarked twin (hits **24/24**, AUC **0.986** on the 1-draw 256-token stems; **24/24** and AUC **0.924** on four 128-token draws). Nested hits 10% FPR on those 96 new-topic files is **83/96** vs **85/96**. Leave-one-of-36-out with four draws reaches **36/36** prompt grain (AUC **0.934**) and a nested-by-stem hits gate of **119/144** vs **134/144**; that is in-domain, same generator. The in-domain mark is front-loaded: a 16-token prefix already ranks **34/36** (AUC **0.916**). Matching the mixin's `ngram_len=5` (`context_len=5`) does **not** beat last-4 (35/36, AUC 0.912). Fitting *and* scoring on those first 16 tokens (`--fit-prefix 16`) lifts unmarked `≤ 0` to **112/144** in-domain (AUC **0.929**) versus 76/144 on the full 128-token hits reader. Namespacing last-4 counts by token position (`poshits`, bucket 16) keeps the same 134/144 marked t=0 detections as hits on 36×4 while unmarked `≤ 0` rises from 76 to **97**. Out of family, both raise file AUC above the full-file 0.793 (matched-prefix **0.818**, poshits **0.811**) and lose a little prompt grain. Shared last-k mass is why the reader is front-loaded, and it is short-context: token index 1 is **96.9%** shared. Scoring only the first **four** tokens already ranks **34/36** (AUC **0.917**), matching the 16-token prefix. A matched 4-token fit with position namespace (`--fit-prefix 4 --pos-bucket 1`) balances in-domain t=0 at **131/144 vs 132/144**. Trained on 24 other topics it ranks the 12×4 files **12/12** (AUC **0.873**) with isolated t=0 **39/48 vs 41/48**, and nested Youden matches that gate. That 39/48 includes Laplace occupancy after shared `'The'` (every novel continuation gets the same δ = 0.330); scoring only next tokens seen in train (`postokhits`) is **16/48** with precision 1.0 among decided files, still **12/12** prompt ranking. Twelve medium-length new topics lift observed-token isolated recall to **19/48** (20/48 combined with the short one-liners); the nine After / Closing / Now / While zeros remain, and The-Laplace flips sign on that train. The 16-token finest-bucket reader copies those OOD numbers. Leave-one-of-12-out on the original 12 prompts alone does not (9/12, 23/48). Extra GPT-2 training draws do not create a Qwen detector (new topics → new Qwen sample: hits 6/12, AUC 0.445; matched-prefix bucket 1 is still chance, 8/12, AUC 0.516). The 29/48 figure is the leave-one-of-12-out hard scorer, not the best isolated-file protocol this lab now has. Isolated observed-token recall equals train opening-atom overlap: `postokbackoff2` (min last-2) stays **13/48** while last-1 backoff carries 16→36; unbucketed last-1 and `--include-first` unigrams spend precision for extra recall. That is still not a universal detector.

| Method | What is being asked | Result |
|---|---|---|
| Official `score` | Public DeepMind keys, 12 matched prompts | **12/12** |
| Key-free, 1 sample | Twin ranking, 12 × 128 tokens | **8/12** |
| Key-free, 4 samples, last-4 | Twin ranking of held-out prompt groups | **10/12** |
| Same LRs, margin 0.02 | Same ranking, unmarked may lead by 0.02 | 11/12 (not the headline) |
| Key-free `hits` (shared 4-grams only) | Same 12×4 twins, skip unseen contexts | **11/12**, AUC **0.737** |
| Key-free hashpool | Feature-hashed last-4, no secret hash | **11/12**, isolated **35/48** |
| Key-free hashpool, 36 topics | Same method, one draw per prompt | **31/36**, AUC **0.877** |
| Key-free hashpool, Qwen 12×1 | Different generator, last-4 hashpool | **10/12**, isolated **11/12** |
| Key-free hits, other topics → 12×4 | Train 24 new stems, score 12×4 files | isolated **39/48**, AUC **0.769** |
| Same split, 4 training draws | 24×4 new stems → 12×4 | **12/12** ranking, isolated **42/48**, AUC **0.793** |
| Nested hashpool Youden, same split | Train-only threshold, frozen on 12×4 | **33/48** marked, **34/48** unmarked |
| Nested hits Youden, 4-draw train | Same 12×4 files, higher threshold | **26/48** marked, **44/48** unmarked |
| Nested hits FPR10, 12×4 → 36×4 | New topics, 96 files, train-only 10% FPR | **83/96** vs **85/96** |
| Key-free hits, 36 topics × 4 draws | In-domain leave-one-out | **36/36**, AUC **0.934**; nested-by-stem **119/144** vs **134/144** |
| Key-free hits, first 16 tokens, 36×4 | In-domain prefix (mark is front-loaded) | **34/36**, AUC **0.916**; isolated 129/144 |
| Key-free hits, tokens 16–32 only, 36×4 | Disjoint window, not a prefix | **22/36**, AUC **0.549** (near chance) |
| Key-free hits, first 16 tokens, 24×4 → 12×4 | New-topic prefix ranking | **11/12**, AUC **0.752**; nested-by-stem 25/48 vs 29/48 |
| Key-free hits, matched 16-token fit, 36×4 | Fit and score the same 16 tokens | **34/36**, AUC **0.929**; unmarked ≤0 **112/144** |
| Key-free poshits (bucket=16), 36×4 | Position-namespaced last-4 | **34/36**, AUC **0.925**; t=0 spec **97/144** (hits 76/144) |
| Key-free hits, matched 16-token 24×4 → 12×4 | New-topic matched prefix | **11/12**, AUC **0.818**; nested-by-stem 39/48 vs 36/48 |
| Key-free poshits, 24×4 → 12×4 | New-topic position-namespaced last-4 | **10/12**, AUC **0.811**; nested-by-stem 37/48 vs 35/48 |
| Key-free poshits, matched 16-token bucket 4, 36×4 | Finer buckets on the opening | **34/36**, AUC **0.937**; unmarked ≤0 **114/144** |
| Key-free hits, tokens 0:4 only, 36×4 | Short-context opening (not extra 4-grams) | **34/36**, AUC **0.917** (matches 0:16) |
| Key-free poshits, matched 4-token bucket 1, 36×4 | Tight matched opening + position namespace | **34/36**, AUC **0.935**; t=0 **131/144 vs 132/144** |
| Same reader, 24×4 → 12×4 | New-topic matched 4-token isolated-file gate | **12/12**, AUC **0.873**; t=0 **39/48 vs 41/48** |
| Nested Youden, same split | Train-only Youden, frozen on 12×4 | **39/48 vs 41/48** |
| Key-free postokhits, same OOD gate | Skip Laplace unseen next tokens | **12/12**, isolated **16/48**, decided precision **1.000** |
| Same postokhits, 36×4 LOO | In-domain observed-token opening | 34/36, AUC 0.912; t=0 **122/144 vs 132/144** |
| Key-free postokhits, 12 medium scenes → 12×4 | Matched ~40-word new topics | **12/12**, isolated **19/48**, decided precision **1.000** |
| Same plus 24 short one-liners | Combined train | **12/12**, isolated **20/48**, decided precision **1.000** |
| Key-free postokbackoff, 12 medium scenes → 12×4 | Shrink last-k until observed next token | **12/12**, isolated **21/48**, decided precision **1.000** |
| Key-free postokbackoff plus 24 short one-liners | Combined train | **12/12**, isolated **22/48**, decided precision **1.000** |
| Key-free postokhits, tail-matched → 12×4 | Last paragraphs from zero-producing seeds | **12/12**, isolated **30/48**, decided precision **1.000** |
| Key-free postokbackoff, short+medium+tails → 12×4 | Same train, shrink last-k | **12/12**, isolated **36/48**, AUC **0.888**, decided precision **1.000** |
| Key-free postokbackoff2 on that combined train | tokbackoff that will not shrink below last-2 | **13/48** last-2+ core (same on 24 short stems) |
| Opening-overlap bound, same twins | Isolated recall = train atom overlap | Two short stems already cover 13/48; tails carry 22→36 |
| Unbucketed tokbackoff on that combined train | Drop the position namespace | **36/48** marked, **3** unmarked FP, precision 0.923 |
| `--include-first` postokhits on that combined train | First-token unigram plus last-k | **43/48** marked, **10** unmarked FP |
| Neighborhood paraphrases, 12 scenes × 4 | Letter/library/ferry/office/station, not tail glue | Official **12/12**; no Closing/Now/While/The ferry |
| Same plus short+medium+tails → 12×4 | Neighborhood last-1 covers ferry was so/over | postokbackoff **42/48**, last-2+ **15/48**, precision **1.000** |
| Key-free last-1, same 4-token OOD split | Truncated last-4 was already last-1 | **12/12**, AUC **0.873**; t=0 **39/48 vs 41/48** |
| `--include-first` on that 4-token OOD gate | Mixing token 0 into hits | 9/12, AUC 0.719 |
| Qwen 12×4 first-token opening | In-domain, Qwen tokenizer | **12/12**, AUC **0.901** (hits without token 0: 7/12) |
| DistilGPT2 12×4 official / in-domain hits | Same keys, GPT-2 tokenizer | **12/12** / **9/12**, AUC 0.705 |
| GPT-2 36×4 → DistilGPT2 | Same BPE, new generator | hits **5/12**, AUC **0.462** |
| Key-free tokmlp, 4-token 24×4 → 12×4 | Tiny token MLP, same gate as poshits | 8/12, AUC 0.714 (does **not** beat poshits 0.873) |
| Key-free hashlog on that OOD gate | Hashed logistic, same split | 7/12, AUC 0.606 |
| GPT-2 learned scorers → Distil / Qwen | tokmlp / charcnn / hashlog | chance (charcnn Qwen AUC 0.496) |
| Key-free poshits vs control-shuffled-30 | 4-token 24×4 → 12×4, other instance | **0/48** control `lr>0`; public vs control **12/12**, AUC **0.906** |
| Key-free postokhits vs control-shuffled-30 | Observed-token only, same split | **0/48** control `lr>0`; public vs control **12/12**, AUC 0.667 |
| Key-free postokbackoff vs control-shuffled-30 | Shrink last-k, same split | **0/48** control `lr>0`; public vs control **12/12**, AUC 0.667 |
| Official lamp on 12×4 control-key twins | 48 files, public vs matching keys | public **0.501**; matching **0.624** |
| Key-free last-k coverage, 36×4 LOO | Shared both-side contexts by window | 0:16 **13.7%** (driven by i=1–2); full last-4 from i=4 is ~4% |
| Key-free poshitmass, matched 16-token bucket 4 | Coverage-weighted bucketed hits | **34/36**, AUC **0.943**; unmarked ≤0 **114/144** |
| Key-free poshits, matched 16-token bucket 1, 36×4 | Same OOD gate as 4-token, longer clip | **34/36**, AUC **0.938**; t=0 **132/144 vs 132/144** |
| Mixin last-5 vs last-4, 36×4 hits | `context_len=5` matches `ngram_len=5` | **35/36**, AUC **0.912** (does **not** beat last-4) |
| UTF-8 surface, 12×4 leave-one-out | Byte hashpool, no tokenizer | **10/12**, AUC **0.602** |
| Same-topic GPT-2 hits → Qwen 12×1 | Probe-tokenizer paired ranking | **11/12** (isolated `lr>0` **1/12**) |
| New Qwen 12×4 sample, GPT-2 hits | Same prompts, new draws | **5/12** (does not replicate 11/12) |
| New topics GPT-2 36×4 → new Qwen 12×4 | Hits / hashpool / surface | chance (hits **6/12**, AUC 0.445) |
| Same-topic GPT-2 surface → new Qwen 12×4 | Byte table, overlapping stems | **7/12**, AUC 0.525 (isolated 5/48) |
| Key-free hits, 12×4 → 24 new topics | Train 12×4, score stems 13–36 | **24/24** ranking, AUC **0.986** |
| Nested freqhits Youden, reverse split | Train-only threshold, frozen on 24 stems | **23/24** and **23/24** |
| 50% train-label shuffle, 36→12×4 | Negative control, isolated sign at 0 | hits **19/48**, hashpool **20/48** |
| Local Qwen2-1.5B, last-2 | Twin ranking, published count tables | **10/12** |
| `indicate` hard, one marked file | Isolated `lr > 0`, leave-one-of-12-out | **29/48** |
| `indicate` hard, one unmarked file | Isolated `lr ≤ 0` | **23/48** |
| Argmax snap, then official `score` | Key-free scrub of 48 marked files | **0.622 → 0.499** |

So `indicate` is an experimental watermark-presence indicator. It is not a universal verdict machine, and 10/12 must not be read as single-text accuracy.

`probe` compares other key-free scorers on the same twins (interpolation, coverage gating, hash pooling, optional unmarked-LM choice geometry) and reports AUC as well as prompt-grain wins. `scrub` tries to remove a known public mark by snapping tokens to the unmarked argmax. Neither reconstructs keys.

Detailed protocol and results: [research/key-free-twins.md](research/key-free-twins.md) and [research/key-free-probe.md](research/key-free-probe.md). Tiny key-free learned scorers (`learn`) are an experiment on the same grains, not a replacement of the count tables: [research/key-free-learn.md](research/key-free-learn.md). Instance contrast against `control-shuffled-30` is [research/key-free-contrast.md](research/key-free-contrast.md): the 4-token poshits reader is instance-specific without keys (**0/48** control `lr>0`), not a generic tournament detector. Occupancy Laplace vs observed next tokens is [research/key-free-tokhits.md](research/key-free-tokhits.md): the 39/48 poshits isolated-file number includes The-Laplace; `postokhits` is **16/48** with precision 1.0 among decided files. Rank-symbol tables that score novel openings without token identity are [research/key-free-rankpath.md](research/key-free-rankpath.md): prefix-4 rankpath ranks control-shuffled-30 with unmarked (AUC **0.511**, isolated **6/48**), not the poshits **0/48**.

---

## The controlled experiment

SynthID-Text does not insert hidden characters or metadata. The watermark changes **which next tokens are selected during generation**.

That makes a paired experiment possible:

```mermaid
flowchart TD
  P[Same prompt] --> U[Generate with watermark off]
  P --> M[Generate with watermark on]
  U --> UT[Unmarked twin]
  M --> MT[Marked twin]
```

With the public keys available, DeepMind's detector confirms that the mark is present:

```text
unmarked ≈ 0.50
marked   ≈ 0.61–0.65
```

For the key-free experiment, those official scores are not used to make the decision:

```mermaid
flowchart LR
  A[Hold out one prompt] --> B[Fit marked/unmarked token tables on the others]
  B --> C[Score held-out text without keys]
  C --> D[Likelihood ratio: marked-like vs unmarked-like]
```

The experiment therefore asks a harder question than ordinary detection: **is there enough structure in the sampler's output to infer watermark presence without reproducing the detector?**

For held-out *groups*, yes (10/12 hard last-4; 11/12 with `hits` or `hashpool`; 36/36 hits on 36 topics × 4 draws). For one file’s hard sign at 0 under leave-one-of-12-out, not reliably (29/48). Out-of-family hits is stronger (39/48 on 12×4 from 1-draw train; 42/48 from 4-draw train; 24/24 ranking on new topics) but still not a universal detector. Nested hits 10% FPR on 96 new-topic 36×4 files is 83/96 vs 85/96. Hashpool’s in-family isolated sign is 35/48.

---

## Commands

```bash
source .venv/bin/activate
python -m pytest tests/ -q

# Key-based reference score
python -m text_watermark_tools score path/to/text.txt

# Generate marked/unmarked twins
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --out-dir experiments/pairs --max-new-tokens 128

# Key-free leave-one-out experiment
python -m text_watermark_tools blind experiments/pairs \
  --out-dir experiments/blind

# Evaluate the key-free indicator
python -m text_watermark_tools indicate holdout experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4

# Fit reusable tables and score a file
python -m text_watermark_tools indicate fit experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/indicator-gpt2 --context-len 4

python -m text_watermark_tools indicate score path/to/text.txt \
  --tables experiments/indicator-gpt2
# Coverage-gated tables print n_used. n_used=0 is ABSTAIN, not unmarked.

# Hashpool tables (usable 35/48 reader) and out-of-family transfer
python -m text_watermark_tools indicate fit experiments/2026-08-17-pair-12x4 \
  --method hashpool --out-dir experiments/indicator-gpt2-hashpool

python -m text_watermark_tools indicate score path/to/text.txt \
  --tables experiments/2026-08-31-transfer-36-to-12x4/tables-hashpool

python -m text_watermark_tools probe experiments/2026-08-17-pair-36 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --overlap drop-from-train \
  --out-dir experiments/transfer

# Compare key-free scorers (AUC + prompt-grain wins)
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/probe

# Token prefixes and disjoint windows (isolated-file curves)
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --methods hits,hashpool \
  --prefix-lens 16,32,64,96,128 \
  --windows 0:16,16:32,32:64,64:128 \
  --out-dir experiments/probe-prefix-windows

# Matched prefix fit, and position-namespaced last-4
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --fit-prefix 16 --methods hits,hashpool \
  --out-dir experiments/probe-fitprefix16
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --methods hits,poshits,pospool --pos-bucket 16 \
  --out-dir experiments/probe-posbucket
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --coverage --windows 0:16,16:32,32:64,64:128 \
  --out-dir experiments/probe-coverage
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --fit-prefix 16 --methods poshits,poshitmass --pos-bucket 1 \
  --out-dir experiments/probe-fitprefix16-pos1
```

`score` and `indicate` answer different questions:

- `score` reproduces the public DeepMind detector for the known `public-deepmind-30` instance.
- `indicate` asks whether text statistically resembles the marked or unmarked side of a learned corpus **without those keys**.

---

## Reference scoring

The repository uses DeepMind's published 30-key reference configuration:

```text
instance=public-deepmind-30
ngram_len=5
```

A sufficiently long text near 0.50 shows no measurable bias toward **that key set**. A marked sample generated with the same public mixin typically scores around 0.61–0.65 in our runs.

This is a controlled research baseline. It is not a general human-vs-AI classifier.

---

## Rewriting experiments

The lab can also take a sample known to be marked under the public instance, rewrite it, and measure what happens to the signal.

Earlier measurements include:

- marked GPT-2 text: **0.617 / 0.638**
- light Sonnet proofread: **0.605 / 0.625**
- full Sonnet rewrite: **0.502 / 0.502**
- Qwen rewrite of a known marked sample: approximately **0.50**

These experiments measure how a known watermark behaves under transformation. They are not needed for the key-free indicator itself.

---

## Claude

Anthropic has announced text marking based on "a version of" SynthID-Text. Their production keys and detector are not public.

That makes Claude interesting for a different reason: it provides a future real-world test of the key-free method.

The repository contains a **pre-mark corpus** in `experiments/claude-premark-2026-08/`. Once a comparable marked corpus exists, the same prompts can be rerun and the before/after shift can be measured without pretending that DeepMind's public keys are Claude's keys.

See [research/claude.md](research/claude.md) and [research/paired-corpus.md](research/paired-corpus.md).

---

## Related work

This lab did **not** invent key-free watermark detection.

[TTP-Detect](https://arxiv.org/abs/2603.14968) (*Rethinking LLM Watermark Detection in Black-Box Settings*) formulates third-party, key-agnostic verification from observable outputs and paired watermarked/unwatermarked reference sets — the same audit problem, a different method. Earlier watermark-stealing and probing work learns structure from black-box samples. [ETH/SRI’s SynthID probe](https://www.sri.inf.ethz.ch/blog/probingsynthid) ([Sabanayagam, Hörl, Dobriban 2024](https://arxiv.org/abs/2405.20777)) shows that SynthID-Text can be detected as a *generator property* with repeated fixed-context queries. That is not the same measurement as scoring a finished string against count tables.

What this repository adds is a small, fully checked-in instance of the second measurement on DeepMind’s **public** mixin: GPT-2 and Qwen twins, leave-one-out, a frozen indicator table, tests, and raw JSON. The interesting claim is narrow. The keyed tournament leaves a distributional footprint that a count-based LR can learn **without reconstructing the g-function**. Independent work landed in the same research question; treat this as an empirical notebook, not a priority claim.

If the 10/12 ranking is a confound (topic reuse, tokenizer mismatch, prompt-family leakage), that is the thing to break. Extra draws of the *same* prompt helped last-4 **for the hard scorer**. Extra topics, by themselves, did not help that scorer (20/36). Coverage gating and hash pooling later showed that extra topics *do* help once unseen 4-grams are not dumped into the unigram (30–31/36).

## Boundaries

The current results support a specific claim:

> **On this public mixin, matched twins leave enough key-free statistical structure that a count-based indicator can rank most held-out prompt groups.**

They do not establish invention of the problem, reliable classification of every isolated paragraph, recovery of secret keys, or equivalence between `public-deepmind-30` and production systems from other vendors.

Those are different questions.

---

## Project layout

```text
AGENTS.md        coding-agent instructions
HOW-TO.md        installation and practical usage
research/        methods and research notes
experiments/     dated runs and result artifacts
src/             score, pair, blind, indicate, iterate
```

The project depends on [`google-deepmind/synthid-text`](https://github.com/google-deepmind/synthid-text) but is not a fork.

Licensed under [MIT](LICENSE).
