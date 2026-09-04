# Results ledger

This is an index, not a fourth detector. Headlines after the
truncated-context recount are **9/12**, **25/48**, **36/36**. The
pre-fix **10/12** / **29/48** stay in historical JSON. Exploratory
ablations live under [../experiments/README.md](../experiments/README.md).
The next measurement is [PROTOCOL-next.md](PROTOCOL-next.md), not another
scorer on the old 12×4 twins. Phase A on 100 new GPT-2 families: lock A
**99/100**. That does not replace **25/48**. Register-matched Grok-length train is
[PROTOCOL-isolated-register.md](PROTOCOL-isolated-register.md): lock A
nested Youden **16/48 vs 41/48** does not beat **25/48**. H-reg-A fails. The two-grain story lock is
[narrative.md](narrative.md): prompt-group ranking is real; isolated
`lr>0` is not a calibrated detector. Do not write a “key-free
detection fails” paper. This laboratory did not refute Christ et al.
(2024) or Zhang et al. (2024). Those papers are not a proof that this
mixin’s count tables must fail
([related-work.md](related-work.md); [CITING.md](CITING.md)). Spatial mask-*k* of the headline 12-LOO scorer
is [PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md). Leftover
versus covered on those tails is
[PROTOCOL-isolated-mask-split.md](PROTOCOL-isolated-mask-split.md).
Occupancy leftover-20 official+atoms bound is
[PROTOCOL-isolated-leftover-bound.md](PROTOCOL-isolated-leftover-bound.md).
Leftover-20 union with short+medium+tails openings is
[PROTOCOL-isolated-leftover-union.md](PROTOCOL-isolated-leftover-union.md):
union **30/48** (equals SMT); leftover **18**; last-4 **10/18 vs 10/18**.
Occupancy-free leftover-18 is closed for more unrelated GPT-2 scenes
([PROTOCOL-isolated-occupancy-closed.md](PROTOCOL-isolated-occupancy-closed.md)).
Leftover-18 mixed rankpath and grok36 interpolate are
[PROTOCOL-isolated-leftover-18.md](PROTOCOL-isolated-leftover-18.md):
rankpath **12/18 vs 13/18**; interpolate **12/18 vs 12/18**; 0:4 unseen
**89 vs 19**. Leftover-18 published key-free readers are closed
([PROTOCOL-isolated-leftover-18-closed.md](PROTOCOL-isolated-leftover-18-closed.md)).
Distil occupancy-free leftover-18 on the original 12 is
[PROTOCOL-isolated-xgen.md](PROTOCOL-isolated-xgen.md): Distil postokhits
t=0 **22/48 vs 43/48**; leftover-18 Distil **3/18** (office 1/3/4).

## Locked headlines

| Claim | Grain | Number | Not |
|---|---|---|---|
| Key-free last-4 count tables | Held-out prompt groups | **9/12** | Single-file accuracy |
| Same scorer, 0.02 margin | Same groups | 10/12 | The main result |
| Isolated hard sign | One marked file, `lr>0` | **25/48** | A 5% binomial test |
| In-domain 36×4 hits | Prompt groups | **36/36** | Cross-generator |
| Confirmatory 100×4 lock A (interpolate last-4) | New prompt groups | **99/100** | Isolated-file detector; not Distil/Qwen |
| 100×4 lock A nested-by-stem Youden | In-family files | **322/400 vs 338/400** | Out-of-family; not **25/48**; threshold nest on already-OOF scores |
| 100×4 lock B nested-by-stem Youden | In-family opening | **392/400 vs 382/400** | Occupancy (198/400 unmarked `n_used=0`); not **25/48** |
| Grok-register → original 12×4 lock A | Nested Youden | **16/48 vs 41/48** | H-reg-A fails; does not beat one-liner **23/48** or **25/48** |

Pre-fix **10/12** / **29/48** counted `(10,)→20` four times at
`context_len=4`. JSON: `experiments/2026-09-01-blind-12x4-recount-last4/`,
`experiments/2026-09-01-probe-12x4-recount-hard-last4/`. Official
public-key `score` on those twins is **12/12**. That path uses keys. It
is the positive control, not the key-free indicator. Ranking and isolated
sign disagree on stems: garden is one of nine 12-LOO hard ranking wins
with no marked file `lr>0`; station, office, and ferry-queue lose ranking
but hold 5 of 25 isolated TPs. `blind` leave-one-prompt-out now prints
that split; historical recount JSON stays stem-mean only. Live JSON:
`experiments/2026-09-01-blind-12x4-ranking-honesty/`. Table:
`experiments/2026-09-01-ranking-isolated-honesty/`.

## Mechanistic finding already on the old corpus

The in-domain mark is front-loaded. A 16-token prefix already ranks
**34/36**. Scoring **0:4** matches that ranking. Window **16:32** is
near chance. Matching mixin `ngram_len=5` (`context_len=5`) does not
beat last-4. Opening occupancy (Laplace on unseen next tokens) inflates
poshits **39/48**; `postokhits` keeps observed tokens only (**16/48**
on that split).

## Occupancy-free hashing on 12×4 is closed

