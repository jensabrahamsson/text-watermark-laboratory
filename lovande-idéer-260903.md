# Proven-promising ideas (2026-09-03)

Backlog of key-free leads that this laboratory **measured and saw
move a published grain**, not a wish list. Locked headlines stay
**9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48** stay
in historical JSON. None of these ideas adds a `probe --methods` name
on the original 12×4 / 36×4 SynthID twins. None replaces **25/48**.
This laboratory did not refute Christ et al. (2024) or Zhang et al.
(2024). Author–year citations follow
[research/CITING.md](research/CITING.md).

`used_keys=false` on every key-free probe below. Official Kirchenbauer
z-scores and SynthID `detector_mean` are positive controls; they use
keys.

Reproduce from the committed pair dumps. Exploratory holdouts lived
under `/tmp/kgw-lab/` on the investigation machine and are not in git.

---

## 1. Kirchenbauer body still ranks (the hole is not “opening hash only”)

**Observation.** On Hugging Face default Kirchenbauer et al. (2023)
twins (`context_width=1`, `greenlist_ratio=0.25`, `bias=2.0`, seed
`20260904`, same original-12 prompt strings as the public SynthID
12×4), leave-one-family-out interpolate last-4 **absolute** windows
(`score_span`) rank the **body**, not only the opening:

| Window | KGW interpolate | KGW hard | SynthID interpolate | SynthID hard |
|---|---|---|---|---|
| 0:4 | 8/12, AUC 0.589 | 6/12 | **9/12**, 0.630 | 5/12 |
| 4:16 | 11/12 | 7/12 | 8/12 | 7/12 |
| 16:32 | 11/12, 0.786 | 8/12 | 6/12 | 7/12 |
| 32:64 | 11/12 | 10/12 | 4/12 | 5/12 |
| 64:128 | **12/12, 0.904** | 11/12 | **3/12** | 8/12 |
| full file | 12/12, 0.947, 44/48 | 12/12, 0.703, 35/48 | 7/12, 0.525, 24/48 | 9/12, 0.590, **25/48** |

SynthID twins: `experiments/2026-08-17-pair-12x4/` (public
`ngram_len=5`, $\Hw=4$). Kirchenbauer twins:
`experiments/2026-09-03-pair-12x4-kgw/` (opened in
[research/PROTOCOL-next-kgw.md](research/PROTOCOL-next-kgw.md)).

Same spatial split on DistilGPT2 Kirchenbauer 12×4: interpolate 0:4
**9/12**, every later window **12/12**, tail 64:128 AUC **0.836**.
Qwen2-1.5B Kirchenbauer 12×4: interpolate 0:4 **7/12**, 64:128
**12/12**, AUC **0.819**. Occupancy-free `postokhits` on GPT-2
Kirchenbauer openings (`--fit-prefix 4 --pos-bucket 1`) is weak:
isolated **11/48**. Full-file interpolate **12/12** is not an
exact-copy detector (atoms: 114 seen vs 12071 unseen).

Confirmatory 100-family interpolate last-4, absolute 0:4 vs 64:128
(same readers; `--skip-nested` on the window slice):

| Mixin | 0:4 | 64:128 |
|---|---|---|
| GPT-2 Kirchenbauer | 88/100, AUC 0.694, 258/400 | **100/100, 0.953, 364/400** |
| DistilGPT2 Kirchenbauer | 78/100, 0.655, 277/400 | **98/100, 0.880, 194/400** |
| Public SynthID | **99/100, 0.885, 372/400** | 93/100, 0.726, 259/400 |

Distil 100 tail ranks **98/100** while isolated t=0 is only **194/400**
(unmarked $\le 0$ **369/400**): newline-loop files already noted in
the Distil Kirchenbauer freeze. Ranking geography still matches GPT-2
Kirchenbauer. Do not sell Distil tail **194/400**.

Kirchenbauer is **back-loaded**. SynthID is **front-loaded**. Original-12
SynthID interpolate 64:128 **3/12** is not “the tail is chance at
every n”: 100-family interpolate 64:128 still ranks **93/100**. Do not
sell **93/100** or **100/100** as replacing **25/48**.

**Scope.** Local Hugging Face Kirchenbauer on GPT-2 / DistilGPT2 /
Qwen2-1.5B, original-12 strings, $T=128$, four draws. Pair dumps:
`experiments/2026-09-03-pair-12x4-kgw/`,
`experiments/2026-09-03-pair-distil-12x4-kgw/`,
`experiments/2026-09-03-pair-qwen-12x4-kgw/`. Not production Gemini.
Not leftover targeting. Windows keep absolute generated indices.

