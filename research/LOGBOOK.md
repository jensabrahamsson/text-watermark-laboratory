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

---
