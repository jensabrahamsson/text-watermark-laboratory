# Narrative freeze (not a paper)

This file locks the **story** of the key-free work. It is not
`thesis/`, not a draft article, and not a new scorer. Isolated-file
detection is **not finished**. Author–year citations follow
[CITING.md](CITING.md).

Headlines after the truncated-context recount remain **9/12**,
**25/48**, and **36/36**. Pre-fix **10/12** / **29/48** stay in
historical JSON. Do **not** write `thesis/` from this file.

A suggested external title of the form "Why Key-Free Watermark Detection Fails"
is **wrong for this laboratory**. Prompt-group ranking
without keys is real. Isolated-file classification at `lr>0` is weak.
Those are two grains. Collapsing them into a single failure claim
weakens a result this repository already has, which
[AGENTS.md](../AGENTS.md) forbids.

That title is a slogan, not a measurement. How to write an indication:
[CITING.md](CITING.md). This laboratory **did not refute** Christ et al.
(2024) or Zhang et al. (2024). Those papers prove claims about a
different construction and different oracles. They are not a proof that
count tables must fail on `public-deepmind-30`. Lock A prompt-group
ranking **99/100** is a scoped measurement, not a complexity-theoretic
distinguisher against their scheme. Isolated **25/48** is a different
grain, not a restoration of those theorems. Placement:
[related-work.md](related-work.md). Do not write `thesis/` from this
file.

## Two grains, not one arc of collapse

```
matched marked/unmarked twins
        │
        ├─ prompt-group ranking (mean LR per stem)
        │    12-LOO hard last-4 **9/12** (margin 0.02 → 10/12)
        │    36×4 hits **36/36**
        │    100×4 lock A **99/100**
        │    Distil lock B **89/100**; Qwen lock B **95/100**
        │
        └─ isolated file (one LR against 0)
             12-LOO hard last-4 **25/48 vs 22/48** (binomial ≈ 0.44)
             leftover occupancy-free zeros **10/20 vs 11/20** (chance)
             occupancy-covered **15/28** of those 25 TPs
```

The “initial success” of **10/12** / **29/48** was truncated-context
overcount (`(10,)→20` stored four times at `context_len=4`). After the
recount, prompt ranking is still **9/12**, not chance. Confirmatory
100-family ranking is **99/100**. That is not an illusion that later
“deconstructs” to **25/48**. **25/48** was always the isolated-file
grain. Ranking and isolated sign disagree on stems (garden ranks with
0 TPs; station/office/ferry-queue hold 5 of 25 TPs, all leftover).

Kirchenbauer et al. (2023) and Dathathri et al. (2024) are the sampling
watermarks this lab measures against. Wang et al. (2026) is the closest
published analog for third-party, key-agnostic verification
([related-work.md](related-work.md)). This freeze is not a priority
claim over that work.

## What the artifacts actually did

| Artifact | What it changed | What it did not do |
|---|---|---|
| Truncated-context overcount | Pre-fix **10/12** / **29/48** → recount **9/12** / **25/48** | Did not erase prompt-group ranking |
| Occupancy Laplace / Witten–Bell backoff | Inflated isolated recall (poshits **39/48**; interpolate nested **26/48** ≠ occupancy-free **10/48**) | Did not create 9/12 or 99/100 from noise |
| Opening n-gram overlap (`'The'→' car'`, `Closing`) | Occupancy-free isolated recall equals train opening coverage | Not a recovered SynthID payload, not keys |
| In-family vs out-of-family | Nested Youden **23/48** (100→original 12) does not beat **25/48**; same-register 36×4 is **109/144** | Not “OOD collapse of the whole method” |

Grok12 window **0:4** is opening overlap, not a hidden bit. Occupancy-free
postokhits `lr>0` iff `n_used>0` iff an observed next token sits in the
train atom set. On grok36→grok12 that bound is **39/48**, equal to
coverage, and window 0:4 marked Δ is dominated by `'The'→' car'`
(n=19). Tail windows are still backoff. That identity is already in
[PROTOCOL-isolated-scale.md](PROTOCOL-isolated-scale.md) and the
`atoms` dumps. It does not replace **25/48**.

PROTOCOL-next **H3** is a generator-specificity prediction: lock C
(rankpath) drops more than lock B (poshits) on Distil and Qwen. It is
not a third detection hypothesis for isolated files.

## Locked tables (published numbers only)

These are Gemini Loop 2 tables assembled from already-opened JSON.
They are not new `probe --methods` names.