`hashtok` is occupancy-free hashpool, not SynthID's hash. Mixer width,
mixer seed, and last-k are knobs, not a denser isolated-file detector.

| Axis | What happened | Keep |
|---|---|---|
| Width `--n-hashes` | n=2/4 beat n=8 in-domain; n=8 won 24→12 at seed 20260831 | `n_hashes=8` |
| Seed | n=2 spec 21–31/48; transfer n=8 is also lucky | seed `20260831` |
| Order `--context-len` | last-1 chance; last-3 11/12 with t=0 24/48; transfer last-4 still wins nested FPR10 | `context_len=4` |

Do not sell 36/48, 35/48, 34/48, 33/48, 24/48, 19/48, 18/48, or 17/48
as replacing **25/48**. Write-up:
[key-free-hashtok.md](key-free-hashtok.md).

## Where the other numbers are

Instance contrast, tokhits, rankpath, cascade, and transfer tables are
not copied here. Start from [key-free-twins.md](key-free-twins.md) and
the experiment index. Neighbours of the measurement, with author–year
citations, are [related-work.md](related-work.md). Nested-by-stem Youden
and FPR figures are a threshold nest on already-OOF scores: the other
stems' models still trained on H. They are not second-level nested CV.
t=0, AUC, and prompt ranking do not use that helper.

## What is scientifically interesting on the old corpus

Ranked for a reader, not for a leaderboard. Later 39/48 and 41/48
isolated signs are discovery, not headlines.

| Rank | Result | Role |
|---|---|---|
| 1 | Front-loaded / opening-token signal | Mechanistic |
| 2 | Key-free ranking on new prompt families | Core claim |
| 3 | 36/36 in-domain hits | Learnable footprint |
| 4 | Control-shuffled-30 instance contrast | Causal check |
| 5 | Poor GPT-2 → Distil/Qwen transfer | Not a tokenizer detector |
| 6 | Occupancy / coverage explains inflated recall | Why 39/48 is not 39 tokens |
| 7 | Opening rankpath 41/48 | Discovery; generator-specific |
| 8 | Cascades 39/48–40/48 | Do not keep optimizing |

Leave-one-out protects a fit. It does not protect against a researcher
who tries thirty scorers on the same twelve groups. That is why
[PROTOCOL-next.md](PROTOCOL-next.md) froze three readers before a
new 100×4 corpus was opened.

## Confirmatory 100×4 Phase A

Protocol SHA `7001489`. Prompts SHA `294dba5`. Pair SHA `bf98c92`.
Official first-draw keyed score **100/100**. Key-free flags unchanged.

| Lock | Reader | Prompt wins | File AUC | Isolated `lr>0` |
|---|---|---|---|---|
| A | interpolate last-4 | **99/100** (miss 088) | **0.898** | 352/400 vs 290/400 |
| B | opening poshits prefix-4 | **100/100** | **0.980** | 393/400 vs 344/400 |
| C | opening rankpath | **96/100** | **0.822** | 314/400 vs 302/400 |

H1 holds (lock A prompt ranking). H2’s committed JSON is a **reindexed**
window measurement: **0:4** **99/100**, AUC **0.885**; **16:32** **89/100**,
AUC **0.689**. Absolute-history remasure
[PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md): **0:4** **99/100**,
AUC **0.885**; **16:32** **87/100**, AUC **0.695**. Opening still
outranks mid-file under real prefix. Absolute 16:32 did not rise versus
reindexed **89/100**. Post-open paired prompt-family McNemar on those
absolute windows is **86 / 13 / 1 / 0** (one-sided ≈ 0.00092); that is
not a second freeze. Isolated **25/48** Clopper–Pearson **[0.372, 0.667]**
includes ½. Unpaired interval overlap is not the H2 test. Do **not**
overwrite the reindexed dump. Isolated `lr>0` is
not H1. `--rankpath` also emitted default methods; those are not lock C.
Do not sell lock B **393/400**, lock A **352/400**, or nested-by-stem
**322/400** / **392/400** as replacing **25/48**. Those are in-family.
Out-of-family isolated transfer is frozen in
[PROTOCOL-isolated.md](PROTOCOL-isolated.md) before those `probe
--test-dir` runs.

## Confirmatory 100×4 Phase B Distil and Qwen

Official Distil lamp **70/100** (weaker mixin than GPT-2 **100/100**).
Lock B **88/100** with **1 tie** (drop 12 from 100; historical persist
printed 89/100). Lock C **68/100** with **1 tie** (drop 28 from
96; historical persist printed 69/100). Isolated Distil signs (216/400, 164/400) are not **25/48**.

Official Qwen lamp **100/100** (local Hugging Face, mixin on). Lock B
**95/100** (drop 5). Lock C **84/100** (drop 12). H3 holds on both
generators: rankpath drops more than poshits. Isolated Qwen signs
(333/400, 275/400) are not **25/48**. `--rankpath` extras are not lock C.

