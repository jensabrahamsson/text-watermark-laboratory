# Isolated-file protocol (36 Grok-length families)

This is a **methods freeze** for a larger Grok-register train. It does
not add a scorer. Twelve Grok-length families did not beat one-liner
lock A (**16/48** vs **23/48**). One hundred one-liners rank those same
Grok-length files **11/12** with nested Youden **22/48 vs 41/48**, while
occupancy-free openings are **0/48**. The `atoms` decode of that
transfer is almost all Witten–Bell backoff plus shared GPT-2 templates
(`'The' → ' car'`, dialogue 4-grams). This file asks whether **more
Grok-length train mass**, disjoint from the already-seen grok12 stems,
creates occupancy-free isolated TPs on held-out Grok-length files, or
still fails.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** run `pair` until the prompt directory is on the remote SHA
named in [LOGBOOK.md](LOGBOOK.md). Do **not** mix
`experiments/2026-09-01-pair-grok12x4/` into the train after seeing
LRs.

## Why freeze now

The locked square is:

| Train | Test | Lock A nested Youden |
|---|---|---|
| 100 one-liners | original 12×4 | **23/48 vs 38/48** |
| 12 Grok-length | original 12×4 | **16/48 vs 41/48** (H-reg-A fails) |
| 100 one-liners | grok12×4 | **22/48 vs 41/48** |
| 12 Grok-length | grok12×4 in-family | nested-by-stem **24/48 vs 40/48** |

Occupancy-free 100→grok12 is **0/48**. Atoms show the 11/12 rank is not
an observed-token core. n=12 Grok-length train is too small to tell
whether register-matched last-4 overlap would appear with more scenes.
The missing cell is **36 new Grok-length families → already-frozen
grok12×4** (out-of-family, same register) and the same tables → original
12×4 (scale-up of H-reg-A). Those test directories already exist. This
protocol only freezes **new train prompts** and the analysis flags.

Do not add grok12 stems to the 36 after peeking. That mix is refused.

## Primary scientific question

Do frozen key-free tables, trained on 36 new GPT-2 twins from
Grok-length scene prompts disjoint from grok12, the original 12, and
the 100 one-liners, classify those held-out files without detector
keys, `hash_iv`, or g-values?

Not: can another `probe --methods` name lift **25/48**. Not: does
in-family ranking on the new 36 families work (that is a check). Not:
does pooling grok12 with the 36 after seeing both LRs help.

## Frozen scorers

Same three readers as [PROTOCOL-isolated.md](PROTOCOL-isolated.md).
Exact CLI. No new method names.

| Lock | Reader | Train flags |
|---|---|---|
| A | Hard last-4 interpolate | `--methods interpolate --context-len 4` |
| B | Opening poshits | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| C | Opening rankpath | `--methods rankpath --fit-prefix 4 --pos-bucket 1` |

Lock C here is **only** rankpath (not `--rankpath`, which also emits
default count methods). Rankpath needs the unmarked LM.

Secondary occupancy-free readout of the **same** lock B tables uses
`--methods postokhits` with those flags. Opening-overlap uses `openings`
with postokhits, `--skip-stem-curve`. Official `score` on the new twins
is a positive control. It is not a key-free endpoint.

## Hypotheses (stated before generation)

- **H-scale-A.** Lock A nested Youden on the original 12×4, trained on
  these 36 Grok-length families, is higher than grok12-train lock A
  **16/48**. More in-register mass. This still does not have to beat
  **25/48**.
- **H-scale-grok.** Lock A nested Youden on grok12×4, trained on the 36,
  is higher than 100-one-liner xreg lock A **22/48**. Same register as
  the test files, more train mass than n=12 in-family.
- **H-scale-B.** Occupancy-free lock B (postokhits t=0) still tracks
  opening-atom overlap on both test sets, not a denser isolated
  detector. Atoms already showed 100→grok12 observed-token openings are
  empty; this asks whether Grok-length train fills that channel.
- **H-scale-iso.** Neither nested Youden replaces **25/48**. Do not sell
  prompt ranking, occupancy, `The car`, or a union of locks A/B/C.

Report `ranking_without_isolated_tp` and
`ranking_losses_with_isolated_tp`. Prompt ranking is not isolated
recall.

## Primary endpoint

**Isolated nested Youden** on each frozen test directory: marked files
above the train-LOO Youden threshold, unmarked files at or below it.

Report both test sets. The scientifically new cell is grok12×4
(out-of-family, Grok register). The original 12×4 cell is the scale-up
of H-reg-A. In-family leave-one-prompt-out on the new 36 is a register
check. It is not **25/48**.

## Corpus

