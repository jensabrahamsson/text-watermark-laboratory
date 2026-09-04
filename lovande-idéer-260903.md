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

Isolated $\tau=0$ on GPT-2 Kirchenbauer interpolate windows is also
back-loaded: 0:4 **28/48** (file-level binom $p\approx 0.16$); 64:128
**40/48**. Full-file **44/48** sits with the tail.

SynthID twins: `experiments/2026-08-17-pair-12x4/` (public
`ngram_len=5`, $\Hw=4$). Kirchenbauer twins:
`experiments/2026-09-03-pair-12x4-kgw/` (opened in
[research/PROTOCOL-next-kgw.md](research/PROTOCOL-next-kgw.md)).

Same spatial split on DistilGPT2 Kirchenbauer 12×4: interpolate 0:4
**9/12**, isolated **29/48** (binom $p\approx 0.10$); tail 64:128
**12/12**, AUC **0.836**, isolated **35/48**; full-file isolated
**42/48**, AUC **0.947**. Qwen2-1.5B Kirchenbauer 12×4: interpolate
0:4 **7/12**, isolated **28/48**, AUC **0.516** (chance); 64:128
**12/12**, AUC **0.819**, isolated **34/48**; full-file isolated
**35/48**, AUC **0.814**, one ranking-only (library). Occupancy-free `postokhits` on GPT-2
Kirchenbauer openings (`--fit-prefix 4 --pos-bucket 1`) is weak:
isolated **11/48**. Full-file interpolate **12/12** is not an
exact-copy detector (atoms: 114 seen vs 12071 unseen).
Unmarked-LM `rankpath` on the same GPT-2 Kirchenbauer 12×4 is weaker
than interpolate: full file **10/12**, **31/48**, AUC **0.634**; tail
64:128 **11/12**, **30/48**, **0.648**; opening 0:4 **8/12**,
**23/48**, **0.604**. Count tables, not rankpath, are the body reader.

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

Confirmatory n=100 last-4 `rankpath` (`--rankpath-pos-bucket 0`,
`--skip-nested`, windows 0:4 and 64:128; Distil uses `--model gpt2`,
same BPE) stays far below interpolate:

| Corpus | full file | 0:4 | 64:128 |
|---|---|---|---|
| GPT-2 KGW 100 rankpath | 79/100, **248/400**, 0.679, unmarked **253/400**, **20** ranking-losses-with-TP | 58/100, **206/400**, 0.526, perm $p\approx 0.07$, isolated chance (binom $p\approx 0.29$) | 71/100, **222/400**, 0.607, unmarked **230/400** |
| Distil KGW 100 rankpath | 82/100, **199/400**, 0.681, isolated chance (binom $p\approx 0.56$), **5** ranking-only | 77/100, **243/400**, 0.609 | 62/100, **128/400**, 0.601, isolated chance (binom $p=1$) |

GPT-2 interpolate last-4 tail remains **100/100**, **364/400**,
**0.953**. Rankpath tail **71/100** / **222/400** / **0.607** is not
that body reader. Distil interpolate last-4 tail was **98/100**,
**194/400**; Distil rankpath isolated **199/400** is chance at
$\tau=0$ while ranking still **82/100**. Count tables, not rankpath,
remain the Kirchenbauer body reader at confirmatory n. Do not sell
**248/400**, **199/400**, or ranking **82/100**.

Table-free `--snaprate` (`snapleave` / `snapupset`; unmarked-LM argmax
geometry, no twin tables) **ranks** GPT-2 Kirchenbauer but does not
sign isolated files at $\tau=0$. 12×4 snapleave is **10/12**, AUC
**0.726**, perm $p\approx 0.0035$, marked>0 **46/48** with unmarked
$\le 0$ only **1/48**; snapupset **9/12**, **0.723**. Confirmatory
n=100 snapleave is **88/100**, AUC **0.755**, perm $p\approx 0.0005$,
marked>0 **386/400** with unmarked $\le 0$ **15/400**; snapupset
**89/100**, **0.755**, unmarked $\le 0$ **24/400**. Nested Youden
n=100 is **271/400** vs **302/400** (snapleave) and **290/400** vs
**281/400** (snapupset). Both classes leave the unmarked argmax;
$\tau=0$ is not a detector. DistilGPT2 Kirchenbauer snaprate does
**not** replicate: 12×4 snapleave **9/12**, AUC 0.658, perm
$p\approx 0.21$; n=100 **31/100**, AUC **0.447**, perm $p=1$ (mean
marked more negative). The same reader on GPT-2 public SynthID
($\Hw=4$) and GPT-2 $\Hw=12$ is chance ranking at confirmatory n:
public 12×4 snapleave **9/12**, AUC **0.613**, perm $p\approx 0.042$
dies at n=100 (**52/100**, AUC **0.512**, perm $p\approx 0.18$,
marked>0 **385/400**, unmarked $\le 0$ **11/400**) and at 36×4
(**18/36**, AUC **0.482**). Grok-register 12 snapleave **10/12**, AUC
**0.589**, perm $p\approx 0.040$ is the same n=12 look; do not sell
it. GPT-2 $\Hw=12$ n=100 AUC **0.507**. Distil public SynthID n=100 is also chance
(**53/100**, **0.488**). Distil $\Hw=12$ n=100 snapleave ranks
**73/100**, AUC **0.631**, perm $p\approx 0.0005$, unmarked $\le 0$
**83/400** (GPT-2 $\Hw=12$ was **11/400**); n=12 was **4/12**, AUC
**0.434**. That Distil ranking is not a public $\Hw=4$ detector and is
not Distil KGW (anti **31/100**). Do not sell **73/100** or n=12
public **9/12**. Interpolate last-4 remains **100/100**, **0.953** on
the GPT-2 KGW tail and still ranks Distil KGW. Count tables, not
snaprate, remain the Kirchenbauer body reader. Qwen2-1.5B Kirchenbauer
12×4 snapleave ranks **10/12**, AUC **0.686**, perm $p\approx 0.0005$,
marked>0 **47/48** with unmarked $\le 0$ **4/48**; snapupset
**11/12**, **0.696**. That is n=12 same-tokenizer corroboration of the
GPT-2 ranking look, not Distil n=100. Isolated $\tau=0$ still fails.
Qwen public SynthID 12 snapleave is chance (**6/12**, AUC 0.453);
Qwen $\Hw=12$ 12 is **9/12**, AUC 0.583, perm $p\approx 0.17$. Do not
sell snapleave ranking **88/100**, marked>0 **386/400**, nested
**271/400**, 12-file **10/12**, Qwen **10/12**, Distil **9/12**, Distil
$\Hw=12$ **73/100**, public SynthID **9/12**, grok12 **10/12**, or
36×4 **18/36**. `--snaprate` does not
emit `--windows` slices (it scores the generated path only).
`snapmiss` (chosen token missed the unmarked top-k) does **not**
carry the GPT-2 KGW ranking: n=100 is **56/100**, AUC **0.518**, perm
$p\approx 0.29$, isolated **0/400**, **56** ranking-only. Distil KGW
snapmiss is anti (**32/100**, **0.385**), same direction as Distil
snapleave. The table-free KGW ranking is in-topk argmax upsets, not
missing the top-k. Public SynthID snapmiss **62/100**, AUC **0.577**,
perm $p\approx 0.0005$ is **62** ranking-only, isolated **0/400**;
Distil $\Hw=12$ snapmiss **74/100**, **0.644**, also **0/400**. Do not
leftover-target those zeros. Aaronson snapmiss is anti (**2/100**,
AUC **0.079**); do not invert. Do not sell snapmiss **56/100**,
**62/100**, or **74/100**.

Same last-4 interpolate tables transfer that body leak across
same-BPE generators (`--overlap keep`, `--skip-nested`, `--model gpt2`):

| Train → test | full file | 0:4 | 64:128 |
|---|---|---|---|
| Distil 100 → GPT-2 100 | **100/100, 331/400, 0.975**, unmarked **392/400** | 84/100, 223/400, 0.666 | **100/100, 306/400, 0.924**, unmarked **366/400**, **2** ranking-only |
| GPT-2 100 → Distil 100 | 99/100, **385/400**, 0.935, unmarked **323/400**, one ranking-loss-with-TP | 84/100, **309/400**, 0.696 | **100/100**, isolated **223/400**, 0.888, **16** ranking-only |

Last-4 hard Distil → GPT-2 100 was **81/100**, isolated only
**53/400**. Interpolate last-4 on the same transfer is a **body** leak:
full-file **331/400** sits with the tail **306/400**. GPT-2 → Distil
interpolate ranks the tail **100/100** while isolated **385/400** sits
with the opening **309/400** (Distil newline-loop files; tail isolated
**223/400**). Distil tables on GPT-2 files remain the cleaner body
isolated count, same as last-1. Do not sell **331/400**, **385/400**,
or tail ranking **100/100**.

Same last-4 interpolate tables on 100 → original-12 (default
`drop-from-train`, dropped=0; `--skip-nested`, `--model gpt2`) recover
isolated sign that last-4 **hard** missed on those 12-file tests:

| Train → test | full file | 0:4 | 64:128 |
|---|---|---|---|
| Distil 100 → GPT-2 12 | **12/12, 43/48, 0.967**, unmarked **40/48** | 11/12, 35/48, 0.714 | **12/12, 42/48, 0.928**, unmarked **39/48** |
| Distil 100 → Distil 12 | **12/12, 42/48, 0.982**, unmarked **45/48** | 10/12, 30/48, 0.732 | **12/12, 40/48, 0.957**, unmarked **44/48** |
| GPT-2 100 → Distil 12 | **12/12, 46/48, 0.986**, unmarked **41/48** | 11/12, 31/48, 0.686 | **12/12, 43/48, 0.935**, unmarked **40/48** |
| GPT-2 100 → GPT-2 12 | **12/12, 46/48, 0.967**, unmarked **40/48** | 10/12, 34/48, 0.737 | **12/12, 42/48, 0.933**, unmarked **36/48** |

Last-4 hard on those same arrows was Distil → GPT-2 12 **15/48**, Distil
→ Distil 12 chance **6/48**, GPT-2 → Distil 12 **22/48**, GPT-2 → GPT-2
12 **32/48**. Interpolate last-4 sits with the **tail** on every
12-file arrow (no ranking-only wins). Distil 100 → Distil 12 last-4
interpolate **42/48** matches that pair’s last-1 **hard** isolated
(idea 2); last-4 hard was chance. Do not sell **46/48**, **43/48**, or
**42/48**.

Those same last-4 interpolate tables do **not** classify public
SynthID or Grok-register SynthID (default `drop-from-train`,
dropped=0; `--skip-nested`; last-1 KGW already failed isolated
**6/48**):

| Train → test | full file | 0:4 | 64:128 |
|---|---|---|---|
| GPT-2 100 → SynthID 12 | 7/12, **0/48**, 0.527, perm $p\approx 0.26$, **7/7** ranking-only | 8/12, 15/48, 0.537 | 6/12, 3/48, 0.476 |
| Distil 100 → SynthID 12 | 7/12, **2/48**, 0.576, **6/7** ranking-only | 4/12, 8/48, 0.324 | 8/12, 5/48, 0.534 |
| GPT-2 100 → grok12 | 8/12, **5/48**, 0.504, perm $p\approx 0.41$ | 4/12, 11/48, 0.414 | 8/12, 9/48, 0.553 |
| Distil 100 → grok12 | 6/12, **7/48**, 0.570, perm $p\approx 0.15$ | 4/12, 10/48, 0.396 | 8/12, 9/48, 0.544 |
| GPT-2 12 → SynthID 12 (`--overlap keep`) | 6/12, **6/48**, 0.546, perm $p\approx 0.45$, **5/6** ranking-only | 7/12, 23/48, 0.502 | 7/12, 12/48, 0.528 |
| GPT-2 100 → SynthID 36 | 10/36, **8/144**, 0.448, perm $p\approx 0.92$ | 13/36, 28/144, 0.381 | 14/36, 18/144, 0.481 |
| Distil 100 → Distil SynthID 12 | 4/12, **1/48**, 0.445, perm $p\approx 0.80$ | 8/12, 30/48, 0.617 | 5/12, 4/48, 0.494 |
| Distil 12 → Distil SynthID 12 (`--overlap keep`) | 7/12, **3/48**, 0.507, perm $p\approx 0.44$ | 8/12, 25/48, 0.560 | 6/12, 6/48, 0.520 |
| Qwen 12 → Qwen SynthID 12 (`--overlap keep`) | **1/12**, **15/48**, 0.441, perm $p\approx 0.88$ | 5/12, 23/48, 0.457 | 5/12, 14/48, 0.395 |
| GPT-2 100 → ngram-13 12 | 7/12, **1/48**, 0.500, **6/7** ranking-only | 4/12, 12/48, 0.357 | 6/12, 8/48, 0.528 |
| GPT-2 100 → ngram-13 100 (`--overlap keep`) | 56/100, **51/400**, 0.513, perm $p\approx 0.26$, **25** ranking-only | 44/100, 147/400, 0.462 | 53/100, 70/400, 0.512 |
| Distil 100 → Distil ngram-13 12 | 5/12, **1/48**, 0.441 | 8/12, 16/48, 0.577 | 4/12, 5/48, 0.428 |
| Distil 100 → Distil ngram-13 100 (`--overlap keep`) | 45/100, **24/400**, 0.450, perm $p\approx 0.997$, **35** ranking-only | 65/100, 280/400, 0.631 | 48/100, 29/400, 0.472 |

File-level binomial on isolated $\tau=0$ is $p=1$ on the **0/48**,
**2/48**, **8/144**, **1/48**, and **3/48** arrows. Same-generator Distil KGW
tables that recover Distil KGW 12 at **42/48** do not classify Distil
public SynthID (**1/48** / same-stem **3/48**). Qwen KGW 12 interpolate
**35/48** does not classify Qwen public SynthID (**15/48**, ranking
**1/12**). Opening **30/48** on the Distil-100 arrow is
not a detector (full file **1/48**); do not leftover-target it. The
body leak is mixin-specific. Do not leftover-target those zeros. Do
not sell **0/48**, **8/144**, **1/48**, **3/48**, or **15/48**.
GPT-2 100 interpolate last-4 → $\Hw=12$ original-12 is also isolated
**1/48**, AUC 0.500, six ranking-only. Same-prompt n=100 `--overlap
keep`: GPT-2 **51/400**, AUC 0.513; Distil **24/400**, 0.450. Distil
opening 0:4 **280/400**, AUC 0.631 is not a detector (full file
**24/400**); do not leftover-target it. Do not sell **51/400**,
**24/400**, or opening **280/400**.

Kirchenbauer is **back-loaded**. SynthID is **front-loaded**. Original-12
SynthID interpolate 64:128 **3/12** is not “the tail is chance at
every n”: 100-family interpolate 64:128 still ranks **93/100**. Do not
sell **93/100** or **100/100** as replacing **25/48**.

**Scope.** Local Hugging Face Kirchenbauer on GPT-2 / DistilGPT2 /
Qwen2-1.5B, original-12 strings, $T=128$, four draws. Pair dumps:
`experiments/2026-09-03-pair-12x4-kgw/`,
`experiments/2026-09-03-pair-distil-12x4-kgw/`,
`experiments/2026-09-03-pair-qwen-12x4-kgw/`,
`experiments/2026-09-03-pair-100x4-kgw/`,
`experiments/2026-09-03-pair-distil-100x4-kgw/`. Mixin-negative test
dirs: `experiments/2026-08-17-pair-12x4/`,
`experiments/2026-08-31-pair-36x4/`,
`experiments/2026-08-31-pair-distilgpt2-12x4/`,
`experiments/2026-08-31-pair-qwen-12x4/`,
`experiments/2026-09-01-pair-grok12x4/`,
`experiments/2026-09-03-pair-12x4-ngram13/`,
`experiments/2026-09-03-pair-100x4-ngram13/`,
`experiments/2026-09-04-pair-distil-12x4-ngram13/`,
`experiments/2026-09-04-pair-distil-100x4-ngram13/`,
`experiments/2026-09-01-pair-100x4/`,
`experiments/2026-09-01-pair-distil-100x4/`. Not production Gemini.
Not leftover targeting. Windows keep absolute generated indices.

**Hypothesis.** The two mixins leak in opposite places under the same
count-table reader. Kirchenbauer’s green list is a **body** leak.
SynthID tournament last-4 interpolate is **opening-heavy**; the
original-12 tail **3/12** overstates how dead the body is at n=100.

**Non-claim.** This does not replace **25/48**. Full-file Kirchenbauer
interpolate **12/12** / **44/48** / **85/96** is a different mixin and
already opened; do not sell those counts as isolated SynthID
detection. Occupancy-free KGW openings are **not** the leak. Rankpath
on Kirchenbauer 12 is below interpolate; do not sell **31/48**. Distil
100-family Kirchenbauer interpolate **100/100** /
isolated **683/800** (opened on `main`) is the same construction at
confirmatory scale, still not **25/48**. Confirmatory n=100 rankpath
is not the interpolate body reader; do not sell **248/400**, Distil
isolated **199/400**, or ranking **82/100**. Distil → GPT-2 last-4
interpolate **331/400** is a different mixin and a transfer, not
**25/48**. Do not sell **331/400** or GPT-2 → Distil **385/400**. Last-4
interpolate 100 → original-12 **46/48** / **43/48** / **42/48** is the
same Kirchenbauer body reader on 12-file tests, not **25/48**. Do not
sell those 12-file counts. Last-4 interpolate KGW tables do **not**
classify public SynthID (**0/48** / **2/48** / **8/144**) or grok12
(**5/48** / **7/48**); same-stem GPT-2 12 KGW → SynthID 12 is
**6/48**; Distil KGW → Distil SynthID is **1/48** / **3/48**; Qwen KGW
12 → Qwen SynthID 12 is **15/48**; $\Hw=12$ original-12 is **1/48**;
n=100 $\Hw=12$ is **51/400** / Distil **24/400**. Do not leftover-target
Distil $\Hw=12$ opening **280/400**. Do not sell
Distil/Qwen interpolate isolated tails **35/48** / **34/48** or GPT-2
tail **40/48**. Do
not sell confirmatory tail **100/100** or SynthID tail **93/100** as
an isolated-file detector. Do not sell Distil $\Hw=12$ snapleave
**73/100** or public SynthID snapleave **9/12** / **52/100** /
grok12 **10/12** / 36×4 **18/36**. Do not sell snapmiss **56/100**,
public snapmiss **62/100**, or Distil $\Hw=12$ snapmiss **74/100**.

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

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-rankpath-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-rankpath-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --model gpt2 --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-kgw-rankpath-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-snaprate

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-snaprate

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-12x4-kgw \
  --model gpt2 --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-kgw-snaprate

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --model gpt2 --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-kgw-snaprate

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-qwen-12x4-kgw-snaprate

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-snaprate

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-snaprate

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-qwen-12x4-aaronson-snaprate

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-aaronson-snaprate

