# text-watermark-laboratory

**text-watermark-laboratory** explores a practical question about statistical text watermarks:

> **Can we tell whether text carries a watermark even when we do not have the detector keys?**

For the experimental setup in this repository, the answer is **yes — to a useful but still limited degree**.

Using Google DeepMind's public SynthID-Text implementation as a controlled reference, we generate matched marked and unmarked text from the same prompts. From those pairs we have built a **key-free watermark indicator**: a model that can score previously unseen text by how strongly its token statistics resemble the marked rather than the unmarked class, without using the watermark keys, `hash_iv`, or g-values.

The clean headline is **10/12 held-out prompt groups**: after training on the other eleven prompt families, the marked side of the twelfth ranks above its unmarked twin group. That is **relative discrimination**, not “here is one unknown file; marked yes/no?”. A 0.02 comparison margin lifts the same ranking to 11/12; that is a robustness check, not the main result. Single-file sign at threshold 0 is much weaker: **29/48** held-out marked files have `lr > 0` and **23/48** unmarked files have `lr ≤ 0` (about 60% sensitivity and 48% specificity). The signal is real. It is not a magic detector, and this lab did not invent key-free watermark detection.

This repository also contains the ordinary key-based reference scorer, matched-pair generation, rewrite/degradation experiments, and a pre-mark Claude corpus for future before/after comparison.

Install and run your first measurement: **[HOW-TO.md](HOW-TO.md)**  
Research notes: **[research/](research/)**  
Coding-agent instructions: **[AGENTS.md](AGENTS.md)**

---

## What we found

The key result is not merely that watermarked text leaves “some statistical trace”. Tournament sampling leaves a **secondary, learnable footprint** in next-token counts. A very simple model — context/token tables plus a likelihood ratio, no keys, no `hash_iv`, no g-values — can pick that footprint up. The code enforces the claim: `BlindModel` carries `used_keys`, `used_hash_iv`, and `used_g_values`, the held-out decision never consults `detector_mean`, and `indicate` refuses to persist a table that says those flags are true.

That still leaves two different tasks.

**Relative discrimination (the 10/12 number).** Leave one prompt family out. Fit marked and unmarked count tables on the rest. Score the held-out marked generations and the held-out unmarked generations. Count a hit if the marked group’s mean LR is higher than the unmarked group’s. Four draws and last-4 context: **10/12**. `--margin 0.02` lets the unmarked side win by up to 0.02 and still count as a marked win; that is how **11/12** appears. Quote **10/12**. Treat 11/12 as a tolerance note.

**Single-text classification (the 29/48 number).** Same leave-one-out tables, but decide from the sign of one file’s LR against 0, with no twin. Marked `lr > 0`: **29/48**. Unmarked `lr ≤ 0`: **23/48**. The two distributions overlap (mean marked LR +0.033, unmarked −0.003).

| Method | What is being asked | Result |
|---|---|---|
| Official `score` | Public DeepMind keys, 12 matched prompts | **12/12** |
| Key-free, 1 sample | Twin ranking, 12 × 128 tokens | **8/12** |
| Key-free, 4 samples, last-4 | Twin ranking of held-out prompt groups | **10/12** |
| Same LRs, margin 0.02 | Same ranking, unmarked may lead by 0.02 | 11/12 (not the headline) |
| Local Qwen2-1.5B, last-2 | Twin ranking, different generator | **10/12** |
| `indicate`, one marked file | Isolated `lr > 0` | **29/48** |
| `indicate`, one unmarked file | Isolated `lr ≤ 0` | **23/48** |

So `indicate` is an experimental watermark-presence indicator. It is not a universal verdict machine, and 10/12 must not be read as single-text accuracy.

Detailed protocol and results: [research/key-free-twins.md](research/key-free-twins.md).

---

## The controlled experiment

SynthID-Text does not insert hidden characters or metadata. The watermark changes **which next tokens are selected during generation**.

That makes a paired experiment possible:

```mermaid
flowchart TD
  P[Same prompt] --> U[Generate with watermark off]
  P --> M[Generate with watermark on]
  U --> UT[Unmarked twin]
  M --> MT[Marked twin]
```

With the public keys available, DeepMind's detector confirms that the mark is present:

```text
unmarked ≈ 0.50
marked   ≈ 0.61–0.65
```

For the key-free experiment, those official scores are not used to make the decision:

```mermaid
flowchart LR
  A[Hold out one prompt] --> B[Fit marked/unmarked token tables on the others]
  B --> C[Score held-out text without keys]
  C --> D[Likelihood ratio: marked-like vs unmarked-like]
```

