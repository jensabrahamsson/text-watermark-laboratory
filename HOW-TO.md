# How to use text-watermark-laboratory

This guide gets the laboratory running, explains the two scoring paths, and shows how to reproduce the key-free watermark experiments.

## What the lab can tell you

There are two different ways to measure text in this repository.

### 1. `score`: known-key reference detection

`score` asks:

> How strongly does this text match DeepMind's public `public-deepmind-30` SynthID-Text instance?

It uses the published keys and DeepMind's detector.

### 2. `indicate`: key-free watermark indication

`indicate` asks:

> Does this text statistically resemble the marked or unmarked side of a corpus learned from matched generations?

It does **not** use the watermark keys, `hash_iv`, or g-values.

This is one of the main research results of the project: we have built a **key-free watermark indicator**. On the current 12-prompt × 4-draw experiment the original last-4 count tables separate held-out prompt groups **10/12** times, or **11/12** with a 0.02 comparison margin. Scoring only shared 4-grams (`hits`) reaches **11/12** with no margin (AUC **0.737**). Hash pooling reaches **11/12** and **35/48** isolated marked files with `lr > 0`. On the original hard scorer, individual files are weaker: **29/48** held-out marked files have `lr > 0`. Four draws on 36 GPT-2 topics lift in-domain hits to **36/36** (AUC **0.934**); a nested-by-stem Youden on those LRs is **119/144** vs **134/144**. Train 12×4 and score 96 new-topic 36×4 files: nested hits 10% FPR is **83/96** vs **85/96**. None of that is a universal yes/no.

Use `score` when you have the relevant public reference instance. Use `indicate` when you are exploring the key-free signal.

---

## Requirements

- Python 3.10+
- Git
- a few GB of disk space
- roughly 8 GB RAM
- internet access during installation

A GPU is not required. The standard setup uses CPU JAX.

The project is developed primarily on macOS with Apple silicon. Linux and WSL2 follow the same shell workflow. Native Windows is expected to work but is less heavily exercised.

---

## Installation

Clone this repository and DeepMind's public SynthID-Text repository beside each other:

```bash
mkdir -p "$HOME/src"
cd "$HOME/src"
git clone https://github.com/jensabrahamsson/text-watermark-laboratory.git
git clone https://github.com/google-deepmind/synthid-text.git
cd text-watermark-laboratory
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

Install the lab and attach the SynthID-Text checkout:

```bash
pip install -e ".[jax-cpu,dev]"
pip install -e "$HOME/src/synthid-text" --no-deps
```

The project intentionally pins:

```text
transformers==4.57.6
```

Transformers 5.x can make GPT-2 generation with the mixin stop at EOS before the requested minimum length. The compatibility shim in `generate.py` keeps the public mixin working on 4.57.6.

Verify the setup:

```bash
python -m pytest tests/ -q
```

---

## First reference measurement

Score a known marked sample:

```bash
python -m text_watermark_tools score \
  experiments/2026-08-17-pair-12x4/01-harbour-marked.txt
```

Typical output:

```text
... mean=0.623224 weighted_mean=0.641979 n_tokens=126 n_unmasked_ngrams=122 instance=public-deepmind-30 ngram_len=5
```

Now score its unmarked twin:

```bash
python -m text_watermark_tools score \
  experiments/2026-08-17-pair-12x4/01-harbour-unmarked-gen.txt
```

Typical mean:

```text
0.508333
```

The public reference detector cleanly separates the known marked and unmarked laboratory twins.

### Reading a `score` line

| Field | Meaning |
|---|---|
| `mean` | DeepMind reference mean for this instance |
| `weighted_mean` | Weighted version of the same measurement |
| `n_tokens` | Tokens processed |
| `n_unmasked_ngrams` | 5-grams included in the score |
| `instance` | Watermark key set being tested |
| `ngram_len` | Detector n-gram length |

A score around 0.60–0.65 with plenty of usable n-grams is strong evidence for the **tested public instance**. Around 0.50 means no measurable bias toward that key set.

Very short text may produce `nan` because there are too few n-grams.

---

## Score your own text

File:

```bash
python -m text_watermark_tools score /full/path/to/text.txt
```

Clipboard on macOS:

```bash
pbpaste | python -m text_watermark_tools score
```

Directory:

```bash
python -m text_watermark_tools score /full/path/to/folder
```

The default tokenizer is GPT-2, matching the bundled experiments:

```bash
python -m text_watermark_tools score path/to/text.txt --model gpt2
```

Tokenization affects n-gram boundaries, so compare scores produced under the same tokenizer.

---

## Shuffled-key control

A marked sample should score highly against the correct public keys and near chance against a shuffled control:

```bash
python -m text_watermark_tools score \
  experiments/2026-08-17-pair-12x4/01-harbour-marked.txt \
  --control-shuffled-keys