Thirty-six **new** English multi-paragraph scene prompts, Grok register
(first person, everyday setting, ~220–330 words, no instruction to the
model). Disjoint as strings from `experiments/2026-08-17-grok-prompts/`,
`experiments/2026-08-17-more-prompts/`,
`experiments/2026-08-31-prompts-long12/`,
`experiments/2026-08-31-prompts-family12/`,
`experiments/2026-08-31-prompts-tails12/`,
`experiments/2026-09-01-prompts-100/`, and
`experiments/2026-09-01-prompts-grok12/`. Topics are not those stems
and not harbour, night bus, library, market, kitchen, station, rain,
letter, workshop, office, garden, ferry queue, service station, car
boot, bowling alley, hospital corridor, charity shop, boxing gym,
campsite, registry office, scrapyard, chip shop, fire station, or taxi
rank.

| Item | Value |
|---|---|
| Prompts | `experiments/2026-09-01-prompts-grok36/` (committed **before** `pair`) |
| Generator | GPT-2 + public DeepMind 30 mixin |
| Draws | `--n-samples 4` |
| Length | `--max-new-tokens 128` |
| Seed | `20260905` |
| Output | `experiments/2026-09-01-pair-grok36x4/` |
| Test A | `experiments/2026-09-01-pair-grok12x4/` |
| Test B | `experiments/2026-08-17-pair-12x4/` |

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-grok36 \
  --n-samples 4 --max-new-tokens 128 --seed 20260905 \
  --out-dir experiments/2026-09-01-pair-grok36x4
```

Do not look at key-free LRs until `pair` has written official first-draw
scores and this protocol's analysis commands have been run once, as
written. Do not add families after seeing LRs.

## Analysis commands

Train is always `experiments/2026-09-01-pair-grok36x4`. Do not change
flags after the first run. Do not look at key-free test LRs until each
command has been run once, as written.

Grok-register held-out files (primary new cell):

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-transfer-grok36x4-to-grok12x4-hard-last4

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods poshits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-grok36x4-to-grok12x4-opening-poshits

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-grok36x4-to-grok12x4-opening-rankpath

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods postokhits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-grok36x4-to-grok12x4-occupancy-free

python -m text_watermark_tools openings experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits --skip-stem-curve \
  --out-dir experiments/2026-09-01-openings-grok36x4-to-grok12x4
```

Original 12×4 (scale-up of H-reg-A):

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods poshits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-grok36x4-to-12x4-opening-poshits

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-grok36x4-to-12x4-opening-rankpath

python -m text_watermark_tools probe experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods postokhits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-grok36x4-to-12x4-occupancy-free

python -m text_watermark_tools openings experiments/2026-09-01-pair-grok36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits --skip-stem-curve \
  --out-dir experiments/2026-09-01-openings-grok36x4-to-12x4
```

In-family check (not the isolated headline):

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-grok36x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-probe-grok36x4-hard-last4
```

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4, 36×4, or
  grok12×4.
- Mixing the 36 with grok12, the 100 one-liners, or neighborhood
  paraphrases after seeing LRs.
- Selling prompt ranking, occupancy, `The car`, or a nested Youden as
  replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs. Local Hugging Face GPT-2 only for this freeze.
- Writing `thesis/`.
- Looking at window LRs or `atoms` dumps of the new tables before the
  frozen commands above have been run once.

## Preregistration mechanic

1. Commit this file and the 36 prompt texts in a commit that still
   precedes `pair`.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then the analysis commands above, then append a dated
   logbook entry with the SHA and the nested Youden counts.
4. If a command fails, fix the harness and re-run the **same** flags.
   Do not add a fourth scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results (opened after the frozen commands)

Official first-draw lamp on the new twins is **36/36**. `used_keys=false`
on every key-free path below.

| Split | Lock | Prompt | Nested Youden | t=0 marked |
|---|---|---|---|---|
| grok12×4 | A interpolate | **12/12** | **36/48 vs 39/48** | **39/48 vs 33/48** |
| grok12×4 | B opening poshits | **12/12** | **39/48 vs 45/48** | **39/48 vs 45/48** |
| grok12×4 | C opening rankpath | 11/12 | **37/48 vs 32/48** | **36/48 vs 35/48** |
| grok12×4 | occupancy-free postokhits | **12/12** | **39/48 vs 45/48** | **39/48 vs 45/48** |
| original 12×4 | A interpolate | **10/12** | **26/48 vs 33/48** | **29/48 vs 29/48** |
| original 12×4 | B opening poshits | 7/12 | **10/48 vs 47/48** | **10/48 vs 47/48** |
| original 12×4 | C opening rankpath | 7/12 | **24/48 vs 31/48** | **24/48 vs 33/48** |
| original 12×4 | occupancy-free postokhits | 11/12 | **10/48 vs 47/48** | **10/48 vs 47/48** |

H-scale-A **holds**: lock A nested on the original 12 is **26/48**, above
grok12-train **16/48**. More in-register mass helps that cell. Nested
**26/48 vs 33/48** is not t=0 **25/48**. Occupancy-free on those files
is **10/48**. Do not sell 26/48 or t=0 **29/48**.

