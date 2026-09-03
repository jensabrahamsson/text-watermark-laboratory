# Confirmatory protocol (Aaronson–Kirchner exponential-minimum mixin)

This is a **methods freeze** for the third structurally different local
mixin named in [PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md) and
[PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md). It does not add a
`probe --methods` name. It does not edit the `synthid-text` checkout.
`transformers==4.57.6` has no Aaronson logits processor; the sampler
lives in this repository (`src/text_watermark_tools/aaronson.py`).
Longer SynthID hash history and Kirchenbauer green-list are different
freezes and are already opened. This file is **not** those
measurements.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from
this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
z-scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score Aaronson twins with SynthID `detector_mean` or
Kirchenbauer `WatermarkDetector` and call that the official control.

## Why freeze now

Sol (2026-09-03) asked that the next external-validity test be
preregistered: same two-grain protocol, either a longer watermark
context or a structurally different local mixin. Kirchenbauer is
opened. The remaining named different-mixin arm is Aaronson and
Kirchner (2023) exponential-minimum sampling (talk slides; not a
peer-reviewed article). The construction is distortion-free in the
exponential-minimum sense: keyed uniforms \(r_v\sim\mathrm{Unif}(0,1)\)
and model probabilities \(p_v\) pick

\[
v^\star=\arg\max_v r_v^{1/p_v}
\]

after the same temperature \(1.0\) / top-\(K=40\) filter as the public
SynthID path. Official control is a z-test on the mean of those
observed \(r\) values against \(\mathrm{Unif}(0,1)\) (mean \(1/2\),
variance \(1/12\)). This is **not** a longer-context test:
`context_width=1` is shorter than public SynthID \(\Hw=4\). Do not
sell it as \(\Hw=12\). Do not sell it as Kirchenbauer.

A finished 100×4 corpus is not required for the freeze to hold. The
original 12 prompt strings with new twins are the first readout. One
hundred families (same mixin defaults) are named but not opened here.

## Primary scientific question

On GPT-2 with this frozen Aaronson–Kirchner exponential-minimum
instance, under leave-one-family-out interpolate last-4 and hard
last-4, do marked prompt-group means still outrank unmarked means, and
does the prespecified isolated \(\tau=0\) confusion matrix remain
chance-like?