```

Typical pattern:

```text
public-deepmind-30   ≈ 0.62
control-shuffled-30 ≈ 0.50
```

This is a useful sanity check that the measured bias follows the correct key set.

---

## Run the key-free experiment

Generate matched twins:

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --out-dir experiments/pairs --max-new-tokens 128
```

Run leave-one-out comparison:

```bash
python -m text_watermark_tools blind experiments/pairs \
  --out-dir experiments/blind
```

For the stronger 12-prompt × 4-draw experiment:

```bash
python -m text_watermark_tools indicate holdout \
  experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4
```

The key point is that the held-out decision is made without calling `detector_mean`.

---

## Fit and use the key-free indicator

Fit reusable token/context tables:

```bash
python -m text_watermark_tools indicate fit \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/indicator-gpt2 \
  --context-len 4
```

Score a file:

```bash
python -m text_watermark_tools indicate score path/to/text.txt \
  --tables experiments/indicator-gpt2
```

The output contains `lr`, a log-likelihood ratio.

- positive `lr`: more similar to the learned marked distribution
- negative `lr`: more similar to the learned unmarked distribution

Hashpool tables (the 35/48 isolated reader) are a different persist:

```bash
python -m text_watermark_tools indicate fit \
  experiments/2026-08-17-pair-12x4 \
  --method hashpool \
  --out-dir experiments/indicator-gpt2-hashpool

python -m text_watermark_tools indicate score path/to/text.txt \
  --tables experiments/indicator-gpt2-hashpool
```

Count tables also accept `--score-mode hits` (shared 4-grams only). Nested
out-of-family hashpool tables, with a train-only `decision_threshold`, are in
`experiments/2026-08-31-transfer-nested-36-to-12x4/tables-hashpool/`.

UTF-8 surface tables need no tokenizer:

```bash
python -m text_watermark_tools indicate fit \
  experiments/2026-08-17-pair-36 \
  --method surface \
  --out-dir experiments/indicator-gpt2-surface

python -m text_watermark_tools indicate score path/to/text.txt \
  --tables experiments/indicator-gpt2-surface
```

That is a genuine indicator signal, but its calibration depends on the training corpus. Leave-one-of-12-out hard last-4 still overlaps at threshold 0 (**29/48**). Hits trained on other topics marks **39/48** of those same 12×4 files. Nested hashpool Youden on that split is **33/48** marked and **34/48** unmarked. Do not turn the sign of one LR into a universal yes/no claim.

The strongest *prompt-group* evidence currently comes from matched/repeated prompts, where the original hard indicator reaches **10/12**, or **11/12** under the documented 0.02 comparison margin. `hits` and `hashpool` reach **11/12** with no margin. `indicate holdout --score-mode hashpool` leave-one-outs the hash buckets.

`indicate holdout` also prints a single-file **AUC** and a label-permutation p-value. The published 29/48 sign at threshold 0 is not a 5% binomial test; ranking of the same LRs is the fairer isolated-file summary.

See [research/key-free-twins.md](research/key-free-twins.md) and [research/key-free-probe.md](research/key-free-probe.md).

---

## Compare key-free scorers (`probe`)

Count tables are not the only way to read paired twins. `probe` leave-one-prompt-outs several key-free scorers on the same corpus and reports prompt-grain wins plus single-file AUC:

```bash
python -m text_watermark_tools probe \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/probe
```

`--pivot` adds an unmarked-LM choice-geometry probe (loads GPT-2; slower; still no watermark keys). `--score-mode` on `indicate holdout` selects one count scorer (`interpolate`, `gated`, `mix`, `hashpool`, `surface`, …). `--test-dir` on `probe` fits one twin directory and scores another (out-of-family transfer). `--shuffle-labels` is a negative control. Nested Youden / 10% FPR thresholds come from leave-one-prompt-out on the training stems only. `--max-draws N` keeps the first N marked/unmarked draws per stem (draw-count ablation). `--prefix-lens 16,32,64,96,128` scores token prefixes as isolated-file curves (in-domain 16 tokens already ranks **34/36**). `--windows 0:16,16:32,32:64,64:128` scores disjoint slices so later tokens are not mixed with the prefix. `--fit-prefix 16` clips every draw *before fit and score* (matched prefix; not the same as scoring a prefix of a full-file table). `--methods poshits,poshitmass,pospool --pos-bucket 16` namespaces last-4 counts by token position so early 4-grams do not share a bucket with the tail. `--coverage` reports the leave-one-out share of last-k contexts seen on both training sides, by token window; that is why the 4-gram reader is front-loaded. `poshitmass` is coverage-weighted hits on those same bucketed tables. Nested Youden / 10% FPR from leave-one-prompt-out on the *training* stems now includes poshits/poshitmass. `--include-first` also scores generated token 0 (the published reader skips it). `--prompt-context` uses `*-prompt.txt` as last-k so token 0 sees the mixin prompt; isolated `indicate score` of a lone file cannot do that. `--methods first` is token 0 alone. Leave-one-out `probe` also reports **nested-youden-by-stem**: a threshold fitted on other prompts' already-held-out LRs, then applied to this prompt.