python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-12x4-synthid-snaprate

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-synthid-snaprate

python -m text_watermark_tools probe experiments/2026-08-31-pair-distilgpt2-12x4 \
  --model gpt2 --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-synthid-snaprate

python -m text_watermark_tools probe experiments/2026-09-01-pair-distil-100x4 \
  --model gpt2 --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-synthid-snaprate

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-ngram13 \
  --model gpt2 --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-ngram13-snaprate

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-ngram13 \
  --model gpt2 --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-ngram13-snaprate

python -m text_watermark_tools probe experiments/2026-08-31-pair-qwen-12x4 \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-qwen-12x4-synthid-snaprate

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-ngram13 \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-qwen-12x4-ngram13-snaprate

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok12x4 \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-grok12x4-synthid-snaprate

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-36x4-synthid-snaprate

python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-12x4-aaronson-snaprate

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods snapmiss --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-snapmiss

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods snapmiss --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-snapmiss

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --methods snapmiss --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-synthid-snapmiss

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-ngram13 \
  --model gpt2 --methods snapmiss --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-ngram13-snapmiss

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --model gpt2 --methods snapmiss --snaprate --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-kgw-snapmiss

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-kgw --overlap keep --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-gpt2100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-distil-100x4-kgw --overlap keep --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-distil100

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-12x4-kgw --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-distil-12x4-kgw --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-distil-12x4-kgw --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-12x4-kgw \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-synthid12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-08-17-pair-12x4 --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-synthid12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-grok12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-01-pair-grok12x4 --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-grok12

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --test-dir experiments/2026-08-17-pair-12x4 --overlap keep \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt212-kgw-interp-k4-to-synthid12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-synthid36

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-synthid-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-12x4-kgw \
  --model gpt2 --methods interpolate --context-len 4 --skip-hashpool \
  --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-kgw-interp-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct --methods interpolate --context-len 4 \
  --skip-hashpool --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-12x4-kgw-interp-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-12x4-kgw \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 --overlap keep --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil12-kgw-interp-k4-to-synthid-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --test-dir experiments/2026-08-31-pair-qwen-12x4 --overlap keep \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-qwen12-kgw-interp-k4-to-synthid-qwen12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-12x4-ngram13 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-ngram13-12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-12x4-ngram13 --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-distil-ngram13-12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-100x4-ngram13 --overlap keep --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-distil-ngram13-100