**Hypothesis.** The two mixins leak in opposite places under the same
count-table reader. Kirchenbauer’s green list is a **body** leak.
SynthID tournament last-4 interpolate is **opening-heavy**; the
original-12 tail **3/12** overstates how dead the body is at n=100.

**Non-claim.** This does not replace **25/48**. Full-file Kirchenbauer
interpolate **12/12** / **44/48** / **85/96** is a different mixin and
already opened; do not sell those counts as isolated SynthID
detection. Occupancy-free KGW openings are **not** the leak. Distil
100-family Kirchenbauer interpolate **100/100** /
isolated **683/800** (opened on `main`) is the same construction at
confirmatory scale, still not **25/48**. Do not sell confirmatory tail
**100/100** or SynthID tail **93/100** as an isolated-file detector.

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-windows

python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-synthid-windows

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-windows-ends
```

**Why it is a backlog item.** If the next honesty pass needs a
reader that is not front-loaded, match the mixin: Kirchenbauer count
tables rank 64:128 at both 12 and 100 families. Do not spend another
leftover-targeting round trying to recover SynthID’s original-12
interpolate tail with last-4 tables.

---

## 2. Match `context_len` to Kirchenbauer hash width (last-1)

**Observation.** Kirchenbauer hashes **one** previous token
(`context_width=1`). The published last-4 hard reader is wider than
that hash. Switching the **existing** `hard` / `interpolate` readers
to `--context-len 1` (not a new method name) lifts isolated hard sign
on every local generator we tried:

| Corpus | last-4 hard | last-1 hard | last-1 interpolate |
|---|---|---|---|
| GPT-2 KGW 12×4 | 12/12, 35/48, AUC 0.703 | **12/12, 43/48, 0.911** | 12/12, 44/48, 0.951 |
| DistilGPT2 KGW 12×4 | 11/12, 34/48, 0.780 | **12/12, 46/48, 0.952** | 12/12, 42/48, 0.945 |
| Qwen2-1.5B KGW 12×4 | 8/12, 19/48, 0.566 | **12/12, 37/48, 0.786** | 12/12, 36/48, 0.834 |
| GPT-2 KGW 100×4 | 62/100, 209/400, 0.573 | **100/100, 389/400, 0.990** | 100/100, 383/400, 0.981 |
| DistilGPT2 KGW 100×4 | 82/100, 180/400, 0.666 | **99/100, 350/400, 0.876** | 100/100, 349/400, 0.915 |

GPT-2 KGW last-1 tail 64:128 is **12/12** hard, AUC **0.887**,
isolated **43/48**. Opening 0:4 last-1 hard is only **6/12**. The
last-1 lift is a **body** lift, same spatial pattern as idea 1.
Confirmatory 100-family last-1 hard windows: 0:4 **94/100**, AUC
**0.740**, isolated **257/400**; 64:128 **100/100**, AUC **0.962**,
isolated **372/400**.

Hard width is not “any shorter k.” GPT-2 Kirchenbauer hard:

| Width | 12×4 | 100×4 |
|---|---|---|
| last-1 | **12/12, 43/48, 0.911** | **100/100, 389/400, 0.990** |
| last-2 | 7/12, 28/48, 0.484 | 79/100, 278/400, 0.677 |
| last-3 | 8/12, 30/48, 0.569 | — |
| last-4 | 12/12, 35/48, 0.703 | 62/100, 209/400, 0.573 |

At n=100, last-1 > last-2 > last-4. Original-12 last-2 collapse is
small-n. Last-2 is the SynthID isolated lift (idea 3), not the
Kirchenbauer companion. Distil 100 last-2 hard is **77/100**,
**253/400**, AUC **0.646**: below last-1 (**99/100 / 350/400**) and
below last-4 ranking (**82/100**).

Existing `unigram` (token identity, no context; not a new method
name) ranks GPT-2 Kirchenbauer 12×4 **12/12**, isolated **46/48**,
AUC **0.791**, unmarked $\le 0$ only **27/48**. 100-family unigram is
**99/100**, **329/400**, AUC **0.887**. Distil 12×4 unigram **12/12**,
**35/48**, 0.812. Qwen 12×4 unigram **9/12**, **16/48**, 0.598. That
is a global bag-of-tokens green-list leak. Last-1 still wins AUC and
(at n=100) isolated sign. Do not sell unigram **46/48**. Public
SynthID unigram is **11/12**, **26/48**, AUC **0.592** (library ranks
with no isolated TP). Mix last-1+last-4 and backoff on public
SynthID 12 are chance (**6/12**, AUC 0.49).

The same knob on **SynthID** full-file last-1 **collapses**: hard
**1/12**, AUC **0.414**. Last-1 is not a universal “shorter is
better.” It matches this mixin’s hash width. (SynthID last-1 window
0:4 can look strong, **9/12** / **37/48**; that is an opening unigram
slice, not a reason to replace last-4 on the public mixin.)

Clopper–Pearson 95% (invert `binomial_sf`; not a second freeze):
Kirchenbauer last-1 hard isolated **43/48** is **[0.773, 0.965]**;
last-4 hard **35/48** is **[0.582, 0.847]**. 100-family last-1 hard
**389/400** is **[0.951, 0.986]**; last-4 hard **209/400** is
**[0.472, 0.572]** and includes ½. Isolated **25/48** still includes ½.
Nested Youden on 100-family last-1 hard is **376/400 vs 369/400**.

**Scope.** Kirchenbauer 12×4 dumps from idea 1 plus confirmatory
`experiments/2026-09-03-pair-100x4-kgw/` and
`experiments/2026-09-03-pair-distil-100x4-kgw/`. Distil 100 last-1 used
the GPT-2 tokenizer id on Distil text (same BPE). Last-1 was not the
preregistered PROTOCOL-next-kgw reader (that freeze is last-4). This
is a post-open width match. Distil 100 has newline-loop files that the
keyed z-test also flags; last-1 unigrams on those loops are not a
reason to sell **350/400**.

**Hypothesis.** When the watermark hash is last-1, last-4 count
tables smear a one-token green list across unused context tokens.
Matching reader width to hash width recovers isolated sign without
keys. A context-free unigram still ranks because green tokens are
over-used in aggregate; last-1 is the tighter match. Interpolate
last-4 was already saturated at 100 families (**100/100** /
**376/400**); last-1 is the hard-reader lift.

**Non-claim.** Do not sell **43/48**, **46/48**, **37/48**,
**48/48**, **47/48**, **389/400**, **350/400**, **329/400**, or
**100/100** as replacing **25/48**. Do not add a method name. Do not retune Kirchenbauer
`context_width` after peeking. Do not run last-1 or unigram as the
headline SynthID reader. Do not switch Kirchenbauer hard to last-2
(12×4 collapse; 100×4 is strictly below last-1). Kirchenbauer last-1
tables trained on 100 GPT-2 families do **not** classify public
SynthID original-12 (isolated **6/48**, AUC 0.542, three ranking wins
with no isolated TP). The last-1 lift is mixin-specific.

Same mixin, shared GPT-2 BPE, last-1 **does** transfer across
generators. Last-4 does not:

| Train → test | last-1 hard | last-4 hard |
|---|---|---|
| GPT-2 100 KGW → GPT-2 12 KGW | **12/12, 48/48, AUC 1.000** | 8/12, 32/48, 0.565 |
| GPT-2 100 KGW → Distil 12 KGW | **12/12, 47/48, AUC 0.991** | 5/12, 22/48, 0.488 |
| Distil 100 KGW → GPT-2 12 KGW | **12/12, 42/48, 0.987** | — |
| Distil 100 KGW → Distil 12 KGW | **12/12, 42/48, 0.982** | — |

`--skip-nested`; isolated is $\tau=0$. Unmarked $\le 0$ on GPT-2 12
is **43/48** (five FPs). Distil in-domain last-1 was **46/48**; GPT-2
tables on Distil files are **47/48**. Do not sell **48/48** or
**47/48**. Qwen uses a different tokenizer; this transfer is same-BPE
only.

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hard,interpolate --context-len 1 --skip-hashpool \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-last1

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods hard,interpolate --context-len 1 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-last1

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-12x4-kgw \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/xfer-kgw100-last1-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-distil-12x4-kgw \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/xfer-kgw100-last1-to-distil12
```

