# Confirmatory protocol (Kirchenbauer green-list mixin)

This is a **methods freeze** for Sol’s 260903 other external-validity
arm: one preregistered two-grain replication on a **structurally
different local mixin**, locked **before** generation. It does not add
a `probe --methods` name. It does not edit the `synthid-text`
checkout. Longer SynthID hash history is a different freeze
([PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md)) and is already
opened. This file is **not** that measurement.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from
this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
z-scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score Kirchenbauer twins with SynthID `detector_mean` and
call that the official control.

## Why freeze now

Sol (2026-09-03) asked that the next external-validity test be
preregistered: same two-grain protocol, either a longer watermark
context or a structurally different local mixin, locked before
generation. `ngram_len=13` ($\Hw=12$) is the longer-context arm.
This file is the different-mixin arm.

The construction is Kirchenbauer et al. (2023) green-list bias, as
shipped in `transformers==4.57.6`
(`WatermarkLogitsProcessor` / `WatermarkDetector`). Defaults are
frozen, not tuned to last-4 tables: `greenlist_ratio=0.25`,
`bias=2.0`, `hashing_key=15485863` (Hugging Face’s public default, the
millionth prime; not a laboratory secret), `seeding_scheme=lefthash`,
`context_width=1`. Official control is the matching z-test
(`z_threshold=3.0`). This is **not** a longer-context test:
`context_width=1` is shorter than public SynthID $\Hw=4`. Do not sell
it as $\Hw=12$. An Aaronson–Kirchner Gumbel mixin is a third freeze
and is **not** this file.

A finished 100×4 corpus is not required for the freeze to hold. The
original 12 prompt strings with new twins are the first readout. One
hundred families (same mixin defaults) are named but not opened here.

## Primary scientific question

On GPT-2 with Hugging Face default Kirchenbauer watermarking, under
leave-one-family-out interpolate last-4 and hard last-4, do marked
prompt-group means still outrank unmarked means, and does the
prespecified isolated $\tau=0$ confusion matrix remain chance-like?

Not: can another table classify the old `public-deepmind-30` 12×4
files. Not: leftover targeting. Not: a new scorer name. Not: is
Kirchenbauer a longer hash history.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `gpt2` (pin Hub SHA `607a30d783dfa663caf39e06633721c8d4cfcd7e`) |
| Mixin | Hugging Face `WatermarkLogitsProcessor` (Kirchenbauer et al. 2023) |
| `greenlist_ratio` | **0.25** |
| `bias` | **2.0** |
| `hashing_key` | **15485863** |
| `seeding_scheme` | **lefthash** |
| `context_width` | **1** |
| Sampling | temperature 1.0, top-$K$ 40, `min_new_tokens=max_new_tokens` (same as the SynthID path) |
| Official control | `transformers.WatermarkDetector`, matching config, `z_threshold=3.0` |
| Prompts | `experiments/2026-08-17-grok-prompts/` (original 12 scene strings; new twins) |
| Draws | `--n-samples 4` |
| Length | `--max-new-tokens 128` |
| Seed | `20260904` |
| Pair out-dir | `experiments/2026-09-03-pair-12x4-kgw/` |
| Fold | leave-one-family-out (Algorithm 1 in the technical report) |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-03-probe-12x4-kgw-hard-last4/` |
| Zero / abstention | $n=0\Rightarrow\Lambda=0$; report coverage / `n_used` |
| Primary group metric | $D_p$ sign count: `n_prompts_marked_above` / 12, strict `>` |
| Primary isolated metric | $\tau=0$ confusion matrix, balanced accuracy, file AUC |
| Occupancy | `atoms --leave-one-out` on the interpolate tables after probe; mechanistic intermediate |

`pair --mixin kgw` must generate **and** official-score with the
Kirchenbauer detector. Scoring those twins with SynthID
`detector_mean` is a harness bug, not a scientific miss.
`--ngram-len` is SynthID-only. `--also-control-keys` and
`--control-only` are SynthID-only.

No new method names. Hard and interpolate last-4 are the published
readers. Do not add poshits, rankpath, hashtok, or cascades after
peeking.

## Hypotheses (stated before generation)

- **H-kgw-ctrl.** Official matching z-score is above $3.0$ on every
  first marked file (mixin on). Unmarked first-draw is not all above
  $3.0$ (expected near $0$). If marked first-draws fail this, stop and
  fix the harness; do not interpret key-free LRs.
- **H-kgw-group.** Interpolate last-4 12-LOO prompt ranking is the
  primary group endpoint. If the published SynthID tournament footprint
  is necessary for this reader, ranking is **below** the public-mixin
  diagnostic **9/12**. If it stays **≥9/12**, the count-table signal is
  not unique to tournament sampling on this 12-family frame. Either
  outcome is informative. It does not replace **25/48**.
- **H-kgw-hard.** Hard last-4 12-LOO ranking is reported beside
  interpolate. Same refuse-to-sell.
- **H-kgw-iso.** Isolated $\tau=0$ confusion matrix (TP, FN, TN, FP;
  sensitivity; specificity; balanced accuracy; AUC) does not replace
  **25/48**. Coverage when `n_used=0` is reported separately.