```

**Why it is a backlog item.** If the next honesty pass needs a
reader that is not front-loaded, match the mixin: Kirchenbauer count
tables rank 64:128 at both 12 and 100 families. Confirmatory n=100
rankpath last-4 does not become that body reader (GPT-2 tail **71/100**
/ **222/400** versus interpolate **100/100** / **364/400**; Distil
isolated **199/400** is chance). Last-4 interpolate tables transfer
the same body leak across Distil and GPT-2 at n=100 (**331/400** vs
last-4 hard **53/400**) and on 100 → original-12 (Distil → Distil 12
**42/48** vs hard chance **6/48**; Distil → GPT-2 12 **43/48** vs
**15/48**); last-4 hard ranking can look fine while files
do not sign. Isolated $\tau=0$ on Distil/Qwen 12 interpolate last-4 is
the same body split (Distil tail **35/48** vs opening **29/48**; Qwen
tail **34/48** vs opening chance **28/48**). Last-4 interpolate KGW
tables do not classify public SynthID (**0/48** / **8/144**) or
Distil public SynthID (**1/48** / **3/48**) or Qwen public SynthID
(**15/48**) or grok12 (**5/48**) or $\Hw=12$ original-12 (**1/48**) or n=100
$\Hw=12$ (**51/400** / Distil **24/400**). Do not leftover-target those
zeros. Do not leftover-target Distil $\Hw=12$ opening **280/400**. Do not spend another leftover-targeting round trying to
recover SynthID’s original-12 interpolate tail with last-4 tables.

---

## 2. Match `context_len` to last-1 hash width (Kirchenbauer and Aaronson–Kirchner)

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

Interpolate last-1 on GPT-2 KGW 12 is already the last-4 interpolate
reader: full-file **44/48** (last-4 interpolate **44/48**); opening
0:4 **7/12**, **27/48**, 0.597; tail 64:128 **12/12**, **42/48**,
0.907. Distil interpolate last-1 windows match last-4 interpolate:
0:4 **9/12**, **29/48**, 0.681; 64:128 **12/12**, **36/48**, 0.839.
Qwen interpolate last-1: 0:4 **7/12**, **28/48**, 0.529 (chance);
64:128 **12/12**, **34/48**, 0.832. The last-1 jump is `hard` / `hits`
/ `hashpool`, not interpolate. Confirmatory 100-family interpolate
last-1 windows (`--skip-nested`) match last-4 interpolate geography:
0:4 **83/100**, **259/400**, AUC **0.685**; 64:128 **100/100**,
**367/400**, **0.957**. Last-4 interpolate was 0:4 **88/100**,
**258/400**, **0.694**; 64:128 **100/100**, **364/400**, **0.953**.
Full-file interpolate last-1 **383/400** vs last-4 **376/400**. Same
body reader. Do not sell interpolate last-1 opening **83/100** or tail
**367/400**. Distil 100 interpolate last-1 windows match last-4
interpolate the same way: 0:4 **80/100**, **281/400**, AUC **0.675**;
64:128 **99/100**, isolated **194/400**, **0.885**, unmarked $\le 0$
**370/400**, **18** ranking wins with no isolated TP. Last-4
interpolate tail was **98/100**, **194/400**, **0.880**. Isolated tail
**194/400** is the Distil newline-loop files, not a last-1 jump. Do
not sell Distil interpolate last-1 tail **194/400** or **99/100**.

GPT-2 KGW last-1 tail 64:128 is **12/12** hard, AUC **0.887**,
isolated **43/48**. Opening 0:4 last-1 hard is only **6/12**. The
last-1 lift is a **body** lift, same spatial pattern as idea 1.
Confirmatory 100-family last-1 hard windows: 0:4 **94/100**, AUC
**0.740**, isolated **257/400**; 64:128 **100/100**, AUC **0.962**,
isolated **372/400**.

Qwen2-1.5B KGW last-1 hard windows: 0:4 **8/12**, **29/48**, AUC
**0.536**; 64:128 **12/12**, **37/48**, **0.757**. Same back-loaded
split.

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

Existing `hits` (shared last-k only; not a new method name) at
`--context-len 1` is the same width match on the overlap spec:

| Corpus | last-4 hits | last-1 hits |
|---|---|---|
| GPT-2 KGW 12×4 | 8/12, 26/48, 0.616 | **12/12, 46/48, 0.975** |
| DistilGPT2 KGW 12×4 | 9/12, 27/48, 0.603 | **12/12, 43/48, 0.971** |
| Qwen2-1.5B KGW 12×4 | 7/12, 22/48, 0.485 | **12/12, 41/48, 0.899** |
| GPT-2 KGW 100×4 | 93/100, 254/400, 0.812 | **100/100, 395/400, 0.996** |

Last-1 hits isolated **46/48** equals unigram on GPT-2 12, with AUC
**0.975** versus unigram **0.791** and unmarked $\le 0$ **40/48** versus
**27/48**. At n=100, last-1 hits isolated **395/400** slightly beats
last-1 hard **389/400**, with more FPs (unmarked $\le 0$ **383/400**
versus **399/400**). Qwen last-4 hits is chance; last-1 recovers
ranking, and isolated **41/48** beats Qwen last-1 hard **37/48**.
Public SynthID hits last-1 is chance (**4/12**,
**24/48**, AUC **0.445**). The width match is mixin-specific, not
“shorten `hits` everywhere.” Aaronson last-4 hits is already
**12/12**, **44/48**, AUC **0.920**, unmarked $\le 0$ **39/48** (one
ranking win with no isolated TP); last-1 hits is **40/48**, **0.988**,
unmarked **48/48**. At n=100 last-4 hits is **100/100**, **388/400**,
**0.990**, unmarked **362/400**; last-1 hits is **384/400**, **0.995**,
unmarked **400/400**. Hits last-4 matches Aaronson rankpath isolated
**44/48** and beats hard last-4 **24/48**, but the geography is
**not** the same leak. GPT-2 Aaronson last-4 hits absolute windows:
opening 0:4 **12/12**, **44/48**, AUC **0.924**; tail 64:128 **5/12**,
isolated **0/48**, AUC **0.482**, five ranking wins with no isolated
TP. DistilGPT2 Aaronson last-4 hits is the same split: 0:4 **11/12**,
**40/48**, **0.889**; tail **0/12**, **0/48**, **0.500** (all zeros).
Aaronson last-4 `hits` is **opening overlap**. Rankpath tail 64:128
is **44/48**. Do not treat those two **44/48** counts as one reader.
Last-1 `hits` on GPT-2 Aaronson is a **different** leak: opening 0:4
**12/12**, **44/48**, AUC **0.934**; tail 64:128 **11/12**, **40/48**,
**0.970**, unmarked $\le 0$ **47/48**. Full-file last-1 hits **40/48**
equals that tail. Last-4 hits tail was isolated **0/48**. Matching
`hits` width to `context_width=1` recovers the body that last-4 hits
missed; it is not “shorten hits and lose the opening copies.”
Confirmatory 100-family last-1 hits windows (`--skip-nested`):
0:4 **100/100**, **392/400**, AUC **0.992**, unmarked $\le 0$
**373/400**; 64:128 **100/100**, **372/400**, **0.989**, unmarked
**400/400**. Body at confirmatory n. Last-4 hits at the same n is
still opening-heavy: 0:4 **100/100**, **392/400**, **0.991**; 64:128
**90/100**, **260/400**, **0.837**, unmarked $\le 0$ **360/400**,
**25** ranking wins with no isolated TP. n=12 last-4 hits tail
**0/48** was the extreme; n=100 last-4 hits has some tail, and last-1
hits is the body match. Do not sell **392/400**, **372/400**, or
last-4 hits tail **260/400**. Occupancy-free `postokhits` last-4 is **12/12**, **40/48**,
AUC **0.892** on GPT-2 Aaronson and **10/12**, **40/48** on Distil;
last-1 `postokhits` is empty on both (**0/48**, all zeros). Occupancy-free
`hashtok` last-4 on GPT-2 Aaronson is **12/12**, **40/48**, AUC
**0.890** (matches `postokhits` last-4); last-1 `hashtok` is empty
(**0/48**). Do not sell
**46/48**, **395/400**, Qwen **41/48**, or Aaronson hits **44/48**.
GPT-2 KGW hits last-1 absolute windows: opening 0:4 **8/12**,
**24/48**, AUC **0.558**; tail 64:128 **12/12**, **45/48**, **0.932**.
Same body geography as hard last-1. Distil 12 hits last-1 windows:
opening 0:4 **9/12**, **31/48**, AUC **0.704**; tail 64:128 **12/12**,
**37/48**, **0.882**. 100-family hits last-1 windows
(`--skip-nested`): opening 0:4 **94/100**, **258/400**, AUC **0.753**;
tail 64:128 **100/100**, **379/400**, **0.986**. Body at confirmatory
n. Do not sell **379/400**. Distil 100 hits last-1 also ranks the tail
above the opening (**98/100**, AUC **0.924** vs **93/100**, **0.718**);
isolated tail **214/400** is below full-file **355/400**. Distil 100
last-1 hard windows (`--skip-nested`) are the same split: 0:4
**90/100**, **253/400**, AUC **0.709**, **2** ranking-only; 64:128
**98/100**, isolated **202/400**, **0.893**, unmarked $\le 0$
**370/400**, **18** ranking-only. Tail ranks; isolated t=0 on the tail
is chance (file-level binom $p\approx 0.44$). Full-file **350/400** is
not that tail. Distil 100 has newline-loop files; do not sell
**355/400** or Distil last-1 hard tail **202/400**. Qwen2-1.5B KGW hits
last-1 windows: opening 0:4 **8/12**, **33/48**, AUC **0.581**,
unmarked $\le 0$ only **18/48**; tail 64:128 **12/12**, **38/48**,
**0.893**, unmarked **41/48**. Ranking/AUC is body like GPT-2 and
Distil. Opening isolated **33/48** has FPs; do not sell it.

Existing `hashpool` (random-hash context pool; not a new method name)
at `--context-len 1` is the same width match on a different count spec:

| Corpus | last-4 hashpool | last-1 hashpool |
|---|---|---|
| GPT-2 KGW 12×4 | 12/12, 40/48, 0.747 | **12/12, 47/48, 0.979** |
| DistilGPT2 KGW 12×4 | 7/12, 26/48, 0.620 | **12/12, 43/48, 0.969** |
| Qwen2-1.5B KGW 12×4 | 6/12, 15/48, 0.519 | **12/12, 39/48, 0.901** |
| GPT-2 KGW 100×4 | 96/100, 304/400, 0.867 | **100/100, 394/400, 0.995** |
| DistilGPT2 KGW 100×4 | 95/100, 149/400, 0.759 | 99/100, 325/400, 0.872 |

Qwen last-4 hashpool is chance. Last-1 hashpool recovers ranking.
Unmarked $\le 0$ on GPT-2 12 last-1 hashpool is **41/48** (better than
unigram **27/48**). Distil 100 last-1 hashpool isolated **325/400** is
below Distil hard last-1 **350/400**: hashpool is not strictly better
than `hard` at every generator. Distil 100 last-4 hashpool ranks
**95/100** with isolated only **149/400** and **34** ranking wins that
have no isolated TP. GPT-2 KGW hashpool last-1 windows:
0:4 **9/12**, **27/48**, 0.570; 64:128 **12/12**, **46/48**, 0.946.
Same body geography as hard last-1. Distil 12 hashpool last-1
windows: 0:4 **10/12**, **27/48**, 0.685; 64:128 **12/12**, **36/48**,
0.882. Qwen hashpool last-1 windows: 0:4 **7/12**, **29/48**, 0.563
(file AUC chance-like, perm $p=0.184$); 64:128 **12/12**, **37/48**,
0.885. Full-file Qwen hashpool last-1 has one ranking win with no
isolated TP (library). Confirmatory 100-family hashpool last-1
windows (`--skip-nested`): 0:4 **95/100**, **263/400**, AUC **0.762**;
64:128 **100/100**, **377/400**, **0.985**. Body at confirmatory n,
same as hard last-1 and hits last-1. Do not sell **377/400**. Distil
100 hashpool last-1 windows: 0:4 **90/100**, **255/400**, AUC
**0.720**; 64:128 **99/100**, isolated **182/400**, **0.913**,
unmarked $\le 0$ **383/400**, **19** ranking wins with no isolated
TP. Tail ranks; isolated t=0 on the tail is below full-file
**325/400** (newline-loop files). Do not sell **182/400** or
**99/100**. Occupancy-free `postokhits` last-1
on GPT-2 KGW 12 is **9/12**, **33/48**, AUC 0.600, unmarked $\le 0$
only **25/48** (last-4 `postokhits` was **11/48**): last-1 occupancy-free
lifts isolated with FPs; it is not the green-list reader. Occupancy-free
`hashtok` last-4 on the same twins is **9/12**, **13/48**, AUC 0.592;
last-1 is empty (**0/48**, all zeros). Distil KGW last-1 `hashtok` is
also empty. Distil KGW last-4 `hashtok` is opening **7/12**,
**14/48**, AUC **0.605**, unmarked $\le 0$ only **40/48**; tail
**0/12**, **0/48**. Occupancy-free hashing is not the Kirchenbauer
last-1 body reader. Qwen KGW last-4 `hashtok` is anti-correlated
ranking **2/12**, isolated **14/48**, AUC **0.432** (opening; tail
**0/48**). Last-1 is empty (**0/48**). Hits last-1 **46/48** is not
occupancy-free hashing (`--skip-hashpool` silently drops `hashtok`).
Public
SynthID hashpool last-1 is chance (**5/12**, **24/48**, AUC 0.472). Do
not sell **47/48**, **394/400**, Distil last-4 hashpool **95/100**, or
**149/400**.

The same last-1 match holds on the laboratory Aaronson–Kirchner
exponential-minimum mixin (Aaronson & Kirchner, 2023; frozen in
[research/PROTOCOL-next-aaronson.md](research/PROTOCOL-next-aaronson.md);
`context_width=1`, not a new method name). Hard last-4 there is
**12/12**, isolated **24/48**, unmarked $\le 0$ **48/48**, AUC 0.976.
Last-1 hard is **12/12**, **40/48**, unmarked $\le 0$ **48/48**, AUC
0.957 (two ranking wins with no isolated TP). Last-2 sits in between
(**11/12**, **28/48**, 0.955). Interpolate last-1 isolated is
**20/48** versus last-4 interpolate **8/48**; ranking stays **11/12**.
Confirmatory 100-family last-1 hard (`--skip-nested`): **99/100**,
**388/400**, AUC **0.989**, unmarked $\le 0$ **399/400**, versus last-4
**95/100**, **344/400**, 0.950, unmarked **400/400**. Last-2 at n=100
(`--skip-nested`) is **98/100**, isolated **388/400** (same TP count as
last-1), AUC **0.973**, unmarked $\le 0$ only **301/400**. Last-2
matches last-1 isolated sign and wrecks specificity. Last-1 remains the
width match. Do not sell last-2 **388/400**. Interpolate
last-1 at n=100 is **100/100**, **296/400**, AUC 0.985, unmarked
$\le 0$ **400/400**, **26** ranking wins with no isolated TP (last-4
interpolate **208/400**). Hard last-1 **388/400** remains the isolated
reader. Hard last-1 windows both rank: 0:4 **100/100**, **388/400**,
0.987; 64:128 **99/100**, **380/400**, 0.985. That is **not**
Kirchenbauer’s tail-only last-1 split. Interpolate last-1 windows
(`--skip-nested`) are **not** that both-windows isolated geography:
0:4 **100/100**, **380/400**, AUC **0.993**, unmarked $\le 0$
**391/400**, **5** ranking wins with no isolated TP; 64:128
**99/100**, **284/400**, **0.980**, unmarked **400/400**, **28**
ranking wins with no isolated TP. Full-file interpolate last-1
**296/400** sits with the tail. Interpolate last-1 isolated is
opening-heavy; tail ranking is ranking-without-isolated-TP. Hard
last-1 is the body isolated reader. Do not sell interpolate last-1
opening **380/400** or tail **284/400**. Freeze interpolate last-4
windows (`--skip-nested`) match that opening-then-dilution: 0:4
**100/100**, **380/400**, AUC **0.988**, unmarked $\le 0$ **392/400**,
**5** ranking-only; 64:128 **99/100**, **208/400**, **0.980**, unmarked
**400/400**, **47** ranking-only. Full-file interpolate last-4
**208/400** equals the tail. Ranking **100/100** is ranking-without-TP
(**48/100**), not isolated **208/400**. Last-4 hard windows: 0:4
**100/100**, **388/400**, AUC **0.985**, unmarked only **323/400**
(FPs); 64:128 **95/100**, **324/400**, **0.944**, unmarked **398/400**,
**14** ranking-only. Full-file last-4 hard **344/400** sits with the
tail. Last-1 hard does not add opening TPs (both widths **388/400** at
0:4); it recovers tail isolated (**324/400** → **380/400**) and
specificity (unmarked **323/400** → **399/400**). Do not sell
interpolate last-4 opening **380/400**, last-4 hard opening **388/400**,
or freeze ranking **100/100**. Occupancy-free `hashtok` last-1 on GPT-2
Aaronson 100 is empty (**0/400**, all zeros). Last-4 `hashtok` (no
`--skip-hashpool`; `--fit-prefix 4`) is **100/100**, **384/400**, AUC
**0.982**, unmarked $\le 0$ **363/400** (precision **0.912**); 0:4 is
the same **384/400**; tail **0/100**, **0/400**. Opening overlap with
FPs, not last-1 hard **388/400**. Hits last-1 isolated **384/400** is
not this occupancy-free reader. Hashpool last-1 on Aaronson 12 is **11/12**, **36/48**, 0.901,
unmarked $\le 0$ **48/48** (below hard last-1). Last-1 hashpool
windows also rank both ends: 0:4 **12/12**, **40/48**, 0.950; 64:128
**10/12**, **36/48**, 0.877. 100-family hashpool
last-1 (`--skip-nested`) is **100/100**, isolated **372/400**, AUC
**0.992**, unmarked $\le 0$ **400/400**, **7** ranking wins with no
isolated TP. Hard last-1 **388/400** remains the isolated reader;
hashpool last-1 is the specificity companion. Do not sell hashpool
**372/400** or **100/100**. Hashpool last-1 windows at n=100
(`--skip-nested`) also rank both ends: 0:4 **100/100**, **388/400**,
AUC **0.991**, unmarked $\le 0$ only **372/400** (FPs), **3** ranking
wins with no isolated TP; 64:128 **99/100**, **360/400**, **0.985**,
unmarked **400/400**, **9** ranking wins with no isolated TP. Opening
isolated matches hard last-1 **388/400** with FPs; tail isolated is
below hard last-1 **380/400**. Full-file **372/400** sits with the
tail. Do not sell hashpool opening **388/400** or tail **360/400**.
100 → 12 last-1 hard
is **11/12**, **40/48**, 0.936, unmarked $\le 0$ **48/48**, one ranking
win with no isolated TP. Absolute windows on that transfer are a
**body** leak: 0:4 **12/12**, isolated **24/48**, AUC **0.917**,
unmarked **44/48**, **6** ranking wins with no isolated TP; 64:128
**11/12**, **40/48**, **0.915**, unmarked **48/48**. Full-file
**40/48** equals the tail. Last-1 `hits` 100 → 12 ranks **12/12**
with isolated only **36/48**, AUC **1.000**, unmarked **48/48**,
**3** ranking wins with no isolated TP; tail 64:128 is **12/12**,
**40/48**, **0.997**. Hard last-1 remains the isolated transfer
reader. Aaronson
last-1 tables do **not** classify Kirchenbauer 12 (isolated **0/48**,
AUC 0.504) or public SynthID 12 (**0/48**, AUC 0.597, ten ranking wins
with no isolated TP). Do not sell **40/48**, **388/400**, or **99/100**.
Existing `unigram` on Aaronson 12 ranks **12/12** with isolated only
**24/48**, unmarked $\le 0$ **48/48**, AUC 0.972, and **6** ranking
wins with no isolated TP — the same isolated count as last-4 hard, not
last-1 **40/48**. 100-family unigram is **96/100**, **308/400**, 0.961,
unmarked $\le 0$ **400/400**, **19** ranking wins with no isolated TP
(last-1 hard **388/400**). Aaronson last-1 is not a bag-of-tokens
companion the way Kirchenbauer unigram is. Do not sell unigram
**12/12** or **308/400**.

Existing `rankpath` (unmarked-LM five-symbol ranks; not a new method
name) on Aaronson 12 is already saturated at last-4: **12/12**,
isolated **44/48**, AUC **1.000**, unmarked $\le 0$ **48/48**, one
ranking win with no isolated TP (kitchen). Last-1 rankpath is the same
**44/48**. That is **not** a last-1 width match. Rankpath last-4
already beats hard last-1 isolated **40/48**. Kirchenbauer last-1
rankpath is only **12/12**, **33/48**, AUC **0.722**, unmarked $\le 0$
**34/48** — a small lift versus last-4 rankpath **10/12**, **31/48**,
**0.634**, and still below last-1 hard **43/48**. Count tables remain
the Kirchenbauer last-1 reader. DistilGPT2 Kirchenbauer last-4
rankpath is chance (**4/12**, **20/48**, AUC **0.397**). Last-1 Distil
KGW rankpath is still weak (**8/12**, **27/48**, AUC **0.602**). Rankpath
**44/48** is Aaronson-specific, not a general last-1-mixin recipe.
Aaronson rankpath last-4 absolute
windows: opening 0:4 **9/12**, **32/48**, AUC **0.721**; tail 64:128
**12/12**, **44/48**, **0.936**, unmarked $\le 0$ **48/48**. That is a
**body** leak in rank geometry, closer to Kirchenbauer interpolate
last-4 than to Aaronson hard last-1 (which ranks both windows at
n=100). Do not sell Aaronson rankpath **44/48**. Existing `rankuni` last-4 on
Aaronson 12 is the same **12/12**, **44/48**, AUC **1.000** — rank
unigrams suffice; the path of last-k ranks is not required. Table-free
`snapleave` on these twins is anti-correlated (**0/12**, **0/48**, AUC
**0.000**). Rank *tables*, not snap-rate, are the Aaronson geometry
reader. Aaronson rankpath
tables trained on the original 12 (`--overlap keep`, same stems,
different mixin) do **not** classify public SynthID 12 (isolated
**0/48**, AUC **0.541**, seven ranking wins with no isolated TP) or
Kirchenbauer 12 (**0/48**, AUC **0.568**). Mixin-specific. GPT-2
Aaronson 100 rankpath last-4 (`--skip-nested`, `--rankpath-pos-bucket
0`) is **100/100**, isolated **396/400**, AUC **1.000**, unmarked
$\le 0$ **398/400**, one ranking-only. Absolute windows: 0:4
**96/100**, **360/400**, **0.953**, unmarked **371/400**, **6**
ranking-only; 64:128 **100/100**, **392/400**, **1.000**, unmarked
**399/400**, **2** ranking-only. Full-file **396/400** sits with the
tail. GPT-2 12 rankpath tail **44/48** **does** survive confirmatory n
as an isolated body leak. Distil 100 rankpath below does **not**. Do
not sell **396/400** or tail **392/400**.

DistilGPT2 Aaronson 12×4 is the opened freeze
[research/PROTOCOL-next-aaronson-distil.md](research/PROTOCOL-next-aaronson-distil.md)
(`experiments/2026-09-04-pair-distil-12x4-aaronson/`, seed
**20260905**, Hub SHA `2290a62682d06624634c1f46a6ad5be0f47f38aa`).
Official first-draw $z>3$ is **12/12** (one unmarked first-draw is
also $z>3$). Freeze last-4 hard is **7/12**, isolated **8/48**, AUC
**0.637**, five ranking wins with no isolated TP; interpolate last-4
is **7/12**, **0/48**. Last-1 hard is **9/12**, **16/48**, **0.755**.
Last-2 is **9/12**, **24/48**, **0.759**. Last-1 still lifts vs last-4
on `hard`. Last-1 hard absolute windows: opening 0:4 **11/12**,
**40/48**, AUC **0.807**, unmarked $\le 0$ only **29/48**; tail 64:128
**7/12**, **12/48**, **0.686**, unmarked **48/48**. Full-file last-1
**16/48** is opening mass that does not survive the file mean, not a
Kirchenbauer-style tail. Do not sell that opening **40/48** (FPs).
Last-2 isolated wins at this n=12; that does not replace
GPT-2 Aaronson last-1 **40/48**. Existing last-4 `hits` on these twins
is **11/12**, isolated **44/48**, AUC **0.924**, unmarked $\le 0$
**38/48** — the same isolated count as Distil rankpath, far above
last-1 hard **16/48**. That **44/48** is **opening overlap**: hits
window 0:4 is **11/12**, **40/48**, **0.889**; tail 64:128 is
**0/12**, **0/48**. Rankpath is the opposite split (tail **44/48**).
Last-1 `hits` **hurts** the full-file isolated count (**10/12**,
**32/48**, **0.800**) relative to last-4 opening copies, but last-1
hits **recovers a tail** last-4 hits missed: opening 0:4 **12/12**,
**40/48**, **0.908**; tail 64:128 **10/12**, **32/48**, **0.752**,
unmarked **48/48**. Last-4 hits tail was **0/48**. Hashpool last-1
windows stay opening-heavy: 0:4 **11/12**, **36/48**, **0.847**; tail
**7/12**, **20/48**, **0.641**. Occupancy-free `postokhits` last-4 is **10/12**,
**40/48**, **0.925**, unmarked $\le 0$ **45/48** (matches hits 0:4
isolated **40/48**); last-1
`postokhits` is empty (**0/12**, **0/48**, all 48 marked zeros).
Occupancy-free `hashtok` last-4 (no `--skip-hashpool`; `--fit-prefix 4`)
is **10/12**, **44/48**, AUC **0.944**, unmarked $\le 0$ only
**40/48** (8 FPs, precision **0.846**); 0:4 is the same **44/48**;
tail **0/12**, **0/48**. Opening overlap with FPs, not rankpath’s
body leak. Last-1 `hashtok` is empty (**0/48**, all zeros). Hashpool last-4 **10/12**, **32/48**, **0.762** beats last-1
**8/12**, **20/48**, **0.682**. Interpolate last-1 stays **7/12**,
**0/48**. On Distil Aaronson, last-1 is a small `hard` lift. Last-1
`hits` recovers a tail last-4 hits missed (**32/48** vs **0/48**)
while the full-file isolated count drops because last-4 was opening
copies. Hashpool last-1 does **not** recover that tail (**7/12**).
Existing `rankpath` last-4 is **12/12**, **44/48**, AUC
**0.998**, unmarked $\le 0$ **48/48** (garden ranks with no isolated
TP). Last-1 rankpath is the same **44/48**. Rankpath last-4 absolute
windows match GPT-2 Aaronson geography: opening 0:4 **9/12**,
**32/48**, AUC **0.785**; tail 64:128 **12/12**, **44/48**, **1.000**,
unmarked $\le 0$ **48/48** — a **body** leak in rank geometry. GPT-2
Aaronson 12 rankpath tables (`--overlap keep`, same stems, same BPE)
copy onto Distil files: **12/12**, **44/48**, AUC **1.000**, same
garden miss. Last-4 hits is the Distil opening-overlap reader; rankpath
is the body reader. Last-1 hard is a smaller in-domain full-file lift.
GPT-2 100 Aaronson last-1 `hard` tables copy onto Distil files as a
**body** leak: tail 64:128 **11/12**, **40/48**, AUC **0.913**, unmarked
$\le 0$ **48/48** (equals full-file isolated **40/48**); opening 0:4
**12/12**, **36/48**, **0.906**. Last-4 hard transfer ranks **12/12**
with isolated only **16/48**. GPT-2 100
Aaronson last-4 `hits` tables also copy onto Distil files:
**12/12**, **44/48**, AUC **0.957** (last-1 hits transfer **32/48**,
four ranking wins with no isolated TP) — that hits copy is opening
overlap, not the last-1 body transfer. Do not sell Distil last-2 **24/48**, last-1
**16/48**, interpolate **0/48**, Distil hits last-4 **44/48**,
hits opening **40/48**, last-1 hard opening **40/48**, postokhits **40/48**, hashpool **32/48**, Distil rankpath **44/48**,
hits transfer **44/48**, last-1 transfer **40/48**, Distil hashtok last-4
**44/48**,
or rankpath transfer **44/48**.

DistilGPT2 Aaronson 100×4 is the opened freeze
[research/PROTOCOL-next-aaronson-distil-100.md](research/PROTOCOL-next-aaronson-distil-100.md)
(`experiments/2026-09-04-pair-distil-100x4-aaronson/`, seed
**20260905**). Freeze last-4 hard is **91/100**, isolated
**308/400**, AUC **0.899**, unmarked $\le 0$ **346/400**, **17**
ranking wins with no isolated TP; interpolate last-4 is **96/100**,
**252/400**, **0.902**, **36** ranking-only (**601/800**). Official
first-draw $z>3$ is only **71/100** (twenty-nine degenerate loops).
Last-1 is post-open (`--model gpt2`, `--skip-nested`). Last-1 hard is
**94/100**, **372/400**, AUC **0.930**, unmarked **344/400**, **4**
ranking-only. Last-1 still lifts full-file isolated versus last-4
(**308/400** → **372/400**). That is **not** GPT-2 Aaronson last-1’s
both-windows isolated geography (tail **380/400**). Absolute windows
(`--skip-nested`):

| Reader | full file | 0:4 | 64:128 |
|---|---|---|---|
| last-4 hard freeze | 91/100, 308/400, 0.899 | 92/100, **364/400**, 0.881 | 89/100, 196/400, 0.889, **40** ranking-only |
| last-1 hard | **94/100, 372/400**, 0.930 | 92/100, 356/400, 0.879 | 93/100, 240/400, 0.916, **33** ranking-only |
| last-1 hits | **97/100, 380/400**, 0.948 | 94/100, 360/400, 0.903 | 96/100, 256/400, 0.947, **32** ranking-only |
| last-4 hits | 94/100, 376/400, 0.922 | 94/100, **368/400**, 0.901 | **56/100**, 140/400, 0.673 |
| last-1 hashpool | 97/100, 364/400, 0.935 | 93/100, 348/400, 0.899 | 95/100, 232/400, 0.938, **37** ranking-only |
| last-4 interpolate freeze | 96/100, 252/400, 0.902, **36** ranking-only | 93/100, **352/400**, 0.908 | 95/100, 128/400, 0.897, **63** ranking-only |
| last-1 interpolate | 97/100, 296/400, 0.919, **26** ranking-only | 91/100, 348/400, 0.899 | 95/100, 176/400, 0.919, **51** ranking-only |
| last-4 rankpath | 97/100, 372/400, 0.871, **7** ranking-only | 87/100, **344/400**, 0.836 | 97/100, 280/400, 0.958, **27** ranking-only |

Opening isolated is already saturated at last-4 hard (**364/400**).
Last-1 does not add opening TPs (last-1 opening **356/400**). The
full-file lift is less dilution of that opening in the file mean
(last-4 full-file **308/400** sits well below opening **364/400**;
last-1 full-file **372/400** sits with opening **356/400**) plus a
modest tail isolated lift (**196/400** → **240/400**). Tail ranking
is ranking-without-isolated-TP, not GPT-2 Aaronson tail isolated
**380/400**. Distil 12 last-1 hard opening **40/48** that did not
survive the file mean (**16/48**) is the same dilution; n=100 last-1
reduces it. Distil 12 last-1 hits tail isolated **32/48** equaled
full-file; n=100 last-1 hits tail **256/400** is below full-file
**380/400**. Last-1 hits still recovers tail **ranking** last-4 hits
missed (**56/100** → **96/100**; Distil 12 tail **0/48** →
**32/48**). Last-4 hits remains opening overlap (full-file
**376/400** equals opening **368/400**; tail AUC **0.673**). Freeze
interpolate **96/100** is the same split: opening isolated
**352/400**, tail isolated **128/400** with **63** ranking-only. Do
not sell last-1 **372/400**, hits **380/400**, interpolate ranking
**96/100**, tail ranking **95/100**, or rankpath **372/400**. Last-1 unigrams on Distil
degenerate loops are not a reason to sell those counts
(H-aar-d100-ctrl **71/100**). Occupancy-free `hashtok` last-1 on Distil
Aaronson 100 is empty (**0/100**, **0/400**, all zeros), same as Distil
12. Last-4 `hashtok` (no `--skip-hashpool`; `--fit-prefix 4`) is
**90/100**, **352/400**, AUC **0.865**, unmarked $\le 0$ only
**290/400** (precision **0.762**); 0:4 is the same **352/400**; tail
**0/100**, **0/400**. Opening overlap with FPs, not last-1 hard’s
full-file **372/400** or GPT-2 Aaronson last-1 body. Hits last-1 is
not occupancy-free hashing.

Existing `rankpath` last-4 on Distil Aaronson 100 (`--model gpt2`,
`--rankpath-pos-bucket 0`, `--skip-nested`) is **97/100**, isolated
**372/400**, AUC **0.871**, unmarked $\le 0$ **336/400**, **7**
ranking-only. Absolute windows: 0:4 **87/100**, **344/400**, AUC
**0.836**, unmarked only **298/400** (FPs), **7** ranking-only; 64:128
**97/100**, isolated **280/400**, **0.958**, unmarked **386/400**,
**27** ranking-only. Ranking and AUC are still **body** (tail
**97/100**, **0.958** vs opening **87/100**, **0.836**), the Distil 12
rankpath split. Isolated t=0 is **opening-heavy**: full-file
**372/400** sits with 0:4 **344/400**, not the tail **280/400**. Distil
12 rankpath tail isolated **44/48** that equaled the file mean does
**not** survive confirmatory n. Last-1 hard full-file **372/400**
matches this rankpath isolated count; last-1 hard tail was only
**240/400**. Rankpath tail isolated **280/400** is above last-1 hard
tail, still below GPT-2 Aaronson last-1 tail **380/400** and far below
GPT-2 Aaronson 100 rankpath tail **392/400**. Distil 12 rankpath body
isolated does not become GPT-2 100 rankpath body isolated. Do not sell
rankpath **372/400**, opening **344/400**, tail ranking **97/100**, or
Distil 12 rankpath **44/48** as n=100 isolated.

GPT-2 Aaronson 100 last-1 `hard` tables copy onto Distil Aaronson 100
(`--overlap keep`, same 100 one-liners, same BPE): full-file
**68/100**, isolated **244/400**, AUC **0.698**, unmarked $\le 0$
**396/400**, **7** ranking-only. Absolute windows are a **body**
ranking leak: opening 0:4 **66/100**, **248/400**, **0.673**; tail
64:128 **92/100**, **244/400**, **0.920**, unmarked **387/400**,
**31** ranking-only. Full-file isolated **244/400** equals the tail.
Last-4 hard transfer isolated is chance (full-file **188/400**,
file-level binom $p\approx 0.89$); tail still ranks **92/100** with
isolated only **176/400** and **48** ranking-only. Distil in-domain
last-1 **372/400** is opening dilution on Distil text, not this
GPT-2-table body transfer. Last-1 `hits` transfer ranks **97/100**,
isolated **240/400**, AUC **0.963**, unmarked **398/400**, **37**
ranking-only — isolated **240/400** in every window; tail
**96/100**. Last-4 hits transfer ranks **81/100**, tail **42/100**,
AUC **0.614**. Do not sell transfer **244/400**, hits ranking
**97/100**, or tail ranking **92/100**. Distil 12 last-1 hard
transfer **40/48** (tail equals full-file) is the n=12 slice of this
body ranking; n=100 full-file ranking **68/100** is dragged by the
opening.

The reverse Distil Aaronson 100 last-1 tables (`--model gpt2`) recover
that body leak on Distil 12, where Distil 12 in-domain last-1 was only
**16/48**: Distil 100 → Distil 12 is **12/12**, isolated **40/48**,
AUC **0.944**, unmarked $\le 0$ **48/48**; tail 64:128 **11/12**,
**40/48**, **0.931** (equals full-file). Distil 100 → GPT-2 12 is
**10/12**, **40/48**, **0.898**, unmarked **48/48**; tail **10/12**,
**40/48** (equals full-file). Last-4 Distil 100 → Distil 12 is
**9/12**, **20/48**; Distil 100 → GPT-2 12 ranks **11/12** with
isolated only **16/48** and **7** ranking-only. Distil 12 in-domain
last-1 **16/48** understated the body leak that Distil 100 last-1
tables recover. Reverse Distil 100 → GPT-2 100 (`--overlap keep`) is
**98/100**, **348/400**, AUC **0.976**, unmarked **400/400**; tail
**96/100**, **340/400**, **0.953**. Opening 0:4 is **99/100**,
**384/400** with unmarked only **313/400** (FPs). GPT-2 100 → Distil
100 last-1 was only **68/100** / **244/400**: Distil tables on GPT-2
files outrank GPT-2 tables on Distil files (Distil degenerate loops).
Last-4 Distil 100 → GPT-2 100 is **96/100**, **252/400**, **33**
ranking-only. Last-1 `hits` Distil 100 → Distil 12 is **12/12**,
isolated **36/48**, AUC **0.998**, unmarked **48/48**; tail
**12/12**, **36/48** (equals full-file). Distil 100 → GPT-2 12 last-1
hits is the same **12/12**, **36/48**, tail **12/12**, **36/48**.
Hard last-1 remains the isolated transfer on those 12s (**40/48**).
Last-4 hits Distil 100 → Distil 12 is opening overlap:
**12/12**, **48/48**, unmarked only **43/48** (FPs); tail **4/12**,
AUC **0.625**. Distil 100 last-1 hits → GPT-2 100 is **99/100**,
**356/400**, AUC **0.991**, unmarked **400/400**; opening 0:4 is
**100/100**, **400/400** with unmarked only **341/400** (FPs); tail
**99/100**, **320/400**, unmarked **400/400**. Last-1 `hashpool`
Distil 100 → Distil 12 matches hits isolated **36/48**, tail
**11/12**, **36/48** (equals full-file). Distil 100 last-1 hashpool →
GPT-2 12 ranks **12/12** with isolated only **24/48** (file-level
binom $p\approx 0.56$), **6** ranking-only; tail isolated **20/48**.
Hard last-1 remains the isolated transfer onto GPT-2 12 (**40/48**).
Distil 100 last-1 hashpool → GPT-2 100 is **99/100**, **316/400**, AUC
**0.992**, unmarked **400/400**, **20** ranking-only; opening 0:4
**100/100**, **388/400** with unmarked only **357/400** (FPs); tail
**98/100**, **304/400**. Below hard last-1 transfer **348/400** and
hits **356/400**. GPT-2 100 last-1 hashpool → Distil 100 is
**97/100**, **236/400**, AUC **0.964**, unmarked **398/400**, **38**
ranking-only; tail **94/100**, **232/400** (equals full-file). That
matches last-1 hits transfer ranking **97/100** / isolated
**240/400**. Do not sell Distil
100 → Distil 12 **40/48**, hits **36/48**, last-4 hits **48/48**,
hashpool ranking **12/12**, Distil 100 → GPT-2 100 **348/400** / hits **356/400** / hashpool **316/400**, GPT-2 100 → Distil 100 hashpool **236/400**, or
**98/100**.

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
`experiments/2026-09-03-pair-distil-100x4-kgw/`. Aaronson–Kirchner
twins: `experiments/2026-09-04-pair-12x4-aaronson/` and
`experiments/2026-09-04-pair-100x4-aaronson/` (opened freeze is last-4;
last-1 is post-open). DistilGPT2 Aaronson 100×4:
`experiments/2026-09-04-pair-distil-100x4-aaronson/` (opened freeze is
last-4; last-1 is post-open). Distil 100 last-1 used
the GPT-2 tokenizer id on Distil text (same BPE). Last-1 was not the
preregistered PROTOCOL-next-kgw reader (that freeze is last-4). This
is a post-open width match. Distil 100 has newline-loop files that the
keyed z-test also flags; last-1 unigrams on those loops are not a
reason to sell **350/400** or Distil 100 hits last-1 **355/400**. Mixin-negative
$\Hw=12$ tests: `experiments/2026-09-03-pair-100x4-ngram13/`,
`experiments/2026-09-03-pair-12x4-ngram13/`,
`experiments/2026-09-04-pair-distil-100x4-ngram13/`,
`experiments/2026-09-04-pair-distil-12x4-ngram13/`,
`experiments/2026-09-04-pair-qwen-12x4-ngram13/`. Distil Aaronson 100 last-1 unigrams on Distil degenerate loops are not a reason to sell **372/400**. DistilGPT2 Aaronson 12×4:
`experiments/2026-09-04-pair-distil-12x4-aaronson/` (opened freeze is
last-4). Qwen2-1.5B Aaronson 12×4 is the opened freeze
[research/PROTOCOL-next-aaronson-qwen.md](research/PROTOCOL-next-aaronson-qwen.md)
(`experiments/2026-09-04-pair-qwen-12x4-aaronson/`, seed **20260905**):
interpolate last-4 **12/12**, isolated **12/48**; hard last-4
**12/12**, **24/48**, unmarked $\le 0$ **48/48**. That hard isolated
count matches GPT-2 Aaronson last-4 **24/48**. Last-1 hard
(post-open, `--skip-nested`, `--model Qwen/Qwen2-1.5B-Instruct`):
**12/12**, **44/48**, AUC **0.995**, unmarked **46/48**. Both windows
rank: 0:4 **12/12**, isolated **48/48** with unmarked $\le 0$ only
**27/48** (FPs); 64:128 **12/12**, **48/48**, unmarked **45/48**.
Full-file **44/48** is the file mean, not the opening 48/48 with FPs.
Last-1 `hits` is **12/12**, **48/48**, AUC **1.000**, unmarked
**48/48**; tail 64:128 is the same **48/48**; last-4 hits is opening
overlap (**10/12**, **32/48**; tail **0/12**, **0/48**, all zeros).
Last-1 hashpool **12/12**, **44/48**, **1.000**, unmarked **48/48**;
tail **12/12**, **44/48**. Last-4 `rankpath` (`--rankpath-pos-bucket 0`)
is **10/12**, isolated **16/48**, AUC **0.780**, six ranking wins with
no isolated TP; tail ranks **12/12** with isolated only **20/48**.
Count last-1, not rankpath, is the Qwen Aaronson body reader. Last-1
`rankpath` lifts isolated versus last-4 (**12/12**, **28/48**, AUC
**0.899**, unmarked $\le 0$ **44/48**, **5** ranking wins with no
isolated TP) but stays below last-1 hard **44/48** and last-1 hits
**48/48**. Windows: 0:4 **9/12**, **28/48**, **0.686**; 64:128
**11/12**, **28/48**, **0.849**. Last-1 width does not turn Qwen
rankpath into the GPT-2 Aaronson last-4 rankpath body reader
(**44/48**). Do not sell rankpath last-1 **28/48**. Last-2
hard is **12/12**, **36/48**, AUC **0.946**, unmarked **48/48** — above
last-4 **24/48**, below last-1 **44/48**. Occupancy-free `postokhits`
last-4 is **8/12**, **32/48** (opening; tail **0/48**, 16 marked zeros),
matching last-4 hits; last-1 `postokhits` is empty (**0/48**, all
zeros), same as GPT-2 and Distil Aaronson. Occupancy-free `hashtok`
last-4 (no `--skip-hashpool`; `--fit-prefix 4`) is **11/12**,
**44/48**, AUC **0.966**, unmarked $\le 0$ **47/48**, 4 marked zeros;
0:4 **11/12**, **44/48**; tail **0/12**, **0/48**. Opening overlap,
stronger isolated than `postokhits` last-4 **32/48**, not a body
reader. Last-1 hits **48/48** remains the isolated body reader. Do not
sell hashtok **44/48** as body. Occupancy-free `hashtok` last-1 is
empty (**0/48**, all zeros), same as GPT-2 and Distil Aaronson.
Interpolate last-1 isolated
is **24/48** (last-4 interpolate **12/48**); tail ranks **12/12** with
isolated only **20/48**. Last-1 hits **48/48** remains the isolated
reader. Do not
sell **44/48**, **48/48**, last-2 **36/48**, interpolate last-1
**24/48**, hashtok last-4 **44/48**, or rankpath **16/48** / last-1
rankpath **28/48**. Last-1
on those twins is a post-open width match, not the freeze.

**Hypothesis.** When the watermark hash is last-1, last-4 count
tables smear that one-token seed across unused context tokens.
Matching reader width to hash width recovers isolated sign without
keys on both last-1 mixins (Kirchenbauer green list and
Aaronson–Kirchner exponential-minimum). A context-free unigram still
ranks Kirchenbauer because green tokens are over-used in aggregate;
last-1 `hard` / `hashpool` are the tighter match. Aaronson unigram
does **not** repeat that bag-of-tokens leak (isolated **24/48**, same
as last-4 hard). Kirchenbauer interpolate last-4 was already saturated
at 100 families (**100/100** / **376/400**); last-1 is the hard-reader
lift, and hashpool last-1 is the same width on the hash-pool spec.
Hits last-1 is the same width on the overlap spec. Aaronson last-1 is not Kirchenbauer’s tail-only geography: both 0:4
and 64:128 rank, including last-1 `hits` (tail **11/12**, **40/48**;
last-4 hits tail was **0/48**). Aaronson last-2 at n=100 matches last-1 isolated
**388/400** with unmarked $\le 0$ only **301/400**; last-1 keeps
specificity (**399/400**). Existing `rankpath` on Aaronson 12 already
sees the leak at last-4 (**44/48**, AUC **1.000**); last-1 width is
the count-table story. Rankpath tail 64:128 matches the full-file
**44/48**; opening 0:4 is **32/48**. DistilGPT2 Aaronson last-1 still
lifts `hard` (**8/48** → **16/48**). At n=100 that lift is
**308/400** → **372/400** because last-4 dilutes an already-saturated
opening (**364/400**) in the file mean; tail isolated stays
**240/400**, not GPT-2 Aaronson **380/400**. Last-1 `hits` **hurts** the
full-file count on Distil 12 (**44/48** → **32/48**) because last-4 was opening
copies, but last-1 hits tail **32/48** is above last-4 hits tail
**0/48**. Distil 100 last-1 hits recovers tail ranking
(**56/100** → **96/100**) while isolated stays opening-heavy
(**380/400** sits with 0:4 **360/400**). Hashpool (**32/48** → **20/48**) and occupancy-free
`postokhits` (**40/48** → **0/48**) still drop. Distil last-4
hits is opening overlap (tail **0/48**); Distil 12 rankpath is the body
reader (tail **44/48**). Distil 100 rankpath last-4 still **ranks** the
tail (**97/100**, AUC **0.958**) but isolated **372/400** sits with
opening **344/400**, not tail **280/400** (27 ranking-only). Distil 12
rankpath **44/48** overstated n=100 isolated geography. GPT-2 100 Aaronson last-1 tables
still transfer onto those Distil files as a body leak (tail
**40/48**, unmarked **48/48**; last-4 hard transfer **16/48**); last-4
hits transfer is opening **44/48**. GPT-2 100 Aaronson last-1 → Distil 100
is the same body ranking (tail **92/100**, isolated **244/400** equals
the tail; last-4 isolated **188/400** is chance). Distil 100 last-1 →
Distil 12 recovers the body leak in-domain last-1 missed
(**40/48**, tail equals full-file, versus **16/48**). Distil 100 →
GPT-2 12 is **40/48**; Distil 100 → GPT-2 100 is **348/400**. GPT-2 100 → GPT-2 12 last-1 hard
is the same isolated body transfer (tail **40/48** equals full-file;
opening **24/48**). Last-1 hits 100 → 12 ranks **12/12** with isolated
**36/48**. Last-4 hits 100 → 12 is opening **24/48** (tail AUC
**0.582**, isolated chance).

**Non-claim.** Do not sell **43/48**, **46/48**, **37/48**,
**48/48**, **47/48**, **389/400**, **350/400**, **329/400**,
**394/400**, **304/400**, **325/400**, **149/400**, KGW hits last-1
**46/48** / **395/400**, KGW hits last-1 tail **379/400**, Qwen hits last-1 **41/48** / tail
**38/48**, hashpool last-1 n=100 tail **377/400**, Aaronson last-1 hits
tail **40/48**, Distil last-1 hits tail **32/48**, Distil 100 hashpool
last-1 tail **182/400**, Distil 100 last-1 hard tail **202/400**,
hits last-1 transfer **48/48** / **44/48**, Distil 100 KGW → GPT-2 100
last-1 **338/400** / hits **343/400**, GPT-2 100 KGW → Distil 100
last-1 **247/400** / hits **253/400**, last-4 Distil → GPT-2 100
**53/400**, last-4 interpolate Distil → GPT-2 100 **331/400** /
GPT-2 → Distil **385/400**,
Aaronson last-1 100→12 **40/48** / hits **36/48** / last-4 **32/48**,
last-4 hits 100→12 **24/48**,
Aaronson hashpool last-1 n=100 opening **388/400** / tail **360/400**,
KGW interpolate last-1 n=100 opening **83/100** / tail **367/400**,
Distil interpolate last-1 n=100 tail **194/400**,
Qwen Aaronson last-1 hard **44/48** / hits **48/48**, Qwen Aaronson
rankpath **16/48** / last-1 rankpath **28/48**, Distil KGW hashtok last-4
**14/48**, Qwen KGW hashtok last-4 **2/12** / **14/48**, Qwen Aaronson hashtok last-4 **44/48**, Distil
Aaronson hashtok last-4 **44/48**, Distil Aaronson 100 hashtok last-4
**352/400**, Aaronson hits
last-4 **44/48** / n=100 **388/400**, Aaronson last-1
**40/48**, **388/400**, **99/100**, Aaronson last-2 n=100 **388/400** /
unmarked **301/400**, Aaronson hashpool last-1 n=100 **372/400**, Aaronson last-1 hits n=100
tail **372/400**, last-4 hits n=100 tail **260/400**, Distil
Aaronson last-1 **16/48** / last-2 **24/48**, Distil Aaronson 100 last-1
hard **372/400** / hits **380/400** / interpolate last-4 tail
**128/400** / rankpath **372/400** / rankpath opening **344/400**, Distil hits last-4
**44/48**, Distil postokhits last-4 **40/48**, Distil hashpool last-4
**32/48**, Distil last-1 hits **32/48**, Distil last-1 postokhits
**0/48**, Aaronson rankpath
**44/48**, Aaronson rankuni **44/48**, Distil Aaronson rankpath **44/48**,
GPT-2 Aaronson 100 rankpath **396/400** / tail **392/400**,
GPT-2 100 Aaronson last-1 → Distil **40/48**, GPT-2 100 Aaronson last-1 → Distil 100
**244/400** / hits ranking **97/100**, Distil 100 Aaronson last-1 → Distil 12
**40/48** / GPT-2 12 **40/48** / GPT-2 100 **348/400**, Distil 100 last-1 hits → Distil 12
**36/48** / GPT-2 100 **356/400**, Distil 100 last-1 hashpool → GPT-2 12
**24/48**, Distil KGW rankpath
**20/48**, Distil KGW 100 rankpath **199/400**, GPT-2 KGW 100 rankpath
**248/400**, Qwen KGW rankpath **26/48**, Aaronson unigram **24/48**,
**308/400**, Aaronson interpolate last-1 **296/400** / opening
**380/400** / tail **284/400**, Aaronson interpolate last-4 opening
**380/400** / tail **208/400**, last-4 hard opening **388/400**, occupancy-free last-1
**33/48**, occupancy-free hashtok last-4 **13/48**, GPT-2 Aaronson 100
hashtok last-4 **384/400**, Qwen Aaronson
hashtok last-4 **44/48**, Qwen hashpool **39/48**, Distil hashpool **43/48**, Distil
hashpool transfer **44/48** / **40/48**, Distil last-4 hashpool
**95/100**, or **100/100** as replacing **25/48**. Do not add a method name. Do not
retune Kirchenbauer or Aaronson `context_width` after peeking. Do not run last-1,
unigram, or hashpool last-1 as the headline SynthID reader. Do not
switch Kirchenbauer hard to last-2 (12×4 collapse; 100×4 is strictly
below last-1). Kirchenbauer last-1 tables trained on 100 GPT-2
families do **not** classify public SynthID original-12 (isolated
**6/48**, AUC 0.542, three ranking wins with no isolated TP) or
Grok-register SynthID 12 (**6/12**, **8/48**, AUC 0.523, two ranking
wins with no isolated TP). Last-1 on same-generator public SynthID is
also chance: Distil 100 → Distil SynthID 12 **0/48**, AUC 0.410, perm
$p\approx 0.94$, five ranking-only; Distil 12 → Distil SynthID 12
(`--overlap keep`) **7/48**, 0.473; last-1 `hits` / `hashpool` on Distil
100 → Distil SynthID 12 are also **0/48** (AUC 0.398 / 0.383);
Qwen 12 → Qwen SynthID 12 **12/48**,
0.505; GPT-2 100 → SynthID 36 **7/144**, 0.422, perm $p\approx 0.99$;
last-1 `hits` on that 36-file arrow is **5/144**, 0.391.
Last-4 interpolate on the same arrows is
also chance: GPT-2 100 → public SynthID **0/48**, AUC 0.527, seven
ranking-only; Distil 100 → public SynthID **2/48**; GPT-2 100 → grok12
**5/48**; Distil 100 → grok12 **7/48**; same-stem GPT-2 12 KGW →
SynthID 12 (`--overlap keep`) **6/48**; GPT-2 100 → SynthID 36
**8/144**; Distil 100 KGW → Distil public SynthID 12 **1/48**;
same-stem Distil 12 KGW → Distil SynthID 12 **3/48**; Qwen 12 KGW →
Qwen SynthID 12 **15/48**, ranking **1/12**
(idea 1). Hashpool last-1 transfer to public SynthID
12 is **2/48**, AUC 0.501. Aaronson last-1 tables trained on 100
families do **not** classify Kirchenbauer 12 (**0/48**) or public
SynthID 12 (**0/48**, ten ranking wins with no isolated TP). Last-4
interpolate on those arrows is also isolated **0/48** (GPT-2 Aaronson
100 → KGW 12 ranks 7/12, AUC 0.507, seven ranking-only; → SynthID 12
ranks 8/12, AUC 0.600, perm $p\approx 0.065$, eight ranking-only;
Distil Aaronson 100 → Distil KGW 12 ranks 5/12, **0/48**, 0.476).
Reverse: Kirchenbauer tables do **not** classify Aaronson on GPT-2
(100 interpolate last-4 → Aaronson 12 isolated **12/48**, AUC 0.361,
perm $p\approx 0.95$; last-1 **8/48**, 0.332). Distil 100 KGW last-1 →
Distil Aaronson 12 ranks **8/12**, AUC **0.682**, perm $p\approx 0.001$
while isolated stays **20/48** (file-level binom $p\approx 0.90$,
unmarked $\le 0$ **46/48**, three ranking-only); interpolate last-4 is
AUC **0.646**, isolated **20/48**. Tail last-1 ranks **9/12** with the
same isolated **20/48**. Ranking without a majority isolated sign is
not a detector. Qwen 12 KGW → Qwen Aaronson interpolate is **20/48**,
AUC 0.609, perm $p\approx 0.39$. Do not sell Distil ranking **8/12**
or **20/48**. Confirmatory n=100 `--overlap keep` (same 100 one-liners)
kills that Distil ranking look: last-1 **54/100**, isolated
**180/400**, AUC **0.519**, perm $p\approx 0.63$; last-1 `hits`
**55/100**, **168/400**, 0.523, perm $p\approx 0.29$; interpolate last-4
**58/100**, **188/400**, 0.587, perm $p\approx 0.43$. GPT-2 100 last-1
is **45/100**, **112/400**, 0.434; interpolate last-4 **36/100**,
**76/400**, 0.410, perm $p=1$. Qwen 12 last-1 KGW → Qwen Aaronson is
**12/48**, AUC 0.411, perm $p\approx 0.99$. Do not sell Distil 12 ranking **8/12**,
**20/48**, n=100 **180/400**, or **168/400**. Aaronson
rankpath 12 → public SynthID 12 is also isolated **0/48**. Last-1
Kirchenbauer tables also miss $\Hw=12$ on isolated $\tau=0$
(`--skip-nested`; n=100 uses `--overlap keep`). GPT-2 100 → ngram-13
100 last-1 `hard` is **62/100**, isolated **49/400**, AUC **0.557**,
perm $p\approx 0.004$, **27** ranking-only; `hits` **59/100**,
**22/400**, 0.541. File-level binomial on isolated $\tau=0$ is $p=1$.
The small AUC shift is not a detector. Distil 100 → Distil ngram-13
100 is **42/100**, **20/400**, 0.479, perm $p\approx 0.998$; `hits`
**12/400**. Opening 0:4 Distil last-1 is **34/400** (not interpolate
last-4 opening **280/400**); do not leftover-target either. 12-file
tests: GPT-2 100 → ngram-13 12 **3/48** / hits **1/48**; Distil 100 →
Distil ngram-13 12 **3/48** / hits **0/48**; Qwen 12 → Qwen ngram-13
12 **14/48**, ranking **5/12**, 0.468. Matching hash width does not
rescue the last-4 interpolate miss (idea 1 **51/400** / **24/400**).
Aaronson last-1 tables onto the same $\Hw=12$ twins **rank without
isolated sign**. GPT-2 100 last-1 `hard` is **98/100**, isolated
**1/400**, AUC **0.844**, perm $p\approx 0.0005$, **97** ranking-only;
last-1 `hits` **97/100**, **0/400**, 0.811, **97** ranking-only.
Last-4 interpolate is **100/100**, **0/400**, AUC **0.890**, unmarked
$\le 0$ **400/400**, **100** ranking-only (mean marked $-3.59$ vs
unmarked $-7.65$). Distil 100 last-1 `hard` is **75/100**, **9/400**,
0.679, **74** ranking-only. Ranking without isolated $\tau=0$ is not a
detector. Unigram on the same GPT-2 Aaronson → $\Hw=12$ arrow is
weaker ranking (**73/100**, AUC **0.628**) with the same isolated
**0/400**, **73** ranking-only: the ranking look is not a bag-of-tokens
detector and still has no isolated TPs. Kirchenbauer unigram on that
arrow is chance (**54/100**, **97/400**, 0.514, perm $p\approx 0.27$).
Do not leftover-target Aaronson last-4 hits opening
**204/400** (full-file isolated **145/400**) or KGW unigram opening
**256/400**. Last-4 `rankpath` on GPT-2 Aaronson → $\Hw=12$ is chance
(**55/100**, **0/400**, 0.532); Kirchenbauer rankpath is **54/100**,
**153/400**, 0.516. Interpolate atoms on that GPT-2 Aaronson → $\Hw=12$
transfer (`used_keys=false`) mix seen and unseen (21415 vs 32087);
full-file marked $\mathrm{lr}>0$ stays **0**; window means sit with the
scores (0:4 marked $\Delta$ $-2.92$ vs unmarked $-6.75$; tail $-3.58$
vs $-7.65$). Top GPT-2 marked $\Delta>0$ atoms are dialogue punctuation
(n=8 `," he said.`). Do not leftover-target those. Same-stem Qwen 12
Aaronson → Qwen $\Hw=12$ last-1 `hard` ranks **12/12** with isolated
**1/48**, AUC **0.849**; interpolate last-4 ranks **12/12** with
**0/48**, **0.914**. Distil 100 interpolate last-4 is **88/100**,
isolated **9/400**, 0.753, **87** ranking-only. Do not sell those
12-file ranking counts. Do not sell ranking
**98/100**, **100/100**, hashpool **99/100**, unigram **73/100**, Qwen
**12/12**, Distil **88/100**, or AUC **0.890**. Hashed logistic last-1 (`learn --archs
hashlog`, full file, not `--fit-prefix 1` which is empty) on GPT-2
Aaronson → $\Hw=12$ is **61/100**, isolated **56/400**, AUC **0.557**:
it does not become interpolate's **100/100** ranking-without-TP look.
Isolated is chance (binom $p=1$). Kirchenbauer hashlog on $\Hw=12$ is
chance (**49/100**, **170/400**, 0.488). Aaronson hashlog → public
SynthID 12 is **8/48**, 0.483. Last-1 `hashpool` (existing hashed
context pool; no `--skip-hashpool`) **does** sit with the count-table
look: GPT-2 100 Aaronson → $\Hw=12$ is **99/100**, isolated **0/400**,
AUC **0.870**, perm $p\approx 0.0005$, **99** ranking-only (mean marked
$-1.12$ vs unmarked $-1.53$). Distil 100 last-1 hashpool is
**71/100**, **9/400**, 0.709, **70** ranking-only (same isolated as
Distil last-1 `hard` **9/400**). Same-stem Qwen 12 last-1 hashpool
ranks **12/12** with isolated **0/48**, AUC **0.891**; n=12 ranking
without isolated $\tau=0$ is not a detector. Kirchenbauer last-1
hashpool on $\Hw=12$ is chance (GPT-2 100 **57/100**, **19/400**,
0.537, perm $p\approx 0.025$; Distil 100 **47/100**, **12/400**, 0.485,
perm $p=1$). Do not leftover-target Aaronson hashpool opening
**33/400**, KGW hashpool opening **120/400**, or Qwen hashpool opening
**14/48**. Distil Aaronson last-4 `rankpath` → Distil $\Hw=12$ is
anti-correlated (**31/100**, **12/400**, 0.397, perm $p=1$). Qwen 12
Aaronson rankpath ranks **10/12** with isolated **0/48**, AUC 0.622;
GPT-2 n=100 rankpath was already chance **55/100**. Ranking-without-TP
onto $\Hw=12$ is a count-table LR mean shift (`hard` / `hits` /
interpolate / `hashpool`; weaker UTF-8 `surface` **83/100**), not
rankpath and not hashed logistic / tokmlp / charcnn. Do
not sell hashpool ranking **99/100**, Distil **71/100**, Qwen
**12/12**, Qwen rankpath **10/12**, or surface **83/100**. Last-1 Aaronson hashpool
does **not** classify public SynthID: GPT-2 100 → original-12 is
chance (**6/12**, **0/48**, AUC 0.528, perm $p\approx 0.30$); Distil
100 → Distil SynthID 12 ranks **10/12** with isolated **0/48**, AUC
0.621, perm $p\approx 0.015$, **10** ranking-only (same isolated miss
as last-1 `hard`). Do not leftover-target GPT-2 hashpool→SynthID
opening **14/48** or Distil ranking **10/12**. Tiny token MLP
(`learn --archs tokmlp`, full file) on GPT-2 Aaronson → $\Hw=12$ is
chance (**48/100**, **122/400**, 0.514, perm $p\approx 0.15$): it does
not become interpolate's **100/100** ranking-without-TP look, same as
hashlog. UTF-8 `surface` (existing byte hashpool; default 8-byte
context) on the same GPT-2 Aaronson → $\Hw=12$ arrow ranks **83/100**
with isolated **0/400**, AUC **0.670**, **83** ranking-only (mean
marked $-1.30$ vs unmarked $-1.33$). That is weaker than interpolate
**100/100** / **0.890** and last-1 hashpool **99/100** / **0.870**,
and the windows are near chance (0:4 **53/100**; 64:128 **58/100**).
Kirchenbauer surface is weak (**56/100**, **92/400**, 0.550, perm
$p\approx 0.005$). Tiny UTF-8 CNN (`learn --archs charcnn`) is
anti-correlated (**33/100**, **17/400**, 0.407, perm $p=1$): it does
not become surface's ranking-without-TP look. Do not sell surface
ranking **83/100**. Distil 100 Aaronson surface → Distil $\Hw=12$ does
**not** replicate that look (**55/100**, **9/400**, 0.581, perm $p=1$;
mean marked more negative than unmarked). Token count tables still
rank on Distil (hashpool **71/100**; interpolate **88/100**). GPT-2
Aaronson surface → public SynthID 12 is chance (**5/12**, **0/48**,
0.466); Distil surface → Distil SynthID 12 ranks **9/12** with
isolated **0/48**, AUC 0.591, perm $p\approx 0.08$. Do not leftover-target KGW surface tail isolated
**190/400** or Distil surface opening **235/400**. The last-1 lift is
mixin-specific.

