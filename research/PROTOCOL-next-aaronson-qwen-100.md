# Confirmatory protocol (Aaronson–Kirchner on Qwen2-1.5B, 100 families)

This is a **methods freeze** for a 100-family generator-transfer of the
already opened Qwen2-1.5B Aaronson 12-LOO lock
([PROTOCOL-next-aaronson-qwen.md](PROTOCOL-next-aaronson-qwen.md)).
It does not add a `probe --methods` name. It does not edit the
`synthid-text` checkout. Qwen original-12 interpolate **12/12** /
isolated **12/48** and Distil 100-family interpolate **96/100** /
**601/800** stay in those dumps. This file asks whether the same
laboratory exponential-minimum instance still ranks prompt groups on
Qwen2-1.5B-Instruct when the prompt frame is the 100 one-liners.

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
Do **not** apply a chat template after peeking.

## Why freeze now

Aaronson on GPT-2 100-family interpolate is **100/100**. Distil
Aaronson 100-family interpolate is **96/100**. Qwen Aaronson 12-LOO
interpolate is **12/12** with **12/48** isolated TPs. The remaining
generator-scale check that is not leftover targeting is the same mixin
on Qwen2-1.5B with the 100 one-liners. Kirchenbauer and SynthID
$\Hw=12$ Qwen 100-family runs are different mixins and are **not**
this file. `transformers==4.57.6` has no Aaronson logits processor; the
sampler stays in this repository.

## Primary scientific question

On Qwen2-1.5B-Instruct with this frozen Aaronson–Kirchner
exponential-minimum instance, under leave-one-family-out interpolate
last-4 and hard last-4 on 100 one-liners, do marked prompt-group means
still outrank unmarked means?

Not: can Qwen 12-LOO Aaronson tables classify the 100 files. Not:
leftover targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `Qwen/Qwen2-1.5B-Instruct` (pin Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`) |
| Mixin | laboratory Aaronson–Kirchner exponential-minimum (`--mixin aaronson`) |
| `hashing_key` | **314159265** |
| `context_width` | **1** |
| Official control | matching mean-\(r\) z-test, `z_threshold=3.0` |
| Prompts | `experiments/2026-09-01-prompts-100/` (plain strings; no chat template) |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260905** |
| Pair out-dir | `experiments/2026-09-04-pair-qwen-100x4-aaronson/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-04-probe-qwen-100x4-aaronson-hard-last4/` |
| Fold | leave-one-family-out |
| Primary group metric | $D_p$ sign count / 100, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

Scoring Qwen Aaronson twins with SynthID `detector_mean` is a harness
bug. Probe and `atoms` must pass `--model Qwen/Qwen2-1.5B-Instruct`;
the default GPT-2 tokenizer is a harness bug on these twins.

## Hypotheses (stated before generation)

- **H-aar-q100-ctrl.** Official matching z-score is above $3.0$ on every
  first marked file. Unmarked first-draw is not all above $3.0$. If
  marked first-draws fail, stop; harness bug.
- **H-aar-q100-group.** Interpolate last-4 100-LOO ranking is reported
  beside GPT-2 Aaronson **100/100** and Distil Aaronson **96/100**.
  Either drop or hold is informative. It does not replace **25/48**.
- **H-aar-q100-iso.** Isolated $\tau=0$ does not replace **25/48**.
- **H-aar-q100-occ.** Exact last-4 occupancy (`atoms --leave-one-out`)
  is logged after probe. Occupancy is a mechanistic intermediate, not
  a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260905 --mixin aaronson \
  --hub-revision ba1cf1846d7df0a0591d6c00649f57e798519da8 \
  --out-dir experiments/2026-09-04-pair-qwen-100x4-aaronson
```

Do not look at key-free LRs until `pair` has written official
first-draw z-scores and the probe command has been run once, as
written. Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-100x4-aaronson \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-qwen-100x4-aaronson-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --model Qwen/Qwen2-1.5B-Instruct \
  --test-dir experiments/2026-09-04-pair-qwen-100x4-aaronson \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-atoms-qwen-100x4-aaronson
```

## What this protocol refuses

- Editing `synthid-text`.
- A Kirchenbauer / SynthID $\Hw=12$ generator in this file.
- New `probe --methods` names.
- Scoring Qwen Aaronson twins with `detector_mean`.
- Scoring Qwen twins with the default GPT-2 tokenizer.
- Adding a chat template after peeking.
- Leftover targeting.
- Selling any Qwen Aaronson 100-family count as replacing **25/48**.
- Paid chat APIs (`iterate --backend qwen` included).
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.

## Results

Protocol SHA `a761a7d`. Named `de035df`. Pair seed **20260905**.
`--mixin aaronson`. `model=Qwen/Qwen2-1.5B-Instruct`. `used_keys=false`.
Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`. Host crash at 37/100;
resume used the same flags.

Pair dump: [experiments/2026-09-04-pair-qwen-100x4-aaronson/](../experiments/2026-09-04-pair-qwen-100x4-aaronson/).
Probe dump: [experiments/2026-09-04-probe-qwen-100x4-aaronson-hard-last4/](../experiments/2026-09-04-probe-qwen-100x4-aaronson-hard-last4/).

H-aar-q100-ctrl **fails** as the preregistered 100/100 first-draw.
Official matching z-score is above $3.0$ on **99/100** first marked
files (min $1.95$ on stem 025, a short Chinese multiple-choice loop,
$n=129$). Unmarked first-draw is **0/100** above $3.0$ (max $2.08$).
Mixin is on for the other 99 stems. Do not sell **99/100**.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **100/100** | 0.999 | 216/400 | 400/400 | 216 184 400 0 | **616/800** |
| hard last-4 | **97/100** | 0.949 | 268/400 | 397/400 | 268 132 397 3 | **665/800** |

GPT-2 Aaronson interpolate on these prompt *strings* (different twins)
was **100/100** (isolated **608/800**). Distil interpolate was
**96/100**. Qwen interpolate is **100/100**, and **46/100** ranking
wins have 0 isolated TPs (unmarked more negative). Mean $D_p=2.588$
(interpolate) / $0.664$ (hard). Isolated interpolate **216/400**
Clopper–Pearson includes ½.

Clopper–Pearson 95% (not a second freeze): interpolate **100/100** is
**[0.964, 1.000]** and does not include ½; BA **616/800** is
**[0.739, 0.799]**. Isolated **25/48** still includes ½.

H-aar-q100-group **holds** as an informative comparison with GPT-2
Aaronson **100/100** and Distil **96/100**. It does not replace
**25/48**.

H-aar-q100-iso **holds**. Isolated interpolate **616/800** is a
different generator from the original-12 SynthID **47/96**. Isolated
marked $t=0$ **216/400** includes ½. Do not sell **100/100**,
**97/100**, **616/800**, or **665/800** as replacing **25/48**.

H-aar-q100-occ **holds**. Leave-one-family-out interpolate atoms
(`used_keys=false`). File LRs match interpolate **216/400**. Exact
next-token overlap is **8750** seen versus **92842** unseen (opening
$[0{:}4)$ is 1470 versus 930, including `'At'→' last'` n=124).
Occupancy is not a detector. Do not sell **8750** or `'At'→' last'`
as replacing **25/48**.

JSON: [experiments/2026-09-04-atoms-qwen-100x4-aaronson/](../experiments/2026-09-04-atoms-qwen-100x4-aaronson/).

Isolated-file detection on the public SynthID original-12 remains
**25/48** / **47/96**. Do not write `thesis/`.