H-scale-grok **holds**: lock A nested on grok12×4 is **36/48**, above
100-one-liner xreg **22/48**. Prompt **12/12**. That is still not
**25/48**.

H-scale-B **holds**: occupancy-free t=0 on grok12×4 is **39/48**, equal
to opening coverage **39/48** (exact **21/48**; decided 39 TP / 3 FP,
precision 0.929). On the original 12 it is **10/48**, equal to coverage
**10/48** (exact **8/48**; 1 FP). Isolated observed-token recall is
still train opening-atom overlap. More Grok-length train filled the
channel that 100 one-liners left at **0/48** on grok12. It did not
invent a denser isolated detector.

H-scale-iso **holds**. Do not sell grok12 occupancy-free **39/48**, lock
A nested **36/48**, prompt **12/12**, lock C nested **37/48** (negative
train threshold), or original-12 nested **26/48**. None of those
replaces **25/48**. Isolated-file detection is not finished.

In-family interpolate on the new 36: prompt **35/36**, nested-by-stem
**93/144 vs 110/144**, t=0 **114/144 vs 98/144**, file AUC **0.823**.
Ranking works in-family. That is not **25/48**.

JSON: `experiments/2026-09-01-pair-grok36x4/`,
`experiments/2026-09-01-transfer-grok36x4-to-grok12x4-hard-last4/`,
`experiments/2026-09-01-transfer-grok36x4-to-grok12x4-opening-poshits/`,
`experiments/2026-09-01-transfer-grok36x4-to-grok12x4-opening-rankpath/`,
`experiments/2026-09-01-transfer-grok36x4-to-grok12x4-occupancy-free/`,
`experiments/2026-09-01-openings-grok36x4-to-grok12x4/`,
`experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4/`,
`experiments/2026-09-01-transfer-grok36x4-to-12x4-opening-poshits/`,
`experiments/2026-09-01-transfer-grok36x4-to-12x4-opening-rankpath/`,
`experiments/2026-09-01-transfer-grok36x4-to-12x4-occupancy-free/`,
`experiments/2026-09-01-openings-grok36x4-to-12x4/`,
`experiments/2026-09-01-probe-grok36x4-hard-last4/`.

## Decode (opened after the frozen probes)

Same lock A interpolate tables, decoded with `atoms` (not a new
`probe --methods` name, not `detector_mean`). Frozen commands above
had already been run once.

```bash
python -m text_watermark_tools atoms \
  experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4/tables-counts \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-01-atoms-grok36x4-to-12x4-interpolate

python -m text_watermark_tools atoms \
  experiments/2026-09-01-transfer-grok36x4-to-grok12x4-hard-last4/tables-counts \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-01-atoms-grok36x4-to-grok12x4-interpolate
```

`used_keys=false`. Full traces are not stored (`store_rows=false`).

Original 12×4: marked `lr>0` **29/48**, matching interpolate t=0.
Nested Youden remains **26/48 vs 33/48**. Occupancy-free postokhits
stays **10/48**. Almost all mass is Witten–Bell backoff (0:4 seen 69
vs unseen 219; tail 64:128 seen 137 vs unseen 5996). Window 0:4
marked Δ is +0.496 because unmarked Δ is more negative (−0.337) and
because a few unbucketed body copies fire. Observed-token 0:4 atoms:
library `'Cl' → 'osing'` (n=4), `'The' → ' dog'` (n=4), `'The' →
' bus'` (n=3). Library is a postokhits zero: opening-bucketed
occupancy-free never sees `Closing`. Interpolate tables are unbucketed
full-file last-4, so a grok36 **body** 4-gram can still score a test
opening. That 29-versus-10 gap is not a denser isolated-file detector.

Grok12×4: marked `lr>0` **39/48**, matching occupancy-free **39/48**
and opening coverage **39/48**. Window 0:4 marked Δ is +2.518 vs
unmarked −0.181 (seen 119 vs unseen 169). Observed-token atoms:
`'The' → ' car'` (n=19), `'The' → ' coach'` (n=6), `'The' → ' bus'`
(n=4). The tail is still backoff (64:128 seen 183 vs unseen 5955).
Interpolate nested **36/48** sits slightly *below* occupancy-free
**39/48** because that tail is not a cleaner sign.

Do not sell nested **26/48**, t=0 **29/48**, occupancy-free **39/48**,
`Closing`, or `The car`. H-scale-B still holds: isolated observed-token
recall equals opening-atom overlap. Does not replace **25/48**.
Isolated-file detection is not finished.

JSON: `experiments/2026-09-01-atoms-grok36x4-to-12x4-interpolate/`,
`experiments/2026-09-01-atoms-grok36x4-to-grok12x4-interpolate/`.