Same mixin, shared GPT-2 BPE, last-1 hard **does** transfer across
generators. Last-4 hard does not. Last-4 interpolate on the same
n=100 `--overlap keep` pairs **does** (idea 1): Distil → GPT-2
**331/400** versus last-4 hard **53/400**. Last-4 interpolate 100 →
original-12 (default `drop-from-train`, dropped=0) likewise: Distil 100
→ Distil 12 **42/48** versus hard **6/48**; Distil 100 → GPT-2 12
**43/48** versus **15/48**; GPT-2 100 → Distil 12 **46/48** versus
**22/48**; GPT-2 100 → GPT-2 12 **46/48** versus **32/48** (idea 1).
Last-4 **hard** transfer:

| Train → test | last-1 hard | last-4 hard |
|---|---|---|
| GPT-2 100 KGW → GPT-2 12 KGW | **12/12, 48/48, AUC 1.000** | 8/12, 32/48, 0.565 |
| GPT-2 100 KGW → Distil 12 KGW | **12/12, 47/48, AUC 0.991** | 5/12, 22/48, 0.488 |
| Distil 100 KGW → GPT-2 12 KGW | **12/12, 42/48, 0.987** | 11/12, 15/48, 0.685 |
| Distil 100 KGW → Distil 12 KGW | **12/12, 42/48, 0.982** | 7/12, 6/48, 0.519 |
| Distil 100 KGW → GPT-2 100 (`--overlap keep`) | **100/100, 338/400, 0.986** | 81/100, 53/400, 0.662 |
| GPT-2 100 KGW → Distil 100 (`--overlap keep`) | 99/100, 247/400, 0.921 | 78/100, 287/400, 0.670 |

