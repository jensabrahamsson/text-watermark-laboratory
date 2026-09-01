# How SynthID-Text works

This note describes the public `google-deepmind/synthid-text` reference implementation used by the laboratory.

## The watermark is a sampling bias

SynthID-Text does not insert hidden Unicode, metadata, or a literal tag into the output.

The watermark is encoded in **which tokens the sampler chooses**.

During generation, a keyed function assigns binary g-values to candidate tokens in context. The sampler slightly favours candidates whose g-values align with the watermark. Detection later asks whether the observed token sequence contains more of that keyed structure than chance predicts.

That is why the mark can survive as a statistical property of ordinary-looking text.

## Public reference configuration

The default reference setup used here has:

```text
ngram_len = 5
context length H = 4
30 public keys
context_history_size = 1024
```

The initial `hash_iv` is SHA-256 over the complete key vector. The implementation then applies the LCG in `accumulate_hash` over context tokens and the layer key.

The actual `get_gvals` implementation performs 12 LCG mixes followed by:

```python
(hash >> 30) % 2
```

The docstring's description of "the lowest three bits" does not match the code.

## Sampling

Only the top-k candidate set is reweighted.

At a high level:

```text
language-model probabilities
        ↓
temperature
        ↓
keyed tournament / g-values
        ↓
slightly reweighted probabilities
        ↓
sample next token
```

Repeated context hashes are masked so they do not add repeated watermark evidence. The first `H` tokens cannot form a complete scored context.

Low temperature concentrates probability on very few candidates and gives the watermark less freedom to steer token choice. Higher temperature gives the tournament more surface to work with.

## Detection

The public implementation contains three related scoring approaches:

| Scorer | Idea | Training |
|---|---|---|
| Mean | average unmasked g-value | none |
| Weighted mean | depth-weighted g-value average | none |
| Bayesian | model `P(w | g)` | per-key training |

For unmarked text:

\[
E[g] = 1/2
\]

With the correct watermark instance, generation biases the observed g-values upward.

This is why a sufficiently long marked sample scores well above 0.50 under the matching keys, while an unrelated key set converges toward 0.50.

## Why the key-free indicator is possible

The official detector projects the text through the keyed g-value function.

Our key-free experiments deliberately throw that projection away and ask a different question:

> Does watermark-biased sampling alter observable token/context frequencies enough to distinguish marked from unmarked generations statistically?

The experiments say yes under the tested matched/repeated conditions.

That does **not** imply that we have reconstructed the keys. See [invertibility.md](invertibility.md).

## Production systems

A production implementation can change the keys, tokenizer, context length, hashing, depth, and detector calibration while still belonging to the same general watermarking family.

So the public DeepMind scorer is a reference implementation, not a universal detector.

This distinction is what motivates the paired key-free experiments.
Keyed detection theory, ZK public verifiability, and stealing sit next
to this measurement in [related-work.md](related-work.md). They do not
replace `indicate`.