**Why it is a backlog item.** Published Kirchenbauer hard last-4
understates the green-list leak: 100-family ranking **62/100** →
**100/100**, isolated **209/400** → **389/400**, AUC **0.573** →
**0.990**. Same `hard` scorer. At n=100 the hard widths are last-1 >
last-2 > last-4. Last-1 tables transfer GPT-2 ↔ Distil and GPT-2 100 →
original-12 KGW (**48/48** vs last-4 **32/48**); last-4 tables do not.
The freeze in
[research/PROTOCOL-next-kgw.md](research/PROTOCOL-next-kgw.md) should
keep last-4 as the preregistered grain and treat last-1 as the
width-matched companion. Unigram is a weaker bag-of-tokens companion,
not a fourth scorer.

---

## 3. Public SynthID: hard last-2 isolated sign (existing `hard`, not a new method)

**Observation.** A post-hoc `context_len` grid $\{1,2,3,4,5\}$ on
original-12 public SynthID hard ($\Hw=4$), then confirmation on 36×4
and 100×4, finds **last-2** as the isolated-file lift. Interpolate
stays better at last-4 on 36×4 ranking. No new `--methods` name:
`--context-len 2` on `hard`. The same width on `ngram_len=13`
($\Hw=12$) twins does **not** repeat the ranking jump.

