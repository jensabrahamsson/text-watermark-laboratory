# Isolated-file protocol (Distil LM rankpath body window [4:16) on gpt2-medium 12)

This is a **methods freeze** for 12-LOO rankpath on already frozen
gpt2-medium 12×4 twins, with **DistilGPT2** as the unmarked LM, scoring
only generated tokens `[4:16)`. It does not add a scorer. Existing
`rankpath` only. Same GPT-2 BPE. Distil LM opening `[0:4)` on these
twins is **11/12**, isolated **30/48 vs 31/48**
([PROTOCOL-isolated-rankpath-d2m.md](PROTOCOL-isolated-rankpath-d2m.md)).
gpt2-medium native `[4:16)` is **6/12**, isolated **20/48 vs 30/48**
([PROTOCOL-isolated-rankpath-m12body.md](PROTOCOL-isolated-rankpath-m12body.md)).
This freeze asks whether Distil ranks on gpt2-medium twins still
classify isolated files after the first four generated tokens.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from this
file.
Do **not** look at Distil-on-medium rankpath `[4:16)` LRs until this
freeze is named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has
been run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice. Do **not** apply
leftover-15 keys. Do **not** merge GitHub PR **#9**.
Do **not** pass `--rankpath-full`. Do **not** score original GPT-2 twins
in this dump.

## Why freeze now

Distil LM opening on gpt2-medium 12 is ranking **11/12**, isolated
**30/48 vs 31/48**. gpt2-medium native `[4:16)` is chance AUC **0.497**.
Isolated-file remains open. Occupancy leftover is closed. Existing
medium twins. Existing `rankpath`. Existing `--windows`. Not a leftover
re-slice.

## Primary scientific question

Under leave-one-prompt-out Distil-LM rankpath on `[4:16)`, with no
detector keys, `hash_iv`, or g-values, do Distil ranks classify
gpt2-medium 12×4 finished strings after the opening four tokens, and
does isolated `lr>0` beat hard **25/48**?

Not: leftover-15. Not: another `probe --methods` name. Not: original
GPT-2 twins. Not: lock A.

## Frozen scorers

`--model distilgpt2 --methods rankpath --fit-prefix 16 --pos-bucket 1
--skip-hashpool --windows 4:16`. Do **not** pass `--rankpath`. Do **not**
leftover-slice.

## Hypotheses (stated before these LRs)

- **H-rpd2mbody.** Distil unmarked-LM rankpath on gpt2-medium generated
  tokens `[4:16)` isolated marked `lr>0` does not beat hard **25/48**.
  Opening on these twins is **30/48 vs 31/48**. Medium native `[4:16)` is
  **20/48 vs 30/48**. A higher count is not leftover-15 recall and does
  not replace **25/48**. Equality with **25/48** is not a win.
- **H-rpd2mbody-iso.** A Distil-on-medium body-window rankpath is not a
  universal isolated-file detector. Do not sell that isolated count,
  Distil-on-medium opening **30/48**, medium native `[4:16)` **20/48**,
  leftover official **15/15**, or PR **#9** last-2 **29/48** as replacing
  **25/48**. Do not leftover-slice. Do not merge PR **#9**.

## Primary endpoint

Isolated t=0 / 48 on the `[4:16)` window dump. Prompt ranking / 12
secondary. `used_keys` false. `model_name` must be `distilgpt2`.
Equality with **25/48** is not a win. The unwindowed fit-prefix-16 file
score is not the frozen slice.

## Corpus

| Role | Path |
|---|---|
| Twins | `experiments/2026-09-01-pair-gpt2-medium-12x4/` |
| Distil-on-medium opening `[0:4)` control | `experiments/2026-09-04-probe-medium-12x4-rankpath-distil-lm/` |
| medium native `[4:16)` control | `experiments/2026-09-04-probe-medium-12x4-rankpath-w4-16/window-4-16/` |
| Probe dump | `experiments/2026-09-04-probe-medium-12x4-rankpath-distil-w4-16/` |

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-gpt2-medium-12x4 \
  --model distilgpt2 --skip-hashpool \
  --fit-prefix 16 --pos-bucket 1 --methods rankpath \
  --windows 4:16 \
  --out-dir experiments/2026-09-04-probe-medium-12x4-rankpath-distil-w4-16
```

Do not change flags after the first run. Do not look at those LRs until
the logbook names this SHA.

## What this protocol refuses

- New `probe --methods` names on 12×4 / 36×4 twins.
- Leftover targeting or leftover-15 keys.
- family-12 paraphrases after leftover peeking.
- Mixing grok12 into any train.
- Original GPT-2 twins. `--rankpath-full` on this dump.
- Merging PR **#5**, **#6**, **#7**, **#8**, or **#9**.
- Selling any of these isolated counts as replacing **25/48**.
- Key recovery. Paid chat APIs. Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe once.
4. Do not add a scorer.

## Results

H-rpd2mbody **holds**. Distil unmarked-LM rankpath on gpt2-medium generated
tokens `[4:16)` ranks **11/12**; isolated **25/48 vs 33/48** (AUC **0.646**;
nested-by-stem Youden **36/48 vs 16/48** at a negative train threshold).
`used_keys=false`. `model_name` is `distilgpt2`. Clopper–Pearson 95% on
**25/48** includes ½. Equality with hard **25/48** is not a win.
Distil-on-medium opening stays **11/12**, isolated **30/48 vs 31/48**.
Medium native `[4:16)` stays **6/12**, isolated **20/48 vs 30/48**. The
unwindowed fit-prefix-16 file score is **11/12**, isolated **33/48 vs 33/48**;
that is not the frozen slice. Do not sell **25/48**, **11/12**, nested
**36/48**, or **33/48**. JSON:
[experiments/2026-09-04-probe-medium-12x4-rankpath-distil-w4-16/window-4-16/](../experiments/2026-09-04-probe-medium-12x4-rankpath-distil-w4-16/window-4-16/).

H-rpd2mbody-iso **holds**. Distil-on-medium opening **11/12** is a different
grain from isolated **25/48**. Do not leftover-slice. Do not merge PR **#9**.
Isolated-file remains open. Do not write `thesis/`.
