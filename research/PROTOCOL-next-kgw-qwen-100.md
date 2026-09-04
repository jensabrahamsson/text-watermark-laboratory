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

## Results

Protocol SHA `ed9fb20`. Named `7db0674`. Pair seed **20260904**.
`mixin=kgw`. `model=Qwen/Qwen2-1.5B-Instruct`. `used_keys=false`.
Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`. First `pair` died
after 44 complete stems; same flags resumed (pid 44722). Complete
stems were re-scored.

Pair dump: [experiments/2026-09-04-pair-qwen-100x4-kgw/](../experiments/2026-09-04-pair-qwen-100x4-kgw/).
Probe dump: [experiments/2026-09-04-probe-qwen-100x4-kgw-hard-last4/](../experiments/2026-09-04-probe-qwen-100x4-kgw-hard-last4/).

H-kgw-q100-ctrl **fails** as the preregistered every-first-draw 100/100.
Official matching z-score is above $3.0$ on **90/100** first marked files
(min passer $3.33$). Unmarked first-draw is **0/100** above $3.0$
(max $2.10$). Mixin is on. Ten misses (stems 003, 017, 021, 033, 041,
058, 065, 069, 081, 097) are Chinese quiz-format completions, not empty
files. Not a GPT-2 tokenizer bug (`--model Qwen/Qwen2-1.5B-Instruct`).
Do not sell **90/100**.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **96/100** | 0.870 | 346/400 | 274/400 | 346 54 274 126 | **620/800** |
| hard last-4 | **63/100** | 0.562 | 290/400 | 140/400 | 290 110 140 260 | **430/800** |

GPT-2 Kirchenbauer interpolate on these prompt *strings* (different
twins) was **100/100** / **747/800**. Distil interpolate is **100/100** /
**683/800**. Qwen interpolate is **96/100**. Mean $D_p=0.486$
(interpolate) / $0.064$ (hard). Zero ranking wins have 0 isolated TPs.
Four ranking losses have isolated TPs (017, 045, 069, 071).

Clopper–Pearson 95% (not a second freeze): interpolate **96/100** is
**[0.901, 0.989]** and does not include ½; hard **63/100** is
**[0.528, 0.724]**; BA **620/800** is **[0.744, 0.804]**. Isolated
**25/48** still includes ½.

H-kgw-q100-group **holds** as an informative comparison with GPT-2
Kirchenbauer **100/100** and Distil **100/100**. It does not replace
**25/48**.

H-kgw-q100-iso **holds**. Isolated interpolate **620/800** is a different
generator and mixin from the original-12 SynthID **47/96**. Do not sell
**96/100**, **63/100**, **620/800**, or **430/800** as replacing
**25/48**.

H-kgw-q100-occ **holds**. Leave-one-family-out interpolate atoms
(`atoms --leave-one-out`; `used_keys=false`). File LRs match
interpolate holdout (marked `lr>0` **346/400**). Exact next-token
overlap is **4858** seen versus **96740** unseen (opening $[0{:}4)$ is
1319 versus 1081). The top opening atom is `'A' '.' → ' �'` (n=25;
quiz-format). Occupancy is a mechanistic intermediate, not a detector.
Do not sell **4858** or `'A.'` as replacing **25/48**.

JSON: [experiments/2026-09-04-atoms-qwen-100x4-kgw/](../experiments/2026-09-04-atoms-qwen-100x4-kgw/).

Isolated-file detection on the public SynthID original-12 remains
**25/48** / **47/96**. Do not write `thesis/`.