JSON: `experiments/2026-09-01-pair-distil-100x4/`,
`experiments/2026-09-01-probe-distil-100x4-opening-poshits/`,
`experiments/2026-09-01-probe-distil-100x4-opening-rankpath/`,
`experiments/2026-09-01-pair-qwen-100x4/`,
`experiments/2026-09-01-probe-qwen-100x4-opening-poshits/`,
`experiments/2026-09-01-probe-qwen-100x4-opening-rankpath/`.

## Isolated-file transfer (100 families → old twins)

Protocol SHA `eb00f92`. Frozen locks A/B/C. Primary endpoint is nested
Youden on the test files (train-LOO threshold).

| Test | Lock | Prompt | Nested Youden |
|---|---|---|---|
| original 12×4 | A interpolate | 8/12 | **23/48 vs 38/48** |
| original 12×4 | B opening poshits | **11/12** | **36/48 vs 42/48** (33/48 unmarked zeros) |
| original 12×4 | C opening rankpath | **10/12** | **24/48 vs 41/48** |
| 36×4 | A interpolate | **36/36** | **109/144 vs 122/144** |
| 36×4 | B opening poshits | 35/36 | **134/144 vs 129/144** (75/144 unmarked zeros) |
| 36×4 | C opening rankpath | **35/36** | **109/144 vs 117/144** |

Lock A does not beat **25/48** on the original 12 files. Lock C nested
Youden **24/48 vs 41/48** does not either; H-iso-C: rankpath is more
domain-specific than lock B **11/12** / **36/48**. Lock C prompt losses
are **letter** and **garden** (garden is also the 12-LOO rankpath miss).
Three of the ten ranking wins have 0 isolated TPs. Do not sell a union
of A/B/C (**42/48** t=0, **40/48** nested). Occupancy-free readout of
the frozen lock B tables (same fit, postokhits): original 12×4
**16/48 vs 48/48** (21 occupancy TPs); 36×4 **114/144 vs 139/144**.
The 36-topic nested Youden is out-of-family but same one-line register;
it does not replace **25/48**. Occupancy TPs are not observed-token TPs.
Stem table:
`experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4/stems.json`.

Opening-overlap bound (same observed-token tables, not a new scorer):
12×4 **18/48** covered (decided 16/0); 36×4 **117/144** covered
(decided 114/5). Isolated postokhits t=0 matches those decided TPs.

JSON: `experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4/`,
`experiments/2026-09-01-transfer-100x4-to-12x4-opening-poshits/`,
`experiments/2026-09-01-transfer-100x4-to-12x4-opening-rankpath/`,
`experiments/2026-09-01-transfer-100x4-to-36x4-hard-last4/`,
`experiments/2026-09-01-transfer-100x4-to-36x4-opening-poshits/`,
`experiments/2026-09-01-transfer-100x4-to-36x4-opening-rankpath/`,
`experiments/2026-09-01-openings-100x4-to-12x4/`,
`experiments/2026-09-01-openings-100x4-to-36x4/`.

## Isolated-file transfer (Grok-register → original 12)

Protocol SHA `07ce009`. Pair SHA `28cf9f5`. Same three locks. Official
first-draw on the new twins is **12/12**. `used_keys=false`.

| Test | Lock | Prompt | Nested Youden | t=0 marked |
|---|---|---|---|---|
| original 12×4 | A interpolate | **5/12** | **16/48 vs 41/48** | **23/48 vs 30/48** |
| original 12×4 | B opening poshits | 7/12 | **6/48 vs 47/48** | **6/48 vs 47/48** |
| original 12×4 | C opening rankpath | **10/12** | **45/48 vs 22/48** | **22/48 vs 31/48** |
| original 12×4 | occupancy-free postokhits | 11/12 | **5/48 vs 47/48** | **5/48 vs 47/48** |

H-reg-A fails: lock A nested **16/48** is below one-liner lock A
**23/48**. Register-matched Grok-length train is not the missing
isolated detector. H-reg-iso holds: nothing here beats **25/48**.
Lock C nested **45/48 vs 22/48** used a negative train threshold
(≈ −0.41). Do not sell 45/48. Occupancy-free t=0 **5/48** equals
opening coverage **5/48** (0 exact 4-token copies). In-family
interpolate on the new 12 is prompt **11/12**, nested-by-stem
**24/48 vs 40/48**. Cross-register → 36×4 nested **50/144 vs 115/144**.

JSON: `experiments/2026-09-01-transfer-grok12x4-to-12x4-hard-last4/`,
`experiments/2026-09-01-transfer-grok12x4-to-12x4-opening-poshits/`,
`experiments/2026-09-01-transfer-grok12x4-to-12x4-opening-rankpath/`,
`experiments/2026-09-01-transfer-grok12x4-to-12x4-occupancy-free/`,
`experiments/2026-09-01-openings-grok12x4-to-12x4/`,
`experiments/2026-09-01-probe-grok12x4-hard-last4/`,
`experiments/2026-09-01-transfer-grok12x4-to-36x4-hard-last4/`.

## Isolated-file transfer (100 one-liners → Grok-register 12)

Protocol SHA `1ef7330`. Same three locks. `used_keys=false`.

