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
as above. Same readers. Same two grains. Named, not opened here.
LOGBOOK names the start before generation.

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

Not opened. Do not fill this section before the frozen commands have
been run once, as written.
