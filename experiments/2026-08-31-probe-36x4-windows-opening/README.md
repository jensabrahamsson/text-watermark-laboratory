# Opening-token windows: 0:4 vs 4:16 (36×4)

Same last-4 `hits` leave-one-out as
[`../2026-08-31-probe-36x4-windows/`](../2026-08-31-probe-36x4-windows/).
`--windows` scores each slice of a **full-file** table. `used_keys=false`.

| Window | Prompt wins | Isolated marked `lr > 0` | Unmarked `≤ 0` | AUC |
|---|---|---|---|---|
| **0:4** | **34/36** | 129/144 | 92/144 | **0.917** |
| 0:16 | **34/36** | 129/144 | 93/144 | **0.916** |
| 4:16 | 29/36 | 99/144 | 74/144 | 0.712 |
| 16:32 | 22/36 | 74/144 | 71/144 | 0.549 |

The 16-token prefix ranking **is** the first four tokens. Coverage
([`../2026-08-31-probe-36x4-coverage/`](../2026-08-31-probe-36x4-coverage/))
shows why: positions 1–2 are almost always shared last-1 / last-2.
Tokens 4–16 still rank above the next 16 tokens, but they do not move
prompt grain.

Out of family, 0:4 matches 0:16 at **11/12** / AUC **0.752**:
[`../2026-08-31-transfer-36x4-to-12x4-windows-opening/`](../2026-08-31-transfer-36x4-to-12x4-windows-opening/).
A **matched** 4-token fit with position buckets is a different protocol:
[`../2026-08-31-probe-36x4-fitprefix4-pos1/`](../2026-08-31-probe-36x4-fitprefix4-pos1/).