| Corpus | last-4 hard | last-2 hard |
|---|---|---|
| GPT-2 12×4 LOO | **9/12**, **25/48**, AUC 0.590 | **10/12, 34/48**, 0.702 |
| GPT-2 36×4 LOO | 26/36, 83/144, 0.606 | 27/36, **106/144**, 0.661 |
| GPT-2 100×4 LOO | 67/100, 254/400, 0.607 | **94/100, 340/400**, 0.781 |
| GPT-2 ngram-13 12×4 | 6/12, 22/48, 0.544 | 8/12, 21/48, 0.481 |
| GPT-2 ngram-13 100×4 | 66/100, 215/400, 0.579 | 63/100, 248/400, 0.592 |

12×4 last-2 absolute windows: tail 64:128 hard **10/12**, AUC 0.680,
isolated **34/48**. Opening 0:4 last-2 hard is **7/12**. That tail
**10/12** does **not** mean last-2 is a body leak at confirmatory n.
100-family hard windows (`--skip-nested` on the window slice; full-file
last-2 matches the LOO dump **94/100 / 340/400**):

| Width | 0:4 | 64:128 | full file |
|---|---|---|---|
| last-2 | **100/100**, 0.947, **389/400** | 58/100, 0.554, 237/400 | **94/100**, 0.781, **340/400** |
| last-4 | 99/100, 0.954, **389/400** | 47/100, 0.483, 189/400 | 67/100, 0.607, 254/400 |

Opening isolated **389/400** is the same grain at both widths
(388 shared TPs). Of last-2 full-file TPs, **334/340** are already
0:4 TPs (**6** are not). Last-4 full-file keeps **248/254** opening
TPs. Last-2’s full-file isolated lift is **opening mass that survives
the file mean**, not a Kirchenbauer-style tail (idea 1 interpolate
64:128 **100/100**). 36-family last-2 windows sit in between: 0:4
**32/36**, **128/144**, AUC **0.869**; 64:128 **19/36**, AUC **0.543**.
Last-4 interpolate tail 64:128 is still **3/12** on the original 12
and **93/100** at n=100. Do not sell **389/400**.

Paired marked-file signs, last-2 vs last-4 on the original 12 (exact
McNemar; McNemar, 1947; not a freeze): **16** gains / **7** losses /
18 both / 7 neither. One-sided $p\approx 0.047$. Unmarked $\le 0$:
gained 12 TN, lost 6. Occupancy leftover-20 (zeros of
`experiments/2026-09-01-openings-100plusgrok36-to-12x4/coverage.json`):
last-4 **10/20 vs 11/20**, last-2 **12/20 vs 12/20**. Covered 15/28 →
**22/28**. Leftover last-2 tail 64:128 is **13/20 vs 12/20**; covered
tail **21/28**. Occupancy-free `postokhits` leftover last-2 is **8/20**,
unmarked $\le 0$ **20/20** — same isolated count as last-4 `postokhits`
leftover. 100→12 last-2 leftover is **11/20 vs 13/20**. Last-2 does
**not** fix leftover; the isolated lift is mostly occupancy-covered
files.

Transfer 100×4 → original 12, hard, no method name:

