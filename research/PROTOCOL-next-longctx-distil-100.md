# Confirmatory protocol (longer watermark history on DistilGPT2, 100 families)

This is a **methods freeze** for a 100-family generator-transfer of the
already opened DistilGPT2 $\Hw=12$ 12-LOO lock
([PROTOCOL-next-longctx-distil.md](PROTOCOL-next-longctx-distil.md)).
It does not add a `probe --methods` name. It does not edit the
`synthid-text` checkout. Distil original-12 interpolate **9/12** /
isolated **49/96** and GPT-2 100-family interpolate **76/100** stay in
those dumps. This file asks whether the same public keys and $\Hw=12$
still rank prompt groups on DistilGPT2 when the prompt frame is the
100 one-liners.

Author–year citations follow [CITING.md](CITING.md). Locked headlines
remain **9/12**, **25/48**, and **36/36**. Do **not** write `thesis/`
from this file.
Do **not** look at key-free LRs until this freeze is named in
[LOGBOOK.md](LOGBOOK.md), `pair` has written official first-draw
scores, and the analysis command has been run once, as written.
Do **not** add a new `probe --methods` name. Do **not** leftover-target
the original 12. Do **not** mix grok12 into any train.
Do **not** score these twins with the public `ngram_len=5` processor.

## Why freeze now

Sol (2026-09-03) asked for a preregistered longer-context two-grain
replication. GPT-2 $\Hw=12$ 100-family interpolate is **76/100**. Distil
$\Hw=12$ 12-LOO interpolate is **9/12**. The remaining cheap
generator-scale check that is not leftover targeting is the same
`ngram_len=13` on DistilGPT2 with the 100 one-liners. Kirchenbauer and
Aaronson Distil 100-family runs are different mixins and are **not**
this file.

## Primary scientific question

On DistilGPT2 with public keys and `ngram_len=13` ($\Hw=12$), under
leave-one-family-out interpolate last-4 and hard last-4 on 100
one-liners, do marked prompt-group means still outrank unmarked means?

Not: can Distil 12-LOO $\Hw=12$ tables classify the 100 files. Not:
leftover targeting. Not: a new scorer name. Not: replacing **25/48**.

## Frozen configuration (locked before generation)

| Item | Value |
|---|---|
| Generator / tokenizer | `distilgpt2` (pin Hub SHA `2290a62682d06624634c1f46a6ad5be0f47f38aa`) |
| Mixin keys | public-deepmind-30 (default) |
| `ngram_len` | **13** (same $\Hw=12$ as PROTOCOL-next-longctx) |
| Prompts | `experiments/2026-09-01-prompts-100/` |
| Draws / length / seed | `--n-samples 4`, `--max-new-tokens 128`, seed **20260903** |
| Pair out-dir | `experiments/2026-09-04-pair-distil-100x4-ngram13/` |
| Readers | `--methods hard,interpolate --context-len 4 --skip-hashpool` |
| Probe out-dir | `experiments/2026-09-04-probe-distil-100x4-ngram13-hard-last4/` |
| Fold | leave-one-family-out |
| Official control | matching `ngram_len=13` `detector_mean` |
| Primary group metric | $D_p$ sign count / 100, strict `>` |
| Primary isolated metric | $\tau=0$ matrix, balanced accuracy, AUC |

`pair --ngram-len 13` must generate **and** official-score with the
same `ngram_len`. Scoring Distil $\Hw=12$ twins with `ngram_len=5` is
a harness bug.

## Hypotheses (stated before generation)

- **H-long-d100-ctrl.** Official matching mean with `ngram_len=13` is
  above $0.55$ on every first marked file. Unmarked first-draw stays
  near $1/2$. If marked first-draws fail, stop; harness bug.
- **H-long-d100-group.** Interpolate last-4 100-LOO ranking is reported
  beside GPT-2 $\Hw=12$ **76/100**. Either drop or hold is informative.
  It does not replace **25/48**.
- **H-long-d100-iso.** Isolated $\tau=0$ does not replace **25/48**.
- **H-long-d100-occ.** Exact last-4 occupancy (`atoms --leave-one-out`)
  is logged after probe. Occupancy is a mechanistic intermediate, not
  a detector.

## Generation command

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260903 \
  --ngram-len 13 --hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa \
  --out-dir experiments/2026-09-04-pair-distil-100x4-ngram13
