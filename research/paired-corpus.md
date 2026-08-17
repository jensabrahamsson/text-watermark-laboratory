# Paired corpus: before / after marking

The lab should see whether T is marked. Without a key you need **the same input twice**.

The mixin dress rehearsal — GPT-2 with/without the public mark, official 12/12, key-free 8/12 — is [key-free-twins.md](key-free-twins.md). This file is the Claude application of that protocol.

## Theory

1. **Before** (now): save `(prompt, Claude-output)` while Sonnet 5 / pre-2-Aug models are not day-one marked and retrofit is not announced.
2. **After**: the same `prompt` list against a model they *say* is marked (a new model from 2 Aug 2026, or an announced retrofit of the same family).
3. Estimate a **surrogate** of how sampling changes: not `keys` / `hash_iv`, but roughly `P(token | context)` marked minus unmarked.

That is presence plus a coarse green/red map. Not an official Anthropic score.

## What works / does not

Works, if the pairs are clean:

- A classifier `(prompt, output) → marked?` that beats style.
- Per context: tokens that become more common after the mark ≈ an approximate green list.
- The same protocol as known-mark against the mixin, but the ground truth is “they turned the mark on”, not our public keys.

Does not work:

- Recovering the integers or the SHA-256 IV.
- A pile of “lots of Claude” without an unmarked twin — that is only style.
- Comparing Sonnet 5-now to a **different** model later. That mixes a model change with the mark. A clean pair = **the same model-id** before/after retrofit, or at least the same family + the same prompt list + the same temp/length.

## What must be saved now

Each row:

- `prompt` (exact string to run again)
- `output`
- `model_claimed` / UI default
- `collected_at`
- `assumed_watermark: false`
- surface (`claude.ai`)

Live in `experiments/claude-premark-2026-08/` + `manifest.jsonl`.
Prompt list for new collection: `scripts/collect_claude_premark.py` (`PROMPTS`). Do not change those strings later; add new ones. `collect` skips prompts already in the manifest.

Existing T′ from 15 Aug are **bad pairs** for step 2: the input was watermarked GPT-2, not a clean prompt. Keep them as extra Claude prose, not as the A/B core.

## When “after” exists

Same `PROMPTS` → new directory `experiments/claude-mark-<date>/`.
Compare n-gram / next-token frequency. Threshold: more than style (control: shuffle unmarked-unmarked).

Until then: collect. Do not train a “Claude detector” on pre-mark only.

Mixin twins (known key, to *practice* the key-free question) live in `experiments/2026-08-17-blind-pairs/`. Numbers and how to rerun: [key-free-twins.md](key-free-twins.md). That is not Claude.
