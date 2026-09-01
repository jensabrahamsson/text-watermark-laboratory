# Results ledger

This is an index, not a fourth detector. Headlines stay **10/12**,
**29/48**, **36/36**. Exploratory ablations live under
[../experiments/README.md](../experiments/README.md). The next
measurement is [PROTOCOL-next.md](PROTOCOL-next.md), not another scorer
on the old 12×4 twins.

## Locked headlines

| Claim | Grain | Number | Not |
|---|---|---|---|
| Key-free last-4 count tables | Held-out prompt groups | **10/12** | Single-file accuracy |
| Same scorer, 0.02 margin | Same groups | 11/12 | The main result |
| Isolated hard sign | One marked file, `lr>0` | **29/48** | A 5% binomial test |
| In-domain 36×4 hits | Prompt groups | **36/36** | Cross-generator |

Official public-key `score` on those twins is **12/12**. That path uses
keys. It is the positive control, not the key-free indicator.

## Mechanistic finding already on the old corpus

The in-domain mark is front-loaded. A 16-token prefix already ranks
**34/36**. Scoring **0:4** matches that ranking. Window **16:32** is
near chance. Matching mixin `ngram_len=5` (`context_len=5`) does not
beat last-4. Opening occupancy (Laplace on unseen next tokens) inflates
poshits **39/48**; `postokhits` keeps observed tokens only (**16/48**
on that split).

## Occupancy-free hashing on 12×4 is closed

`hashtok` is occupancy-free hashpool, not SynthID's hash. Mixer width,
mixer seed, and last-k are knobs, not a denser isolated-file detector.

| Axis | What happened | Keep |
|---|---|---|
| Width `--n-hashes` | n=2/4 beat n=8 in-domain; n=8 won 24→12 at seed 20260831 | `n_hashes=8` |
| Seed | n=2 spec 21–31/48; transfer n=8 is also lucky | seed `20260831` |
| Order `--context-len` | last-1 chance; last-3 11/12 with t=0 24/48; transfer last-4 still wins nested FPR10 | `context_len=4` |

Do not sell 36/48, 35/48, 34/48, 33/48, 24/48, 19/48, 18/48, or 17/48
as replacing **29/48**. Write-up:
[key-free-hashtok.md](key-free-hashtok.md).

## Where the other numbers are

Instance contrast, tokhits, rankpath, cascade, and transfer tables are
not copied here. Start from [key-free-twins.md](key-free-twins.md) and
the experiment index. Neighbours of the measurement, with author–year
citations, are [related-work.md](related-work.md).