`--skip-nested`; isolated is $\tau=0$. Unmarked $\le 0$ on GPT-2 12
hard last-1 is **43/48** (five FPs). Distil in-domain last-1 was
**46/48**; GPT-2 tables on Distil files are **47/48**. Distil last-4
→ GPT-2 12 ranks **11/12** with isolated only **15/48** (two ranking
wins with no isolated TP). Distil last-4 → Distil 12 is chance
isolated **6/48**. Distil 100 → GPT-2 100 last-1 is a **body** leak:
tail 64:128 **100/100**, **327/400**, AUC **0.948**, unmarked
**373/400**; opening 0:4 **85/100**, **218/400**, **0.714**. Full-file
**338/400** sits with the tail. Last-4 Distil → GPT-2 100 ranks
**81/100** with isolated only **53/400** and **45** ranking-only; tail
isolated **66/400**. GPT-2 100 → Distil 100 last-1 ranks **99/100**
with isolated **247/400**, **10** ranking-only; tail **94/100**,
**230/400**, **0.887** (equals full-file isolated). Distil in-domain
last-1 **350/400** is stronger: Distil tables on GPT-2 files outrank
GPT-2 tables on Distil files (newline-loop files), same as Aaronson
Distil 100 ↔ GPT-2 100. Last-4 GPT-2 → Distil 100 isolated
**287/400** has unmarked $\le 0$ only **222/400** (FPs). Last-1 is the
isolated transfer; last-4 ranking can
look fine while files do not sign. Same last-1 `hashpool` tables:
GPT-2 100 → GPT-2 12 **12/12, 48/48**, AUC **0.998**, unmarked $\le 0$
**40/48** (eight FPs); GPT-2 100 → Distil 12 **12/12, 47/48**, 0.994.
Distil 100 hashpool last-1 → GPT-2 12 is **12/12, 44/48**, AUC
**0.994**, unmarked $\le 0$ **47/48**; Distil 100 → Distil 12 is
**12/12, 40/48**, 0.991, unmarked $\le 0$ **47/48**.
Do not sell **48/48**, **47/48**, **44/48**, **40/48**, **338/400**,
**247/400**, last-4 interpolate **331/400**, GPT-2 → Distil
interpolate **385/400**, last-4 interpolate 100 → original-12
**46/48** / **43/48** / **42/48**, last-1 Distil 100 → Distil SynthID
**0/48** (`hard` / `hits` / `hashpool`), last-1 GPT-2 100 → SynthID 36
**7/144**, Distil KGW last-1 → Distil Aaronson **20/48** / ranking
**8/12** or n=100 **180/400**, last-1 KGW → $\Hw=12$ **49/400** /
Distil **20/400** / 12-file **3/48**, or Aaronson last-1 → $\Hw=12$
ranking **98/100** with isolated **1/400** (interpolate last-4
**100/100**, **0/400**, AUC **0.890**; last-1 hashpool **99/100**,
**0/400**, 0.870). Qwen uses a
different tokenizer; this transfer is same-BPE only.

Same last-1 on Aaronson–Kirchner (Distil 100 → 12 uses default
`drop-from-train`, dropped=0; Distil 100 ↔ GPT-2 100 uses `--overlap
keep`):

| Train → test | last-1 hard | last-4 hard |
|---|---|---|
| Distil 100 Aaronson → Distil 12 | **12/12, 40/48, 0.944** | 9/12, 20/48, 0.804 |
| Distil 100 Aaronson → GPT-2 12 | **10/12, 40/48, 0.898** | 11/12, 16/48, 0.908 |
| Distil 100 Aaronson → GPT-2 100 | **98/100, 348/400, 0.976** | 96/100, 252/400, 0.946 |
| GPT-2 100 Aaronson → Distil 100 | 68/100, 244/400, 0.698 | 69/100, 188/400, 0.683 |

GPT-2 100 → Distil 12 last-1 remains **11/12, 40/48**. Distil 12
in-domain last-1 **16/48** is not the Distil 100 → Distil 12 transfer.
Last-4 Distil 100 → GPT-2 12 ranks **11/12** with isolated only
**16/48**. Last-1 is the isolated transfer here too. Do not sell
**40/48** or **348/400**.

Same last-1 `hits` tables transfer like `hard` last-1:

