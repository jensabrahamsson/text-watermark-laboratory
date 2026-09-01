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

---
