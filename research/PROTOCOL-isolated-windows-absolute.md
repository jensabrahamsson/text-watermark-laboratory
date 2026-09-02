# Isolated-file protocol (absolute-history OOD windows)

This is a **methods freeze** for a bug-fix remasure of
[PROTOCOL-isolated-windows.md](PROTOCOL-isolated-windows.md). It does
not add a scorer. The committed transfer window dumps
(`experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-windows/` and
`experiments/2026-09-01-transfer-100x4-to-12x4-hard-windows/`) scored
each `--windows` slice as a **reindexed** substring. Probe now passes
absolute `score_span` and keeps preceding tokens as context
([`blind.py`](../src/text_watermark_tools/blind.py)
`likelihood_ratio`; [`transfer.py`](../src/text_watermark_tools/transfer.py)
`score_sequence`). In-family absolute H2 is already opened
([PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md): 0:4 **99/100** vs
16:32 **87/100**; reindexed 16:32 was **89/100**). Until this remasure,
do not sell “out-of-family interpolate is not front-loaded” from those
reindexed transfer dumps.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Reindexed grok12 **0:4** **7/12** and tail
**9/12** stay in those historical dumps. Do **not** overwrite them.
Do **not** rewrite PROTOCOL-isolated-windows first-run flags.
Do **not** write `thesis/` from this file.
Do **not** look at absolute-history transfer window LRs until this
freeze is named in [LOGBOOK.md](LOGBOOK.md) and the two analysis
commands have been run once, as written.
Do **not** mix grok12 into any train. Do **not** add a new
`probe --methods` name. Do **not** target leftover-15 openings.
Do **not** Distil ∪ gpt2-medium union. Do **not** run lock A interpolate
on Distil or gpt2-medium twins. Do **not** generate a matched-seed
multi-key `pair()` after peeking control-as-marked **30/48**.
Do **not** occupancy-free postokhits on the constructed xkey pair.
Do **not** leftover-slice control rankpath.

## Why freeze now

PROTOCOL-isolated-windows is still a reindexed measurement. The harness
now refuses to reindex a window as a new sequence. Occupancy-free
leftover-15 is closed. Distil↔gpt2-medium occupancy-free is opened
([PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md)). Absolute
in-family H2 is opened. Second-key in-domain lock A is opened
([PROTOCOL-isolated-xkey.md](PROTOCOL-isolated-xkey.md): interpolate
**7/12**, isolated **30/48 vs 25/48**; H-xkey-iso fails as a raw count).
Isolated-file detection is still not finished. The remaining confirmatory
honesty item that is not leftover targeting is whether 100 one-liner
interpolate tables still put grok12 **tail 9/12** above **opening 7/12**
when mid-file 4-grams keep their real prefix.

The `atoms` decode of those interpolate tables already walks absolute
positions. Do **not** re-run `atoms` in this freeze.

## Primary scientific question

Under absolute generated-token history, on Grok-register 12×4 files
scored with 100 one-liner interpolate tables, is prompt ranking still
concentrated away from generated tokens **0:4**, and does at least one
later window still rank above **6/12**?

Secondary: the same absolute windows on the original 12×4 (100→12).
Reindexed that split was front-loaded (0:4 **9/12**; 16:32 **6/12**).

Not: leftover-15. Not: Distil ∪ gpt2-medium. Not: another
`probe --methods` name. Not: a matched-seed multi-key `pair()`.
Not: 12-LOO mask-*k* (those dumps stay reindexed;
[PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md)).

## Frozen scorers

Existing interpolate last-4 only. Same flags as PROTOCOL-isolated-windows.
New out-dirs so the reindexed dumps are not overwritten. No new method
names.

| Lock | Reader | Flags |
|---|---|---|
| A windows | Hard last-4 interpolate | `--methods interpolate --context-len 4 --windows 0:4,4:16,16:32,32:64,64:128` |

Windows use absolute `score_span`. Do **not** change the window list.
Do **not** add poshits, rankpath, hashtok, or cascades to this remasure.

## Hypotheses (stated before absolute-history transfer LRs)

- **H-win-abs-open.** Absolute-history window **0:4** on grok12×4 does
  not recover occupancy-free opening TPs (those remain **0/48**). Prompt
  ranking on 0:4 is at or below full-file **11/12**. Window 0:4 has no
  preceding generated tokens, so absolute 0:4 should **equal** reindexed
  **7/12**. Isolated t=0 is not a detector.
