# Confirmatory protocol (Qwen Kirchenbauer 100-family windows)

This is a **methods freeze** for a window remasure of twins that already
exist. It does not add a `probe --methods` name. It does not edit the
`synthid-text` checkout. It does not overwrite
`experiments/2026-09-04-probe-qwen-100x4-kgw-hard-last4/` (full-file
interpolate **96/100**). GitHub PRs **#5**, **#6**, and **#7** stay
**unmerged**. This file asks the same two-grain question on committed
Qwen2-1.5B Kirchenbauer 100-family dumps, with flags locked before
those window LRs are opened.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`
from this file.
Do **not** look at window LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md) and the analysis command has been run once,
as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score these twins with SynthID `detector_mean`.

## Why freeze now

[PROTOCOL-next-kgw-qwen-100.md](PROTOCOL-next-kgw-qwen-100.md) opened
Qwen Kirchenbauer interpolate last-4 as **96/100** (isolated
**620/800**); hard **63/100**. Official first-draw z>3 is **90/100**.
Leave-one-family-out interpolate atoms already show marked mean $\Delta$
on every committed window (0:4 $+0.621$; 64:128 $+0.255$). Mean $\Delta$
is not prompt ranking. The missing grain is the same strict `>`
prompt-win count on tokens $[64{:}128)$ versus the opening $[0{:}4)$.

$\Hw=12$ interpolate $[64{:}128)$ on GPT-2 was **50/100** versus public
**93/100** ([PROTOCOL-next-longctx-windows.md](PROTOCOL-next-longctx-windows.md)).
That is a different mixin. This file is Hugging Face Kirchenbauer on
Qwen2-1.5B. It does not leftover-target. It does not replace **25/48**.

## Primary scientific question

On Qwen2-1.5B-Instruct Kirchenbauer 100-family twins, under
leave-one-family-out interpolate last-4, do marked prompt-group means
still outrank unmarked means on generated tokens $[64{:}128)$, and how
does that compare with the opening $[0{:}4)$?

Not: leftover targeting. Not: a new scorer name. Not: replacing
**25/48**. Not: official keyed detection failed (it is **90/100**
first-draw, mixin on).

## Frozen configuration (locked before these window LRs)

| Item | Value |
|---|---|
| Twins | `experiments/2026-09-04-pair-qwen-100x4-kgw/` (already opened; seed **20260904**) |
| Generator / tokenizer | `Qwen/Qwen2-1.5B-Instruct` |
| Readers | `--methods interpolate,hard --context-len 4 --skip-hashpool` |
| Windows | `0:4,4:16,16:32,32:64,64:128` |
| Out-dir | `experiments/2026-09-04-probe-qwen-100x4-kgw-windows/` |
| Fold | leave-one-family-out |
| Primary group metric | $D_p$ sign count / 100, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, AUC |

Probe must pass `--model Qwen/Qwen2-1.5B-Instruct`. Do not overwrite
the full-file interpolate dump. Full-file interpolate on the window run
must still be **96/100** (same reader). If it is not, stop; harness bug.

## Hypotheses (stated before these window LRs)

- **H-kgw-q100-win-ctrl.** Full-file interpolate on the window run
  remains **96/100**. If it moves, stop; harness bug.
- **H-kgw-q100-win-open.** Interpolate last-4 on $[0{:}4)$ is reported
  beside full-file **96/100**. Either drop or hold is informative. It
  does not replace **25/48**.
- **H-kgw-q100-win-body.** Interpolate last-4 on $[64{:}128)$ is
  reported beside the opening. Chance-like ranking (near 50/100 or AUC
  near $1/2$) would mean full-file **96/100** is not a body reader.
  Either drop or hold is informative. It does not replace **25/48**.
- **H-kgw-q100-win-iso.** Isolated $\tau=0$ on any window does not
  replace **25/48**.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-100x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods interpolate,hard --context-len 4 --skip-hashpool \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-probe-qwen-100x4-kgw-windows
```

`used_keys=false`. Do not change flags after the first run.

## What this protocol refuses

- Editing `synthid-text`.
- New `probe --methods` names.
- Scoring Qwen Kirchenbauer twins with `detector_mean`.
- Scoring Qwen twins with the default GPT-2 tokenizer.
- Leftover targeting.
- Selling any window count as replacing **25/48**.
- Selling full-file **96/100** or **620/800** as replacing **25/48**.
- Paid chat APIs.
- Writing `thesis/`.
- Merging GitHub PRs **#5**, **#6**, or **#7**.

## Preregistration mechanic

1. Commit this file before the window probe.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before those LRs.
3. Run the analysis command once, as written.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.
