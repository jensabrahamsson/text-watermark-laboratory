# Isolated-file protocol (Distil native rankpath body window [4:16))

This is a **methods freeze** for 12-LOO rankpath on already frozen
DistilGPT2 12×4 twins, with **DistilGPT2** as the unmarked LM, scoring
only generated tokens `[4:16)`. It does not add a scorer. Existing
`rankpath` only. Same GPT-2 BPE. Distil native opening `[0:4)` on these
twins is **8/12**, isolated **28/48 vs 32/48**, AUC **0.579**
(`experiments/2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath/`).
Distil-LM `[4:16)` on the original GPT-2 twins is **6/12**, isolated
**24/48 vs 23/48**
([PROTOCOL-isolated-rankpath-dbody.md](PROTOCOL-isolated-rankpath-dbody.md)).
This freeze asks whether Distil ranks on Distil twins still classify
isolated files after the first four generated tokens.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from this
file.
Do **not** look at Distil native rankpath `[4:16)` LRs until this freeze
is named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice. Do **not** apply
leftover-15 keys. Do **not** merge GitHub PR **#9**.
Do **not** pass `--rankpath-full`. Do **not** score original GPT-2 twins
in this dump.

## Why freeze now

Distil native opening rankpath is chance. GPT-2-small, Distil-LM, and
gpt2-medium-LM `[4:16)` on the original GPT-2 12 are opened. Isolated-file
remains open. Occupancy leftover is closed. Existing Distil twins.
Existing `rankpath`. Existing `--windows`. Not a leftover re-slice.

## Primary scientific question

Under leave-one-prompt-out Distil native rankpath on `[4:16)`, with no
detector keys, `hash_iv`, or g-values, do Distil ranks classify Distil
12×4 finished strings after the opening four tokens, and does isolated
`lr>0` beat hard **25/48**?

Not: leftover-15. Not: another `probe --methods` name. Not: original
GPT-2 twins. Not: lock A.

## Frozen scorers

`--model distilgpt2 --methods rankpath --fit-prefix 16 --pos-bucket 1
--skip-hashpool --windows 4:16`. Do **not** pass `--rankpath`. Do **not**
leftover-slice.

## Hypotheses (stated before these LRs)

- **H-rpd12body.** Distil native rankpath on generated tokens `[4:16)`
  isolated marked `lr>0` does not beat hard **25/48**. Distil native
  opening is chance (**8/12**, AUC **0.579**, isolated **28/48 vs
  32/48**). Distil-LM `[4:16)` on GPT-2 twins is **24/48 vs 23/48**. A
  higher count is not leftover-15 recall and does not replace **25/48**.
- **H-rpd12body-iso.** A Distil native body-window rankpath is not a
  universal isolated-file detector. Do not sell that isolated count,
  Distil native opening **28/48**, Distil-LM `[4:16)` **24/48**,
  gpt2-medium-LM `[4:16)` **27/48**, leftover official **15/15**, or PR
  **#9** last-2 **29/48** as replacing **25/48**. Do not leftover-slice.
  Do not merge PR **#9**.

## Primary endpoint

Isolated t=0 / 48 on the `[4:16)` window dump. Prompt ranking / 12
secondary. `used_keys` false. `model_name` must be `distilgpt2`.
Equality with **25/48** is not a win. The unwindowed fit-prefix-16 file
score is not the frozen slice.

## Corpus

| Role | Path |
|---|---|
| Twins | `experiments/2026-08-31-pair-distilgpt2-12x4/` |
| Distil native opening `[0:4)` control | `experiments/2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath/` |
| Distil-LM `[4:16)` on GPT-2 12 control | `experiments/2026-09-04-probe-12x4-rankpath-distil-w4-16/window-4-16/` |
| Probe dump | `experiments/2026-09-04-probe-distil-12x4-rankpath-w4-16/` |

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-distilgpt2-12x4 \
  --model distilgpt2 --skip-hashpool \
  --fit-prefix 16 --pos-bucket 1 --methods rankpath \
  --windows 4:16 \
  --out-dir experiments/2026-09-04-probe-distil-12x4-rankpath-w4-16
```

Do not change flags after the first run. Do not look at those LRs until
the logbook names this SHA.

## What this protocol refuses

- New `probe --methods` names on 12×4 / 36×4 twins.
- Leftover targeting or leftover-15 keys.
- family-12 paraphrases after leftover peeking.
- Mixing grok12 into any train.
- Original GPT-2 twins in this dump. `--rankpath-full` on this dump.
- Merging PR **#5**, **#6**, **#7**, **#8**, or **#9**.
- Selling any of these isolated counts as replacing **25/48**.
- Key recovery. Paid chat APIs. Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe once.
4. Do not add a scorer.

## Results

H-rpd12body **holds**. Distil native rankpath on generated tokens
`[4:16)` ranks **9/12**; isolated **25/48 vs 30/48** (AUC **0.630**;
nested-by-stem Youden **33/48 vs 21/48** at a negative train threshold).
`used_keys=false`. `model_name` is `distilgpt2`. Clopper–Pearson 95% on
**25/48** includes ½. Equality with hard **25/48** is not a win. Distil
native opening `[0:4)` stays **8/12**, isolated **28/48 vs 32/48**.
Distil-LM `[4:16)` on GPT-2 twins stays **6/12**, isolated
**24/48 vs 23/48**. The unwindowed fit-prefix-16 file score on this run
is **9/12**, isolated **26/48 vs 26/48**; that is not the frozen slice.
Do not sell **25/48**, **9/12**, nested **33/48**, or **26/48**. JSON:
[experiments/2026-09-04-probe-distil-12x4-rankpath-w4-16/window-4-16/](../experiments/2026-09-04-probe-distil-12x4-rankpath-w4-16/window-4-16/).

H-rpd12body-iso **holds**. Distil native opening chance does not become a
universal isolated-file detector in `[4:16)`. Do not leftover-slice. Do
not merge PR **#9**. Isolated-file remains open. Do not write `thesis/`.