- **H-kgw-occ.** Exact last-4 occupancy (`atoms` seen vs unseen) is
  logged. This mixin’s hash window is one previous token, not
  $\Hw=4$ or $\Hw=12$. Occupancy is a mechanistic intermediate, not a
  detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --n-samples 4 --max-new-tokens 128 --seed 20260904 --mixin kgw \
  --hub-revision 607a30d783dfa663caf39e06633721c8d4cfcd7e \
  --out-dir experiments/2026-09-03-pair-12x4-kgw
```

Do not look at key-free LRs until `pair` has written official
first-draw z-scores and this protocol’s analysis command has been run
once, as written. Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-03-probe-12x4-kgw-hard-last4
```

`used_keys=false`. After that dump exists, occupancy (not a second
freeze; same interpolate reader):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-09-03-pair-12x4-kgw \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-03-atoms-12x4-kgw
```

## One hundred families (named)

Same mixin defaults, GPT-2, `--n-samples 4`, $T=128$, seed
`20260904`, prompts `experiments/2026-09-01-prompts-100/`, Hub SHA
as above. Same readers. Same two grains. Named here before generation.
Opened below. LOGBOOK names the start before generation.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --n-samples 4 --max-new-tokens 128 --seed 20260904 --mixin kgw \
  --hub-revision 607a30d783dfa663caf39e06633721c8d4cfcd7e \
  --out-dir experiments/2026-09-03-pair-100x4-kgw

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-03-probe-100x4-kgw-hard-last4
```

A finished 100×4 corpus is not required for the freeze to hold.

## What this protocol refuses

- Editing the `synthid-text` checkout.
- An Aaronson / other-mixin generator in this file.
- Hugging Face `selfhash`, a fished `bias`, or `context_width` matched
  to last-4 after peeking.
- Scoring Kirchenbauer twins with SynthID `detector_mean` as the
  official control.
- Combining `--mixin kgw` with `--ngram-len` other than the unused
  SynthID default, `--also-control-keys`, or `--control-only`.
- New hashed / backoff / cascade / learned scorers on 12×4 or the
  new twins.
- Leftover targeting, occupancy-free leftover unions, Distil ∪ SMT.
- Selling any Kirchenbauer count as replacing **25/48**.
- Selling this freeze as the $\Hw=12$ experiment.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file (and the `--mixin kgw` CLI it names) in a commit
   that still precedes `pair`.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then the probe command, then append a dated logbook
   entry with the SHA and the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.
   Do not add a scorer.

Human merge of PR #4 is out of scope for this file.

## Results

Protocol SHA `8371406`. Named `09e40d4`. Pair seed **20260904**.
`mixin=kgw`. `used_keys=false` on the key-free probe. Hub revision
`607a30d783dfa663caf39e06633721c8d4cfcd7e`.

Pair dump: [experiments/2026-09-03-pair-12x4-kgw/](../experiments/2026-09-03-pair-12x4-kgw/).
Probe dump: [experiments/2026-09-03-probe-12x4-kgw-hard-last4/](../experiments/2026-09-03-probe-12x4-kgw-hard-last4/).

H-kgw-ctrl **holds**. Official matching z-score is above $3.0$ on all
12 first marked files (min $8.45$). Unmarked first-draw is **0/12**
above $3.0$ (max $2.10$). Mixin is on. Post-open extra-draw check,
using the shipped `kgw_score_text` on the committed files: **48/48**
marked above $3.0$ (min $7.22$), **2/48** unmarked above $3.0$
(night-bus draw 2 $z=3.13$; rain draw 4 $z=3.53$). Not a second freeze.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **12/12** | 0.947 | 44/48 | 41/48 | 44 4 41 7 | **85/96** |
| hard last-4 | **12/12** | 0.703 | 35/48 | 25/48 | 35 13 25 23 | **60/96** |

Public-mixin diagnostic on these prompt *strings* (different twins,
`ngram_len=5`) was hard **9/12**, isolated **25/48 vs 22/48**, AUC
**0.590**. That is not a matched-seed pair and not this mixin.

Clopper–Pearson 95% (invert `binomial_sf`; not a second freeze):

| Count | Interval | Includes ½? |
|---|---|---|
| kgw interpolate **12/12** | **[0.735, 1.000]** | no |
| kgw interpolate t=0 **44/48** | **[0.800, 0.977]** | no |
| kgw interpolate BA **85/96** | **[0.804, 0.941]** | no |
| kgw hard t=0 **35/48** | **[0.582, 0.847]** | no |
| Isolated **25/48** | **[0.372, 0.667]** | yes |

H-kgw-group **holds** as the $\ge$**9/12** branch. Interpolate last-4
12-LOO prompt ranking is **12/12** (clustered permutation
$p\approx 0.0005$; mean $D_p=0.437$). Short tournament $\Hw=4$ is not
shown to be necessary for this reader on this 12-family frame.
`context_width=1` is shorter than public $\Hw=4$. It does not replace
**25/48**.

