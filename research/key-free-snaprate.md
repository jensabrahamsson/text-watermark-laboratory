# Table-free snap-rate (key-free, not a tournament detector)

Rank-path tables ask *which* unmarked-LM rank was chosen. The simpler
hypothesis is binary: marked text leaves the unmarked argmax more
often. That needs no twin tables. `--snaprate` scores each opening from
the public unmarked LM only.

Score is rate − 0.5 so threshold 0 means a majority. Still no keys,
`hash_iv`, or g-values. Isolated `indicate score` of a lone file still
needs the unmarked LM, same as pivot.

| Method | Meaning |
|---|---|
| `snapleave` | chosen token is not the unmarked argmax (upsets + misses) |
| `snapupset` | among in-topk rows, chosen token is not rank 1 (the tournament step) |
| `snapmiss` | chosen token missed the unmarked top-k (negative control for the mixin) |

Tournament sampling only reweights the unmarked top-k. If the isolated
signal were “the mixin left the greedy token”, `snapupset` would rank.
`snapmiss` should be chance or *lower* on marked text, because the
mixin stays inside top-k.

JSON: [../experiments/2026-09-01-probe-12x4-fitprefix4-snaprate/](../experiments/2026-09-01-probe-12x4-fitprefix4-snaprate/),
[../experiments/2026-09-01-probe-12x4-prefix4-snaprate/](../experiments/2026-09-01-probe-12x4-prefix4-snaprate/).
`used_keys=false`. Isolated generated-only geometry (token 0 has no
context without a prompt).

## In-domain 12×4 leave-one-prompt-out

Opening: `--fit-prefix 4` (three rank rows, generated tokens 1–3).
Prefix-4: `--fit-prefix 5` (four rank rows).

| Protocol | Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | perm p | mean rate M / U |
|---|---|---|---|---|---|---|---|
| Opening | snapleave | 9/12 | 0.569 | **48/48** | 7/48 | 0.057 | 0.826 / 0.750 |
| Opening | **snapupset** | **7/12** | **0.501** | 24/48 | 20/48 | **0.55** | **0.649 / 0.653** |
| Opening | snapmiss | **10/12** | **0.707** | **21/48** | **41/48** | 0.0005 | 0.458 / 0.278 |
| Prefix-4 | snapleave | 8/12 | 0.601 | 42/48 | 10/48 | 0.029 | — |
| Prefix-4 | **snapupset** | **6/12** | **0.501** | 25/48 | 14/48 | 0.23 | — |
| Prefix-4 | snapmiss | 11/12 | 0.717 | 2/48 | 46/48 | 0.0005 | 0.391 / 0.245 |

**`snapupset` is chance.** Marked and unmarked leave the in-topk argmax
at the same rate. Binary “was it greedy?” is not a detector. Rank-path
tables are doing something else: they learn *which* rank symbol is
occupied, not the upset bit. File-level correlation of opening
`snapupset` with in-domain rankpath is **−0.15**.

**`snapleave` majority vote is not a detector.** Unmarked sampling also
leaves the argmax (~75% of opening rows). Threshold 0 marks 48/48
marked files and 41 unmarked files. Nested 10% FPR is 0/48.

**`snapmiss` ranks, and it is not the tournament.** Marked openings miss
GPT-2 top-k more often (46% vs 28%). Prompt ranking 10/12 and AUC 0.707
are real (perm p=0.0005). Isolated t=0 is **21/48 vs 41/48** (precision
0.750). Nested Youden stays 21/48 vs 31/48. Nested FPR10 is 0/48. Do
not sell 21/48 as beating **29/48** or in-domain rankpath **41/48**.

Prefix-4 miss rates sit below 0.5, so majority-miss t=0 is 2/48.
Nested Youden (t=−0.25) is 27/48 vs 39/48. Same ranking, still not an
isolated-file headline.

Opening `snapmiss` correlates **0.83** with opening pivot-lda and
**0.87** with pivot-rank, and only **0.23** with rankpath. It is a
one-feature off-mode / rank statistic the LDA already uses, not a new
channel. Opening pivot-lda on the same files is **10/12**, **27/48 vs
37/48**. Snap-miss isolated 21/48 is weaker than that LDA.

## Leftover 8 after positive-when cascade

The eight 60-stem count-nonpositive files that prefix-4 rankpath also
misses (`The ferry was in/waiting`, `The conductor turned and`,
`Now in the second`, `While working on the`, `The printer worked.` ×2)
are not a snap-rate threshold problem.

Opening `snapleave>0` hits all eight because it hits almost every file.
Opening `snapmiss>0` hits 4/8 and spends 7 unmarked FPs globally.
Prefix-4 `snapmiss>0` hits **0/8**. Do not OR snap-rate into the
positive-when cascade as a headline.

## Why scrub still kills the official mean

Argmax snap on 128-token marked files moves official mean **0.622 →
0.499** even though the *rate* of in-topk upsets is the same on marked
and unmarked openings. Scrub changes *which* tokens sit in those
non-argmax slots. The public detector reads g-values on the chosen
ids. Snap-rate does not. Removal and detection are different uses of
the same unmarked-LM rows.

## What to use

- Table-free isolated-file reader: **do not**. `snapupset` is chance.
  `snapleave` majority vote is not a detector. `snapmiss` ranking is
  real and is already inside opening LDA / pivot-rank.
- Isolated-file geometry that *does* transfer as ranking: rank-symbol
  **tables** (`rankpath`), not the binary upset bit. See
  [key-free-rankpath.md](key-free-rankpath.md).
- High-precision isolated-file channel remains observed-token
  `postokbackoff` with `n_used` and **ABSTAIN**.

```bash
python -m text_watermark_tools probe \
  experiments/2026-08-17-pair-12x4 \
  --methods snapleave,snapupset,snapmiss \
  --skip-hashpool \
  --fit-prefix 4 \
  --out-dir experiments/2026-09-01-probe-12x4-fitprefix4-snaprate
```

Still not keys. Still not a universal detector. Do not replace
**10/12**, **29/48**, or **36/36**.
