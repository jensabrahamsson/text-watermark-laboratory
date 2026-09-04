# Confirmatory protocol (Hw=12 vs Hw=4 body windows)

This is a **methods freeze** for a window remasure of twins that already
exist. It does not add a `probe --methods` name. It does not edit the
`synthid-text` checkout. It does not overwrite
`experiments/2026-09-03-probe-100x4-ngram13-hard-last4/` (full-file
interpolate **76/100**) or
`experiments/2026-09-01-probe-100x4-hard-windows-absolute/` (public
absolute windows through 32:64). Draft GitHub PRs **#5**, **#6**, and
**#7** named the scientific hole; they are **not** merged. This file
asks the same two-grain question on committed dumps, with flags locked
before those window LRs are opened in this repository.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`
from this file.
Do **not** look at window LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md) and the analysis commands have been run once,
as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.

## Why freeze now

PROTOCOL-next-longctx Phase B opened $\Hw=12$ interpolate last-4 as
**76/100** and called that attenuation of lock A **99/100**, not
collapse. Committed leave-one-family-out atoms already show marked
mean $\Delta$ dying after the opening under $\Hw=12$ (0:4 $+2.712$;
16:32 $-0.009$; 64:128 $+0.008$) while public $\Hw=4$ keeps a tail
($+0.174$ at 64:128). Mean $\Delta$ is not prompt ranking. The missing
grain is the same strict `>` prompt-win count on tokens $[64{:}128)$.

Public $\Hw=4$ absolute H2 windows on disk stop at 32:64
(**85/100**). $[64{:}128)$ is not in that dump. $\Hw=12$ 100-family
has no committed `--windows` probe. Draft PR #5 wrote those two
probes to `/tmp` on another host; those holdouts are **not** in git.
This freeze re-runs them into dated `experiments/` paths.

Kirchenbauer body ranking in draft PR #7 is a different mixin and is
**not** this file. Matching `--context-len` to $\Hw=12$ (last-12) is
a different freeze and is **not** this file. Occupancy-free opening
precision (draft PR #6 hold 1) is already published; this file does
not leftover-target it.

## Primary scientific question

On the same 100 one-liner prompt strings, under leave-one-family-out
interpolate last-4, do marked prompt-group means still outrank unmarked
means on generated tokens $[64{:}128)$ when the mixin hash history is
$\Hw=12$, and how does that compare with public $\Hw=4$ on the same
slice?

Not: can another table classify the original 12. Not: leftover
targeting. Not: a new scorer name. Not: replacing **25/48**. Not:
official keyed detection failed (it is **400/400** on the $\Hw=12$
twins).

## Frozen configuration (locked before these window LRs)

| Item | Value |
|---|---|
| $\Hw=12$ twins | `experiments/2026-09-03-pair-100x4-ngram13/` (already opened; seed **20260903**) |
| Public $\Hw=4$ twins | `experiments/2026-09-01-pair-100x4/` (lock A) |
| Readers | `--methods interpolate,hard,hits --context-len 4 --skip-hashpool` |
| Windows | `0:4,4:16,16:32,32:64,64:128` on $\Hw=12$; `64:128` on public $\Hw=4$ (H2 dump already has 0:4 through 32:64) |
| $\Hw=12$ out-dir | `experiments/2026-09-04-probe-100x4-ngram13-windows/` |
| Public tail out-dir | `experiments/2026-09-04-probe-100x4-public-w64-128/` |
| Fold | leave-one-family-out (probe default on these twins) |
| Primary group metric | $D_p$ sign count / 100, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, AUC |

`hits` is an existing method (shared 4-grams only). It is the
diagnostic for “full-file ranking that drops unseen body 4-grams.”
It is not a new `--methods` name. Do not add tokhits, unigram,
rankpath, or hashtok to this freeze after the first run.

Do not overwrite the full-file $\Hw=12$ interpolate dump. Full-file
interpolate on the new $\Hw=12$ window run must still be **76/100**
(same reader). If it is not, stop; harness bug.

## Hypotheses (stated before these window LRs)

- **H-long-win-ctrl.** Full-file interpolate on the $\Hw=12$ window
  run remains **76/100**. Public lock A full-file interpolate remains
  **99/100**. If either moves, stop; harness bug.
- **H-long-win-body.** $\Hw=12$ interpolate last-4 on $[64{:}128)$ is
  reported beside public $\Hw=4$ on the same slice. Chance-like ranking
  (near 50/100 or AUC near $1/2$) would mean full-file **76/100** is
  not a weaker copy of lock A **99/100** on the body. Either drop or
  hold is informative. It does not replace **25/48**.
- **H-long-win-open.** $\Hw=12$ window $[0{:}4)$ still ranks. That is
  the occupancy already in the atoms dump, not a new detector.
- **H-long-win-hits.** If `hits` full-file ranking on $\Hw=12$ sits
  with $[0{:}4)$ and not with $[64{:}128)$, the residual is the
  opening with unseen body 4-grams dropped. Do not sell that full-file
  hits count as replacing **25/48**.

## Analysis commands

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods interpolate,hard,hits --context-len 4 --skip-hashpool \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-probe-100x4-ngram13-windows
```

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --methods interpolate --context-len 4 --skip-hashpool \
  --windows 64:128 \
  --out-dir experiments/2026-09-04-probe-100x4-public-w64-128
```

`used_keys=false`. Do not change flags after the first run. Do not
start these probes while a Qwen `pair` still holds the CPU.

## What this protocol refuses

- Editing `synthid-text`.
- Merging GitHub PRs **#5**, **#6**, or **#7**.
- New `probe --methods` names.
- Overwriting the reindexed or absolute H2 dumps, or the $\Hw=12$
  full-file interpolate dump.
- Leftover targeting.
- Selling any window count as replacing **25/48**.
- A last-12 reader matched to $\Hw=12$ (different freeze).
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before the window probes.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before those LRs.
3. Run the two commands, then log the two-grain counts from JSON.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.
