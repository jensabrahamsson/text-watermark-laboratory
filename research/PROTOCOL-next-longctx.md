# Confirmatory protocol (longer watermark history)

This is a **methods freeze** for Sol’s 260903 next experiment: one
preregistered two-grain replication on a **materially longer**
watermark hash history, locked **before** generation. It does not add
a `probe --methods` name. It does not edit the `synthid-text`
checkout. The public instance stays `public-deepmind-30` keys; only
`ngram_len` changes.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Absolute-history 12-LOO mask-*k*
is a separate honesty remasure
([PROTOCOL-isolated-mask-absolute.md](PROTOCOL-isolated-mask-absolute.md)).
Do **not** write `thesis/` from this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.

## Why freeze now

The public mixin uses `ngram_len=5`, hence watermark hash history
$\Hw=4$. Count-table reuse on last-4 contexts is then the same length
as the keyed hash window. Group ranking **36/36** / **99/100** /
**9/12** versus isolated **47/96** is a property of that short-context
instance until a longer history is measured.

Sol (2026-09-03) asked that the next external-validity test be
preregistered: same two-grain protocol, either a longer watermark
context or a structurally different local mixin, locked before
generation. A different mixin (Kirchenbauer green-list, Aaronson
Gumbel, …) would be a second freeze and is **not** this file. This
file only lengthens SynthID hash history.

A finished 100×4 corpus is not required for the freeze to hold. Phase A
is the original 12 prompt strings with new twins. Phase B (100 new
families, same `ngram_len`) is named but not opened here.

## Primary scientific question

On GPT-2 with public keys and `ngram_len=13` ($\Hw=12$), under
leave-one-family-out interpolate last-4 and hard last-4, do marked
prompt-group means still outrank unmarked means, and does the
prespecified isolated $\tau=0$ confusion matrix remain chance-like?

Not: can another table classify the old `ngram_len=5` 12×4 files.
Not: leftover targeting. Not: a new scorer name.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `gpt2` (Hugging Face id; Hub revision was not pinned on earlier corpora; do not change the id) |
| Mixin keys | public-deepmind-30 (default) |
| `ngram_len` | **13** (watermark history $\Hw=12$; three times public $\Hw=4$) |
| Prompts | `experiments/2026-08-17-grok-prompts/` (original 12 Grok scene strings; new twins) |
| Draws | `--n-samples 4` |
| Length | `--max-new-tokens 128` |
| Seed | `20260903` |
| Pair out-dir | `experiments/2026-09-03-pair-12x4-ngram13/` |
| Fold | leave-one-family-out (Algorithm 1 in the technical report) |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-03-probe-12x4-ngram13-hard-last4/` |
| Zero / abstention | $n=0\Rightarrow\Lambda=0$; report coverage / `n_used` |
| Primary group metric | $D_p$ sign count: `n_prompts_marked_above` / 12, strict `>` |
| Primary isolated metric | $\tau=0$ confusion matrix, balanced accuracy, file AUC |
| Occupancy | `atoms` on the interpolate tables after probe; mechanistic intermediate |
| Official control | `score` / pair first-draw with **matching** `ngram_len=13` |

`pair --ngram-len 13` must generate **and** official-score with the
same `ngram_len`. Scoring `ngram_len=13` text with the public
`ngram_len=5` processor is a harness bug, not a scientific miss.

No new method names. Hard and interpolate last-4 are the published
readers. Do not add poshits, rankpath, hashtok, or cascades after
peeking.

## Hypotheses (stated before generation)

- **H-long-ctrl.** Official first-draw mean with matching
  `ngram_len=13` is above $0.55$ on every first marked file (mixin
  on). Unmarked first-draw stays near $1/2$. If this fails, stop and
  fix the harness; do not interpret key-free LRs.
- **H-long-group.** Interpolate last-4 12-LOO prompt ranking is the
  primary group endpoint. If short reusable $\Hw=4$ is necessary for
  this reader, ranking is **below** the public-mixin diagnostic
  **9/12**. If it stays **≥9/12**, short $\Hw$ is not necessary on
  this 12-family frame. Either outcome is informative. It does not
  replace **25/48**.
- **H-long-hard.** Hard last-4 12-LOO ranking is reported beside
  interpolate. Same refuse-to-sell.
- **H-long-iso.** Isolated $\tau=0$ confusion matrix (TP, FN, TN, FP;
  sensitivity; specificity; balanced accuracy; AUC) does not replace
  **25/48**. Coverage when `n_used=0` is reported separately, not
  counted as a confident negative without saying so.
- **H-long-occ.** Exact last-4 occupancy (`atoms` seen vs unseen) is
  logged. Lower exact overlap than public $\Hw=4$ in-domain is the
  expected mechanistic direction; it is not a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --n-samples 4 --max-new-tokens 128 --seed 20260903 --ngram-len 13 \
  --out-dir experiments/2026-09-03-pair-12x4-ngram13
```

