# Isolated-file protocol (GPT-2-small LM on gpt2-medium 12×4)

This is a **methods freeze** for opening rankpath 12-LOO on already
frozen gpt2-medium 12×4 twins, with **GPT-2-small** as the unmarked LM.
It does not add a scorer. Existing `rankpath` only. Same GPT-2 BPE.
gpt2-medium native opening rankpath on these twins is **6/12**, isolated
**22/48 vs 30/48** ([PROTOCOL-isolated-rankpath-m12.md](PROTOCOL-isolated-rankpath-m12.md)).
GPT-2-small native on GPT-2 twins is **11/12**, isolated **41/48 vs 35/48**.
This freeze asks whether GPT-2-small ranks still fire on gpt2-medium
generations of the same 12 Grok seeds.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from this
file.
Do **not** look at GPT-2-small-on-medium rankpath LRs until this freeze
is named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice. Do **not** apply
leftover-15 GPT-2 keys. Do **not** merge GitHub PR **#9**.
Do **not** run lock A interpolate on gpt2-medium twins.

## Why freeze now

gpt2-medium native opening rankpath is chance-like ranking **6/12** and
isolated **22/48**. Distil native is chance **8/12**. Isolated-file
detection is still not finished. The remaining honesty item that is not
leftover targeting is whether the GPT-2-small rank LM, which scores
**41/48** on GPT-2 twins, still classifies gpt2-medium 12×4 files.
Existing twins. Existing `rankpath`. Not a leftover re-slice.

## Primary scientific question

Under leave-one-prompt-out opening rankpath, with no detector keys,
`hash_iv`, or g-values, do GPT-2-small ranks classify gpt2-medium 12×4
finished strings, and does isolated `lr>0` beat hard **25/48**?

Not: leftover-15. Not: another `probe --methods` name. Not: lock A.

## Frozen scorers

| Twins | Unmarked LM | `--model` |
|---|---|---|
| gpt2-medium 12×4 | gpt2 (small) | `gpt2` |

`--methods rankpath --fit-prefix 4 --pos-bucket 1 --skip-hashpool`.
Do **not** pass `--rankpath`. Do **not** leftover-slice.

## Hypotheses (stated before these LRs)

- **H-rpg2m.** GPT-2-small unmarked-LM opening rankpath on gpt2-medium
  12×4 isolated marked `lr>0` does not beat hard **25/48**. Medium
  native is **22/48 vs 30/48**. A higher count is not leftover-15
  recall and does not replace **25/48**.
- **H-rpg2m-iso.** Cross-size opening rankpath is not a universal
  isolated-file detector. Do not sell that isolated count, medium
  native **22/48**, Distil native **28/48**, Distil-LM-on-GPT-2
  **32/48**, GPT-2-small **41/48**, leftover official **15/15**, or PR
  **#9** last-2 **29/48** as replacing **25/48**. Do not leftover-slice.
  Do not merge PR **#9**.

## Primary endpoint

Isolated t=0 / 48. Prompt ranking / 12 secondary. `used_keys` false.
`model_name` must be `gpt2`. Equality with **25/48** is not a win.

## Corpus

| Role | Path |
|---|---|
| Twins | `experiments/2026-09-01-pair-gpt2-medium-12x4/` |
| Medium native control | `experiments/2026-09-04-probe-medium-12x4-rankpath-native/` |
| Probe dump | `experiments/2026-09-04-probe-medium-12x4-rankpath-gpt2-lm/` |

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-gpt2-medium-12x4 \
  --model gpt2 --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 --methods rankpath \
  --out-dir experiments/2026-09-04-probe-medium-12x4-rankpath-gpt2-lm
```

Do not change flags after the first run. Do not look at those LRs until
the logbook names this SHA.

## What this protocol refuses

- New `probe --methods` names on 12×4 / 36×4 twins.
- Leftover targeting or leftover-15 keys on gpt2-medium files.
- family-12 paraphrases after leftover peeking.
- Mixing grok12 into any train.
- Lock A interpolate on gpt2-medium twins.
- Merging PR **#5**, **#6**, **#7**, **#8**, or **#9**.
- Selling any of these isolated counts as replacing **25/48**.
- Key recovery. Paid chat APIs. Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe once.
4. Do not add a scorer.

## Results

*(empty until the SHA is named in LOGBOOK.md and the probe has been
run once, as written)*