| Width | Prompt wins | Isolated t=0 | Nested Youden |
|---|---|---|---|
| last-4 | 8/12 | 21/48 | 14/48 vs 43/48 |
| last-2 | 7/12 | **29/48** | **23/48 vs 36/48** |

Same-register 100 → 36×4 (`--skip-nested`): last-2 **31/36**, isolated
**118/144**, AUC **0.743** versus last-4 **25/36**, **96/144**, 0.624.
Last-2 helps the 36-family transfer. It does **not** transfer to
Distil SynthID 12 (**5/12**, 21/48, AUC 0.510). 100 one-liners →
Grok-register (`--skip-nested`; do not mix grok12 into train): last-2
grok12 **6/12**, **29/48**, AUC **0.590** versus last-4 **4/12**,
**12/48**, 0.424; grok36 last-2 **18/36**, **77/144**, 0.516 versus
last-4 **15/36**, **43/144**, 0.458. Isolated **29/48** equals
100→original-12 last-2; ranking is chance. In-domain grok12 last-2
TPs overlap that transfer on **19/29** files. Grok36 last-2 windows:
0:4 **24/36**, **96/144**, 0.621; 64:128 **19/36**, **77/144**, 0.539.
Kirchenbauer last-1 cross-generator transfer is idea 2, not this width.

Second-key control-as-marked 12×4 (constructed twins, not a matched
`pair()`; interpolate freeze stays **7/12 / 30/48**): hard last-2
**11/12**, **34/48**, AUC **0.730** versus last-4 **9/12**, **32/48**,
0.616. Isolated McNemar is **10** gains / **8** losses,
$p\approx 0.41$. Ranking moved; isolated did **not** repeat the public
16/7. Last-2 windows: 0:4 **12/12**, **47/48**, AUC **0.912**; 64:128
**9/12**, AUC **0.633** (last-4 opening is also **12/12 / 47/48**;
tail **7/12 / 0.492**). Do not leftover-slice control files. Do not
sell **34/48** or opening **47/48**.

Other generators, in-domain hard (`--model gpt2` on Distil / medium,
same BPE; Qwen uses `Qwen/Qwen2-1.5B-Instruct`):

| Corpus | last-4 hard | last-2 hard |
|---|---|---|
| DistilGPT2 12×4 | 11/12, 33/48, 0.644 | 10/12, 33/48, 0.628 |
| DistilGPT2 100×4 | 54/100, 147/400, 0.499 | 66/100, 182/400, 0.581 |
| gpt2-medium 12×4 | 7/12, 21/48, 0.555 | 6/12, 18/48, 0.503 |
| gpt2-medium 100×4 | 82/100, 274/400, 0.663 | 85/100, **330/400**, 0.719 |
| Qwen2-1.5B 12×4 | 5/12, 15/48, 0.383 | 9/12, 23/48, 0.520 |
| Qwen2-1.5B 100×4 | 74/100, 351/400, 0.626 | 74/100, 257/400, 0.620 |
| Grok-register 12×4 | 8/12, 25/48, 0.509 | 8/12, **34/48**, 0.588 |
| Grok-register 36×4 | 22/36, 77/144, 0.477 | 23/36, 91/144, 0.570 |

gpt2-medium 12 is chance both widths (official lamp **12/12**). At
n=100 medium last-2 isolates **330/400** vs last-4 **274/400**; ranking
only +3. Medium last-2 windows match GPT-2 geography: 0:4 **99/100**,
**387/400**, AUC **0.949**; 64:128 **54/100**, AUC **0.519**. Distil 100
last-4 is chance; last-2 ranking **66/100** is not GPT-2 **94/100**; both
widths have **108/400** marked zeros; Distil last-2 0:4 is only
**74/100**. Qwen 100 ranking is tied; last-4 isolated **351/400** has
unmarked $\le 0$ only **121/400**. Qwen last-2 0:4 is **88/100**,
**325/400**, AUC **0.783**; 64:128 still ranks **71/100**, AUC
**0.582** (GPT-2 last-2 tail was **58/100**). Do not sell **330/400**,
**66/100**, **351/400**, or Qwen opening **88/100**. Occupancy-free
`postokhits` last-2 on the original 12
is **9/12 / 23/48**, unmarked $\le 0$ **48/48** — the same isolated
count as last-4 `postokhits`. Hard last-2 **34/48** is not that
occupancy-free reader. Grok-register in-domain last-2 repeats the
isolated McNemar (12 gains / 3 losses, $p\approx 0.018$) at **34/48**
with ranking still **8/12**; grok36 last-2 is **91/144** vs last-4
**77/144** (37/23, $p\approx 0.046$). Grok-register last-2 0:4 is
**8/12 / 31/48**; 64:128 **6/12 / 30/48** — isolated is not the
GPT-2-100 opening-only split. Do not mix grok12 into any train. Do
not sell grok **34/48**.