Do not look at key-free LRs until `pair` has written official
first-draw scores and this protocol’s analysis command has been run
once, as written. Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-03-probe-12x4-ngram13-hard-last4
```

`used_keys=false`. After that dump exists, occupancy (not a second
freeze; same tables):

```bash
python -m text_watermark_tools atoms \
  experiments/2026-09-03-probe-12x4-ngram13-hard-last4/tables-counts \
  --test-dir experiments/2026-09-03-pair-12x4-ngram13 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-03-atoms-12x4-ngram13
```

If `tables-counts` was dropped from the probe out-dir, persist it
once with the same fit flags; do not add a method.

## Phase B (named)

Same `ngram_len=13`, GPT-2, `--n-samples 4`, $T=128$, seed
`20260903`, prompts `experiments/2026-09-01-prompts-100/`. Same
readers. Same two grains. Phase A is checked in. LOGBOOK names the
Phase B start before generation.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --n-samples 4 --max-new-tokens 128 --seed 20260903 --ngram-len 13 \
  --out-dir experiments/2026-09-03-pair-100x4-ngram13

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-03-probe-100x4-ngram13-hard-last4
```

Do not look at these 100×4 key-free LRs until that logbook line exists
and both commands have been run once, as written. A finished 100×4
corpus is not required for the freeze to hold; it is the n=100
readout of the same lock.

## What this protocol refuses

- Editing the `synthid-text` checkout.
- A Kirchenbauer / Aaronson / other-mixin generator in this file.
- New hashed / backoff / cascade / learned scorers on 12×4 or the
  new twins.
- Fishing `--ngram-len` after looking at LRs.
- Leftover targeting, occupancy-free leftover unions, Distil ∪ SMT.
- Selling any ngram-13 count as replacing **25/48**.
- Scoring ngram-13 twins with the public `ngram_len=5` processor
  and calling that the official control.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file (and the `--ngram-len` CLI it names) in a commit
   that still precedes `pair`.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then the probe command, then append a dated logbook
   entry with the SHA and the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.
   Do not add a scorer.

Human merge of PR #4 is out of scope for this file.

## Results

Protocol SHA `b70986d`. Named `7ec4509`. Pair seed **20260903**.
`ngram_len=13`. `used_keys=false` on the key-free probe.

Pair dump: [experiments/2026-09-03-pair-12x4-ngram13/](../experiments/2026-09-03-pair-12x4-ngram13/).
Probe dump: [experiments/2026-09-03-probe-12x4-ngram13-hard-last4/](../experiments/2026-09-03-probe-12x4-ngram13-hard-last4/).

H-long-ctrl **holds**. Official first-draw mean with matching
`ngram_len=13` is above $0.55$ on all 12 first marked files
(range $0.601$–$0.634$). Unmarked first-draw stays near $1/2$
($0.471$–$0.508$). Mixin is on. `n_unmasked_ngrams=116` on every
128-token twin (`ngram_len=13`). Post-open extra-draw check, using
the shipped `official_score_text` on the committed files: **48/48**
marked above $0.55$ (min $0.599$), **0/48** unmarked above $0.55$
(max $0.523$). Not a second freeze.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **6/12** | 0.541 | 20/48 | 31/48 | 20 28 31 17 | **51/96** |
| hard last-4 | **6/12** | 0.544 | 22/48 | 30/48 | 22 26 30 18 | **52/96** |

Public-mixin diagnostic on these prompt *strings* (different twins,
`ngram_len=5`) was hard **9/12**, isolated **25/48 vs 22/48**, AUC
**0.590**. That is not a matched-seed pair.

Clopper–Pearson 95% (invert `binomial_sf`; not a second freeze):