- **H-win-abs-mid.** At least one later window (**4:16**, **16:32**,
  **32:64**, or **64:128**) still ranks grok12 prompt groups above
  **6/12**. If none do, the 11/12 full-file rank is an accumulation of
  weak slices, not a mid-file core. If absolute tails **rise** versus
  reindexed **9/12**, that is history accumulation. If they **fall**
  versus **9/12**, reindexed overstated mid-file ranking. In-family
  absolute 16:32 did **not** rise versus reindexed **89/100**.
- **H-win-abs-12.** On the original 12×4, absolute **0:4** ranks at least
  as high as **16:32** (front-loaded transfer). Absolute 0:4 should
  **equal** reindexed **9/12**. Isolated t=0 on no window replaces
  **25/48**.
- **H-win-abs-iso.** No window prompt ranking, nested-by-stem, or t=0
  sign replaces **25/48**. Do not sell reindexed tail **9/12**, absolute
  tails, H2 **99/100**, xkey **30/48**, or occupancy-free **16/48** as
  replacing **25/48**. Do not overwrite the reindexed dumps.

## Primary endpoint

Prompt-level paired discrimination per window: `n_prompts_marked_above`
/ 12, strict `>`. File AUC and isolated `lr>0` are secondary.
`used_keys` must be false. Equality is a **tie**, not a win. Nested
Youden on window holdouts is **not** the primary.

## Corpus

No new `pair`. Train/test are the already-frozen 100×4 GPT-2 confirmatory
twins and the two already-frozen 12×4 test piles. Out-of-family transfer,
not leave-one-prompt-out.

| Role | Path |
|---|---|
| Train | `experiments/2026-09-01-pair-100x4/` |
| Test A | `experiments/2026-09-01-pair-grok12x4/` |
| Test B | `experiments/2026-08-17-pair-12x4/` |
| Reindexed A (keep) | `experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-windows/` |
| Reindexed B (keep) | `experiments/2026-09-01-transfer-100x4-to-12x4-hard-windows/` |
| Absolute A | `experiments/2026-09-02-transfer-100x4-to-grok12x4-hard-windows-absolute/` |
| Absolute B | `experiments/2026-09-02-transfer-100x4-to-12x4-hard-windows-absolute/` |

Prompts: `experiments/2026-09-01-prompts-100/` (train), grok12 seeds and
the original 12 Grok seeds (tests). Do not mix grok12 into train.

## Analysis commands

Do not change flags after the first run. Do not look at window LRs until
the logbook names this SHA. Do not write into the reindexed out-dirs.
Drop duplicate `tables-counts/` from the new out-dirs (the fit is the
same as the full-file transfer dumps).

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods interpolate --context-len 4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-02-transfer-100x4-to-grok12x4-hard-windows-absolute

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods interpolate --context-len 4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-02-transfer-100x4-to-12x4-hard-windows-absolute
```

`used_keys=false`.

## What this protocol refuses

- Overwriting `experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-windows/`
  or `experiments/2026-09-01-transfer-100x4-to-12x4-hard-windows/`.
- Changing PROTOCOL-isolated-windows first-run flags.
- Re-running `atoms` on these tables.
- Remeasuring 12-LOO mask-*k* in this freeze
  ([PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md) stays
  reindexed).
- New hashed / backoff / cascade / learned scorers on 12×4 or 100×4.
- Leftover-15 re-slices and leftover-slice rankpath.
- Targeting leftover-15 openings after peeking.
- Family-12 paraphrases of the original 12 after leftover peeking.
- Distil ∪ gpt2-medium opening union.
- Lock A interpolate on Distil or gpt2-medium twins.
- Mixing grok12 into any train.
- A matched-seed multi-key `pair()` after peeking xkey **30/48**.
- Occupancy-free postokhits on the constructed xkey pair after peeking.
- Selling absolute 0:4, absolute tails, reindexed **7/12** / **9/12**,
  H2 **99/100** / **87/100**, xkey **30/48**, Distil→gpt2-medium
  **20/48**, or occupancy-free **16/48** as replacing **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name it in [LOGBOOK.md](LOGBOOK.md).
3. Run the two probe commands above once.
4. Do not add a scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results

*(empty until the SHA is named in LOGBOOK.md)*