Interpolate last-2 **hurts** 36×4 ranking: **32/36** vs last-4
interpolate **34/36**. Original-12 interpolate last-2 is **7/12**,
same sign count as last-4 interpolate. Keep interpolate at last-4.
Hits last-2 on original-12 is also worse ranking than published last-4
hits: **9/12**, AUC **0.632**, isolated 29/48 versus last-4 hits
**10/12**, AUC **0.718**, isolated 28/48. The last-2 lift is a
**hard** width effect, not “shorten every count spec.”

Grid losers on original-12 hard: last-1 **1/12** / 22/48 / AUC 0.414;
last-3 **8/12** / 26/48; last-5 **9/12** / 23/48. Matching mixin
`ngram_len=5` (`context_len=5`) still does not beat last-4. Last-2 is
not “match $\Hw=4$.”

Clopper–Pearson 95% (not a freeze): original-12 last-2 isolated
**34/48** is **[0.559, 0.830]** (excludes ½); locked last-4 **25/48**
is **[0.372, 0.667]** (includes ½). 100-family last-2 ranking
**94/100** is **[0.874, 0.978]**. Leftover last-2 **12/20** still
includes ½.

**Scope.** Public SynthID GPT-2 twins already in git:
`experiments/2026-08-17-pair-12x4/`,
`experiments/2026-08-31-pair-36x4/`,
`experiments/2026-09-01-pair-100x4/`. Last-2 was not the headline
freeze. Distil/Qwen/medium last-2 is in-domain only
(`experiments/2026-08-31-pair-distilgpt2-12x4/`,
`experiments/2026-08-31-pair-qwen-12x4/`,
`experiments/2026-09-01-pair-distil-100x4/`,
`experiments/2026-09-01-pair-qwen-100x4/`,
`experiments/2026-09-01-pair-gpt2-medium-12x4/`,
`experiments/2026-09-01-pair-gpt2-medium-100x4/`). Grok-register
in-domain last-2 is `experiments/2026-09-01-pair-grok12x4/` and
`experiments/2026-09-01-pair-grok36x4/` (not mixed into the original-12
train). Second-key hard is
`experiments/2026-09-02-pair-12x4-control-as-marked/`.

**Hypothesis.** Hard last-4 on $\Hw=4$ tournament text is slightly too
long for **full-file** isolated sign: last-2 keeps opening last-k mass
in the file mean without falling into last-1 unigram collapse. It is
not a body-hash match (n=100 last-2 tail **58/100**; Kirchenbauer
last-1 tail is **100/100**). Grok-register 12 last-2 isolated
**34/48** is not that opening-only split (0:4 **31/48**, tail
**30/48**). It is tied to short tournament history:
`ngram_len=13` ($\Hw=12$) last-2 does not rescue ranking (12×4 isolated
**21/48** vs last-4 **22/48**; 100×4 ranking **63/100** vs **66/100**).