```

Do not look at key-free LRs until `pair` has written official
first-draw scores and the probe command has been run once, as written.
Do not change flags after the first run.

## Analysis command

```bash
python -m text_watermark_tools probe experiments/2026-09-04-pair-distil-100x4-ngram13 \
  --methods hard,interpolate --context-len 4 --skip-hashpool \
  --out-dir experiments/2026-09-04-probe-distil-100x4-ngram13-hard-last4
```

`used_keys=false`. Occupancy after probe (not a second freeze):

```bash
python -m text_watermark_tools atoms --leave-one-out \
  --test-dir experiments/2026-09-04-pair-distil-100x4-ngram13 \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-09-04-atoms-distil-100x4-ngram13
```

## What this protocol refuses

- Editing `synthid-text`.
- A Kirchenbauer / Aaronson generator in this file.
- New `probe --methods` names.
- Scoring Distil $\Hw=12$ twins with `ngram_len=5`.
- Leftover targeting.
- Selling any Distil $\Hw=12$ 100-family count as replacing **25/48**.
- Paid chat APIs.
- Writing `thesis/`.

## Preregistration mechanic

1. Commit this file before `pair`.
2. Name the SHA in [LOGBOOK.md](LOGBOOK.md) before generation.
3. Run `pair`, then probe, then log the two-grain counts.
4. If a command fails, fix the harness and re-run the **same** flags.

Human merge of PR #4 is out of scope for this file.

## Results

Protocol SHA `d891622`. Named `0598357`. Pair seed **20260903**.
`ngram_len=13`. `model=distilgpt2`. `used_keys=false`. Hub SHA
`2290a62682d06624634c1f46a6ad5be0f47f38aa`.

Pair dump: [experiments/2026-09-04-pair-distil-100x4-ngram13/](../experiments/2026-09-04-pair-distil-100x4-ngram13/).
Probe dump: [experiments/2026-09-04-probe-distil-100x4-ngram13-hard-last4/](../experiments/2026-09-04-probe-distil-100x4-ngram13-hard-last4/).

H-long-d100-ctrl **fails** as the preregistered 100/100 first-draw.
Official matching mean with `ngram_len=13` is above $0.55$ on
**98/100** first marked files. Stems 020 and 047 have
`n_unmasked_ngrams=1` and mean $0.533$. Unmarked first-draw is
**0/100** above $0.55$. Mixin is on for the other 98 stems. This is
not a `ngram_len=5` scoring bug. Do not sell **98/100**.

| Reader | Prompt wins | File AUC | Isolated t=0 | Unmarked ≤0 | TP FN TN FP | Balanced accuracy |
|---|---|---|---|---|---|---|
| interpolate last-4 | **88/100** | 0.785 | 325/400 | 232/400 | 325 75 232 168 | **557/800** |
| hard last-4 | **89/100** | 0.829 | 354/400 | 190/400 | 354 46 190 210 | **544/800** |

GPT-2 $\Hw=12$ interpolate on these prompt *strings* (different twins)
was **76/100**. Distil interpolate is **88/100**. Mean $D_p=0.322$
(interpolate) / $0.334$ (hard). Zero ranking wins have 0 isolated TPs.

Clopper–Pearson 95% (not a second freeze): interpolate **88/100** is
**[0.800, 0.936]** and does not include ½; BA **557/800** is
**[0.663, 0.728]**. Isolated **25/48** still includes ½.

H-long-d100-group **holds** as an informative comparison with GPT-2
$\Hw=12$ **76/100**. It does not replace **25/48**.

H-long-d100-iso **holds**. Isolated interpolate **557/800** is a
different generator and $\Hw$ from the original-12 SynthID **47/96**.
Do not sell **88/100**, **89/100**, **557/800**, or **544/800** as
replacing **25/48**.

H-long-d100-occ **holds**. Leave-one-family-out interpolate atoms
(`used_keys=false`). File LRs match interpolate **325/400**. Exact
next-token overlap is **11182** seen versus **85493** unseen (opening
$[0{:}4)$ is 2036 versus 364, including Distil newline loops).
Occupancy is not a detector. Do not sell **11182** as replacing
**25/48**.

JSON: [experiments/2026-09-04-atoms-distil-100x4-ngram13/](../experiments/2026-09-04-atoms-distil-100x4-ngram13/).

Isolated-file detection on the public SynthID original-12 remains
**25/48** / **47/96**. Do not write `thesis/`.