| Train → test | last-1 hits |
|---|---|
| GPT-2 100 KGW → GPT-2 12 KGW | **12/12, 48/48, AUC 1.000** |
| GPT-2 100 KGW → Distil 12 KGW | **12/12, 47/48, 0.993** |
| Distil 100 KGW → GPT-2 12 KGW | **12/12, 46/48, 0.995** |
| Distil 100 KGW → Distil 12 KGW | **12/12, 44/48, 0.992** |
| Distil 100 KGW → GPT-2 100 | **100/100, 343/400, 0.996** |
| GPT-2 100 KGW → Distil 100 | 99/100, 253/400, 0.945 |

`--skip-nested`. Unmarked $\le 0$ is **43/48**, **43/48**, **45/48**,
**46/48**. Distil 100 → Distil 12 hits last-1 **44/48** is above that
pair’s hard last-1 **42/48**. Distil 100 → GPT-2 100 last-1 hits is
**100/100**, **343/400**, AUC **0.996**, unmarked **399/400**; tail
**100/100**, **320/400**, **0.976**. GPT-2 100 → Distil 100 last-1
hits is **99/100**, **253/400**, **0.945**, **9** ranking-only; tail
**96/100**, **242/400**, **0.921**. Do not sell **48/48**, **44/48**,
**343/400**, or **253/400**.

Same mixin, shared GPT-2 BPE, Aaronson last-1 **does** transfer
100 GPT-2 families onto DistilGPT2 original-12 files. Last-4 ranks
the prompt groups while files mostly do not sign:

| Train → test | last-1 hard | last-4 hard |
|---|---|---|
| GPT-2 100 Aaronson → GPT-2 12 Aaronson | **11/12, 40/48, AUC 0.936** | **10/12, 32/48, 0.885** |
| GPT-2 100 Aaronson → Distil 12 Aaronson | **11/12, 40/48, AUC 0.915** | **12/12, 16/48, 0.932** |
| GPT-2 12 Aaronson → Distil 12 (`--overlap keep`) | 10/12, 24/48, 0.825 | — |

`--skip-nested`; isolated is $\tau=0$. Unmarked $\le 0$ on 100 →
GPT-2 12 last-1 and last-4, and on 100 → Distil last-1, is **48/48**
(precision **1.000**). 100 → GPT-2 12 last-1 tail 64:128 is **40/48**
(equals full-file); opening 0:4 is only **24/48**. Last-4 100 → GPT-2
12 is a **weaker body** leak: tail 64:128 **10/12**, **32/48**, AUC
**0.877**, unmarked **48/48** (equals full-file **32/48**); opening
**24/48**. Last-1 `hits` 100 → GPT-2 12 ranks **12/12** with isolated
**36/48**; tail **40/48**. Last-4 `hits` 100 → GPT-2 12 is **opening
overlap**, not that body transfer: **8/12**, isolated **24/48**, AUC
**0.708**, unmarked $\le 0$ **45/48**, **2** ranking wins with no
isolated TP (night-bus, garden); 0:4 is the same **24/48**; tail
64:128 **6/12**, **12/48**, AUC **0.582**. Isolated **24/48** is
chance at $\tau=0$. Distil last-4 transfer
ranks **12/12** with **8** ranking wins with no isolated TP. Same
pattern as Kirchenbauer GPT-2 ↔ Distil: last-1 is the isolated
transfer. Same-stem n=12 last-1 is thinner (**24/48**). Do not sell
Aaronson transfer **40/48**, last-4 in-family **32/48**, hits transfer
**36/48**, last-4 hits transfer **24/48**, or Distil last-4 **16/48**.

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hard,interpolate --context-len 1 --skip-hashpool \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-last1

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods hard,interpolate --context-len 1 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-last1

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods interpolate --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-interp-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --model gpt2 --methods interpolate --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-kgw-interp-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-12x4-kgw \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/xfer-kgw100-last1-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-distil-12x4-kgw \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/xfer-kgw100-last1-to-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --model gpt2 --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-kgw-last1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-kgw --overlap keep --model gpt2 \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-kgw100-last1-to-gpt2100

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-kgw --overlap keep --model gpt2 \
  --methods hard --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-kgw100-last4-to-gpt2100

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-kgw --overlap keep --model gpt2 \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-kgw100-hits-k1-to-gpt2100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-distil-100x4-kgw --overlap keep --model gpt2 \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2-kgw100-last1-to-distil100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-distil-100x4-kgw --overlap keep --model gpt2 \
  --methods hard --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2-kgw100-last4-to-distil100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-distil-100x4-kgw --overlap keep --model gpt2 \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2-kgw100-hits-k1-to-distil100

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 --model gpt2 \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-last1-to-synthid-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-12x4-kgw \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 --overlap keep --model gpt2 \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil12-kgw-last1-to-synthid-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --test-dir experiments/2026-08-31-pair-qwen-12x4 --overlap keep \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-qwen12-kgw-last1-to-synthid-qwen12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-last1-to-synthid36

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-12x4-kgw \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-interp-k4-to-kgw12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-distil-12x4-kgw --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-interp-k4-to-distil-kgw12

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-interp-k4-to-synthid12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-aaronson12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-12x4-aaronson --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-distil-aaronson12

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson --overlap keep \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt212-kgw-interp-k4-to-aaronson12

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --test-dir experiments/2026-09-04-pair-qwen-12x4-aaronson --overlap keep \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-qwen12-kgw-interp-k4-to-qwen-aaronson12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-last1-to-aaronson12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-12x4-aaronson --model gpt2 \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-last1-to-distil-aaronson12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-100x4-aaronson --overlap keep --model gpt2 \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-last1-to-distil-aaronson100

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-100x4-aaronson --overlap keep --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-interp-k4-to-distil-aaronson100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-100x4-aaronson --overlap keep \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-last1-to-aaronson100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-100x4-aaronson --overlap keep \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-interp-k4-to-aaronson100

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-100x4-aaronson --overlap keep --model gpt2 \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-hits-k1-to-distil-aaronson100

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --test-dir experiments/2026-09-04-pair-qwen-12x4-aaronson --overlap keep \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-qwen12-kgw-last1-to-qwen-aaronson12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods hard,hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-last1-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-100x4-ngram13 --overlap keep --model gpt2 \
  --methods hard,hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-last1-to-distil-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-12x4-ngram13 \
  --methods hard,hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-last1-to-ngram13-12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-12x4-ngram13 --model gpt2 \
  --methods hard,hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-last1-to-distil-ngram13-12

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --test-dir experiments/2026-09-04-pair-qwen-12x4-ngram13 --overlap keep \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hard,hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-qwen12-kgw-last1-to-qwen-ngram13-12

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-aaronson-last1-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-ngram13 --overlap keep --model gpt2 \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-aaronson-last1-to-distil-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods interpolate,hits --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-aaronson-interp-k4-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-aaronson-hits-k1-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods unigram --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-aaronson-unigram-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods unigram --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-unigram-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-aaronson-rankpath-k4-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-rankpath-k4-to-ngram13-100

python -m text_watermark_tools atoms \
  /tmp/kgw-lab/xfer-gpt2100-aaronson-interp-k4-to-ngram13-100/tables-counts \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/atoms-aaronson100-interp-k4-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --test-dir experiments/2026-09-04-pair-qwen-12x4-ngram13 --overlap keep \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-qwen12-aaronson-last1-to-qwen-ngram13-12

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --test-dir experiments/2026-09-04-pair-qwen-12x4-ngram13 --overlap keep \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-qwen12-aaronson-interp-k4-to-qwen-ngram13-12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-ngram13 --overlap keep --model gpt2 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-aaronson-interp-k4-to-distil-ngram13-100

python -m text_watermark_tools learn experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --archs hashlog --context-len 1 --pos-bucket 1 --skip-nested \
  --out-dir /tmp/kgw-lab/learn-gpt2100-aaronson-hashlog-k1-full-to-ngram13-100

python -m text_watermark_tools learn experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --archs hashlog --context-len 1 --pos-bucket 1 --skip-nested \
  --out-dir /tmp/kgw-lab/learn-gpt2100-kgw-hashlog-k1-full-to-ngram13-100

python -m text_watermark_tools learn experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --archs hashlog --context-len 1 --pos-bucket 1 --skip-nested \
  --out-dir /tmp/kgw-lab/learn-gpt2100-aaronson-hashlog-k1-to-synthid12

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-aaronson-hashpool-k1-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-hashpool-k1-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-ngram13 --overlap keep --model gpt2 \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-aaronson-hashpool-k1-to-distil-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-09-04-pair-distil-100x4-ngram13 --overlap keep --model gpt2 \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-hashpool-k1-to-distil-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-ngram13 --overlap keep --model gpt2 \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-aaronson-rankpath-k4-to-distil-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --test-dir experiments/2026-09-04-pair-qwen-12x4-ngram13 --overlap keep \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-qwen12-aaronson-rankpath-k4-to-qwen-ngram13-12

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --test-dir experiments/2026-09-04-pair-qwen-12x4-ngram13 --overlap keep \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-qwen12-aaronson-hashpool-k1-to-qwen-ngram13-12

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-aaronson-hashpool-k1-to-synthid12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 --model gpt2 \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-aaronson-hashpool-k1-to-synthid-distil12

python -m text_watermark_tools learn experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --archs tokmlp --context-len 1 --pos-bucket 1 --skip-nested \
  --out-dir /tmp/kgw-lab/learn-gpt2100-aaronson-tokmlp-k1-full-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods surface --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-aaronson-surface-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --methods surface --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-surface-to-ngram13-100

python -m text_watermark_tools learn experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 --overlap keep \
  --archs charcnn --context-len 1 --pos-bucket 1 --skip-nested \
  --out-dir /tmp/kgw-lab/learn-gpt2100-aaronson-charcnn-k1-full-to-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-ngram13 --overlap keep --model gpt2 \
  --methods surface --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-aaronson-surface-to-distil-ngram13-100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods surface --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-aaronson-surface-to-synthid12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 --model gpt2 \
  --methods surface --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-aaronson-surface-to-synthid-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-ngram13-snaprate

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods snapleave,snapupset --snaprate --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-ngram13-snaprate

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 --model gpt2 \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-hits-k1-to-synthid-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 --model gpt2 \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil100-kgw-hashpool-k1-to-synthid-distil12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-gpt2100-kgw-hits-k1-to-synthid36

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hashpool --context-len 1 \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-hashpool-k1

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hashtok --context-len 4 --fit-prefix 4 --skip-nested \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-hashtok-k4-ok

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hashtok --context-len 1 --fit-prefix 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-hashtok-k1-ok

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods hashpool --context-len 1 --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-hashpool-k1

python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --methods hard,interpolate --context-len 1 --skip-hashpool \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-aaronson-last1

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-last1

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hard --context-len 2 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-k2

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hashpool --context-len 1 --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-hashpool-k1

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hits --context-len 1 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-hits-k1

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-kgw-hits-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-hits-k1

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-hits-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct --methods hits --context-len 1 \
  --skip-hashpool --out-dir /tmp/kgw-lab/probe-qwen-12x4-kgw-hits-k1

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct --methods hits --context-len 1 \
  --skip-hashpool --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-12x4-kgw-hits-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct --methods hashpool --context-len 1 \
  --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-12x4-kgw-hashpool-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-12x4-kgw \
  --model gpt2 --methods hits --context-len 1 --skip-hashpool \
  --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-kgw-hits-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-12x4-kgw \
  --model gpt2 --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-kgw-hashpool-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-kgw-hashpool-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --methods hits --context-len 4 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-12x4-aaronson-hits-k4

python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --out-dir /tmp/kgw-lab/probe-12x4-aaronson-rankpath-k4

python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-aaronson-rankpath-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --test-dir experiments/2026-08-17-pair-12x4 --overlap keep \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested \
  --out-dir /tmp/kgw-lab/xfer-aaronson12-rankpath-to-synthid12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods hits --context-len 4 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-distil-aaronson-hits-k4

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --fit-prefix 4 --pos-bucket 1 --methods postokhits --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-distil-aaronson-postokhits-k4

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-last1-to-distil12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-aaronson-rankpath-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods hits --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-aaronson-hits-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --methods hits --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-aaronson-hits-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-aaronson-hits-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-aaronson-hashpool-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-aaronson-hits-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-100x4-kgw \
  --model gpt2 --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-kgw-hashpool-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-12x4-kgw \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/xfer-kgw100-hits-k1-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --test-dir experiments/2026-09-03-pair-distil-12x4-kgw \
  --model gpt2 --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/xfer-kgw100-hits-k1-to-distil12

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --model Qwen/Qwen2-1.5B-Instruct --methods hard --context-len 1 \
  --skip-hashpool --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-aaronson-hard-k1

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --model Qwen/Qwen2-1.5B-Instruct --methods hits --context-len 1 \
  --skip-hashpool --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-aaronson-hits-k1

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --model Qwen/Qwen2-1.5B-Instruct --methods rankpath --context-len 4 \
  --skip-hashpool --rankpath --rankpath-pos-bucket 0 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-aaronson-rankpath-k4

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-hits-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hits --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-hits-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods interpolate --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-interp-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-interp-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hard --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-hard-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-hard-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods hard --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-hard-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-hits-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods hits --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-hits-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-interp-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods interpolate --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-interp-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-hashpool-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods hashtok --context-len 1 --fit-prefix 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-hashtok-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods hashtok --context-len 4 --fit-prefix 4 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-hashtok-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --model gpt2 --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-aaronson-rankpath-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods rankpath --context-len 4 --skip-hashpool --rankpath \
  --rankpath-pos-bucket 0 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-rankpath-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hashtok --context-len 1 --fit-prefix 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-hashtok-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hashtok --context-len 4 --fit-prefix 4 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-hashtok-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-aaronson --overlap keep \
  --model gpt2 --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-last1-to-distil100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-aaronson --overlap keep \
  --model gpt2 --methods hard --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-last4-to-distil100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-aaronson --overlap keep \
  --model gpt2 --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-hits-k1-to-distil100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-aaronson --overlap keep \
  --model gpt2 --methods hits --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-hits-k4-to-distil100

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-last1-to-distil12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --model gpt2 --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-last1-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-100x4-aaronson --overlap keep \
  --model gpt2 --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-last1-to-gpt2100

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-hits-k1-to-distil12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --model gpt2 --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-hits-k1-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-100x4-aaronson --overlap keep \
  --model gpt2 --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-hits-k1-to-gpt2100

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-hashpool-k1-to-distil12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --model gpt2 --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-hashpool-k1-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-100x4-aaronson --overlap keep \
  --model gpt2 --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-distil-aaronson100-hashpool-k1-to-gpt2100

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-distil-100x4-aaronson --overlap keep \
  --model gpt2 --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-hashpool-k1-to-distil100

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --model Qwen/Qwen2-1.5B-Instruct --methods hashtok --context-len 4 \
  --fit-prefix 4 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-aaronson-hashtok-k4

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --model Qwen/Qwen2-1.5B-Instruct --methods hashtok --context-len 1 \
  --fit-prefix 1 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-aaronson-hashtok-k1

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods hashtok --context-len 4 --fit-prefix 4 \
  --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-aaronson-hashtok-k4

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-aaronson \
  --model gpt2 --methods hashtok --context-len 1 --fit-prefix 1 \
  --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-aaronson-hashtok-k1

python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-12x4-kgw \
  --model gpt2 --methods hashtok --context-len 4 --fit-prefix 4 \
  --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-kgw-hashtok-k4

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct --methods hashtok --context-len 4 \
  --fit-prefix 4 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-12x4-kgw-hashtok-k4