**Non-claim.** Do not rewrite the locked headline to **34/48** or
**10/12**. Do not sell transfer **29/48** or nested **23/48**. Do not
sell leftover **12/20**, leftover tail **13/20**, leftover occupancy-free
**8/20**, or leftover 100→12 last-2 **11/20**. Do not sell
opening **389/400**, second-key **34/48**, second-key opening **47/48**, medium **330/400**, Distil
**66/100**, Qwen **351/400**, grok **34/48**, transfer grok **29/48**, or occupancy-free last-2 **23/48**. Do not switch interpolate to last-2.
Do not switch `hits` to last-2 (ranking **9/12**, AUC 0.632). Do not
add `hard2` as a method name. Do not present last-2 as matching the
keyed hash window (last-5 lost the grid; $\Hw=12$ last-2 does not
repeat the 100-family **94/100** jump). Do not present last-2 as a
Kirchenbauer-style body companion. Public last-2 tables trained on
100 GPT-2 families do not classify Kirchenbauer original-12
(isolated **24/48**, AUC 0.554).

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hard,interpolate --context-len 2 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-12x4-synthid-k2

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --methods hard --context-len 2 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-36x4-synthid-k2

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --methods hard --context-len 2 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-100x4-synthid-k2

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --methods hard --context-len 2 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-synthid-k2-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods hard,interpolate --context-len 2 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-12x4-ngram13-k2
```

**Why it is a backlog item.** Isolated **25/48** is the honest last-4
headline. Last-2 is the one existing-scorer width that moved isolated
sign on 12, 36, and 100 **public** GPT-2 families in the same
direction. At n=100 that lift is opening mass kept in the file mean
(**334/340** of last-2 TPs are 0:4 TPs), not a body window: original-12
tail **10/12** overstates geography. It is not a universal
shorter-context recipe: longer hash history kills the ranking jump;
Distil/Qwen/medium 12 do not repeat the isolated McNemar; Grok-register
12 does (**34/48**, ranking still **8/12**). Keep leftover-20 as the
honesty bound on any SynthID width change.

---

## Investigated and not promoted

These were the other 2026-09-03 leads. They did **not** earn a backlog
slot as improvements to key-free **document** indication.

### Claude finished strings

Premark vs `experiments/claude-sample-2026-09-03/` last-4 ranks
**35/40**, last-2 **38/40**, unmarked $\le 0$ **40/40**. Window 0:4 is
**0/40** on both readers; the shift is in the body (4:16 through
64:128 are 36–39/40). Same-day 19a vs 19b is **19/38**; tail 64:128
**23/38**. That is a long-timescale GPT-2-BPE style drift, killed by
the same-day control, not a watermark detector. Do not put **35/40**
on a detection list. Logbook already records the premark comparison.

### Gloaguen generator queries

Gloaguen et al. (2025) ask whether a **generator** is watermarked, with
black-box queries and no matched document pairs. Production Table 2 in
that paper fails to reject GPT-4 / Claude 3 / Gemini 1.0 Pro; the
authors refuse to conclude. App. F.4 finds no evidence of SynthID on
Gemini 1.5 Flash. That is their result, not ours.

Locally, a Red-Green fruit/digit matrix on Qwen2-1.5B **sampling**
(N1=4, N2=6, K=8 valid completions, H=1) held the unmarked null
($S=1$, $p\approx 0.98$) and **did not reject** Hugging Face
Kirchenbauer either ($S=1$, $p\approx 0.93$), even though mean
$p(\texttt{apples})$ moved 0.35 → 0.64 (a global shift, not
column-consistent t2 structure). Logit-level last-token=t2 on the same
model **rejected unmarked** ($S=5$, $p\approx 0.001$). GPT-2 digit
logits also reject unmarked. That is an LM-digit effect, not a
watermark detector.

Gloaguen remains the right *question* for an API without twins. It is
not a proven improvement of this lab’s finished-string `indicate` /
`blind` path at this budget. Do not call paid chat APIs. Wang et al.
(2026) (TTP-Detect) stays the closest published finished-string analog
and was not reimplemented.

### Occupancy-free KGW openings; SynthID last-1 full file; interpolate last-2; mix/backoff; occupancy-free last-2

`postokhits` on Kirchenbauer 12×4 is **11/48**. SynthID last-1
full-file hard is **1/12**. Interpolate last-2 drops 36×4 ranking
from **34/36** to **32/36**. Mix last-1+last-4 and backoff on public
SynthID 12 are chance (**6/12**). Occupancy-free `postokhits` last-2
on public 12 is **23/48**, same as last-4 `postokhits`, below **25/48**.
None of those is a backlog item.

---

## What this file is for

A freeze of **width and mixin geography** that already moved a grain:

1. Kirchenbauer green-list leak is a **body** leak under last-4
   interpolate (100-family tail **100/100**, opening **88/100**).
2. Matching `context_len` to that mixin’s last-1 hash recovers
   isolated hard sign (100-family **389/400** vs last-4 **209/400**).
3. On public SynthID $\Hw=4$, the existing `hard` reader is stronger at
   last-2 than at last-4 for **full-file** isolated sign, without
   fixing leftover and without touching interpolate. At n=100 that
   lift is opening mass kept in the file mean, not a body leak. The
   jump does not repeat at $\Hw=12$.

Keep leftover-20 as the honesty bound on any SynthID width change.
Do not write `thesis/` from this file.
