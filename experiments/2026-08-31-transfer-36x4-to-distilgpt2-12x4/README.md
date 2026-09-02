# GPT-2 36×4 → DistilGPT2 12×4 (same tokenizer, negative)

Train 24 new GPT-2 stems, score DistilGPT2 12×4. Same BPE as GPT-2.
Overlapping stems dropped. Frozen count tables omitted (large).
`used_keys=false`.

| Method | Prompt wins | File AUC | t=0 |
|---|---|---|---|
| hits | 5/12 | **0.462** | 25/48 vs 19/48 |
| hashpool | 9/12 | 0.615 | 20/48 vs 38/48 |
| poshits | 9/12 | 0.585 | 18/48 vs 29/48 |

Same keys, same ngram_len, same tokenizer. Hits does **not** transfer.
The 4-gram footprint is generator-weight specific, not a universal
public-key fingerprint. Hashpool ranking is weak (perm p ≈ 0.013).
Distil in-domain still has its own 9/12. Not a 12/12 detector.