python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct --methods hashtok --context-len 1 \
  --fit-prefix 1 --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-12x4-kgw-hashtok-k1

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-aaronson \
  --model Qwen/Qwen2-1.5B-Instruct --methods rankpath --context-len 1 \
  --skip-hashpool --rankpath --rankpath-pos-bucket 0 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-qwen-aaronson-rankpath-k1

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --methods hard --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-last1-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --methods hits --context-len 1 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-hits-k1-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --methods hard --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-last4-to-gpt212

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hashpool --context-len 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-aaronson-hashpool-k1-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --methods hits --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/xfer-aaronson100-hits-k4-to-gpt212
```

**Why it is a backlog item.** Published Kirchenbauer hard last-4
understates the green-list leak: 100-family ranking **62/100** →
**100/100**, isolated **209/400** → **389/400**, AUC **0.573** →
**0.990**. Same `hard` scorer. Existing `hits` last-1 is the overlap
spec at the same width (100-family **395/400**, AUC **0.996** vs last-4
hits **254/400**, **0.812**); public SynthID hits last-1 is chance.
Existing `hashpool` last-1 is the same
width match (100-family **394/400**, AUC **0.995** vs last-4 hashpool
**304/400**, **0.867**); Qwen last-4 hashpool is chance. At n=100 the
hard widths are last-1 > last-2 > last-4. Last-1 tables transfer
GPT-2 ↔ Distil and GPT-2 100 → original-12 KGW (**48/48** vs last-4
**32/48**); Distil 100 → GPT-2 100 last-1 is **338/400** vs last-4
**53/400**; GPT-2 100 → Distil 100 last-1 is **247/400**. Last-4 tables
do not (Distil 100 last-4 → Distil 12 is isolated **6/48**). Last-1
KGW tables do not classify $\Hw=12$ (GPT-2 **49/400**, Distil
**20/400**, 12-file **3/48**); Aaronson last-1 ranks those twins
**98/100** with isolated **1/400** (interpolate last-4 **100/100**,
**0/400**). Ranking without isolated sign is not a detector. Unigram
on that Aaronson arrow is **73/100** with isolated **0/400**, below
last-1 hard. Last-4 `rankpath` on the same arrow is chance
(**55/100**, isolated **0/400**, AUC **0.532**, perm $p\approx 0.14$);
Kirchenbauer rankpath is also chance (**54/100**, **153/400**, 0.516).
The ranking-without-isolated-TP look is a count-table mean shift, not
unmarked-LM rankpath. Same-stem Qwen 12 Aaronson → Qwen $\Hw=12$
repeats the ranking look at n=12 (last-1 `hard` **12/12**, isolated
**1/48**, AUC **0.849**, **11** ranking-only; interpolate last-4
**12/12**, **0/48**, **0.914**). Distil 100 interpolate last-4 is
**88/100**, isolated **9/400**, AUC **0.753**, **87** ranking-only
(newline-loop files). Do not sell those 12-file ranking
counts; GPT-2 n=100 already killed isolated $\tau=0$. Opening last-1
**24/48** is not a detector. Do not leftover-target it. Hashed logistic
last-1 does not become that ranking look (**61/100**, **56/400**). The freeze in
[research/PROTOCOL-next-kgw.md](research/PROTOCOL-next-kgw.md) should
keep last-4 as the preregistered grain and treat last-1 as the
width-matched companion. Unigram is a weaker bag-of-tokens companion.
Hits last-1 and hashpool last-1 are the other existing-scorer
companions, not a fourth method name. Aaronson–Kirchner last-1 is the same width match on a
third mixin (`context_width=1`): isolated **24/48** → **40/48** at
n=12 and **344/400** → **388/400** at n=100, without selling those
counts. Aaronson interpolate last-1 at n=100 ranks both windows but
isolated **296/400** is opening-heavy (**380/400**) plus tail
ranking-without-TP (**284/400**); hard last-1 remains the body
isolated reader. Existing `rankpath` on Aaronson 12 is **44/48** at last-4
already, not a width match. GPT-2 100 rankpath last-4 isolated
**396/400** sits with the tail **392/400**; Distil 100 rankpath
isolated **372/400** sits with the opening. DistilGPT2 Aaronson 12 last-1 still lifts
`hard` vs last-4 (**16/48** vs **8/48**). Last-4 `hits` **44/48** is
opening overlap (Distil tail **0/48**; GPT-2 last-4 hits tail isolated
**0/48**); last-1 hits recovers that body (GPT-2 tail **11/12**,
**40/48**; Distil tail **10/12**, **32/48**) even when the full-file
count drops. Occupancy-free last-4
`postokhits` is **40/48**; last-1 is empty. GPT-2 100 last-1 tables
classify those Distil files at **40/48** (last-4 hard transfer isolated
**16/48** with eight ranking wins with no isolated TP); last-4 hits
transfer is **44/48**. Last-2 isolated
**24/48** wins at that n=12 and is not GPT-2 last-1 **40/48**. The freeze in
[research/PROTOCOL-next-aaronson.md](research/PROTOCOL-next-aaronson.md)
keeps last-4 as the preregistered grain.

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
| DistilGPT2 ngram-13 12×4 | 6/12, 16/48, 0.485 | 6/12, 25/48, 0.540 |
| DistilGPT2 ngram-13 100×4 | 89/100, 354/400, 0.829 | 88/100, 313/400, 0.799 |
| Qwen2-1.5B ngram-13 12×4 | 4/12, 16/48, 0.415 | 5/12, 19/48, 0.445 |

Matching `context_len` to $\Hw=12$ does **not** repeat the Kirchenbauer
last-1 jump. Original-12 ngram-13 hard width grid (k=4 is the freeze
dump; other k used `--skip-nested`):

| Width | 12×4 | 100×4 |
|---|---|---|
| last-2 | 8/12, 21/48, 0.481 | 63/100, 248/400, 0.592 |
| last-3 | 5/12, 21/48, 0.473 | — |
| last-4 | 6/12, 22/48, 0.544 | 66/100, 215/400, 0.579 |
| last-6 | 6/12, 24/48, 0.560 | — |
| last-8 | 6/12, 24/48, 0.551 | — |
| last-10 | 7/12, 24/48, 0.553 | — |
| last-12 | 7/12, 24/48, 0.553 | 71/100, 226/400, 0.620 |
| last-13 | 7/12, 24/48, 0.553 | — |

Last-6 is the half-window analog of last-2 on $\Hw=4$. Last-12 matches
$\Hw=12$. Neither rescues isolated sign. 100-family last-12 ranking
**71/100** is only +5 vs last-4; isolated **226/400** is below last-2
**248/400**. Do not sell **71/100**. GPT-2 ngram-13 100 last-2
windows (`--skip-nested`): 0:4 **87/100**, **301/400**, AUC
**0.795**; 64:128 **60/100**, **214/400**, **0.537**. Full-file
**63/100** sits below the opening. Tail AUC is chance. Last-2 at
$\Hw=12$ is opening mass, same geography as Distil $\Hw=12$ 100 last-2
and public $\Hw=4$ last-2 at n=100, not a Kirchenbauer body leak. Do
not sell opening **87/100** or **301/400**. GPT-2 ngram-13 100 last-12
windows (`--skip-nested`): 0:4 **82/100**, **293/400**, AUC
**0.763**; 64:128 **59/100**, **192/400**, **0.545**. Full-file
**71/100** sits below the opening. Tail AUC is chance. Matching
last-12 to $\Hw=12$ is still opening mass, not a body rescue. Do not
sell last-12 opening **82/100** or **293/400**. Occupancy-free
`hashtok` last-4 on these $\Hw=12$ twins is **opening overlap**, not a
body rescue: GPT-2 12 **11/12**, **23/48**, AUC **0.724** (0:4 equals
full-file; tail **0/12**; isolated chance, file-level binom
$p\approx 0.67$); GPT-2 100 **95/100**, **313/400**, **0.888**, **12**
ranking-only (0:4 equals full-file; tail **0/100**). Distil 12
**9/12**, **28/48**, **0.727**; Distil 100 **98/100**, **369/400**,
**0.943**; tail **0**. Last-1 `hashtok` is empty on both generators.
Do not sell **313/400** or **369/400**.

DistilGPT2 ngram-13 12×4 hard
width grid (`--model gpt2`, same BPE; k=4 is the freeze dump in
[research/PROTOCOL-next-longctx-distil.md](research/PROTOCOL-next-longctx-distil.md);
other k under `/tmp/kgw-lab/`):

| Width | Prompt | Isolated | unmarked $\le 0$ | AUC |
|---|---|---|---|---|
| last-1 | 7/12 | 23/48 | 32/48 | 0.595 |
| last-2 | 6/12 | 25/48 | 24/48 | 0.540 |
| last-4 freeze | 6/12 | 16/48 | 26/48 | 0.485 |
| last-6 | 8/12 | 17/48 | 27/48 | 0.500 |
| last-12 | 8/12 | 17/48 | 27/48 | 0.501 |

Distil last-2 isolated **25/48** is a different generator and $\Hw$ from
the locked public GPT-2 last-4 **25/48**. Ranking stays chance
(**6/12**); freeze interpolate last-4 on these twins is **9/12**,
**21/48**, 0.563. Last-12 matches $\Hw=12$ and does not rescue
(ranking **8/12**, isolated **17/48**). Do not sell Distil last-2
**25/48**. DistilGPT2 ngram-13 100×4 (opened freeze
[research/PROTOCOL-next-longctx-distil-100.md](research/PROTOCOL-next-longctx-distil-100.md);
last-4 dump `experiments/2026-09-04-probe-distil-100x4-ngram13-hard-last4/`)
interpolate last-4 is **88/100**, isolated **325/400**, AUC **0.785**
(**557/800**). Hard last-4 is **89/100**, **354/400**, **0.829**.
Post-open last-2 (`--skip-nested`) is **88/100**, **313/400**,
**0.799**, unmarked $\le 0$ **246/400** — last-2 does **not** beat
last-4 ranking or isolated. Absolute windows: 0:4 **92/100**,
**348/400**, AUC **0.876**; 64:128 **70/100**, **222/400**,
**0.580**. Opening mass, same geography as public $\Hw=4$ last-2 at
n=100, not a Kirchenbauer-style body. Do not sell Distil $\Hw=12$
last-4 **89/100**, interpolate **88/100**, last-2 **88/100**, isolated
**313/400**, or opening **348/400**. Matching last-12 to $\Hw=12$
(`--skip-nested`) is **87/100**, **350/400**, AUC **0.828**, unmarked
$\le 0$ **185/400** — below last-4 ranking **89/100**, isolated
**354/400**. Windows: 0:4 **92/100**, **348/400**, **0.880**; 64:128
**71/100**, **282/400**, **0.628**. Last-12 does not rescue. Do not
sell last-12 **87/100** or **350/400**. Interpolate last-4 windows
(`--skip-nested`): 0:4 **90/100**, **346/400**, AUC **0.894**; 64:128
**60/100**, **219/400**, **0.565**. Front-loaded, opposite of
Kirchenbauer interpolate last-4. Tail AUC is chance. Lengthening the
hash history to $\Hw=12$ does not make a Kirchenbauer-style body leak
on Distil. Do not sell interpolate opening **90/100** or tail
**60/100**. GPT-2 ngram-13 100 interpolate last-4 windows
(`--skip-nested`): 0:4 **86/100**, **327/400**, AUC **0.823**; 64:128
**50/100**, **184/400**, **0.501**. Tail ranking is chance. Full-file
interpolate **76/100** is opening mass. Lengthening $\Hw$ to 12 kills
the public $\Hw=4$ interpolate tail (**93/100**). Do not sell
interpolate **76/100**, opening **86/100**, or tail **50/100**.

Qwen2-1.5B ngram-13 12×4 hard width grid (`--model
Qwen/Qwen2-1.5B-Instruct`; k=4 is the freeze dump in
[research/PROTOCOL-next-longctx-qwen.md](research/PROTOCOL-next-longctx-qwen.md)):

| Width | Prompt | Isolated | unmarked $\le 0$ | AUC |
|---|---|---|---|---|
| last-1 | 5/12 | 22/48 | 28/48 | 0.505 |
| last-2 | 5/12 | 19/48 | 26/48 | 0.445 |
| last-4 freeze | 4/12 | 16/48 | 31/48 | 0.415 |
| last-6 | 4/12 | 14/48 | 30/48 | 0.410 |
| last-12 | 4/12 | 15/48 | 30/48 | 0.417 |

Qwen last-2 ranking stays chance (**5/12**). Freeze interpolate last-4
is **4/12**, **14/48**, 0.400. Last-12 does not rescue. Official
first-draw matching mean was **11/12** above $0.55$ (library $0.515$).
Do not sell Qwen last-2 **19/48** or last-1 **22/48**. Distil
interpolate last-2 is **9/12**, **20/48**, AUC
**0.553** versus freeze last-4 interpolate **9/12**, **21/48**,
**0.563**: ranking tied, isolated not better. Keep interpolate at
last-4. Hashpool last-2 on public
SynthID 12 **hurts** ranking versus published last-4 hashpool:
**10/12**, **31/48**, AUC **0.629** versus **11/12**, **35/48**,
**0.716**. Hits last-2 already hurt; hashpool last-2 is the same. The
last-2 lift is a **hard** width effect.

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

24 new stems from the 36-family pile (`--overlap drop-from-train`,
`n_train=24`): last-2 **8/12**, **31/48**, AUC **0.625** versus last-4
**8/12**, **28/48**, 0.585. Ranking tied; leftover last-2 **10/20 vs
13/20**. Do not sell **31/48**.

Same-register 100 → 36×4 (`--skip-nested`): last-2 **31/36**, isolated
**118/144**, AUC **0.743** versus last-4 **25/36**, **96/144**, 0.624.
Last-2 helps the 36-family transfer. It does **not** transfer to
Distil SynthID 12 (**5/12**, 21/48, AUC 0.510). Distil 100 last-2 →
original-12 GPT-2 is also chance (**7/12**, 26/48, 0.493 versus last-4
**7/12**, 29/48, 0.596). Public 100 last-2 tables do **not** classify
control-as-marked 12 (**4/12**, 19/48, AUC 0.441 versus last-4
**7/12**, 19/48, 0.522): last-2 is instance-specific when the train
key is public. In-domain second-key last-2 below is a different split.
100 one-liners → Grok-register (`--skip-nested`; do not mix grok12 into
train): last-2 grok12 **6/12**, **29/48**, AUC **0.590** versus last-4
**4/12**, **12/48**, 0.424; grok36 last-2 **18/36**, **77/144**, 0.516 versus
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
**10/12**, AUC **0.718**, isolated 28/48. The last-2 lift is a **hard** width effect, not “shorten every count spec.”
Occupancy-free `hashtok` last-2 on the original 12 is **11/12**,
**23/48**, AUC **0.788**, unmarked $\le 0$ **48/48** versus last-4
`hashtok` **11/12**, **24/48**, **0.796** — isolated does not repeat
the hard last-2 jump. Do not sell hashtok last-2 **23/48**.

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
`experiments/2026-09-02-pair-12x4-control-as-marked/`. DistilGPT2
$\Hw=12$ twins: `experiments/2026-09-04-pair-distil-12x4-ngram13/`
(opened freeze is last-4 interpolate **9/12** / hard **6/12**).
Qwen2-1.5B $\Hw=12$: `experiments/2026-09-04-pair-qwen-12x4-ngram13/`
(opened freeze is last-4 interpolate **4/12** / hard **4/12**).

**Hypothesis.** Hard last-4 on $\Hw=4$ tournament text is slightly too
long for **full-file** isolated sign: last-2 keeps opening last-k mass
in the file mean without falling into last-1 unigram collapse. It is
not a body-hash match (n=100 last-2 tail **58/100**; Kirchenbauer
last-1 tail is **100/100**). Grok-register 12 last-2 isolated
**34/48** is not that opening-only split (0:4 **31/48**, tail
**30/48**). It is tied to short tournament history:
`ngram_len=13` ($\Hw=12$) last-2 does not rescue ranking (12×4 isolated
**21/48** vs last-4 **22/48**; 100×4 ranking **63/100** vs **66/100**).
Matching last-12 to $\Hw=12$ does not either (12×4 **24/48**; 100×4
ranking **71/100**, isolated **226/400**, below last-2 **248/400**).
DistilGPT2 $\Hw=12$ last-2 ranking is chance (**6/12**); isolated
**25/48** vs last-4 **16/48** is a small-n isolated lift, not the
public GPT-2 **94/100** jump, and is not the locked **25/48**.
Qwen2-1.5B $\Hw=12$ last-2 ranking is **5/12**; last-12 is **4/12**.

**Non-claim.** Do not rewrite the locked headline to **34/48** or
**10/12**. Do not sell transfer **29/48**, 24-stem **31/48**, or nested **23/48**. Do not
sell leftover **12/20**, leftover tail **13/20**, leftover occupancy-free
**8/20**, or leftover 100→12 last-2 **11/20**. Do not sell
opening **389/400**, second-key **34/48**, second-key opening **47/48**, medium **330/400**, Distil
**66/100**, Qwen **351/400**, grok **34/48**, transfer grok **29/48**,
xkey transfer **19/48**, Distil→GPT-2 last-2 **26/48**, or occupancy-free last-2 **23/48**. Do not switch interpolate to last-2.
Do not switch `hits` to last-2 (ranking **9/12**, AUC 0.632). Do not
switch occupancy-free `hashtok` to last-2 (**23/48** vs last-4
**24/48**). Do not
add `hard2` as a method name. Do not present last-2 as matching the
keyed hash window (last-5 lost the grid; $\Hw=12$ last-2 does not
repeat the 100-family **94/100** jump). Matching last-12 to $\Hw=12$
does not replace last-2 (100-family isolated **226/400** vs last-2
**248/400**). Do not present last-2 as a Kirchenbauer-style body
companion. Public last-2 tables trained on 100 GPT-2 families do not
classify Kirchenbauer original-12 (isolated **24/48**, AUC 0.554). Do
not sell ngram-13 last-12 **71/100**, Distil ngram-13 last-2 **25/48**,
GPT-2 $\Hw=12$ last-2 opening **87/100**, last-12 opening **82/100**, Distil last-12 **8/12**, Distil $\Hw=12$ 100 last-2 **88/100** /
**313/400**, Distil $\Hw=12$ last-4 **89/100** / interpolate
**88/100**, Distil last-12 n=100 **87/100**, Distil interpolate last-4
opening **90/100** / tail **60/100**, GPT-2 $\Hw=12$ interpolate last-4
opening **86/100** / tail **50/100**, Qwen ngram-13 last-2 **5/12**, hashpool last-2 **31/48**, GPT-2 $\Hw=12$ hashtok last-4 **313/400**, Distil $\Hw=12$ hashtok last-4 **369/400**, Distil $\Hw=12$ snapleave **73/100**, or public SynthID snapleave **52/100**.

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

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods hard --context-len 12 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-12x4-ngram13-k12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods hard --context-len 12 --skip-hashpool --skip-nested \
  --out-dir /tmp/kgw-lab/probe-100x4-ngram13-k12

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods hard --context-len 2 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-ngram13-k2-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods hard --context-len 12 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-ngram13-k12-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-ngram13 \
  --model gpt2 --methods hard --context-len 2 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-ngram13-k2

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-ngram13 \
  --model gpt2 --methods hard --context-len 2 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-ngram13-k2

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-ngram13 \
  --model gpt2 --methods hard --context-len 12 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-ngram13-k12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-ngram13 \
  --model gpt2 --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-ngram13-interp-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods interpolate --context-len 4 --skip-hashpool --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-ngram13-interp-k4-windows-ends

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-ngram13 \
  --model gpt2 --methods hard --context-len 12 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-ngram13-k12

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-ngram13 \
  --model gpt2 --methods interpolate --context-len 2 --skip-hashpool \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-ngram13-interp-k2

python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-12x4-ngram13 \
  --model Qwen/Qwen2-1.5B-Instruct --methods hard --context-len 2 \
  --skip-hashpool --out-dir /tmp/kgw-lab/probe-qwen-12x4-ngram13-k2

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods hashtok --context-len 4 --fit-prefix 4 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-ngram13-hashtok-k4

python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods hashtok --context-len 1 --fit-prefix 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-12x4-ngram13-hashtok-k1

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods hashtok --context-len 4 --fit-prefix 4 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-ngram13-hashtok-k4

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods hashtok --context-len 1 --fit-prefix 1 --skip-nested \
  --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-100x4-ngram13-hashtok-k1

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-ngram13 \
  --model gpt2 --methods hashtok --context-len 4 --fit-prefix 4 \
  --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-12x4-ngram13-hashtok-k4

python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-ngram13 \
  --model gpt2 --methods hashtok --context-len 4 --fit-prefix 4 \
  --skip-nested --windows 0:4,64:128 \
  --out-dir /tmp/kgw-lab/probe-distil-100x4-ngram13-hashtok-k4
```

