# 2026-08-17 — Qwen2-1.5B-Instruct twins (local)

Same 12 Grok seeds. Generator: **Qwen/Qwen2-1.5B-Instruct** on CPU with the SynthID mixin (our `KeyedSynthIDQwen2`, not a DashScope call). Score uses the **Qwen tokenizer**.

| File | Sampler |
|---|---|
| `*-marked.txt` | Qwen2 + public DeepMind 30 |
| `*-unmarked-gen.txt` | Qwen2, mixin off |

## Official lamp

Marked means **0.577–0.638**. Unmarked **≈ 0.48–0.51**. **12/12**. n_tokens=128. Wall clock 459 s.

The mixin tournament is not GPT-2-specific. Same keys, different model and tokenizer, lamp still splits.

`score` / `blind` on this dir need `--model Qwen/Qwen2-1.5B-Instruct`.

Key-free: [../2026-08-17-blind-qwen/](../2026-08-17-blind-qwen/).
