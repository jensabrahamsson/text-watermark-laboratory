# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=['0:2', '0:4', '0:8', '2:128', '4:128', '8:128'] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 9/12 | 0.590 | 25/48 | 22/48 | 0.04048 | 0.0251 |
| interpolate | 7/12 | 0.525 | 24/48 | 24/48 | 0.3708 | 0.0129 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 9/12 | 1/9 (11-garden) | 3 (06-station, 10-office, 12-ferry-queue) |
| interpolate | 7/12 | 0/7 | 4 (04-market, 06-station, 07-rain, 08-letter) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 25/23 | 26/22 | 0.490 |
| interpolate | 0/48 | 0/48 | 24/24 | 24/24 | 0.500 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 39/48 | 21/48 | -0.0311 | 0.812 | 0.438 |
| interpolate | 20/48 | 35/48 | 0.0674 | 0.417 | 0.729 |

| window tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 0:2 | hard | 10/12 | 0.689 | 35/48 | 24/48 |
| 0:2 | interpolate | 9/12 | 0.704 | 25/48 | 42/48 |
| 0:4 | hard | 5/12 | 0.540 | 25/48 | 28/48 |
| 0:4 | interpolate | 9/12 | 0.630 | 17/48 | 46/48 |
| 0:8 | hard | 6/12 | 0.596 | 27/48 | 35/48 |
| 0:8 | interpolate | 8/12 | 0.659 | 27/48 | 37/48 |
| 2:128 | hard | 9/12 | 0.567 | 35/48 | 20/48 |
| 2:128 | interpolate | 5/12 | 0.494 | 21/48 | 17/48 |
| 4:128 | hard | 9/12 | 0.589 | 37/48 | 17/48 |
| 4:128 | interpolate | 5/12 | 0.474 | 13/48 | 29/48 |
| 8:128 | hard | 9/12 | 0.561 | 35/48 | 19/48 |
| 8:128 | interpolate | 4/12 | 0.435 | 14/48 | 26/48 |

hard auc=0.590 mean_pos=0.0232 mean_neg=-0.0019 diff=0.0251 pos>0=25/48 neg<=0=22/48 perm_p=0.04048 (file-level, descriptive) binom_p=0.4427 (file-level, descriptive) youden_t=-0.0305 youden_sens=0.812 youden_spec=0.458 J=0.271
hard prompts_marked_above=9/12 ranking_without_isolated_tp=1/9 ranking_losses_with_isolated_tp=3 instance=key-free-counts used_keys=False
interpolate auc=0.525 mean_pos=0.0037 mean_neg=-0.0092 diff=0.0129 pos>0=24/48 neg<=0=24/48 perm_p=0.3708 (file-level, descriptive) binom_p=0.5573 (file-level, descriptive) youden_t=0.0676 youden_sens=0.417 youden_spec=0.750 J=0.167
interpolate prompts_marked_above=7/12 ranking_without_isolated_tp=0/7 ranking_losses_with_isolated_tp=4 instance=key-free-interpolate used_keys=False
