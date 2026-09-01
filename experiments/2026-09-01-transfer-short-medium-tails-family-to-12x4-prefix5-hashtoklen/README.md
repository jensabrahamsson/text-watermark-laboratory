# 60-stem prefix-5 exact-length hashed backoff → 12×4

Same train as prefix-5 `hashtok`. `hashtoklen` hashes only last-4 of
length 4 (official 5-gram grain). `hashtoklenbackoff` fits per-order
tables the same way: order-k is used only when the context has k
tokens. Short prefixes are not mixed into a longer-order mixer.
`used_keys=false`.

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashtok | 9/12 | 0.761 | **30/48** | 36/48 | 26/48 vs 42/48 | 0.714 |
| **hashtoklen** | **12/12** | 0.701 | **21/48** | 45/48 | **21/48 vs 45/48** | 0.875 |
| **hashtoklenbackoff** | 11/12 | 0.822 | **36/48** | 34/48 | **33/48 vs 42/48** | 0.720 |
| **hashtoklenbackoff2** | 10/12 | 0.769 | **36/48** | 35/48 | **28/48 vs 43/48** | 0.735 |
| postokbackoff2 | 12/12 | 0.642 | 15/48 | 46/48 | 15/48 vs 46/48 | 0.882 |

`hashtoklen` scores only the official 5-gram slot. 27 marked files
abstain. That 21/48 is not a denser isolated-file reader.

Letter d2 official 5-gram `I` is still unseen as a 4-gram
(`hashtoklen` `n_used=0`). Exact backoff2 lr=0.797 is last-2
`'Now in' → ' the'`, not token 4. Including last-1 of `I` (unmarked,
δ=−1.10) dilutes hashtoklenbackoff to −0.152. Library ×4 survive as
a legal last-3 `'Cl' 'osing' ' is' → ' the'` hashed hit, not the
illegal order-4-at-i=3 collision. Letter d3's collision extra is
gone (lr=−1.37).

Nested Youden **33/48** is the honest isolated-file number for
exact hashed backoff. Do not sell 36/48 or 33/48 as beating poshits
**39/48** or replacing **29/48**.

JSON: `exact-order-trace.json`. Write-up:
[../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
