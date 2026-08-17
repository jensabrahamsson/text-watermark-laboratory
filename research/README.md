# Research

Background notes. The current findings live in the root [README.md](../README.md).

| File | Question |
|---|---|
| [HOW-TO.md](../HOW-TO.md) | Install, score a file, read the line. Start here if you are new |
| [key-free-twins.md](key-free-twins.md) | Same prompt, mixin on vs off. Official 12/12; key-free 8/12 — idea looks promising |
| [how-synthid-works.md](how-synthid-works.md) | Hash, g, sampling, the three scorers. The docstring lies; trust the code |
| [invertibility.md](invertibility.md) | You cannot recover a key/IV from a string. More text + wrong key = a more confident 0.50 |
| [claude.md](claude.md) | Day-one 2 Aug 2026. Sonnet 5 = 30 Jun. No public detector |
| [paired-corpus.md](paired-corpus.md) | Same protocol for Claude: save prompts now, rerun after announced marking |
| [dipper-local.md](dipper-local.md) | No 7B. 11B ~45 GB / 40 GB GPU. Do not download |

Key-free path: twins, then a next-token table. Not `keys` / `hash_iv`. Not an official Anthropic score.
