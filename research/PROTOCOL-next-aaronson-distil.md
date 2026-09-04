# Confirmatory protocol (Aaronson–Kirchner on DistilGPT2)

This is a **methods freeze** for a generator-transfer of the already
opened Aaronson–Kirchner exponential-minimum lock
([PROTOCOL-next-aaronson.md](PROTOCOL-next-aaronson.md)). It does not
add a `probe --methods` name. It does not edit the `synthid-text`
checkout. GPT-2 Aaronson original-12 interpolate **11/12** / isolated
**56/96** and 100-family interpolate **100/100** / **608/800** stay in
those dumps. This file asks whether the same laboratory exponential-
minimum instance still ranks prompt groups when the generator is
DistilGPT2.

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

Aaronson on GPT-2 is opened. The remaining cheap generator check that
is not leftover targeting is the same mixin on DistilGPT2, same 12
prompt strings, same two grains. Kirchenbauer Distil and SynthID
$\Hw=12$ Distil are different mixins and are **not** this file.
`transformers==4.57.6` has no Aaronson logits processor; the sampler
stays in this repository.

A finished 100×4 Distil Aaronson corpus is not required.

## Primary scientific question

On DistilGPT2 with this frozen Aaronson–Kirchner exponential-minimum
instance, under leave-one-family-out interpolate last-4 and hard
last-4, do marked prompt-group means still outrank unmarked means?

Not: can GPT-2 Aaronson tables classify Distil files. Not: leftover
targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `distilgpt2` (pin Hub SHA `2290a62682d06624634c1f46a6ad5be0f47f38aa`) |
| Mixin | laboratory Aaronson–Kirchner exponential-minimum (`--mixin aaronson`) |
| `hashing_key` | **314159265** |
| `context_width` | **1** |
| Official control | matching mean-\(r\) z-test, `z_threshold=3.0` |
| Prompts | `experiments/2026-08-17-grok-prompts/` |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260905** |
| Pair out-dir | `experiments/2026-09-04-pair-distil-12x4-aaronson/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-04-probe-distil-12x4-aaronson-hard-last4/` |
| Fold | leave-one-family-out |
| Primary group metric | $D_p$ sign count / 12, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

Scoring Distil Aaronson twins with SynthID `detector_mean` is a harness
bug.

## Hypotheses (stated before generation)

- **H-aar-d-ctrl.** Official matching z-score is above $3.0$ on every
  first marked file. Unmarked first-draw is not all above $3.0$. If
  marked first-draws fail, stop; harness bug.
- **H-aar-d-group.** Interpolate last-4 12-LOO ranking is reported
  beside GPT-2 Aaronson **11/12**. Either drop or hold is informative.
  It does not replace **25/48**.
- **H-aar-d-iso.** Isolated $\tau=0$ does not replace **25/48**.
- **H-aar-d-occ.** Exact last-4 occupancy (`atoms --leave-one-out`)
  is logged after probe. Occupancy is a mechanistic intermediate, not
  a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260905 \
  --mixin aaronson --hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa \
  --out-dir experiments/2026-09-04-pair-distil-12x4-aaronson
```

Do not look at key-free LRs until `pair` has written official
first-draw z-scores and the probe command has been run once, as
written. Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-12x4-aaronson \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-distil-12x4-aaronson-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-09-04-pair-distil-12x4-aaronson \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-atoms-distil-12x4-aaronson
```

## What this protocol refuses

- Editing `synthid-text`.
- A Kirchenbauer / SynthID $\Hw=12$ generator in this file.
- New `probe --methods` names.
- Scoring Distil Aaronson twins with `detector_mean`.
- Leftover targeting.
- Selling any Distil Aaronson count as replacing **25/48**.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.
