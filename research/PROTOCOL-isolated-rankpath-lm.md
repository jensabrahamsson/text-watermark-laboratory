# Isolated-file protocol (Distil / gpt2-medium unmarked-LM opening rankpath)

This is a **methods freeze** for opening rankpath 12-LOO on the original
GPT-2 12×4 twins when the unmarked LM is **not** GPT-2-small. It does
not add a scorer. Existing `rankpath` only. Same GPT-2 BPE. The files
are already frozen (`experiments/2026-08-17-pair-12x4/`). DistilGPT2
and gpt2-medium are the unmarked LMs that assign five-symbol ranks.
They are **not** new generators of these twins.

Occupancy-free leftover-15 is closed
([PROTOCOL-isolated-leftover-15-closed.md](PROTOCOL-isolated-leftover-15-closed.md)).
Leftover-18 published key-free readers are exhausted
([PROTOCOL-isolated-leftover-18-closed.md](PROTOCOL-isolated-leftover-18-closed.md)).
Count tables cannot copy leftover unique openings without targeting.
Opening rankpath does not use token identity
([key-free-rankpath.md](key-free-rankpath.md)). GPT-2-small opening
rankpath on these twins is already opened (**11/12**, isolated
**41/48 vs 35/48** after the recount). Distil *native* opening
rankpath (Distil LM on Distil twins) is chance (**8/12**, AUC
**0.579**). This freeze asks whether isolated rankpath on the original
GPT-2 files still fires when the rank LM is DistilGPT2 or gpt2-medium.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from this
file.
Do **not** look at Distil-LM or gpt2-medium-LM rankpath LRs until this
freeze is named in [LOGBOOK.md](LOGBOOK.md) and the analysis commands
have been run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice these holdouts.
Do **not** target leftover-15 openings after peeking. Do **not** apply
leftover-15 or leftover-18 keys. Do **not** merge GitHub PR **#9**.
Do **not** start these probes while the Qwen Kirchenbauer 100 `pair`
holds the CPU.

## Why freeze now

Isolated-file detection is still not finished. Occupancy-free leftover
unions are closed. Mask-*k* absolute remasure is opened
([PROTOCOL-isolated-mask-absolute.md](PROTOCOL-isolated-mask-absolute.md)).
PR **#9** last-1 / last-2 hits on public SynthID original-12 stay
**unmerged**; last-2 hits **29/48** (AUC **0.632**) does not replace
**25/48**, and last-1 hits **24/48** (AUC **0.445**) is worse. Those
are inspected dumps, not this freeze. Kirchenbauer last-1 hits
**46/48** is a different mixin (`context_width=1` body leak), not
SynthID isolated-file detection.

The remaining honesty item that is not leftover targeting is whether
opening rankpath on the original GPT-2 12 needs the **sampler's**
unmarked LM. GPT-2-small ranks GPT-2 tournament draws. DistilGPT2 and
gpt2-medium share BPE with GPT-2 and already exist as local Hugging
Face models. No new `pair`. Existing `rankpath` method. Not a leftover
re-slice of published holdouts.

## Primary scientific question

Under leave-one-prompt-out opening rankpath, with no detector keys,
`hash_iv`, or g-values, do DistilGPT2 ranks and gpt2-medium ranks
classify the original GPT-2 12×4 finished strings, and does either
isolated `lr>0` beat hard **25/48**?

Not: leftover-15. Not: leftover-18 re-slices. Not: another
`probe --methods` name. Not: Distil native twins. Not: lock A
interpolate. Not: PR **#9** last-k hits.

## Frozen scorers

Existing opening rankpath only. No new method names. Lock C flags.

| Arm | Unmarked LM | `--model` |
|---|---|---|
| Distil LM | DistilGPT2 | `distilgpt2` |
| medium LM | gpt2-medium | `gpt2-medium` |

| Lock | Reader | Flags |
|---|---|---|
| C | Opening rankpath | `--methods rankpath --fit-prefix 4 --pos-bucket 1` |

`--skip-hashpool`. Do **not** pass `--rankpath` (that also emits default
count methods). Do **not** run lock A interpolate. Do **not** leftover-slice.
Probe has no `--hub-revision`; local Hugging Face weights. Distil
generation pin `2290a62682d06624634c1f46a6ad5be0f47f38aa` is not this
scoring run. Same BPE as GPT-2 (`is_gpt2_name`).

## Hypotheses (stated before Distil-LM / medium-LM rankpath LRs)

- **H-rplm-d.** DistilGPT2 unmarked-LM opening rankpath isolated marked
  `lr>0` does not beat hard **25/48**. Distil native opening rankpath is
  chance (**8/12**, AUC **0.579**). Ranks from a model that did not
  sample the twins are not the sampler's tournament.
- **H-rplm-m.** gpt2-medium unmarked-LM opening rankpath isolated marked
  `lr>0` does not beat hard **25/48**. Same BPE, larger GPT-2 family.
  A higher in-domain count is not leftover-15 recall and does not
  replace **25/48**.
