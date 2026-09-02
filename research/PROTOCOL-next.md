# Confirmatory protocol (next corpus)

This is a **methods freeze**, not a paper. It exists so the next
measurement is a prediction about data that has not been opened, rather
than another scorer on `experiments/2026-08-17-pair-12x4`. Out-of-family
isolated-file transfer of these same three readers is
[PROTOCOL-isolated.md](PROTOCOL-isolated.md).

Author–year citations follow [CITING.md](CITING.md). Lab counts after the truncated-context recount are **9/12**, **25/48**,
and **36/36**. Pre-fix **10/12** / **29/48** stay in historical JSON.
Closest published finished-string paired-reference analog for third-party verification remains Wang et al.
(2026) TTP-Detect; this protocol is not a priority claim over that work
([related-work.md](related-work.md)).

Do **not** write `thesis/` from this file.

## Why freeze now

The original key-free last-4 count tables separate held-out prompt
groups **9/12** times after storing each real suffix once (pre-fix
**10/12** overcounted truncated openings). Isolated hard sign at 0 is
**25/48**. In-domain 36×4 hits is still **36/36**. Those three numbers
are the locked headlines. Frozen analysis commands below are unchanged.

Later readers on the same twins (hashpool, poshits, rankpath, hashtok,
cascades, mixer width, mixer seed, last-k) are **hypothesis
generators**. Leave-one-prompt-out protects a fit, not the researcher.
Occupancy-free last-k at the frozen mixer (`n_hashes=8`, seed
`20260831`) is the last order axis on that corpus: in-domain last-1 is
chance; last-3 prompt **11/12** has t=0 **24/48**; 24→12 last-4 still
wins nested FPR10. That is a negative on isolated-file density, not a
reason to invent another hashed scorer.

No new `probe --methods` names on the 12×4 / 36×4 twins after this
file's commit SHA.

## Primary scientific question

Is there a watermark-induced perturbation of the **early conditional
next-token distribution** that generalizes across new prompts and
sampling seeds on the public DeepMind GPT-2 mixin?

Not: can another table classify the old 12×4 files.

## Frozen scorers

Three readers, named before any new generation. Exact CLI. No keys,
`hash_iv`, or g-values.

| Lock | Reader | Command fragment |
|---|---|---|
| A | Hard last-4 (historical baseline) | `--methods interpolate --context-len 4` |
| B | Opening poshits (simple count) | `--methods poshits --fit-prefix 4 --pos-bucket 1` |
| C | Opening rankpath (rank symbols) | `--rankpath --fit-prefix 4 --pos-bucket 1` |

`interpolate` is the published hard last-4 count table (`indicate`
holdout `--rotate --context-len 4`). `poshits` is position-bucketed
last-4 on the first four generated tokens. `rankpath` is the five-symbol
unmarked-LM rank table on the same opening. Do not add hashtok, hashpool,
cascades, backoff, or learned combiners to this list after the corpus
exists.

Official `score` on the new twins is a **positive control** (the mixin
is on). It is not a key-free endpoint.

## Hypotheses (stated before generation)

- **H1.** On new prompt families, marked mean LR > unmarked mean LR
  under lock A (prompt-grain paired discrimination).
- **H2.** Window **0:4** ranks marked above unmarked more strongly than
  window **16:32** under lock A (`--windows 0:4,16:32` on the same
  files).
- **H3.** Lock C (rankpath) is more generator-specific than lock B
  (opening poshits) when the same prompts are generated with DistilGPT2
  and Qwen2-1.5B. Phase B; not required to open Phase A.

## Primary endpoint

**Prompt-level paired discrimination** under lock A: number of new
prompt stems whose marked-group mean LR exceeds the unmarked-group mean
LR, with no comparison margin.

Report file AUC and permutation p as secondary ranking. Do **not**
promote isolated `lr > 0` to the primary endpoint. Nested Youden / 10%
FPR, if reported, are frozen from training stems only.

## Corpus (Phase A)

One hundred **new** English one-line scene prompts, disjoint as strings
from `experiments/2026-08-17-prompts-36/`. Same register as seeds
13–36 (one sentence, everyday setting, no instruction to the model).

