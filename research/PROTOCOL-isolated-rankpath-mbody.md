# Isolated-file protocol (gpt2-medium-LM rankpath body window [4:16))

This is a **methods freeze** for 12-LOO rankpath on already frozen
original GPT-2 12×4 twins, with **gpt2-medium** as the unmarked LM,
scoring only generated tokens `[4:16)`. It does not add a scorer.
Existing `rankpath` only. Same GPT-2 BPE. gpt2-medium-LM opening
`[0:4)` on these twins is **10/12**, isolated **31/48 vs 32/48**
([PROTOCOL-isolated-rankpath-lm.md](PROTOCOL-isolated-rankpath-lm.md)).
GPT-2-small `[4:16)` is **7/12**, isolated **20/48 vs 22/48**, AUC
**0.430**. Distil-LM `[4:16)` is **6/12**, isolated **24/48 vs 23/48**,
AUC **0.447**. This freeze asks whether gpt2-medium ranks on the same
twins still classify isolated files after the first four generated
tokens.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from this
file.
Do **not** look at gpt2-medium-LM rankpath `[4:16)` LRs until this freeze
is named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice. Do **not** apply
leftover-15 keys. Do **not** merge GitHub PR **#9**.
Do **not** pass `--rankpath-full`. Do **not** run gpt2-medium native
twins.

## Why freeze now

GPT-2-small and Distil-LM `[4:16)` on these twins are below chance.
gpt2-medium-LM opening `[0:4)` is **31/48 vs 32/48**. Isolated-file
remains open. Occupancy leftover is closed. Existing twins. Existing
`rankpath`. Existing `--windows`. Not a leftover re-slice.

## Primary scientific question

Under leave-one-prompt-out gpt2-medium-LM rankpath on `[4:16)`, with no
detector keys, `hash_iv`, or g-values, do gpt2-medium ranks classify the
original GPT-2 12×4 finished strings after the opening four tokens, and
does isolated `lr>0` beat hard **25/48**?

Not: leftover-15. Not: another `probe --methods` name. Not: gpt2-medium
native twins. Not: lock A.

## Frozen scorers

`--model gpt2-medium --methods rankpath --fit-prefix 16 --pos-bucket 1
--skip-hashpool --windows 4:16`. Do **not** pass `--rankpath`. Do **not**
leftover-slice.

## Hypotheses (stated before these LRs)

- **H-rpmbody.** gpt2-medium unmarked-LM rankpath on generated tokens
  `[4:16)` isolated marked `lr>0` does not beat hard **25/48**.
  gpt2-medium-LM opening is **31/48 vs 32/48**. GPT-2-small `[4:16)` is
  **20/48 vs 22/48**. Distil-LM `[4:16)` is **24/48 vs 23/48**. A higher
  count is not leftover-15 recall and does not replace **25/48**.
- **H-rpmbody-iso.** A gpt2-medium-LM body-window rankpath is not a
  universal isolated-file detector. Do not sell that isolated count,
  medium-LM opening **31/48**, Distil-LM `[4:16)` **24/48**, GPT-2
  `[4:16)` **20/48**, leftover official **15/15**, or PR **#9** last-2
  **29/48** as replacing **25/48**. Do not leftover-slice. Do not merge
  PR **#9**.

## Primary endpoint

Isolated t=0 / 48 on the `[4:16)` window dump. Prompt ranking / 12
secondary. `used_keys` false. `model_name` must be `gpt2-medium`.
Equality with **25/48** is not a win. The unwindowed fit-prefix-16 file
score is not the frozen slice.

## Corpus

| Role | Path |
|---|---|
| Twins | `experiments/2026-08-17-pair-12x4/` |
| medium-LM opening `[0:4)` control | `experiments/2026-09-04-probe-12x4-rankpath-medium-lm/` |
| Distil-LM `[4:16)` control | `experiments/2026-09-04-probe-12x4-rankpath-distil-w4-16/window-4-16/` |
| GPT-2 `[4:16)` control | `experiments/2026-09-04-probe-12x4-rankpath-w4-16/window-4-16/` |
| Probe dump | `experiments/2026-09-04-probe-12x4-rankpath-medium-w4-16/` |

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --model gpt2-medium --skip-hashpool \
  --fit-prefix 16 --pos-bucket 1 --methods rankpath \
  --windows 4:16 \
  --out-dir experiments/2026-09-04-probe-12x4-rankpath-medium-w4-16
```

Do not change flags after the first run. Do not look at those LRs until
the logbook names this SHA.

## What this protocol refuses

- New `probe --methods` names on 12×4 / 36×4 twins.
- Leftover targeting or leftover-15 keys.
- family-12 paraphrases after leftover peeking.
- Mixing grok12 into any train.
- gpt2-medium native twins. `--rankpath-full` on this dump.
- Merging PR **#5**, **#6**, **#7**, **#8**, or **#9**.
- Selling any of these isolated counts as replacing **25/48**.
- Key recovery. Paid chat APIs. Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe once.
4. Do not add a scorer.

## Results

H-rpmbody **fails** as a raw count. gpt2-medium unmarked-LM rankpath on
generated tokens `[4:16)` ranks **9/12**; isolated **27/48 vs 28/48**
(AUC **0.580**; nested-by-stem Youden **18/48 vs 31/48**).
`used_keys=false`. `model_name` is `gpt2-medium`. Clopper–Pearson 95% on
**27/48** includes ½. gpt2-medium-LM opening `[0:4)` stays **10/12**,
isolated **31/48 vs 32/48**. Distil-LM `[4:16)` stays **6/12**, isolated
**24/48 vs 23/48**. GPT-2 `[4:16)` stays **7/12**, isolated
**20/48 vs 22/48**. The unwindowed fit-prefix-16 file score on this run
is **11/12**, isolated **25/48 vs 31/48**; that is not the frozen slice
and is not the locked headline **25/48**. Do not sell **27/48**, **9/12**,
or parent **25/48**. JSON:
[experiments/2026-09-04-probe-12x4-rankpath-medium-w4-16/window-4-16/](../experiments/2026-09-04-probe-12x4-rankpath-medium-w4-16/window-4-16/).

H-rpmbody-iso **holds**. Cross-LM body-window rankpath is not a universal
isolated-file detector. Prompt ranking **9/12** is a different grain from
isolated **27/48**. Do not leftover-slice. Do not merge PR **#9**.
Isolated-file remains open. Do not write `thesis/`.