**Why it is a backlog item.** Isolated **25/48** is the honest last-4
headline. Last-2 is the one existing-scorer width that moved isolated
sign on 12, 36, and 100 **public** GPT-2 families in the same
direction. At n=100 that lift is opening mass kept in the file mean
(**334/340** of last-2 TPs are 0:4 TPs), not a body window: original-12
tail **10/12** overstates geography. It is not a universal
shorter-context recipe: longer hash history kills the ranking jump
(matching last-12 to $\Hw=12$ does not recover it; DistilGPT2 $\Hw=12$
last-2 ranking is **6/12**); Distil/Qwen/medium public-$\Hw$ 12 do not
repeat the isolated McNemar; Grok-register 12 does
(**34/48**, ranking still **8/12**). Hits and hashpool last-2 hurt
ranking. Keep leftover-20 as the honesty bound on any SynthID width
change.

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
and was not reimplemented. Li-Chen and Kim (2026) (ChainMark;
arXiv:2607.18445) is model-free detection **from the secret key and
tokenizer**, not `indicate`. Gloaguen et al. (2026) (unified watermark
framework; arXiv:2602.06754) is scheme design, not a finished-string
reader this laboratory can port. Signature filtering
(arXiv:2606.18430) is a detection-time n-gram filter in front of a
**keyed** statistic $Z(T)$; the filter itself is key-free, the test is
not `indicate`. DHMark (arXiv:2608.03093) is public-key scheme design.
Rao–Blackwellized e-processes (arXiv:2607.21958) reconstruct the
Gumbel-max PRNG from the secret key. Attribute-based undetectable
watermarking (arXiv:2608.03174) is keyed cryptographic delegation.
Mansouri et al. (2026) (Pattern Stability Score; arXiv:2608.18102) is
keyed local z-score plus paraphrase-depth stability, not `indicate`.
Luan et al. (2026) (VOW; arXiv:2604.27666) is Verifiable Oblivious PRF
detection with the provider key. Ceppi and Sanchez (2026) (Stateless
Bernoulli Watermarking; arXiv:2609.03844) is keyed z-score scheme
design. Tolstokorov et al. (2026) (DirBucket / Rent-a-RAG;
arXiv:2609.03749) watermarks RAG documents in embedding space, not
`indicate` on sampling twins. Bakshi et al. (2026) (OpenStamp;
arXiv:2608.27899) implants a keyed mark in the unembedding layer and
detects with an LLR against a privately held base checkpoint.
Diaa et al. (2026) ($k$-SwordStamp; arXiv:2608.27666) is semantic
scheme design. Zhang et al. (2026) (SemTrace; arXiv:2608.29575) traces
document exposure with NLI bits, not sampling twins. Feng et al.
(2026) (Cocktail complementary watermarks; arXiv:2608.12713) is keyed
dual tournament scores. Park et al. (2026) (WeaveMark;
arXiv:2609.02177) is keyed multi-bit scheme design. te Lintelo et al.
(2026) (WoE; arXiv:2608.29151) plants a secret green list in selected
MoE expert vocabularies and tests with that seed. Gao et al. (2026)
(PathMark; arXiv:2607.03688) is keyed MoE routing-path IP. Sun et al.
(2026) (WaterMoE; arXiv:2607.13099) is keyed MoE router perturbation.
None of those is a finished-string key-free reader this laboratory can
port.

### Occupancy-free KGW openings; SynthID last-1 full file; interpolate last-2; mix/backoff; occupancy-free last-2; ngram-13 last-12; Distil ngram-13 last-2/last-12; ngram-13 hashtok; SynthID hashpool last-1/last-2; Aaronson snapleave; Qwen KGW rankpath

`postokhits` on Kirchenbauer 12×4 last-4 is **11/48**; last-1 is
**33/48** with unmarked $\le 0$ only **25/48**. SynthID last-1
full-file hard is **1/12**; SynthID hashpool last-1 is **5/12**,
**24/48**, AUC 0.472. Interpolate last-2 drops 36×4 ranking from
**34/36** to **32/36**. Mix last-1+last-4 and backoff on public
SynthID 12 are chance (**6/12**). Occupancy-free `postokhits` last-2
on public 12 is **23/48**, same as last-4 `postokhits`, below
**25/48**. Occupancy-free `hashtok` last-2 is **23/48** versus last-4
**24/48**. Matching last-12 / last-6 / last-13 to $\Hw=12$ leaves
ngram-13 isolated at **21–24/48**. Occupancy-free `hashtok` last-4 on
GPT-2 $\Hw=12$ 12×4 is opening **11/12**, **23/48**, AUC **0.724**
(0:4 equals full-file; tail **0/12**); isolated is chance (file-level
binom $p\approx 0.67$). Last-1 is empty (**0/48**). At n=100 last-4 is
**95/100**, **313/400**, **0.888**, **12** ranking-only; 0:4 equals
full-file; tail **0/100**. Distil $\Hw=12$ last-4 hashtok is the same
split: 12×4 **9/12**, **28/48**, **0.727** (0:4 equals full-file; tail
**0/12**); 100×4 **98/100**, **369/400**, **0.943**; tail **0/100**.
Last-1 empty on both generators. Occupancy-free hashing is not a
$\Hw=12$ body reader and does not repeat last-2. Do not sell
**313/400** or **369/400**. DistilGPT2 $\Hw=12$ last-2 ranking is
chance (**6/12**); isolated **25/48** is not the locked public last-4
headline. Distil $\Hw=12$ 100 last-2 is **88/100**, **313/400**,
below last-4 **89/100**, **354/400**; opening **92/100**, tail
**70/100**. Distil last-12 is **8/12**, **17/48**. Distil interpolate
last-2 is **9/12**, **20/48**, not better than last-4 interpolate
**9/12**, **21/48**. Qwen $\Hw=12$ last-2 ranking is **5/12**. Hashpool last-2 on public 12 is
**10/12**, **31/48**, AUC **0.629**, below last-4 hashpool **11/12**,
**35/48**, **0.716**. KGW `rankpath` tail **11/12** is below
interpolate **12/12**, AUC **0.904**. DistilGPT2 KGW last-4 rankpath is
chance (**4/12**, **20/48**, AUC **0.397**). At n=100 Distil KGW
rankpath still ranks **82/100** while isolated **199/400** is chance
(file-level binom $p\approx 0.56$); tail isolated **128/400** is
chance (binom $p=1$). GPT-2 KGW 100 rankpath is **79/100**,
**248/400**, 0.679; tail **71/100**, **222/400**, 0.607, far below
interpolate tail **100/100**, **364/400**. Last-1 Distil KGW rankpath
is **8/12**, **27/48**, AUC **0.602**. Qwen2-1.5B KGW last-4
rankpath is also chance (**8/12**, **26/48**, AUC **0.540**; windows
0:4 **3/12** / 64:128 **3/12**). Last-1 Qwen KGW rankpath is
**10/12**, **29/48**, AUC **0.668**, unmarked $\le 0$ only **28/48**
— below Qwen hits last-1 **41/48**. Count
tables remain the Kirchenbauer body reader. Aaronson `snapleave` is
**0/12**. Confirmatory n=100 is anti-correlated: snapleave **0/100**,
isolated **0/400**, AUC **0.000**, mean marked $-0.34$ vs unmarked
$+0.10$ (marked text stays at the unmarked argmax more often). Do not
invert that sign into a detector. Do not sell **0/100** or inverted
AUC **1.000**. Distil Aaronson n=100 is the same anti-correlation
(snapleave **0/100**, **0/400**, AUC **0.077**). Distil Aaronson 12 is
the same anti-correlation (snapleave **0/12**, **0/48**, AUC
**0.000**). Aaronson `snapmiss` n=100 is also anti (**2/100**, AUC
**0.079**, isolated **0/400**); do not invert. Qwen Aaronson 12 is
anti at n=12 (snapleave **6/12**, AUC 0.444, perm $p\approx 0.9995$).
Table-free `--snaprate` on GPT-2 $\Hw=12$ is chance ranking:
12×4 snapleave **7/12**, marked>0 **48/48** with unmarked $\le 0$
**0/48**, AUC 0.523, perm $p\approx 0.33$; snapupset **6/12**. At n=100
snapleave **51/100**, marked>0 **383/400** with unmarked $\le 0$ only
**11/400**, AUC **0.507**, perm $p\approx 0.34$; snapupset **48/100**,
**375/400**. Both classes leave the unmarked argmax; nested Youden is
chance (**224/400** vs **189/400**). GPT-2 public SynthID ($\Hw=4$)
is the same chance at confirmatory n: 12×4 snapleave **9/12**, AUC
**0.613**, perm $p\approx 0.042$ dies at n=100 (**52/100**, AUC
**0.512**, perm $p\approx 0.18$, marked>0 **385/400**, unmarked
$\le 0$ **11/400**). 36×4 is **18/36**, AUC **0.482**. Grok-register
12 snapleave **10/12**, AUC **0.589**, perm $p\approx 0.040$ is the
same n=12 look as original-12 **9/12**. Distil public SynthID n=100 is chance
(**53/100**, **0.488**); Qwen public 12 is **6/12**, 0.453. Distil
$\Hw=12$ n=100 snapleave ranks **73/100**, AUC **0.631**, perm
$p\approx 0.0005$, unmarked $\le 0$ **83/400**; n=12 was **4/12**,
AUC **0.434**. Qwen $\Hw=12$ 12 is **9/12**, 0.583, perm $p\approx 0.17$.
Matching tournament width does not make snaprate a public-SynthID
detector. Distil $\Hw=12$ ranking is not Distil KGW (anti **31/100**)
and is not isolated $\tau=0$. Do not sell **383/400**, **48/48**,
**73/100**, public **9/12**, grok12 **10/12**, or 36×4 **18/36**.
`snapmiss` on GPT-2 KGW is chance (**56/100**, **0.518**, isolated
**0/400**); public SynthID snapmiss **62/100** / Distil $\Hw=12$
**74/100** are ranking-only. Do not leftover-target those zeros. Do
not sell **62/100** or **74/100**.
Occupancy-free `postokhits` last-1 is empty on GPT-2, Distil,
and Qwen Aaronson (**0/48**, all zeros); last-4 Qwen Aaronson
`postokhits` is opening **32/48** (tail **0/48**). Occupancy-free
`hashtok` last-1 on GPT-2 Kirchenbauer 12 is also empty (**0/48**);
last-4 is **13/48**. Distil KGW last-4 `hashtok` is opening **7/12**,
**14/48**, AUC **0.605** (tail **0/48**); last-1 is empty. Qwen KGW
last-4 `hashtok` is anti-correlated **2/12**, **14/48**, AUC **0.432**
(tail **0/48**); last-1 is empty. Distil KGW and GPT-2 Aaronson last-1 `hashtok`
are empty too; Aaronson last-4 `hashtok` is opening **40/48**. GPT-2
Aaronson 100 last-4 `hashtok` is **100/100**, **384/400**, AUC
**0.982** (0:4 equals full-file; tail **0/100**); last-1 is empty.
Qwen
Aaronson last-4 `hashtok` is opening **11/12**, **44/48**, AUC
**0.966** (tail **0/48**), above `postokhits` last-4 **32/48**, still
not last-1 hits **48/48**. Qwen Aaronson last-1 `rankpath` is
**12/12**, **28/48**, AUC **0.899** — above last-4 rankpath
**16/48**, below last-1 hits **48/48**. Distil Aaronson last-4 `hashtok` is opening
**10/12**, **44/48**, AUC **0.944**, unmarked $\le 0$ only **40/48**
(8 FPs); tail **0/48**. Distil Aaronson 100 last-4 `hashtok` is the
same opening split: **90/100**, **352/400**, AUC **0.865**, unmarked
only **290/400**; 0:4 equals full-file; tail **0/100**. Last-1 `hashtok`
is empty on Distil 100 too (**0/400**). Last-1 `hashtok` is empty on Distil and Qwen
Aaronson too (**0/48**). None of those is a backlog item.

---

## What this file is for

A freeze of **width and mixin geography** that already moved a grain:

1. Kirchenbauer green-list leak is a **body** leak under last-4
   interpolate (100-family tail **100/100**, opening **88/100**).
   Confirmatory n=100 rankpath is not that body reader (GPT-2 tail
   **71/100** / **222/400**; Distil isolated **199/400** is chance).
   Distil → GPT-2 last-4 interpolate transfers the body (**331/400**,
   tail **306/400**) where last-4 hard isolated **53/400**. GPT-2 →
   Distil interpolate isolated **385/400** is opening-heavy. Last-4
   interpolate 100 → original-12 recovers the same body leak last-4
   hard missed (Distil → Distil 12 **42/48** vs **6/48**; Distil →
   GPT-2 12 **43/48** vs **15/48**). Isolated $\tau=0$ on Distil/Qwen
   12 interpolate last-4 sits with the tail (Distil **35/48**, Qwen
   **34/48**), not the opening. Those tables do not classify
   public SynthID (**0/48** / **8/144**) or grok12 (**5/48**) or Distil
   public SynthID (**1/48** / same-stem **3/48**) or Qwen public SynthID
   (**15/48**, ranking **1/12**) or $\Hw=12$ original-12 (**1/48**) or
   n=100 $\Hw=12$ (**51/400** / Distil **24/400**). Do not leftover-target
   Distil $\Hw=12$ opening **280/400**. Do not
   sell **331/400**, **385/400**, **46/48**, **43/48**, **42/48**,
   **40/48**, **35/48**, or **34/48**. Table-free snaprate ranks GPT-2
   KGW (**88/100**) and Distil $\Hw=12$ (**73/100**) without isolated
   $\tau=0$; public SynthID n=100 is chance (**52/100**, **0.512**;
   36×4 **18/36**).    Do not sell **73/100**, **9/12**, or grok12
   **10/12**. GPT-2 KGW snapmiss is chance (**56/100**); public
   snapmiss **62/100** is ranking-only.
2. Matching `context_len` to last-1 hash width recovers isolated
   `hard` / `hits` / `hashpool` sign on Kirchenbauer (100-family hard
   **389/400** vs last-4 **209/400**; hits **395/400** vs **254/400**;
   hashpool **394/400** vs **304/400**) and `hard` on Aaronson–Kirchner
   (**388/400** vs last-4 **344/400**). Kirchenbauer interpolate last-1
   at 100 families matches last-4 interpolate geography (opening
   **83/100**, tail **100/100**). Aaronson last-1 ranks both
   windows on `hard`; interpolate last-1 isolated at n=100 is
   opening-heavy (**380/400**) plus tail ranking-without-TP
   (**284/400**). Freeze interpolate last-4 is the same split
   (opening **380/400**, full-file **208/400** equals the tail). Last-4
   hard opening is already **388/400** with FPs; last-1 recovers tail
   isolated (**324/400** → **380/400**) and specificity. Kirchenbauer last-1 `hard` / `hits` / `hashpool` is a body lift. DistilGPT2 Aaronson
   last-1 still lifts `hard` only at n=12 (**16/48**); at n=100 last-1
   hard is **372/400** versus last-4 **308/400** because last-4 dilutes
   an already-saturated opening, not because Distil grows a GPT-2
   Aaronson tail (**240/400**, not **380/400**). last-4 `hits` **44/48** is opening
   overlap, not rankpath’s body leak. Distil 100 last-4 hits stays
   opening (**376/400** equals 0:4 **368/400**; tail **56/100**). GPT-2 100 Aaronson last-1 tables
   transfer onto Distil files (**40/48** vs last-4 hard **16/48**);
   last-4 hits transfer is also **44/48**. GPT-2 100 Aaronson last-1 →
   Distil 100 is a body ranking leak (tail **92/100**, isolated
   **244/400** equals the tail; last-4 isolated **188/400** is chance);
   Distil in-domain last-1 **372/400** is opening dilution, not that
   transfer. Distil 100 last-1 tables recover the Distil 12 body leak
   in-domain last-1 missed (**12/12**, **40/48**, tail equals
   full-file, versus in-domain **16/48**); Distil 100 → GPT-2 12 is
   the same isolated **40/48**; Distil 100 → GPT-2 100 is **98/100**,
   **348/400**. GPT-2 100 → original-12
   last-1 hard is the same isolated **40/48** (tail equals full-file;
   last-1 hits transfer isolated **36/48**). Distil 100 rankpath last-4
   still ranks the tail (**97/100**) while isolated **372/400** sits
   with opening **344/400**, not Distil 12 rankpath tail **44/48**. GPT-2
   Aaronson 100 rankpath last-4 isolated **396/400** sits with the tail
   **392/400**.
   Distil 100 KGW → GPT-2 100
   last-1 is a body leak (**338/400**, tail **327/400** vs last-4
   **53/400**); GPT-2 100 KGW → Distil 100 last-1 is **247/400** (Distil
   tables on GPT-2 files outrank GPT-2 tables on Distil files). Last-1
   KGW tables do not classify public SynthID (Distil 100 → Distil
   SynthID **0/48**; GPT-2 100 → SynthID 36 **7/144**) or Aaronson
   (n=100 Distil last-1 **180/400**, AUC 0.519; Distil 12 ranking
   **8/12** does not survive confirmatory n) or $\Hw=12$ (last-1 KGW
   **49/400** / Distil **20/400**; last-1 KGW hashpool **19/400** /
   Distil **12/400**; Aaronson last-1 ranking **98/100**
   with isolated **1/400**; interpolate last-4 **100/100**,
   **0/400**; last-1 hashpool **99/100**, **0/400**; unigram **73/100**,
   **0/400**; rankpath **55/100**, **0/400**; Distil rankpath
   **31/100**, **12/400**). Do not sell Aaronson
   ranking **98/100**, hashpool **99/100**, unigram **73/100**, Qwen
   **12/12**, Distil interpolate **88/100**, Distil hashpool
   **71/100**, Distil hashpool→SynthID ranking **10/12** with isolated
   **0/48**, hashlog **56/400**, tokmlp **122/400**, surface ranking
   **83/100**, charcnn **17/400**, Distil surface **55/100**, or AUC
   **0.890**.
3. On public SynthID $\Hw=4$, the existing `hard` reader is stronger at
   last-2 than at last-4 for **full-file** isolated sign, without
   fixing leftover and without touching interpolate. At n=100 that
   lift is opening mass kept in the file mean, not a body leak. The
   jump does not repeat at $\Hw=12$, including last-12, DistilGPT2
   $\Hw=12$ last-2 ranking **6/12** (n=12) and **88/100** below last-4
   **89/100** (n=100), and Qwen2-1.5B $\Hw=12$ last-2 ranking
   **5/12**. Distil $\Hw=12$ interpolate last-4 is front-loaded
   (opening **90/100**, tail **60/100**, AUC **0.565**), opposite of
   Kirchenbauer interpolate.

Keep leftover-20 as the honesty bound on any SynthID width change.
Do not write `thesis/` from this file.
