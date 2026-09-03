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

Protocol SHA `1540d3c`. Named `55ca96e`. Pair seed **20260904**.
`mixin=kgw`. `model=distilgpt2`. `used_keys=false`. Hub revision was
not passed (`null` in `results.json`); the laboratory cache after this
run is `2290a62682d06624634c1f46a6ad5be0f47f38aa`. Do not backfill.

Pair dump: [experiments/2026-09-03-pair-distil-12x4-kgw/](../experiments/2026-09-03-pair-distil-12x4-kgw/).
Probe dump: [experiments/2026-09-03-probe-distil-12x4-kgw-hard-last4/](../experiments/2026-09-03-probe-distil-12x4-kgw-hard-last4/).

H-kgw-d-ctrl **holds**. Official matching z-score is above $3.0$ on all
12 first marked files (min $7.22$). Unmarked first-draw is **0/12**
above $3.0$ (max $2.72$). Mixin is on.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **12/12** | 0.947 | 42/48 | 43/48 | 42 6 43 5 | **85/96** |
| hard last-4 | **11/12** | 0.780 | 34/48 | 32/48 | 34 14 32 16 | **66/96** |

GPT-2 Kirchenbauer interpolate on the same prompt *strings* (different
twins) was **12/12** / **85/96**. Distil interpolate matches that
balanced accuracy. Mean $D_p=0.504$ (interpolate) / $0.094$ (hard).
Hard loses rain.

Clopper–Pearson 95% (not a second freeze): interpolate **12/12** is
**[0.735, 1.000]**; hard **11/12** is **[0.615, 0.998]**; BA
**85/96** is **[0.804, 0.941]**. Isolated **25/48** still includes ½.

H-kgw-d-group **holds**. Interpolate last-4 is **12/12**, the same
sign count as GPT-2 Kirchenbauer on these strings. It does not replace
**25/48**.

H-kgw-d-iso **holds**. Isolated interpolate **85/96** is a different
generator and mixin from the original-12 SynthID **47/96**. Do not sell
**12/12**, **85/96**, **11/12**, or **66/96** as replacing **25/48**.

Occupancy: **130** seen vs **11972** unseen (opening 63 vs 225).
`used_keys=false`. File LRs match interpolate **42/48**. Do not sell
**130** as replacing **25/48**.

JSON: [experiments/2026-09-03-atoms-distil-12x4-kgw/](../experiments/2026-09-03-atoms-distil-12x4-kgw/).

Isolated-file detection on the public SynthID original-12 remains
**25/48** / **47/96**. Do not write `thesis/`.
