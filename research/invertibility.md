# Can you work backwards?

Short: **not from a text.** Not the keys, not the SHA-256 IV, not the official green/red partition.

## What recovering a key would mean

`detector_mean` needs the same keys and the same n-gram window as at generation. Without that there are no g-values to invert. The theory models the hash as a PRF and does not claim that \(k\) sits in the string.

## Where the bias lives

More text makes a biased coin clearer **if you know which side is heads**. The key *is* that definition.

Raw text / unigrams are deliberately almost unbiased (that is why quality holds). The projection

```text
tokens → [IV from ALL keys] → n-gram hash → layer key → 1 bit
```

gives \(\mathbb{E}[g]\approx 0.53\text{–}0.62\) with the right key and \(0.50\) with the wrong key. More text + wrong key gives a *more confident* 0.50.

`hash_iv` is SHA-256 of the **entire** key list. Wrong IV ⇒ other bits. Searching one key with the right start requires that you already have all the keys.

## What does not work (static text)

No reviewed source shows:

- algebraic inversion of `accumulate_hash`
- a SHA-256 preimage of `hash_iv`
- recovery of secret keys from tokens alone

Neither the IV nor the keys are written into the token stream.

The LCG has no crypto guarantee. That is not the same as “so we can solve \(k\) from an essay”. Production hashes (Gemini app, Claude) can also be a different function. Hugging Face’s processor starts from ones + a sampling table and says explicitly that that hash differs from the Gemini app.

## What published methods do instead

They **query a marked generator many times** and estimate context-dependent rules. That does not give this repo’s `detector_mean` and not the integers in `keys`. Published notes (ETH blog, layer-count papers) report that kind of estimate. They are not Claude figures and not a method we ship.

Putting a fake mark on human text is a different goal and is out of scope.

## Claude text specifically

A paste gives the wrong tokenizer, unknown hash, unknown \(H\), unknown IV, and the text may not even be marked (Sonnet 5 is before the 2 Aug cutoff). A key that happens to give mean > 0.5 on *your* pasted text is almost certainly a false hit.

“Improve T” isolates Claude’s *choices*, but those choices are almost only style. \(\varepsilon\) in g-space drowns in the model prior. Low temp on T makes the mark *weaker*.

## What we *can* compute

The reference keys are public. Then there is nothing to invert — we score. We did that on 2026-08-15. See [experiments/2026-08-15-gpt2-sonnet5/](../experiments/2026-08-15-gpt2-sonnet5/).

When we *pretend* the keys are unknown, we do not invert them either. We generate the same prompt with the mixin on and off, and fit token counts. That run: [key-free-twins.md](key-free-twins.md). `detector_mean` 12/12; key-free `blind` 8/12.