| Item | Value |
|---|---|
| Prompts | `experiments/2026-09-01-prompts-100/` (committed **before** `pair`) |
| Generator | GPT-2 + public DeepMind 30 mixin |
| Draws | `--n-samples 4` |
| Length | `--max-new-tokens 128` |
| Seed | `20260901` |
| Output | `experiments/2026-09-01-pair-100x4/` |

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-100x4
```

Do not look at key-free LRs until `pair` has written official first-draw
scores and this protocol's analysis commands have been run once, as
written.

## Analysis commands (Phase A)

Replace `PAIR` with the pair directory. Do not change flags after the
first run.

```bash
python -m text_watermark_tools probe PAIR \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-probe-100x4-hard-last4

python -m text_watermark_tools probe PAIR \
  --methods poshits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-probe-100x4-opening-poshits

python -m text_watermark_tools probe PAIR \
  --rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-probe-100x4-opening-rankpath

python -m text_watermark_tools probe PAIR \
  --methods interpolate --context-len 4 \
  --windows 0:4,4:16,16:32,32:64 \
  --out-dir experiments/2026-09-01-probe-100x4-hard-windows
```

Official lamp (first draw only, as in the 36×4 README):

```bash
python -m text_watermark_tools score experiments/2026-09-01-pair-100x4/001-marked.txt
```

H1 is lock A prompt wins. H2 is lock A window 0:4 versus 16:32 (prompt
wins and file AUC). Isolated `lr>0` may be logged; it is not H1.

## Phase B (same prompts, other generators)

Only after Phase A is checked in. Native DistilGPT2 and native
Qwen2-1.5B-Instruct, same 100 prompts, `--n-samples 4`, 128 tokens.
Locks B and C only (opening grain). H3: lock C prompt ranking drops
more than lock B relative to GPT-2 Phase A. Tokenizer match is not
treated as a detector ([key-free-contrast.md](key-free-contrast.md)).

Seed `20260901`. Do not change flags after the first run. Do not run
lock A on these twins. Do not look at key-free LRs until each `pair`
has written official first-draw scores and the two opening probes have
run once, as written.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-distil-100x4

python -m text_watermark_tools probe experiments/2026-09-01-pair-distil-100x4 \
  --model distilgpt2 --methods poshits --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-probe-distil-100x4-opening-poshits

python -m text_watermark_tools probe experiments/2026-09-01-pair-distil-100x4 \
  --model distilgpt2 --rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-probe-distil-100x4-opening-rankpath

python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-qwen-100x4

python -m text_watermark_tools probe experiments/2026-09-01-pair-qwen-100x4 \
  --model Qwen/Qwen2-1.5B-Instruct --methods poshits --fit-prefix 4 \
  --pos-bucket 1 \
  --out-dir experiments/2026-09-01-probe-qwen-100x4-opening-poshits

python -m text_watermark_tools probe experiments/2026-09-01-pair-qwen-100x4 \
  --model Qwen/Qwen2-1.5B-Instruct --rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-probe-qwen-100x4-opening-rankpath
```

H3 compares prompt-win *drops* from GPT-2 Phase A (lock B **100/100**,
lock C **96/100**). Isolated `lr>0` is not H3.

### DistilGPT2 (2026-09-01)

Official first-draw **70/100**. Lock B **88/100** with **1 tie** (drop 12
from GPT-2 **100/100** when ties are not awarded). Lock C **68/100** with
**1 tie** (drop 28 from **96/100**). Rankpath drops more. Historical
JSON still prints 89/100 and 69/100 under the old non-strict comparison;
do not rewrite that LOGBOOK entry. Qwen opened below.

`used_keys=false`. Do not sell 88/100, 68/100, 89/100, or 69/100 as replacing **25/48**.

### Qwen2-1.5B-Instruct (2026-09-01)

Local Hugging Face, not Dashscope. Official first-draw **100/100** (mixin
on; Distil lamp was **70/100**). Lock B **95/100** (drop 5 from 100).
Lock C **84/100** (drop 12 from 96). H3 holds on Qwen: rankpath drops
more. Isolated Qwen signs (333/400, 275/400) are not **25/48**.

`--rankpath` also scored default count methods. Lock C is rankpath
**84/100**, not those extras.

JSON: `experiments/2026-09-01-pair-qwen-100x4/`,
`experiments/2026-09-01-probe-qwen-100x4-opening-poshits/`,
`experiments/2026-09-01-probe-qwen-100x4-opening-rankpath/`.