These methods do not reconstruct keys. Hash pooling is a random feature-hash of contexts, not SynthID’s secret hash. `surface` hashes UTF-8 bytes of the raw string. On the 12×4 corpus, `hits` and `hashpool` both reach **11/12** prompt groups; hashpool’s isolated sign is **35/48**. Trained on 24 other topics, hits marks **39/48** of the 12×4 files (AUC 0.769); nested hashpool Youden is **33/48** vs **34/48**. Four training draws lift that ranking to **12/12** and **42/48** at t=0 (nested hits Youden 26/48 vs 44/48). Train 12×4, score 96 new-topic 36×4 files: nested hits 10% FPR **83/96** vs **85/96**. A 16-token prefix of the 36×4 twins already ranks **34/36** in-domain (AUC 0.916); matching mixin `ngram_len=5` does not beat last-4. A matched 16-token fit lifts unmarked ≤0 to **112/144** in-domain (AUC 0.929) and OOD file AUC to **0.818**. Position-bucketed hits keep 134/144 marked at t=0 on 36×4 with unmarked ≤0 **97/144**, and raise OOD file AUC to **0.811**. `--coverage` shows why the reader is front-loaded: token index 1 is **96.9%** shared last-1. Scoring only **0:4** already ranks **34/36** (AUC **0.917**). A matched 4-token fit with `--pos-bucket 1` balances in-domain t=0 at **131/144 vs 132/144**, and on 24 other topics ranks 12×4 **12/12** (AUC **0.873**, isolated **39/48 vs 41/48**, nested Youden matching t=0). Last-1 on those four tokens copies that OOD gate. Mixing token 0 into hits hurts it (9/12). Qwen's in-domain opening is first-token **12/12** (AUC **0.901**); hits without token 0 is 7/12. DistilGPT2 is officially 12/12; GPT-2 tables do not transfer across the shared tokenizer (hits 5/12, AUC 0.462). That GPT-2 isolated-file gate does not appear under leave-one-of-12-out (9/12) and does not transfer to Qwen. GPT-2 36×4 → new Qwen stays at chance. Witten–Bell interpolation did not help on 12×4. See [research/key-free-probe.md](research/key-free-probe.md).

## Key-free argmax snap (`scrub`)

Tournament sampling only reweights the unmarked model’s top-k. Snapping each token to that argmax, using the original prefixes, is a key-free scrub. Official `score` afterwards is a reference check, not part of the snap:

```bash
python -m text_watermark_tools scrub \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/scrub
```

This is not a fluent rewriter. It asks whether the public mark dies when tournament “upsets” are removed. On the 12×4 marked twins the official mean went **0.622 → 0.499**.

---

## Rewriting a known-marked sample

```bash
cp DASHSCOPE-KEY.conf.example DASHSCOPE-KEY.conf
python -m text_watermark_tools iterate path/to/marked.txt \
  --backend qwen \
  --out-dir experiments/iterate
```

For a light-edit control:

```bash
python -m text_watermark_tools iterate path/to/marked.txt \
  --backend qwen \
  --via polish \
  --out-dir experiments/iterate-polish
```

The rewrite experiments ask how an already-known mark changes under paraphrase or light editing. They are separate from the key-free classification experiment.

Keep API credentials in the gitignored config files or environment variables, never in tracked files or command-line arguments.

---

## Claude and other production systems

The public DeepMind key set is a reference instance, not a universal SynthID key.

A provider can use the same family of watermarking method with different keys, tokenization, hashing, depth, and thresholds. In that case the public `score` is simply testing the wrong instance.

That is exactly why the key-free work is interesting: a paired before/after corpus can reveal statistical changes without assuming access to the production detector.

For the Claude plan, see:

- [research/claude.md](research/claude.md)
- [research/paired-corpus.md](research/paired-corpus.md)

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named text_watermark_tools` | Activate `.venv` and reinstall the project |
| `No module named synthid_text` | Install the DeepMind checkout with `--no-deps` |
| JAX/CUDA errors on macOS | Use the `jax-cpu` extra |
| Generation stops too early | Confirm `transformers==4.57.6` |
| `mean=nan` | Use a longer text |
| `indicate` is near zero | The one-file signal is weak; aggregate or use matched evidence |

Rerun the tests at any time:

```bash
source .venv/bin/activate
python -m pytest tests/ -q
```

---

## Where to go next

- [README.md](README.md) — project and current result
- [research/key-free-twins.md](research/key-free-twins.md) — experimental protocol and key-free indicator
- [research/how-synthid-works.md](research/how-synthid-works.md) — implementation details
- [experiments/README.md](experiments/README.md) — experiment index