| Test | Lock | Prompt | Nested Youden | t=0 marked |
|---|---|---|---|---|
| grok12×4 | A interpolate | **11/12** | **22/48 vs 41/48** | **27/48 vs 28/48** |
| grok12×4 | B opening poshits | 10/12 | **36/48 vs 44/48** | **36/48 vs 44/48** |
| grok12×4 | C opening rankpath | 8/12 | **10/48 vs 41/48** | **10/48 vs 41/48** |
| grok12×4 | occupancy-free postokhits | 10/12 | **0/48 vs 48/48** | **0/48 vs 48/48** |

H-xreg-A holds versus Grok-train → original 12 **16/48**. H-xreg-hard
holds: **22/48** is at or below in-family nested-by-stem **24/48**. The
original 12 are not uniquely cursed. Occupancy-free t=0 **0/48** is
bounded by opening coverage **5/48**. Do not sell prompt **11/12** or
lock B **36/48** (occupancy). Does not replace **25/48**.

JSON: `experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-last4/`,
`experiments/2026-09-01-transfer-100x4-to-grok12x4-opening-poshits/`,
`experiments/2026-09-01-transfer-100x4-to-grok12x4-opening-rankpath/`,
`experiments/2026-09-01-transfer-100x4-to-grok12x4-occupancy-free/`,
`experiments/2026-09-01-openings-100x4-to-grok12x4/`.

## Isolated-file windows (100 one-liner interpolate)

Protocol SHA `7d8759a`. Same lock A tables. `used_keys=false`.

On Grok-register test files, window **0:4** ranks **7/12**; tail
**32:64** and **64:128** rank **9/12**. Full-file **11/12** is not
front-loaded on that split. Occupancy-free openings remain **0/48**.
On the original 12, window **0:4** ranks **9/12** and **16:32** ranks
**6/12** (front-loaded, matching PROTOCOL-next H2). Isolated t=0 is
chance-like in every slice. Do not sell tail **9/12**. Does not replace
**25/48**.

JSON: `experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-windows/`,
`experiments/2026-09-01-transfer-100x4-to-12x4-hard-windows/`.

## Interpolate atoms (100 one-liners → Grok-register)

Decode of the same lock A tables. Not a new scorer. `used_keys=false`.
Marked `lr>0` **27/48**. Almost all mass is Witten–Bell backoff
(`unseen_next`): tail 64:128 is 214 seen vs 5924 unseen. Window 0:4
ranks because unmarked Δ is more negative (−0.397 vs −0.017), not
because occupancy-free openings fire (**0/48**). Observed-token atoms:
`'The' → ' car'` (n=19) and tail GPT-2 paragraph/dialogue templates.
Do not sell `The car` or tail **9/12**. Does not replace **25/48**.

JSON: `experiments/2026-09-01-atoms-100x4-to-grok12x4-interpolate/`.

## Isolated-file scale (36 Grok-length families)

Protocol SHA `e537d71`. Pair `69ef41f`. Official **36/36**.
`used_keys=false`.

36 Grok-length → grok12×4 lock A nested **36/48 vs 39/48** (prompt
**12/12**). Occupancy-free **39/48 vs 45/48** equals opening coverage
**39/48** (exact 21/48; 3 FP). H-scale-grok holds vs 100-one-liner
**22/48**. Isolated observed-token recall is still opening overlap.

36 Grok-length → original 12×4 lock A nested **26/48 vs 33/48**.
H-scale-A holds vs n=12 train **16/48**. Occupancy-free **10/48** equals
coverage **10/48**. Do not sell 26/48, t=0 **29/48**, or grok12
**39/48**. Does not replace **25/48**.

JSON: `experiments/2026-09-01-transfer-grok36x4-to-grok12x4-hard-last4/`,
`experiments/2026-09-01-openings-grok36x4-to-grok12x4/`,
`experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4/`.

## Interpolate atoms (36 Grok-length tables)

Decode of the same lock A tables, after the frozen probes. Not a new
scorer. `used_keys=false`.

Original 12×4: marked `lr>0` **29/48**. Almost all mass is Witten–Bell
backoff (tail 64:128: 137 seen vs 5996 unseen). Nested **26/48** is
not occupancy-free **10/48**. Library `'Cl' → 'osing'` (n=4) is an
unbucketed body copy; opening postokhits zeros `Closing`.

Grok12×4: marked `lr>0` **39/48**, equal to occupancy-free and
coverage. Window 0:4 marked Δ +2.518 (`'The' → ' car'` n=19). Tail
still backoff (183 vs 5955). Interpolate nested **36/48** is not
denser than occupancy-free **39/48**. Do not sell `Closing` or
`The car`. Does not replace **25/48**.

JSON: `experiments/2026-09-01-atoms-grok36x4-to-12x4-interpolate/`,
`experiments/2026-09-01-atoms-grok36x4-to-grok12x4-interpolate/`.

Isolated-file detection is not finished. Do not write `thesis/`.

## Isolated-file pool freeze (100 ∪ grok36)