H-kgw-hard **holds** as a companion readout: hard is also **12/12**
(AUC **0.703**; mean paired difference $0.070$).

H-kgw-iso **holds**. Isolated $\tau=0$ on these Kirchenbauer twins is
not the original-12 SynthID matrix. Interpolate is 44 TP, 4 FN, 41 TN,
7 FP (**85/96**); hard is **60/96**. Nested Youden interpolate
42/48 vs 42/48 is post hoc. Do not sell **12/12**, **44/48**,
**85/96**, **35/48**, or **60/96** as replacing **25/48**. Official
**48/48** uses the matching z-test.

H-kgw-occ **holds**. Leave-one-family-out interpolate atoms
(`atoms --leave-one-out`; `used_keys=false`). File LRs match interpolate
holdout file-by-file (marked `lr>0` **44/48**). Exact next-token overlap
on the Kirchenbauer twins is **114** seen vs **12071** unseen
(Witten–Bell backoff). Public $\Hw=4$ original-12 twins (same prompt
strings, different generation): **269** seen vs **11912** unseen.
Opening $[0{:}4)$ is 40 seen vs 248 unseen. Interpolate ranking
**12/12** is not an exact last-4 copy detector. Occupancy is a
mechanistic intermediate, not a detector. Do not sell **114**, **40**,
or `'I' → ' walked'` as replacing **25/48**.

JSON: [experiments/2026-09-03-atoms-12x4-kgw/](../experiments/2026-09-03-atoms-12x4-kgw/).

Isolated-file detection on the public SynthID original-12 remains
**25/48** / **47/96**. The 100-family readout follows. Do not write
`thesis/`.

## One hundred families (opened)

Named `8f09aa6` before generation. Pair seed **20260904**. `mixin=kgw`.
`used_keys=false`. Hub SHA `607a30d783dfa663caf39e06633721c8d4cfcd7e`.

Pair dump: [experiments/2026-09-03-pair-100x4-kgw/](../experiments/2026-09-03-pair-100x4-kgw/).
Probe dump: [experiments/2026-09-03-probe-100x4-kgw-hard-last4/](../experiments/2026-09-03-probe-100x4-kgw-hard-last4/).

H-kgw-B-ctrl **holds**. Official first-draw matching z-score is above
$3.0$ on **100/100** first marked files (min $6.61$). Unmarked
first-draw: **1/100** above $3.0$ (max $3.13$). Mixin is on.
Post-open extra-draw check: **400/400** marked above $3.0$ (min
$3.53$), **5/400** unmarked above $3.0$ (max $5.45$). Not a second
freeze.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **100/100** | 0.982 | 376/400 | 371/400 | 376 24 371 29 | **747/800** |
| hard last-4 | **62/100** | 0.573 | 209/400 | 231/400 | 209 191 231 169 | **440/800** |

Public-mixin lock A interpolate on these prompt *strings* (different
twins, `ngram_len=5`) was **99/100**. Kirchenbauer interpolate
**100/100** is a different construction. Mean $D_p=0.745$ (median
$0.759$; every family $D_p>0$). Hard mean paired difference is $0.030$.

Clopper–Pearson 95% (invert `binomial_sf`; not a second freeze):

| Count | Interval | Includes ½? |
|---|---|---|
| kgw interpolate **100/100** | **[0.964, 1.000]** | no |
| kgw interpolate BA **747/800** | **[0.914, 0.950]** | no |
| kgw hard **62/100** | **[0.517, 0.715]** | no |
| Isolated **25/48** | **[0.372, 0.667]** | yes |

H-kgw-B-group **holds** as a report. Interpolate last-4 100-LOO ranking
is **100/100** (clustered permutation $p\approx 0.0005$). It does not
replace lock A **99/100** (different mixin) or isolated **25/48**.
`context_width=1` is shorter than public $\Hw=4$.

H-kgw-B-iso **holds**. Isolated interpolate **747/800** (AUC **0.982**)
is a different corpus and mixin from the original-12 SynthID
**47/96**. Hard isolated **440/800** (AUC **0.573**) is near chance at
file grain. Nested Youden interpolate 368/400 vs 379/400 is post hoc.
Do not sell **100/100**, **376/400**, **747/800**, **62/100**, or
**440/800** as replacing **25/48**. Official **100/100** uses the
matching z-test.

H-kgw-occ on this frame: leave-one-family-out interpolate atoms
(`used_keys=false`). File LRs match interpolate holdout (marked
`lr>0` **376/400**). Exact next-token overlap is **4557** seen vs
**96991** unseen. Public $\Hw=4$ 100-family was **10158** seen;
$\Hw=12$ was **5878** seen. Opening $[0{:}4)$ is 1044 seen vs 1356
unseen. Interpolate **100/100** is not an exact last-4 copy detector.
Do not sell **4557**, **1044**, or `'They' → ' were'` as replacing
**25/48**.

JSON: [experiments/2026-09-03-atoms-100x4-kgw/](../experiments/2026-09-03-atoms-100x4-kgw/).

Isolated-file detection on the public SynthID original-12 remains
**25/48** / **47/96**. Do not write `thesis/`.
