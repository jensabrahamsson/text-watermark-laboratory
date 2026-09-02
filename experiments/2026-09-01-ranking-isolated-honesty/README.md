# Ranking vs isolated-file honesty (frozen holdouts)

Not a new `probe --methods` name. Derived from already-saved holdout
JSON via `IndicatorHoldout.ranking_without_isolated_tp` and
`ranking_losses_with_isolated_tp`. The 9/12 producer (`blind`) now
stores the same per-file split. Live JSON:
`../2026-09-01-blind-12x4-ranking-honesty/`. `used_keys=false`.

Prompt-group ranking and isolated `lr>0` are different grains. This
table names the stems where they disagree.

**12-LOO hard last-4 (headline 9/12, isolated 25/48).** Garden ranks
with **0/4** marked files above 0. Station, office, and ferry-queue
*lose* ranking but still hold **5** of the **25** isolated TPs
(ferry-queue 3/4). Do not rewrite **9/12** or **25/48**.

**100→12 lock C.** Three ranking wins (night-bus, library, market) have
no isolated TP. Zero isolated TPs on ranking losses. Prompt **10/12**
is inflated relative to isolated **24/48**.

**100→12 lock A.** No hidden ranking wins. Four isolated TPs sit on
ranking losses (harbour, night-bus, library). Nested Youden **23/48**
still does not beat **25/48**.

See `readout.json`.