### Headline vs ablated isolated sign

| Claim | Grain | Number | Ablation |
|---|---|---|---|
| Pre-fix hard last-4 | Prompt / isolated | 10/12, 29/48 | Truncated-context overcount; historical JSON only |
| Recount hard last-4 | Prompt / isolated | **9/12**, **25/48** | Locked headline |
| Hits (shared 4-grams) | Prompt | **10/12**, AUC **0.718** | Same twins, coverage gate |
| Occupancy poshits | Isolated t=0 | **39/48** vs **41/48** | Laplace on unseen next; not **25/48** |
| Occupancy-free postokhits | Isolated t=0 | **16/48** on that OOD gate | Observed tokens only |
| Leftover vs covered of 25 | Isolated TPs | leftover **10/20 vs 11/20**, covered **15/28** | [PROTOCOL-isolated-split.md](PROTOCOL-isolated-split.md) |

### Nested Youden vs occupancy-free transfer

| Train → test | Nested Youden | Occupancy-free t=0 | Coverage |
|---|---|---|---|
| 100 one-liners → original 12 | lock A **23/48 vs 38/48** | **16/48** | **18/48** |
| 100 one-liners → 36×4 | lock A **109/144 vs 122/144** | — | **117/144** |
| Grok-register 12 → original 12 | lock A **16/48 vs 41/48** | **5/48** | **5/48** |
| 100 one-liners → grok12 | lock A **22/48 vs 41/48** | **0/48** | **5/48** |
| grok36 → grok12 | lock A **36/48 vs 39/48** | **39/48** | **39/48** |
| grok36 → original 12 | lock A **26/48 vs 33/48** | **10/48** | **10/48** |
| 100+grok36 mixed → original 12 | interpolate **27/48 vs 39/48** | **26/48** | **28/48** |

None of those occupancy-free or nested counts replace **25/48**.

### Cross-generator (published; not a new pair)

| Train | Test | Reader | Prompt | Isolated / note |
|---|---|---|---|---|
| GPT-2 12×4 LOO | same | hard last-4 | **9/12** | **25/48** |
| DistilGPT2 12×4 LOO | same | hits | **9/12** | official **12/12** |
| DistilGPT2 12×4 LOO | same | opening rankpath | **8/12** | chance (AUC **0.579**) |
| Qwen2-1.5B 12×4 LOO | same | hits | **8/12** | first-token **12/12** |
| Qwen2-1.5B 12×4 LOO | same | opening rankpath | **8/12** | not first-token 12/12 |
| GPT-2 36×4 | Distil 12×4 | hits | **5/12** | AUC **0.462** |
| GPT-2 36×4 | Distil 12×4 | rankpath | **9/12** | **21/48** |
| GPT-2 36×4 | new Qwen 12×4 | hits | **6/12** | chance (AUC 0.445) |
| GPT-2 100×4 | Distil 100×4 | official / B / C | **70 / 89 / 69** | H3: C drops more |
| GPT-2 100×4 | Qwen 100×4 | official / B / C | **100 / 95 / 84** | H3: C drops more |

In-domain occupancy can rank. Cross-generator count tables do not
become a tokenizer-universal isolated-file detector. GPT-2 learned
scorers → Distil / Qwen are chance.

## What remains (isolated-file)

Leftover occupancy-free zeros on the original 12 are **20** files.
In-domain hard last-4 on that slice is **10/20 vs 11/20**. Mixed
opening rankpath is **12/20 vs 14/20**. In-domain opening rankpath
leftover is **16/20 vs 16/20**. The leftover files even in-domain
rankpath misses are letter-2 (`Now in the second`), office-4, garden
1/4. Do not target new train prompts at those openings after peeking.

Spatial ablation of the **headline** 12-LOO hard last-4 scorer (mask
first *k* generated tokens with existing `--windows`) is
[PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md). Opened: hard
prefix **0:4** is **5/12**; tails **4:128** and **8:128** stay **9/12**.
Interpolate is front-loaded; hard is not. Isolated t=0 stays chance-like.
Do not sell prefix **10/12** or tail **9/12**.

Leftover versus occupancy-covered on those windows is
[PROTOCOL-isolated-mask-split.md](PROTOCOL-isolated-mask-split.md).
Hard 4:128 leftover is **11/20 vs 11/20**; covered **16/28**. Tail
**9/12** is occupancy-covered ranking, not leftover-file recall.
Prefix 0:4 isolated **29/48** is **12 leftover + 17 covered**. Do not
sell leftover **11/20**, covered **16/28**, or window **29/48**.

