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
## 2026-08-23 resample

**Collection.** `/Users/jens/kod/text-watermark-tools/experiments/claude-sample-2026-08-23` — **0** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-08-23-resample-work`.

---
## 2026-08-26 resample

**Collection.** `/Users/jens/kod/text-watermark-tools/experiments/claude-sample-2026-08-26` — **0** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-08-26-resample-work`.

---
## 2026-08-28 resample

**Collection.** `/Users/jens/kod/text-watermark-tools/experiments/claude-sample-2026-08-28` — **0** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-08-28-resample-work`.

---
## 2026-08-30 resample

**Collection.** `/Users/jens/kod/text-watermark-tools/experiments/claude-sample-2026-08-30` — **0** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-08-30-resample-work`.

---
## 2026-08-31 key-free probe and argmax snap

Same 12×4 GPT-2 twins. No keys. `used_keys=false`.

Coverage-gated last-4 (`hits`) **11/12**, file AUC **0.737**. Hashpool **11/12**, isolated marked `lr>0` **35/48** (binomial p≈0.001). Hard last-4 still **10/12** / **29/48**. Witten–Bell interpolate and backoff did **not** help (7/12, AUC≈0.52). Unmarked-LM pivot is above chance but weaker (LDA 10/12, AUC 0.599).

Argmax snap on all 48 marked files: official mean **0.6216 → 0.4994**. Unmarked control stayed near half. Statistical scrub, not a fluent rewrite.

36 GPT-2 topics × 1: hard last-4 **20/36**; `hits` **30/36** AUC **0.886**; hashpool **31/36** AUC **0.877**. The old “more topics do not help” result was the hard scorer. Qwen 12×1: hashpool **10/12** AUC **0.750**; exact `hits` AUC **0.417**.

Notes: [key-free-probe.md](key-free-probe.md). JSON: `experiments/2026-08-31-probe-12x4/`, `experiments/2026-08-31-probe-36/`, `experiments/2026-08-31-probe-qwen/`, `experiments/2026-08-31-scrub-12x4/`.

Train 24 other 36-topic stems, score 12×4: hits isolated **39/48** (AUC **0.769**); hashpool prompt **11/12**. Train 12×4, score stems 13–36: hits **24/24** ranking (AUC **0.986**, unmarked ≤0 14/24); hashpool **23/24**. Stack LDA of hits+hashpool on 12×4 LOO: **11/12**, AUC 0.732, unmarked ≤0 44/48. Frozen hashpool tables: `experiments/2026-08-31-transfer-36-to-12x4/tables-hashpool/`. `indicate fit --method hashpool` / `indicate score` can now use that reader on one file.

JSON: `experiments/2026-08-31-transfer-36-to-12x4/`, `experiments/2026-08-31-transfer-12x4-to-36/`, `experiments/2026-08-31-stack-12x4/`.

Nested train-only thresholds on the same splits: OOD hashpool Youden **33/48** marked / **34/48** unmarked; reverse `freqhits` **23/24** and **23/24**. `hitmass` recovers OOD prompt grain **10/12**. A 50% train-label shuffle drops isolated sign to 19–20/48. `surface` is a UTF-8 byte hashpool (no tokenizer): 12×4 LOO **10/12** AUC 0.602; Qwen LOO **9/12**. Same-topic GPT-2 hits through GPT-2 BPE of Qwen text ranks **11/12** (isolated `lr>0` 1/12); new topics plus Qwen is chance. `logit` is nested-calibrated ridge logistic on the file scores. JSON: `experiments/2026-08-31-transfer-nested-36-to-12x4/`, `experiments/2026-08-31-transfer-nested-12x4-to-36/`, `experiments/2026-08-31-transfer-shuffle-36-to-12x4/`, `experiments/2026-08-31-probe-surface-12x4/`, `experiments/2026-08-31-transfer-gpt2-to-qwen/`, `experiments/2026-08-31-transfer-36-to-qwen/`.

---

## 2026-08-31 extra draws (36×4)

New GPT-2 corpus: 36 prompts × 4 draws × 128 tokens (`experiments/2026-08-31-pair-36x4/`). Official first-draw **36/36**. `used_keys=false` on every key-free number below.

