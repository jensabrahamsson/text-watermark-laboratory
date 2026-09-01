# Key-free instance contrast (not key recovery)

Official `score` is instance-specific. Text sampled with `control_keys()`
(`control-shuffled-30`) sits near **0.50** on the public DeepMind 30 and near
**0.62** on the matching control keys. That is already in
[../experiments/2026-08-17-pair-limit/](../experiments/2026-08-17-pair-limit/).

This note asks a different question:

> Does the **key-free** count-table reader see *this* public instance, or
> does it see tournament sampling in general?

The theory this rests on is not original to this repository.

- **DeepMind SynthID-Text** (tournament sampling) is the watermark. The
  official detector needs the keys used at sampling. See
  [how-synthid-works.md](how-synthid-works.md).
- A permutation of those keys is a **different instance**, not “mixin off”.
  `control_keys()` offsets and shuffles the public 30 with a fixed seed. It
  is a laboratory dummy, not a second vendor and not Anthropic.
- **Stealing-style readers** estimate context-dependent token preference
  from samples, without reconstructing the secret hash or SHA-256 IV. See
  [invertibility.md](invertibility.md).
- **This lab's contribution** is to fit the public marked/unmarked tables
  with no keys, then score a third pile that the official public detector
  already calls chance.

If control ranks with unmarked, the key-free reader is instance-specific
without keys. If it ranks with marked, the reader is detecting tournament
sampling, not this instance. Neither outcome recovers keys.

Do not replace the recounted headlines **9/12**, **25/48**, or **36/36**.
Pre-fix **10/12** / **29/48** stay in historical JSON.
This is not a universal detector. It is not Claude.

## Protocol

Fit on public-key twins only. Drop overlapping test stems from train
(`drop-from-train`). Score three comparisons. In each name, the first class
is the positive class:

| Comparison | Positive | Negative | Question |
|---|---|---|---|
| `public-vs-unmarked` | public marked | unmarked | can the reader still see the public mark |
| `control-vs-unmarked` | control-gen | unmarked | does the other instance look marked |
| `public-vs-control` | public marked | control-gen | can it tell the two instances apart |

Control files are `*-control-gen.txt`. They are never a `*-marked.txt`, so
`blind` / `indicate fit` do not train on them.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --control-only --n-samples 4 --max-new-tokens 128 --seed 20260931 \
  --out-dir experiments/2026-08-31-pair-12x4-controlkeys

python -m text_watermark_tools contrast experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --control-dir experiments/2026-08-31-pair-12x4-controlkeys \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4