Not: can another table classify the old `public-deepmind-30` 12×4
files. Not: leftover targeting. Not: a new scorer name. Not: is
Aaronson a longer hash history.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `gpt2` (pin Hub SHA `607a30d783dfa663caf39e06633721c8d4cfcd7e`) |
| Mixin | laboratory Aaronson–Kirchner exponential-minimum (`--mixin aaronson`) |
| `hashing_key` | **314159265** (public digits of π; not a laboratory secret) |
| PRF | BLAKE2b-64 of key, context length, context ids, vocab id; \(u=(x+1/2)/2^{64}\) |
| `context_width` | **1** (previous token only) |
| Sampling | temperature 1.0, top-\(K\) 40, then \(v^\star=\arg\max r^{1/p}\); `min_new_tokens=max_new_tokens` |
| Official control | matching mean-\(r\) z-test, `z_threshold=3.0`. \(z=(\bar r-1/2)/\sqrt{(1/12)/n}\) |
| Prompts | `experiments/2026-08-17-grok-prompts/` (original 12 scene strings; new twins) |
| Draws | `--n-samples 4` |
| Length | `--max-new-tokens 128` |
| Seed | `20260905` |
| Pair out-dir | `experiments/2026-09-04-pair-12x4-aaronson/` |
| Fold | leave-one-family-out (Algorithm 1 in the technical report) |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-04-probe-12x4-aaronson-hard-last4/` |
| Zero / abstention | \(n=0\Rightarrow\Lambda=0\); report coverage / `n_used` |
| Primary group metric | \(D_p\) sign count: `n_prompts_marked_above` / 12, strict `>` |
| Primary isolated metric | \(\tau=0\) confusion matrix, balanced accuracy, file AUC |
| Occupancy | `atoms --leave-one-out` on the interpolate tables after probe; mechanistic intermediate |

Official scoring of a `*-marked.txt` file uses only tokens in that
file (same file-grain convention as Kirchenbauer). Generation still
sees the prompt as live prefix. The first generated token is therefore
the one position where score-time context can differ from sample-time
context when `context_width=1`.

`pair --mixin aaronson` must generate **and** official-score with this
module. Scoring those twins with SynthID `detector_mean` or
Kirchenbauer `WatermarkDetector` is a harness bug, not a scientific
miss. `--ngram-len` is SynthID-only. `--also-control-keys` and
`--control-only` are SynthID-only.

No new method names. Hard and interpolate last-4 are the published
readers. Do not add poshits, rankpath, hashtok, or cascades after
peeking.

## Hypotheses (stated before generation)

- **H-aar-ctrl.** Official matching z-score is above \(3.0\) on every
  first marked file (mixin on). Unmarked first-draw is not all above
  \(3.0\) (expected near \(0\)). If marked first-draws fail this, stop
  and fix the harness; do not interpret key-free LRs.
- **H-aar-group.** Interpolate last-4 12-LOO prompt ranking is the
  primary group endpoint. If the published SynthID tournament footprint
  is necessary for this reader, ranking is **below** the public-mixin
  diagnostic **9/12**. If it stays **≥9/12**, the count-table signal is
  not unique to tournament sampling on this 12-family frame. Either
  outcome is informative. It does not replace **25/48**.
- **H-aar-hard.** Hard last-4 12-LOO ranking is reported beside
  interpolate. Same refuse-to-sell.
- **H-aar-iso.** Isolated \(\tau=0\) confusion matrix (TP, FN, TN, FP;
  sensitivity; specificity; balanced accuracy; AUC) does not replace
  **25/48**. Coverage when `n_used=0` is reported separately.
- **H-aar-occ.** Exact last-4 occupancy (`atoms` seen vs unseen) is
  logged. This mixin's hash window is one previous token, not
  \(\Hw=4\) or \(\Hw=12\). Occupancy is a mechanistic intermediate, not
  a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --n-samples 4 --max-new-tokens 128 --seed 20260905 --mixin aaronson \
  --hub-revision 607a30d783dfa663caf39e06633721c8d4cfcd7e \
  --out-dir experiments/2026-09-04-pair-12x4-aaronson
```

Do not look at key-free LRs until `pair` has written official
first-draw z-scores and this protocol's analysis command has been run
once, as written. Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-12x4-aaronson \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-12x4-aaronson-hard-last4
```

`used_keys=false`. After that dump exists, occupancy (not a second
freeze; same interpolate reader):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-09-04-pair-12x4-aaronson \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-atoms-12x4-aaronson
```

## One hundred families (named)

Same mixin defaults, GPT-2, `--n-samples 4`, \(T=128\), seed
`20260905`, prompts `experiments/2026-09-01-prompts-100/`, Hub SHA
as above. Same readers. Same two grains. Named here before generation.
A finished 100×4 corpus is not required for the freeze to hold.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --n-samples 4 --max-new-tokens 128 --seed 20260905 --mixin aaronson \
  --hub-revision 607a30d783dfa663caf39e06633721c8d4cfcd7e \
  --out-dir experiments/2026-09-04-pair-100x4-aaronson

python -m text_watermark_tools probe experiments/2026-09-04-pair-100x4-aaronson \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-100x4-aaronson-hard-last4
```

## What this protocol refuses

- Editing the `synthid-text` checkout.
- A Kirchenbauer / SynthID / other-mixin generator in this file.
- Fishing `context_width`, top-\(K\), or the hashing key after peeking.
- Scoring Aaronson twins with SynthID `detector_mean` or Kirchenbauer
  `WatermarkDetector` as the official control.
- Combining `--mixin aaronson` with `--ngram-len` other than the unused
  SynthID default, `--also-control-keys`, or `--control-only`.
- New hashed / backoff / cascade / learned scorers on 12×4 or the
  new twins.
- Leftover targeting, occupancy-free leftover unions, Distil ∪ SMT.
- Selling any Aaronson count as replacing **25/48**.
- Selling this freeze as the \(\Hw=12\) experiment or as Kirchenbauer.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file (and the `--mixin aaronson` CLI it names) in a
   commit that still precedes `pair`.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then the probe command, then append a dated logbook
   entry with the SHA and the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.
   Do not add a scorer.

Human merge of PR #4 is out of scope for this file.
