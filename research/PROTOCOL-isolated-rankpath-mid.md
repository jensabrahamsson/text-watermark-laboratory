# Isolated-file protocol (opening rankpath mid-file window [16:32))

This is a **methods freeze** for in-domain 12-LOO rankpath on already
frozen GPT-2 12×4 twins, scoring only generated tokens `[16:32)`. It
does not add a scorer. Existing `rankpath` only. Opening `[0:4)` on
these twins is **11/12**, isolated **41/48 vs 35/48**. Bucketed
`[4:16)` is **7/12**, isolated **20/48 vs 22/48**, AUC **0.430**
([PROTOCOL-isolated-rankpath-body.md](PROTOCOL-isolated-rankpath-body.md)).
Unbucketed full-file rankpath `[16:32)` is chance **6/12**, isolated
**23/48 vs 24/48**. The GPT-2-family `[4:16)` 3×3 is filled. This freeze
asks whether the bucketed reader still classifies isolated files in the
next sixteen generated tokens.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from this
file.
Do **not** look at rankpath `[16:32)` LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md) and the analysis command has been run once, as
written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice. Do **not** apply
leftover-15 keys. Do **not** merge GitHub PR **#9**.
Do **not** pass `--rankpath-full`.

## Why freeze now

The `[4:16)` 3×3 is filled. Isolated-file remains open. Occupancy
leftover is closed. Unbucketed `[16:32)` is already chance. The
remaining honesty item that is not leftover targeting is whether
bucketed rankpath on the original GPT-2 12 fires in `[16:32)`. Existing
twins. Existing `rankpath`. Existing `--windows`. Not a leftover
re-slice.

## Primary scientific question

Under leave-one-prompt-out rankpath on `[16:32)`, with no detector keys,
`hash_iv`, or g-values, do GPT-2 ranks classify GPT-2 12×4 finished
strings on generated tokens 16–31, and does isolated `lr>0` beat hard
**25/48**?

Not: leftover-15. Not: another `probe --methods` name. Not: lock A.

## Frozen scorers

`--methods rankpath --fit-prefix 32 --pos-bucket 1 --skip-hashpool
--windows 16:32`. Do **not** pass `--rankpath`. Do **not** leftover-slice.

## Hypotheses (stated before these LRs)

- **H-rpmid.** Bucketed rankpath on generated tokens `[16:32)` isolated
  marked `lr>0` does not beat hard **25/48**. Opening `[0:4)` is
  **41/48 vs 35/48**. Bucketed `[4:16)` is **20/48 vs 22/48**. Unbucketed
  `[16:32)` is **23/48 vs 24/48**. A higher count is not leftover-15
  recall and does not replace **25/48**. Equality with **25/48** is not
  a win.
- **H-rpmid-iso.** A mid-file rankpath window is not a universal
  isolated-file detector. Do not sell that isolated count, opening
  **41/48**, bucketed `[4:16)` **20/48**, unbucketed `[16:32)` **23/48**,
  medium-on-Distil body **32/48**, leftover official **15/15**, or PR
  **#9** last-2 **29/48** as replacing **25/48**. Do not leftover-slice.
  Do not merge PR **#9**.

## Primary endpoint

Isolated t=0 / 48 on the `[16:32)` window dump. Prompt ranking / 12
secondary. `used_keys` false. `model_name` must be `gpt2`. Equality with
**25/48** is not a win. The unwindowed fit-prefix-32 file score is not
the frozen slice.

## Corpus

| Role | Path |
|---|---|
| Twins | `experiments/2026-08-17-pair-12x4/` |
| Opening `[0:4)` control | `experiments/2026-09-01-probe-12x4-recount-opening-rankpath/` |
| Bucketed `[4:16)` control | `experiments/2026-09-04-probe-12x4-rankpath-w4-16/window-4-16/` |
| Probe dump | `experiments/2026-09-04-probe-12x4-rankpath-w16-32/` |

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --skip-hashpool \
  --fit-prefix 32 --pos-bucket 1 --methods rankpath \
  --windows 16:32 \
  --out-dir experiments/2026-09-04-probe-12x4-rankpath-w16-32
```

Do not change flags after the first run. Do not look at those LRs until
the logbook names this SHA.

## What this protocol refuses

- New `probe --methods` names on 12×4 / 36×4 twins.
- Leftover targeting or leftover-15 keys.
- family-12 paraphrases after leftover peeking.
- Mixing grok12 into any train.
- `--rankpath-full` on this dump.
- Merging PR **#5**, **#6**, **#7**, **#8**, or **#9**.
- Selling any of these isolated counts as replacing **25/48**.
- Key recovery. Paid chat APIs. Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe once.
4. Do not add a scorer.

## Results

H-rpmid **holds**. Bucketed rankpath on generated tokens `[16:32)` ranks
**7/12**; isolated **23/48 vs 26/48** (AUC **0.506**; nested-by-stem Youden
**9/48 vs 28/48**). `used_keys=false`. `model_name` is `gpt2`.
Clopper–Pearson 95% on **23/48** includes ½. Opening `[0:4)` stays
**11/12**, isolated **41/48 vs 35/48**. Bucketed `[4:16)` stays **7/12**,
isolated **20/48 vs 22/48**. The unwindowed fit-prefix-32 file score on
this run is **10/12**, isolated **28/48 vs 34/48**; that is not the frozen
slice. Do not sell **23/48**, **7/12**, or **28/48**. JSON:
[experiments/2026-09-04-probe-12x4-rankpath-w16-32/window-16-32/](../experiments/2026-09-04-probe-12x4-rankpath-w16-32/window-16-32/).

H-rpmid-iso **holds**. File AUC **0.506** is chance. Opening **41/48**
does not live in `[16:32)`. Do not leftover-slice. Do not merge PR
**#9**. Isolated-file remains open. Do not write `thesis/`.