The experiment therefore asks a harder question than ordinary detection: **is there enough structure in the sampler's output to infer watermark presence without reproducing the detector?**

For held-out *groups*, so far yes (10/12). For one file’s sign, not reliably.

---

## Commands

```bash
source .venv/bin/activate
python -m pytest tests/ -q

# Key-based reference score
python -m text_watermark_tools score path/to/text.txt

# Generate marked/unmarked twins
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --out-dir experiments/pairs --max-new-tokens 128

# Key-free leave-one-out experiment
python -m text_watermark_tools blind experiments/pairs \
  --out-dir experiments/blind

# Evaluate the key-free indicator
python -m text_watermark_tools indicate holdout experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4

# Fit reusable tables and score a file
python -m text_watermark_tools indicate fit experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/indicator-gpt2 --context-len 4

python -m text_watermark_tools indicate score path/to/text.txt \
  --tables experiments/indicator-gpt2
```

`score` and `indicate` answer different questions:

- `score` reproduces the public DeepMind detector for the known `public-deepmind-30` instance.
- `indicate` asks whether text statistically resembles the marked or unmarked side of a learned corpus **without those keys**.

---

## Reference scoring

The repository uses DeepMind's published 30-key reference configuration:

```text
instance=public-deepmind-30
ngram_len=5
```

A sufficiently long text near 0.50 shows no measurable bias toward **that key set**. A marked sample generated with the same public mixin typically scores around 0.61–0.65 in our runs.

This is a controlled research baseline. It is not a general human-vs-AI classifier.

---

## Rewriting experiments

The lab can also take a sample known to be marked under the public instance, rewrite it, and measure what happens to the signal.

Earlier measurements include:

- marked GPT-2 text: **0.617 / 0.638**
- light Sonnet proofread: **0.605 / 0.625**
- full Sonnet rewrite: **0.502 / 0.502**
- Qwen rewrite of a known marked sample: approximately **0.50**

These experiments measure how a known watermark behaves under transformation. They are not needed for the key-free indicator itself.

---

## Claude

Anthropic has announced text marking based on "a version of" SynthID-Text. Their production keys and detector are not public.

That makes Claude interesting for a different reason: it provides a future real-world test of the key-free method.

The repository contains a **pre-mark corpus** in `experiments/claude-premark-2026-08/`. Once a comparable marked corpus exists, the same prompts can be rerun and the before/after shift can be measured without pretending that DeepMind's public keys are Claude's keys.

See [research/claude.md](research/claude.md) and [research/paired-corpus.md](research/paired-corpus.md).

---

## Related work

This lab did **not** invent key-free watermark detection.

[TTP-Detect](https://arxiv.org/abs/2603.14968) (*Rethinking LLM Watermark Detection in Black-Box Settings*) formulates third-party, key-agnostic verification from observable outputs and paired watermarked/unwatermarked reference sets — the same audit problem, a different method. Earlier watermark-stealing and probing work learns structure from black-box samples. [ETH/SRI’s SynthID probe](https://www.sri.inf.ethz.ch/blog/probingsynthid) ([Sabanayagam, Hörl, Dobriban 2024](https://arxiv.org/abs/2405.20777)) shows that SynthID-Text can be detected as a *generator property* with repeated fixed-context queries. That is not the same measurement as scoring a finished string against count tables.

What this repository adds is a small, fully checked-in instance of the second measurement on DeepMind’s **public** mixin: GPT-2 and Qwen twins, leave-one-out, a frozen indicator table, tests, and raw JSON. The interesting claim is narrow. The keyed tournament leaves a distributional footprint that a count-based LR can learn **without reconstructing the g-function**. Independent work landed in the same research question; treat this as an empirical notebook, not a priority claim.

If the 10/12 ranking is a confound (topic reuse, tokenizer mismatch, prompt-family leakage), that is the thing to break. Extra draws of the *same* prompt helped last-4. Extra topics, by themselves, did not.

## Boundaries

The current results support a specific claim:

> **On this public mixin, matched twins leave enough key-free statistical structure that a count-based indicator can rank most held-out prompt groups.**

They do not establish invention of the problem, reliable classification of every isolated paragraph, recovery of secret keys, or equivalence between `public-deepmind-30` and production systems from other vendors.

Those are different questions.

---

## Project layout

```text
AGENTS.md        coding-agent instructions
HOW-TO.md        installation and practical usage
research/        methods and research notes
experiments/     dated runs and result artifacts
src/             score, pair, blind, indicate, iterate
```

The project depends on [`google-deepmind/synthid-text`](https://github.com/google-deepmind/synthid-text) but is not a fork.

Licensed under [MIT](LICENSE).