| Count | Interval | Includes ½? |
|---|---|---|
| ngram-13 interpolate **6/12** | **[0.211, 0.789]** | yes |
| ngram-13 hard **6/12** | **[0.211, 0.789]** | yes |
| ngram-13 hard t=0 **22/48** | **[0.314, 0.608]** | yes |
| ngram-13 hard BA **52/96** | **[0.437, 0.644]** | yes |
| Isolated **25/48** | **[0.372, 0.667]** | yes |

H-long-group **holds**. Interpolate last-4 12-LOO prompt ranking is
**6/12**, below the public-mixin diagnostic **9/12**. Short $\Hw=4$
is not shown to be unnecessary on this 12-family frame. The
Clopper–Pearson interval includes ½. n=12 is small. Mean paired
file difference is $0.021$ (interpolate) / $0.009$ (hard).
Interpolate `prompt_sign_p` is $0.247$ (2000 shuffles); hard is
$0.294$. Phase B is the n=100 readout.

H-long-hard **holds** as a companion readout: hard is also **6/12**.

H-long-iso **holds**. Isolated $\tau=0$ is chance-like (hard 22/48
sensitivity, 30/48 specificity, **52/96** balanced accuracy, AUC
**0.544**). Nested Youden 24/48 vs 21/48 is post hoc. Do not sell
**6/12**, **22/48**, **52/96**, or nested 24/48 as replacing
**25/48**. Official first-draw **12/12** uses keys.

H-long-occ is **not opened**. Probe dropped `tables-counts` (same as
other 12-LOO dumps). A single pooled fit would leak the held-out
family. Occupancy remains a mechanistic intermediate for a later
LOO-aware decode. Do not invent unseen/seen counts.

Isolated-file detection is still not finished. Do not write `thesis/`.

## Phase B results

Named `facc538` before generation. Pair seed **20260903**.
`ngram_len=13`. `used_keys=false`.

Pair dump: [experiments/2026-09-03-pair-100x4-ngram13/](../experiments/2026-09-03-pair-100x4-ngram13/).
Probe dump: [experiments/2026-09-03-probe-100x4-ngram13-hard-last4/](../experiments/2026-09-03-probe-100x4-ngram13-hard-last4/).

H-long-B-ctrl **holds**. Official first-draw matching `ngram_len=13`
is above $0.55$ on **100/100** first marked files (min $0.582$).
Unmarked first-draw: **0/100** above $0.55$ (max $0.519$). Post-open
extra-draw check: **400/400** marked above $0.55$ (min $0.574$),
**0/400** unmarked above $0.55$ (max $0.525$). Not a second freeze.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **76/100** | 0.666 | 267/400 | 222/400 | 267 133 222 178 | **489/800** |
| hard last-4 | **66/100** | 0.579 | 215/400 | 221/400 | 215 185 221 179 | **436/800** |

Public-mixin lock A interpolate on these prompt *strings* (different
twins, `ngram_len=5`) was **99/100**.

Clopper–Pearson 95% (invert `binomial_sf`; not a second freeze):

| Count | Interval | Includes ½? |
|---|---|---|
| ngram-13 interpolate **76/100** | **[0.664, 0.840]** | no |
| ngram-13 hard **66/100** | **[0.558, 0.752]** | no |
| ngram-13 interpolate t=0 **267/400** | **[0.619, 0.714]** | no |
| ngram-13 interpolate BA **489/800** | **[0.576, 0.645]** | no |
| Isolated **25/48** | **[0.372, 0.667]** | yes |

H-long-B-group **holds**. Interpolate last-4 100-LOO ranking is
**76/100**, below public-mixin lock A **99/100**. It is not chance
on this n=100 one-liner set. Phase A **6/12** was small-n; Phase B
shows attenuation, not collapse. Mean paired file difference is
$0.156$ (interpolate) / $0.027$ (hard). Interpolate
`prompt_sign_p` is $0.00050$ (2000 prompt-mean sign shuffles). Do **not** sell **76/100** as
replacing **99/100** or **25/48**.

H-long-B-iso **does not hold as “chance-like vs 47/96”** on this
corpus: interpolate isolated BA is **489/800** (AUC **0.666**), a
different register and $n$ from the original 12. Hard isolated BA is
**436/800** (AUC **0.579**). Neither is the prespecified original-12
matrix. Do not sell **267/400**, **489/800**, or **76/100** as
replacing **25/48**. Nested Youden is post hoc.

Isolated-file detection is still not finished. Do not write `thesis/`.