python -m text_watermark_tools contrast experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-limit \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-contrast-36x4-to-limit-fitprefix4
```

`--control-dir` defaults to `--test-dir` (the 12×1×700 pile already has
control-gen). Quote **isolated `lr > 0` on control** separately from
prompt-mean wins. When every control LR is exactly 0, prompt-mean “wins”
against negative unmarked LRs are not evidence that control is marked.

`--methods poshits,postokhits` runs the occupancy-gated reader on the
same split. Control stays **0/48**. See [key-free-tokhits.md](key-free-tokhits.md).

`--methods rankpath,rankuni` is the unmarked-LM rank-symbol reader.
Prefix-4 rankpath control `lr>0` is **6/48** (chance ranking). Opening
rankuni control is **30/48**. See [key-free-rankpath.md](key-free-rankpath.md).

The matched 4-token poshits gate is the same split as
[key-free-probe.md](key-free-probe.md): train 24 other 36×4 stems, skip
generated token 0, position bucket 1.

## Official lamp on the new 12×4 control pile

Corpus: [../experiments/2026-08-31-pair-12x4-controlkeys/](../experiments/2026-08-31-pair-12x4-controlkeys/).
12 prompts × 4 draws × 128 tokens. Seed 20260931.

| Keys | Mean of 48 file means | Range |
|---|---|---|
| `public-deepmind-30` | **0.501** | 0.483–0.526 |
| matching `control-shuffled-30` | **0.624** | 0.604–0.641 |

Every file scores higher on the matching control keys than on the public
keys. Same pattern as pair-limit.

## Result: matched 4-token poshits (n=48)

JSON: [../experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4/](../experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4/).
`used_keys=false`. Public-vs-unmarked copies the published OOD gate
(**12/12**, AUC **0.873**, t=0 **39/48 vs 41/48**).

| Method | Comparison | Prompt wins | File AUC | pos `lr>0` | neg `lr≤0` | perm p |
|---|---|---|---|---|---|---|
| **poshits** | public-vs-unmarked | **12/12** | **0.873** | **39/48** | **41/48** | 0.00050 |
| **poshits** | control-vs-unmarked | 9/12 | **0.510** | **0/48** | 41/48 | 0.023 |
| **poshits** | public-vs-control | **12/12** | **0.906** | **39/48** | **48/48** | 0.00050 |
| hits | public-vs-unmarked | 11/12 | 0.820 | 39/48 | 33/48 | 0.00050 |
| hits | control-vs-unmarked | 8/12 | 0.458 | **0/48** | 33/48 | 0.16 |
| hits | public-vs-control | **12/12** | **0.906** | 39/48 | **48/48** | 0.00050 |
| hashpool | public-vs-unmarked | 11/12 | 0.788 | 29/48 | 38/48 | 0.00050 |
| hashpool | control-vs-unmarked | 9/12 | 0.617 | **6/48** | 38/48 | 0.012 |
| hashpool | public-vs-control | 8/12 | 0.697 | 29/48 | 42/48 | 0.00050 |

**poshits and hits never assign `lr > 0` to a control-key opening.** All
48 control LRs are 0 under those tables (no shared last-k from the public
fit). Public marked still ranks **12/12** against control (AUC **0.906**),
and every control file is `≤ 0`.

The control-vs-unmarked AUC near 0.5 is the honest ranking. Prompt wins
9/12 and perm p=0.023 for poshits are the artifact that zeros beat
*negative* unmarked LRs. That is not “control looks marked”. Hashpool is
leakier: **6/48** control files have `lr > 0`, AUC 0.617. Do not headline
hashpool as instance-specific.

Brier (LR as log-odds): poshits public-vs-unmarked **0.182**;
control-vs-unmarked **0.241** (near the 0.25 of a constant 0.5). The
opening-token LR is still not a calibrated yes/no on one file.

## Full 128-token files (same 48 control draws)

JSON: [../experiments/2026-08-31-contrast-36x4-to-12x4-full/](../experiments/2026-08-31-contrast-36x4-to-12x4-full/).

| Method | Comparison | Prompt wins | File AUC | pos `lr>0` | neg `lr≤0` |
|---|---|---|---|---|---|
| poshits | control-vs-unmarked | 9/12 | 0.500 | **0/48** | 40/48 |
| poshits | public-vs-control | **12/12** | **0.906** | 39/48 | **48/48** |
| hits | control-vs-unmarked | 7/12 | 0.475 | **29/48** | 24/48 |
| hits | public-vs-control | 11/12 | 0.842 | 42/48 | 19/48 |
| hashpool | control-vs-unmarked | 7/12 | 0.511 | 17/48 | 36/48 |
| hashpool | public-vs-control | 8/12 | 0.718 | 30/48 | 31/48 |

Position-bucketed last-k stays instance-specific on the full file because
later tokens sit in other buckets and the public opening 4-grams still do
not fire. **Unbucketed hits on the full file is not a clean instance
check:** 29/48 control files have `lr > 0`, while ranking vs unmarked is
chance (AUC 0.475). Shared function-word 4-grams are not the same thing as
this key instance. Quote poshits `0/48`, not hits `29/48`, for
instance-specificity.

## 700-token pair-limit (n=12)

JSON:
[../experiments/2026-08-31-contrast-36x4-to-limit-fitprefix4/](../experiments/2026-08-31-contrast-36x4-to-limit-fitprefix4/)
and
[../experiments/2026-08-31-contrast-36x4-to-limit-full/](../experiments/2026-08-31-contrast-36x4-to-limit-full/).
Train is the same 24 other 36×4 stems.

| Protocol | Method | public-vs-unmarked | control-vs-unmarked | public-vs-control |
|---|---|---|---|---|
| 4-token | poshits | 12/12, AUC 0.854, 10/12 `lr>0` | AUC 0.417, **0/12** `lr>0` | **12/12**, AUC **0.917** |
| 4-token | hits | 12/12, AUC 0.854 | AUC 0.417, **0/12** `lr>0` | **12/12**, AUC **0.917** |
| 4-token | hashpool | 10/12, AUC 0.833 | AUC 0.750, 2/12 `lr>0` | 6/12, AUC 0.625 |
| full 700 | hits | 11/12, AUC **0.965** | AUC 0.556, 7/12 `lr>0` | **12/12**, AUC **1.000** |
| full 700 | poshits | 11/12, AUC 0.806 | AUC 0.417, **0/12** `lr>0` | **12/12**, AUC **0.917** |
| full 700 | hashpool | 12/12, AUC 0.944 | AUC 0.431, **0/12** `lr>0` | **12/12**, AUC **0.965** |

On 700-token files, unbucketed hits **ranks** the two instances perfectly
(AUC 1.000) while control vs unmarked stays chance. The 4-token hashpool
AUC 0.750 on n=12 is the same leakage seen at 6/48 on the 12×4 pile; full
hashpool on 700 tokens does not repeat it.

## What this does and does not show

It shows: a public-trained last-k count table, especially **matched
4-token poshits**, is a reader of **this key instance's opening-token
preferences**, not a generic “tournament is on” detector. That is why
control-key text that the official public lamp already scores at chance
also gets `lr > 0` on **0/48** isolated files.

It does not show: key recovery, SHA-256 IV recovery, a second-vendor
detector, or a calibrated isolated-file yes/no. Public marked isolated
sign on this gate remains **39/48**. That 39/48 includes The-Laplace
occupancy; observed-token `postokhits` is **16/48** with precision 1.0
among decided files, and control stays **0/48** under that reader too.
Leave-one-of-12-out hard last-4 remains **25/48** (pre-fix **29/48**). Qwen and DistilGPT2
token-identity transfer remain chance. Native Distil rankpath is chance
(**8/12**, AUC **0.579**) despite official 12/12. Tiny nets still do not
beat poshits.

Rank-path tables (unmarked-LM rank symbols, not token identity) are a
different instance check. Unbucketed prefix-4 **rankpath** ranks
control with unmarked (AUC **0.511**, isolated **6/48** `lr>0`, matching
the unmarked false-positive rate) while public vs unmarked stays
**11/12**, AUC **0.759**. Opening rankuni is *not* instance-specific
(control **30/48**, public vs control AUC **0.502**). See
[key-free-rankpath.md](key-free-rankpath.md). Not key recovery.

`control_keys()` is a laboratory permutation of the public 30. A genuinely
independent key sample, or a different generator, is a different
experiment.