Protocol: [PROTOCOL-isolated-pool.md](PROTOCOL-isolated-pool.md).
Published occupancy-free zeros on the original 12 are disjoint:
100 one-liners **18/48**, grok36 **10/48**, union **28/48**, leftover
**20/48**. That arithmetic is determined before mixed tables. Do not
sell **28/48** or leftover grok36 interpolate **13/20**. Mixed
`postokhits` / interpolate LRs are not opened in this entry.

JSON: `experiments/2026-09-01-openings-union-100-and-grok36-to-12x4/`.

## Isolated-file pool (mixed 100 + grok36)

Protocol SHA `244d23a`. `used_keys=false`. Mixed openings coverage
**28/48** equals the published set-union (no combo atoms). Occupancy-free
t=0 is **26/48 vs 47/48**. Mixed interpolate nested **27/48 vs 39/48**.
Do not sell 28/48, 26/48, or 27/48. Does not replace **25/48**.

JSON: `experiments/2026-09-01-openings-100plusgrok36-to-12x4/`,
`experiments/2026-09-01-transfer-100plusgrok36-to-12x4-occupancy-free/`,
`experiments/2026-09-01-transfer-100plusgrok36-to-12x4-hard-last4/`.

## Isolated-file leftover rankpath (mixed lock C)

Protocol SHA `7afd049`. `used_keys=false`. Leftover 20: marked `lr>0`
**12/20**, unmarked `lr≤0` **14/20**. Full nested **35/48 vs 38/48**
includes covered openings; do not sell 35/48. Does not replace
**25/48**.

JSON: `experiments/2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath/`.

## Isolated-file leftover vs covered (in-domain 25/48)

Protocol SHA `f09d0e2`. `used_keys=false`. Headline 12-LOO hard last-4
**25/48** splits leftover **10/20 vs 11/20** and occupancy-covered
**15/28 vs 11/28**. Leftover last-4 is chance. Ranking-loss TPs are all
leftover. Do not sell 10/20 or 15/28. Does not replace **25/48**.

JSON: `experiments/2026-09-01-isolated-split-25-leftover-vs-covered/`.

## Headline 12-LOO mask-*k* (hard vs interpolate)

Protocol SHA `004397c`. `used_keys=false`. Hard prefix **0:4** is
**5/12**; tails **4:128** / **8:128** stay **9/12**. Interpolate tails
drop to **5/12** then **3/12**. Isolated t=0 stays chance-like. The
headline hard **9/12** is not an opening-only n-gram artifact. Do not
sell prefix 10/12 or tail 9/12. Does not replace **25/48**.

JSON: `experiments/2026-09-01-probe-12x4-headline-windows/`.

## Headline 12-LOO mask-*k* (absolute history)

Protocol SHA `b70986d`. `used_keys=false`. New out-dir. Reindexed dump
stays. Absolute prefixes equal reindexed (hard 0:4 **5/12**). Hard
tails **4:128** / **8:128** stay **9/12**. Interpolate 8:128 rose 3→4.
Isolated t=0 stays chance-like. Do not sell tail 9/12 or interpolate
4/12. Does not replace **25/48**.

JSON: `experiments/2026-09-03-probe-12x4-headline-windows-absolute/`.

## Longer-context two-grain Phase A (`ngram_len=13`)

Protocol SHA `b70986d`. Official first-draw matching `ngram_len=13`
**12/12** above 0.55. Key-free interpolate last-4 **6/12**, hard
**6/12**. Isolated hard **22/48 vs 30/48** (**52/96**), AUC **0.544**.
Below public-mixin **9/12**. Clopper–Pearson on **6/12** includes ½.
Do not sell **6/12** or **52/96**. Does not replace **25/48**.

JSON: `experiments/2026-09-03-pair-12x4-ngram13/`,
`experiments/2026-09-03-probe-12x4-ngram13-hard-last4/`.

## Longer-context occupancy (original-12 leave-one-out atoms)

Named `df5487d` before the counts. `used_keys=false`. Hw=12 interpolate
atoms **160** seen vs **12026** unseen (marked `lr>0` **20/48**,
matching holdout). Public Hw=4 original-12 **269** vs **11912**. Every
window has fewer seen events under Hw=12. Do not sell **160** or
**269**. Does not replace **25/48**.

JSON: `experiments/2026-09-03-atoms-12x4-ngram13/`,
`experiments/2026-09-03-atoms-12x4-public-loo/`.

## Longer-context two-grain Phase B (`ngram_len=13`, 100 families)

Protocol SHA `b70986d`; start `facc538`. Official first-draw **100/100**.
Interpolate last-4 **76/100** (AUC **0.666**, isolated **267/400 vs
222/400**, BA **489/800**). Hard **66/100**. Below public-mixin lock A
**99/100**. Do not sell **76/100** or **489/800**. Does not replace
**25/48**.

JSON: `experiments/2026-09-03-pair-100x4-ngram13/`,
`experiments/2026-09-03-probe-100x4-ngram13-hard-last4/`.

## Longer-context occupancy (100-family leave-one-out atoms)

`used_keys=false`. Hw=12 interpolate atoms **5878** seen vs **95624**
unseen (marked `lr>0` **267/400**, matching holdout). Public Hw=4
100-family **10158** vs **91353** (lock A interpolate **352/400**).
Every window has fewer seen events under Hw=12. Do not sell **5878**
or **10158**. Does not replace **25/48**.