- **H-rplm-iso.** Distil-LM / medium-LM opening rankpath is not a
  universal isolated-file detector. Do not sell those isolated counts,
  GPT-2-small opening rankpath **41/48**, nested-by-stem **37/48 vs
  41/48**, leftover last-4 **9/15**, leftover official **15/15**, PR
  **#9** last-2 hits **29/48**, or Kirchenbauer last-1 **46/48** as
  replacing **25/48**. Do not leftover-slice these holdouts. Do not
  merge PR **#9**.

## Primary endpoint

Isolated t=0: marked `n_marked_lr_positive` / 48 and unmarked
`n_unmarked_lr_nonpositive` / 48 on each arm. Prompt ranking
`n_prompts_marked_above` / 12 is secondary. `used_keys` must be false.
`model_name` must be `distilgpt2` on the Distil arm and `gpt2-medium`
on the medium arm. Equality with **25/48** is not a win.

GPT-2-small recount
(`experiments/2026-09-01-probe-12x4-recount-opening-rankpath/`) stays
the same-LM control. Do not overwrite it.

## Corpus

No new `pair`. Original 12 GPT-2 twins.

| Role | Path |
|---|---|
| Twins | `experiments/2026-08-17-pair-12x4/` |
| Prompts | `experiments/2026-08-17-grok-prompts/` |
| Same-LM control | `experiments/2026-09-01-probe-12x4-recount-opening-rankpath/` |
| Distil-LM dump | `experiments/2026-09-04-probe-12x4-rankpath-distil-lm/` |
| medium-LM dump | `experiments/2026-09-04-probe-12x4-rankpath-medium-lm/` |

## Analysis commands

Do not change flags after the first run. Do not look at Distil-LM or
medium-LM rankpath LRs until the logbook names this SHA. Do not start
while `experiments/2026-09-04-pair-qwen-100x4-kgw/` is still generating.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --model distilgpt2 --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 --methods rankpath \
  --out-dir experiments/2026-09-04-probe-12x4-rankpath-distil-lm

python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --model gpt2-medium --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 --methods rankpath \
  --out-dir experiments/2026-09-04-probe-12x4-rankpath-medium-lm
```

## What this protocol refuses

- New `probe --methods` names on the original 12×4 / 36×4 twins.
- Leftover-15 / leftover-18 re-slices of these or published holdouts.
- Targeting leftover-15 openings after peeking.
- family-12 paraphrases of the original 12 after leftover peeking.
- Mixing grok12 into any train.
- `--rankpath` (emits default count methods).
- Lock A interpolate on Distil or gpt2-medium twins.
- Distil ∪ gpt2-medium occupancy-free union.
- Starting these probes while the Qwen Kirchenbauer 100 `pair` holds
  the CPU.
- Merging GitHub PR **#5**, **#6**, **#7**, **#8**, or **#9**.
- Copying PR **#9** `/tmp` holdouts into this dump.
- Selling Distil-LM rankpath, medium-LM rankpath, GPT-2-small
  **41/48**, PR **#9** last-2 **29/48**, Kirchenbauer last-1 **46/48**,
  leftover official **15/15**, or leftover last-4 **9/15** as replacing
  **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the two probe commands above once, after the Qwen Kirchenbauer
   100 `pair` releases the CPU.
4. Do not add a scorer.

Human merge of PR **#9** is out of scope for this file.

## Results

H-rplm-d **fails** as a raw count. DistilGPT2 unmarked-LM opening
rankpath on the original GPT-2 12×4 ranks **10/12**; isolated
**32/48 vs 31/48** (AUC **0.761**; nested-by-stem Youden
**28/48 vs 37/48**). `used_keys=false`. `model_name` is `distilgpt2`.
Clopper–Pearson 95% on **32/48** excludes ½. Same-LM GPT-2-small
recount stays **41/48 vs 35/48**. Distil native opening rankpath on
Distil twins stays chance (**8/12**, AUC **0.579**). Do not sell **32/48**.
JSON:
[experiments/2026-09-04-probe-12x4-rankpath-distil-lm/](../experiments/2026-09-04-probe-12x4-rankpath-distil-lm/).

H-rplm-m **fails** as a raw count. gpt2-medium unmarked-LM opening
rankpath on the original GPT-2 12×4 ranks **10/12**; isolated
**31/48 vs 32/48** (AUC **0.679**; nested-by-stem Youden
**31/48 vs 30/48**). `used_keys=false`. `model_name` is `gpt2-medium`.
Clopper–Pearson 95% on **31/48** includes ½. Do not sell **31/48**.
JSON:
[experiments/2026-09-04-probe-12x4-rankpath-medium-lm/](../experiments/2026-09-04-probe-12x4-rankpath-medium-lm/).

H-rplm-iso **holds**. Distil-LM **32/48** and medium-LM **31/48** are
not a universal isolated-file detector. Same-LM GPT-2-small remains
**41/48 vs 35/48**. Do not leftover-slice. Do not merge PR **#9**.
Isolated-file remains open. Do not write `thesis/`.
