# Confirmatory protocol (Kirchenbauer on Qwen2-1.5B, 100 families)

This is a **methods freeze** for a 100-family generator-transfer of the
already opened Qwen2-1.5B Kirchenbauer 12-LOO lock
([PROTOCOL-next-kgw-qwen.md](PROTOCOL-next-kgw-qwen.md)).
It does not add a `probe --methods` name. It does not edit the
`synthid-text` checkout. Qwen original-12 interpolate **12/12** /
isolated **68/96** and Distil 100-family interpolate **100/100** /
**683/800** stay in those dumps. This file asks whether the same
Hugging Face Kirchenbauer defaults still rank prompt groups on
Qwen2-1.5B-Instruct when the prompt frame is the 100 one-liners.

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

Kirchenbauer 100-family interpolate is **100/100** on GPT-2 and
**100/100** on DistilGPT2. Qwen Kirchenbauer 12-LOO interpolate is
**12/12**. The remaining generator-scale check that is not leftover
targeting is the same mixin defaults on Qwen2-1.5B with the 100
one-liners. Aaronson and SynthID $\Hw=12$ Qwen 100-family runs are
different mixins and are **not** this file.

PROTOCOL-next-kgw-qwen said a finished 100×4 corpus is not required
for the original-12 freeze. This file is the named 100-family readout.

## Primary scientific question

On Qwen2-1.5B-Instruct with Hugging Face default Kirchenbauer
watermarking, under leave-one-family-out interpolate last-4 and hard
last-4 on 100 one-liners, do marked prompt-group means still outrank
unmarked means?

Not: can Qwen 12-LOO Kirchenbauer tables classify the 100 files. Not:
leftover targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `Qwen/Qwen2-1.5B-Instruct` (pin Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`) |
| Mixin | Hugging Face `WatermarkLogitsProcessor` (`--mixin kgw`) |
| `greenlist_ratio` / `bias` / `hashing_key` | **0.25** / **2.0** / **15485863** |
| `seeding_scheme` / `context_width` | **lefthash** / **1** |
| Official control | matching `WatermarkDetector` z-test, `z_threshold=3.0` |
| Prompts | `experiments/2026-09-01-prompts-100/` (plain strings; no chat template) |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260904** |
| Pair out-dir | `experiments/2026-09-04-pair-qwen-100x4-kgw/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-04-probe-qwen-100x4-kgw-hard-last4/` |
| Fold | leave-one-family-out |
| Primary group metric | $D_p$ sign count / 100, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

Scoring Qwen Kirchenbauer twins with SynthID `detector_mean` is a
harness bug. Probe and `atoms` must pass `--model
Qwen/Qwen2-1.5B-Instruct`; the default GPT-2 tokenizer is a harness
bug on these twins.

## Hypotheses (stated before generation)

- **H-kgw-q100-ctrl.** Official matching z-score is above $3.0$ on every
  first marked file. Unmarked first-draw is not all above $3.0$. If
  marked first-draws fail, stop; harness bug.
- **H-kgw-q100-group.** Interpolate last-4 100-LOO ranking is reported
  beside GPT-2 Kirchenbauer **100/100** and Distil **100/100**. Either
  drop or hold is informative. It does not replace **25/48**.
- **H-kgw-q100-iso.** Isolated $\tau=0$ does not replace **25/48**.
- **H-kgw-q100-occ.** Exact last-4 occupancy (`atoms --leave-one-out`)
  is logged after probe. Occupancy is a mechanistic intermediate, not
  a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260904 --mixin kgw \
  --hub-revision ba1cf1846d7df0a0591d6c00649f57e798519da8 \
  --out-dir experiments/2026-09-04-pair-qwen-100x4-kgw
```

Do not look at key-free LRs until `pair` has written official
first-draw z-scores and the probe command has been run once, as
written. Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-100x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-qwen-100x4-kgw-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --model Qwen/Qwen2-1.5B-Instruct \
  --test-dir experiments/2026-09-04-pair-qwen-100x4-kgw \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-atoms-qwen-100x4-kgw
```

## What this protocol refuses

- Editing `synthid-text`.
- An Aaronson / SynthID $\Hw=12$ generator in this file.
- New `probe --methods` names.
- Scoring Qwen Kirchenbauer twins with `detector_mean`.
- Scoring Qwen twins with the default GPT-2 tokenizer.
- Adding a chat template after peeking.
- Leftover targeting.
- Selling any Qwen Kirchenbauer 100-family count as replacing **25/48**.
- Paid chat APIs (`iterate --backend qwen` included).
- Writing `thesis/`.
- Merging GitHub PRs **#5**, **#6**, or **#7**.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.