JSON: `experiments/2026-09-03-atoms-100x4-ngram13/`,
`experiments/2026-09-03-atoms-100x4-public-loo/`.

## Isolated-file leftover vs covered (mask-*k* hard windows)

Protocol SHA `3e30e70`. `used_keys=false`. Hard **4:128** leftover
**11/20 vs 11/20**, occupancy-covered **16/28 vs 11/28**. Leftover tail
is chance. Tail prompt **9/12** is not leftover-file recall. Prefix
0:4 isolated **29/48** is **12 leftover + 17 covered**. Do not sell
11/20, 16/28, window 29/48, or tail 9/12. Does not replace **25/48**.

JSON: `experiments/2026-09-01-isolated-split-windows-leftover-vs-covered/`.

## Occupancy leftover-20 bound (official + leftover atoms)

Protocol SHA `802186e`. Official `used_keys=true`. Leftover-20 full-file
mean **0.624**, **20/20** above 0.55 (covered **0.620**, 28/28). Prefix-5
**18/20** (office-1/3 at 0.500 on one 5-gram). Leftover interpolate 0:4
seen 21 vs unseen **99**; seen mass is `'Cl'→'osing'`; leftover
`lr>0` **13/20**. Leftover key-free chance is not an unmarked mixin
miss. Do not sell official 20/20 or interpolate 13/20. Does not replace
**25/48**.

JSON: `experiments/2026-09-01-isolated-leftover-bound/`.

## Isolated-file leftover-20 ∪ short-medium-tails openings

Protocol SHA `e5a5f6b`. `used_keys=false`. Union **30/48** equals
published SMT coverage; mixed 100+grok36 is a subset (`covered_a_only`
empty). SMT-only covers are garden 1/4. Leftover after union is **18**.
12-LOO hard last-4 leftover is **10/18 vs 10/18**. Mixed occupancy-free
leftover sign is **0/18 vs 18/18** by construction. Do not sell union
30/48 or leftover 10/18. Does not replace **25/48**.

JSON: `experiments/2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4/`.

## Occupancy-free leftover-18 closed

Protocol [PROTOCOL-isolated-occupancy-closed.md](PROTOCOL-isolated-occupancy-closed.md).
No new decode. Leftover-18 official prefix-128 is **18/18** by subset
of leftover-20 **20/20**. Prefix-5 is **16/18** (office-1/3 remain).
Published disjoint-topic GPT-2 occupancy-free trains are exhausted for
leftover-18. Do not add family-12 paraphrases or target leftover
openings after peeking. Do not sell leftover official 18/18. Does not
replace **25/48**.

JSON: leftover-18 keys in
`experiments/2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4/`,
official arithmetic from
`experiments/2026-09-01-isolated-leftover-bound/`.

## Leftover-18 remaining readers (mixed rankpath + grok36 interpolate)

Protocol SHA `5621544`. `used_keys=false`. Leftover-18 mixed rankpath
**12/18 vs 13/18**. Grok36 interpolate **12/18 vs 12/18**. 12-LOO hard
last-4 check **10/18 vs 10/18**. Leftover-18 interpolate 0:4 seen 19 vs
unseen **89**; seen mass is `'Cl'→'osing'`. Garden leftover had 0 mixed
rankpath TPs and 1 interpolate TP. Do not sell leftover-18 rankpath
12/18 or leftover-18 interpolate 12/18. Does not replace **25/48**.

JSON: `experiments/2026-09-01-isolated-leftover-18-readers/`.

## Leftover-18 published readers closed

Protocol SHA `cdccae5`
([PROTOCOL-isolated-leftover-18-closed.md](PROTOCOL-isolated-leftover-18-closed.md)).
No new decode. Leftover-18 occupancy-free is **0/18** by construction.
Mixed rankpath **12/18 vs 13/18**. Interpolate **12/18 vs 12/18**; 0:4
unseen **89 vs 19**. Last-4 **10/18 vs 10/18**. Official **18/18** uses
keys. Do not re-slice more leftover-18 holdouts as leftover-file
detection. Does not replace **25/48**.

## Distil occupancy-free leftover-18 (PROTOCOL-isolated-xgen)

