# Narrative freeze (not a paper)

This file locks the **story** of the key-free work. It is not
`thesis/`, not a draft article, and not a new scorer. Isolated-file
detection is **not finished**. Author–year citations follow
[CITING.md](CITING.md). Locked abstract (shop window: what is new first):
[abstract.md](abstract.md). Report author line: Jens Abrahamsson,
Master of Science. Do not write `thesis/` from this file.

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
        │    Distil lock B **88/100** (1 tie); Qwen lock B **95/100**
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
published finished-string paired-reference analog for third-party,
key-agnostic verification
([related-work.md](related-work.md)). This freeze is not a priority
claim over that work. The notebook is empirically strong and
interesting; it is **not field-defining** and **not a finished conference paper** ([threat-model.md](threat-model.md)).

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

DistilGPT2 unmarked-LM opening rankpath 12-LOO on the original GPT-2
twins is ranking **10/12**, isolated **32/48 vs 31/48**
([PROTOCOL-isolated-rankpath-lm.md](PROTOCOL-isolated-rankpath-lm.md)).
H-rplm-d **fails** as a raw count. gpt2-medium-LM isolated is
**31/48 vs 32/48**. Do not sell **32/48** or **31/48**. Occupancy-free leftover unions stay closed.
Do not leftover-slice. Do not merge PR **#9**.
gpt2-medium native opening rankpath on gpt2-medium 12×4 is ranking
**6/12**, isolated **22/48 vs 30/48**
([PROTOCOL-isolated-rankpath-m12.md](PROTOCOL-isolated-rankpath-m12.md)).
H-rpm12 **holds**. Do not sell **22/48**.
GPT-2-small LM on those gpt2-medium twins is ranking **8/12**, isolated
**20/48 vs 32/48**
([PROTOCOL-isolated-rankpath-g2m.md](PROTOCOL-isolated-rankpath-g2m.md)).
H-rpg2m **holds**. Do not sell **20/48**.
Distil LM on those gpt2-medium twins is ranking **11/12**, isolated
**30/48 vs 31/48**
([PROTOCOL-isolated-rankpath-d2m.md](PROTOCOL-isolated-rankpath-d2m.md)).
H-rpd2m **fails** as a raw count. Do not sell **30/48**.
GPT-2-small LM on Distil 12×4 is ranking **6/12**, isolated
**24/48 vs 27/48**
([PROTOCOL-isolated-rankpath-g2d.md](PROTOCOL-isolated-rankpath-g2d.md)).
H-rpg2d **holds**. Do not sell **24/48**.
gpt2-medium LM on Distil 12×4 is ranking **9/12**, isolated
**30/48 vs 33/48**
([PROTOCOL-isolated-rankpath-m2d.md](PROTOCOL-isolated-rankpath-m2d.md)).
H-rpm2d **fails** as a raw count. Do not sell **30/48**.
Opening rankpath on generated tokens `[4:16)` is ranking **7/12**,
isolated **20/48 vs 22/48**
([PROTOCOL-isolated-rankpath-body.md](PROTOCOL-isolated-rankpath-body.md)).
H-rpbody **holds**. Do not sell **20/48**.
Distil-LM rankpath on generated tokens `[4:16)` is ranking **6/12**,
isolated **24/48 vs 23/48**
([PROTOCOL-isolated-rankpath-dbody.md](PROTOCOL-isolated-rankpath-dbody.md)).
H-rpdbody **holds**. Do not sell **24/48**.
gpt2-medium-LM rankpath on generated tokens `[4:16)` is ranking **9/12**,
isolated **27/48 vs 28/48**
([PROTOCOL-isolated-rankpath-mbody.md](PROTOCOL-isolated-rankpath-mbody.md)).
H-rpmbody **fails** as a raw count. Do not sell **27/48**.
Distil native rankpath on generated tokens `[4:16)` is ranking **9/12**,
isolated **25/48 vs 30/48**
([PROTOCOL-isolated-rankpath-d12body.md](PROTOCOL-isolated-rankpath-d12body.md)).
H-rpd12body **holds**. Equality with **25/48** is not a win. Do not sell **25/48**.
gpt2-medium native rankpath on generated tokens `[4:16)` is ranking **6/12**,
isolated **20/48 vs 30/48**
([PROTOCOL-isolated-rankpath-m12body.md](PROTOCOL-isolated-rankpath-m12body.md)).
H-rpm12body **holds**. Do not sell **20/48**.
GPT-2-small LM rankpath on Distil generated tokens `[4:16)` is ranking **4/12**,
isolated **26/48 vs 21/48**
([PROTOCOL-isolated-rankpath-g2dbody.md](PROTOCOL-isolated-rankpath-g2dbody.md)).
H-rpg2dbody **fails** as a raw count. Do not sell **26/48**.
Distil LM rankpath on gpt2-medium generated tokens `[4:16)` is ranking
**11/12**, isolated **25/48 vs 33/48**
([PROTOCOL-isolated-rankpath-d2mbody.md](PROTOCOL-isolated-rankpath-d2mbody.md)).
H-rpd2mbody **holds**. Equality with **25/48** is not a win.
GPT-2-small LM rankpath on gpt2-medium generated tokens `[4:16)` is ranking
**8/12**, isolated **28/48 vs 30/48**
([PROTOCOL-isolated-rankpath-g2mbody.md](PROTOCOL-isolated-rankpath-g2mbody.md)).
H-rpg2mbody **fails** as a raw count. Do not sell **28/48**.
gpt2-medium LM rankpath on Distil generated tokens `[4:16)` is ranking
**9/12**, isolated **32/48 vs 25/48**
([PROTOCOL-isolated-rankpath-m2dbody.md](PROTOCOL-isolated-rankpath-m2dbody.md)).
H-rpm2dbody **fails** as a raw count. Do not sell **32/48**.
GPT-2 rankpath on generated tokens `[16:32)` is ranking **7/12**,
isolated **23/48 vs 26/48**
([PROTOCOL-isolated-rankpath-mid.md](PROTOCOL-isolated-rankpath-mid.md)).
H-rpmid **holds**. Do not sell **23/48**.

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
[PROTOCOL-isolated-qgen.md](PROTOCOL-isolated-qgen.md). Opened:
Qwen→Qwen postokhits t=0 **31/48 vs 48/48**; coverage **37/48**; six
covered files have negative LR. Cross-corpus **31/48** > **25/48** does
not replace original-12 GPT-2. Do not sell Qwen→Qwen **31/48**.
Distil ∪ SMT occupancy-free openings on the original 12 is
[PROTOCOL-isolated-dsmt.md](PROTOCOL-isolated-dsmt.md). Opened:
union **33/48**; leftover **15**; last-4 **9/15 vs 8/15**; Distil-only
office 1/3/4. Do not sell union **33/48** or leftover **9/15**. Do not
target leftover-15 openings after peeking. Occupancy-free leftover-15
is closed
([PROTOCOL-isolated-leftover-15-closed.md](PROTOCOL-isolated-leftover-15-closed.md)).
Leftover-15 official is **15/15** at prefix-5 and uses keys. Leftover
last-4 is **9/15 vs 8/15**. Do not sell leftover official **15/15**.
The leftover-15 gpt2-medium analog is
[PROTOCOL-isolated-mgen.md](PROTOCOL-isolated-mgen.md).
Opened: leftover-15 coverage **0/15**; occupancy-free t=0 **16/48 vs
48/48**. Do not sell **0/15** or **16/48**. gpt2-medium 100×4 →
gpt2-medium 12×4 occupancy-free is
[PROTOCOL-isolated-m12.md](PROTOCOL-isolated-m12.md). Opened:
occupancy-free t=0 **10/48 vs 48/48**; coverage **13/48**. Do not sell
**10/48**. The remaining occupancy-free analog that is not leftover
targeting is
[PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md): Distil↔gpt2-medium
occupancy-free transfer on already-frozen 12×4 twins. Opened:
Distil→gpt2-medium t=0 **20/48 vs 48/48** (coverage **22/48**);
gpt2-medium→Distil t=0 **3/48 vs 47/48** (coverage **5/48**). Do not
sell **20/48** or **3/48**. Absolute-history H2 is opened in
[PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md): 0:4 **99/100** vs
16:32 **87/100**; reindexed 16:32 was **89/100**. Paired prompt-family
McNemar on those absolute windows is **13 vs 1** among 14 discordant
families. Isolated **25/48** Clopper–Pearson **[0.372, 0.667]** includes
½. Do not sell **99/100**
or **87/100**. Isolated-file detection is still not finished. Second-key
lock A is opened ([PROTOCOL-isolated-xkey.md](PROTOCOL-isolated-xkey.md):
interpolate **7/12**, isolated **30/48 vs 25/48**; H-xkey-iso **fails**
as a raw count). Absolute-history OOD windows are opened
([PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md):
grok12 0:4 **7/12**; 32:64 **10/12** rose versus reindexed **9/12**;
original 12 0:4 **9/12** vs 16:32 **6/12**). Do not sell absolute
**10/12** or **30/48**. Reindexed window dumps stay. The remaining
honesty item that is not leftover targeting was 12-LOO mask-*k*
absolute remasure of [PROTOCOL-isolated-mask-absolute.md](PROTOCOL-isolated-mask-absolute.md)
(reindexed dumps stay). Opened: absolute prefixes equal reindexed
(hard 0:4 **5/12**); hard tails stay **9/12**; interpolate 8:128 rose
3→4. Do not sell tail **9/12**. Sol's preregistered longer-context two-grain
lock is [PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md)
(`ngram_len=13`, $\Hw=12$). Opened Phase A: official first-draw
**12/12**; interpolate and hard **6/12**; isolated hard **22/48 vs
30/48** (**52/96**). Opened Phase B: interpolate **76/100** (below
lock A **99/100**); isolated **489/800**. Original-12 interpolate
occupancy is **160** seen versus public $\Hw=4$ **269** seen
(leave-one-family-out; H-long-occ holds). 100-family occupancy is
**5878** seen versus public **10158** seen. Do not sell **6/12**,
**76/100**, **160**, **269**, **5878**, or **10158**.
DistilGPT2 $\Hw=12$ 12-LOO is
[PROTOCOL-next-longctx-distil.md](PROTOCOL-next-longctx-distil.md)
(freeze SHA `bae6d81`). Opened: interpolate **9/12** (isolated
**49/96**); hard **6/12**; occupancy **175** seen vs **11994** unseen
(opening **111** vs **177**). Do not sell
**9/12** or **49/96**. Qwen2-1.5B $\Hw=12$ 12-LOO is
[PROTOCOL-next-longctx-qwen.md](PROTOCOL-next-longctx-qwen.md)
(freeze SHA `d7303a2`). Opened: interpolate **4/12** (isolated
**41/96**); hard **4/12**; official first-draw **11/12** (library
$0.515$); occupancy **65** seen vs **12127** unseen (opening **41** vs
**247**). Do not sell **4/12** or **41/96**. DistilGPT2 Aaronson 12-LOO is
[PROTOCOL-next-aaronson-distil.md](PROTOCOL-next-aaronson-distil.md)
(freeze SHA `9bdf12a`). Opened: interpolate **7/12** (isolated
**0/48 vs 48/48**); hard **7/12** (**56/96**); occupancy **196** seen
vs **11996** unseen (opening **133** vs **155**); unmarked first-draw
z>3 **1/12**. Do not sell **7/12**
or **0/48**. Qwen2-1.5B Aaronson 12-LOO is
[PROTOCOL-next-aaronson-qwen.md](PROTOCOL-next-aaronson-qwen.md)
(freeze SHA `1171d5c`). Opened: interpolate **12/12** (isolated
**12/48 vs 48/48**, **60/96**); hard **12/12** (**72/96**); occupancy
**457** seen vs **11735** unseen (opening **127** vs **161**). Do not
sell **12/12** or **60/96**. DistilGPT2 $\Hw=12$ 100-family is
[PROTOCOL-next-longctx-distil-100.md](PROTOCOL-next-longctx-distil-100.md)
(freeze SHA `d891622`). Opened: interpolate **88/100** (isolated
**557/800**); hard **89/100**; occupancy **11182** seen vs **85493**
unseen (opening **2036** vs **364**). Do not sell **88/100** or **557/800**.
Qwen2-1.5B $\Hw=12$ 100-family is
[PROTOCOL-next-longctx-qwen-100.md](PROTOCOL-next-longctx-qwen-100.md)
(freeze SHA `636765c`). Opened: interpolate **76/100** (isolated
**474/800**); hard **74/100**; occupancy **3535** seen vs **98064**
unseen (opening **1092** vs **1308**). Do not sell **76/100** or **474/800**.
Whether $\Hw=12$ interpolate **76/100** is a weaker body reader or an
opening residual is
[PROTOCOL-next-longctx-windows.md](PROTOCOL-next-longctx-windows.md)
(freeze SHA `8283d1f`). Opened: interpolate $[64{:}128)$ **50/100**
versus public **93/100**; opening **86/100**. Do not sell **50/100**
or **93/100**. DistilGPT2 Aaronson 100-family is
[PROTOCOL-next-aaronson-distil-100.md](PROTOCOL-next-aaronson-distil-100.md)
(freeze SHA `bf05759`). Opened: interpolate **96/100** (isolated
**601/800**); hard **91/100**; occupancy **28824** seen vs **61305**
unseen (opening **2048** vs **352**); unmarked first-draw z>3 **3/100**.
Do not sell **96/100** or **601/800**.
Qwen2-1.5B Aaronson 100-family is
[PROTOCOL-next-aaronson-qwen-100.md](PROTOCOL-next-aaronson-qwen-100.md)
(freeze SHA `a761a7d`). Opened: interpolate **100/100** (isolated
**616/800**); hard **97/100**; occupancy **8750** seen vs **92842**
unseen (opening **1470** vs **930**). Do not sell **100/100** or **616/800**.
Qwen2-1.5B Kirchenbauer 100-family is
[PROTOCOL-next-kgw-qwen-100.md](PROTOCOL-next-kgw-qwen-100.md)
(freeze SHA `ed9fb20`) and is named before generation. Opened: official
z>3 **90/100**; interpolate **96/100** (isolated **620/800**); hard
**63/100**. Do not sell **96/100** or **620/800**.
Qwen Kirchenbauer 100-family windows are
[PROTOCOL-next-kgw-qwen-100-windows.md](PROTOCOL-next-kgw-qwen-100-windows.md)
(freeze SHA `e270546`). Opened: interpolate $[0{:}4)$ **84/100**;
$[64{:}128)$ **97/100**. Do not sell **97/100** or **84/100**.
Isolated-file detection is still not
finished. Sol's different-mixin two-grain lock is
[PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md) (Hugging Face Kirchenbauer
defaults, `--mixin kgw`, seed **20260904**). Opened: official z>3
**48/48** marked; interpolate and hard **12/12**; isolated interpolate
**44/48 vs 41/48** (**85/96**); occupancy **114** seen vs **12071**
unseen. 100-family interpolate **100/100** (isolated **747/800**);
occupancy **4557** seen vs **96991** unseen. DistilGPT2 Kirchenbauer
original-12 interpolate **12/12** (isolated **85/96**); hard **11/12**;
occupancy **130** seen vs **11972** unseen. Distil 100-family interpolate
**100/100** (isolated **683/800**); hard **82/100**; occupancy **16170**
seen vs **71541** unseen. Qwen2-1.5B Kirchenbauer original-12 interpolate
**12/12** (isolated **68/96**); hard **8/12**; occupancy **84** seen vs
**12108** unseen. Do not sell **12/12**,
**100/100**, **85/96**, **747/800**, **114**, **683/800**, **82/100**,
**68/96**, or **8/12** as replacing
**25/48**. Do not write `thesis/`.

