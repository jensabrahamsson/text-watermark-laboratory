# How to use text-watermark-laboratory

This guide gets the laboratory running, explains the two scoring paths, and shows how to reproduce the key-free watermark experiments. The result in one paragraph is the [README abstract](README.md#abstract).

## What the lab can tell you

There are two different ways to measure text in this repository.

### 1. `score`: known-key reference detection

`score` asks:

> How strongly does this text match DeepMind's public `public-deepmind-30` SynthID-Text instance?

It uses the published keys and DeepMind's detector.

### 2. `indicate`: key-free watermark indication

`indicate` asks:

> Does this text statistically resemble the marked or unmarked side of a corpus learned from matched generations?

It does **not** use the watermark keys, `hash_iv`, or g-values.

This is one of the main research results of the project: we have built a **key-free watermark indicator**. After correcting truncated-context overcount, the original last-4 count tables separate held-out prompt groups **9/12** times, or **10/12** with a 0.02 comparison margin. Scoring only shared 4-grams (`hits`) reaches **10/12** (AUC **0.718**). On the hard scorer, individual files are weaker: **25/48** held-out marked files have `lr > 0`. Four draws on 36 GPT-2 topics still lift in-domain hits to **36/36** (AUC **0.930**). Frozen lock A on 100 new GPT-2 families is **99/100**; that is prompt-group ranking on a new corpus, not a replacement of **25/48**. In-family nested-by-stem Youden on that lock is **322/400 vs 338/400**. Out-of-family, those tables score the original 12×4 files at nested Youden **23/48 vs 38/48** (does not beat **25/48**). Occupancy-free readout of the same lock B tables is **16/48 vs 48/48**; isolated observed-token recall equals train opening coverage (**18/48** covered). Lock C opening rankpath is **10/12**, nested **24/48 vs 41/48**; losses are letter and garden, and three ranking wins have no isolated TPs. Protocol: [research/PROTOCOL-isolated.md](research/PROTOCOL-isolated.md). Register-matched Grok-length train is [research/PROTOCOL-isolated-register.md](research/PROTOCOL-isolated-register.md): lock A nested **16/48 vs 41/48** does not beat **25/48**. Reverse 100 one-liners → Grok-register 12 is [research/PROTOCOL-isolated-xreg.md](research/PROTOCOL-isolated-xreg.md): lock A nested **22/48 vs 41/48**; occupancy-free **0/48**. Window readout is [research/PROTOCOL-isolated-windows.md](research/PROTOCOL-isolated-windows.md): that **11/12** is not front-loaded. The `atoms` decode of those interpolate tables is almost all Witten–Bell backoff, not occupancy-free openings. Thirty-six Grok-length families ([research/PROTOCOL-isolated-scale.md](research/PROTOCOL-isolated-scale.md)) fill grok12 occupancy-free to **39/48** (equals coverage) and original-12 lock A nested to **26/48 vs 33/48**; occupancy-free on those 12 is **10/48**. The `atoms` decode of those interpolate tables is still mostly Witten–Bell backoff: original-12 nested **26/48** is not occupancy-free **10/48** (library `Closing` is an unbucketed body copy); grok12 0:4 is opening overlap (`'The' → ' car'` n=19). Isolated recall is still opening overlap. Do not sell `Closing` or `The car`. Published occupancy-free zeros of those two trains on the original 12 are disjoint (union **28/48**); mixed extra-train coverage equals that union and occupancy-free t=0 is **26/48** ([research/PROTOCOL-isolated-pool.md](research/PROTOCOL-isolated-pool.md)). Mixed leftover rankpath is leftover **12/20 vs 14/20**. In-domain **25/48** splits leftover **10/20 vs 11/20** and occupancy-covered **15/28 vs 11/28** ([research/PROTOCOL-isolated-split.md](research/PROTOCOL-isolated-split.md)); leftover last-4 is chance. Mask-*k* hard tails stay **9/12** while prefix 0:4 is **5/12** ([research/PROTOCOL-isolated-mask.md](research/PROTOCOL-isolated-mask.md)); leftover versus covered on hard 4:128 is leftover **11/20 vs 11/20**, covered **16/28** ([research/PROTOCOL-isolated-mask-split.md](research/PROTOCOL-isolated-mask-split.md)); leftover tail is chance. Occupancy leftover-20 files are still officially marked (**20/20** at prefix-128); leftover interpolate 0:4 is unseen **99 vs 21** ([research/PROTOCOL-isolated-leftover-bound.md](research/PROTOCOL-isolated-leftover-bound.md)). Leftover-20 ∪ short+medium+tails openings is union **30/48** (equals SMT; mixed is a subset); leftover after union is **18**; leftover last-4 is **10/18 vs 10/18** ([research/PROTOCOL-isolated-leftover-union.md](research/PROTOCOL-isolated-leftover-union.md)). Occupancy-free leftover-18 is closed for more unrelated GPT-2 scenes ([research/PROTOCOL-isolated-occupancy-closed.md](research/PROTOCOL-isolated-occupancy-closed.md)). Leftover-18 mixed rankpath is **12/18 vs 13/18**; grok36 interpolate is **12/18 vs 12/18**; leftover-18 0:4 unseen **89 vs 19** ([research/PROTOCOL-isolated-leftover-18.md](research/PROTOCOL-isolated-leftover-18.md)). Leftover-18 published key-free readers are closed ([research/PROTOCOL-isolated-leftover-18-closed.md](research/PROTOCOL-isolated-leftover-18-closed.md)). Distil occupancy-free leftover-18 on the original 12 is [research/PROTOCOL-isolated-xgen.md](research/PROTOCOL-isolated-xgen.md): Distil postokhits t=0 **22/48 vs 43/48** (beats GPT-2 occupancy-free **16/48**, not **25/48**); leftover-18 Distil coverage **3/18** (office 1/3/4). Distil 100×4 → Distil 12×4 occupancy-free analog is [research/PROTOCOL-isolated-dgen.md](research/PROTOCOL-isolated-dgen.md): Distil→Distil postokhits t=0 **16/48 vs 39/48** (equals coverage **16/48**; does not beat **25/48**). Qwen 100×4 → Qwen 12×4 occupancy-free analog is [research/PROTOCOL-isolated-qgen.md](research/PROTOCOL-isolated-qgen.md): Qwen→Qwen postokhits t=0 **31/48 vs 48/48** (coverage **37/48**; does not replace **25/48**). Distil ∪ SMT occupancy-free openings on the original 12 is [research/PROTOCOL-isolated-dsmt.md](research/PROTOCOL-isolated-dsmt.md): union **33/48**; leftover **15**; last-4 **9/15 vs 8/15**. Occupancy-free leftover-15 is closed ([research/PROTOCOL-isolated-leftover-15-closed.md](research/PROTOCOL-isolated-leftover-15-closed.md)). Occupancy-free leftover-15 gpt2-medium analog is [research/PROTOCOL-isolated-mgen.md](research/PROTOCOL-isolated-mgen.md) (leftover **0/15**; t=0 **16/48**). gpt2-medium 100×4 → gpt2-medium 12×4 occupancy-free analog is [research/PROTOCOL-isolated-m12.md](research/PROTOCOL-isolated-m12.md): t=0 **10/48 vs 48/48**; coverage **13/48**; does not beat **25/48**. Do not sell Distil **22/48**, Distil→Distil **16/48**, Qwen→Qwen **31/48**, leftover Distil **3/18**, union **33/48**, leftover **9/15**, or leftover official **15/15**. Do not sell **28/48**, **26/48**, **10/20**, **15/28**, **11/20**, **16/28**, tail **9/12**, leftover official **20/20**, leftover interpolate **13/20**, union **30/48**, leftover **10/18**, leftover official **18/18**, leftover-18 rankpath **12/18**, or leftover-18 interpolate **12/18**. None of that is a replacement of **25/48**. The pre-fix **10/12** / **29/48** stay in historical JSON; they overweighted openings. None of that is a universal yes/no.

Use `score` when you have the relevant public reference instance. Use `indicate` when you are exploring the key-free signal.

---

## Requirements

- Python 3.10+
- Git
- a few GB of disk space
- roughly 8 GB RAM
- internet access during installation

A GPU is not required. The standard setup uses CPU JAX.

The project is developed primarily on macOS with Apple silicon. Linux and WSL2 follow the same shell workflow. Native Windows is expected to work but is less heavily exercised.

---

## Installation

Clone this repository and DeepMind's public SynthID-Text repository beside each other:

```bash
mkdir -p "$HOME/src"
cd "$HOME/src"
git clone https://github.com/jensabrahamsson/text-watermark-laboratory.git
git clone https://github.com/google-deepmind/synthid-text.git
cd text-watermark-laboratory
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

Install the lab and attach the SynthID-Text checkout:

```bash
pip install -e ".[jax-cpu,dev]"
pip install -e "$HOME/src/synthid-text" --no-deps
```

The project intentionally pins:

```text
transformers==4.57.6
```

Transformers 5.x can make GPT-2 generation with the mixin stop at EOS before the requested minimum length. The compatibility shim in `generate.py` keeps the public mixin working on 4.57.6.

Verify the setup:

```bash
python -m pytest tests/ -q
```

---

## First reference measurement

Score a known marked sample:

```bash
python -m text_watermark_tools score \
  experiments/2026-08-17-pair-12x4/01-harbour-marked.txt
```

Typical output:

```text
... mean=0.623224 weighted_mean=0.641979 n_tokens=126 n_unmasked_ngrams=122 instance=public-deepmind-30 ngram_len=5
```

Now score its unmarked twin:

```bash
python -m text_watermark_tools score \
  experiments/2026-08-17-pair-12x4/01-harbour-unmarked-gen.txt
```

Typical mean:

```text
0.508333
```

The public reference detector cleanly separates the known marked and unmarked laboratory twins.

### Reading a `score` line

| Field | Meaning |
|---|---|
| `mean` | DeepMind reference mean for this instance |
| `weighted_mean` | Weighted version of the same measurement |
| `n_tokens` | Tokens processed |
| `n_unmasked_ngrams` | 5-grams included in the score |
| `instance` | Watermark key set being tested |
| `ngram_len` | Detector n-gram length |

A score around 0.60–0.65 with plenty of usable n-grams is strong evidence for the **tested public instance**. Around 0.50 means no measurable bias toward that key set.

Very short text may produce `nan` because there are too few n-grams.

---

## Score your own text

File:

```bash
python -m text_watermark_tools score /full/path/to/text.txt
```

Clipboard on macOS:

```bash
pbpaste | python -m text_watermark_tools score
```

Directory:

```bash
python -m text_watermark_tools score /full/path/to/folder
```

The default tokenizer is GPT-2, matching the bundled experiments:

```bash
python -m text_watermark_tools score path/to/text.txt --model gpt2
```

Tokenization affects n-gram boundaries, so compare scores produced under the same tokenizer.

---

## Shuffled-key control

A marked sample should score highly against the correct public keys and near chance against a shuffled control:

```bash
python -m text_watermark_tools score \
  experiments/2026-08-17-pair-12x4/01-harbour-marked.txt \
  --control-shuffled-keys
```

Typical pattern:

```text
public-deepmind-30   ≈ 0.62
control-shuffled-30 ≈ 0.50
```

This is a useful sanity check that the measured bias follows the correct key set.

`contrast` asks the same question of the **key-free** reader. Fit public
marked/unmarked tables. Score `*-control-gen.txt` sampled with
`control-shuffled-30`. See [research/key-free-contrast.md](research/key-free-contrast.md).

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --control-only --n-samples 4 --max-new-tokens 128 --seed 20260931 \
  --out-dir experiments/2026-08-31-pair-12x4-controlkeys

python -m text_watermark_tools contrast experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --control-dir experiments/2026-08-31-pair-12x4-controlkeys \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4
```

On that 4-token poshits gate, control isolated `lr>0` is **0/48**. Public
vs control ranks **12/12** (AUC **0.906**). That is instance-specificity
without keys, not key recovery. Observed-token `postokhits` on the same
pile is also **0/48** control `lr>0` (public isolated **16/48**). See
[research/key-free-tokhits.md](research/key-free-tokhits.md).

Unbucketed prefix-4 rankpath on the same split ranks control with
unmarked (AUC **0.511**, isolated **6/48**). Opening rankuni does not
(control **30/48**). See [research/key-free-rankpath.md](research/key-free-rankpath.md).

```bash
python -m text_watermark_tools contrast experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --control-dir experiments/2026-08-31-pair-12x4-controlkeys \
  --fit-prefix 5 --pos-bucket 0 --methods rankpath,rankuni \
  --out-dir experiments/2026-08-31-contrast-36x4-to-12x4-prefix4-rankpath
```

---

## Run the key-free experiment

Generate matched twins:

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --out-dir experiments/pairs --max-new-tokens 128
```

Run leave-one-out comparison:

```bash
python -m text_watermark_tools blind experiments/pairs \
  --out-dir experiments/blind
```

`n_marked_wins` is prompt-mean ranking, not per-file accuracy. The same
command now prints `ranking_without_isolated_tp` (ranking wins with no
marked file `lr>0`) and `ranking_losses_with_isolated_tp` (ranking losses
that still have isolated TPs). Isolated sign is `marked_lr_positive`.
On the recounted 12×4 last-4 run that is garden vs station / office /
ferry-queue. Do not rewrite **9/12** or **25/48**.

For the stronger 12-prompt × 4-draw experiment:

```bash
python -m text_watermark_tools indicate holdout \
  experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4
```

The key point is that the held-out decision is made without calling `detector_mean`.

---

## Fit and use the key-free indicator

Fit reusable token/context tables:

```bash
python -m text_watermark_tools indicate fit \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/indicator-gpt2 \
  --context-len 4
```

Score a file:

```bash
python -m text_watermark_tools indicate score path/to/text.txt \
  --tables experiments/indicator-gpt2
```

The output contains `lr`, a log-likelihood ratio, and `n_used` (how many
positions had table coverage).

- positive `lr`: more similar to the learned marked distribution
- negative `lr`: more similar to the learned unmarked distribution
- `n_used=0` / `decision=ABSTAIN`: no overlapping atom; this is not
  “unmarked”. Observed-token tables cannot score a novel opening.
  See [research/key-free-cascade.md](research/key-free-cascade.md).
- Opening poshits tables can have `n_used>0` from Laplace on an unseen
  next token (`The`→` ferry`). Isolated `indicate score` then prints
  `occupancy_only=true` and `decision=ABSTAIN`. That is not a watermark
  call. `--score-mode postokhits` scores observed tokens only. Probe
  `--methods poshits` on the frozen lock B experiment is unchanged.

Hashpool tables (the 35/48 isolated reader) are a different persist:

```bash
python -m text_watermark_tools indicate fit \
  experiments/2026-08-17-pair-12x4 \
  --method hashpool \
  --out-dir experiments/indicator-gpt2-hashpool

python -m text_watermark_tools indicate score path/to/text.txt \
  --tables experiments/indicator-gpt2-hashpool
```

Count tables also accept `--score-mode hits` (shared 4-grams only). Nested
out-of-family hashpool tables, with a train-only `decision_threshold`, are in
`experiments/2026-08-31-transfer-nested-36-to-12x4/tables-hashpool/`.

Tiny key-free learned scorers (`hashlog`, `tokmlp`, `charcnn`) use the same
twins and grains. They do not use keys. They are not a universal detector.
See [research/key-free-learn.md](research/key-free-learn.md).

```bash
python -m text_watermark_tools learn experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/learn-36x4-to-12x4
```

`contrast` is documented with the shuffled-key control above and in
[research/key-free-contrast.md](research/key-free-contrast.md).

UTF-8 surface tables need no tokenizer:

```bash
python -m text_watermark_tools indicate fit \
  experiments/2026-08-17-pair-36 \
  --method surface \
  --out-dir experiments/indicator-gpt2-surface

python -m text_watermark_tools indicate score path/to/text.txt \
  --tables experiments/indicator-gpt2-surface
```

That is a genuine indicator signal, but its calibration depends on the training corpus. Leave-one-of-12-out hard last-4 still overlaps at threshold 0 (**25/48** after the counting fix; the published **29/48** overcounted truncated openings). Hits trained on other topics marks **39/48** of those same 12×4 files. Nested hashpool Youden on that split is **33/48** marked and **34/48** unmarked. Do not turn the sign of one LR into a universal yes/no claim.

`contrast` is a different grain: the same 4-token poshits tables assign
`lr>0` to **0/48** control-shuffled-30 files and still rank public vs
control **12/12**. See [research/key-free-contrast.md](research/key-free-contrast.md).

The strongest *prompt-group* evidence currently comes from matched/repeated prompts, where the original hard indicator reaches **9/12** after the counting fix, or **10/12** under the documented 0.02 comparison margin. `hits` reaches **10/12** with no margin. `indicate holdout --score-mode hashpool` leave-one-outs the hash buckets.

`indicate holdout` also prints a single-file **AUC** and a label-permutation p-value. The isolated sign at threshold 0 is **25/48**; ranking of the same LRs is the fairer isolated-file summary.

See [research/key-free-twins.md](research/key-free-twins.md) and [research/key-free-probe.md](research/key-free-probe.md).

---

## Compare key-free scorers (`probe`)

Count tables are not the only way to read paired twins. `probe` leave-one-prompt-outs several key-free scorers on the same corpus and reports prompt-grain wins plus single-file AUC:

```bash
python -m text_watermark_tools probe \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/probe
```

`atoms` decodes frozen interpolate tables into per-window mean Δ and
the most common observed-token 4-grams. It is not a new scorer and not
`detector_mean`. On the 100 one-liner → Grok-register split, almost all
mass is Witten–Bell backoff; occupancy-free openings stay **0/48**.

```bash
python -m text_watermark_tools atoms \
  experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-last4/tables-counts \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-01-atoms-100x4-to-grok12x4-interpolate

python -m text_watermark_tools atoms \
  experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4/tables-counts \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-01-atoms-grok36x4-to-12x4-interpolate
```

`--pivot` adds an unmarked-LM choice-geometry probe (loads GPT-2; slower; still no watermark keys). `--rankpath` fits five-symbol tables on those same unmarked-LM ranks (no token identity); `--cascade-fallback rankuni` uses the rank unigram when count tables abstain. `--pivot-weight entropy` pools near-ties; `--cascade postokbackoff` uses the count LR when `n_used>0` and the fallback otherwise (signs at 0 are comparable; mixed AUC is not a detector). `--extra-train DIR` adds train twins on `--test-dir` transfer. `--score-mode` on `indicate holdout` selects one count scorer (`interpolate`, `gated`, `mix`, `hashpool`, `surface`, …). `--test-dir` on `probe` fits one twin directory and scores another (out-of-family transfer). `--shuffle-labels` is a negative control. Nested Youden / 10% FPR thresholds come from leave-one-prompt-out on the training stems only. `--max-draws N` keeps the first N marked/unmarked draws per stem (draw-count ablation). `--prefix-lens 16,32,64,96,128` scores token prefixes as isolated-file curves (in-domain 16 tokens already ranks **34/36**). `--windows 0:16,16:32,32:64,64:128` scores disjoint slices so later tokens are not mixed with the prefix. `--fit-prefix 16` clips every draw *before fit and score* (matched prefix; not the same as scoring a prefix of a full-file table). `--methods poshits,poshitmass,pospool --pos-bucket 16` namespaces last-4 counts by token position so early 4-grams do not share a bucket with the tail. `--coverage` reports the leave-one-out share of last-k contexts seen on both training sides, by token window; that is why the 4-gram reader is front-loaded. `poshitmass` is coverage-weighted hits on those same bucketed tables. Nested Youden / 10% FPR from leave-one-prompt-out on the *training* stems now includes poshits/poshitmass. `--include-first` also scores generated token 0 (the published reader skips it). `--prompt-context` uses `*-prompt.txt` as last-k so token 0 sees the mixin prompt; isolated `indicate score` of a lone file cannot do that. `--methods first` is token 0 alone. Leave-one-out `probe` also reports **nested-youden-by-stem**: a threshold fitted on other prompts' already-held-out LRs, then applied to this prompt.

These methods do not reconstruct keys. Hash pooling is a random feature-hash of contexts, not SynthID’s secret hash. `hashtok` is that same mixer without occupancy Laplace: skip a hash unless the observed next token appeared in the bucket. On 60-stem prefix-5, hashtok’s 30 true positives equal `postokhits`; hashpool’s extra four (letter d2’s official 5-gram among them) are empty-cell occupancy. `hashtoklen` at that grain is **21/48**: 20 TPs match `postokhits`, and harbour d2 `The ferry was over ,` is a hashed collision (1/8 hashes, c_m=11, c_u=0) where the exact 4-gram is unmarked-like. Letter d2 still abstains. `--cascade hashtoklen --cascade-fallback rankpath` is **33/48 vs 37/48**. Prefix-4 exact backoff **35/48** (mixed backoff had hurt: 31/48). GPT-2 60-stem hashtoklen tables on Distil AUC **0.571**. Occupancy-free drop-one skip-grams (`hashskip`) are **25/48 vs 35/48** at t=0 and nested Youden **16/48 vs 41/48**; letter d2's official `I` is seen unmarked-only. `hashtoklen2` skips singleton collisions on the same 5-gram tables: **10/48 vs 48/48**, precision 1.0; 11 of 21 hashtoklen TPs were singletons; harbour d2 survives (c_m=11). Count-weighting those hashes keeps 21/48 (no singleton+dense mix; rain d1 n=7 vs n=8). `hashtoklen2` plus prefix-4 rankpath is **28/48 vs 40/48** (copies rankpath). Occupancy-free MASK replace (`hashmask`) is **21/48 vs 42/48** at t=0 and nested Youden **19/48 vs 45/48**, worse than hashtoklen; letter d2's official slot is two opposing singletons (lr=+0.240). In-domain full-file hashtok is **33/48 vs 22/48**, nested-by-stem **22/48 vs 30/48**. `--n-hashes 2` on that mixer is **34/48 vs 31/48**, nested **28/48 vs 37/48** (prompt **11/12**, AUC **0.764**); `--n-hashes 4` is **36/48 vs 30/48**, nested **35/48 vs 30/48**; `--n-hashes 16` copies 36/48 at t=0 with nested spec **24/48**; `--n-hashes 32` hurts (30/48, nested **21/48 vs 38/48**). Default n=8 is not the best in-domain width at seed 20260831; that n=2 win is seed-confounded (spec 21–31/48); 24→12 nested Youden prefers n=8 (**17/48 vs 46/48**). Keep the CLI default. Do not sell 36/48, 35/48, 34/48, 31/48, 19/48, or 17/48. OR with hard last-4 indicate is **39/48 vs 12/48**, combined **51/96** (worse than indicate 52/96); nested LDA **21/48 vs 37/48**. Do not sell 39/48. `tokhybrid` copies in-domain hashtok **33/48 vs 22/48** (prompt **11/12**); `poshashtok` nested **14/48 vs 38/48**. `hashtokgap` (hashtok only where tokhits abstains) is **27/48 vs 21/48**, nested **17/48 vs 31/48**, a strict subset of hashtok's 33 TPs. `hashtok2` (unbucketed min_count=2) is **34/48 vs 21/48**, nested **19/48 vs 35/48**, a sign reshuffle not a singleton core. In-domain `--fit-prefix 4` occupancy-free hashing copies tokhits density, not opening rankpath **41/48**: tokhits **23/48 vs 48/48** (prompt **12/12**); hashtok **24/48 vs 47/48** (nested **23/48 vs 47/48**, extra TP letter d3 only); hashtok2 **22/48 vs 48/48**. Letter d2 is zero at that grain. Marked isolated recall **24/48** is below hard last-4 **25/48**. Do not sell 34/48, 33/48, 28/48, 27/48, 24/48, 23/48, 22/48, 21/48, 25/48, 19/48, 16/48, or 10/48 as beating poshits **39/48**. `hashtokbackoff` / `hashtokbackoff2` fit separate hashpool tables per last-k order and keep the longest occupancy-free hit. Those tables also hash short prefixes into longer-order mixers: prefix-5 t=0 **38/48 / 36/48** is that collision plus last-1; nested Youden stays **30/48**. `hashtoklen` / `hashtoklenbackoff` hash only exact last-k. Prefix-5 hashtoklen is **21/48** (official 5-gram slot only). Exact backoff nested Youden is **33/48 vs 42/48**. Letter d2’s official `I` is last-1 unmarked; exact backoff2 lr=0.797 is last-2 `'Now in' → ' the'`. On the published prefix-4 opening, mixed hashed backoff **hurts** versus hashtok (**31/48** vs **35/48**). Do not sell 38/48, 36/48, 35/48, or 33/48 as beating poshits **39/48**. `surface` hashes UTF-8 bytes of the raw string. On the 12×4 corpus, `hits` and `hashpool` both reach **11/12** prompt groups; hashpool’s isolated sign is **35/48**. Trained on 24 other topics, hits marks **39/48** of the 12×4 files (AUC 0.769); nested hashpool Youden is **33/48** vs **34/48**. Four training draws lift that ranking to **12/12** and **42/48** at t=0 (nested hits Youden 26/48 vs 44/48). Train 12×4, score 96 new-topic 36×4 files: nested hits 10% FPR **83/96** vs **85/96**. A 16-token prefix of the 36×4 twins already ranks **34/36** in-domain (AUC 0.916); matching mixin `ngram_len=5` does not beat last-4. A matched 16-token fit lifts unmarked ≤0 to **112/144** in-domain (AUC 0.929) and OOD file AUC to **0.818**. Position-bucketed hits keep 134/144 marked at t=0 on 36×4 with unmarked ≤0 **97/144**, and raise OOD file AUC to **0.811**. `--coverage` shows why the reader is front-loaded: token index 1 is **96.9%** shared last-1. Scoring only **0:4** already ranks **34/36** (AUC **0.917**). A matched 4-token fit with `--pos-bucket 1` balances in-domain t=0 at **131/144 vs 132/144**, and on 24 other topics ranks 12×4 **12/12** (AUC **0.873**, isolated **39/48 vs 41/48**, nested Youden matching t=0). That 39/48 includes The-Laplace occupancy; `--methods poshits,postokhits` keeps only next tokens seen in train (**16/48**, precision 1.0 among decided files). Twelve medium-length new topics lift that observed-token isolated recall to **19/48** (20/48 with the short one-liners); the nine After / Closing / Now / While zeros remain. `--methods postokbackoff` shrinks last-k until an observed next token hits: **21/48** on the medium train, **22/48** combined; it copies **16/48** on the short one-liner gate. `postokbackoff2` will not shrink below last-2: that core is **13/48** on every train set in the opening-overlap curve (24 short, +medium, +tails). `python -m text_watermark_tools openings TRAIN --test-dir TEST --extra-train …` reports that isolated recall equals train atom overlap. Unbucketed last-1 copies 36/48 with 3 unmarked FPs. `--include-first` on postokhits is a first-token unigram (43/48, 10 FP). Last-1 on those four tokens copies that OOD gate. Mixing token 0 into hits hurts it (9/12). Qwen's in-domain opening is first-token **12/12** (AUC **0.901**); hits without token 0 is 7/12. DistilGPT2 is officially 12/12; GPT-2 tables do not transfer across the shared tokenizer (hits 5/12, AUC 0.462). That GPT-2 isolated-file gate does not appear under leave-one-of-12-out (9/12) and does not transfer to Qwen. GPT-2 36×4 → new Qwen stays at chance. Witten–Bell interpolation did not help on 12×4. Opening-only unmarked-LM geometry (4 generated tokens, no prompt) is stronger in-domain than the published 128-token pivot (10/12, AUC 0.672, 27/48 vs 17/48) and does not transfer as a calibrated OOD isolated-file reader; prompt-conditioned opening LDA is worse than chance under leave-one-prompt-out. `indicate score` prints `decision=ABSTAIN` when `n_used=0`. `--cascade-when positive` also sends covered-negative count files to the fallback (60-stem prefix-4: **40/48 vs 40/48**, 8 FPs; not 39/48). Rank-path tables on the same 4-token openings reach in-domain **12/12 / 41/48** and OOD **10/12 / 28/48**; they are not 29/48 and not a calibrated detector. Unbucketed full-file rank-path is chance (8/12); a matched prefix of four rank symbols transfers **11/12** with isolated **25/48 vs 43/48**. Native Distil opening rankpath is chance (**8/12**, AUC **0.579**) despite official 12/12; Qwen opening rankpath is **8/12** against first-token **12/12**. 60-stem prefix-4 standalone is **10/12**, **28/48 vs 40/48** (same 68/96 combined as 24-short). `--rankpath-full` keeps rank symbols from the unclipped file when count tables use `--fit-prefix`. `--snaprate` is the table-free baseline on the same unmarked-LM rows: `snapleave` (not argmax), `snapupset` (in-topk not argmax), `snapmiss` (missed top-k). Opening `snapupset` is chance (**7/12**, AUC **0.501**); `snapleave` majority vote is not a detector; `snapmiss` ranks **10/12** with isolated **21/48 vs 41/48** and is already inside opening LDA. Rank-path tables are not a dressed-up upset bit. See [research/key-free-probe.md](research/key-free-probe.md), [research/key-free-tokhits.md](research/key-free-tokhits.md), [research/key-free-hashtok.md](research/key-free-hashtok.md), [research/key-free-cascade.md](research/key-free-cascade.md), [research/key-free-rankpath.md](research/key-free-rankpath.md), [research/key-free-snaprate.md](research/key-free-snaprate.md), [research/related-work.md](research/related-work.md), and [research/CITING.md](research/CITING.md).

## Key-free argmax snap (`scrub`)

Tournament sampling only reweights the unmarked model’s top-k. Snapping each token to that argmax, using the original prefixes, is a key-free scrub. Official `score` afterwards is a reference check, not part of the snap:

```bash
python -m text_watermark_tools scrub \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/scrub
```

This is not a fluent rewriter. It asks whether the public mark dies when tournament “upsets” are removed. On the 12×4 marked twins the official mean went **0.622 → 0.499**.

`--snaprate` is the matching *detection* baseline: the same unmarked-LM rows, no twin tables, no keys. Opening `snapupset` is chance (**7/12**, AUC **0.501**): marked and unmarked leave the greedy top-k token at the same rate. `snapmiss` ranks **10/12** (isolated **21/48 vs 41/48**) because marked openings sit off-mode; that is already inside opening LDA, not a new isolated-file headline. Rank-path tables ask *which* rank was chosen; binary snap-rate is not a substitute. See [research/key-free-snaprate.md](research/key-free-snaprate.md).

```bash
python -m text_watermark_tools probe \
  experiments/2026-08-17-pair-12x4 \
  --methods snapleave,snapupset,snapmiss \
  --skip-hashpool \
  --fit-prefix 4 \
  --out-dir experiments/2026-09-01-probe-12x4-fitprefix4-snaprate
```

Matched opening occupancy-free hashing on the same 12×4 twins copies tokhits density (**24/48**), not opening rankpath **41/48**:

```bash
python -m text_watermark_tools probe \
  experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --methods hits,tokhits,hashtok,hashtok2 \
  --out-dir experiments/2026-09-01-probe-12x4-fitprefix4-hashtok
```

In-domain full-file `--n-hashes` on that same mixer: default n=8 is **not** the best width on 12×4 LOO. n=2 is **34/48 vs 31/48**, nested **28/48 vs 37/48**, AUC **0.764**. n=4 is denser at t=0 (**36/48 vs 30/48**, nested **35/48 vs 30/48**). n=16 copies 36/48 with nested spec **24/48**. n=32 hurts (**30/48**, nested **21/48 vs 38/48**). That in-domain win does **not** transfer: 24 new 36×4 stems → 12×4 nested Youden prefers n=8 (**11/12**, **29/48 vs 35/48**, nested **17/48 vs 46/48**) over n=2 and n=4. It is also seed-confounded: n=2 unmarked spec ranges **21–31/48** across feature-hash seeds; default seed 20260831 is a lucky n=2 mixer; n=8 seed 7 nested **28/48 vs 37/48**. Transfer n=8 at that seed is likewise lucky: other n=8 seeds drop prompt to 10/12; n=2 seed 7 nested **19/48 vs 47/48**. Keep the frozen protocol (`n_hashes=8`, seed `20260831`). Do not fish a seed. Occupancy-free last-k at that frozen mixer: in-domain last-1 is chance (**5/12**); last-3 prompt **11/12** has t=0 **24/48**, below hard last-4 **25/48**. 24→12 last-4 still wins prompt ranking and nested FPR10 (**17/48 vs 46/48**); last-2 file AUC **0.738** is ranking (nested **15/48**); last-1 nested **18/48** has prompt **7/12**. Keep `--context-len 4`. Do not sell 36/48, 35/48, 34/48, 31/48, 24/48, 19/48, 18/48, or 17/48 as replacing **25/48**. Occupancy-free order/width/seed on this corpus is closed. Next measurement: [research/PROTOCOL-next.md](research/PROTOCOL-next.md).

```bash
python -m text_watermark_tools probe \
  experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 2 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-nhashes2

python -m text_watermark_tools probe \
  experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 8 \
  --out-dir experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8

python -m text_watermark_tools probe \
  experiments/2026-08-17-pair-12x4 \
  --methods hashtok --context-len 3 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-k3

python -m text_watermark_tools probe \
  experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashtok --context-len 2 \
  --out-dir experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-k2
```

---

## Rewriting a known-marked sample

```bash
cp DASHSCOPE-KEY.conf.example DASHSCOPE-KEY.conf
python -m text_watermark_tools iterate path/to/marked.txt \
  --backend qwen \
  --out-dir experiments/iterate
```

For a light-edit control:

```bash
python -m text_watermark_tools iterate path/to/marked.txt \
  --backend qwen \
  --via polish \
  --out-dir experiments/iterate-polish
```

The rewrite experiments ask how an already-known mark changes under paraphrase or light editing. They are separate from the key-free classification experiment.

Keep API credentials in the gitignored config files or environment variables, never in tracked files or command-line arguments.

---

## Claude and other production systems

The public DeepMind key set is a reference instance, not a universal SynthID key.

A provider can use the same family of watermarking method with different keys, tokenization, hashing, depth, and thresholds. In that case the public `score` is simply testing the wrong instance.

That is exactly why the key-free work is interesting: a paired before/after corpus can reveal statistical changes without assuming access to the production detector.

For the Claude plan, see:

- [research/claude.md](research/claude.md)
- [research/paired-corpus.md](research/paired-corpus.md)

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named text_watermark_tools` | Activate `.venv` and reinstall the project |
| `No module named synthid_text` | Install the DeepMind checkout with `--no-deps` |
| JAX/CUDA errors on macOS | Use the `jax-cpu` extra |
| Generation stops too early | Confirm `transformers==4.57.6` |
| `mean=nan` | Use a longer text |
| `indicate` is near zero | The one-file signal is weak; aggregate or use matched evidence |

Rerun the tests at any time:

```bash
source .venv/bin/activate
python -m pytest tests/ -q
```

---

## Where to go next

- [README.md](README.md) — project and current result
- [research/key-free-twins.md](research/key-free-twins.md) — experimental protocol and key-free indicator
- [research/how-synthid-works.md](research/how-synthid-works.md) — implementation details
- [experiments/README.md](experiments/README.md) — experiment index
