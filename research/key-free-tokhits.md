# Observed-token hits vs Laplace occupancy

The 4-token new-topic isolated-file gate
(`experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-pos1/`,
`--pos-bucket 1`, skip generated token 0) is **12/12** prompt ranking
and **39/48** marked files with `lr > 0`. That 39/48 is **not** 39
independent next-token preferences. Nine of the twelve missed marked
files are **zeros**, not wrong-sign scores. Among files with a non-zero
LR, marked is **39/39** positive on this gate.

`tokhits` / `postokhits` skip a context that never produced the observed
next token on either side of the training tables
(`n_m[token] + n_u[token] < 1`). They keep the same Laplace log-ratio
when the token **was** seen at least once. They do not reconstruct keys.

## Protocol

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits,hits,tokhits \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --fit-prefix 4 --pos-bucket 1 --methods poshits,postokhits \
  --out-dir experiments/2026-08-31-probe-36x4-fitprefix4-postokhits

python -m text_watermark_tools contrast experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --control-dir experiments/2026-08-31-pair-12x4-controlkeys \
  --fit-prefix 4 --pos-bucket 1 \
  --methods hits,tokhits,poshits,postokhits \
  --out-dir experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokhits
```

Fit 24 other 36×4 stems. Score 12×4 files, first 4 generated tokens.
Position bucket 1 prepends `i`. Skip token 0.

Rebuild the atom dump from the persisted poshits tables (no keys):

```python
from pathlib import Path
from text_watermark_tools.atoms import dump_opening_atoms

dump_opening_atoms(
    Path("experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits/tables-poshits"),
    Path("experiments/2026-08-17-pair-12x4"),
    Path("experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits/atoms.json"),
)
```

## Laplace occupancy on shared "The"

At generated index 1 the previous token is often `'The'`. On this
training split the context occupancy is **8 marked vs 52 unmarked**.
Hits still fire when the **context** is shared, even if the next token
never appeared. Unequal occupancy then gives every novel continuation
the same δ:

```
log(α / (8 + αV)) − log(α / (52 + αV)) = 0.330103
```

That one family of atoms accounts for **23 of 39** marked true positives
(The ferry / bus / dog / printer / car / …) **and all 7** unmarked false
positives (The weather / passengers / cat / day / green / line /
drivers). The effect is **anti-occupancy**: marked used “The” *less* in
the training openings, so unseen-after-The looks marked. It is not a
preference for ferry versus weather.

The remaining true positives are observed-token atoms, mainly dialogue
openings actually seen in train: `'"' → 'This'` (δ 3.22) then
`'"This' → ' is'` (δ 4.78), n=9; also `'Oh'`, `'Who'`, `'My'`.

The nine marked zeros are openings with **no** overlapping context at
indices 1–3: `After two and a` (night-bus draw 3), `Closing is the`
(all four library draws), `Now in the second` / `While working on the`
(letter), `Now a little after` (garden). Library is a prompt echo of
“Closing time is announced twice”, not a generic temporal class. Zeros
are abstentions, not sign errors.

Atom counts on this gate: **26** distinct (ctx, next) types; unseen-next
mass **34**, seen-next mass **33**. JSON: `atoms.json` in the transfer
directory.

## Seed length on this split

The 12×4 test seeds are 37–241 words (three long Grok paragraphs, nine
~40-word scenes). The 24 extra 36×4 train seeds are **10–12 word
one-liners**. Out-of-family here is new topics *and* shorter seeds. The
transferable observed-token atoms are quote-dialogue openings that both
seed lengths produce (`'"' → 'This'`). The nine zeros (`After` /
`Closing` / `Now` / `While`) continue the longer test seeds; extra
one-liners almost never open that way (on 36×4 marked files, generated
token 0 is `"` 114 times and `The` 23 times). Covering those zeros needs
train seeds whose continuations share those openings, not more short
one-liners. That is still not a universal detector.

## Medium-length new topics (12×4 long seeds)

Twelve new ~41–51 word scene seeds, four 128-token draws, seed 20260901.
Official lamp **12/12**. Generated token 0 is only `"` (26/48) and `The`
(22/48). Still no After / Closing / Now / While.

```bash
python -m text_watermark_tools pair experiments/2026-08-31-prompts-long12 \
  --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-08-31-pair-long12x4

python -m text_watermark_tools probe experiments/2026-08-31-pair-long12x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods poshits,postokhits \
  --out-dir experiments/2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokhits
```

