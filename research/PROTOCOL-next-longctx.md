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

## Phase B (named, not opened)

Same `ngram_len=13`, GPT-2, `--n-samples 4`, $T=128$, seed
`20260903`, prompts `experiments/2026-09-01-prompts-100/`. Same
readers. Same two grains. Do **not** generate Phase B until Phase A
is checked in and a later logbook line names a Phase B start. A
finished 100×4 corpus is not required for this freeze to hold.

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

*(empty until the SHA is named in LOGBOOK.md)*
