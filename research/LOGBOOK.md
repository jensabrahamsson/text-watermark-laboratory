# Lab logbook

Append-only. One dated entry after every collection or measurement. Do not
rewrite old entries; add a later note if something was wrong.

English. Same `PROMPTS` strings as `scripts/collect_claude_premark.py` — never
edit those; add new rows if needed.

## Cadence

While Claude’s mark and voice are in flux: **resample the same 40 prompts
often** (daily if the limit allows). Each run gets its own directory
`experiments/claude-sample-YYYY-MM-DD/` (or `claude-mark-YYYY-MM-DD/` if the
mark is announced). Then pair against `claude-premark-2026-08` and against
the previous sample, run last-1 and last-4 leave-one-out, and write a
logbook line.

A style shift should keep lighting up **last-1**. A SynthID-like tournament
should prefer **last-4** once the same prompts have reuse. If last-1 stays
ahead of last-4, do not call it a watermark.

Scheduled: **Wednesday, Friday, Sunday at 04:00** local time via launchd
(`se.makeitso.text-watermark-claude-resample`). Cancel:

```bash
scripts/install_claude_resample_schedule.sh uninstall
```

```bash
source .venv/bin/activate
python -m text_watermark_tools resample
# analyze an existing corpus only:
python -m text_watermark_tools resample --skip-collect \
  --new-dir experiments/claude-sample-YYYY-MM-DD
```

---

## 2026-08-15

Collected the Claude **pre-mark** control: `experiments/claude-premark-2026-08/`
(40 A/B texts, `assumed_watermark: false`). Sonnet 5 is before the 2 Aug
day-one cutoff; retrofit unpublished.

---

## 2026-08-17

Public-mixin dress rehearsal (GPT-2 / Qwen), not Claude. Official `score`
**12/12**. Key-free last-4 on 12×4 **10/12**. Isolated `indicate` sign
**29/48**. Write-up: [key-free-twins.md](key-free-twins.md).

---

## 2026-08-19

Rumor that Anthropic text marking is live. Same 40 `PROMPTS` on claude.ai
(logged-in Chrome, AppleScript + one Playwright seed).

**Collection.** `experiments/claude-mark-2026-08-19/`
`assumed_watermark: rumored`. **37/40** texts, ~112k characters. Usage
limit on the courtyard washing-line prompt. Still missing: washing line,
ferry in wind, teacher letter. Not an announced retrofit. Do not treat
this pile as ground-truth marked.

**Public `score` (wrong instance).** Chance on both dates:

| Prompt | Premark mean | 2026-08-19 mean |
|---|---:|---:|
| harbour | 0.495 | 0.506 |
| library | 0.504 | 0.504 |
| chess club | 0.499 | 0.497 |

**Key-free pairing.** 37 same-prompt twins in
`experiments/2026-08-19-claude-rumor-twins/`
(pre-mark = `unmarked-gen`, today = `marked` for the hypothesis only).
GPT-2 tokenizer. `used_keys=false`.

| Path | Result |
|---|---|
| last-1 leave-one-out | **28/37** |
| last-4 leave-one-out | **24/37** |
| indicate last-4, isolated marked `lr>0` | 26/37 |
| indicate last-4, isolated unmarked `lr≤0` | 15/37 |

**Reading.** Last-1 beat last-4. On the public mixin the watermark window
did the opposite. This is a **held-out style / model shift** between 15 Aug
and 19 Aug, not a claim that Claude is watermarked. Matches complaints that
the language changed. Isolated sign is still weak.

**Same-day resample finished** (evening). Same 40 `PROMPTS`, claude.ai,
AppleScript. `used_keys=false`. GPT-2 tokenizer.

- 19b corpus: `experiments/claude-sample-2026-08-19b/` — **40/40**
- 19a salvage: washing-line saved as `0038-sonnet5-mark.txt` (false
  usage-limit stop). 19a is now **38/40**. Still missing from 19a:
  ferry-in-wind, teacher letter.
- Same-day twins: `experiments/2026-08-19-claude-sameday-twins/`
  (19a = `unmarked-gen`, 19b = `marked`, labels arbitrary)
