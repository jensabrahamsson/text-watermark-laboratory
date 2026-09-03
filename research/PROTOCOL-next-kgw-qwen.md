# Confirmatory protocol (Kirchenbauer on Qwen2-1.5B)

This is a **methods freeze** for a second generator-transfer of the
already opened Kirchenbauer two-grain lock
([PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md)). It does not add a
`probe --methods` name. It does not edit the `synthid-text` checkout.
GPT-2 Kirchenbauer original-12 interpolate **12/12** / **85/96** and
Distil interpolate **12/12** / **85/96** stay in those dumps. This
file asks whether the same Hugging Face Kirchenbauer defaults still
rank prompt groups on Qwen2-1.5B-Instruct.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`
from this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
z-scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score these twins with SynthID `detector_mean`.
Do **not** apply a chat template after peeking.

## Why freeze now

Kirchenbauer on GPT-2 and DistilGPT2 is opened. The remaining local
generator in the laboratory's native Phase B set is Qwen2-1.5B. Same
12 prompt strings, same two grains, same mixin defaults. An Aaronson
Gumbel mixin is a different freeze (`transformers==4.57.6` has no
Aaronson logits processor) and is **not** this file.

A finished 100×4 Qwen Kirchenbauer corpus is not required.

## Primary scientific question

On Qwen2-1.5B-Instruct with Hugging Face default Kirchenbauer
watermarking, under leave-one-family-out interpolate last-4 and hard
last-4, do marked prompt-group means still outrank unmarked means?

Not: can GPT-2 Kirchenbauer tables classify Qwen files. Not: leftover
targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `Qwen/Qwen2-1.5B-Instruct` (record Hub SHA in `results.json`; pin if a local snapshot exists) |
| Mixin | Hugging Face `WatermarkLogitsProcessor` (same defaults as PROTOCOL-next-kgw) |
| `greenlist_ratio` / `bias` / `hashing_key` | **0.25** / **2.0** / **15485863** |
| `seeding_scheme` / `context_width` | **lefthash** / **1** |
| Official control | `WatermarkDetector` with the **Qwen** config vocab, `z_threshold=3.0` |
| Prompts | `experiments/2026-08-17-grok-prompts/` (plain strings; no chat template) |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260904** |
| Pair out-dir | `experiments/2026-09-03-pair-qwen-12x4-kgw/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-03-probe-qwen-12x4-kgw-hard-last4/` |
| Fold | leave-one-family-out |
| Primary group metric | $D_p$ sign count / 12, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

Matching official scoring must use the Qwen tokenizer and config.
Scoring Qwen Kirchenbauer twins with a GPT-2 `WatermarkDetector` is a
harness bug.

## Hypotheses (stated before generation)

- **H-kgw-q-ctrl.** Official matching z-score is above $3.0$ on every
  first marked file. Unmarked first-draw is not all above $3.0$. If
  marked first-draws fail, stop; harness bug.
- **H-kgw-q-group.** Interpolate last-4 12-LOO ranking is reported
  beside GPT-2 Kirchenbauer **12/12** and Distil **12/12**. Either drop
  or hold is informative. It does not replace **25/48**.
- **H-kgw-q-iso.** Isolated $\tau=0$ does not replace **25/48**.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260904 --mixin kgw \
  --out-dir experiments/2026-09-03-pair-qwen-12x4-kgw
```

If a local Hub SHA exists, pass `--hub-revision` that SHA. Do not
change other flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-qwen-12x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-03-probe-qwen-12x4-kgw-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --model Qwen/Qwen2-1.5B-Instruct \
  --test-dir experiments/2026-09-03-pair-qwen-12x4-kgw \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-03-atoms-qwen-12x4-kgw
```

## What this protocol refuses

- Editing `synthid-text`.
- An Aaronson generator in this file.
- New `probe --methods` names.
- Scoring Qwen Kirchenbauer twins with SynthID `detector_mean` or a
  GPT-2 `WatermarkDetector`.
- Adding a chat template after peeking.
- Leftover targeting.
- Selling any Qwen Kirchenbauer count as replacing **25/48**.
- Paid chat APIs (`iterate --backend qwen` included).
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

## Results

Protocol SHA `45a75c9`. Named `4f0ce39`. Pair seed **20260904**.
`mixin=kgw`. `model=Qwen/Qwen2-1.5B-Instruct`. `used_keys=false`.
Hub revision was not passed (`null` in `results.json`); the laboratory
cache after this run is
`ba1cf1846d7df0a0591d6c00649f57e798519da8`. Do not backfill.

Pair dump: [experiments/2026-09-03-pair-qwen-12x4-kgw/](../experiments/2026-09-03-pair-qwen-12x4-kgw/).
Probe dump: [experiments/2026-09-03-probe-qwen-12x4-kgw-hard-last4/](../experiments/2026-09-03-probe-qwen-12x4-kgw-hard-last4/).

H-kgw-q-ctrl **holds**. Official matching z-score is above $3.0$ on all
12 first marked files (min $4.56$). Unmarked first-draw is **0/12**
above $3.0$ (max $1.90$). Mixin is on.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **12/12** | 0.814 | 35/48 | 33/48 | 35 13 33 15 | **68/96** |
| hard last-4 | **8/12** | 0.566 | 19/48 | 31/48 | 19 29 31 17 | **50/96** |

GPT-2 and Distil Kirchenbauer interpolate on these prompt *strings*
(different twins) were **12/12** / **85/96**. Qwen interpolate keeps
the group ranking and drops isolated balanced accuracy to **68/96**.
Mean $D_p=0.224$ (interpolate) / $0.017$ (hard). Hard **8/12**
Clopper–Pearson includes ½.

H-kgw-q-group **holds**. Interpolate last-4 is **12/12**. It does not
replace **25/48**.

H-kgw-q-iso **holds**. Isolated interpolate **68/96** is a different
generator and mixin from the original-12 SynthID **47/96**. Hard
isolated **50/96** is chance-like. Do not sell **12/12**, **68/96**,
**8/12**, or **50/96** as replacing **25/48**.

Occupancy: **84** seen vs **12108** unseen (opening 62 vs 226).
`used_keys=false`. File LRs match interpolate **35/48**. Do not sell
**84** as replacing **25/48**.

JSON: [experiments/2026-09-03-atoms-qwen-12x4-kgw/](../experiments/2026-09-03-atoms-qwen-12x4-kgw/).

Isolated-file detection on the public SynthID original-12 remains
**25/48** / **47/96**. Do not write `thesis/`.