## What this protocol refuses

- New hashed / backoff / cascade / learned scorers on 12×4 or 36×4.
- Fishing `--n-hashes`, mixer `seed`, or `--context-len` after looking
  at the 100×4 LRs.
- Selling 39/48, 41/48, 33/48, 24/48, last-3 **11/12**, or in-family
  100×4 nested Youden **322/400** / **392/400** as replacing **25/48**.
  Out-of-family isolated transfer is [PROTOCOL-isolated.md](PROTOCOL-isolated.md).
  Register-matched Grok-length train is
  [PROTOCOL-isolated-register.md](PROTOCOL-isolated-register.md)
  (lock A nested **16/48 vs 41/48**, does not beat **25/48**). Reverse
  100 one-liners → Grok-register 12 is
  [PROTOCOL-isolated-xreg.md](PROTOCOL-isolated-xreg.md)
  (lock A nested **22/48 vs 41/48**, occupancy-free **0/48**).
- Key recovery, SynthID `hash_iv`, or reimplementing `detector_mean`.
- Training a Claude marked/unmarked classifier on the pre-mark corpus.
- A 7-day Grok interval loop. Claude resample stays Wed/Fri/Sun 04:00.

## Preregistration mechanic

1. Commit this file (and, in a commit that still precedes `pair`, the
   100 prompt texts).
2. That git SHA is the protocol version.
3. Run `pair`, then the analysis commands above, then append a dated
   [LOGBOOK.md](LOGBOOK.md) entry with the SHA.
4. If a command fails, fix the harness and re-run the **same** flags.
   Do not add a fourth scorer.

Human merge of PR #2 / PR #3 is out of scope for this file.

## Read the old numbers

Locked headlines and the ablation index:

- [results-ledger.md](results-ledger.md)
- [../experiments/README.md](../experiments/README.md)
- [key-free-twins.md](key-free-twins.md)

## Phase A outcome (2026-09-01)

Protocol SHA `7001489`. Prompts committed in `294dba5`. Pair committed
in `bf98c92`. Analysis-code SHA `bbc802e` (truncated-context recount).
Official first-draw keyed score **100/100**. Frozen
commands above were run once, flags unchanged.

| Hypothesis | Result |
|---|---|
| H1 lock A prompt ranking | **99/100** (stem 088 misses). File AUC **0.898**, permutation p < 0.001 (file-level, descriptive). Isolated 352/400 vs 290/400 is secondary. |
| H2 window 0:4 vs 16:32 | **Reindexed** substring scorers: **0:4** **99/100**, AUC **0.885**; **16:32** **89/100**, AUC **0.689**. Absolute-history remasure [PROTOCOL-h2-absolute.md](PROTOCOL-h2-absolute.md): **0:4** **99/100**, AUC **0.885**; **16:32** **87/100**, AUC **0.695**. Opening still outranks mid-file. Absolute 16:32 did not rise versus reindexed **89/100**. Post-open paired McNemar is **86 / 13 / 1 / 0** (not a second freeze). Isolated **25/48** Clopper–Pearson includes ½. Do **not** overwrite this dump. Do **not** rewrite the first-run flags above. Prefix-4 still shows an opening is **sufficient** in-domain. Out-of-family onto Grok-length files the same interpolate tables are **not** front-loaded (0:4 **7/12**; tail **9/12**; [PROTOCOL-isolated-windows.md](PROTOCOL-isolated-windows.md)). Absolute-history remasure of those transfer windows is [PROTOCOL-isolated-windows-absolute.md](PROTOCOL-isolated-windows-absolute.md). Do **not** overwrite the reindexed dumps. |
| Lock B opening poshits | **100/100**, AUC **0.980** |
| Lock C opening rankpath | **96/100**, AUC **0.822** |
| H3 Distil/Qwen | Distil official **70/100**, B **88/100** (1 tie; drop 12), C **68/100** (1 tie; drop 28). Qwen official **100/100**, B **95/100** (drop 5), C **84/100** (drop 12). Rankpath drops more on both. |

`--rankpath` also scored default count methods. Lock C is rankpath
**96/100**, not hashpool/hard 100/100 from that same run. Do not sell
isolated 352/400 or poshits 393/400 as replacing **25/48**. Nested-by-stem
is still a threshold nest on already-OOF scores.
