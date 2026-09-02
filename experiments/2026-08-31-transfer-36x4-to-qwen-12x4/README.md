# GPT-2 36×4 → new Qwen 12×4 (drop overlapping stems)

Train on the 24 new GPT-2 36-prompt stems × 4 draws. Test on
[`../2026-08-31-pair-qwen-12x4/`](../2026-08-31-pair-qwen-12x4/)
(Qwen2-1.5B-Instruct, same 12 stems as the original 12×4, four draws).
`--overlap drop-from-train`. Token methods retokenize Qwen text with
GPT-2 BPE. Nested train-LOO was skipped (`nested=false`).

## Result

| Method | Prompts marked > unmarked | Isolated marked `lr > 0` | Unmarked `lr ≤ 0` | AUC |
|---|---|---|---|---|
| Official `score` (Qwen test, first draws) | **12/12** | — | — | keyed reference |
| Hits last-4 | 6/12 | 25/48 | 23/48 | 0.445 |
| Hashpool 64 | 3/12 | 8/48 | 37/48 | 0.447 |
| Surface bytes | 6/12 | 0/48 | 48/48 | 0.461 |

New topics plus a second generator stay at chance even with four GPT-2
training draws and a tokenizer-free surface table. Extra GPT-2 data does
not create a Qwen detector. Hashpool's 3/12 prompt grain is *below*
chance; do not salvage it.

Do not overwrite the published original-corpus Qwen hashpool **10/12**
(AUC 0.750). That number is tied to that Qwen sample.
