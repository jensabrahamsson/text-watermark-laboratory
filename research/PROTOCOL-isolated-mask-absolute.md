# Isolated-file protocol (absolute-history 12-LOO mask-*k*)

This is a **methods freeze** for a bug-fix remasure of
[PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md). It does not
add a scorer. The committed headline-window dump
(`experiments/2026-09-01-probe-12x4-headline-windows/`) scored each
`--windows` slice as a **reindexed** substring. Probe now passes
absolute `score_span` and keeps preceding tokens as context
([`probe_models.py`](../src/text_watermark_tools/probe_models.py)
`_call_scorer`; [`blind.py`](../src/text_watermark_tools/blind.py)
`likelihood_ratio`). In-family absolute H2 is already opened
([PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md)). Absolute-history
OOD interpolate windows are already opened
([PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md)).
Until this remasure, do not sell “headline hard 9/12 is not an
opening-only n-gram artifact” from those reindexed mask dumps.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Reindexed hard prefix **0:4**
**5/12** and tails **4:128** / **8:128** **9/12** stay in that
historical dump. Do **not** overwrite it.
Do **not** rewrite PROTOCOL-isolated-mask first-run flags.
Do **not** write `thesis/` from this file.
Do **not** look at absolute-history mask LRs until this freeze is
named in [LOGBOOK.md](LOGBOOK.md) and the analysis command has been
run once, as written.
Do **not** add a new `probe --methods` name. Do **not** pass
`--include-first`. Do **not** leftover-slice these windows.
Do **not** mix grok12 into any train. Do **not** target leftover-15
openings.

## Why freeze now

PROTOCOL-isolated-mask is still a reindexed measurement. The harness
now refuses to reindex a window as a new sequence. Occupancy leftover
unions are closed. Absolute OOD windows are opened. Isolated-file
detection is still not finished. The remaining confirmatory honesty
item that is not leftover targeting is whether 12-LOO hard last-4
still keeps tail ranking **9/12** and prefix **0:4** **5/12** when
mid-file 4-grams keep their real prefix.

Sol’s 260903 review asked for a preregistered longer-context or
different-mixin two-grain replication as the next *external-validity*
axis. That lock is [PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md).
This file is the remaining *honesty remasure* of an already-opened
reader. It is not leftover targeting.

## Primary scientific question

Under absolute generated-token history, on the original 12×4 files,
12-LOO hard last-4: does prompt ranking **9/12** still survive after
masking the first scored tokens (`4:128`, `8:128`), and is prefix
**0:4** still **5/12**?

Secondary: interpolate on the same absolute windows. Reindexed
interpolate was front-loaded (0:4 **9/12**; 8:128 **3/12**).

Not: leftover-15. Not: a new `probe --methods` name. Not: selling a
window 9/12 as **25/48**. Not: the longer-context mixin (that is
PROTOCOL-next-longctx).

## Frozen scorers

Same readers as PROTOCOL-isolated-mask. Same window list. New out-dir
so the reindexed dump is not overwritten. No new method names.

| Item | Value |
|---|---|
| Readers | `--methods hard,interpolate --context-len 4` |
| Windows | `0:2,0:4,0:8,2:128,4:128,8:128` |
| Pair | `experiments/2026-08-17-pair-12x4/` |
| Token 0 | skipped (no `--include-first`) |
| History | absolute `score_span`; preceding generated tokens remain visible |

Windows use absolute `score_span`. Do **not** change the window list.
Do **not** add poshits, rankpath, hashtok, or cascades to this remasure.

Prefix windows that start at 0 have no preceding generated tokens
outside the slice. Absolute 0:2 / 0:4 / 0:8 should therefore **equal**
the reindexed ranks. Tails `2:128`, `4:128`, `8:128` are the
remasure: reindexed skipped the first token of each slice; absolute
scores that token with its real prefix.

## Hypotheses (stated before absolute-history mask LRs)

- **H-mask-abs-open.** Absolute prefix **0:2**, **0:4**, and **0:8**
  match the reindexed prompt ranks (hard **10/12**, **5/12**,
  **6/12**; interpolate **9/12**, **9/12**, **8/12**). Window 0:4 has
  no preceding generated tokens outside the slice. Isolated t=0 on
  no prefix replaces **25/48**.
- **H-mask-abs-tail.** At least one absolute tail (**4:128** or
  **8:128**) is still reported. If hard tails **rise** versus
  reindexed **9/12**, that is history accumulation. If they **fall**,
  reindexed overstated tail ranking. Isolated t=0 on no tail replaces
  **25/48**. In-family absolute H2 16:32 did **not** rise versus
  reindexed **89/100**; OOD interpolate 32:64 **did** rise 9→10.
- **H-mask-abs-2.** Absolute **0:2** remains different from **0:4**
  for hard (reindexed 10/12 vs 5/12). Absolute **2:128** is not
  required to match full-file **9/12**.
- **H-mask-abs-iso.** No window prompt ranking or isolated t=0 sign
  replaces **25/48**. Do not sell reindexed tail **9/12**, absolute
  tails, prefix **10/12**, isolated 27/48 / 29/48 / 31/48 / 33/48,
  H2 **99/100**, or OOD absolute **10/12** as replacing **25/48**.
  Do not overwrite the reindexed dump.

## Primary endpoint

Prompt-level paired discrimination per window: `n_prompts_marked_above`
/ 12, strict `>`. File AUC and isolated `lr>0` are secondary.
`used_keys` must be false. Equality is a **tie**, not a win. Nested
Youden on window holdouts is **not** the primary.

## Corpus

No new `pair`. The original 12×4 twins already exist.

| Role | Path |
|---|---|
| Pair | `experiments/2026-08-17-pair-12x4/` |
| Reindexed (keep) | `experiments/2026-09-01-probe-12x4-headline-windows/` |
| Absolute | `experiments/2026-09-03-probe-12x4-headline-windows-absolute/` |

## Analysis command

Do not change flags after the first run. Do not look at window LRs until
the logbook names this SHA. Do not write into the reindexed out-dir.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --windows 0:2,0:4,0:8,2:128,4:128,8:128 \
  --out-dir experiments/2026-09-03-probe-12x4-headline-windows-absolute
```

`used_keys=false`.

## What this protocol refuses

- Overwriting `experiments/2026-09-01-probe-12x4-headline-windows/`.
- Changing PROTOCOL-isolated-mask first-run flags.
- `--include-first` on this run.
- New hashed / backoff / cascade / learned scorers on 12×4.
- Leftover-slicing these absolute windows after peeking.
- Targeting leftover-15 openings after peeking.
- Mixing grok12 into any train.
- Selling absolute tails, reindexed tail **9/12**, prefix **10/12**,
  isolated window counts, H2 **99/100**, or OOD **10/12** as replacing
  **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the probe command above once.
4. Do not add a scorer.

Human merge of PR #4 is out of scope for this file.

## Results

*(empty until the SHA is named in LOGBOOK.md)*