Whether those leftover-20 files are still officially marked, and
whether leftover interpolate mass is still backoff, is
[PROTOCOL-isolated-leftover-bound.md](PROTOCOL-isolated-leftover-bound.md).
Opened: leftover-20 official full-file mean **0.624**, **20/20** above
0.55. Prefix-5 **18/20**. Leftover interpolate 0:4 is unseen **99 vs
21**; seen mass is `'Cl'→'osing'`; leftover `lr>0` **13/20**. Leftover
key-free chance is not an unmarked mixin miss. Do not sell official
**20/20** or interpolate **13/20**.

Whether short+medium+tails openings cover any leftover-20 files is
[PROTOCOL-isolated-leftover-union.md](PROTOCOL-isolated-leftover-union.md).
Opened: union **30/48** equals published SMT coverage (mixed 100+grok36
is a subset). SMT-only covers are garden 1/4. Leftover after union is
**18**. Leftover last-4 is **10/18 vs 10/18**. Occupancy-free mixed
leftover sign is 0/18 by construction. Do not sell union **30/48** or
leftover **10/18**.

Occupancy-free leftover-18 is closed for more unrelated GPT-2 scenes
([PROTOCOL-isolated-occupancy-closed.md](PROTOCOL-isolated-occupancy-closed.md)).
Leftover-18 official is **18/18** at prefix-128 by subset of leftover-20
**20/20**. Prefix-5 is **16/18**. Do not add family-12 paraphrases or
target leftover openings after peeking. Do not sell leftover official
**18/18**.

Mixed opening rankpath and grok36 interpolate on leftover-18 are
[PROTOCOL-isolated-leftover-18.md](PROTOCOL-isolated-leftover-18.md).
Opened: leftover-18 mixed rankpath **12/18 vs 13/18**; grok36 interpolate
**12/18 vs 12/18**; leftover-18 interpolate 0:4 unseen **89 vs 19**.
Garden leftover had 0 mixed rankpath TPs. Do not sell leftover-18
rankpath **12/18** or leftover-18 interpolate **12/18**.

Leftover-18 published key-free readers are closed
([PROTOCOL-isolated-leftover-18-closed.md](PROTOCOL-isolated-leftover-18-closed.md)).
Do not re-slice more leftover-18 holdouts as leftover-file detection.
Distil occupancy-free leftover-18 on the original 12 is
[PROTOCOL-isolated-xgen.md](PROTOCOL-isolated-xgen.md). Opened:
Distil occupancy-free t=0 **22/48 vs 43/48** (beats GPT-2 lock B occupancy-free
**16/48**, not **25/48**); leftover-18 Distil coverage **3/18** (office
1/3/4). Isolated recall equals Distil opening overlap **23/48**. Do not
sell Distil **22/48** or leftover Distil **3/18**. Distil 100×4 → Distil
12×4 occupancy-free analog is
[PROTOCOL-isolated-dgen.md](PROTOCOL-isolated-dgen.md). Opened:
Distil→Distil postokhits t=0 **16/48 vs 39/48** equals coverage
**16/48**; not leftover-18; not **25/48**. Do not sell Distil→Distil
**16/48**. Qwen 100×4 → Qwen 12×4 occupancy-free analog is
[PROTOCOL-isolated-qgen.md](PROTOCOL-isolated-qgen.md) (not leftover-18;
not lock A; not `--include-first`).

## What this freeze refuses

- Writing `thesis/` or drafting Loop 3 sections as a paper.
- Selling leftover **10/20**, covered **15/28**, leftover window
  **11/20**, covered **16/28**, leftover official **20/20**, leftover
  interpolate **13/20**, union **30/48**, leftover **10/18**, leftover
  official **18/18**, leftover-18 rankpath **12/18**, leftover-18
  interpolate **12/18**, Distil occupancy-free **22/48**, leftover Distil
  **3/18**, Distil→Distil **16/48**, grok12 **39/48**, nested **23/48** / **26/48** /
  **27/48** / **35/48**, or rankpath **41/48** as replacing **25/48**.
- Using pre-fix **10/12** / **29/48** as the main result.
- Calling key-free indication a failure at prompt-group grain.
- New `probe --methods` names on the 12×4 / 36×4 twins.
- Mixing grok12 into grok36 train.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Re-running PROTOCOL-isolated-scale; that protocol is already open.

Human merge of PR #2 / PR #3 is out of scope for this file.
