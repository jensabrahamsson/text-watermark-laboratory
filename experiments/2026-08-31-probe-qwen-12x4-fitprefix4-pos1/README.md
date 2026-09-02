# Qwen 12×4 opening without include-first

Same twins as the include-first run, but token 0 is skipped by hits.
`--methods first` still scores token 0 from the stored sentinel bucket.

| Method | wins | AUC | marked>0 | unmarked≤0 |
|---|---|---|---|---|
| hits / poshits | 7/12 | 0.576 | 15/48 | 38/48 |
| **first** | **12/12** | **0.901** | 28/48 | **47/48** |

Qwen's key-free opening signal **is generated token 0**. Hits on
tokens 1–3 of a 4-token prefix is near the full-file 8/12. Include
token 0 and hits matches first.