Protocol SHA `8e33445`. `used_keys=false`. Distil occupancy-free
postokhits t=0 **22/48 vs 43/48** beats GPT-2 lock B occupancy-free
**16/48** and does not beat **25/48**. Openings covered **23/48**.
Leftover-18 Distil coverage **3/18** (office 1/3/4); leftover
occupancy-free **3/18 vs 16/18**. Nested Youden **47/48** is a negative
threshold. Do not sell Distil 22/48 or leftover Distil 3/18. Does not
replace **25/48**. Distil 100×4 → Distil 12×4 occupancy-free analog is
[PROTOCOL-isolated-dgen.md](PROTOCOL-isolated-dgen.md): Distil→Distil
postokhits t=0 **16/48 vs 39/48** equals coverage **16/48**. Nested
**48/48** is a negative threshold. Do not sell Distil→Distil **16/48**.
Does not replace **25/48**. Qwen 100×4 → Qwen 12×4 occupancy-free analog
is [PROTOCOL-isolated-qgen.md](PROTOCOL-isolated-qgen.md): Qwen→Qwen
postokhits t=0 **31/48 vs 48/48**; coverage **37/48**. Cross-corpus
**31/48** > **25/48** does not replace original-12 GPT-2. Do not sell
Qwen→Qwen **31/48**. Does not replace **25/48**. Distil ∪ SMT occupancy-free
openings on the original 12 is
[PROTOCOL-isolated-dsmt.md](PROTOCOL-isolated-dsmt.md): union **33/48**;
leftover **15**; last-4 **9/15 vs 8/15**; Distil-only office 1/3/4. Do
not sell union **33/48** or leftover **9/15**. Does not replace
**25/48**. Occupancy-free leftover-15 after Distil ∪ SMT is closed
([PROTOCOL-isolated-leftover-15-closed.md](PROTOCOL-isolated-leftover-15-closed.md)):
leftover-15 official **15/15** at prefix-5 (keys); last-4 **9/15 vs
8/15**. Do not sell leftover official **15/15**. Does not replace
**25/48**. The leftover-15 gpt2-medium analog is
[PROTOCOL-isolated-mgen.md](PROTOCOL-isolated-mgen.md).
Opened: leftover-15 coverage **0/15**; occupancy-free t=0 **16/48 vs
48/48**. Do not sell **0/15** or **16/48**. Does not replace **25/48**.
gpt2-medium 100×4 → gpt2-medium 12×4 occupancy-free is
[PROTOCOL-isolated-m12.md](PROTOCOL-isolated-m12.md). Opened:
occupancy-free t=0 **10/48 vs 48/48**; coverage **13/48**. Do not sell
**10/48**. Does not replace **25/48**. The remaining occupancy-free
analog that is not leftover targeting is
[PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md): Distil↔gpt2-medium
occupancy-free transfer on already-frozen 12×4 twins. Opened:
Distil→gpt2-medium t=0 **20/48 vs 48/48** (coverage **22/48**);
gpt2-medium→Distil t=0 **3/48 vs 47/48** (coverage **5/48**). Do not
sell **20/48** or **3/48**. Does not replace **25/48**. Absolute-history
H2 is opened in [PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md):
0:4 **99/100** vs 16:32 **87/100**; reindexed 16:32 was **89/100**.
Post-open paired McNemar is **86 / 13 / 1 / 0**. Isolated **25/48**
Clopper–Pearson **[0.372, 0.667]** includes ½. Do
not sell **99/100** or **87/100**. Isolated-file remains open. Second-key
lock A is opened ([PROTOCOL-isolated-xkey.md](PROTOCOL-isolated-xkey.md):
interpolate **7/12**, isolated **30/48 vs 25/48**; H-xkey-iso **fails**
as a raw count). Absolute-history OOD windows are opened
([PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md):
grok12 0:4 **7/12**; 32:64 **10/12** rose versus reindexed **9/12**;
original 12 0:4 **9/12** vs 16:32 **6/12**). Do not sell absolute
**10/12** or **30/48**. Reindexed dumps stay. The remaining honesty
item that is not leftover targeting was 12-LOO mask-*k* absolute
remasure of [PROTOCOL-isolated-mask-absolute.md](PROTOCOL-isolated-mask-absolute.md)
(reindexed dumps stay). Opened: absolute prefixes equal reindexed
(hard 0:4 **5/12**); hard tails stay **9/12**; interpolate 8:128 rose
3→4. Do not sell tail **9/12**. Sol's preregistered longer-context two-grain
lock is [PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md)
(`ngram_len=13`, $\Hw=12$). Opened Phase A: official first-draw
**12/12**; interpolate and hard prompt ranking **6/12**; isolated hard
**22/48 vs 30/48** (**52/96**). Opened Phase B: official **100/100**;
interpolate **76/100** (below lock A **99/100**); isolated
**267/400 vs 222/400** (**489/800**). Do not sell **6/12** or
**76/100**. Isolated-file remains open. DistilGPT2 $\Hw=12$ 12-LOO is
[PROTOCOL-next-longctx-distil.md](PROTOCOL-next-longctx-distil.md)
(freeze SHA `bae6d81`). Opened: official first-draw **12/12**;
interpolate **9/12** (isolated **21/48 vs 28/48**, **49/96**); hard
**6/12** (**42/96**); occupancy **175** seen vs **11994** unseen. Do not
sell **9/12** or **49/96**. Isolated-file remains open. Qwen2-1.5B $\Hw=12$ 12-LOO is
[PROTOCOL-next-longctx-qwen.md](PROTOCOL-next-longctx-qwen.md)
(freeze SHA `d7303a2`). Opened: official first-draw **11/12** (library
$0.515$); interpolate **4/12** (isolated **14/48 vs 27/48**, **41/96**);
hard **4/12** (**47/96**); occupancy **65** seen vs **12127** unseen. Do
not sell **4/12** or **41/96**. Isolated-file remains open. DistilGPT2 Aaronson
12-LOO is [PROTOCOL-next-aaronson-distil.md](PROTOCOL-next-aaronson-distil.md)
(freeze SHA `9bdf12a`). Opened: official z>3 **12/12**; interpolate
**7/12** (isolated **0/48 vs 48/48**); hard **7/12** (**56/96**);
occupancy **196** seen. Do not sell **7/12** or **0/48**. Isolated-file remains open. Qwen2-1.5B Aaronson
12-LOO is [PROTOCOL-next-aaronson-qwen.md](PROTOCOL-next-aaronson-qwen.md)
(freeze SHA `1171d5c`). Opened: official z>3 **12/12**; interpolate
**12/12** (isolated **12/48 vs 48/48**, **60/96**); hard **12/12**
(**72/96**); occupancy **457** seen. Do not sell **12/12** or
**60/96**. Isolated-file remains open. Sol's different-mixin two-grain
lock is [PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md) (`--mixin kgw`,
Hugging Face Kirchenbauer defaults, seed **20260904**). Opened:
interpolate **12/12** (isolated **85/96**); hard **12/12**
(**60/96**); occupancy **114** seen. 100-family interpolate
**100/100** (isolated **747/800**); occupancy **4557** seen. Do not
sell **12/12**, **100/100**, **85/96**, or **747/800** as replacing
**25/48**. Isolated-file remains open.