| Train | postokhits wins | File AUC | marked `lr>0` | decided tp/fp | precision |
|---|---|---|---|---|---|
| 24 short one-liners | **12/12** | 0.694 | **16/48** | 16/0 | **1.000** |
| 12 medium scenes | **12/12** | 0.729 | **19/48** | 19/0 | **1.000** |
| short + medium (36 stems) | **12/12** | 0.739 | **20/48** | 20/0 | **1.000** |

The +3 files on medium-only are all four *market* draws: `'The' → ' dog'`
is actually seen in canal-lock train. Combined train adds rain draw 2
back (20/48). The same nine zeros remain.

Library `Closing is the` continues the seed sentence “Closing time is
announced twice”. Unrelated medium scenes never emit that opening.
Covering those zeros needs train seeds whose *tails* produce the same
first tokens, which is close to training on the same prompt family.

On this medium-seed train, unseen-after-The Laplace **flips sign**
(δ ≈ −0.365). poshits is then **8/12** with **20 marked wrong-sign**
files. Those 20 become postokhits zeros. The 39/48 poshits number on the
short-seed train is occupancy-specific: marked used `The` *less* there.
Equalising seed length does not make occupancy a token preference, and
it does not cover After / Closing / Now / While.

JSON: `experiments/2026-08-31-pair-long12x4/`,
`experiments/2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokhits/`,
`experiments/2026-08-31-transfer-short24-plus-long12-to-12x4-fitprefix4-tokhits/`.

## tokbackoff: shrink last-k until an observed next token hits

Tables already store every suffix length 1..k. `tokbackoff` /
`postokbackoff` try last-k, then last-(k-1), …, last-1, and keep the
longest context that has both-side support **and** the observed next
token. Laplace occupancy is still skipped. This is not stupid backoff
to the unigram, and it is not key recovery.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits,postokbackoff \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokbackoff
```

| Train | postokhits `lr>0` | postokbackoff `lr>0` | extra files | precision |
|---|---|---|---|---|
| 24 short one-liners | **16/48** | **16/48** | none | **1.000** |
| 12 medium scenes | **19/48** | **21/48** | harbour 3 and 4 | **1.000** |
| short + medium | **20/48** | **22/48** | same two harbour draws | **1.000** |

The two extra files open `The ferry was in`. Full last-3 never saw
`in`. Last-1 `' was' → ' in'` at index 3 was seen (2 marked / 0 unmarked
on the medium train). The nine After / Closing / Now / While zeros still
have no observed next token at any shorter order.

In-domain 36×4 LOO: postokbackoff stays **122/144** marked and adds one
unmarked false positive (**131/144** unmarked ≤0 vs postokhits **132/144**).
Control-shuffled-30 stays **0/48** `lr>0` on the short-train gate.

Do **not** sell 21/48 or 22/48 as beating 39/48. tokbackoff is a
coverage knob on observed tokens, not a detector for prompt-idiosyncratic
openings.

JSON: `experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokbackoff/`,
`experiments/2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokbackoff/`,
`experiments/2026-08-31-transfer-short24-plus-long12-to-12x4-fitprefix4-tokbackoff/`,
`experiments/2026-08-31-probe-36x4-fitprefix4-postokbackoff/`,
`experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokbackoff/`.

## Prompt-tail transplant (not new-topic OOD)

Three new bodies with last paragraphs from night-bus, library, letter,
and garden. Official lamp **12/12**. Generated token 0 is mostly `The`
(41/48). **No Closing.** One depot-tail draw is exactly `After two and a`.
One letter-tail draw is `Now a little after`. Transplanting the library
last paragraph did not copy `Closing is the`.

```bash
python -m text_watermark_tools pair experiments/2026-08-31-prompts-tails12 \
  --n-samples 4 --max-new-tokens 128 --seed 20260902 \
  --out-dir experiments/2026-08-31-pair-tails12x4
