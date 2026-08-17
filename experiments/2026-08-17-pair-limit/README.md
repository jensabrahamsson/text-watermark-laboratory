# 2026-08-17 — GPT-2 CPU limit twins (12 × 700)

Same 12 Grok seeds as the 128-token dress rehearsal. GPT-2 context is 1024; the longest seed (harbour) leaves 747 new tokens, so **700** is the common length that fits every prompt. Mixin on / mixin off / `control-shuffled-30`.

| File | Sampler |
|---|---|
| `*-prompt.txt` | Seed (not stamped) |
| `*-marked.txt` | GPT-2 + public DeepMind 30 |
| `*-unmarked-gen.txt` | GPT-2, mixin off |
| `*-control-gen.txt` | GPT-2 + `control_keys()` (not a `*-marked.txt`; `blind` ignores it) |

## Official lamp (`public-deepmind-30`)

Every marked twin: mean **0.614–0.626**. Every unmarked twin: **≈ 0.50**. **12/12**. n_tokens=700.

## Second instance (`control-shuffled-30`)

`*-control-gen.txt` scored with the public keys: **≈ 0.50**. Same files scored with the matching control keys: **0.614–0.630**. Different instance, not “GPT-2 style”.

Wall clock: 545 s for 12 × 3 generations on this CPU.

Key-free `blind` on the public twins: [../2026-08-17-blind-limit/](../2026-08-17-blind-limit/).