Leave-one-out hits **36/36**, AUC **0.934**, isolated 134/144 at t=0. Nested-by-stem Youden (threshold from other stems' held-out LRs): **119/144** vs **134/144**. Draw ablation on the same files: 1-draw hits **30/36** (AUC 0.845); 2-draw **33/36**; 4-draw **36/36**. Extra draws, not extra topics, are the lift. Hashpool on the short 1-draw slice is only 23/36.

Train 24 new stems × 4, score original 12×4: hits **12/12**, AUC **0.793**, isolated **42/48**. Nested hits Youden **26/48** vs **44/48**. Reverse — train 12×4, score 96 new-topic files: hits **24/24**, AUC 0.924; nested hits 10% FPR **83/96** vs **85/96**.

Do not replace the published hard last-4 **10/12** / **29/48** with 36/36. 36/36 is in-domain. The 83/96 gate is still GPT-2 laboratory prompts.

JSON: `experiments/2026-08-31-probe-36x4/`, `experiments/2026-08-31-transfer-36x4-to-12x4/`, `experiments/2026-08-31-transfer-12x4-to-36x4/`.

New Qwen 12×4 sample (`experiments/2026-08-31-pair-qwen-12x4/`, seed 20260831): official **12/12**. In-domain hits **8/12** AUC 0.602; hashpool 7/12. Extra Qwen draws do not copy the GPT-2 extra-draw lift. GPT-2 12×4 tables on this new Qwen sample (probe BPE): hits **5/12** AUC 0.355. The published same-topic **11/12** on the original Qwen 12×1 corpus does not replicate.

JSON: `experiments/2026-08-31-probe-qwen-12x4/`, `experiments/2026-08-31-transfer-gpt2-to-qwen-12x4/`.

---

## 2026-08-31 prefix curves, last-5 ablation, Qwen negatives

Same 36×4 GPT-2 twins. `used_keys=false`. `--prefix-lens` clips completions
before scoring. Sixteen tokens already rank **34/36** in-domain (AUC **0.916**,
isolated 129/144). Prefix 128 matches the published full-file 36/36 / 0.934 /
119 vs 134. New-topic 24×4 → 12×4: 16-token hits **11/12** AUC **0.752**,
nested-by-stem **25/48** vs **29/48**. Ranking is early; the nested isolated
gate on short prefixes is not. Disjoint windows show the key-free 4-gram
signal is in the opening, not throughout: in-domain 16–32 tokens are near
chance (hits 22/36, AUC 0.549); OOD 16–32 is chance (8/12, AUC 0.512). The
keyed mixin still marks later tokens; the count-table reader does not pick
them up as shared 4-grams.

`--context-len 5` on 36×4 hits **35/36** AUC **0.912**. Matching mixin
`ngram_len=5` does not beat last-4. Keep `context_len=4`.

GPT-2 36×4 → new Qwen 12×4 (drop overlapping stems): hits **6/12** AUC 0.445,
hashpool 3/12, surface 6/12. Same-topic GPT-2 surface → that Qwen sample:
**7/12** AUC 0.525, isolated 5/48. Extra GPT-2 draws do not create a Qwen
detector. Do not overwrite the published original-corpus Qwen hashpool 10/12.

JSON: `experiments/2026-08-31-probe-36x4-prefixes/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-prefixes/`,
`experiments/2026-08-31-probe-36x4-windows/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-windows/`,
`experiments/2026-08-31-probe-36x4-k5/`,
`experiments/2026-08-31-transfer-36x4-to-qwen-12x4/`,
`experiments/2026-08-31-transfer-gpt2-surface-to-qwen-12x4/`.

---

## 2026-08-31 matched 16-token fit and position-bucketed last-4

Same 36×4 / 12×4 GPT-2 twins. `used_keys=false`. `--fit-prefix 16` clips
token ids before fit and score (not `--prefix-lens 16` on a full-file
table). `--pos-bucket 16` prepends `i // 16` to last-4 for `poshits` /
`pospool`. That namespace is not a watermark key.

In-domain matched 16-token hits: **34/36**, AUC **0.929**, isolated
132/144, unmarked ≤0 **112/144** (full-file hits unmarked ≤0 76/144;
fit-full/score-prefix 16 was 93/144). Nested-by-stem **121/144** vs
**136/144**. New-topic matched 16-token hits: **11/12**, AUC **0.818**,
unmarked ≤0 31/48, nested-by-stem **39/48** vs **36/48**. File AUC beats
full-file OOD hits (0.793). Prompt grain drops one stem.

In-domain poshits: **34/36**, AUC 0.925, same **134/144** marked t=0 as
hits, unmarked ≤0 **97/144**. Nested-by-stem 119 vs 129. New-topic
poshits: **10/12**, AUC **0.811**, nested-by-stem **37/48** vs **35/48**.
On 12×4 leave-one-out poshits is a specificity knob (24/48 marked,
37/48 unmarked). Do not replace 10/12, 29/48, or 36/36.

JSON: `experiments/2026-08-31-probe-36x4-fitprefix16/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix16/`,
`experiments/2026-08-31-probe-36x4-posbucket/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-posbucket/`,
`experiments/2026-08-31-probe-12x4-posbucket/`.

Bucket 4 on the same 16-token window (not bucket 16, which is a no-op
there): in-domain poshits **34/36**, AUC **0.937**, unmarked ≤0
**114/144**. New-topic **11/12**, AUC **0.820**, nested-by-stem **39/48**
vs **38/48**. JSON: `experiments/2026-08-31-probe-36x4-fitprefix16-pos4/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos4/`.

---

## 2026-08-31 coverage mechanism and finest-bucket isolated-file gate

Same twins. `used_keys=false`. `--coverage` is leave-one-prompt-out share
of last-k contexts seen on both training sides.

Window 0:16 shares **13.7%** vs **3.9%** on 16:32, but that average is
last-1/last-2 at i=1–2 (i=1 is **96.9%** shared). Full last-4 from i=4
is ~3–4% everywhere. Scoring **0:4** already ranks **34/36** (AUC
**0.917**), matching 0:16. Tokens 4:16 are 29/36 (AUC 0.712); 16:32 is
chance.

Matched `--fit-prefix 4 --pos-bucket 1`: in-domain **34/36**, AUC
**0.935**, t=0 **131/144 vs 132/144**. New-topic **12/12**, AUC
**0.873**, t=0 **39/48 vs 41/48**, nested Youden matching t=0. The
16-token finest-bucket reader copies those OOD numbers (nested Youden
there is conservative). poshitmass on 16-token bucket 4: in-domain AUC
**0.943** (still 34/36). 12×4 LOO of the 16-token reader is 9/12 / 23/48.
GPT-2 → Qwen is chance (8/12, AUC 0.516). Do not replace 10/12, 29/48,
or 36/36.

JSON: `experiments/2026-08-31-probe-36x4-coverage/`,
`experiments/2026-08-31-probe-36x4-windows-opening/`,
`experiments/2026-08-31-probe-36x4-fitprefix4-pos1/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-pos1/`,
`experiments/2026-08-31-probe-36x4-fitprefix16-pos-sweep/`,
`experiments/2026-08-31-probe-36x4-fitprefix16-poshitmass/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos1/`.

---

## 2026-08-31 first token, prompt context, Qwen opening, DistilGPT2

The published last-k reader skips generated token 0. `--include-first`
stores it under a sentinel unigram (not a key). `--prompt-context` uses
`*-prompt.txt` as last-k so token 0 sees the prompt the mixin sees.
`--methods first` is token 0 alone. Isolated `indicate score` of a lone
file cannot reconstruct the prompt.

Last-1 on the four-token opening copies the new-topic poshits gate
(**12/12**, AUC **0.873**, t=0 **39/48 vs 41/48**). Mixing token 0 into
hits hurts that gate (9/12, AUC 0.719). Prompt-as-context ranks 12/12
OOD with isolated 13/48.

Qwen in-domain first-token opening is **12/12**, AUC **0.901**. Hits
without token 0 is 7/12. GPT-2 → Qwen stays chance.

DistilGPT2 12×4 is officially **12/12**. In-domain hits **9/12**, AUC
0.705. GPT-2 36×4 → Distil (same BPE) hits **5/12**, AUC **0.462**. Same
keys and tokenizer are not a transferable 4-gram detector. Do not
replace 10/12, 29/48, or 36/36.

JSON: `experiments/2026-08-31-probe-36x4-fitprefix4-k1-pos1/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-k1-pos1/`,
`experiments/2026-08-31-probe-qwen-12x4-fitprefix4-pos1/`,
`experiments/2026-08-31-pair-distilgpt2-12x4/`,
`experiments/2026-08-31-transfer-36x4-to-distilgpt2-12x4/`.

## 2026-08-31 learned scorers (hashlog / tokmlp / charcnn)

Tiny key-free classifiers on the same 4-token twins. Not keys, not
Claude, not a replacement of 10/12 or 29/48. Protocol:
[key-free-learn.md](key-free-learn.md).

On the new-topic GPT-2 gate (24×4 → 12×4) poshits remains **12/12**,
AUC **0.873**, t=0 **39/48 vs 41/48**. tokmlp is 8/12, AUC 0.714.
hashlog 7/12, AUC 0.606. charcnn 7/12, AUC 0.557. GPT-2 nets do not
transfer to DistilGPT2 or Qwen (charcnn Qwen AUC 0.496). Qwen
`--include-first` hashlog ranks 12/12, AUC 0.826 — below the first-token
count table (0.901). hashlog 12×4 LOO 11/12 is in-family; the same
reader is 7/12 on new topics. tokmlp shuffle collapses (5/12, AUC
0.471); hashlog/charcnn shuffle do not.

JSON: `experiments/2026-08-31-learn-36x4-to-12x4-fitprefix4/`,
`experiments/2026-08-31-learn-36x4-fitprefix4/`,
`experiments/2026-08-31-learn-36x4-to-distil-fitprefix4/`,
`experiments/2026-08-31-learn-36x4-to-qwen-fitprefix4/`.

## 2026-08-31 instance contrast (public vs control-shuffled-30)

Official `score` already treats `control-shuffled-30` as another instance
(public ~0.50, matching ~0.62). Key-free tables fit on public
marked/unmarked only; control-gen is never a `*-marked.txt`. Protocol:
[key-free-contrast.md](key-free-contrast.md). Not key recovery. Do not
replace 10/12, 29/48, or 36/36.

New 12×4 control pile (`--control-only`, seed 20260931): 48 files, public
mean of means **0.501**, matching **0.624**. Matched 4-token poshits
(24 other 36×4 stems → 12×4): public-vs-unmarked still **12/12**, AUC
**0.873**, t=0 **39/48 vs 41/48**. Control-vs-unmarked isolated `lr>0` is
**0/48** (AUC 0.510). Public vs control **12/12**, AUC **0.906**, all 48
control files `≤ 0`. Hits on that opening is also **0/48** control `lr>0`.
Hashpool leaks (**6/48**). Unbucketed hits on full 128-token files is not
the instance sign (control `lr>0` **29/48**, AUC vs unmarked 0.475).
700-token hits public vs control AUC **1.000**; control vs unmarked 0.556.

JSON: `experiments/2026-08-31-pair-12x4-controlkeys/`,
`experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4/`,
`experiments/2026-08-31-contrast-36x4-to-12x4-full/`,
`experiments/2026-08-31-contrast-36x4-to-limit-fitprefix4/`,
`experiments/2026-08-31-contrast-36x4-to-limit-full/`.

## 2026-08-31 tokhits: occupancy Laplace vs observed next tokens

The 4-token poshits OOD gate is still **12/12**, AUC **0.873**, t=0
**39/48 vs 41/48**. Nine marked misses are zeros. Hits scores an unseen
next token after a shared context via Laplace. On this split `'The'` at
index 1 is 8 marked vs 52 unmarked, so every novel continuation gets
δ = 0.330103: **23 of 39** marked TPs and **all 7** unmarked FPs.
`postokhits` skips those: **12/12**, isolated **16/48**, decided
precision **1.000** (16 TP, 0 FP). In-domain 36×4 LOO poshits **131/144**
drops only to **122/144**; 9 of 131 TPs were occupancy. Control-shuffled-30
stays **0/48** `lr>0` under postokhits. Do not sell 16/48 as beating
39/48. Do not replace 10/12, 29/48, or 36/36. Protocol:
[key-free-tokhits.md](key-free-tokhits.md).

JSON: `experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits/`,
`experiments/2026-08-31-probe-36x4-fitprefix4-postokhits/`,
`experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokhits/`.

The 24 extra train seeds are 10–12 word one-liners; the 12×4 test seeds
are 37–241 words. Observed-token transfer is mostly quote-dialogue.
The nine zeros continue the longer seeds.

## 2026-08-31 medium-length new-topic twins

Twelve new ~41–51 word scene seeds × 4 draws × 128 tokens
(`experiments/2026-08-31-prompts-long12/`, seed 20260901). Official
first-draw lamp **12/12**. Generated token 0 is only `"` and `The`.

Train those 12, score original 12×4 (`--fit-prefix 4 --pos-bucket 1`):
postokhits **12/12**, isolated **19/48**, precision **1.000** among
decided (19 TP, 0 FP). Combined with the 24 short one-liners:
**20/48**. The same nine After / Closing / Now / While zeros remain.

On this train, unseen-after-The Laplace **flips** (δ ≈ −0.365). poshits
is 8/12 with 20 marked wrong-sign files. The 39/48 short-train poshits
number is occupancy-specific. Do not replace 10/12, 29/48, 16/48, or
39/48.

JSON: `experiments/2026-08-31-pair-long12x4/`,
`experiments/2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokhits/`,
`experiments/2026-08-31-transfer-short24-plus-long12-to-12x4-fitprefix4-tokhits/`.

## 2026-08-31 tokbackoff: shrink last-k until an observed next token

`postokbackoff` on the short-train 4-token OOD gate copies postokhits
**16/48**. On the 12 medium scenes it is **21/48** (harbour draws 3 and
4 via last-1 `' was' → ' in'`). Combined short+medium **22/48**. Precision
**1.000** among decided. The nine After / Closing / Now / While zeros
remain. In-domain 36×4: still **122/144** marked, one extra unmarked FP.
Control-shuffled-30 stays **0/48**. Do not sell 21/48 or 22/48 as beating
39/48.

JSON: `experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokbackoff/`,
`experiments/2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokbackoff/`,
`experiments/2026-08-31-transfer-short24-plus-long12-to-12x4-fitprefix4-tokbackoff/`,
`experiments/2026-08-31-probe-36x4-fitprefix4-postokbackoff/`,
`experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokbackoff/`.

## 2026-08-31 prompt-tail transplant

Three new bodies with last paragraphs from night-bus / library / letter /
garden (`experiments/2026-08-31-prompts-tails12/`, seed 20260902). Official
lamp **12/12**. Token 0 is mostly `The`. No Closing. One depot-tail draw
is `After two and a`. One letter-tail draw is `Now a little after`.

Train tails only → 12×4: postokhits **10/48**, postokbackoff **23/48**,
precision **1.000**. Short+medium+tails: postokhits **30/48**,
postokbackoff **36/48**, AUC **0.888**, precision **1.000**. Of the nine
zeros, night-bus and garden become exact hits; library scores only under
backoff last-1 `' is' → ' the'`; letter stays zero. Tail-matching is
close to in-family. Do not sell 30/48 or 36/48 as beating 39/48. Do not
replace 10/12, 29/48, or 36/36.

JSON: `experiments/2026-08-31-pair-tails12x4/`,
`experiments/2026-08-31-transfer-tails12x4-to-12x4-fitprefix4-tokbackoff/`,
`experiments/2026-08-31-transfer-short-medium-tails-to-12x4-fitprefix4-tokbackoff/`.

## 2026-08-31 opening-overlap bound and last-2 floor

Isolated observed-token recall equals train opening-atom overlap.
`postokbackoff2` (will not shrink below last-2) stays **13/48** on 24
short, +medium, and +tails. Last-1 carries 16→36 (six later last-1:
library `' is' → ' the'`, harbour `' was' → ' in'`). Unbucketed
tokbackoff copies 36/48 with **3** unmarked FP. `--include-first`
postokhits is a first-token unigram (**43/48**, 10 FP). Leftover
postokbackoff zeros: ferry was so/over/waiting, printer worked, one
station, `Now in the second`, `While working on the`. Not a universal
detector. Do not sell 13/48, 36/48, or 43/48 as beating 39/48. Do not
replace 10/12, 29/48, or 36/36.

JSON: `experiments/2026-08-31-openings-short-medium-tails/`,
`experiments/2026-08-31-openings-short-medium-tails-unbucketed/`,
`experiments/2026-08-31-openings-short-medium-tails-includefirst/`.

## 2026-08-31 neighborhood paraphrases for leftover zeros

Twelve new ~40–55 word scenes in the leftover-zero neighborhoods
(`experiments/2026-08-31-prompts-family12/`, seed 20260903). Official
lamp **12/12**. Token 0 is `The` or quote-dialogue. No Closing / Now /
While / After / The ferry / The printer.

Added to the opening-overlap curve: postokhits **38/48**, postokbackoff
**42/48**, postokbackoff2 **15/48**, precision **1.000**. Exact 4-token
stays 19/48. The +6 backoff files are ferry `was so/over/waiting` via
last-1. Letter Now/While, printer, and station remain zeros. Neighborhood
is not those openings. Do not sell 42/48 as beating 39/48.

JSON: `experiments/2026-08-31-pair-family12x4/`,
`experiments/2026-08-31-openings-short-medium-tails-family/`.

## 2026-08-31 coverage-then-pivot cascade

Opening-only unmarked-LM geometry (4 generated tokens, no prompt)
leave-one-of-12-out: pivot-lda **10/12**, AUC **0.672**, isolated
**27/48**. That beats the published 128-token pivot-lda (0.599, 17/48).
Prompt-conditioned opening LDA is worse than chance (7/12, AUC 0.468).
OOD 24-short → 12×4: postokbackoff still **16/48** precision 1.0;
opening LDA does not transfer (4/12). Combined 60-stem train covers
42/48 and marks **34/48** (eight covered files have negative LR);
cascade combined 39/48 spends 15 unmarked FPs. `indicate score` now
prints `n_used` and `decision=ABSTAIN` at coverage 0. Not a universal
detector. Do not sell 27/48, 34/48, or 39/48 as beating 39/48 poshits
or replacing 29/48. Do not replace 10/12 or 36/36.

JSON: `experiments/2026-08-31-probe-12x4-fitprefix4-cascade-isolated/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-cascade-isolated/`,
`experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-isolated/`.
Write-up: [key-free-cascade.md](key-free-cascade.md).

## 2026-08-31 rank-path tables

Five-symbol unmarked-LM rank paths (miss / argmax / 2–3 / 4–10 / 11–k),
still no keys. 4-token isolated openings. In-domain 12×4 LOO: rankpath
**12/12**, AUC **0.797**, isolated **41/48** vs 39/48 unmarked ≤0
(precision 0.820). That beats opening LDA 27/48. OOD 24-short → 12×4:
rankpath **10/12**, **28/48**, precision 0.651; LDA stays at chance
(4/12). Combined 60-stem: rankpath **12/12** ranking, rankuni 37/48
with 17 unmarked FPs; leftover count zeros 2/6. Cascade mixed scores
are not a detector. Do not sell 41/48, 28/48, or 37/48 as replacing
29/48 or beating 39/48 poshits.

JSON: `experiments/2026-08-31-probe-12x4-fitprefix4-rankpath-isolated/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-rankpath-isolated/`,
`experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-rankpath-isolated/`.
Write-up: [key-free-rankpath.md](key-free-rankpath.md).

## 2026-08-31 full-file rank-path is front-loaded

Unbucketed `--rankpath-full` on 128-token files. In-domain full path is
chance (8/12, AUC 0.559, perm p=0.145). Window 16:32 is chance in-domain
and OOD, matching token-identity hits. Matched prefix of four rank
symbols transfers: **11/12**, AUC **0.759**, isolated **25/48 vs 43/48**
(5 unmarked FPs, precision 0.833). That is not the pos-bucket-1 opening
28/48 and not 39/48. 60-stem count tables plus full-file rankpath
fallback: 4/6 leftover zeros, 17 unmarked FPs, cascade 38/48 precision
0.691. Do not sell full-file rankpath or cascade 38/48. Keep the opening
reader.

JSON: `experiments/2026-08-31-probe-12x4-rankpath-full-isolated/`,
`experiments/2026-08-31-transfer-36x4-to-12x4-rankpath-full-isolated/`,
`experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-rankpath-full-cascade/`.
Write-up: [key-free-rankpath.md](key-free-rankpath.md).

## 2026-08-31 rank-path instance contrast and prefix-4 cascade

Public 36×4 rankpath tables vs 12×4 public and `control-shuffled-30`.
Opening rankpath control ranking is chance (AUC **0.498**); isolated
control `lr>0` **17/48**. Unbucketed prefix-4 rankpath: public
**11/12**, AUC **0.759**, **25/48 vs 43/48**; control AUC **0.511**,
isolated **6/48** (same FP rate as unmarked). Opening rankuni is a
tournament detector (control **30/48**, public vs control AUC **0.502**).
Not poshits **0/48**. Not key recovery.

60-stem count plus prefix-4 rankpath fallback: **1/6** leftover zeros,
5 unmarked FPs, cascade **35/48 vs 43/48**. Higher precision than
opening rankuni (15 FPs) and full-file rankpath (17 FPs). Do not sell
35/48.

JSON: `experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4-rankpath/`,
`experiments/2026-08-31-contrast-36x4-to-12x4-prefix4-rankpath/`,
`experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/`.
Write-up: [key-free-rankpath.md](key-free-rankpath.md).

## 2026-08-31 Distil/Qwen rankpath and 60-stem prefix-4 standalone

DistilGPT2 12×4 is officially **12/12**. Native Distil unmarked-LM
opening rankpath is chance: **8/12**, AUC **0.579**, perm p=0.132,
isolated 28/48 vs 32/48. Prefix-4 is **7/12**, AUC 0.563. Distil
in-domain token hits on the same pile is 9/12. Rank-path is **not** a
universal tournament detector across GPT-2-family generators.

GPT-2 36×4 rankpath scored on Distil tokens with the GPT-2 LM (wrong
LM): **9/12**, AUC 0.636, isolated **21/48 vs 34/48**. Weak ranking,
not a Distil reader. Token hits on that split stay 5/12 / 0.462.

Qwen2-1.5B opening rankpath: **8/12**, AUC **0.590**, isolated 24/48 vs
32/48. Prefix-4 is **9/12**, AUC **0.662**, isolated 25/48 vs 33/48
(perm p=0.0035). Qwen’s in-domain opening remains token 0 (`first`
**12/12**, AUC **0.901**). Rankpath starts at generated token 1 and
does not recover that.

60-stem prefix-4 as a standalone isolated-file reader (not leftover
cascade): rankpath **10/12**, AUC **0.770**, **28/48 vs 40/48**.
24-short prefix-4 was 11/12, 25/48 vs 43/48. Combined accuracy is the
same **68/96**. Do not sell 28/48 as beating 29/48, or rankuni 39/48
(16 FPs) as beating poshits 39/48.

JSON: `experiments/2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath/`,
`experiments/2026-08-31-probe-distilgpt2-12x4-prefix4-rankpath/`,
`experiments/2026-08-31-transfer-36x4-to-distilgpt2-fitprefix4-rankpath/`,
`experiments/2026-08-31-probe-qwen-12x4-fitprefix4-rankpath/`,
`experiments/2026-08-31-probe-qwen-12x4-prefix4-rankpath/`,
`experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-prefix4-rankpath/`.
Write-up: [key-free-rankpath.md](key-free-rankpath.md).

## 2026-08-31 cascade-when positive on covered-negative ferry openings

Coverage cascade keeps a negative count LR when `n_used>0`. Eight
60-stem covered files are harbour / ferry-queue `The ferry was …`
openings (last-1 `' was'` looks unmarked). Rebound prefix-4 rankpath
on count-nonpositive files (`--cascade-when positive`), no new GPT-2
forwards: combined **40/48 vs 40/48** (5 of 8 covered-negatives plus
the leftover printer zero; 8 unmarked FPs). Count alone stays
**34/48 vs 48/48**, precision 1.0. Combined accuracy 80/96 vs count
82/96. Do not sell 40/48 as beating poshits 39/48 or replacing 29/48.

JSON: `experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4-when-positive/`.
Write-up: [key-free-cascade.md](key-free-cascade.md).

## 2026-09-01 table-free opening snap-rate

No twin tables. Unmarked GPT-2 rows only. Opening `--fit-prefix 4`:
`snapupset` (in-topk not argmax) is chance **7/12**, AUC **0.501**, perm
p=0.55. Marked and unmarked leave the greedy top-k token at the same
rate (0.649 vs 0.653). `snapleave` majority vote is 48/48 vs 7/48 (not
a detector). `snapmiss` ranks **10/12**, AUC **0.707**, isolated
**21/48 vs 41/48** (off-mode continuation, corr 0.87 with opening
pivot-rank, 0.23 with rankpath). Prefix-4 `snapupset` stays chance
(6/12, AUC 0.501). Do not sell 21/48 as beating 29/48. Rank-symbol
tables are not a dressed-up upset bit.

JSON: `experiments/2026-09-01-probe-12x4-fitprefix4-snaprate/`,
`experiments/2026-09-01-probe-12x4-prefix4-snaprate/`.
Write-up: [key-free-snaprate.md](key-free-snaprate.md).

## 2026-09-01 leftover eight are officially marked

Positive-when cascade misses eight 12×4 files. Official prefix-16 mean
**0.627**, all eight >0.55, matching the other 40 marked files
(0.626). Unmarked 0.496 (3/48 >0.55). Prefix 4 cannot be scored
(`ngram_len=5`). Letter d2/d3 first 5-grams are **0.733 / 0.767**.
Office d1/d3 are chance at 5 tokens and marked at 8. In-domain opening
rankpath already signs 7/8.

60-stem prefix-8 postokbackoff: **38/48 vs 40/48**, AUC **0.818**,
precision 0.826. Signs station / letter d3 / office ×2 via last-1
punctuation, not official 5-grams. Combined 78/96 vs prefix-4 count
82/96. Letter d2 stays a miss. Prefix-8 rankpath 30/48 vs 35/48. Do
not sell 38/48 as beating poshits 39/48.

JSON: `experiments/2026-09-01-official-prefix-leftover/`,
`experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-rankpath/`.
Write-up: [key-free-cascade.md](key-free-cascade.md).

## 2026-09-01 letter d2 official 5-gram is isolated-rank invisible

Letter d2 first 5-gram `Now in the second I` is officially marked
(mean **0.733**, 22/30). Isolated `--fit-prefix 4` never scores token
4. Isolated unmarked GPT-2 ranks that token at **41** (miss);
prompt-conditioned rank is **11**. Prefix-5 rankpath is **11/12**,
**30/48 vs 36/48**, letter d2 still `lr<0`. Fifth-token rankuni is
**4/12**, AUC **0.406**. Ferry-queue d4 is official 0.700 on the
argmax. Keep prefix-4. Do not sell 30/48.

JSON: `experiments/2026-09-01-letter-d2-first-ngram/`,
`experiments/2026-09-01-probe-12x4-fitprefix5-rankpath/`.
Write-up: [key-free-cascade.md](key-free-cascade.md).

60-stem prefix-8 `postokbackoff` letter d2 `n_used=2` is last-1
`' in' → ' the'` (2 vs 8), not the official 5-gram. That 5-gram is
unseen at last-4/3/2; `' second'` never continues with `' I'`.
`postokbackoff2` abstains. Letter d3's prefix-8 rescue is last-1
`',' → ' my'`. Isolated token-4 miss rate is 9/48 marked vs 7/48
unmarked. Officially marked 5-grams include both argmax (10) and miss
(8). Prefix-8 backoff's four extra TPs are last-1 punctuation; **20 of
38** TPs are last-1 only. `postokbackoff2` is **18/48 vs 46/48**.

## 2026-09-01 hashtok is occupancy-free hashpool, not a 5-gram reader

60-stem prefix-5 (`--fit-prefix 5`, last-4, official 5-gram grain).
hashpool **11/12**, **34/48 vs 34/48**, zero abstentions. hashtok
**9/12**, **30/48 vs 36/48**, five marked zeros. Those 30 true
positives are **exactly** postokhits' 30. Hashpool's extra four
(harbour d2/d3/d4, letter d2) have hashtok ≤0.

Letter d2 prefix-5 `Now in the second I`: all four positions have
0/8 hashes that saw the next token, including the official 5-gram
`I`. hashpool lr=0.372 is Laplace occupancy. hashtok `n_used=0`.
hybrid copies hashpool. Nested hashtok Youden **26/48 vs 42/48**.
Do not sell 34/48 or 30/48 as beating poshits 39/48.

JSON: `experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtok/`,
`experiments/2026-09-01-letter-d2-first-ngram/hashtok-trace.json`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashed backoff is per-order tables, not a 5-gram reader

60-stem prefix-5. `hashtokbackoff` fits separate hashpool tables per
order (1,2,3,4) and keeps the longest occupancy-free hit.
hashtokbackoff **10/12**, **38/48 vs 35/48**; hashtokbackoff2 **36/48
vs 34/48**. Nested Youden stays **30/48 vs 40–42/48**. Do not sell
38/48 or 36/48 as beating poshits 39/48.

Letter d2 official 5-gram `I`: last-4/3/2 hashes unseen; last-1 saw it
unmarked only (c_m=0, c_u=2, δ=−1.10). hashtokbackoff2's letter d2
lr=0.694 is tokens 1–2, not token 4. At i=1 the winning "order 3" is a
one-token prefix hashed into the order-3 table, not a 3-gram. Harbour
d3/d4 need last-1; library ×4 and letter d3 are order-4 hashed
observed-token extras.

Same train, published prefix-4 opening: hashtok **35/48 vs 39/48**;
hashed backoff **hurts** (**31/48 vs 33/48**, 15 FPs). Hashpool's extra
three versus hashtok are occupancy. Keep prefix-4 hashtok.

JSON: `experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtokbackoff/`,
`experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtokbackoff/`,
`experiments/2026-09-01-letter-d2-first-ngram/hashtokbackoff-trace.json`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 exact-length hashing drops short-prefix collisions

`hashtoklen` / `hashtoklenbackoff` hash only when `len(ctx) == order`.
60-stem prefix-5. hashtoklen **12/12**, **21/48 vs 45/48** (27 marked
zeros: only the official 5-gram slot). hashtoklenbackoff **11/12**,
**36/48 vs 34/48**, nested Youden **33/48 vs 42/48**.
hashtoklenbackoff2 t=0 **36/48 vs 35/48**, nested **28/48 vs 43/48**.

Mixed backoff library ×4 / letter d3 extras were order 4 at i=3
(`order > i`). Exact length: library survives as last-3
`'Cl' 'osing' ' is' → ' the'`; letter d3 extra is gone. Letter d2
hashtoklen `n_used=0`; backoff2 lr=0.797 is last-2 `'Now in' → ' the'`,
not official `I`; including last-1 of `I` (unmarked) makes
hashtoklenbackoff −0.152. Do not sell 36/48 or 33/48 as beating
poshits 39/48 or replacing 29/48.

JSON: `experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen/`,
`experiments/2026-09-01-letter-d2-first-ngram/hashtoklen-trace.json`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashtoklen recovers one exact 5-gram by collision

Twenty of 21 prefix-5 hashtoklen TPs are exact `postokhits`. Harbour
d2 `The ferry was over ,` is the extra: exact last-4 of the comma is
unmarked-like (lr=−2.65); occupancy-free hashing is marked-like
(+0.618) on **1/8** hashes (bucket 178, c_m=11, c_u=0). Not Laplace.
Letter d2 still abstains. In-domain 12×4 LOO hashtoklen **7/48 vs
48/48** (harbour d2 already a TP; letter d2 zero). Prefix-4
`hashtoklen` is **0/48** (no last-4 on a 4-token prefix). Exact
prefix-4 backoff **35/48 vs 38/48**, nested **35/48 vs 40/48** (mixed
backoff had hurt: 31/48). hashtoklen+rankpath cascade **33/48 vs
37/48**. Distil native hashtoklen **7/48 vs 48/48**. GPT-2 60-stem
tables on Distil: hashtoklen AUC **0.571**, **10/48**; backoff chance
(4/12, AUC 0.470). Do not sell 33/48, 10/48, or 7/48 as beating
poshits 39/48 or replacing 29/48.

JSON: `experiments/2026-09-01-letter-d2-first-ngram/harbour-d2-hashtoklen-trace.json`,
`experiments/2026-09-01-probe-12x4-fitprefix5-hashtoklen/`,
`experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtoklen/`,
`experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen-cascade-rankpath/`,
`experiments/2026-09-01-probe-distilgpt2-12x4-fitprefix5-hashtoklen/`,
`experiments/2026-09-01-transfer-short-medium-tails-family-to-distil-prefix5-hashtoklen/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 drop-one skip-grams see letter d2 unmarked

`hashskip` hashes exact last-4 with one token dropped (tagged so they
are not last-3). Occupancy-free. 60-stem prefix-5 → 12×4: **8/12**,
**25/48 vs 35/48**, nested Youden **16/48 vs 41/48**. t=0 extras vs
hashtoklen 21/48: harbour d3/d4, night-bus d2/d4, workshop d4; 13
unmarked FPs. Nested leftover fill-in **0/8**.

Letter d2 official `I` is no longer unseen: drop-2 and drop-3 skip
views saw it unmarked-only (c_m=0, c_u=1, lr=−0.847). Coarsening the
5-gram does not invent a marked preference. Do not sell 25/48 or
16/48 as beating poshits 39/48 or replacing 29/48.

JSON: `experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashskip/`,
`experiments/2026-09-01-letter-d2-first-ngram/letter-d2-hashskip-trace.json`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 eleven of twenty-one hashtoklen TPs are singleton collisions

`hashtoklen2` skips a hash unless `c_m + c_u ≥ 2`. Same frozen
exact-length tables. 60-stem prefix-5 → 12×4: **10/48 vs 48/48**,
precision 1.0, nested Youden matching t=0. Harbour d2 survives
(c_m=11, lr=+0.618). Letter d2 still abstains. Lost: night-bus d3,
market ×4, kitchen d2, station d1/d3, rain d2, garden d1/d4.
Leftover eight stay zeros.

`hashskip2` **22/48 vs 39/48**, nested **15/48 vs 41/48**. Letter d2
goes from −0.847 to 0 (unmarked singleton votes). Nested leftover
fill-in still **0/8**. Coverage-then-hashskip on saved holdouts is
worse than hashtoklen alone (26/48 vs 35/48). Do not sell 10/48,
22/48, or 15/48 as beating poshits 39/48 or replacing 29/48.

JSON: `experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 count-weighting and hashtoklen2 cascade are dead ends

Weighting occupancy-free hashes by `c_m+c_u` or `log(1+n)` keeps
prefix-5 hashtoklen **21/48 vs 45/48** (no sign flips). No file mixes
a singleton with a dense hash on the official slot. Rain d1 mixes n=7
with n=8; LR shifts 0.005. Weight `n-1` copies `min_count=2` (**10/48
vs 48/48**). Not a product.

Rebound `hashtoklen2` onto saved prefix-4 rankpath: coverage cascade
**28/48 vs 40/48**, the same as standalone rankpath. All 10 robust
5-gram TPs are already rankpath TPs. Leftover fill-in **0/8**. Combined
**68/96** vs hashtoklen cascade **70/96**. Do not add hashtoklen2 as a
cascade count channel. Do not sell 28/48.

JSON: `experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2-cascade-rankpath/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 MASK replace is worse nested than exact 5-grams

`hashmask` replaces one last-4 token with `MASK_TAG` (length stays 4).
Occupancy-free. 60-stem prefix-5 → 12×4: **11/12**, **21/48 vs 42/48**,
nested Youden **19/48 vs 45/48**. Same 21 TPs as hashtoklen at t=0
(extras harbour d3/d4, letter d2, workshop d4; lost market ×4). Nested
is **worse** than hashtoklen **21/48 vs 45/48**. `hashmask2` **15/48 vs
44/48**, nested **11/48 vs 45/48**.

Letter d2 official `I` is a MASK hit at `mask_i=3` (`Now in the MASK`
→ `I`): two opposing singletons average to file lr=+0.240, which is
that slot. Nested 0.778 throws it out. Leftover nested fill-in is
harbour d3/d4 only, not 8/8. Do not sell 21/48, 19/48, or 15/48 as
beating poshits 39/48 or replacing 29/48.

JSON: `experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashmask/`,
`experiments/2026-09-01-letter-d2-first-ngram/letter-d2-hashmask-trace.json`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 in-domain full-file hashtok is 33/48 vs 22/48

Leave-one-prompt-out on 12×4, full 128-token last-4. Hashpool matches
the published **35/48 vs 29/48**. Occupancy-free `hashtok` is **9/12**,
**33/48 vs 22/48**, nested-by-stem **22/48 vs 30/48** (hits nested
**22/48 vs 39/48**). `hashtoklen` **33/48 vs 23/48**, nested **30/48 vs
20/48**. Four extra TPs versus hard 29/48, 26 unmarked FPs. Occupancy
and occupancy-free disagree on six files. Letter d2 stays negative.
Do not sell 33/48 as replacing 29/48.

JSON: `experiments/2026-09-01-probe-12x4-hashtok/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashtok OR indicate is 39/48 TPs and not a detector

Saved 12×4 LOO scores. Complementary TPs are real: hashtok recovers
10 of 19 hard last-4 misses; indicate recovers 6 of 15 hashtok misses;
letter d2/d3/d4 stay misses on both. OR at t=0 is **39/48 vs 12/48**,
combined **51/96**, worse than indicate **52/96**. Nested LDA of the
two channels is **21/48 vs 37/48**. Coverage postokhits-then-hashtok
is **35/48 vs 22/48** (combined 57/96 vs postokhits 69/96). Do not
sell 39/48 as beating poshits 39/48 or replacing 29/48.

JSON: `experiments/2026-09-01-probe-12x4-hashtok-indicate-or/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 tokhybrid copies hashtok isolated 33/48

In-domain 12×4 LOO. Occupancy-free token-level hybrid (tokhits, then
hashtok) copies hashtok **33/48 vs 22/48** (same 33 TPs). Prompt grain
rises to **11/12** (station remains). Nested **23/48 vs 35/48**.
Occupancy hybrid extras are the same four files as hashpool vs hashtok.
`poshashtok` is **28/48 vs 25/48**, nested **14/48 vs 38/48**. Letter
d2 stays negative. Do not sell 33/48 or tokhybrid 11/12 as replacing
29/48.

JSON: `experiments/2026-09-01-probe-12x4-tokhybrid-poshashtok/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashtokgap is weaker than hashtok (27/48)

In-domain 12×4 LOO. Occupancy-free residual (hashtok only where tokhits
abstains) is **27/48 vs 21/48**, nested **17/48 vs 31/48**, prompt
**8/12**. True positives are a strict subset of hashtok's 33: loses
harbour d2, kitchen d1, station d1/d2/d3, rain d3; gains none. Combined
t=0 is 48/96 (chance). Letter d2 stays negative. Dropping
tokhits-scorable positions does not isolate a complementary hashed
signal. Do not sell 27/48 as replacing 29/48.

JSON: `experiments/2026-09-01-probe-12x4-hashtokgap/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashtok2 reshuffles full-file signs (34/48)

In-domain 12×4 LOO. Unbucketed `min_count=2` is **34/48 vs 21/48**,
nested **19/48 vs 35/48**, prompt **8/12**, AUC 0.602. Not the prefix-5
hashtoklen2 collapse (10/48 precision 1.0). Lost harbour d2, night-bus
d4, station d1; gained night-bus d3, library d1/d2, ferry-queue d4.
Combined t=0 stays 55/96. Letter d2 stays negative. Do not sell 34/48
as replacing 29/48.

JSON: `experiments/2026-09-01-probe-12x4-hashtok2/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 opening-grain hashtok copies tokhits (24/48)

In-domain 12×4 LOO, `--fit-prefix 4`. Occupancy-free hashing at the
published opening is sparse like tokhits, not opening rankpath
**41/48**. tokhits **23/48 vs 48/48** (prompt **12/12**, 25 marked
zeros). hashtok **24/48 vs 47/48**, nested **23/48 vs 47/48**, prompt
**12/12**: tokhits ⊂ hashtok; extra TP is letter d3; one unmarked FP
(kitchen d4). hashtok2 **22/48 vs 48/48** (gains letter d3, loses
kitchen d4 and rain d1). Letter d2 is zero on all four readers at this
grain. Marked isolated `lr>0` is **24/48**, below hard last-4 **29/48**.
Do not sell 24/48 as replacing 29/48.

JSON: `experiments/2026-09-01-probe-12x4-fitprefix4-hashtok/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 related-work note

Recorded keyed vs key-free neighbours so the research notes stay
current: Omidi et al. (2026) (SynthID mean/Bayesian theory;
layer-inflation is a keyed removal study, not implemented here);
Duan et al. (2025) (ZK of keyed detection); Wang et al. (2026)
(TTP-Detect).

## 2026-09-01 scientific references and annotation

Author–year convention ([CITING.md](CITING.md)), canonical BibTeX
([references.bib](references.bib)), and critical annotations
([annotated-bibliography.md](annotated-bibliography.md)). Corrected two
wrong attributions in earlier notes: Jovanović et al. (2024) stealing is
arXiv 2402.19361, not 2311.04378 (that is Zhang et al., 2024); arXiv
2405.20777 is Gloaguen et al. (2025), not Sabanayagam, Hörl, and Dobriban.
Do not write the dissertation until isolated-file research is finished.

## 2026-09-01 same problem, not a priority claim

Neither this lab nor the agent invented key-free detection. Closest
published analog is Wang et al. (2026) (TTP-Detect): same audit problem,
different method. Gloaguen et al. (2025) ask whether a *generator* is
watermarked via queries, not whether one finished file is marked.
Isolated hard last-4 stays **29/48**. See [related-work.md](related-work.md).

## 2026-09-01 hashtok mixer-width ablation

In-domain 12×4 full-file occupancy-free `hashtok` while varying
`--n-hashes`. Default n=8 is **33/48 vs 22/48**, nested **22/48 vs
30/48**, prompt **9/12**. n=2 is **34/48 vs 31/48**, nested **28/48 vs
37/48**, prompt **11/12**, AUC **0.764**. n=4 is densest t=0
(**36/48 vs 30/48**, nested **35/48 vs 30/48**). n=16 copies 36/48
with nested spec **24/48**. n=32 hurts (**30/48**, nested **21/48 vs
38/48**). Letter d2 stays negative except n=16; that prompt still
loses. Keep the CLI default at 8. Do not sell 36/48, 35/48, or 34/48
as replacing **29/48**. JSON:
`experiments/2026-09-01-probe-12x4-hashtok-nhashes{2,4,16,32}/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashtok mixer width does not transfer

24 new 36×4 stems → original 12×4 files, occupancy-free `hashtok`.
Default n=8 wins OOD: **11/12**, **29/48 vs 35/48**, nested Youden
**17/48 vs 46/48**, nested FPR10 **17/48 vs 46/48**. n=2 is 10/12,
nested **17/48 vs 44/48**. n=4 is densest t=0 (**31/48**) and nested
recall (**19/48 vs 41/48**) with the worst nested spec. The in-domain
n=2 / n=4 win did not transfer. Keep the CLI default at 8. t=0 29/48
here is not the headline hard last-4 **29/48**. Do not sell 31/48,
19/48, or 17/48. JSON:
`experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes{2,4,8}/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashtok n=2 seed sweep: not a width law

In-domain 12×4 hashtok n=2 while varying the feature-hash seed (not
SynthID `hash_iv`). Default seed 20260831 reproduces **34/48 vs 31/48**,
nested **28/48 vs 37/48**. Other n=2 seeds: unmarked spec **21–31/48**,
nested spec **25–37/48**, prompt **9–11/12**. Seed 0 keeps 34 TPs and
collapses spec to **21/48**. n=8 seed 7 nested **28/48 vs 37/48**
matches the advertised n=2 default. Letter d2 flips at seeds 0 and
12345. Keep CLI `n_hashes=8` and seed `20260831`. Do not sell 34/48 as
a width law. JSON:
`experiments/2026-09-01-probe-12x4-hashtok-nhashes2-seeds/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashtok transfer seed sweep: n=8 win is not a width law

24→12 occupancy-free `hashtok` at other feature-hash seeds (not
`hash_iv`). Default n=8 seed 20260831 is **11/12**, nested **17/48 vs
46/48**. Other n=8 seeds: prompt **10/12**, t=0 marked **25–27/48**.
n=2 seed 7 nested **19/48 vs 47/48** beats that default nested, with
prompt 9/12. Letter d2 flips at seed 0. Keep `n_hashes=8` and seed
`20260831`. Do not fish a seed. Do not sell 19/48. JSON:
`experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-seeds/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashtok last-k ablation: last-1 is chance

In-domain 12×4 occupancy-free `hashtok` while varying `--context-len`,
frozen `n_hashes=8` and seed `20260831`. Last-1 is chance (**5/12**,
AUC **0.507**, **22/48 vs 22/48**, nested **9/48 vs 42/48**). Last-3
is the best prompt ranking (**11/12**) and nested spec (**22/48 vs
40/48**), with sparser t=0 marked (**24/48**, below default **33/48**
and below hard last-4 **29/48**). Last-2 ranking is not a 5% test.
Letter d2 flips positive at last-3; not the official 5-gram. Keep
`--context-len 4`. Do not sell 24/48 or last-3 **11/12**. JSON:
`experiments/2026-09-01-probe-12x4-hashtok-k{1,2,3}/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 hashtok last-k does not transfer as a denser detector

24 new 36×4 stems → original 12×4 files, same frozen mixer. Last-4
still wins prompt ranking (**11/12**) and nested FPR10 (**17/48 vs
46/48**). Last-2 has the best file AUC (**0.738**) with nested Youden
**15/48 vs 45/48**. Last-1 nested-Youden recall **18/48** has prompt
**7/12** and FPR10 **8/48**. In-domain last-3 **11/12** does not
transfer (nested **11/48 vs 47/48**). Transfer t=0 29/48 is not the
headline hard last-4 **29/48**. Keep `--context-len 4`. Do not sell
18/48 nested or AUC 0.738. JSON:
`experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-k{1,2,3}/`.
Write-up: [key-free-hashtok.md](key-free-hashtok.md).

## 2026-09-01 confirmatory protocol freeze

Occupancy-free hashing on the old 12×4 / 36×4 twins is closed (width,
seed, last-k are knobs, not a denser isolated-file detector). Next
measurement is a frozen prediction on a new 100×4 corpus, not another
`probe --methods` name. Primary endpoint: prompt-level paired
discrimination under hard last-4. Opening poshits and opening rankpath
are the other two locked readers. Isolated `lr>0` is not the primary
endpoint. Protocol: [PROTOCOL-next.md](PROTOCOL-next.md). Index:
[results-ledger.md](results-ledger.md). Do not write `thesis/` from
this freeze.

## 2026-09-01 confirmatory prompts committed before pair

One hundred new one-line scenes in
`experiments/2026-09-01-prompts-100/`, disjoint from the 36-topic
seeds. This commit is still before `pair`. Seed `20260901`, four
draws, 128 tokens, as [PROTOCOL-next.md](PROTOCOL-next.md). Do not
open key-free LRs until generation and the frozen analysis commands
have run.

## 2026-09-01 README cut to three headlines

The root README is no longer an ablation dump. Locked claims are
**10/12**, **36/36**, **29/48**, plus the front-loaded opening. The
rest of the table lives in [results-ledger.md](results-ledger.md) and
[../experiments/README.md](../experiments/README.md). Wang et al.
(2026) stays the closest analog; a later TTP-Detect comparison is a
shared-data question, not a method race
([related-work.md](related-work.md)).

## 2026-09-01 truncated-context recount

Count tables used to store every order `1..k` even when fewer tokens
existed, so `fit_table([[10,20]], context_len=4)` counted `(10,)→20`
four times. Rankpath also skipped the empty first-symbol context.
After storing each real suffix once and scoring the first rank symbol:

- hard last-4 prompt ranking **9/12** (misses station, office,
  ferry-queue); binomial P(≥9) = 0.073
- same LRs, margin 0.02: **10/12** (ferry-queue flips)
- isolated hard `lr>0` **25/48 vs 22/48**; AUC **0.590**, permutation
  p **0.040**; binomial P(≥25) ≈ 0.44
- `hits` **10/12**, AUC **0.718**, **28/48 vs 31/48**
- opening poshits **9/12**, **23/48 vs 48/48**
- opening rankpath **11/12**, isolated still **41/48 vs 35/48**
- 36×4 hits still **36/36**, AUC **0.930**
- interpolate last-4 still **7/12** (PROTOCOL-next lock A unchanged)

Pre-fix **10/12** / **29/48** stay in historical JSON. Hashpool does
not use `_add_sequence`; those 2026-08-31 numbers were not this bug.
`indicate score --score-mode auto` now follows the fitted hash mixer.
Nested-by-stem remains a threshold nest on already-OOF scores, not a
second-level table refit. JSON:
`experiments/2026-09-01-blind-12x4-recount-last4/`,
`experiments/2026-09-01-probe-12x4-recount-hard-last4/`,
`experiments/2026-09-01-probe-12x4-recount-hits/`,
`experiments/2026-09-01-probe-12x4-recount-opening-poshits/`,
`experiments/2026-09-01-probe-12x4-recount-opening-rankpath/`,
`experiments/2026-09-01-probe-36x4-recount-hits/`. The confirmatory
100×4 pair is still generating; do not open those LRs until the frozen
PROTOCOL-next commands run on the corrected readers.

## 2026-09-01 confirmatory 100×4 pair (official lamp)

`pair` on `experiments/2026-09-01-prompts-100/` finished.
`experiments/2026-09-01-pair-100x4/`: seed `20260901`, four draws,
128 tokens, GPT-2 + `public-deepmind-30`. Official first-draw marked
mean > unmarked mean on **100/100** stems (min marked ≈ 0.576, max
unmarked ≈ 0.519). That is the keyed positive control, not the
key-free indicator. Frozen PROTOCOL-next probes run next on the
corrected readers; do not change flags.

## 2026-09-01 confirmatory Phase A (frozen probes)

Protocol SHA `7001489`. Prompts `294dba5`. Pair `bf98c92`. Flags
unchanged. `used_keys=false`.

- **H1 / lock A** interpolate last-4: **99/100** prompt ranking, file
  AUC **0.898**, permutation p < 0.001. Isolated **352/400 vs 290/400**.
  Stem **088** misses (`The stone trough held rainwater and a single
  floating leaf.`).
- **H2** windows: **0:4** **99/100**, AUC **0.885**; **16:32**
  **89/100**, AUC **0.689**. Early is stronger; mid-file is not chance.
- **Lock B** opening poshits: **100/100**, AUC **0.980**, isolated
  **393/400 vs 344/400**.
- **Lock C** opening rankpath: **96/100**, AUC **0.822**, isolated
  **314/400 vs 302/400**. `--rankpath` also emitted default methods;
  lock C is rankpath, not those extras.
- **H3** Distil/Qwen: not opened.

Do not sell 352/400 or 393/400 as replacing recounted hard **25/48**.
Nested-by-stem remains a threshold nest on already-OOF scores. JSON:
`experiments/2026-09-01-probe-100x4-hard-last4/`,
`experiments/2026-09-01-probe-100x4-opening-poshits/`,
`experiments/2026-09-01-probe-100x4-opening-rankpath/`,
`experiments/2026-09-01-probe-100x4-hard-windows/`.

## 2026-09-01 Phase B commands frozen before Distil/Qwen pair

Phase A is checked in. Exact DistilGPT2 and Qwen2-1.5B-Instruct pair
and opening probes (locks B and C only) are now in
[PROTOCOL-next.md](PROTOCOL-next.md). Seed `20260901`, four draws,
128 tokens, same 100 prompts. This commit still precedes those
`pair` runs. Do not look at key-free LRs until official first-draw
scores exist and the frozen opening probes have run once. H3 is
rankpath drop vs poshits drop relative to GPT-2 Phase A. Do not run
lock A on these twins.

## 2026-09-01 Phase B Distil opening locks

Native DistilGPT2, same 100 prompts, seed `20260901`. Official
first-draw marked > unmarked is **70/100** (weaker lamp than GPT-2
**100/100**; min marked ≈ 0.433). Mixin on/off remains ground truth.

- **Lock B** opening poshits: **89/100**, AUC **0.713**, isolated
  **216/400 vs 247/400**
- **Lock C** opening rankpath: **69/100**, AUC **0.598**, isolated
  **164/400 vs 270/400**

H3 on Distil so far: rankpath drop from GPT-2 Phase A is **27**
(96→69); poshits drop is **11** (100→89). Rankpath drops more.
`--rankpath` extras are not lock C. Do not sell Distil 89/100 or
69/100 as replacing **25/48**.

JSON: `experiments/2026-09-01-pair-distil-100x4/`,
`experiments/2026-09-01-probe-distil-100x4-opening-poshits/`,
`experiments/2026-09-01-probe-distil-100x4-opening-rankpath/`.

## 2026-09-01 isolated-file transfer frozen before 100→12 / 100→36

In-family 100×4 nested-by-stem Youden is already measured: lock A
**322/400 vs 338/400**, lock B **392/400 vs 382/400** (198/400 unmarked
`n_used=0`), lock C **312/400 vs 319/400**. Those do not replace
**25/48**. Exact out-of-family `probe --test-dir` commands for locks
A/B (and C after Qwen RAM) are in
[PROTOCOL-isolated.md](PROTOCOL-isolated.md). This commit still
precedes those transfer runs. Do not look at test LRs until the frozen
commands have been run once. Primary isolated endpoint is nested Youden
on the test files (threshold from train LOO only).

## 2026-09-01 isolated-file transfer 100→12 and 100→36

Protocol SHA `eb00f92`. Frozen lock A/B `probe --test-dir` once. Official
keys unused.

- **12×4 lock A** interpolate: prompt **8/12**, AUC **0.663**, nested
  Youden **23/48 vs 38/48**. Isolated recall does not beat **25/48**.
- **12×4 lock B** opening poshits: prompt **11/12**, AUC **0.844**, nested
  Youden **36/48 vs 42/48**, occupancy 9/48 vs 33/48 zeros.
- **36×4 lock A**: prompt **36/36**, AUC **0.858**, nested Youden
  **109/144 vs 122/144**.
- **36×4 lock B**: prompt **35/36**, AUC **0.955**, nested Youden
  **134/144 vs 129/144**, occupancy 7/144 vs 75/144 zeros.

H-iso-A holds only as 8/12 > 6/12. H-iso-B holds on the original 12
(11≥8). Do not sell 36/48 or 109/144 as replacing **25/48**. Lock C
waits on Qwen RAM. JSON:
`experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4/`,
`experiments/2026-09-01-transfer-100x4-to-12x4-opening-poshits/`,
`experiments/2026-09-01-transfer-100x4-to-36x4-hard-last4/`,
`experiments/2026-09-01-transfer-100x4-to-36x4-opening-poshits/`.

## 2026-09-01 lock B occupancy-free readout of the frozen 100-family tables

Same poshits tables as PROTOCOL-isolated lock B. No new `probe
--methods`. Observed-token scorer is postokhits on those tables.

- Original 12×4: postokhits t=0 **16/48 vs 48/48**. **21** poshits TPs
  were unseen next (`The`→` ferry` / ` bus` / ` dog` / ` printer`).
  Nested poshits **36/48** is not 36 observed tokens.
- 36×4: postokhits t=0 **114/144 vs 139/144**. Occupancy marked TP
  **20**. Shared `"This is the"` openings are register overlap.

Do not sell 16/48 or 114/144 as replacing **25/48**. JSON:
`experiments/2026-09-01-transfer-100x4-to-12x4-opening-poshits/occupancy-free.json`,
`experiments/2026-09-01-transfer-100x4-to-36x4-opening-poshits/occupancy-free.json`.

Lock A 12×4 prompt losses are harbour, night-bus, library, ferry-queue
(not the 12-LOO trio station/office/ferry-queue). Lock B loses letter
only. JSON:
`experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4/stems.json`.

## 2026-09-01 opening-overlap bound on the 100-family tables

`openings` `--methods postokhits --skip-stem-curve`. Isolated
observed-token recall equals train opening coverage.

- Original 12×4: covered **18/48**, exact 4-token **14/48**, decided
  16 TP / 0 FP. Occupancy-free t=0 **16/48 vs 48/48**.
- 36×4: covered **117/144**, exact 4-token **103/144**, decided 114 TP
  / 5 FP. Occupancy-free t=0 **114/144 vs 139/144**.

Zeros on the original 12 are `The ferry` / `Closing` / `The dog` /
`The printer` openings the 100 one-liners do not produce. Do not sell
18/48 or 117/144 as replacing **25/48**. JSON:
`experiments/2026-09-01-openings-100x4-to-12x4/`,
`experiments/2026-09-01-openings-100x4-to-36x4/`.

## 2026-09-01 indicate score occupancy-only ABSTAIN

`indicate score` auto on the frozen lock B poshits tables called
`01-harbour-marked.txt` **marked** (`lr≈0.149`, `n_used=1`) via Laplace
on unseen `The`→` ferry`. That is occupancy, not an observed token.
Isolated `indicate score` now prints `n_observed` and
`occupancy_only=true`, and **ABSTAINs** when `n_observed=0`. Probe
`--methods poshits` is unchanged. `--score-mode postokhits` still has
`n_used=0`. This does not replace **25/48**.

## 2026-09-01 Phase B Qwen opening locks

Native `Qwen/Qwen2-1.5B-Instruct`, same 100 prompts, seed `20260901`.
Local Hugging Face, not Dashscope. Official first-draw marked > unmarked
is **100/100** (mixin on; min marked ≈ 0.518). Mixin on/off remains
ground truth.

- **Lock B** opening poshits: **95/100**, AUC **0.873**, isolated
  **333/400 vs 308/400**
- **Lock C** opening rankpath: **84/100**, AUC **0.706**, isolated
  **275/400 vs 259/400**

H3 on Qwen: rankpath drop from GPT-2 Phase A is **12** (96→84); poshits
drop is **5** (100→95). Rankpath drops more. `--rankpath` extras are
not lock C. Do not sell Qwen 95/100 or 84/100 as replacing **25/48**.

JSON: `experiments/2026-09-01-pair-qwen-100x4/`,
`experiments/2026-09-01-probe-qwen-100x4-opening-poshits/`,
`experiments/2026-09-01-probe-qwen-100x4-opening-rankpath/`.

## 2026-09-01 isolated lock C transfer 100→12 and 100→36

Qwen pair gone. Frozen `--methods rankpath --fit-prefix 4 --pos-bucket 1`.
`used_keys=false`. Overlap dropped 0.

- Original 12×4: prompt **10/12**, nested Youden **24/48 vs 41/48**,
  t=0 **24/48 vs 40/48**, AUC **0.770**. Does not beat **25/48**.
- 36×4: prompt **35/36**, nested Youden **109/144 vs 117/144**, t=0
  **115/144 vs 112/144**, AUC **0.838**.

H-iso-C: rankpath is more domain-specific than lock B (**11/12** /
**36/48** occupancy on the original 12). JSON:
`experiments/2026-09-01-transfer-100x4-to-12x4-opening-rankpath/`,
`experiments/2026-09-01-transfer-100x4-to-36x4-opening-rankpath/`.

## 2026-09-01 isolated lock C stem losses on the original 12

Readout of the frozen 100→12 rankpath holdout. No new `probe --methods`.

Lock C prompt losses: **letter**, **garden**. Not lock A
harbour/night-bus/library/ferry-queue. Not 12-LOO hard
station/office/ferry-queue. Garden is also the 12-LOO opening-rankpath
miss. Letter is lock B's only miss.

Three ranking wins have **0/4** marked `lr>0`: night-bus, library,
market. Those stems rank because unmarked LRs are more negative.
Harbour and ferry-queue, which lock A missed, are 4/4 isolated TPs
under rankpath (`The ferry` openings). Do not sell union A/B/C t=0
**42/48** or nested **40/48**. On 36×4 the only prompt loss is library
(same Closing opening, different draws, still 0/4 marked t=0).

## 2026-09-01 ranking-without-isolated-TP is a first-class holdout field

Prompt-group ranking can hide stems whose marked files are all `lr<=0`.
Lock C 10/12 includes night-bus, library, and market that way.
`IndicatorHoldout.ranking_without_isolated_tp` now reports those stems.
`probe` / `transfer` / `indicate holdout` print the count. Not a new
scorer. Does not replace **25/48**.

## 2026-09-01 ranking vs isolated-file honesty on frozen holdouts

Same derived fields, applied to already-saved holdouts. No new scorer.

12-LOO hard last-4 (**9/12**, **25/48**): garden ranks with 0/4 marked
`lr>0`. Station, office, and ferry-queue lose ranking but hold **5** of
the **25** isolated TPs (ferry-queue 3/4). Lock C 100→12: three ranking
wins with 0 isolated TPs, zero TPs on ranking losses. Lock A 100→12: no
hidden ranking wins; 4 isolated TPs on ranking losses.

Do not rewrite **9/12** or **25/48**. JSON:
`experiments/2026-09-01-ranking-isolated-honesty/`.

## 2026-09-01 blind leave-one-prompt-out reports ranking vs isolated

The 9/12 producer (`blind`) stored only stem-mean LRs, so it could not
name garden as a ranking win with 0 isolated TPs. `leave_one_prompt_out`
now keeps per-file LRs. Stem-mean ranking is unchanged. New persists
print `ranking_without_isolated_tp` and `ranking_losses_with_isolated_tp`.
Historical `experiments/2026-09-01-blind-12x4-recount-last4/` stays
stem-mean only. Isolated sign stays hard `lr>0` even when `--margin` is
nonzero. Live 12×4 last-4 remeasure wrote
`experiments/2026-09-01-blind-12x4-ranking-honesty/`: **9/12**, garden
**0/4**, isolated **25**, ranking losses station/office/ferry-queue
with **5** TPs. Historical recount JSON unchanged. Not a new scorer.
Does not replace **25/48**.

## 2026-09-01 Grok-register isolated protocol frozen

[PROTOCOL-isolated-register.md](PROTOCOL-isolated-register.md) and
`experiments/2026-09-01-prompts-grok12/` committed at SHA `07ce009`.
Twelve new multi-paragraph scene prompts, disjoint from the original 12
and from the 100 one-liners. Same three locks as PROTOCOL-isolated.
Seed `20260904`. Do **not** run `pair` until this line is on origin.
Do not look at key-free LRs until the frozen analysis commands have
been run once. Nested Youden on the original 12×4 is the primary
endpoint. It still does not replace **25/48**.

## 2026-09-01 Grok-register isolated transfer opened

SHA `07ce009` protocol, pair SHA `28cf9f5`. Official first-draw **12/12**.
`used_keys=false`.

Lock A nested Youden **16/48 vs 41/48** (prompt **5/12**, t=0 **23/48**).
That is below one-liner lock A **23/48** and does not beat **25/48**.
H-reg-A fails. Harbour and library now rank; night-bus and ferry-queue
still lose.

Lock B nested **6/48 vs 47/48**. Occupancy-free postokhits t=0 **5/48**,
opening coverage **5/48** (0 exact). H-reg-B holds.

Lock C prompt **10/12**, t=0 **22/48**. Nested **45/48 vs 22/48** at a
negative threshold: do not sell 45/48.

In-family interpolate **11/12**, nested-by-stem **24/48 vs 40/48**.
Cross-register → 36×4 nested **50/144 vs 115/144**. Isolated-file
detection is still not finished.

## 2026-09-01 100 one-liners → Grok-register isolated protocol frozen

[PROTOCOL-isolated-xreg.md](PROTOCOL-isolated-xreg.md) committed at SHA
`1ef7330`. Same three locks as PROTOCOL-isolated. Train is the existing
100×4 one-liners. Test is the existing grok12×4 twins. No new `pair`.
Do not look at key-free test LRs until this line is on origin and the
frozen analysis commands have been run once. Nested Youden on grok12×4
is the primary endpoint. It does not replace **25/48**. Do not write
`thesis/`.

## 2026-09-01 100 one-liners → Grok-register isolated transfer opened

SHA `1ef7330` protocol. `used_keys=false`. Official first-draw on the
Grok twins remains **12/12**.

Lock A nested Youden **22/48 vs 41/48** (prompt **11/12**, t=0 **27/48**).
H-xreg-A holds versus Grok-train → original 12 **16/48**. H-xreg-hard
holds: 22/48 is at or below in-family nested-by-stem **24/48**. The
original 12 are not uniquely cursed. Taxi-rank is the ranking loss with
isolated TPs.

Lock B nested **36/48 vs 44/48** is occupancy (37/48 unmarked zeros).
Occupancy-free postokhits t=0 **0/48**, opening coverage **5/48** (0
exact). All ten postokhits ranking wins have 0 isolated TPs. H-xreg-B
holds.

Lock C prompt **8/12**, nested **10/48 vs 41/48**, t=0 **10/48**.
H-xreg-iso holds: nothing here replaces **25/48**. Isolated-file
detection is still not finished.

## 2026-09-01 interpolate window readout frozen

[PROTOCOL-isolated-windows.md](PROTOCOL-isolated-windows.md) committed at
SHA `7d8759a`. Same lock A interpolate tables as PROTOCOL-isolated-xreg.
Windows `0:4,4:16,16:32,32:64,64:128` on grok12 and on the original 12.
No new scorer. Do not look at window LRs until this line is on origin.
Does not replace **25/48**. Do not write `thesis/`.

## 2026-09-01 interpolate window readout opened

SHA `7d8759a`. `used_keys=false`.

Grok-register files: window 0:4 ranks **7/12** (AUC 0.619, t=0
**23/48 vs 31/48**). Windows **32:64** and **64:128** rank **9/12**.
Window 4:16 anti-ranks **4/12**. Full-file **11/12** is not an opening
core on this split. Occupancy-free openings remain **0/48**.

Original 12: window 0:4 ranks **9/12**; 16:32 ranks **6/12**.
Front-loaded transfer holds on the original 12 and not on Grok-length
OOD files. Isolated t=0 is chance-like in every slice. H-win-iso holds.
Does not replace **25/48**. Isolated-file detection is still not
finished.

## 2026-09-01 interpolate atoms on Grok-register transfer

Same lock A tables as PROTOCOL-isolated-xreg / windows. CLI `atoms`
(not a new `probe --methods` name). `used_keys=false`. Marked `lr>0`
**27/48**. Almost all interpolate mass is Witten–Bell backoff on
unseen next tokens (tail 64:128: 214 seen, 5924 unseen). Window 0:4
ranks because unmarked Δ is more negative, not because occupancy-free
openings fire (**0/48**). Observed-token hits: `'The' → ' car'` (n=19)
and GPT-2 dialogue templates in the tail. Shared continuation 4-grams,
not a denser isolated-file detector. Do not sell `The car`. Does not
replace **25/48**. Isolated-file detection is still not finished.

JSON: `experiments/2026-09-01-atoms-100x4-to-grok12x4-interpolate/`.

## 2026-09-01 36 Grok-length train protocol frozen

[PROTOCOL-isolated-scale.md](PROTOCOL-isolated-scale.md) and
`experiments/2026-09-01-prompts-grok36/` committed at SHA `e537d71`.
Thirty-six new Grok-register scenes, disjoint from grok12. Seed
`20260905`. Do not run `pair` until this line is on origin. Do not mix
grok12 into the train. Does not replace **25/48**. Do not write
`thesis/`.

## 2026-09-01 36 Grok-length scale protocol opened

SHA `e537d71`. Pair `69ef41f`. Official first-draw **36/36**.
`used_keys=false`.

Lock A nested Youden, grok12×4 test: **36/48 vs 39/48** (prompt
**12/12**). Occupancy-free postokhits **39/48 vs 45/48**, equal to
opening coverage **39/48** (exact 21/48; 3 unmarked FP). H-scale-grok
holds vs 100-one-liner xreg **22/48**. Isolated observed-token recall
is still opening-atom overlap.

Lock A nested Youden, original 12×4: **26/48 vs 33/48** (prompt
**10/12**). Occupancy-free **10/48**, equal to coverage **10/48**.
H-scale-A holds vs grok12-train **16/48**. Do not sell 26/48 or t=0
**29/48**.

H-scale-iso holds. Nothing here replaces **25/48**. Isolated-file
detection is still not finished.

JSON: `experiments/2026-09-01-transfer-grok36x4-to-grok12x4-hard-last4/`,
`experiments/2026-09-01-openings-grok36x4-to-grok12x4/`,
`experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4/`.

## 2026-09-01 interpolate atoms on 36 Grok-length transfer

Same lock A tables as PROTOCOL-isolated-scale, after the frozen
probes. CLI `atoms` (not a new `probe --methods` name).
`used_keys=false`.

Original 12×4: marked `lr>0` **29/48**. Nested interpolate stays
**26/48 vs 33/48**. Occupancy-free stays **10/48**. Almost all mass is
Witten–Bell backoff (tail 64:128: 137 seen vs 5996 unseen). Window
0:4 ranks because unmarked Δ is more negative and because unbucketed
body copies fire (`'Cl' → 'osing'` n=4 on library; postokhits zeros
that opening). The 29-versus-10 gap is not isolated recall.

Grok12×4: marked `lr>0` **39/48**, equal to occupancy-free and
opening coverage. Window 0:4 marked Δ +2.518 (`'The' → ' car'` n=19).
Tail still backoff (183 seen vs 5955 unseen). Interpolate nested
**36/48** is not denser than occupancy-free **39/48**.

Do not sell 26/48, 29/48, 39/48, `Closing`, or `The car`. Does not
replace **25/48**. Isolated-file detection is still not finished.

JSON: `experiments/2026-09-01-atoms-grok36x4-to-12x4-interpolate/`,
`experiments/2026-09-01-atoms-grok36x4-to-grok12x4-interpolate/`.

## 2026-09-01 pooled-train isolated protocol frozen

[PROTOCOL-isolated-pool.md](PROTOCOL-isolated-pool.md) and the
published-zero union dump
`experiments/2026-09-01-openings-union-100-and-grok36-to-12x4/` committed
at SHA `244d23a`. Set-union of occupancy-free openings on the original
12 is **28/48** (18+10, intersection 0, leftover 20). That number is
determined from already-opened zeros. Do not look at mixed `probe` /
mixed `openings` LRs until this line is on origin. Do not sell
**28/48** as replacing **25/48**. Do not write `thesis/`.

## 2026-09-01 pooled-train isolated transfer opened

SHA `244d23a`. `used_keys=false`. Mixed openings coverage **28/48**
equals the published set-union (no combo atoms). Occupancy-free
postokhits t=0 is **26/48 vs 47/48** (two covered letter files are
negative). Nested interpolate **27/48 vs 39/48**. H-pool-B holds for
coverage; H-pool-A holds vs grok36-only 26/48. Do not sell 28/48, 26/48,
or 27/48. Leftover 20 files remain. Nothing replaces **25/48**.
Isolated-file detection is still not finished.

JSON: `experiments/2026-09-01-openings-100plusgrok36-to-12x4/`,
`experiments/2026-09-01-transfer-100plusgrok36-to-12x4-occupancy-free/`,
`experiments/2026-09-01-transfer-100plusgrok36-to-12x4-hard-last4/`.

## 2026-09-01 leftover-opening rankpath protocol frozen

[PROTOCOL-isolated-leftover.md](PROTOCOL-isolated-leftover.md) committed
at SHA `7afd049`. The 20 mixed postokhits zeros are the isolated-file
core. Do not look at mixed rankpath LRs until this line is on origin.
Do not sell leftover signs as replacing **25/48**. Do not write
`thesis/`.

## 2026-09-01 leftover-opening rankpath opened

SHA `7afd049`. `used_keys=false`. Leftover 20 mixed rankpath marked
`lr>0` **12/20**, unmarked `lr≤0` **14/20**. Library leftover **0/4**.
H-left-C holds. Full nested **35/48 vs 38/48** fails H-left-full as a
raw count; do not sell 35/48 (it includes covered openings). Nothing
replaces **25/48**. Isolated-file detection is still not finished.

JSON: `experiments/2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath/`.

## 2026-09-01 leftover-versus-covered 25/48 split frozen

[PROTOCOL-isolated-split.md](PROTOCOL-isolated-split.md) committed at
SHA `f09d0e2`. Leftover membership stays the mixed postokhits zeros
(20 files). Primary holdout stays 12-LOO hard last-4 (**25/48**). Do
not look at leftover-versus-covered TP counts until this line is on
origin. Do not sell either slice as replacing **25/48**. Do not write
`thesis/`.

## 2026-09-01 leftover-versus-covered 25/48 split opened

SHA `f09d0e2`. `used_keys=false`. Headline 12-LOO hard last-4 **25/48**
splits leftover marked `lr>0` **10/20**, unmarked `lr≤0` **11/20**, and
occupancy-covered **15/28 vs 11/28**. H-split-left, H-split-cov, and
H-split-iso hold. Leftover last-4 is chance. Ranking-loss TPs are all
leftover. Letter leftover and garden leftover are 0 TPs. Do not sell
10/20 or 15/28. Nothing replaces **25/48**. Isolated-file detection is
still not finished.

JSON: `experiments/2026-09-01-isolated-split-25-leftover-vs-covered/`.

## 2026-09-01 two-grain narrative and mask-k protocol frozen

[narrative.md](narrative.md) and
[PROTOCOL-isolated-mask.md](PROTOCOL-isolated-mask.md) committed at
SHA `004397c`. Prompt-group ranking stays real; isolated **25/48** stays
chance-like. Do not write a “key-free detection fails” paper. Do not
look at 12-LOO `--windows` LRs until this line is on origin. Do not
write `thesis/`.

## 2026-09-01 headline 12-LOO mask-k windows opened

SHA `004397c`. `used_keys=false`. Hard prefix 0:4 is **5/12**; tails
4:128 and 8:128 stay **9/12**. Interpolate tails drop to **5/12** then
**3/12**. Isolated t=0 stays chance-like. H-mask-open and H-mask-tail
fail for hard. H-mask-iso holds. The headline hard 9/12 is not an
opening-only n-gram artifact. Do not sell prefix 10/12, isolated 29/48,
or tail 9/12. Nothing replaces **25/48**. Isolated-file detection is
still not finished.

JSON: `experiments/2026-09-01-probe-12x4-headline-windows/`.

## 2026-09-01 leftover-versus-covered mask-k window split frozen

[PROTOCOL-isolated-mask-split.md](PROTOCOL-isolated-mask-split.md)
committed at SHA `3e30e70`. Leftover membership stays mixed postokhits
zeros. Primary holdout stays hard 4:128. Do not look at leftover
versus covered window counts until this line is on origin. Do not sell
tail **9/12**. Do not write `thesis/`.

## 2026-09-01 leftover-versus-covered mask-k window split opened

SHA `3e30e70`. `used_keys=false`. Hard 4:128 leftover marked `lr>0`
**11/20**, unmarked `lr≤0` **11/20**, occupancy-covered **16/28 vs
11/28**. H-wsplit-tail, H-wsplit-open, and H-wsplit-iso hold. Leftover
tail is chance. Tail **9/12** is not leftover-file recall. Prefix 0:4
isolated **29/48** is **12 leftover + 17 covered**. Do not sell 11/20,
16/28, window 29/48, or tail 9/12. Nothing replaces **25/48**.
Isolated-file detection is still not finished.

JSON: `experiments/2026-09-01-isolated-split-windows-leftover-vs-covered/`.

## 2026-09-01 occupancy leftover-20 bound frozen

[PROTOCOL-isolated-leftover-bound.md](PROTOCOL-isolated-leftover-bound.md)
committed at SHA `802186e`. Leftover membership stays mixed postokhits
zeros. Official prefixes stay the published keyed dump. Interpolate
tables stay grok36 lock A. Do not look at leftover-20 official means
or leftover-only atom windows until this line is on origin. Do not
write `thesis/`.

## 2026-09-01 occupancy leftover-20 bound opened

SHA `802186e`. Official `used_keys=true`. Leftover-20 full-file mean
**0.624**, **20/20** above 0.55 (covered **0.620**, 28/28). Prefix-5
**18/20** (office-1 and office-3 at 0.500 on one 5-gram; both marked by
prefix-16). Leftover interpolate atoms 0:4 seen 21 vs unseen **99**;
seen mass is `'Cl'→'osing'`; leftover marked `lr>0` **13/20**.
H-bound-lamp, H-bound-open, H-bound-atom, and H-bound-iso hold.
Leftover key-free chance is not an unmarked mixin miss. Do not sell
official 20/20, interpolate 13/20, or Closing. Nothing replaces
**25/48**. Isolated-file detection is still not finished.

JSON: `experiments/2026-09-01-isolated-leftover-bound/`.

## 2026-09-01 leftover-20 ∪ short-medium-tails openings frozen

[PROTOCOL-isolated-leftover-union.md](PROTOCOL-isolated-leftover-union.md)
committed at SHA `e5a5f6b`. Leftover membership stays mixed postokhits
zeros. Short+medium+tails zeros stay that dump. Do not look at
leftover-after-union counts until this line is on origin. Do not write
`thesis/`.

## 2026-09-01 leftover-20 ∪ short-medium-tails openings opened

SHA `e5a5f6b`. `used_keys=false`. Union **30/48** equals published SMT
coverage; mixed 100+grok36 is a subset. SMT-only covers are garden 1/4.
Leftover after union is **18**. 12-LOO hard last-4 leftover is
**10/18 vs 10/18**. Mixed occupancy-free leftover sign is **0/18 vs
18/18** by construction. H-union-smt, H-union-left, and H-union-iso
hold. Do not sell union 30/48 or leftover 10/18. Nothing replaces
**25/48**. Isolated-file detection is still not finished.

JSON: `experiments/2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4/`.

## 2026-09-01 occupancy-free leftover-18 closed

[PROTOCOL-isolated-occupancy-closed.md](PROTOCOL-isolated-occupancy-closed.md)
committed at SHA `afb7668`. Occupancy-free remainder after SMT ∪ mixed
is leftover **18**. Leftover-18 official prefix-128 is **18/18** by
subset of leftover-20 **20/20**. Prefix-5 is **16/18**. Do not add
family-12 paraphrases or target leftover openings after peeking. Do
not write `thesis/`.

## 2026-09-01 leftover-18 remaining readers frozen

[PROTOCOL-isolated-leftover-18.md](PROTOCOL-isolated-leftover-18.md)
committed at SHA `5621544`. Leftover membership stays leftover-union
leftover-18 keys. Mixed rankpath and grok36 interpolate stay those
dumps. Do not look at leftover-18 rankpath or leftover-18 interpolate
counts until this line is on origin. Do not write `thesis/`.

## 2026-09-01 leftover-18 remaining readers opened

SHA `5621544`. `used_keys=false`. Leftover-18 mixed rankpath **12/18 vs
13/18**. Grok36 interpolate **12/18 vs 12/18**. 12-LOO hard last-4 check
**10/18 vs 10/18**. Leftover-18 interpolate 0:4 seen 19 vs unseen **89**;
seen mass is `'Cl'→'osing'`. Garden leftover had 0 mixed rankpath TPs
and 1 interpolate TP. H-left18-C, H-left18-A, and H-left18-iso hold.
Do not sell leftover-18 rankpath 12/18 or leftover-18 interpolate 12/18.
Nothing replaces **25/48**. Isolated-file detection is still not
finished.

JSON: `experiments/2026-09-01-isolated-leftover-18-readers/`.

## 2026-09-01 leftover-18 published key-free readers closed

[PROTOCOL-isolated-leftover-18-closed.md](PROTOCOL-isolated-leftover-18-closed.md)
committed at SHA `cdccae5`. Leftover-18 published key-free readers
(occupancy-free, mixed rankpath, grok36 interpolate, 12-LOO hard last-4)
are exhausted for leftover-file detection. Mixed rankpath leftover-18
is **12/18 vs 13/18**. Interpolate leftover-18 is **12/18 vs 12/18**.
Last-4 leftover-18 is **10/18 vs 10/18**. Do not re-slice more leftover-18
holdouts, including leftover-18 mask-*k*. Do not write `thesis/`.

## 2026-09-01 Distil occupancy-free leftover-18 frozen

[PROTOCOL-isolated-xgen.md](PROTOCOL-isolated-xgen.md)
committed at SHA `8e33445`. Distil 100×4 tables score the original 12
GPT-2 files. Leftover membership stays leftover-union leftover-18 keys.
Do not look at Distil occupancy-free leftover-18 coverage until this
line is on origin. Do not write `thesis/`.

## 2026-09-01 Distil occupancy-free leftover-18 opened

SHA `8e33445`. `used_keys=false`. Distil occupancy-free postokhits t=0
on the original 12 is **22/48 vs 43/48**. That beats GPT-2 lock B
occupancy-free **16/48 vs 48/48** and does not beat **25/48**. Openings
covered **23/48**. Leftover-18 Distil coverage is **3/18** (office 1/3/4);
leftover occupancy-free sign **3/18 vs 16/18**. Remaining leftover-15 is
harbour, library, station-4, letter 2–3, ferry-queue. H-xgen-cover holds.
H-xgen-B fails versus 16/48. H-xgen-iso holds. Do not sell Distil 22/48
or leftover Distil 3/18. Nothing replaces **25/48**. Isolated-file
detection is still not finished.

JSON: `experiments/2026-09-01-isolated-xgen-leftover-18/`,
`experiments/2026-09-01-transfer-distil100x4-to-12x4-opening-poshits/`,
`experiments/2026-09-01-openings-distil100x4-to-12x4/`.

## 2026-09-01 Distil occupancy-free Distil-12 transfer frozen

[PROTOCOL-isolated-dgen.md](PROTOCOL-isolated-dgen.md)
committed at SHA `6bb95a6`. Distil 100×4 tables score Distil 12×4 files.
Not leftover-18. Do not apply leftover-18 GPT-2 keys to Distil files.
Do not look at Distil→Distil occupancy-free LRs until this line is on
origin. Do not write `thesis/`.

## 2026-09-01 Distil occupancy-free Distil-12 transfer opened

SHA `6bb95a6`. `used_keys=false`. Distil occupancy-free postokhits t=0
on Distil 12×4 is **16/48 vs 39/48**. Openings covered **16/48** (exact
9/48). That equals opening-atom overlap and does not beat **25/48**.
Distil→GPT-2 occupancy-free **22/48** used different test files.
H-dgen-cover, H-dgen-B, and H-dgen-iso hold. Nested Youden **48/48** is
a negative train threshold; do not sell 48/48. Distil poshits **25/48 vs
25/48** includes occupancy. Do not sell Distil→Distil 16/48. Nothing
replaces **25/48**. Isolated-file detection is still not finished.

JSON: `experiments/2026-09-01-transfer-distil100x4-to-distil12x4-opening-poshits/`,
`experiments/2026-09-01-openings-distil100x4-to-distil12x4/`.

## 2026-09-01 Qwen occupancy-free Qwen-12 transfer frozen

[PROTOCOL-isolated-qgen.md](PROTOCOL-isolated-qgen.md)
committed at SHA `3c0a5c9`. Qwen 100×4 tables score Qwen 12×4 files.
Not leftover-18. Native tokenizer. No lock A. No `--include-first`.
Do not apply leftover-18 GPT-2 keys to Qwen files. Do not look at
Qwen→Qwen occupancy-free LRs until this line is on origin. Do not
write `thesis/`.

## 2026-09-01 Qwen occupancy-free Qwen-12 transfer opened

SHA `3c0a5c9`. `used_keys=false`. Local Hugging Face, not Dashscope.
Qwen occupancy-free postokhits t=0 on Qwen 12×4 is **31/48 vs 48/48**.
Openings covered **37/48** (exact 12/48). Six covered files have
negative LR. H-qgen-cover holds on not 48/48. H-qgen-B fails as a raw
count (**31/48** > **25/48**) across corpora. H-qgen-iso holds: these
are Qwen files, not original-12 GPT-2. Nested Youden **31/48 vs 48/48**
at a positive threshold. Do not sell Qwen→Qwen 31/48. Nothing replaces
**25/48**. Isolated-file detection is still not finished.

JSON: `experiments/2026-09-01-transfer-qwen100x4-to-qwen12x4-opening-poshits/`,
`experiments/2026-09-01-openings-qwen100x4-to-qwen12x4/`.

## 2026-09-01 Distil ∪ SMT openings union frozen

[PROTOCOL-isolated-dsmt.md](PROTOCOL-isolated-dsmt.md)
committed at SHA `b1f0c7d`. Distil 100×4 occupancy-free zeros and
short+medium+tails zeros on the original 12. No new tables. Do not look
at leftover-after-union counts until this line is on origin. Do not
write `thesis/`.

## 2026-09-01 Distil ∪ SMT openings union opened

SHA `b1f0c7d`. `used_keys=false`. Distil 100×4 covers **23/48**. SMT
covers **30/48**. Set-union is **33/48**. Leftover is **15/48**.
Distil-only covers are office 1/3/4. Leftover last-4 is **9/15 vs
8/15**. Distil occupancy-free leftover sign is **0/15** marked.
H-dsmt-cover, H-dsmt-left, and H-dsmt-iso hold. Do not sell union
33/48 or leftover 9/15. Nothing replaces **25/48**. Isolated-file
detection is still not finished. Do not target leftover-15 openings
after peeking.

JSON: `experiments/2026-09-01-openings-union-distil100x4-and-smt-to-12x4/`.

## 2026-09-01 leftover-15 occupancy-free closed

[PROTOCOL-isolated-leftover-15-closed.md](PROTOCOL-isolated-leftover-15-closed.md)
committed at SHA `570a5c6`. Leftover-15 official is **15/15** at
prefix-5 from the published keyed dump. Occupancy-free leftover-15
versus Distil is **0/15** by construction. Leftover last-4 is **9/15 vs
8/15**. Do not target leftover-15 openings. Nothing replaces **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.

## 2026-09-01 gpt2-medium occupancy-free leftover-15 freeze

[PROTOCOL-isolated-mgen.md](PROTOCOL-isolated-mgen.md) committed at SHA
`cc9c4ca`. Occupancy-free leftover-15 is closed for more unrelated GPT-2
scenes. The remaining analog is gpt2-medium 100×4 on the already-frozen
100 prompts (same BPE; not leftover targeting). Hypotheses H-mgen-cover,
H-mgen-B, and H-mgen-iso are stated before any gpt2-medium→12 LRs.
Do not look at those LRs until the pair, probe, and openings commands
have been run once, as written. Do not target leftover-15 openings.
Nothing replaces **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`.

## 2026-09-01 manuscript position and Distil strict recount

Locked [threat-model.md](threat-model.md): the auditor is **key-free,
not reference-free, not fully blind**. The notebook is a **strong
empirical** measurement, interesting to the field; it is **not
field-defining** and **not a finished conference paper**. The honest
next artifact is a workshop, artifact, or focused empirical report with
the two-grain sentence first. Do not write `thesis/` from that lock.

Strict prompt ranking is `marked_lr + margin > unmarked_lr`. Equality is
a **tie**, not a win. Distil lock B/C historical persist still prints
**89/100** and **69/100**. Recomputed from the same LRs: **88 wins + 1
tie** and **68 wins + 1 tie**. H3 still holds (drops 12 and 28 from
GPT-2 Phase A). Do not rewrite the Phase B LOGBOOK entry. Do not sell
88/100 or 68/100 as replacing **25/48**. PROTOCOL-next H2 remains a
**reindexed** window measurement until an absolute-history rerun.

File-level permutation and binomial p-values are descriptive. The
inferential unit is the prompt family.

JSON unchanged: `experiments/2026-09-01-probe-distil-100x4-opening-poshits/`,
`experiments/2026-09-01-probe-distil-100x4-opening-rankpath/`.

Occupancy-free postokhits notes that said “ranking wins with 0 isolated
TPs” mixed true ranking wins with 0=0 ties. Strict recount from the same
LRs: Grok-register → original 12 is **2 wins + 9 ties** (the 9 ties have
0 isolated TPs; the 2 wins do not). 100 one-liners → Grok-register is
**4 wins + 6 ties** (all four wins have 0 isolated TPs: marked occupancy
zero vs negative unmarked). Isolated t=0 is unchanged. Do not sell the
old `>=` prompt counts as ranking wins.

## 2026-09-01 gpt2-medium occupancy-free leftover-15 opened

[PROTOCOL-isolated-mgen.md](PROTOCOL-isolated-mgen.md) named `883532b`.
Official first-draw lamp on gpt2-medium 100×4 is **100/100**. Occupancy-free
postokhits t=0 on the original 12 is **16/48 vs 48/48** (equals opening
coverage **16/48**, exact **14/48**, decided FP 0). Leftover-15 coverage
is **0/15**. Leftover occupancy-free sign is **0/15 vs 15/15**. H-mgen-cover,
H-mgen-B, and H-mgen-iso hold. Prompt ranking postokhits is **7/12** strict
with **5 ties**. Do not sell **16/48**, **0/15**, **7/12**, or official
**100/100** as replacing **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`.

JSON: `experiments/2026-09-01-pair-gpt2-medium-100x4/`,
`experiments/2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits/`,
`experiments/2026-09-01-openings-gpt2-medium-100x4-to-12x4/`,
`experiments/2026-09-01-isolated-mgen-leftover-15/`.

## 2026-09-01 gpt2-medium 12×4 occupancy-free freeze

[PROTOCOL-isolated-m12.md](PROTOCOL-isolated-m12.md) committed at SHA
`5be70f3`. Occupancy-free leftover-15 versus gpt2-medium is **0/15**.
The remaining analog is gpt2-medium 100×4 tables scoring gpt2-medium
12×4 files from the original 12 Grok seeds (same BPE; not leftover
targeting). Hypotheses H-m12-cover, H-m12-B, and H-m12-iso are stated
before any gpt2-medium→gpt2-medium LRs. Do not look at those LRs until
the pair, probe, and openings commands have been run once, as written.
Do not apply leftover-15 keys to gpt2-medium 12 files. Do not target
leftover-15 openings. Nothing replaces **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

## 2026-09-01 gpt2-medium occupancy-free medium-12 transfer opened

[PROTOCOL-isolated-m12.md](PROTOCOL-isolated-m12.md) named `3610cef`.
Official first-draw lamp on gpt2-medium 12×4 is **12/12**. Occupancy-free
postokhits t=0 on those files is **10/48 vs 48/48** (coverage **13/48**,
exact **10/48**, three covered files have negative LR, decided FP 0).
H-m12-cover, H-m12-B, and H-m12-iso hold. Prompt ranking postokhits is
**8/12** strict with **3 ties**. Do not sell **10/48**, **13/48**,
**8/12**, or official **12/12** as replacing **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-01-pair-gpt2-medium-12x4/`,
`experiments/2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits/`,
`experiments/2026-09-01-openings-gpt2-medium-100x4-to-medium12x4/`.

## 2026-09-01 Distil↔gpt2-medium occupancy-free freeze

[PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md) committed at SHA
`3bb8430`. gpt2-medium→gpt2-medium occupancy-free is already **10/48**.
The remaining analog is Distil 100×4 tables scoring gpt2-medium 12×4
files and gpt2-medium 100×4 tables scoring Distil 12×4 files (same BPE;
already-frozen twins; not leftover targeting). Hypotheses H-xsize-cover,
H-xsize-B, and H-xsize-iso are stated before any Distil↔gpt2-medium LRs.
Do not look at those LRs until the probe and openings commands have been
run once, as written. Do not apply leftover-15 or leftover-18 keys to
Distil 12 or gpt2-medium 12 files. Do not target leftover-15 openings.
Do not freeze Distil ∪ gpt2-medium union in this file. Nothing replaces
**25/48**. Isolated-file detection is still not finished. Do not write
`thesis/`.

## 2026-09-01 Distil occupancy-free gpt2-medium transfer opened

[PROTOCOL-isolated-xsize.md](PROTOCOL-isolated-xsize.md) named `fbf2cb5`.
Occupancy-free Distil→gpt2-medium postokhits t=0 is **20/48 vs 48/48**
(coverage **22/48**, exact **4/48**, two covered files have negative LR,
decided FP 0). Occupancy-free gpt2-medium→Distil postokhits t=0 is
**3/48 vs 47/48** (coverage **5/48**, exact **2/48**, decided FP 1).
H-xsize-cover, H-xsize-B, and H-xsize-iso hold. Nested Youden Distil→gpt2-medium
**46/48 vs 11/48** is a negative train threshold; do not sell 46/48.
Prompt ranking Distil→gpt2-medium postokhits is **11/12** strict with
**1 tie**. Prompt ranking gpt2-medium→Distil postokhits is **6/12**
strict with **6 ties**. Do not sell **20/48**, **22/48**, **11/12**,
**3/48**, **5/48**, or **6/12** as replacing **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-01-transfer-distil100x4-to-medium12x4-opening-poshits/`,
`experiments/2026-09-01-openings-distil100x4-to-medium12x4/`,
`experiments/2026-09-01-transfer-gpt2-medium-100x4-to-distil12x4-opening-poshits/`,
`experiments/2026-09-01-openings-gpt2-medium-100x4-to-distil12x4/`.

## 2026-09-01 absolute-history H2 remasure freeze

[PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md) committed at SHA
`89cb62d`. PROTOCOL-next H2 is still a reindexed window measurement
(0:4 **99/100** vs 16:32 **89/100**). Occupancy-free leftover-15 and
Distil↔gpt2-medium occupancy-free are already opened. The remaining
confirmatory honesty remasure is absolute `score_span` on the same
100×4 interpolate windows, without overwriting the reindexed dump.
Hypotheses H2-abs, H2-abs-acc, and H2-abs-iso are stated before any
absolute-history window LRs. Do not look at those LRs until the probe
command has been run once, as written. Do not add a scorer. Do not
overwrite `experiments/2026-09-01-probe-100x4-hard-windows/`. Nothing
replaces **25/48**. Isolated-file detection is still not finished. Do
not write `thesis/`.

## 2026-09-01 absolute-history H2 remasure opened

[PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md) named `450658c`.
Absolute-history lock A interpolate window **0:4** ranks **99/100**
(AUC **0.885**, isolated 372/400 vs 272/400). Window **16:32** ranks
**87/100** (AUC **0.695**, isolated 267/400 vs 240/400). H2-abs, H2-abs-acc,
and H2-abs-iso hold. Absolute 0:4 equals the reindexed opening. Absolute
16:32 did **not** rise versus reindexed **89/100**. `used_keys=false`.
Do not overwrite the reindexed dump. Do not sell **99/100**, **87/100**,
isolated **372/400**, or isolated **267/400** as replacing **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-01-probe-100x4-hard-windows-absolute/`.
Reindexed (keep): `experiments/2026-09-01-probe-100x4-hard-windows/`.

## 2026-09-02 paired prompt-family H2 readout

Post-open clustered description of the already-opened absolute H2
holdouts. Not a second freeze. Not a new scorer. Prompt family is the
unit. 0:4 versus 16:32 is **86 / 13 / 1 / 0**. Exact one-sided McNemar
P(X ≥ 13 | Bin(14, ½)) ≈ **0.00092**. Clopper–Pearson 95% on isolated
**25/48** is **[0.372, 0.667]** and includes ½; on **9/12** includes ½;
on absolute **87/100** is **[0.788, 0.929]** and excludes ½. Unpaired
interval overlap is not the H2 test. Do not sell McNemar **0.00092**,
**93/100** gap signs, **99/100**, or **87/100** as replacing **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.

## 2026-09-02 second-key in-domain lock A freeze

[PROTOCOL-isolated-xkey.md](PROTOCOL-isolated-xkey.md) committed at SHA
`d25e495`. Occupancy-free leftover-15, Distil↔gpt2-medium occupancy-free,
and absolute-history H2 are already opened. The remaining honesty item
that is not leftover targeting is whether lock A interpolate last-4 still
ranks held-out prompt groups when the marked side is control-shuffled-30
against the original unmarked pile. Seeds **20260931** vs **0**. Not a
matched `pair()` run. Complementary to instance contrast. Hypotheses
H-xkey-A, H-xkey-iso, and H-xkey-seed are stated before any
control-as-marked interpolate LRs. Do not look at those LRs until the
probe command has been run once, as written. Do not add a scorer.
`--fit-prefix` now rewrites UTF-8 strings from clipped ids. Nothing
replaces **25/48**. Isolated-file detection is still not finished. Do
not write `thesis/`.

## 2026-09-02 second-key in-domain lock A opened

[PROTOCOL-isolated-xkey.md](PROTOCOL-isolated-xkey.md) named `9ec3b0c`.
Leave-one-prompt-out interpolate last-4 on control-as-marked 12×4 ranks
**7/12** (AUC **0.590**, isolated **30/48 vs 25/48**). H-xkey-A and
H-xkey-seed hold. H-xkey-iso **fails** as a raw count (**30/48** >
**25/48**). These are control-shuffled-30 files, not the original public
marked 12. Clopper–Pearson 95% on **7/12** is **[0.277, 0.848]** and
includes ½; on **30/48** is **[0.474, 0.760]** and includes ½.
`used_keys=false`. Seeds **20260931** vs **0**. Not a matched `pair()`
run. Nested Youden **33/48 vs 20/48** is a negative threshold; do not
sell 33/48. Do not sell **7/12** or **30/48** as replacing **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-02-probe-12x4-control-as-marked-hard-last4/`.

---

## 2026-09-02 absolute-history OOD windows freeze

[PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md)
committed at SHA `1504cb4`. Second-key lock A, occupancy-free leftover-15,
Distil↔gpt2-medium occupancy-free, and in-family absolute H2 are already
opened. The remaining honesty item that is not leftover targeting is
whether 100→grok12 interpolate windows still put tail **9/12** above
opening **7/12** when mid-file 4-grams keep their real prefix. Reindexed
dumps stay. Hypotheses H-win-abs-open, H-win-abs-mid, H-win-abs-12, and
H-win-abs-iso are stated before any absolute transfer window LRs. Do
not look at those LRs until the two probe commands have been run once,
as written. Do not add a scorer. Do not overwrite the reindexed dumps.
Nothing replaces **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`.

## 2026-09-02 absolute-history OOD windows remasure opened

[PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md)
named `b32ea50`. Same flags as PROTOCOL-isolated-windows. New out-dirs.
`used_keys=false`. Grok12 absolute 0:4 is **7/12** (equals reindexed);
32:64 **10/12** (rose versus reindexed **9/12**); 64:128 **9/12**.
Original 12 absolute 0:4 is **9/12** (equals reindexed) and outranks
16:32 **6/12**; 64:128 fell 8→6. H-win-abs-open, H-win-abs-mid,
H-win-abs-12, and H-win-abs-iso hold. Clopper–Pearson 95% on grok
32:64 **10/12** is **[0.516, 0.979]** and excludes ½; n=12 is still
small. Isolated t=0 stays chance-like. Do not sell absolute **10/12**,
**7/12**, orig window **25/48**, or reindexed tail **9/12** as
replacing **25/48**. Do not overwrite the reindexed dumps. Isolated-file
detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-02-transfer-100x4-to-grok12x4-hard-windows-absolute/`,
`experiments/2026-09-02-transfer-100x4-to-12x4-hard-windows-absolute/`.
Reindexed (keep): `experiments/2026-09-01-transfer-100x4-to-grok12x4-hard-windows/`,
`experiments/2026-09-01-transfer-100x4-to-12x4-hard-windows/`.

---

## 2026-09-03 absolute-history 12-LOO mask-*k* freeze

[PROTOCOL-isolated-mask-absolute.md](PROTOCOL-isolated-mask-absolute.md)
committed at SHA `b70986d`. Absolute-history OOD windows are already
opened. The remaining honesty item that is not leftover targeting is
whether 12-LOO hard last-4 still keeps tail ranking **9/12** and prefix
**0:4** **5/12** when mid-file 4-grams keep their real prefix.
Reindexed dumps stay. Hypotheses H-mask-abs-open, H-mask-abs-tail,
H-mask-abs-2, and H-mask-abs-iso are stated before any absolute mask
LRs. Do not look at those LRs until the probe command has been run
once, as written. Do not add a scorer. Do not overwrite the reindexed
dump. Nothing replaces **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`.

## 2026-09-03 absolute-history 12-LOO mask-*k* remasure opened

[PROTOCOL-isolated-mask-absolute.md](PROTOCOL-isolated-mask-absolute.md)
named `7ec4509`. Same flags as PROTOCOL-isolated-mask. New out-dir.
`used_keys=false`. Absolute prefixes equal reindexed: hard 0:4 is
**5/12**; 0:2 **10/12**; 0:8 **6/12**. Hard tails **4:128** and
**8:128** stay **9/12** (neither rose nor fell). Interpolate 8:128
**rose** 3→4. H-mask-abs-open, H-mask-abs-tail, H-mask-abs-2, and
H-mask-abs-iso hold. Isolated t=0 stays chance-like. Do not sell
absolute tail **9/12**, prefix **10/12**, interpolate **4/12**, or
isolated 29/48 as replacing **25/48**. Do not overwrite the reindexed
dump. Isolated-file detection is still not finished. Do not write
`thesis/`.

JSON: `experiments/2026-09-03-probe-12x4-headline-windows-absolute/`.
Reindexed (keep): `experiments/2026-09-01-probe-12x4-headline-windows/`.

## 2026-09-03 longer-context two-grain freeze

[PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md) committed at SHA
`b70986d`. Sol's 260903 next experiment: public keys, `ngram_len=13`
($\Hw=12$), original 12 Grok prompt strings, GPT-2, 4 draws, $T=128$,
seed **20260903**, leave-one-family-out hard+interpolate last-4.
Hypotheses H-long-ctrl, H-long-group, H-long-hard, H-long-iso, and
H-long-occ are stated before generation. Do not look at key-free LRs
until `pair` has written official first-draw scores and the probe
command has been run once, as written. Do not add a scorer. A finished
100×4 corpus is not required for this freeze. Nothing replaces
**25/48**. Isolated-file detection is still not finished. Do not write
`thesis/`.

---

## 2026-09-03 longer-context two-grain Phase A opened

[PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md) named `7ec4509`.
Pair seed **20260903**, `ngram_len=13`, original 12 Grok strings.
Official first-draw matching `ngram_len=13` is above 0.55 on **12/12**
first marked files (H-long-ctrl holds). Post-open extra-draw check:
**48/48** marked above 0.55 (min $0.599$), **0/48** unmarked above 0.55. Key-free 12-LOO interpolate
last-4 is **6/12** (AUC **0.541**, isolated **20/48 vs 31/48**). Hard
is **6/12** (AUC **0.544**, isolated **22/48 vs 30/48**, balanced
accuracy **52/96**). `used_keys=false`. Below the public-mixin
diagnostic **9/12**. Clopper–Pearson on **6/12** is **[0.211, 0.789]**
and includes ½. H-long-group, H-long-hard, and H-long-iso hold.
H-long-occ is not opened (`tables-counts` dropped). Do not sell
**6/12**, **22/48**, or **52/96** as replacing **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`. Phase B is
not opened.

JSON: `experiments/2026-09-03-pair-12x4-ngram13/`,
`experiments/2026-09-03-probe-12x4-ngram13-hard-last4/`.

## 2026-09-03 longer-context Phase B start

[PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md) Phase B, named
before generation. Same freeze SHA `b70986d`. Public keys,
`ngram_len=13`, GPT-2, prompts
`experiments/2026-09-01-prompts-100/`, `--n-samples 4`, $T=128$,
seed **20260903**. Same readers: hard and interpolate last-4
leave-one-family-out. Same two grains. No new `probe --methods` name.

Stated before these 100×4 LRs:

- **H-long-B-ctrl.** Official first-draw matching `ngram_len=13` is
  above $0.55$ on every first marked file.
- **H-long-B-group.** Interpolate last-4 prompt ranking is below
  public-mixin lock A **99/100**. Isolated $\tau=0$ does not replace
  **25/48**.
- **H-long-B-iso.** Isolated $\tau=0$ confusion matrix stays
  chance-like relative to **47/96**. Do not sell any ngram-13 100-family
  count as replacing **25/48**.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --n-samples 4 --max-new-tokens 128 --seed 20260903 --ngram-len 13 \
  --out-dir experiments/2026-09-03-pair-100x4-ngram13

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-03-probe-100x4-ngram13-hard-last4
```

Do not look at key-free LRs until `pair` has written official
first-draw scores and the probe command has been run once, as written.

## 2026-09-03 longer-context Phase B opened

[PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md) Phase B named
`facc538`. Pair seed **20260903**, `ngram_len=13`, 100 one-liners.
Official first-draw **100/100** above 0.55 (H-long-B-ctrl holds).
Post-open extra-draw: **400/400** marked above 0.55, **0/400** unmarked.
Key-free interpolate last-4 **76/100** (AUC **0.666**, isolated
**267/400 vs 222/400**, BA **489/800**). Hard **66/100** (AUC
**0.579**, isolated **215/400 vs 221/400**). `used_keys=false`.
Below public-mixin lock A **99/100**. Clopper–Pearson on **76/100** is
**[0.664, 0.840]** and excludes ½. H-long-B-group holds. Isolated
**489/800** is not chance-like vs **47/96** on this different corpus;
do not sell **76/100**, **267/400**, or **489/800** as replacing
**25/48**. Isolated-file detection is still not finished. Do not write
`thesis/`.

JSON: `experiments/2026-09-03-pair-100x4-ngram13/`,
`experiments/2026-09-03-probe-100x4-ngram13-hard-last4/`.

## 2026-09-03 Hw=12 occupancy decode start

Named `df5487d` before looking at occupancy counts. H-long-occ is
leave-one-family-out interpolate atoms (`atoms --leave-one-out`), not
pooled `tables-counts`. Same interpolate reader as the Hw=12 probe.
Original-12 `ngram_len=13` twins, public `ngram_len=5` original-12
comparison, and 100-family companion. Not a new `probe --methods`
name. Do not sell occupancy as replacing **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-09-03-pair-12x4-ngram13 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-03-atoms-12x4-ngram13

python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-03-atoms-12x4-public-loo

python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-09-03-pair-100x4-ngram13 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-03-atoms-100x4-ngram13
```

## 2026-09-03 Hw=12 occupancy (original 12)

Named `df5487d` before the counts. Leave-one-family-out interpolate
atoms, `used_keys=false`. File LRs match interpolate holdout
(marked `lr>0` **20/48**). Hw=12 exact overlap **160** seen vs
**12026** unseen. Public Hw=4 original-12 **269** seen vs **11912**
unseen. Every window has fewer seen events under Hw=12 (0:4 is 71 vs
84). H-long-occ holds. Occupancy is not a detector. Do not sell
**160**, **269**, `'The' → ' bus'`, or `'The' → ' ferry'` as replacing
**25/48**. Isolated-file detection is still not finished. Do not write
`thesis/`.

JSON: `experiments/2026-09-03-atoms-12x4-ngram13/`,
`experiments/2026-09-03-atoms-12x4-public-loo/`.

## 2026-09-03 Hw=12 occupancy (100 families)

Same `atoms --leave-one-out` command. `used_keys=false`. File LRs
match interpolate holdout (marked `lr>0` **267/400**). Hw=12 exact
overlap **5878** seen vs **95624** unseen (0:4 is 1287 vs 1113).
Public Hw=4 100-family **10158** seen vs **91353** unseen (lock A
interpolate **352/400**). Every window has fewer seen events under
Hw=12. Occupancy is not a detector. Do not sell **5878**, **10158**,
`'The' → ' house'`, or `'"' → 'This'` as replacing **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-03-atoms-100x4-ngram13/`,
`experiments/2026-09-03-atoms-100x4-public-loo/`.

## 2026-09-03 Kirchenbauer mixin two-grain freeze

[PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md) committed at SHA
`8371406`. Frozen before generation.
Sol's 260903 other external-validity arm: Hugging Face Kirchenbauer
green-list defaults (`WatermarkLogitsProcessor` /
`WatermarkDetector`), not a SynthID `ngram_len` change. Original 12
Grok prompt strings, GPT-2, 4 draws, $T=128$, seed **20260904**,
`--mixin kgw`, Hub SHA `607a30d783dfa663caf39e06633721c8d4cfcd7e`.
Official control is matching z-score (`z_threshold=3.0`), not
`detector_mean`. Hypotheses H-kgw-ctrl, H-kgw-group, H-kgw-hard,
H-kgw-iso, and H-kgw-occ are stated before generation. Do not look at
key-free LRs until `pair` has written official first-draw z-scores and
the probe command has been run once, as written. Do not add a scorer.
Do not score those twins with SynthID `detector_mean`. A finished
100×4 corpus is not required for this freeze. Nothing replaces
**25/48**. Isolated-file detection is still not finished. Do not write
`thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --n-samples 4 --max-new-tokens 128 --seed 20260904 --mixin kgw \
  --hub-revision 607a30d783dfa663caf39e06633721c8d4cfcd7e \
  --out-dir experiments/2026-09-03-pair-12x4-kgw
```

## 2026-09-03 Kirchenbauer mixin two-grain opened

[PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md) named `09e40d4`. Pair seed
**20260904**, `--mixin kgw`, original 12 Grok strings. Official
first-draw matching z-score is above 3.0 on **12/12** first marked
files (H-kgw-ctrl holds). Post-open extra-draw check: **48/48** marked
above 3.0 (min $7.22$), **2/48** unmarked above 3.0. Key-free 12-LOO
interpolate last-4 is **12/12** (AUC **0.947**, isolated **44/48 vs
41/48**, balanced accuracy **85/96**). Hard is **12/12** (AUC
**0.703**, isolated **35/48 vs 25/48**, **60/96**). `used_keys=false`.
Occupancy **114** seen vs **12071** unseen (opening 40 vs 248). H-kgw-group
holds as the ≥**9/12** branch. Do not sell **12/12**, **44/48**,
**85/96**, or **114** as replacing **25/48**. Isolated-file detection
on the public SynthID original-12 is still not finished. Do not write
`thesis/`. One hundred families are not opened.

JSON: `experiments/2026-09-03-pair-12x4-kgw/`,
`experiments/2026-09-03-probe-12x4-kgw-hard-last4/`,
`experiments/2026-09-03-atoms-12x4-kgw/`.

## 2026-09-03 Kirchenbauer 100-family start

[PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md) 100-family readout, named
before generation. Same freeze SHA `8371406`. Hugging Face Kirchenbauer
defaults, GPT-2, prompts `experiments/2026-09-01-prompts-100/`,
`--n-samples 4`, $T=128$, seed **20260904**, `--mixin kgw`, Hub SHA
`607a30d783dfa663caf39e06633721c8d4cfcd7e`. Same readers: hard and
interpolate last-4 leave-one-family-out. Same two grains. No new
`probe --methods` name.

Stated before these 100×4 LRs:

- **H-kgw-B-ctrl.** Official first-draw matching z-score is above $3.0$
  on every first marked file.
- **H-kgw-B-group.** Interpolate last-4 prompt ranking is reported
  beside original-12 **12/12**. It does not replace lock A **99/100**
  or isolated **25/48**.
- **H-kgw-B-iso.** Isolated $\tau=0$ confusion matrix does not replace
  **25/48**. Do not sell any Kirchenbauer 100-family count as replacing
  **25/48**.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --n-samples 4 --max-new-tokens 128 --seed 20260904 --mixin kgw \
  --hub-revision 607a30d783dfa663caf39e06633721c8d4cfcd7e \
  --out-dir experiments/2026-09-03-pair-100x4-kgw

python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-kgw \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-03-probe-100x4-kgw-hard-last4
```

Do not look at key-free LRs until `pair` has written official
first-draw z-scores and the probe command has been run once, as written.

## 2026-09-03 Kirchenbauer 100-family opened

[PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md) 100-family named `8f09aa6`.
Pair seed **20260904**, `--mixin kgw`, 100 one-liners. Official
first-draw z>3 **100/100** (H-kgw-B-ctrl holds). Extra-draw **400/400**
marked above 3.0, **5/400** unmarked. Key-free interpolate last-4
**100/100** (AUC **0.982**, isolated **376/400 vs 371/400**, BA
**747/800**, mean $D_p=0.745$). Hard **62/100** (AUC **0.573**, BA
**440/800**). `used_keys=false`. Occupancy **4557** seen vs **96991**
unseen (opening 1044 vs 1356), below public $\Hw=4$ **10158** and
$\Hw=12$ **5878**. Do not sell **100/100**, **747/800**, or **4557** as
replacing **25/48**. Isolated-file detection on the public SynthID
original-12 is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-03-pair-100x4-kgw/`,
`experiments/2026-09-03-probe-100x4-kgw-hard-last4/`,
`experiments/2026-09-03-atoms-100x4-kgw/`.

---

## 2026-09-02 resample

**Collection.** `/Users/jens/kod/text-watermark-tools/experiments/claude-sample-2026-09-02` — **0** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-09-02-resample-work`.

---
## 2026-09-03 Qwen2-1.5B Kirchenbauer freeze

[PROTOCOL-next-kgw-qwen.md](PROTOCOL-next-kgw-qwen.md) committed at SHA
`45a75c9`. Frozen before generation. Same Hugging Face Kirchenbauer defaults as
[PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md), generator
`Qwen/Qwen2-1.5B-Instruct`, original 12 prompt strings, seed
**20260904**, `--mixin kgw`, plain prompts (no chat template).
Hypotheses H-kgw-q-ctrl, H-kgw-q-group, and H-kgw-q-iso are stated
before generation. Probe and atoms use `--model Qwen/Qwen2-1.5B-Instruct`.
Do not look at key-free LRs until `pair` has written official first-draw
z-scores and the probe command has been run once, as written. Do not add
a scorer. Nothing replaces **25/48**. Isolated-file detection is still
not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260904 --mixin kgw \
  --out-dir experiments/2026-09-03-pair-qwen-12x4-kgw
```

## 2026-09-03 Qwen2-1.5B Kirchenbauer opened

[PROTOCOL-next-kgw-qwen.md](PROTOCOL-next-kgw-qwen.md) named `4f0ce39`.
Pair seed **20260904**, `--mixin kgw`, `--model Qwen/Qwen2-1.5B-Instruct`.
Official first-draw z>3 **12/12** (H-kgw-q-ctrl holds). Interpolate
last-4 **12/12** (AUC **0.814**, isolated **35/48 vs 33/48**, BA
**68/96**). Hard **8/12** (AUC **0.566**, BA **50/96**). Occupancy
**84** seen vs **12108** unseen. `used_keys=false`. Hub revision was
unpinned (`null`). Do not sell **12/12** or **68/96** as replacing
**25/48**. Isolated-file detection is still not finished. Do not write
`thesis/`.

JSON: `experiments/2026-09-03-pair-qwen-12x4-kgw/`,
`experiments/2026-09-03-probe-qwen-12x4-kgw-hard-last4/`,
`experiments/2026-09-03-atoms-qwen-12x4-kgw/`.

## 2026-09-03 DistilGPT2 Kirchenbauer freeze

[PROTOCOL-next-kgw-distil.md](PROTOCOL-next-kgw-distil.md) committed at
SHA `1540d3c`. Frozen before generation. Same Hugging Face Kirchenbauer defaults as
[PROTOCOL-next-kgw.md](PROTOCOL-next-kgw.md), generator `distilgpt2`,
original 12 prompt strings, seed **20260904**, `--mixin kgw`.
Hypotheses H-kgw-d-ctrl, H-kgw-d-group, and H-kgw-d-iso are stated
before generation. Do not look at key-free LRs until `pair` has written
official first-draw z-scores and the probe command has been run once,
as written. Do not add a scorer. Nothing replaces **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260904 \
  --mixin kgw --out-dir experiments/2026-09-03-pair-distil-12x4-kgw
```

## 2026-09-03 DistilGPT2 Kirchenbauer opened

[PROTOCOL-next-kgw-distil.md](PROTOCOL-next-kgw-distil.md) named
`55ca96e`. Pair seed **20260904**, `--mixin kgw`, `--model distilgpt2`.
Official first-draw z>3 **12/12** (H-kgw-d-ctrl holds). Interpolate
last-4 **12/12** (AUC **0.947**, isolated **42/48 vs 43/48**, BA
**85/96**). Hard **11/12** (AUC **0.780**, BA **66/96**). Occupancy
**130** seen vs **11972** unseen. `used_keys=false`. Hub revision was
unpinned (`null`). Do not sell **12/12** or **85/96** as replacing
**25/48**. Isolated-file detection is still not finished. Do not write
`thesis/`.

JSON: `experiments/2026-09-03-pair-distil-12x4-kgw/`,
`experiments/2026-09-03-probe-distil-12x4-kgw-hard-last4/`,
`experiments/2026-09-03-atoms-distil-12x4-kgw/`.

## 2026-09-03 resample

**Collection.** `experiments/claude-sample-2026-09-03` — **40** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

| Contrast | last-1 | last-4 |
|---|---|---|
| premark-vs-new (40 prompts) | 37/40 | 35/40 |
| previous-vs-new (40 prompts) | 33/40 | 29/40 |

Last-1 ahead of last-4 is the style-shift order. Last-4 ahead of last-1 is the public-mixin watermark-window order. Do not call either a vendor detector. Same-day chance means draw noise.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-09-03-resample-work`.

---

## 2026-09-03 DistilGPT2 Kirchenbauer 100-family freeze

[PROTOCOL-next-kgw-distil.md](PROTOCOL-next-kgw-distil.md) 100-family
arm named `4fad227` before generation. Same Hugging Face Kirchenbauer defaults,
generator `distilgpt2`, prompts `experiments/2026-09-01-prompts-100/`,
seed **20260904**, `--mixin kgw`, Hub SHA
`2290a62682d06624634c1f46a6ad5be0f47f38aa`. Hypotheses H-kgw-d100-ctrl,
H-kgw-d100-group, H-kgw-d100-iso, and H-kgw-d100-occ are stated before
generation. Do not look at key-free LRs until `pair` has written
official first-draw z-scores and the probe command has been run once,
as written. Do not add a scorer. Nothing replaces **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260904 \
  --mixin kgw --hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa \
  --out-dir experiments/2026-09-03-pair-distil-100x4-kgw
```

## 2026-09-03 DistilGPT2 Kirchenbauer 100-family opened

[PROTOCOL-next-kgw-distil.md](PROTOCOL-next-kgw-distil.md) named
`4fad227`. Pair seed **20260904**, `--mixin kgw`, `--model distilgpt2`,
Hub SHA `2290a62682d06624634c1f46a6ad5be0f47f38aa`. First `pair` hit a
full disk at stem 088; persist `.strip()` had also emptied newline-only
draws. Harness fix `8984759`. Same flags after the fix. Official
first-draw z>3 **100/100** (H-kgw-d100-ctrl holds; unmarked **16/100**
above 3.0 are newline loops). Interpolate last-4 **100/100** (AUC
**0.915**, isolated **346/400 vs 337/400**, BA **683/800**). Hard
**82/100** (AUC **0.666**, BA **502/800**). Occupancy **16170** seen vs
**71541** unseen (opening 1800 vs 600; `'\n\n' → '\n\n'` n=172).
`used_keys=false`. Do not sell **100/100** or **683/800** as replacing
**25/48**. Isolated-file detection is still not finished. Do not write
`thesis/`.

JSON: `experiments/2026-09-03-pair-distil-100x4-kgw/`,
`experiments/2026-09-03-probe-distil-100x4-kgw-hard-last4/`,
`experiments/2026-09-03-atoms-distil-100x4-kgw/`.

## 2026-09-04 Aaronson–Kirchner exponential-minimum freeze

[PROTOCOL-next-aaronson.md](PROTOCOL-next-aaronson.md) committed at SHA
`747f3cd`. Frozen before generation. Laboratory exponential-minimum sampler
(`--mixin aaronson`), not in `transformers==4.57.6`. GPT-2, original 12
prompt strings, seed **20260905**, Hub SHA
`607a30d783dfa663caf39e06633721c8d4cfcd7e`, `hashing_key` **314159265**,
`context_width=1`. Official control is the matching mean-\(r\) z-test,
not `detector_mean` and not Kirchenbauer `WatermarkDetector`.
Hypotheses H-aar-ctrl, H-aar-group, H-aar-hard, H-aar-iso, and
H-aar-occ are stated before generation. Do not look at key-free LRs
until `pair` has written official first-draw z-scores and the probe
command has been run once, as written. Do not add a scorer. Nothing
replaces **25/48**. Isolated-file detection is still not finished. Do
not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --n-samples 4 --max-new-tokens 128 --seed 20260905 --mixin aaronson \
  --hub-revision 607a30d783dfa663caf39e06633721c8d4cfcd7e \
  --out-dir experiments/2026-09-04-pair-12x4-aaronson
```

## 2026-09-04 Aaronson–Kirchner exponential-minimum opened

[PROTOCOL-next-aaronson.md](PROTOCOL-next-aaronson.md) named `29a1436`.
Pair seed **20260905**, `--mixin aaronson`. Official first-draw z>3
**12/12** (H-aar-ctrl holds; unmarked **0/12**). Interpolate last-4
**11/12** (AUC **0.955**, isolated **8/48 vs 48/48**, BA **56/96**;
loses station). Hard **12/12** (AUC **0.976**, BA **72/96**). Occupancy
**573** seen vs **11618** unseen. `used_keys=false`. Hub SHA
`607a30d783dfa663caf39e06633721c8d4cfcd7e`. Do not sell **11/12**,
**12/12**, **8/48**, or **56/96** as replacing **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-12x4-aaronson/`,
`experiments/2026-09-04-probe-12x4-aaronson-hard-last4/`,
`experiments/2026-09-04-atoms-12x4-aaronson/`.

## 2026-09-04 Aaronson–Kirchner 100-family start

[PROTOCOL-next-aaronson.md](PROTOCOL-next-aaronson.md) 100-family arm
named before generation (same freeze SHA `747f3cd`). GPT-2, prompts
`experiments/2026-09-01-prompts-100/`, `--n-samples 4`, $T=128$, seed
**20260905**, `--mixin aaronson`, Hub SHA
`607a30d783dfa663caf39e06633721c8d4cfcd7e`. Same readers: hard and
interpolate last-4 leave-one-family-out. Same two grains. No new
`probe --methods` name.

Stated before these 100×4 LRs:

- **H-aar-B-ctrl.** Official matching z-score is above $3.0$ on every
  first marked file. Unmarked first-draw is not all above $3.0$.
- **H-aar-B-group.** Interpolate last-4 prompt ranking is reported
  beside original-12 Aaronson **11/12** and GPT-2 Kirchenbauer
  **100/100**. Either drop or hold is informative. It does not replace
  **25/48**.
- **H-aar-B-iso.** Isolated $\tau=0$ does not replace **25/48**.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --n-samples 4 --max-new-tokens 128 --seed 20260905 --mixin aaronson \
  --hub-revision 607a30d783dfa663caf39e06633721c8d4cfcd7e \
  --out-dir experiments/2026-09-04-pair-100x4-aaronson
```

Do not look at key-free LRs until `pair` has written official first-draw
z-scores and the probe command has been run once, as written. Do not add
a scorer. Nothing replaces **25/48**. Isolated-file detection is still
not finished. Do not write `thesis/`.

## 2026-09-04 Aaronson–Kirchner 100-family opened

[PROTOCOL-next-aaronson.md](PROTOCOL-next-aaronson.md) named `2f9de1a`.
Pair seed **20260905**, `--mixin aaronson`. Official first-draw z>3
**100/100** (H-aar-B-ctrl holds; unmarked **0/100**). Interpolate last-4
**100/100** (AUC **0.986**, isolated **208/400 vs 400/400**, BA
**608/800**). Hard **95/100** (AUC **0.950**, BA **744/800**). Occupancy
**25167** seen vs **76418** unseen. `used_keys=false`. Do not sell
**100/100** or **608/800** as replacing **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-100x4-aaronson/`,
`experiments/2026-09-04-probe-100x4-aaronson-hard-last4/`,
`experiments/2026-09-04-atoms-100x4-aaronson/`.

## 2026-09-04 DistilGPT2 ngram_len=13 freeze

[PROTOCOL-next-longctx-distil.md](PROTOCOL-next-longctx-distil.md)
committed at SHA `bae6d81`. Frozen before generation. Same public keys and `ngram_len=13` ($\Hw=12$) as
[PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md), generator
`distilgpt2`, original 12 prompt strings, seed **20260903**, Hub SHA
`2290a62682d06624634c1f46a6ad5be0f47f38aa`. Hypotheses H-long-d-ctrl,
H-long-d-group, H-long-d-iso, and H-long-d-occ are stated before
generation. Do not look at key-free LRs until `pair` has written
official first-draw scores and the probe command has been run once, as
written. Do not add a scorer. Nothing replaces **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260903 \
  --ngram-len 13 --hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa \
  --out-dir experiments/2026-09-04-pair-distil-12x4-ngram13
```

## 2026-09-04 DistilGPT2 ngram_len=13 opened

[PROTOCOL-next-longctx-distil.md](PROTOCOL-next-longctx-distil.md) named
`c120dc4`. Pair seed **20260903**, `ngram_len=13`, `--model distilgpt2`.
Official first-draw mean>0.55 **12/12** (H-long-d-ctrl holds). Interpolate
last-4 **9/12** (AUC **0.563**, isolated **21/48 vs 28/48**, BA
**49/96**). Hard **6/12** (AUC **0.485**, BA **42/96**). Occupancy
**175** seen vs **11994** unseen. `used_keys=false`. Do not sell
**9/12** or **49/96** as replacing **25/48**. Isolated-file detection is
still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-distil-12x4-ngram13/`,
`experiments/2026-09-04-probe-distil-12x4-ngram13-hard-last4/`,
`experiments/2026-09-04-atoms-distil-12x4-ngram13/`.

## 2026-09-04 Qwen2-1.5B ngram_len=13 freeze

[PROTOCOL-next-longctx-qwen.md](PROTOCOL-next-longctx-qwen.md)
committed at SHA `d7303a2`. Frozen before generation. Same public keys and `ngram_len=13` ($\Hw=12$)
as [PROTOCOL-next-longctx.md](PROTOCOL-next-longctx.md), generator
`Qwen/Qwen2-1.5B-Instruct`, original 12 prompt strings, seed **20260903**,
Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`. Hypotheses
H-long-q-ctrl, H-long-q-group, H-long-q-iso, and H-long-q-occ are stated
before generation. Do not look at key-free LRs until `pair` has written
official first-draw scores and the probe command has been run once, as
written. Do not add a scorer. Nothing replaces **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260903 --ngram-len 13 \
  --hub-revision ba1cf1846d7df0a0591d6c00649f57e798519da8 \
  --out-dir experiments/2026-09-04-pair-qwen-12x4-ngram13
```

## 2026-09-04 Qwen2-1.5B ngram_len=13 opened

[PROTOCOL-next-longctx-qwen.md](PROTOCOL-next-longctx-qwen.md) named
`21a3e1b`. Pair seed **20260903**, `ngram_len=13`,
`--model Qwen/Qwen2-1.5B-Instruct`. Official first-draw mean>0.55
**11/12** (library $0.515$; H-long-q-ctrl fails as a raw 12/12). Mixin
is on for the other eleven stems (`n_unmasked_ngrams=116`). Interpolate
last-4 **4/12** (AUC **0.400**, isolated **14/48 vs 27/48**, BA
**41/96**). Hard **4/12** (AUC **0.415**, BA **47/96**). Occupancy
**65** seen vs **12127** unseen. `used_keys=false`. Do not sell
**4/12** or **41/96** as replacing **25/48**. Isolated-file detection is
still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-qwen-12x4-ngram13/`,
`experiments/2026-09-04-probe-qwen-12x4-ngram13-hard-last4/`,
`experiments/2026-09-04-atoms-qwen-12x4-ngram13/`.

## 2026-09-04 resample

**Collection.** `experiments/claude-sample-2026-09-04` — **0** long texts.
Separate Chrome profile (`--via cdp --no-cdp`) hit Cloudflare
verification and never logged in. Did not attach to the already-open
claude.ai tab (that collector navigates the first tab to `/new`). Did
not quit the live Chrome session to start CDP on :9222. Last successful
sample remains `experiments/claude-sample-2026-09-03` (**40** texts).
`assumed_watermark: rumored`. Not a Claude detector. Not a watermark
claim.

Do not train a Claude detector on the pre-mark pile alone.

## 2026-09-04 DistilGPT2 Aaronson freeze

[PROTOCOL-next-aaronson-distil.md](PROTOCOL-next-aaronson-distil.md)
committed at SHA `9bdf12a`. Frozen before generation. Same laboratory Aaronson–Kirchner
exponential-minimum as [PROTOCOL-next-aaronson.md](PROTOCOL-next-aaronson.md),
generator `distilgpt2`, original 12 prompt strings, seed **20260905**,
`--mixin aaronson`, Hub SHA `2290a62682d06624634c1f46a6ad5be0f47f38aa`.
Hypotheses H-aar-d-ctrl, H-aar-d-group, H-aar-d-iso, and H-aar-d-occ
are stated before generation. Do not look at key-free LRs until `pair`
has written official first-draw z-scores and the probe command has been
run once, as written. Do not add a scorer. Nothing replaces **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260905 \
  --mixin aaronson --hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa \
  --out-dir experiments/2026-09-04-pair-distil-12x4-aaronson
```

## 2026-09-04 DistilGPT2 Aaronson opened

[PROTOCOL-next-aaronson-distil.md](PROTOCOL-next-aaronson-distil.md)
named `40a6300`. Pair seed **20260905**, `--mixin aaronson`,
`--model distilgpt2`. Official first-draw z>3 **12/12** (H-aar-d-ctrl
holds; unmarked **1/12** above 3, night-bus $3.029$). Interpolate
last-4 **7/12** (AUC **0.618**, isolated **0/48 vs 48/48**, BA
**48/96**; all 7 ranking wins have 0 isolated TPs). Hard **7/12**
(AUC **0.637**, isolated **8/48 vs 48/48**, BA **56/96**). Occupancy
**196** seen vs **11996** unseen. `used_keys=false`. Do not sell
**7/12** or **0/48** as replacing **25/48**. Isolated-file detection is
still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-distil-12x4-aaronson/`,
`experiments/2026-09-04-probe-distil-12x4-aaronson-hard-last4/`,
`experiments/2026-09-04-atoms-distil-12x4-aaronson/`.

## 2026-09-04 Qwen2-1.5B Aaronson freeze

[PROTOCOL-next-aaronson-qwen.md](PROTOCOL-next-aaronson-qwen.md)
committed at SHA `1171d5c`. Frozen before generation. Same laboratory Aaronson–Kirchner
exponential-minimum as [PROTOCOL-next-aaronson.md](PROTOCOL-next-aaronson.md),
generator `Qwen/Qwen2-1.5B-Instruct`, original 12 prompt strings, seed
**20260905**, `--mixin aaronson`, Hub SHA
`ba1cf1846d7df0a0591d6c00649f57e798519da8`. Hypotheses H-aar-q-ctrl,
H-aar-q-group, H-aar-q-iso, and H-aar-q-occ are stated before
generation. Probe and atoms use `--model Qwen/Qwen2-1.5B-Instruct`.
Do not look at key-free LRs until `pair` has written official
first-draw z-scores and the probe command has been run once, as
written. Do not add a scorer. Nothing replaces **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260905 --mixin aaronson \
  --hub-revision ba1cf1846d7df0a0591d6c00649f57e798519da8 \
  --out-dir experiments/2026-09-04-pair-qwen-12x4-aaronson
```

## 2026-09-04 Qwen2-1.5B Aaronson opened

[PROTOCOL-next-aaronson-qwen.md](PROTOCOL-next-aaronson-qwen.md) named
`406c91d`. Pair seed **20260905**, `--mixin aaronson`,
`--model Qwen/Qwen2-1.5B-Instruct`. Official first-draw z>3 **12/12**
(H-aar-q-ctrl holds; unmarked **0/12**). Interpolate last-4 **12/12**
(AUC **0.993**, isolated **12/48 vs 48/48**, BA **60/96**; 9/12 ranking
wins have 0 isolated TPs). Hard **12/12** (AUC **0.911**, isolated
**24/48 vs 48/48**, BA **72/96**). Occupancy **457** seen vs **11735**
unseen. `used_keys=false`. Do not sell **12/12** or **60/96** as
replacing **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-qwen-12x4-aaronson/`,
`experiments/2026-09-04-probe-qwen-12x4-aaronson-hard-last4/`,
`experiments/2026-09-04-atoms-qwen-12x4-aaronson/`.

## 2026-09-04 DistilGPT2 ngram_len=13 100-family freeze

[PROTOCOL-next-longctx-distil-100.md](PROTOCOL-next-longctx-distil-100.md)
committed at SHA `d891622`. Frozen before generation. Same public keys and `ngram_len=13` ($\Hw=12$)
as [PROTOCOL-next-longctx-distil.md](PROTOCOL-next-longctx-distil.md),
generator `distilgpt2`, 100 one-liners, seed **20260903**, Hub SHA
`2290a62682d06624634c1f46a6ad5be0f47f38aa`. Hypotheses H-long-d100-ctrl,
H-long-d100-group, H-long-d100-iso, and H-long-d100-occ are stated
before generation. Do not look at key-free LRs until `pair` has written
official first-draw scores and the probe command has been run once, as
written. Do not add a scorer. Nothing replaces **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260903 \
  --ngram-len 13 --hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa \
  --out-dir experiments/2026-09-04-pair-distil-100x4-ngram13
```

## 2026-09-04 DistilGPT2 ngram_len=13 100-family opened

[PROTOCOL-next-longctx-distil-100.md](PROTOCOL-next-longctx-distil-100.md)
named `0598357`. Pair seed **20260903**, `ngram_len=13`,
`--model distilgpt2`. Official first-draw mean>0.55 **98/100**
(H-long-d100-ctrl fails as a raw 100/100; stems 020 and 047 have
`n_unmasked_ngrams=1`). Interpolate last-4 **88/100** (AUC **0.785**,
isolated **325/400 vs 232/400**, BA **557/800**). Hard **89/100**
(AUC **0.829**, BA **544/800**). Occupancy **11182** seen vs **85493**
unseen. `used_keys=false`. Do not sell **88/100** or **557/800** as
replacing **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-distil-100x4-ngram13/`,
`experiments/2026-09-04-probe-distil-100x4-ngram13-hard-last4/`,
`experiments/2026-09-04-atoms-distil-100x4-ngram13/`.

## 2026-09-04 DistilGPT2 Aaronson 100-family freeze

[PROTOCOL-next-aaronson-distil-100.md](PROTOCOL-next-aaronson-distil-100.md)
committed at SHA `bf05759`. Frozen before generation. Same laboratory Aaronson–Kirchner
exponential-minimum as [PROTOCOL-next-aaronson-distil.md](PROTOCOL-next-aaronson-distil.md),
generator `distilgpt2`, 100 one-liners, seed **20260905**,
`--mixin aaronson`, Hub SHA `2290a62682d06624634c1f46a6ad5be0f47f38aa`.
Hypotheses H-aar-d100-ctrl, H-aar-d100-group, H-aar-d100-iso, and
H-aar-d100-occ are stated before generation. Do not look at key-free
LRs until `pair` has written official first-draw z-scores and the probe
command has been run once, as written. Do not add a scorer. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260905 \
  --mixin aaronson --hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa \
  --out-dir experiments/2026-09-04-pair-distil-100x4-aaronson
```

## 2026-09-04 DistilGPT2 Aaronson 100-family opened

[PROTOCOL-next-aaronson-distil-100.md](PROTOCOL-next-aaronson-distil-100.md)
named `bbef06e`. Pair seed **20260905**, `--mixin aaronson`,
`--model distilgpt2`. Official first-draw z>3 **71/100**
(H-aar-d100-ctrl fails as a raw 100/100; 29 Distil degenerate loops at
$z=-5.52$). Interpolate last-4 **96/100** (AUC **0.902**, isolated
**252/400 vs 349/400**, BA **601/800**; 36/96 ranking wins have 0
isolated TPs). Hard **91/100** (AUC **0.899**, BA **654/800**).
Occupancy **28824** seen vs **61305** unseen. `used_keys=false`. Do not
sell **96/100** or **601/800** as replacing **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-distil-100x4-aaronson/`,
`experiments/2026-09-04-probe-distil-100x4-aaronson-hard-last4/`,
`experiments/2026-09-04-atoms-distil-100x4-aaronson/`.

## 2026-09-04 Qwen2-1.5B Aaronson 100-family freeze

[PROTOCOL-next-aaronson-qwen-100.md](PROTOCOL-next-aaronson-qwen-100.md)
committed at SHA `a761a7d`. Frozen before generation. Same laboratory Aaronson–Kirchner
exponential-minimum as [PROTOCOL-next-aaronson-qwen.md](PROTOCOL-next-aaronson-qwen.md),
generator `Qwen/Qwen2-1.5B-Instruct`, 100 one-liners, seed **20260905**,
`--mixin aaronson`, Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`.
Hypotheses H-aar-q100-ctrl, H-aar-q100-group, H-aar-q100-iso, and
H-aar-q100-occ are stated before generation. Do not look at key-free
LRs until `pair` has written official first-draw z-scores and the probe
command has been run once, as written. Probe and `atoms` must pass
`--model Qwen/Qwen2-1.5B-Instruct`. Do not add a scorer. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260905 --mixin aaronson \
  --hub-revision ba1cf1846d7df0a0591d6c00649f57e798519da8 \
  --out-dir experiments/2026-09-04-pair-qwen-100x4-aaronson
```

## 2026-09-04 resample

**Collection.** `/Users/jens/kod/text-watermark-tools/experiments/claude-sample-2026-09-04` — **0** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-09-04-resample-work`.

---
## 2026-09-04 resample

**Collection.** `experiments/claude-sample-2026-09-04` — **40** long texts.
`assumed_watermark: rumored`. `used_keys=false`. GPT-2 tokenizer.
Not a Claude detector. Not a watermark claim.

| Contrast | last-1 | last-4 |
|---|---|---|
| premark-vs-new (40 prompts) | 36/40 | 37/40 |
| previous-vs-new (40 prompts) | 20/40 | 19/40 |

Last-1 ahead of last-4 is the style-shift order. Last-4 ahead of last-1 is the public-mixin watermark-window order. Do not call either a vendor detector. Same-day chance means draw noise.

Do not train a Claude detector on the pre-mark pile alone. Work dir: `/Users/jens/kod/text-watermark-tools/experiments/2026-09-04-resample-work`.

## 2026-09-04 Qwen2-1.5B Aaronson 100-family pair resume

Host crashed while `pair` was writing
`experiments/2026-09-04-pair-qwen-100x4-aaronson/` (37/100 complete
stems on disk; no `results.json`). Resume used the same frozen flags
(seed **20260905**, `--mixin aaronson`, Hub SHA
`ba1cf1846d7df0a0591d6c00649f57e798519da8`) and the same `--out-dir`.
`pair` re-scores complete stems and regenerates the rest. Do not look
at key-free LRs until official first-draw z-scores and the probe
command have been run once, as written. Nothing replaces **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.

## 2026-09-04 Qwen2-1.5B ngram_len=13 100-family freeze

[PROTOCOL-next-longctx-qwen-100.md](PROTOCOL-next-longctx-qwen-100.md)
committed at SHA `636765c`. Frozen before generation. Same public keys and `ngram_len=13`
($\Hw=12$) as [PROTOCOL-next-longctx-qwen.md](PROTOCOL-next-longctx-qwen.md),
generator `Qwen/Qwen2-1.5B-Instruct`, 100 one-liners, seed **20260903**,
Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`.
Hypotheses H-long-q100-ctrl, H-long-q100-group, H-long-q100-iso, and
H-long-q100-occ are stated before generation. Do not look at key-free
LRs until `pair` has written official first-draw scores and the probe
command has been run once, as written. Probe and `atoms` must pass
`--model Qwen/Qwen2-1.5B-Instruct`. Do not add a scorer. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260903 --ngram-len 13 \
  --hub-revision ba1cf1846d7df0a0591d6c00649f57e798519da8 \
  --out-dir experiments/2026-09-04-pair-qwen-100x4-ngram13
```

## 2026-09-04 Hw=12 vs Hw=4 body-window freeze

Draft GitHub PRs **#5**, **#6**, and **#7** (not merged) named a hole:
full-file $\Hw=12$ interpolate **76/100** may be the opening, not a
weaker body reader. [PROTOCOL-next-longctx-windows.md](PROTOCOL-next-longctx-windows.md)
committed at SHA `8283d1f`. Frozen before those window LRs. Existing twins only
(`experiments/2026-09-03-pair-100x4-ngram13/`,
`experiments/2026-09-01-pair-100x4/`). Existing methods
`interpolate,hard,hits`. Do not overwrite the full-file $\Hw=12$ dump
or the public H2 absolute windows. Do not look at window LRs until
the two probe commands have been run once, as written. Do not start
those probes while Qwen Aaronson 100 `pair` holds the CPU. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods interpolate,hard,hits --context-len 4 --skip-hashpool \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-probe-100x4-ngram13-windows

python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --methods interpolate --context-len 4 --skip-hashpool \
  --windows 64:128 \
  --out-dir experiments/2026-09-04-probe-100x4-public-w64-128
```

## 2026-09-04 Hw=12 vs Hw=4 body-window dumps

The two freeze commands were run once, as written, into
`experiments/2026-09-04-probe-100x4-ngram13-windows/` and
`experiments/2026-09-04-probe-100x4-public-w64-128/`.
`used_keys=false`. Full-file interpolate stayed **76/100** ($\Hw=12$)
and **99/100** (public lock A). Interpolate last-4 on $[64{:}128)$ is
**50/100**, AUC **0.501** under $\Hw=12$ and **93/100**, AUC **0.726**
under public $\Hw=4$. Opening $[0{:}4)$ under $\Hw=12$ is **86/100**.
Hits full-file **91/100** sits with the opening (**95/100**), not the
tail (**53/100**). Those `/tmp` window-end previews were the same two
grains; git now has the freeze dumps. Do not sell **50/100** or
**93/100** as replacing **25/48**. Isolated-file detection is still
not finished. Do not write `thesis/`.

## 2026-09-04 Qwen2-1.5B Aaronson 100-family opened

[PROTOCOL-next-aaronson-qwen-100.md](PROTOCOL-next-aaronson-qwen-100.md)
named `de035df`. Pair seed **20260905**, `--mixin aaronson`,
`--model Qwen/Qwen2-1.5B-Instruct`. Official first-draw z>3 **99/100**
(H-aar-q100-ctrl fails as a raw 100/100; stem 025 $z=1.95$).
Interpolate last-4 **100/100** (AUC **0.999**, isolated
**216/400 vs 400/400**, BA **616/800**; 46/100 ranking wins have 0
isolated TPs). Hard **97/100** (AUC **0.949**, BA **665/800**).
Occupancy **8750** seen vs **92842** unseen. `used_keys=false`. Do not
sell **100/100** or **616/800** as replacing **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-qwen-100x4-aaronson/`,
`experiments/2026-09-04-probe-qwen-100x4-aaronson-hard-last4/`,
`experiments/2026-09-04-atoms-qwen-100x4-aaronson/`.

## 2026-09-04 Qwen2-1.5B ngram_len=13 100-family opened

[PROTOCOL-next-longctx-qwen-100.md](PROTOCOL-next-longctx-qwen-100.md)
named `fd72ec5`. Pair seed **20260903**, `ngram_len=13`,
`--model Qwen/Qwen2-1.5B-Instruct`. Official first-draw mean>0.55
**91/100** (H-long-q100-ctrl fails as a raw 100/100). Unmarked
**0/100** above $0.55$. Interpolate last-4 **76/100** (AUC **0.647**,
isolated **273/400 vs 201/400**, BA **474/800**). Hard **74/100**
(AUC **0.599**, BA **476/800**). Occupancy **3535** seen vs **98064**
unseen. `used_keys=false`. Do not sell **76/100** or **474/800** as
replacing **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-qwen-100x4-ngram13/`,
`experiments/2026-09-04-probe-qwen-100x4-ngram13-hard-last4/`,
`experiments/2026-09-04-atoms-qwen-100x4-ngram13/`.

## 2026-09-04 Qwen2-1.5B Kirchenbauer 100-family freeze

[PROTOCOL-next-kgw-qwen-100.md](PROTOCOL-next-kgw-qwen-100.md)
named `ed9fb20` before generation. Same Hugging Face Kirchenbauer defaults as
[PROTOCOL-next-kgw-qwen.md](PROTOCOL-next-kgw-qwen.md), generator
`Qwen/Qwen2-1.5B-Instruct`, 100 one-liners, seed **20260904**,
`--mixin kgw`, Hub SHA `ba1cf1846d7df0a0591d6c00649f57e798519da8`.
Hypotheses H-kgw-q100-ctrl, H-kgw-q100-group, H-kgw-q100-iso, and
H-kgw-q100-occ are stated before generation. Do not look at key-free
LRs until `pair` has written official first-draw z-scores and the probe
command has been run once, as written. Probe and `atoms` must pass
`--model Qwen/Qwen2-1.5B-Instruct`. Do not add a scorer. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260904 --mixin kgw \
  --hub-revision ba1cf1846d7df0a0591d6c00649f57e798519da8 \
  --out-dir experiments/2026-09-04-pair-qwen-100x4-kgw
```

## 2026-09-04 Qwen Kirchenbauer 100-family pair resume

Pid **35117** exited at 15:21 CEST with **44/100** complete stems and no
`results.json`. Resume used the same frozen flags and
`--out-dir experiments/2026-09-04-pair-qwen-100x4-kgw` (pid **44722**).
Complete stems are re-scored, not regenerated. Do not invent interpolate
counts. That lock is not **25/48**. Isolated-file detection is still
not finished. Do not write `thesis/`.

## 2026-09-04 PR #7 remains markdown-only

GitHub PR **#7** (`cursor/lovande-ideer-kgw-gloaguen-1051`) was updated
on the remote and stays **unmerged**. Those notes are not this
laboratory's dump-backed lock. Do not copy `/tmp` holdouts from that
file into the report. Qwen2-1.5B Kirchenbauer 100-family
([PROTOCOL-next-kgw-qwen-100.md](PROTOCOL-next-kgw-qwen-100.md), freeze
`ed9fb20`) is the in-flight pair. Window remasure of those twins, if
any, waits until `results.json` and the frozen last-4 probe exist. Do
not add a `probe --methods` name. Do not leftover-target. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

## 2026-09-04 PR #9 inspected, stays unmerged

GitHub PR **#9** (`cursor/lovande-holdouts-1051`) copies 146 JSON
holdouts from exploratory `/tmp` probes (`used_keys=false`). It stays
**unmerged**. Public SynthID original-12 last-2 hits is **29/48**
(ranking **9/12**, AUC **0.632**). Last-1 hits is **24/48** (ranking
**4/12**, AUC **0.445**). Neither replaces hard last-4 **25/48**.
Kirchenbauer original-12 last-1 hits **46/48** (AUC **0.975**) is a
different mixin (`context_width=1` body leak). Qwen Aaronson last-1
hits **48/48 vs 48/48** is a different mixin. Do not copy those
`/tmp` files onto `main`. Do not add a `probe --methods` name. Do not
leftover-target. Isolated-file detection is still not finished. Do not
write `thesis/`.

## 2026-09-04 Distil / gpt2-medium unmarked-LM opening rankpath freeze

This freeze names
[PROTOCOL-isolated-rankpath-lm.md](PROTOCOL-isolated-rankpath-lm.md)
(`d8e6f7f`) named before Distil-LM / gpt2-medium-LM opening rankpath
LRs. Existing
`rankpath` on `experiments/2026-08-17-pair-12x4/`. Flags:

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --model distilgpt2 --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 --methods rankpath \
  --out-dir experiments/2026-09-04-probe-12x4-rankpath-distil-lm

python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --model gpt2-medium --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 --methods rankpath \
  --out-dir experiments/2026-09-04-probe-12x4-rankpath-medium-lm
```

Do not start while the Qwen Kirchenbauer 100 `pair` holds the CPU. Do
not leftover-slice. Do not merge PR **#9**. Do not invent those scores.
Same-LM GPT-2-small recount stays **11/12**, isolated **41/48 vs 35/48**.
Nothing replaces **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`.

## 2026-09-04 Distil unmarked-LM opening rankpath opened

H-rplm-d **fails** as a raw count. DistilGPT2 unmarked-LM opening
rankpath on original GPT-2 12×4 is ranking **10/12**, isolated
**32/48 vs 31/48** (AUC **0.761**; nested **28/48 vs 37/48**).
`used_keys=false`. Do not sell **32/48**. gpt2-medium-LM isolated is
**31/48 vs 32/48** (ranking **10/12**, AUC **0.679**). H-rplm-m **fails**
as a raw count. Do not sell **31/48**. Qwen Kirchenbauer 100 official
first-draw z>3 is **90/100**; unmarked **0/100**; interpolate **96/100**
/ **620/800**. H-kgw-q100-ctrl **fails**. Nothing replaces **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.

## 2026-09-04 Qwen2-1.5B Kirchenbauer 100-family opened

[PROTOCOL-next-kgw-qwen-100.md](PROTOCOL-next-kgw-qwen-100.md)
named `ed9fb20`. Pair seed **20260904**, `--mixin kgw`,
`--model Qwen/Qwen2-1.5B-Instruct`. Official first-draw z>3
**90/100** (H-kgw-q100-ctrl fails as a raw 100/100). Unmarked
**0/100** above $3.0$. Interpolate last-4 **96/100** (AUC **0.870**,
isolated **346/400 vs 274/400**, BA **620/800**). Hard **63/100**
(AUC **0.562**, BA **430/800**). Occupancy **4858** seen vs **96740**
unseen. `used_keys=false`. Do not sell **96/100** or **620/800** as
replacing **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

JSON: `experiments/2026-09-04-pair-qwen-100x4-kgw/`,
`experiments/2026-09-04-probe-qwen-100x4-kgw-hard-last4/`,
`experiments/2026-09-04-atoms-qwen-100x4-kgw/`.

## 2026-09-04 Qwen Kirchenbauer 100-family windows freeze

[PROTOCOL-next-kgw-qwen-100-windows.md](PROTOCOL-next-kgw-qwen-100-windows.md)
named `e270546` before those LRs. Same Qwen2-1.5B Kirchenbauer 100-family
twins, leave-one-family-out interpolate/hard last-4 on windows
`0:4,4:16,16:32,32:64,64:128`. Full-file interpolate **96/100** stays
in `experiments/2026-09-04-probe-qwen-100x4-kgw-hard-last4/`. Do not
overwrite it. Do not look at window LRs until the analysis command has
been run once, as written. Probe must pass `--model
Qwen/Qwen2-1.5B-Instruct`. Nothing replaces **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-qwen-100x4-kgw \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods interpolate,hard --context-len 4 --skip-hashpool \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-probe-qwen-100x4-kgw-windows
```

## 2026-09-04 Qwen Kirchenbauer 100-family windows opened

[PROTOCOL-next-kgw-qwen-100-windows.md](PROTOCOL-next-kgw-qwen-100-windows.md)
named `e270546`. Full-file interpolate **96/100** (H-kgw-q100-win-ctrl
holds). Opening $[0{:}4)$ interpolate **84/100** (AUC **0.679**). Tail
$[64{:}128)$ interpolate **97/100** (AUC **0.785**, isolated
**314/400 vs 252/400**, **566/800**). Not chance; not $\Hw=12$
**50/100**. `used_keys=false`. Do not sell **97/100** or **84/100** as
replacing **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

JSON: `experiments/2026-09-04-probe-qwen-100x4-kgw-windows/`.

## 2026-09-04 gpt2-medium native opening rankpath freeze

This freeze names
[PROTOCOL-isolated-rankpath-m12.md](PROTOCOL-isolated-rankpath-m12.md)
named before gpt2-medium native opening rankpath LRs. Existing
`rankpath` on `experiments/2026-09-01-pair-gpt2-medium-12x4/`. Flags:

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-gpt2-medium-12x4 \
  --model gpt2-medium --skip-hashpool \
  --fit-prefix 4 --pos-bucket 1 --methods rankpath \
  --out-dir experiments/2026-09-04-probe-medium-12x4-rankpath-native
```

Do not leftover-slice. Do not merge PR **#9**. Do not invent those
scores. Distil native stays **8/12**, isolated **28/48 vs 32/48**.
Nothing replaces **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`. Freeze SHA `2577771`.

## 2026-09-04 gpt2-medium native opening rankpath opened

H-rpm12 **holds**. gpt2-medium native opening rankpath on gpt2-medium
12×4 is ranking **6/12**, isolated **22/48 vs 30/48** (AUC **0.641**;
nested **19/48 vs 31/48**). `used_keys=false`. Do not sell **22/48**.
Nothing replaces **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`.

## 2026-09-04 GPT-2-small LM on gpt2-medium 12 freeze

This freeze names
[PROTOCOL-isolated-rankpath-g2m.md](PROTOCOL-isolated-rankpath-g2m.md)
named before GPT-2-small-on-medium opening rankpath LRs. Existing
`rankpath` on `experiments/2026-09-01-pair-gpt2-medium-12x4/` with
`--model gpt2`. Do not leftover-slice. Do not invent those scores.
Medium native stays **6/12**, isolated **22/48 vs 30/48**. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`. Freeze SHA `336a1fd`.

## 2026-09-04 GPT-2-small LM on gpt2-medium 12 opened

H-rpg2m **holds**. GPT-2-small LM opening rankpath on gpt2-medium 12×4
is ranking **8/12**, isolated **20/48 vs 32/48** (AUC **0.619**; nested
**17/48 vs 47/48**). `used_keys=false`. Do not sell **20/48**. GPT-2-small
on GPT-2 twins stays **41/48**. Nothing replaces **25/48**. Isolated-file
detection is still not finished. Do not write `thesis/`.

## 2026-09-04 Distil LM on gpt2-medium 12 freeze

This freeze names
[PROTOCOL-isolated-rankpath-d2m.md](PROTOCOL-isolated-rankpath-d2m.md)
named before Distil-on-medium opening rankpath LRs. Existing `rankpath`
on `experiments/2026-09-01-pair-gpt2-medium-12x4/` with
`--model distilgpt2`. Do not leftover-slice. Do not invent those scores.
GPT-2-small on the same twins stays **8/12**, isolated **20/48 vs 32/48**.
Nothing replaces **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`. Freeze SHA `b3fd331`.

## 2026-09-04 Distil LM on gpt2-medium 12 opened

H-rpd2m **fails** as a raw count. Distil LM opening rankpath on
gpt2-medium 12×4 is ranking **11/12**, isolated **30/48 vs 31/48** (AUC
**0.703**; nested **23/48 vs 41/48**). `used_keys=false`. Do not sell
**30/48** or **11/12**. Prompt ranking is a different grain. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

## 2026-09-04 GPT-2-small LM on Distil 12 freeze

This freeze names
[PROTOCOL-isolated-rankpath-g2d.md](PROTOCOL-isolated-rankpath-g2d.md)
named before GPT-2-on-Distil opening rankpath LRs. Existing `rankpath`
on `experiments/2026-08-31-pair-distilgpt2-12x4/` with `--model gpt2`.
Do not leftover-slice. Do not invent those scores. Distil native stays
**8/12**, isolated **28/48 vs 32/48**. Nothing replaces **25/48**.
Isolated-file detection is still not finished. Do not write `thesis/`.
Freeze SHA `d62c732`.

## 2026-09-04 GPT-2-small LM on Distil 12 opened

H-rpg2d **holds**. GPT-2-small LM opening rankpath on Distil 12×4 is
ranking **6/12**, isolated **24/48 vs 27/48** (AUC **0.532**; nested
**16/48 vs 34/48**). `used_keys=false`. Do not sell **24/48**. Distil
native stays **8/12**, isolated **28/48 vs 32/48**. File AUC is chance.
Nothing replaces **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`.

## 2026-09-04 gpt2-medium LM on Distil 12 freeze

This freeze names
[PROTOCOL-isolated-rankpath-m2d.md](PROTOCOL-isolated-rankpath-m2d.md)
named before gpt2-medium-on-Distil opening rankpath LRs. Existing
`rankpath` on `experiments/2026-08-31-pair-distilgpt2-12x4/` with
`--model gpt2-medium`. Do not leftover-slice. Do not invent those
scores. Distil native stays **8/12**, isolated **28/48 vs 32/48**.
GPT-2-small on Distil stays **6/12**, isolated **24/48 vs 27/48**.
Nothing replaces **25/48**. Isolated-file detection is still not
finished. Do not write `thesis/`. Freeze SHA `571d4f1`.

## 2026-09-04 gpt2-medium LM on Distil 12 opened

H-rpm2d **fails** as a raw count. gpt2-medium LM opening rankpath on
Distil 12×4 is ranking **9/12**, isolated **30/48 vs 33/48** (AUC
**0.638**; nested **26/48 vs 34/48**). `used_keys=false`. Do not sell
**30/48** or **9/12**. Distil native stays **8/12**, isolated
**28/48 vs 32/48**. GPT-2-small on Distil stays **6/12**, isolated
**24/48 vs 27/48**. Prompt ranking is a different grain. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`.

## 2026-09-04 opening rankpath body [4:16) freeze

This freeze names
[PROTOCOL-isolated-rankpath-body.md](PROTOCOL-isolated-rankpath-body.md)
named before rankpath `[4:16)` LRs. Existing `rankpath` on
`experiments/2026-08-17-pair-12x4/` with `--windows 4:16 --fit-prefix 16
--pos-bucket 1`. Do not leftover-slice. Do not invent those scores.
Opening `[0:4)` stays **11/12**, isolated **41/48 vs 35/48**. Nothing
replaces **25/48**. Isolated-file detection is still not finished.
Do not write `thesis/`. Freeze SHA `dbc61c5`.

## 2026-09-04 opening rankpath body [4:16) opened

H-rpbody **holds**. Bucketed rankpath on `[4:16)` is ranking **7/12**,
isolated **20/48 vs 22/48** (AUC **0.430**; nested **2/48 vs 43/48**).
`used_keys=false`. Opening `[0:4)` stays **11/12**, isolated
**41/48 vs 35/48**. The unwindowed fit-prefix-16 file score **29/48** is
not the frozen slice. Do not sell **20/48** or **29/48**. File AUC is
below chance. Nothing replaces **25/48**. Isolated-file detection is
still not finished. Do not write `thesis/`.

## 2026-09-04 Distil-LM rankpath body [4:16) freeze

This freeze names
[PROTOCOL-isolated-rankpath-dbody.md](PROTOCOL-isolated-rankpath-dbody.md)
named before Distil-LM rankpath `[4:16)` LRs. Existing `rankpath` on
`experiments/2026-08-17-pair-12x4/` with `--model distilgpt2 --windows
4:16 --fit-prefix 16 --pos-bucket 1`. Do not leftover-slice. Do not
invent those scores. Distil-LM opening stays **10/12**, isolated
**32/48 vs 31/48**. GPT-2 `[4:16)` stays **7/12**, isolated
**20/48 vs 22/48**. Nothing replaces **25/48**. Isolated-file detection
is still not finished. Do not write `thesis/`.

---
