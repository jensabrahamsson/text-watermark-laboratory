# DistilGPT2 12×4 in-domain last-4

Leave-one-of-12-out. DistilGPT2 tokenizer (GPT-2 BPE). `used_keys=false`.

| Method | wins | AUC | marked>0 | unmarked≤0 |
|---|---|---|---|---|
| hits | 9/12 | 0.705 | 33/48 | 27/48 |
| hashpool | 9/12 | **0.754** | 27/48 | 39/48 |
| poshits bucket 16 | 10/12 | 0.605 | 27/48 | 25/48 |

Official lamp is 12/12. Key-free is real and weaker than GPT-2 12×4
hits 11/12 / 0.737. Extra topics were not generated for Distil.