## DistilGPT2 longer-context two-grain (`ngram_len=13`)

Protocol SHA `bae6d81`; named `c120dc4`. Official first-draw matching
`ngram_len=13` **12/12** above 0.55. Key-free interpolate last-4
**9/12**, isolated **21/48 vs 28/48** (**49/96**), AUC **0.563**. Hard
**6/12**, isolated **42/96**. Occupancy **175** seen vs **11994** unseen.
Above GPT-2 $\Hw=12$ interpolate **6/12** on these prompt strings
(different twins). Clopper–Pearson on **9/12** includes ½. Do not sell
**9/12** or **49/96**. Does not replace **25/48**.

JSON: `experiments/2026-09-04-pair-distil-12x4-ngram13/`,
`experiments/2026-09-04-probe-distil-12x4-ngram13-hard-last4/`,
`experiments/2026-09-04-atoms-distil-12x4-ngram13/`.

## Qwen2-1.5B longer-context two-grain (`ngram_len=13`)

Protocol SHA `d7303a2`; named `21a3e1b`. Official first-draw matching
`ngram_len=13` **11/12** above 0.55 (library $0.515$). Key-free
interpolate last-4 **4/12**, isolated **14/48 vs 27/48** (**41/96**),
AUC **0.400**. Hard **4/12**, isolated **47/96**. Occupancy **65** seen
vs **12127** unseen. Below Distil $\Hw=12$ interpolate **9/12** and
GPT-2 $\Hw=12$ **6/12** on these prompt strings (different twins).
Clopper–Pearson on **4/12** includes ½. Do not sell **4/12** or
**41/96**. Does not replace **25/48**.

JSON: `experiments/2026-09-04-pair-qwen-12x4-ngram13/`,
`experiments/2026-09-04-probe-qwen-12x4-ngram13-hard-last4/`,
`experiments/2026-09-04-atoms-qwen-12x4-ngram13/`.

## DistilGPT2 Aaronson–Kirchner 12-LOO

Protocol SHA `9bdf12a`; named `40a6300`. Official first-draw z>3
**12/12**. Interpolate last-4 **7/12**, isolated **0/48 vs 48/48**
(**48/96**), AUC **0.618**; all 7 ranking wins have 0 isolated TPs.
Hard **7/12**, isolated **8/48 vs 48/48** (**56/96**). Occupancy
**196** seen vs **11996** unseen. Below GPT-2 Aaronson interpolate
**11/12**. Clopper–Pearson on **7/12** includes ½. Do not sell **7/12**
or **0/48**. Does not replace **25/48**.

JSON: `experiments/2026-09-04-pair-distil-12x4-aaronson/`,
`experiments/2026-09-04-probe-distil-12x4-aaronson-hard-last4/`,
`experiments/2026-09-04-atoms-distil-12x4-aaronson/`.

## Qwen2-1.5B Aaronson–Kirchner 12-LOO

Protocol SHA `1171d5c`; named `406c91d`. Official first-draw z>3
**12/12**. Interpolate last-4 **12/12**, isolated **12/48 vs 48/48**
(**60/96**), AUC **0.993**; 9/12 ranking wins have 0 isolated TPs.
Hard **12/12**, isolated **24/48 vs 48/48** (**72/96**). Occupancy
**457** seen vs **11735** unseen. Above Distil Aaronson interpolate
**7/12**. Do not sell **12/12** or **60/96**. Does not replace
**25/48**.

JSON: `experiments/2026-09-04-pair-qwen-12x4-aaronson/`,
`experiments/2026-09-04-probe-qwen-12x4-aaronson-hard-last4/`,
`experiments/2026-09-04-atoms-qwen-12x4-aaronson/`.

JSON: `experiments/2026-09-01-isolated-xgen-leftover-18/`.

