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
detection. Occupancy-free KGW openings are **not** the leak. Rankpath
on Kirchenbauer 12 is below interpolate; do not sell **31/48**. Distil
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
has newline-loop files; do not sell **355/400**. Qwen2-1.5B KGW hits
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
Kirchenbauer 12 (**0/48**, AUC **0.568**). Mixin-specific. n=12 only;
no 100-family rankpath.

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
**96/100**, or tail ranking **95/100**. Last-1 unigrams on Distil
degenerate loops are not a reason to sell those counts
(H-aar-d100-ctrl **71/100**). Occupancy-free `hashtok` last-1 on Distil
Aaronson 100 is empty (**0/100**, **0/400**, all zeros), same as Distil
12. Last-4 `hashtok` (no `--skip-hashpool`; `--fit-prefix 4`) is
**90/100**, **352/400**, AUC **0.865**, unmarked $\le 0$ only
**290/400** (precision **0.762**); 0:4 is the same **352/400**; tail
**0/100**, **0/400**. Opening overlap with FPs, not last-1 hard’s
full-file **372/400** or GPT-2 Aaronson last-1 body. Hits last-1 is
not occupancy-free hashing.

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
reason to sell **350/400** or Distil 100 hits last-1 **355/400**. Distil Aaronson 100 last-1 unigrams on Distil degenerate loops are not a reason to sell **372/400**. DistilGPT2 Aaronson 12×4:
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
hits is opening overlap (tail **0/48**); rankpath is the body reader
(tail **44/48**). GPT-2 100 Aaronson last-1 tables
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
last-1 tail **182/400**, hits last-1 transfer **48/48** / **44/48**,
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
**128/400**, Distil hits last-4
**44/48**, Distil postokhits last-4 **40/48**, Distil hashpool last-4
**32/48**, Distil last-1 hits **32/48**, Distil last-1 postokhits
**0/48**, Aaronson rankpath
**44/48**, Aaronson rankuni **44/48**, Distil Aaronson rankpath **44/48**,
GPT-2 100 Aaronson last-1 → Distil **40/48**, GPT-2 100 Aaronson last-1 → Distil 100
**244/400** / hits ranking **97/100**, Distil 100 Aaronson last-1 → Distil 12
**40/48** / GPT-2 12 **40/48** / GPT-2 100 **348/400**, Distil 100 last-1 hits → Distil 12
**36/48** / GPT-2 100 **356/400**, Distil 100 last-1 hashpool → GPT-2 12
**24/48**, Distil KGW rankpath
**20/48**, Qwen KGW rankpath **26/48**, Aaronson unigram **24/48**,
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
wins with no isolated TP). Hashpool last-1 transfer to public SynthID
12 is **2/48**, AUC 0.501. Aaronson last-1 tables trained on 100
families do **not** classify Kirchenbauer 12 (**0/48**) or public
SynthID 12 (**0/48**, ten ranking wins with no isolated TP). Aaronson
rankpath 12 → public SynthID 12 is also isolated **0/48**. The
last-1 lift is mixin-specific.

Same mixin, shared GPT-2 BPE, last-1 **does** transfer across
generators. Last-4 does not:

| Train → test | last-1 hard | last-4 hard |
|---|---|---|
| GPT-2 100 KGW → GPT-2 12 KGW | **12/12, 48/48, AUC 1.000** | 8/12, 32/48, 0.565 |
| GPT-2 100 KGW → Distil 12 KGW | **12/12, 47/48, AUC 0.991** | 5/12, 22/48, 0.488 |
| Distil 100 KGW → GPT-2 12 KGW | **12/12, 42/48, 0.987** | 11/12, 15/48, 0.685 |
| Distil 100 KGW → Distil 12 KGW | **12/12, 42/48, 0.982** | 7/12, 6/48, 0.519 |

