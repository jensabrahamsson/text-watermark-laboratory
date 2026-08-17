# 2026-08-17 — key-free last-4 on 12×4 GPT-2 samples

Twins: [../2026-08-17-pair-12x4/](../2026-08-17-pair-12x4/). Four draws per prompt, leave-one-*prompt*-out, `context_len=4`, no backoff. **10/12**.

Misses: station, office. `used_keys=false`.

Last-2 and last-3 on the same files are also 10/12. Last-1 collapses to 1/12 (style). Four samples were enough for the watermark window (H=4) to have reuse.
