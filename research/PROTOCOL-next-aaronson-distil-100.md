# Confirmatory protocol (Aaronson–Kirchner on DistilGPT2, 100 families)

This is a **methods freeze** for a 100-family generator-transfer of the
already opened DistilGPT2 Aaronson 12-LOO lock
([PROTOCOL-next-aaronson-distil.md](PROTOCOL-next-aaronson-distil.md)).
It does not add a `probe --methods` name. It does not edit the
`synthid-text` checkout. Distil original-12 interpolate **7/12** /
isolated **0/48** and GPT-2 100-family interpolate **100/100** /
**608/800** stay in those dumps. This file asks whether the same
laboratory exponential-minimum instance still ranks prompt groups on
DistilGPT2 when the prompt frame is the 100 one-liners.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`
from this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
z-scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score these twins with SynthID `detector_mean` or
Kirchenbauer `WatermarkDetector`.

## Why freeze now

Aaronson on GPT-2 100-family interpolate is **100/100**. Distil Aaronson
12-LOO interpolate is **7/12** with **0/48** isolated TPs. The remaining
cheap generator-scale check that is not leftover targeting is the same
mixin on DistilGPT2 with the 100 one-liners. Kirchenbauer and SynthID
$\Hw=12$ Distil 100-family runs are different mixins and are **not**
this file. `transformers==4.57.6` has no Aaronson logits processor; the
sampler stays in this repository.

## Primary scientific question

On DistilGPT2 with this frozen Aaronson–Kirchner exponential-minimum
instance, under leave-one-family-out interpolate last-4 and hard last-4
on 100 one-liners, do marked prompt-group means still outrank unmarked
means?

Not: can Distil 12-LOO Aaronson tables classify the 100 files. Not:
leftover targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `distilgpt2` (pin Hub SHA `2290a62682d06624634c1f46a6ad5be0f47f38aa`) |
| Mixin | laboratory Aaronson–Kirchner exponential-minimum (`--mixin aaronson`) |
| `hashing_key` | **314159265** |
| `context_width` | **1** |
| Official control | matching mean-\(r\) z-test, `z_threshold=3.0` |
| Prompts | `experiments/2026-09-01-prompts-100/` |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260905** |
| Pair out-dir | `experiments/2026-09-04-pair-distil-100x4-aaronson/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-04-probe-distil-100x4-aaronson-hard-last4/` |
| Fold | leave-one-family-out |
| Primary group metric | $D_p$ sign count / 100, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

Scoring Distil Aaronson twins with SynthID `detector_mean` is a harness
bug.

## Hypotheses (stated before generation)

- **H-aar-d100-ctrl.** Official matching z-score is above $3.0$ on every
  first marked file. Unmarked first-draw is not all above $3.0$. If
  marked first-draws fail, stop; harness bug.
- **H-aar-d100-group.** Interpolate last-4 100-LOO ranking is reported
  beside GPT-2 Aaronson **100/100**. Either drop or hold is informative.
  It does not replace **25/48**.
- **H-aar-d100-iso.** Isolated $\tau=0$ does not replace **25/48**.
- **H-aar-d100-occ.** Exact last-4 occupancy (`atoms --leave-one-out`)
  is logged after probe. Occupancy is a mechanistic intermediate, not
  a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260905 \
  --mixin aaronson --hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa \
  --out-dir experiments/2026-09-04-pair-distil-100x4-aaronson
```

Do not look at key-free LRs until `pair` has written official
first-draw z-scores and the probe command has been run once, as
written. Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-aaronson \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-distil-100x4-aaronson-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-09-04-pair-distil-100x4-aaronson \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-atoms-distil-100x4-aaronson
```

## What this protocol refuses

- Editing `synthid-text`.
- A Kirchenbauer / SynthID $\Hw=12$ generator in this file.
- New `probe --methods` names.
- Scoring Distil Aaronson twins with `detector_mean`.
- Leftover targeting.
- Selling any Distil Aaronson 100-family count as replacing **25/48**.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.
