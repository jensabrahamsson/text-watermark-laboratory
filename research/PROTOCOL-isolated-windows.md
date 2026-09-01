# Isolated-file protocol (where lock A lives on Grok-length files)

This is a **methods freeze** for a window readout of tables that already
exist. It does not add a scorer. PROTOCOL-isolated-xreg found that 100
one-liner interpolate tables rank Grok-register files **11/12** with
nested Youden **22/48 vs 41/48**, while occupancy-free opening
postokhits is **0/48** (coverage **5/48**, 0 exact copies). The mark
cannot be an observed opening token on that split. This file asks
**where in the 128-token file** the remaining interpolate LR lives.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** / **29/48**
stay in historical JSON. Do **not** write `thesis/` from this file.
Do **not** look at window LRs until the freeze SHA is named in
[LOGBOOK.md](LOGBOOK.md).

## Why freeze now

In-family, PROTOCOL-next H2 already showed lock A is front-loaded:
window **0:4** ranks **99/100** (AUC **0.885**); **16:32** ranks
**89/100** (AUC **0.689**). Out-of-family onto Grok-length files, the
opening observed-token channel is empty. If interpolate still ranks
**11/12** on the whole file, either (i) window 0:4 still scores via
truncated-context / occupancy Laplace, or (ii) later windows carry
generic last-4 overlap. Those are different scientific objects.

The 100-family interpolate tables are already fit. This protocol only
**scores slices** of the test files against those same last-4 counts
(`--windows`, existing probe flag). Fit stays full-file. No new
`probe --methods` name. No new `pair`.

## Primary scientific question

On Grok-register 12×4 files scored with 100 one-liner interpolate
tables, is prompt ranking concentrated in generated tokens **0:4**, or
does it survive in later windows after occupancy-free openings are
known to be empty?

Secondary: the same windows on the original 12×4 (100→12). That
transfer was front-loaded in PROTOCOL-isolated lock B; lock A nested
**23/48** did not report windows.

## Frozen reader

Lock A only. Exact CLI. Same flags as PROTOCOL-isolated lock A, plus
`--windows`.

| Item | Value |
|---|---|
| Reader | `--methods interpolate --context-len 4` |
| Windows | `0:4,4:16,16:32,32:64,64:128` |
| Train | `experiments/2026-09-01-pair-100x4/` |
| Test A | `experiments/2026-09-01-pair-grok12x4/` |
| Test B | `experiments/2026-08-17-pair-12x4/` |

Tables are fit on full training sequences. Each window scores only that
slice of the test file. Nested Youden on window holdouts is
**not** the PROTOCOL-isolated primary (that nested row is train-LOO on
full-file LRs). Window endpoints are prompt ranking, file AUC, and
t=0 sign. Do not promote `nested_stem` on test window LRs to an
isolated-file detector.

Do not duplicate `tables-counts/tables.json` in git; the fit is the
same as `experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-last4/`
and `experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4/`.

## Hypotheses (stated before these window scores)

- **H-win-open.** Window **0:4** interpolate on grok12×4 does not
  recover occupancy-free opening TPs. Prompt ranking on 0:4 is at or
  below full-file **11/12**; isolated t=0 is not a detector.
- **H-win-mid.** At least one later window (**4:16**, **16:32**,
  **32:64**, or **64:128**) still ranks grok12 prompt groups above
  **6/12**. If none do, the 11/12 full-file rank is an accumulation of
  weak slices, not a mid-file core.
- **H-win-12.** On the original 12×4, window **0:4** ranks at least as
  high as **16:32** (front-loaded transfer, matching PROTOCOL-next H2
  and lock B). Isolated t=0 on no window replaces **25/48**.
- **H-win-iso.** No window nested-by-stem or t=0 sign replaces
  **25/48**. This readout does not finish isolated-file detection.

## Analysis commands

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --methods interpolate --context-len 4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-windows

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods interpolate --context-len 4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-12x4-hard-windows
```

`used_keys=false`. Do not change flags after the first run.

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers.
- Mixing train families after seeing LRs.
- Selling a window 11/12 or a mid-file 4-gram overlap as replacing
  **25/48**.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.
- New `pair` generation.

## Preregistration mechanic

1. Commit this file. That git SHA is the protocol version.
2. Name that SHA in [LOGBOOK.md](LOGBOOK.md) before looking at window
   LRs.
3. Run the two commands above, drop duplicate `tables-counts/` from
   the new out-dirs, then append a dated logbook entry.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #2 / PR #3 is out of scope for this file.