- 19b vs pre-mark twins: `experiments/2026-08-19b-claude-vs-premark-twins/`

| Contrast | last-1 | last-4 |
|---|---|---|
| 19a vs 19b (same day, 38 prompts) | **19/38** | **19/38** |
| 15 Aug vs 19a (37 prompts, morning pairing) | **28/37** | 24/37 |
| 15 Aug vs 19b (40 prompts) | 24/40 | **29/40** |

**Reading.** Same-day ranking is exact chance on both windows. Within-day
draw noise does **not** explain the 15-vs-19a last-1 shift. That shift is
between days. 19b vs pre-mark flipped the order (last-4 ahead of last-1).
Do not call that a watermark. Resample tomorrow.

---

## 2026-08-20 schedule

Installed host calendar job `se.makeitso.text-watermark-claude-resample`
(launchd): **Wednesday, Friday, Sunday at 04:00** local, until cancelled.
Command: `python -m text_watermark_tools resample`. Cancel:
`scripts/install_claude_resample_schedule.sh uninstall`.
Mac must be awake and Chrome logged in at claude.ai. Next fire: Friday
2026-08-21 04:00.

---
## 2026-08-21 resample

**Collection.** `/Users/jens/kod/text-watermark-tools/experiments/claude-sample-2026-08-21` — **0** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-08-21-resample-work`.

---
## 2026-08-21 resample

**Collection.** `experiments/claude-sample-2026-08-21` — **40** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

| Contrast | last-1 | last-4 |
|---|---|---|
| premark-vs-new (40 prompts) | 33/40 | 34/40 |
| previous-vs-new (40 prompts) | 31/40 | 35/40 |

Last-1 ahead of last-4 is the style-shift order. Last-4 ahead of last-1 is the public-mixin watermark-window order. Do not call either a vendor detector. Same-day chance means draw noise.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-08-21-resample-work`.

---

## 2026-08-22 Xenova tokenizer check

Same twins as 21 Aug, retokenized with `Xenova/claude-tokenizer` (Claude 1/2-era
65k BPE from Anthropic’s old SDK, **not** Claude 3+/5). `used_keys=false`.
Not their detector.

| Contrast | GPT-2 last-1 | GPT-2 last-4 | Xenova last-1 | Xenova last-4 |
|---|---|---|---|---|
| 15 Aug vs 21 | 33/40 | 34/40 | 35/40 | 35/40 |
| 19b vs 21 | 31/40 | 35/40 | 30/40 | 32/40 |
| 19a vs 19b (same day) | 19/38 | 19/38 | 21/38 | 20/38 |

Same-day stays near chance. Between-day ranking is not a GPT-2 artifact.
Xenova is still the wrong generation of tokenizer. Do not call this a watermark.

---

## 2026-08-31 key-free probe and argmax snap

Same 12×4 GPT-2 twins. No keys. `used_keys=false`.

Coverage-gated last-4 (`hits`) **11/12**, file AUC **0.737**. Hashpool **11/12**, isolated marked `lr>0` **35/48** (binomial p≈0.001). Hard last-4 still **10/12** / **29/48**. Witten–Bell interpolate and backoff did **not** help (7/12, AUC≈0.52). Unmarked-LM pivot is above chance but weaker (LDA 10/12, AUC 0.599).

Argmax snap on all 48 marked files: official mean **0.6216 → 0.4994**. Unmarked control stayed near half. Statistical scrub, not a fluent rewrite.

36 GPT-2 topics × 1: hard last-4 **20/36**; `hits` **30/36** AUC **0.886**; hashpool **31/36** AUC **0.877**. The old “more topics do not help” result was the hard scorer. Qwen 12×1: hashpool **10/12** AUC **0.750**; exact `hits` AUC **0.417**.

Notes: [key-free-probe.md](key-free-probe.md). JSON: `experiments/2026-08-31-probe-12x4/`, `experiments/2026-08-31-probe-36/`, `experiments/2026-08-31-probe-qwen/`, `experiments/2026-08-31-scrub-12x4/`.

---