```

Train those 12, score original 12×4:

| Train | postokhits | postokbackoff | precision |
|---|---|---|---|
| tails only | **10/48** | **23/48** | **1.000** |
| short + medium + tails | **30/48** | **36/48** | **1.000** |

Of the original nine zeros under combined postokhits: night-bus and both
garden files become exact-context hits. Library and letter stay zero at
last-k. Under postokbackoff the four library files score via last-1
`' is' → ' the'` (23 marked / 0 unmarked at index 3 on this train), not
via a Closing opening. Letter `Now in the second` / `While working on
the` remain zeros.

Isolated-file recall is bounded by opening overlap. Tail-matching is
close to in-family for those seeds. It is not a universal detector.
Do not sell 30/48 or 36/48 as beating 39/48. Do not replace 10/12,
29/48, or 36/36.

JSON: `experiments/2026-08-31-pair-tails12x4/`,
`experiments/2026-08-31-transfer-tails12x4-to-12x4-fitprefix4-tokbackoff/`,
`experiments/2026-08-31-transfer-short-medium-tails-to-12x4-fitprefix4-tokbackoff/`.

## Opening-overlap bound and last-2 floor

Isolated observed-token recall **is** train opening-atom overlap:
`lr == 0` iff `n_used == 0`. Exact 4-token copy of a marked train
opening is a lower bound (it does not require both-side last-k support).
`postokbackoff2` (`min_order=2`) refuses generic last-1 English.

```bash
python -m text_watermark_tools openings experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --methods postokhits,postokbackoff,postokbackoff2 \
  --out-dir experiments/2026-08-31-openings-short-medium-tails
```

| Train | postokhits | postokbackoff | postokbackoff2 | last-1 later | decided fp |
|---|---|---|---|---|---|
| 24 short one-liners | **16/48** | **16/48** | **13/48** | 0 | 0 |
| +12 medium scenes | **20/48** | **22/48** | **13/48** | 2 | 0 |
| +12 tail-transplants | **30/48** | **36/48** | **13/48** | 6 | 0 |

The last-2+ core is **13/48** on every train set. Adding medium and
tail seeds does not grow it. The 16→36 lift is last-1: opening
first-transitions at index 1 (`The` → ` dog`, `"` → `This`, `After` →
` two`) plus six later last-1 files (library `' is' → ' the'`, harbour
`' was' → ' in'`). Stem curve: two short stems already cover 13/48;
tails (stems 49–60) carry 22→36.

Unbucketed (`--pos-bucket 0`) tokbackoff still covers **36/48** but adds
**3** unmarked FPs (precision 0.923). Position bucket 1 is the precision
guard.

`--include-first` on postokhits is a first-token unigram: **43/48**
marked, **10** unmarked FP. Remaining zeros are all four `Closing is the`
and `While working on the`. tokbackoff refuses empty last-k, so
include-first does not change 36/48.

The leftover twelve postokbackoff zeros are coverage holes, not sign
errors: `The ferry was so/over/waiting`, `The printer worked`, one
station non-quote, `Now in the second`, `While working on the`. `'Now'`
at index 1 has both-side support (4/4) but never continues `' in'`
(train saw `' a little after'`). That is still not a universal detector.

Do **not** sell 13/48, 36/48, 42/48, or 43/48 as beating 39/48. Do not replace
10/12, 29/48, or 36/36.

JSON: `experiments/2026-08-31-openings-short-medium-tails/`,
`experiments/2026-08-31-openings-short-medium-tails-unbucketed/`,
`experiments/2026-08-31-openings-short-medium-tails-includefirst/`.

## Neighborhood paraphrases (not last-paragraph glue)

Twelve new ~40–55 word scenes in the leftover-zero neighborhoods
(letter, library closing, ferry/harbour, office, station). Official lamp
**12/12**. Generated token 0 is `The` or quote-dialogue. **No Closing /
Now / While / After / The ferry / The printer.**

```bash
python -m text_watermark_tools pair experiments/2026-08-31-prompts-family12 \
  --n-samples 4 --max-new-tokens 128 --seed 20260903 \
  --out-dir experiments/2026-08-31-pair-family12x4

python -m text_watermark_tools openings experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --extra-train experiments/2026-08-31-pair-family12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-openings-short-medium-tails-family
```

| Train | postokhits | postokbackoff | postokbackoff2 | exact 4-token |
|---|---|---|---|---|
| short+medium+tails | **30/48** | **36/48** | **13/48** | 19/48 |
| +12 neighborhood | **38/48** | **42/48** | **15/48** | 19/48 |

Precision **1.000**. The +6 postokbackoff files are ferry
`was so/over/waiting` via last-1 `' was' → …`, not a copied 4-gram.
Letter `Now in the second` / `While working on the`, library
`Closing is the` (last-k), and `The printer worked` stay zeros.
Neighborhood is not those openings. The last-2+ core barely moves
(13→15). Still not a universal detector.