`--skip-nested`; isolated is $\tau=0$. Unmarked $\le 0$ on GPT-2 12
hard last-1 is **43/48** (five FPs). Distil in-domain last-1 was
**46/48**; GPT-2 tables on Distil files are **47/48**. Distil last-4
→ GPT-2 12 ranks **11/12** with isolated only **15/48** (two ranking
wins with no isolated TP). Distil last-4 → Distil 12 is chance
isolated **6/48**. Last-1 is the isolated transfer; last-4 ranking can
look fine while files do not sign. Same last-1 `hashpool` tables:
GPT-2 100 → GPT-2 12 **12/12, 48/48**, AUC **0.998**, unmarked $\le 0$
**40/48** (eight FPs); GPT-2 100 → Distil 12 **12/12, 47/48**, 0.994.
Distil 100 hashpool last-1 → GPT-2 12 is **12/12, 44/48**, AUC
**0.994**, unmarked $\le 0$ **47/48**; Distil 100 → Distil 12 is
**12/12, 40/48**, 0.991, unmarked $\le 0$ **47/48**.
Do not sell **48/48**, **47/48**, **44/48**, or **40/48**. Qwen uses a
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

`--skip-nested`. Unmarked $\le 0$ is **43/48**, **43/48**, **45/48**,
**46/48**. Distil 100 → Distil 12 hits last-1 **44/48** is above that
pair’s hard last-1 **42/48**. Do not sell **48/48** or **44/48**.

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
**32/48**); last-4 tables do not (Distil 100 last-4 → Distil 12 is
isolated **6/48**). The freeze in
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
already, not a width match. DistilGPT2 Aaronson 12 last-1 still lifts
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
sell last-12 opening **82/100** or **293/400**.

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
opening **86/100** / tail **50/100**, Qwen ngram-13 last-2 **5/12**, or hashpool last-2 **31/48**.

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
reader this laboratory can port.

### Occupancy-free KGW openings; SynthID last-1 full file; interpolate last-2; mix/backoff; occupancy-free last-2; ngram-13 last-12; Distil ngram-13 last-2/last-12; SynthID hashpool last-1/last-2; Aaronson snapleave; Qwen KGW rankpath

`postokhits` on Kirchenbauer 12×4 last-4 is **11/48**; last-1 is
**33/48** with unmarked $\le 0$ only **25/48**. SynthID last-1
full-file hard is **1/12**; SynthID hashpool last-1 is **5/12**,
**24/48**, AUC 0.472. Interpolate last-2 drops 36×4 ranking from
**34/36** to **32/36**. Mix last-1+last-4 and backoff on public
SynthID 12 are chance (**6/12**). Occupancy-free `postokhits` last-2
on public 12 is **23/48**, same as last-4 `postokhits`, below
**25/48**. Occupancy-free `hashtok` last-2 is **23/48** versus last-4
**24/48**. Matching last-12 / last-6 / last-13 to $\Hw=12$ leaves
ngram-13 isolated at **21–24/48**. DistilGPT2 $\Hw=12$ last-2 ranking is
chance (**6/12**); isolated **25/48** is not the locked public last-4
headline. Distil $\Hw=12$ 100 last-2 is **88/100**, **313/400**,
below last-4 **89/100**, **354/400**; opening **92/100**, tail
**70/100**. Distil last-12 is **8/12**, **17/48**. Distil interpolate
last-2 is **9/12**, **20/48**, not better than last-4 interpolate
**9/12**, **21/48**. Qwen $\Hw=12$ last-2 ranking is **5/12**. Hashpool last-2 on public 12 is
**10/12**, **31/48**, AUC **0.629**, below last-4 hashpool **11/12**,
**35/48**, **0.716**. KGW `rankpath` tail **11/12** is below
interpolate **12/12**, AUC **0.904**. DistilGPT2 KGW last-4 rankpath is
chance (**4/12**, **20/48**, AUC **0.397**). Last-1 Distil KGW rankpath
is **8/12**, **27/48**, AUC **0.602**. Qwen2-1.5B KGW last-4
rankpath is also chance (**8/12**, **26/48**, AUC **0.540**; windows
0:4 **3/12** / 64:128 **3/12**). Last-1 Qwen KGW rankpath is
**10/12**, **29/48**, AUC **0.668**, unmarked $\le 0$ only **28/48**
— below Qwen hits last-1 **41/48**. Count
tables remain the Kirchenbauer body reader. Aaronson `snapleave` is
**0/12**. Occupancy-free `postokhits` last-1 is empty on GPT-2, Distil,
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
   last-1 hits transfer isolated **36/48**).
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
