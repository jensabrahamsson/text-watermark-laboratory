# Why the key-free indicator is not key recovery

The laboratory can infer **watermark-like statistical structure without the keys**. That should not be confused with recovering the keys themselves.

## What the official detector needs

DeepMind's `detector_mean` evaluates g-values generated from:

```text
tokens
  → IV derived from the complete key vector
  → context hash
  → layer key
  → binary g-value
```

To reproduce the official detector, you need the same watermark configuration used during generation.

The finished text does not contain the key vector or SHA-256 IV as an embedded field.

## More text does not reveal a wrong key

There is a useful analogy with a biased coin.

If you know which outcome the watermark calls "1", more observations make the bias clearer. The key defines that mapping.

With the wrong mapping, more text does not gradually reveal the right one. It instead gives a more stable estimate near chance.

That is exactly what makes the public reference scorer specific to its own instance.

## What our key-free method does instead

We do **not** try to invert the hash or solve for the public key integers.

We learn observable distributional differences from paired data:

```text
same prompt
  ├── watermark off → unmarked distribution
  └── watermark on  → marked distribution
```

From those samples we estimate token/context tendencies and calculate a likelihood ratio for held-out text.

This is a surrogate for **presence**, not a reconstruction of the official detector.

## Static text vs generator access

A single static paragraph gives far less information than repeated access to a marked generator.

Published attacks on statistical watermarks typically exploit many generated samples to estimate context-dependent preferences. That is a different problem from algebraically recovering the secret state from one string.

The experiments in this repository stay on the inference side: can enough paired observations reveal a usable statistical signature?

Current answer: **yes, at matched/repeated prompt grain; much less reliably for one isolated file.** The key-free opening-token reader is **instance-specific** on this mixin (control-shuffled-30 isolated `lr>0` is **0/48** under 4-token poshits) without recovering keys. See [key-free-contrast.md](key-free-contrast.md).

See [key-free-twins.md](key-free-twins.md).
