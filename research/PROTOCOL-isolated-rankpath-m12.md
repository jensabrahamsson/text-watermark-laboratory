# Isolated-file protocol (gpt2-medium native opening rankpath)

This is a **methods freeze** for opening rankpath 12-LOO on the already
frozen gpt2-medium 12×4 twins, with gpt2-medium as the unmarked LM.
It does not add a scorer. Existing `rankpath` only. Same GPT-2 BPE.
The files are gpt2-medium generations of the original 12 Grok seeds
(`experiments/2026-09-01-pair-gpt2-medium-12x4/`). Leftover-15 keys
name GPT-2 files and must not be applied here.

Distil *native* opening rankpath (Distil LM on Distil twins) is chance
(**8/12**, AUC **0.579**, isolated **28/48 vs 32/48**). GPT-2-small
native opening rankpath on GPT-2 twins is **11/12**, isolated
**41/48 vs 35/48**. Distil LM and gpt2-medium LM scoring those GPT-2
twins is [PROTOCOL-isolated-rankpath-lm.md](PROTOCOL-isolated-rankpath-lm.md):
Distil-LM **32/48 vs 31/48**, medium-LM **31/48 vs 32/48**. This freeze
asks whether opening rankpath still fires when sampler and rank LM are
both gpt2-medium.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from this
file.
Do **not** look at gpt2-medium native rankpath LRs until this freeze is
named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice these holdouts.
Do **not** target leftover-15 openings after peeking. Do **not** apply
leftover-15 or leftover-18 GPT-2 keys. Do **not** merge GitHub PR **#9**.
Do **not** run lock A interpolate on gpt2-medium twins.

## Why freeze now

Occupancy-free leftover unions are closed. Distil/medium unmarked-LM
rankpath on GPT-2 twins is opened. Distil native opening rankpath is
chance. Isolated-file detection is still not finished. The remaining
honesty item that is not leftover targeting is whether gpt2-medium
native opening rankpath on gpt2-medium 12×4 beats hard **25/48**.
Existing twins. Existing `rankpath`. Not a leftover re-slice. Not a
new method name. Occupancy-free gpt2-medium→gpt2-medium was
**10/48** ([PROTOCOL-isolated-m12.md](PROTOCOL-isolated-m12.md)).

## Primary scientific question

Under leave-one-prompt-out opening rankpath, with no detector keys,
`hash_iv`, or g-values, do gpt2-medium ranks classify gpt2-medium 12×4
finished strings, and does isolated `lr>0` beat hard **25/48**?

Not: leftover-15. Not: leftover-18 re-slices. Not: another
`probe --methods` name. Not: lock A interpolate. Not: Distil LM on
GPT-2 twins.

## Frozen scorers

Existing opening rankpath only. No new method names.

| Arm | Twins | Unmarked LM | `--model` |
|---|---|---|---|
| medium native | gpt2-medium 12×4 | gpt2-medium | `gpt2-medium` |

| Lock | Reader | Flags |
|---|---|---|
| C | Opening rankpath | `--methods rankpath --fit-prefix 4 --pos-bucket 1` |

`--skip-hashpool`. Do **not** pass `--rankpath` (that also emits default
count methods). Do **not** leftover-slice. Probe has no `--hub-revision`.
Same BPE (`is_gpt2_name`).

## Hypotheses (stated before gpt2-medium native rankpath LRs)

- **H-rpm12.** gpt2-medium native opening rankpath isolated marked
  `lr>0` does not beat hard **25/48**. Distil native is chance
  (**8/12**, isolated **28/48 vs 32/48**). A higher in-domain count is
  not leftover-15 recall and does not replace **25/48**.
- **H-rpm12-iso.** gpt2-medium native opening rankpath is not a
  universal isolated-file detector. Do not sell that isolated count,
  Distil native **28/48**, Distil-LM-on-GPT-2 **32/48**, medium-LM-on-GPT-2
  **31/48**, GPT-2-small **41/48**, leftover last-4 **9/15**, leftover
  official **15/15**, or PR **#9** last-2 hits **29/48** as replacing
  **25/48**. Do not leftover-slice. Do not merge PR **#9**.

## Primary endpoint

Isolated t=0: marked `n_marked_lr_positive` / 48 and unmarked
`n_unmarked_lr_nonpositive` / 48. Prompt ranking
`n_prompts_marked_above` / 12 is secondary. `used_keys` must be false.
`model_name` must be `gpt2-medium`. Equality with **25/48** is not a
win.

## Corpus

No new `pair`.

| Role | Path |
|---|---|
| Twins | `experiments/2026-09-01-pair-gpt2-medium-12x4/` |
| Prompts | `experiments/2026-08-17-grok-prompts/` |
| Distil native control | `experiments/2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath/` |
| Probe dump | `experiments/2026-09-04-probe-medium-12x4-rankpath-native/` |

## Analysis command

Do not change flags after the first run. Do not look at gpt2-medium
native rankpath LRs until the logbook names this SHA.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-gpt2-medium-12x4 \
  --model gpt2-medium --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 --methods rankpath \
  --out-dir experiments/2026-09-04-probe-medium-12x4-rankpath-native
```

## What this protocol refuses

- New `probe --methods` names on the original 12×4 / 36×4 twins.
- Leftover-15 / leftover-18 re-slices.
- Targeting leftover-15 openings after peeking.
- family-12 paraphrases of the original 12 after leftover peeking.
- Mixing grok12 into any train.
- `--rankpath` (emits default count methods).
- Lock A interpolate on gpt2-medium twins.
- Applying leftover-15 GPT-2 keys to gpt2-medium 12 files.
- Merging GitHub PR **#5**, **#6**, **#7**, **#8**, or **#9**.
- Selling gpt2-medium native rankpath, Distil native **28/48**,
  Distil-LM **32/48**, medium-LM-on-GPT-2 **31/48**, GPT-2-small
  **41/48**, leftover official **15/15**, or leftover last-4 **9/15**
  as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe command above once.
4. Do not add a scorer.

Human merge of PR **#9** is out of scope for this file.

## Results

H-rpm12 **holds**. gpt2-medium native opening rankpath on gpt2-medium
12×4 ranks **6/12**; isolated **22/48 vs 30/48** (AUC **0.641**;
nested-by-stem Youden **19/48 vs 31/48**). `used_keys=false`.
`model_name` is `gpt2-medium`. Clopper–Pearson 95% on **22/48**
includes ½. Distil native stays **8/12**, isolated **28/48 vs 32/48**.
Do not sell **22/48** or **6/12**. JSON:
[experiments/2026-09-04-probe-medium-12x4-rankpath-native/](../experiments/2026-09-04-probe-medium-12x4-rankpath-native/).

H-rpm12-iso **holds**. gpt2-medium native opening rankpath is not a
universal isolated-file detector. Do not leftover-slice. Do not merge
PR **#9**. Isolated-file remains open. Do not write `thesis/`.
