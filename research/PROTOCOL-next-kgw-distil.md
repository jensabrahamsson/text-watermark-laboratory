# Confirmatory protocol (Kirchenbauer on DistilGPT2)

This is a **methods freeze** for a generator-transfer of the already
opened Kirchenbauer two-grain lock
([PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md)). It does not add a
`probe --methods` name. It does not edit the `synthid-text` checkout.
GPT-2 Kirchenbauer original-12 interpolate **12/12** / isolated
**85/96** and 100-family interpolate **100/100** / **747/800** stay in
those dumps. This file asks whether the same Hugging Face Kirchenbauer
defaults still rank prompt groups when the generator is DistilGPT2.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`
from this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
z-scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score these twins with SynthID `detector_mean`.

## Why freeze now

Sol (2026-09-03) asked for a structurally different local mixin.
Kirchenbauer on GPT-2 is opened. The remaining cheap generator check
that is not leftover targeting is the same mixin on DistilGPT2, same
12 prompt strings, same two grains. An Aaronson Gumbel mixin is a
third freeze and is **not** this file (`transformers==4.57.6` has no
Aaronson logits processor).

A finished 100×4 Distil Kirchenbauer corpus is not required.

## Primary scientific question

On DistilGPT2 with Hugging Face default Kirchenbauer watermarking,
under leave-one-family-out interpolate last-4 and hard last-4, do
marked prompt-group means still outrank unmarked means?

Not: can GPT-2 Kirchenbauer tables classify Distil files. Not: leftover
targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `distilgpt2` (record Hub SHA in `results.json`; pin if a local snapshot exists) |
| Mixin | Hugging Face `WatermarkLogitsProcessor` (same defaults as PROTOCOL-next-kgw) |
| `greenlist_ratio` / `bias` / `hashing_key` | **0.25** / **2.0** / **15485863** |
| `seeding_scheme` / `context_width` | **lefthash** / **1** |
| Official control | `WatermarkDetector`, `z_threshold=3.0` |
| Prompts | `experiments/2026-08-17-grok-prompts/` |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260904** |
| Pair out-dir | `experiments/2026-09-03-pair-distil-12x4-kgw/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-03-probe-distil-12x4-kgw-hard-last4/` |
| Fold | leave-one-family-out |
| Primary group metric | $D_p$ sign count / 12, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

## Hypotheses (stated before generation)

- **H-kgw-d-ctrl.** Official matching z-score is above $3.0$ on every
  first marked file. Unmarked first-draw is not all above $3.0$. If
  marked first-draws fail, stop; harness bug.
- **H-kgw-d-group.** Interpolate last-4 12-LOO ranking is reported
  beside GPT-2 Kirchenbauer **12/12**. Either drop or hold is
  informative. It does not replace **25/48**.
- **H-kgw-d-iso.** Isolated $\tau=0$ does not replace **25/48**.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260904 \
  --mixin kgw --out-dir experiments/2026-09-03-pair-distil-12x4-kgw
```

If a local `distilgpt2` Hub SHA exists, pass `--hub-revision` that SHA.
Do not change other flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-distil-12x4-kgw \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-03-probe-distil-12x4-kgw-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-09-03-pair-distil-12x4-kgw \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-03-atoms-distil-12x4-kgw
```

## What this protocol refuses

- Editing `synthid-text`.
- An Aaronson generator in this file.
- New `probe --methods` names.
- Scoring Distil Kirchenbauer twins with SynthID `detector_mean`.
- Leftover targeting.
- Selling any Distil Kirchenbauer count as replacing **25/48**.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

## Results

Not opened. Do not fill this section before the frozen commands have
been run once, as written.
