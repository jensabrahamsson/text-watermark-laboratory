# Isolated-file protocol (mask first *k* on the headline 12-LOO scorer)

This is a **methods freeze** for Gemini Loop 2.1 on the locked
headline reader. It does not add a scorer. Published tables already
skip generated token 0 (`include_first` is off). Masking *k*=1 is
therefore a no-op for last-4 hard / interpolate: `--windows 1:128`
matches the full file. This file asks what happens when the first
**scored** tokens are dropped (*k* ∈ {2, 4, 8}) and what remains in
the complementary prefixes `0:2`, `0:4`, `0:8`.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Pre-fix **10/12** /
**29/48** stay in historical JSON. Do **not** write `thesis/` from
this file. Do **not** look at these window LRs until this freeze is
named in [LOGBOOK.md](LOGBOOK.md) and the command has been run once,
as written. Do **not** add a new `probe --methods` name. Do **not**
pass `--include-first` (already measured; it hurts on the 4-token OOD
gate).

The story lock is [narrative.md](narrative.md). 36×4 window **0:4**
already ranks **34/36**; **16:32** is **22/36**. 100×4 lock A **0:4**
is **99/100**. This protocol is the same `--windows` flag on the
12-LOO hard last-4 files that produce **9/12** / **25/48**.

## Why freeze now

An external checklist asked to quantify how much classification
strength falls when the first *k* tokens are masked. That readout
does not exist for the headline 12-LOO hard scorer (the 12×4 recount
JSON has `windows=[]`). It is a slice of an existing reader, not a
new method. Grok12 `'The'→' car'` is **not** this experiment; that
identity is already in the scale `atoms` dumps.

`--windows` slices generated token ids, then the scorer still skips
index 0 of the slice. Prefix `0:4` therefore scores generated tokens
1–3. Tail `4:128` skips generated token 4 as well. Same mechanic as
[PROTOCOL-isolated-windows.md](PROTOCOL-isolated-windows.md).

## Primary scientific question

On the original 12×4 files, 12-LOO hard last-4, does prompt ranking
**9/12** and isolated **25/48** live in the opening prefix (`0:4` /
`0:8`), or does it survive after masking the first scored tokens
(`2:128`, `4:128`, `8:128`)?

Not: can another method lift **25/48**. Not: is grok12 0:4
steganography.

## Frozen scorer

Same readers as `experiments/2026-09-01-probe-12x4-recount-hard-last4/`.
Exact CLI. Existing `--windows`. No new method names.

| Item | Value |
|---|---|
| Readers | `--methods hard,interpolate --context-len 4` |
| Windows | `0:2,0:4,0:8,2:128,4:128,8:128` |
| Pair | `experiments/2026-08-17-pair-12x4/` |
| Token 0 | skipped (no `--include-first`) |

## Hypotheses (stated before these window LRs)

- **H-mask-open.** Prefix **0:4** hard prompt ranking is at least
  **8/12** (front-loaded, matching 36×4 **0:4 = 0:16**). Isolated t=0
  on 0:4 does not replace **25/48**.
- **H-mask-tail.** At least one tail window (**4:128** or **8:128**)
  drops hard prompt ranking below **8/12**. Isolated t=0 on no tail
  replaces **25/48**.
- **H-mask-2.** Prefix **0:2** (one scored token after skipping 0) is
  weaker than **0:4**. Mask **2:128** is not a no-op.
- **H-mask-iso.** No window prompt rank or isolated sign replaces
  **25/48**. Do not sell a prefix 9/12 as a detector.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --windows 0:2,0:4,0:8,2:128,4:128,8:128 \
  --out-dir experiments/2026-09-01-probe-12x4-headline-windows
```

`used_keys` must be false. Do not change flags after the first run.

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4.
- `--include-first` on this run.
- Selling a prefix 9/12, a tail 9/12, or any isolated window count as
  replacing **25/48**.
- Re-running grok12 atoms as if they were this ablation.
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Paid chat APIs.
- Writing `thesis/`.
- Looking at these window LRs until this SHA is named in the logbook
  and the command above has been run once.

## Preregistration mechanic

1. Commit this file in a commit that still precedes the window dump.
2. That git SHA is the protocol version. Name it in
   [LOGBOOK.md](LOGBOOK.md) before window LRs.
3. Run the command above, then append a dated logbook entry with the
   SHA and hard 0:4 / 4:128 prompt ranks plus isolated t=0.
4. If the command fails, fix the harness and re-run the **same**
   flags. Do not add a method.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Results (opened after the frozen command)

Protocol SHA `004397c`. `used_keys=false`. Full-file hard remains **9/12**,
isolated **25/48**.

| Window | Hard prompt | Hard isolated | Interpolate prompt | Interpolate isolated |
|---|---|---|---|---|
| 0:2 | **10/12** | 27/48 vs 31/48 | **9/12** | 31/48 vs 31/48 |
| 0:4 | **5/12** | 29/48 vs 26/48 | **9/12** | 30/48 vs 27/48 |
| 0:8 | **6/12** | 33/48 vs 25/48 | **8/12** | 31/48 vs 30/48 |
| 2:128 | **9/12** | 29/48 vs 23/48 | **5/12** | 21/48 vs 25/48 |
| 4:128 | **9/12** | 27/48 vs 22/48 | **5/12** | 20/48 vs 26/48 |
| 8:128 | **9/12** | 29/48 vs 23/48 | **3/12** | 19/48 vs 24/48 |

H-mask-open **fails** for hard: prefix 0:4 is **5/12**, not ≥8/12. Interpolate
0:4 is **9/12** (front-loaded on interpolate only).

H-mask-tail **fails** for hard: 4:128 and 8:128 stay **9/12**. Interpolate
tails drop to **5/12** then **3/12**.

H-mask-2 **fails as stated** for hard: 0:2 is **stronger** than 0:4
(10/12 vs 5/12), and 2:128 matches full-file rank. Interpolate 2:128 is
5/12 vs full-file 7/12.

H-mask-iso **holds**. Isolated t=0 stays chance-like. Do not sell prefix
10/12, isolated 27/48 / 29/48 / 31/48 / 33/48, or tail **9/12**. The
headline 12-LOO **hard** 9/12 is not an opening-only n-gram artifact.
Grok12 `'The'→' car'` is a different split. Isolated-file detection is
not finished.

JSON: `experiments/2026-09-01-probe-12x4-headline-windows/`.
