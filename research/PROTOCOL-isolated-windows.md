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

## Results (opened after the frozen commands)

`used_keys=false`. Full-file nested Youden is unchanged (grok12
**22/48 vs 41/48**; original 12 **23/48 vs 38/48**). Window endpoints
are prompt ranking, file AUC, and t=0.

Grok-register 12×4:

| Window | Prompt | File AUC | t=0 marked | unmarked ≤0 |
|---|---|---|---|---|
| 0:4 | 7/12 | 0.619 | 23/48 | 31/48 |
| 4:16 | 4/12 | 0.467 | 21/48 | 26/48 |
| 16:32 | 8/12 | 0.497 | 23/48 | 23/48 |
| 32:64 | **9/12** | 0.630 | 26/48 | 28/48 |
| 64:128 | **9/12** | 0.616 | 26/48 | 31/48 |

Original 12×4:

| Window | Prompt | File AUC | t=0 marked | unmarked ≤0 |
|---|---|---|---|---|
| 0:4 | **9/12** | 0.636 | 25/48 | 31/48 |
| 4:16 | 9/12 | 0.572 | 25/48 | 29/48 |
| 16:32 | 6/12 | 0.560 | 27/48 | 25/48 |
| 32:64 | 6/12 | 0.493 | 25/48 | 26/48 |
| 64:128 | 8/12 | 0.603 | 27/48 | 28/48 |

H-win-open **holds**: grok12 window 0:4 is **7/12**, below full-file
**11/12**. Isolated t=0 **23/48 vs 31/48** is not occupancy-free
opening TPs (those are **0/48**).

H-win-mid **holds**: windows **32:64** and **64:128** rank **9/12**.
The 11/12 full-file rank on Grok-length files is not an opening core.
Window **4:16** anti-ranks **4/12**. Window **16:32** ranks **8/12**
with file AUC **0.497** — prompt ranking without file ranking. Do not
sell tail 9/12.

H-win-12 **holds**: on the original 12, window **0:4** ranks **9/12**
and **16:32** ranks **6/12**. Front-loaded transfer is register-specific.

H-win-iso **holds**. Isolated t=0 is chance-like in every slice. This
does not replace **25/48**. Isolated-file detection is not finished.

Absolute-history remasure of these transfer windows is
[PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md).
Do **not** overwrite these dumps. Do **not** rewrite the first-run flags
above.

JSON: `experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-windows/`,
`experiments/2026-09-01-transfer-100x4-to-12x4-hard-windows/`.

## Decode (opened after the window scores)

The same frozen interpolate tables, decoded with `atoms` (not a new
`probe --methods` name, not `detector_mean`):

```bash
python -m text_watermark_tools atoms \
  experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-last4/tables-counts \
  --test-dir experiments/2026-09-01-pair-grok12x4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-01-atoms-100x4-to-grok12x4-interpolate
```

`used_keys=false`. Full-file marked `lr>0` is **27/48**, matching the
xreg t=0 readout. Almost all interpolate mass is Witten–Bell backoff
on **unseen** next tokens, not observed last-4 copies:

| Window | Mean marked Δ | Mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | −0.017 | −0.397 | 81 | 207 |
| 4:16 | −0.096 | 0.003 | 16 | 1136 |
| 16:32 | 0.040 | −0.002 | 28 | 1508 |
| 32:64 | 0.085 | −0.114 | 87 | 2985 |
| 64:128 | 0.056 | −0.086 | 214 | 5924 |

Window **0:4** ranks **7/12** because unmarked Δ is more negative, not
because occupancy-free openings fire (those remain **0/48**). Observed-
token atoms that do fire: opening `'The' → ' car'` (n=19), and tail
GPT-2 paragraph/dialogue templates (`'\n\n" I' → ' am'`,
`'I turned my' → ' head'`). Shared continuation 4-grams, not a denser
isolated-file detector. Do not sell `The car` or tail **9/12**. Does
not replace **25/48**.

The next isolated freeze is
[PROTOCOL-isolated-scale.md](PROTOCOL-isolated-scale.md): 36 new
Grok-length families. Prompts before `pair`. Do not mix grok12 into
that train. The `atoms` decode of those later interpolate tables is
`experiments/2026-09-01-atoms-grok36x4-to-12x4-interpolate/` and
`experiments/2026-09-01-atoms-grok36x4-to-grok12x4-interpolate/`.
Original-12 nested **26/48** is still not occupancy-free **10/48**.
Does not replace **25/48**.

