# Isolated-file protocol (Distil LM on gpt2-medium 12×4)

This is a **methods freeze** for opening rankpath 12-LOO on already
frozen gpt2-medium 12×4 twins, with **DistilGPT2** as the unmarked LM.
Existing `rankpath` only. Same GPT-2 BPE. GPT-2-small LM on these twins
is **8/12**, isolated **20/48 vs 32/48**
([PROTOCOL-isolated-rankpath-g2m.md](PROTOCOL-isolated-rankpath-g2m.md)).
Distil LM on GPT-2 twins is **10/12**, isolated **32/48 vs 31/48**.
Distil native on Distil twins is chance **8/12**, isolated **28/48 vs 32/48**.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`.
Do **not** look at Distil-on-medium rankpath LRs until this freeze is
named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-slice.
Do **not** apply leftover-15 keys. Do **not** merge PR **#9**.
Do **not** mix grok12 into any train. family-12 paraphrases are refused.

## Why freeze now

The GPT-2-family opening-rankpath matrix on original-12 seeds is missing
Distil LM scoring gpt2-medium generations. Isolated-file remains open.
Existing twins. Existing `rankpath`. Not leftover targeting.

## Primary scientific question

Do DistilGPT2 ranks classify gpt2-medium 12×4 finished strings under
leave-one-prompt-out opening rankpath without keys, and does isolated
`lr>0` beat hard **25/48**?

## Frozen scorers

`--model distilgpt2 --methods rankpath --fit-prefix 4 --pos-bucket 1
--skip-hashpool`. Do **not** pass `--rankpath`.

## Hypotheses (stated before these LRs)

- **H-rpd2m.** Distil unmarked-LM opening rankpath on gpt2-medium 12×4
  isolated marked `lr>0` does not beat hard **25/48**. GPT-2-small on
  the same twins is **20/48 vs 32/48**.
- **H-rpd2m-iso.** Do not sell that isolated count, GPT-2-on-medium
  **20/48**, medium native **22/48**, Distil-LM-on-GPT-2 **32/48**,
  Distil native **28/48**, GPT-2-small **41/48**, leftover official
  **15/15**, or PR **#9** last-2 **29/48** as replacing **25/48**.
  Do not leftover-slice. Do not merge PR **#9**.

## Primary endpoint

Isolated t=0 / 48. `used_keys` false. `model_name` is `distilgpt2`.

## Corpus

| Role | Path |
|---|---|
| Twins | `experiments/2026-09-01-pair-gpt2-medium-12x4/` |
| Probe dump | `experiments/2026-09-04-probe-medium-12x4-rankpath-distil-lm/` |

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-gpt2-medium-12x4 \
  --model distilgpt2 --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 --methods rankpath \
  --out-dir experiments/2026-09-04-probe-medium-12x4-rankpath-distil-lm
```

## What this protocol refuses

- New `probe --methods` names on 12×4 / 36×4 twins.
- Leftover targeting. family-12 paraphrases after leftover peeking.
- Mixing grok12. Lock A on gpt2-medium twins. Merging PR **#5–#9**.
- Selling any of these counts as replacing **25/48**.
- Key recovery. Paid APIs. Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. 2. Name it in LOGBOOK. 3. Run the probe once.

## Results

*(empty until the SHA is named in LOGBOOK.md and the probe has been
run once, as written)*