## What this freeze refuses

- Writing `thesis/` or drafting Loop 3 sections as a paper.
- Selling leftover **10/20**, covered **15/28**, leftover window
  **11/20**, covered **16/28**, leftover official **20/20**, leftover
  interpolate **13/20**, union **30/48**, leftover **10/18**, leftover
  official **18/18**, leftover-18 rankpath **12/18**, leftover-18
  interpolate **12/18**, Distil $\Hw=12$ **9/12** / **49/96**, Qwen $\Hw=12$ **4/12** / **41/96**, Distil Aaronson **7/12** / **0/48**, Qwen Aaronson **12/12** / **60/96**, Distil $\Hw=12$ 100-family **88/100** / **557/800**, Distil Aaronson 100-family **96/100** / **601/800**, Distil occupancy-free **22/48**, leftover Distil
  **3/18**, Distil→Distil **16/48**, Qwen→Qwen **31/48**, union **33/48**, leftover **9/15**, leftover official **15/15**, gpt2-medium leftover **0/15**, gpt2-medium occupancy-free **16/48**, gpt2-medium→gpt2-medium **10/48**, Distil→gpt2-medium **20/48**, gpt2-medium→Distil **3/48**, absolute H2 **99/100** / **87/100**, absolute OOD 32:64 **10/12**, grok12 **39/48**, nested **23/48** / **26/48** /
  **27/48** / **35/48**, or rankpath **41/48** as replacing **25/48**.
- Using pre-fix **10/12** / **29/48** as the main result.
- Calling key-free indication a failure at prompt-group grain.
- New `probe --methods` names on the 12×4 / 36×4 twins.
- Mixing grok12 into grok36 train.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Re-running PROTOCOL-isolated-scale; that protocol is already open.

Human merge of PR #2 / PR #3 is out of scope for this file.
