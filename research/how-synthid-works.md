# How SynthID-Text works

Source: the `synthid-text` checkout (Nature reference) plus Nature SI. Not Claude production, not the Gemini app.

## The mark is not in the string

No hidden characters, no metadata. The mark is *which tokens the sampler chose*. A keyed tournament replaces ordinary randomness. Detection asks whether the chosen tokens match binary g-values more often than 1/2.

## Hash → g

Default in the mixin (`DEFAULT_WATERMARKING_CONFIG`):

- `ngram_len = 5` (context \(H=4\))
- 30 public keys: `654, 400, 836, …, 960`
- `context_history_size = 1024`

`hash_iv = SHA-256(all key bytes)` as the start. Then LCG (`accumulate_hash`, multiplier `6364136223846793005`, increment `1`) over n-gram tokens and the layer key. Twelve extra mixes. \(g = (\mathrm{hash} \gg 30) \bmod 2\).

README: the LCG has **no** crypto guarantee. The keys in the reference are public. `hash_iv` depends on the **whole** key vector — you cannot test one key at a time with the right start value.

Docstring vs code: `get_gvals` talks about “the lowest three bits”. The implementation is 12× LCG then `(>> 30) % 2`. Trust the code.

## Sampling

Only top-k is reweighted. Temp first, then the tournament. Two leaves, one layer:

\[
p \leftarrow p\,(1 + g - g_{\mathrm{mass}})
\]

Repeated context hash ⇒ no extra mark. The first \(H\) tokens are not scored.

Low temperature ⇒ mass on 1–2 tokens ⇒ weaker mark. High temp (mixin max **1.0**) ⇒ more surface.

## Detection

All three drop the EOS suffix and already-seen contexts.

| Scorer | What | Training |
|---|---|---|
| Mean | average of unmasked \(g\) | no |
| Weighted mean | weights `linspace(10, 1)` across depth | no |
| Bayesian | \(P(w\mid g)\), \(P(g\mid\neg w)=1/2\) | yes, **per key** |

Unmarked: \(\mathbb{E}[g]=1/2\). One layer, \(N=2\), uniform LM: \(\mathbb{E}[g\mid\mathrm{wm}] \approx 0.5 + 0.25(1-1/|V|)\). More layers add less extra bias (collision entropy).

The README points at `train_detector_bayesian.py`. That file **does not exist**. Use `detector_bayesian.train` / `train_best_detector_given_g_values`.

## Claude vs this code

Anthropic: “a version of” the 2024 method. Unpublished: keys, \(H\), depth, hash, tokenizer, thresholds. Day-one from **2 Aug 2026**. Sonnet 5 / Opus 5 / Fable 5 are older; retrofit “in progress”. No public detector.

This repo’s detector on Claude text is the **wrong instance**, even if the family matches.