JSON: `experiments/2026-08-31-pair-family12x4/`,
`experiments/2026-08-31-openings-short-medium-tails-family/`.

## Frozen result (24 other 36×4 stems → 12×4)

| Method | Prompt wins | File AUC | marked `lr>0` | unmarked `lr≤0` | zeros M/U | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|---|---|---|
| poshits | **12/12** | **0.873** | **39/48** | **41/48** | 9/33 | 39/0 | 7/8 | 0.848 |
| **postokhits** | **12/12** | 0.694 | **16/48** | **48/48** | 32/44 | **16/0** | **0/4** | **1.000** |
| hits | 11/12 | 0.820 | 39/48 | 33/48 | 9/22 | 39/0 | 15/11 | 0.722 |
| tokhits | 11/12 | 0.674 | 16/48 | 45/48 | 32/39 | 16/0 | 3/6 | 0.842 |

`postokhits` among decided files is **perfect** on this gate
(16 TP, 0 FN, 0 FP, 4 TN). Prompt ranking stays **12/12**. Isolated
`lr>0` drops to **16/48** because The-Laplace true positives become
zeros. Nested Youden: 16/48 vs 48/48, spec **1.000**.

Do **not** sell 16/48 as beating 39/48. Quote both: 39/48 includes
occupancy Laplace; 16/48 is observed next-token only, precision 1.0 on
this gate. The 29/48 last-4 isolated-file headline is unchanged.

## In-domain 36×4 LOO

`--fit-prefix 4 --pos-bucket 1`, 36×4 leave-one-file-out, same opening
window:

| Method | Prompt wins | File AUC | marked `lr>0` | unmarked `lr≤0` | zeros M/U | decided tp/fn | decided fp |
|---|---|---|---|---|---|---|---|
| poshits | 34/36 | 0.935 | **131/144** | **132/144** | 8/89 | 131/5 | 12 |
| postokhits | 34/36 | 0.912 | **122/144** | **132/144** | 19/105 | 122/3 | 12 |

Only **9 of 131** in-domain poshits true positives were occupancy
Laplace. The extra true positives versus the OOD 16/48 are observed
continuations of repeated 36×4 topics, not The-ferry. The 12 unmarked
false positives stay after tokhits: they are observed-token errors, not
occupancy. Nested-by-stem Youden: poshits 121/144 vs 132/144;
postokhits 121/144 vs 139/144.

## Instance contrast

Same 4-token tables, `control-shuffled-30` openings
([key-free-contrast.md](key-free-contrast.md)):

| Method | control `lr>0` | public vs control |
|---|---|---|
| poshits | **0/48** | **12/12**, AUC **0.906** |
| postokhits | **0/48** | **12/12**, AUC 0.667 |

The 16 observed-token true positives are still this public instance.
Control files never get `lr > 0`. Public-vs-control AUC drops because
32 marked zeros tie with control zeros; quote **0/48**, not the 12/12
control-vs-unmarked prompt-mean artifact (zeros beating negative
unmarked LRs).

## What this is not

- Not a universal calibrated detector.
- Not key recovery. Tokhits only gates Laplace on next-token occupancy.
- Not a claim that 16/48–36/48 isolated-file is the headline. 39/48
  remains the short-train poshits number; it flips when train occupancy
  of `The` flips. tokhits explains it. tokbackoff and tail-matching raise
  observed-token recall; they do not make a universal detector.
  `postokbackoff2` shows the last-2+ core is **13/48** on every train
  set in that curve. Unbucketed last-1 and `--include-first` unigrams
  raise recall only by spending precision.
- Covering an opening is not the same as `lr>0`. On the 60-stem
  combined train, postokbackoff covers **42/48** and marks **34/48**;
  eight covered files have a negative observed-token LR. Precision
  among decided files stays 1.0 (no unmarked FP). See
  [key-free-cascade.md](key-free-cascade.md).
- Unmarked-LM opening geometry (4 generated tokens, no prompt) is
  stronger in-domain than the published 128-token pivot (27/48 vs
  17/48) and does **not** transfer as a calibrated OOD isolated-file
  reader. Prompt-conditioned geometry is worse than chance under
  leave-one-prompt-out. Cascade is two channels, not one score.
  `indicate score` prints `decision=ABSTAIN` when `n_used=0`.
- Not a replacement of **10/12**, **29/48**, or **36/36**.
