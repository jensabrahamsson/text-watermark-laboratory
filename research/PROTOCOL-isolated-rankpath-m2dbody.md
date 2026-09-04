# Isolated-file protocol (gpt2-medium LM rankpath body window [4:16) on Distil 12)

This is a **methods freeze** for 12-LOO rankpath on already frozen
DistilGPT2 12×4 twins, with **gpt2-medium** as the unmarked LM, scoring
only generated tokens `[4:16)`. It does not add a scorer. Existing
`rankpath` only. Same GPT-2 BPE. gpt2-medium LM opening `[0:4)` on these
twins is **9/12**, isolated **30/48 vs 33/48**
([PROTOCOL-isolated-rankpath-m2d.md](PROTOCOL-isolated-rankpath-m2d.md)).
Distil native `[4:16)` is **9/12**, isolated **25/48 vs 30/48**
([PROTOCOL-isolated-rankpath-d12body.md](PROTOCOL-isolated-rankpath-d12body.md)).
GPT-2-on-Distil `[4:16)` is **4/12**, isolated **26/48 vs 21/48**
([PROTOCOL-isolated-rankpath-g2dbody.md](PROTOCOL-isolated-rankpath-g2dbody.md)).
This freeze asks whether gpt2-medium ranks on Distil twins still
classify isolated files after the first four generated tokens.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from this
file.
Do **not** look at medium-on-Distil rankpath `[4:16)` LRs until this
freeze is named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has
been run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice. Do **not** apply
leftover-15 keys. Do **not** merge GitHub PR **#9**.
Do **not** pass `--rankpath-full`. Do **not** score original GPT-2 twins
or gpt2-medium twins in this dump.

## Why freeze now

gpt2-medium LM opening on Distil 12 is ranking **9/12**, isolated
**30/48 vs 33/48**. Distil native `[4:16)` equality with **25/48** is
not a win. GPT-2-on-medium `[4:16)` **28/48** is not a win. Isolated-file
remains open. Occupancy leftover is closed. Existing Distil twins.
Existing `rankpath`. Existing `--windows`. Not a leftover re-slice. This
is the last GPT-2-family 3×3 body-window cell.

## Primary scientific question

Under leave-one-prompt-out gpt2-medium-LM rankpath on `[4:16)`, with no
detector keys, `hash_iv`, or g-values, do gpt2-medium ranks classify
Distil 12×4 finished strings after the opening four tokens, and does
isolated `lr>0` beat hard **25/48**?

Not: leftover-15. Not: another `probe --methods` name. Not: original
GPT-2 twins. Not: lock A.

## Frozen scorers

`--model gpt2-medium --methods rankpath --fit-prefix 16 --pos-bucket 1
--skip-hashpool --windows 4:16`. Do **not** pass `--rankpath`. Do **not**
leftover-slice.

## Hypotheses (stated before these LRs)

- **H-rpm2dbody.** gpt2-medium unmarked-LM rankpath on Distil generated
  tokens `[4:16)` isolated marked `lr>0` does not beat hard **25/48**.
  Opening on these twins is **30/48 vs 33/48**. Distil native `[4:16)` is
  **25/48 vs 30/48**. GPT-2-on-Distil `[4:16)` is **26/48 vs 21/48**. A
  higher count is not leftover-15 recall and does not replace **25/48**.
  Equality with **25/48** is not a win.
- **H-rpm2dbody-iso.** A medium-on-Distil body-window rankpath is not a
  universal isolated-file detector. Do not sell that isolated count,
  medium-on-Distil opening **30/48**, Distil native `[4:16)` **25/48**,
  GPT-2-on-Distil `[4:16)` **26/48**, GPT-2-on-medium `[4:16)` **28/48**,
  leftover official **15/15**, or PR **#9** last-2 **29/48** as replacing
  **25/48**. Do not leftover-slice. Do not merge PR **#9**.

## Primary endpoint

Isolated t=0 / 48 on the `[4:16)` window dump. Prompt ranking / 12
secondary. `used_keys` false. `model_name` must be `gpt2-medium`.
Equality with **25/48** is not a win. The unwindowed fit-prefix-16 file
score is not the frozen slice.

## Corpus

| Role | Path |
|---|---|
| Twins | `experiments/2026-08-31-pair-distilgpt2-12x4/` |
| medium-on-Distil opening `[0:4)` control | `experiments/2026-09-04-probe-distil-12x4-rankpath-medium-lm/` |
| Distil native `[4:16)` control | `experiments/2026-09-04-probe-distil-12x4-rankpath-w4-16/window-4-16/` |
| GPT-2-on-Distil `[4:16)` control | `experiments/2026-09-04-probe-distil-12x4-rankpath-gpt2-w4-16/window-4-16/` |
| Probe dump | `experiments/2026-09-04-probe-distil-12x4-rankpath-medium-w4-16/` |

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-distilgpt2-12x4 \
  --model gpt2-medium --skip-hashpool \
  --fit-prefix 16 --pos-bucket 1 --methods rankpath \
  --windows 4:16 \
  --out-dir experiments/2026-09-04-probe-distil-12x4-rankpath-medium-w4-16
```

Do not change flags after the first run. Do not look at those LRs until
the logbook names this SHA.

## What this protocol refuses

- New `probe --methods` names on 12×4 / 36×4 twins.
- Leftover targeting or leftover-15 keys.
- family-12 paraphrases after leftover peeking.
- Mixing grok12 into any train.
- Original GPT-2 twins or gpt2-medium twins in this dump. `--rankpath-full`
  on this dump.
- Merging PR **#5**, **#6**, **#7**, **#8**, or **#9**.
- Selling any of these isolated counts as replacing **25/48**.
- Key recovery. Paid chat APIs. Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe once.
4. Do not add a scorer.

## Results

H-rpm2dbody **fails** as a raw count. gpt2-medium unmarked-LM rankpath on
Distil generated tokens `[4:16)` ranks **9/12**; isolated **32/48 vs 25/48**
(AUC **0.626**; nested-by-stem Youden **21/48 vs 31/48**).
`used_keys=false`. `model_name` is `gpt2-medium`. Clopper–Pearson 95% on
**32/48** excludes ½. Medium-on-Distil opening `[0:4)` stays **9/12**,
isolated **30/48 vs 33/48**. Distil native `[4:16)` stays **9/12**,
isolated **25/48 vs 30/48**. GPT-2-on-Distil `[4:16)` stays **4/12**,
isolated **26/48 vs 21/48**. The unwindowed fit-prefix-16 file score on
this run is **9/12**, isolated **28/48 vs 31/48**; that is not the frozen
slice and is not the locked headline **25/48**. Do not sell **32/48**,
**9/12**, or parent **28/48**. JSON:
[experiments/2026-09-04-probe-distil-12x4-rankpath-medium-w4-16/window-4-16/](../experiments/2026-09-04-probe-distil-12x4-rankpath-medium-w4-16/window-4-16/).

H-rpm2dbody-iso **holds**. Isolated **32/48** is seven files above hard
**25/48** and is not a universal isolated-file detector. Do not
leftover-slice. Do not merge PR **#9**. Isolated-file remains open. Do
not write `thesis/`.
