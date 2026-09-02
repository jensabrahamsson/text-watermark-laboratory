# Qwen 12×4 opening with include-first

Leave-one-of-12-out on the new Qwen sample. `--fit-prefix 4 --pos-bucket 1
--include-first`. Qwen tokenizer. `used_keys=false`.

| Method | wins | AUC | marked>0 | unmarked≤0 |
|---|---|---|---|---|
| hits / poshits / first | **12/12** | **0.901** | 28/48 | **47/48** |

Full-file Qwen hits was **8/12** (AUC 0.602). The opening first-token
reader ranks every prompt. Isolated t=0 is conservative (28 vs 47).
Do not overwrite the published original-corpus Qwen hashpool 10/12.
Not a GPT-2 → Qwen detector.
