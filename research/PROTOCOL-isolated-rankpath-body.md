# Isolated-file protocol (opening rankpath body window [4:16))

This is a **methods freeze** for in-domain 12-LOO rankpath on already
frozen GPT-2 12×4 twins, scoring only generated tokens `[4:16)`. It does
not add a scorer. Existing `rankpath` only. Opening `[0:4)` on these
twins is **11/12**, isolated **41/48 vs 35/48**. Unbucketed full-file
rankpath `[16:32)` is chance **6/12**, isolated **23/48 vs 24/48**.
Unbucketed `[0:16)` ranks **9/12**. This freeze asks whether the
bucketed opening reader still classifies isolated files after the first
four generated tokens.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from this
file.
Do **not** look at rankpath `[4:16)` LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md) and the analysis command has been run once, as
written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** leftover-slice. Do **not** apply
leftover-15 keys. Do **not** merge GitHub PR **#9**.
Do **not** pass `--rankpath-full`.

## Why freeze now

The GPT-2-family opening-rankpath 3×3 matrix is filled. Isolated-file
detection is still not finished. Occupancy leftover is closed. The
remaining honesty item that is not leftover targeting is whether the
in-domain opening rankpath sign (**41/48**) lives past token 4. Existing
twins. Existing `rankpath`. Existing `--windows`. Not a leftover
re-slice.

## Primary scientific question

Under leave-one-prompt-out rankpath on `[4:16)`, with no detector keys,
`hash_iv`, or g-values, do GPT-2 ranks classify GPT-2 12×4 finished
strings after the opening four tokens, and does isolated `lr>0` beat
hard **25/48**?

Not: leftover-15. Not: another `probe --methods` name. Not: lock A.

## Frozen scorers

`--methods rankpath --fit-prefix 16 --pos-bucket 1 --skip-hashpool
--windows 4:16`. Do **not** pass `--rankpath`. Do **not** leftover-slice.

## Hypotheses (stated before these LRs)

- **H-rpbody.** Bucketed rankpath on generated tokens `[4:16)` isolated
  marked `lr>0` does not beat hard **25/48**. Opening `[0:4)` is
  **41/48 vs 35/48**. Unbucketed `[16:32)` is **23/48 vs 24/48**. A
  higher count is not leftover-15 recall and does not replace **25/48**.
- **H-rpbody-iso.** A body-window rankpath is not a universal
  isolated-file detector. Do not sell that isolated count, opening
  **41/48**, unbucketed `[16:32)` **23/48**, Distil-on-medium **30/48**,
  medium-on-Distil **30/48**, leftover official **15/15**, or PR **#9**
  last-2 **29/48** as replacing **25/48**. Do not leftover-slice. Do not
  merge PR **#9**.

## Primary endpoint

Isolated t=0 / 48. Prompt ranking / 12 secondary. `used_keys` false.
Equality with **25/48** is not a win.

## Corpus

| Role | Path |
|---|---|
| Twins | `experiments/2026-08-17-pair-12x4/` |
| Opening `[0:4)` control | `experiments/2026-09-01-probe-12x4-recount-opening-rankpath/` |
| Probe dump | `experiments/2026-09-04-probe-12x4-rankpath-w4-16/` |

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --skip-hashpool \
  --fit-prefix 16 --pos-bucket 1 --methods rankpath \
  --windows 4:16 \
  --out-dir experiments/2026-09-04-probe-12x4-rankpath-w4-16
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

*(empty until the SHA is named in LOGBOOK.md and the analysis command
has been run once.)*
