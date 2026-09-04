# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-qwen-100x4-kgw context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=['0:4', '4:16', '16:32', '32:64', '64:128'] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| interpolate | 96/100 | 0.870 | 346/400 | 274/400 | 0.0004998 | 0.4862 |
| hard | 63/100 | 0.562 | 290/400 | 140/400 | 0.0004998 | 0.0638 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| interpolate | 96/100 | 0/96 | 4 (017, 045, 069, 071) |
| hard | 63/100 | 2/63 (003, 081) | 37 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| interpolate | 0/400 | 0/400 | 346/54 | 126/274 | 0.733 |
| hard | 0/400 | 0/400 | 290/110 | 260/140 | 0.527 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| interpolate | 316/400 | 339/400 | 0.1091 | 0.790 | 0.848 |
| hard | 332/400 | 118/400 | -0.0554 | 0.830 | 0.295 |

| window tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 0:4 | interpolate | 84/100 | 0.679 | 272/400 | 237/400 |
| 0:4 | hard | 74/100 | 0.642 | 221/400 | 249/400 |
| 4:16 | interpolate | 79/100 | 0.665 | 280/400 | 191/400 |
| 4:16 | hard | 49/100 | 0.493 | 347/400 | 59/400 |
| 16:32 | interpolate | 88/100 | 0.749 | 244/400 | 318/400 |
| 16:32 | hard | 50/100 | 0.530 | 266/400 | 150/400 |
| 32:64 | interpolate | 92/100 | 0.752 | 290/400 | 259/400 |
| 32:64 | hard | 69/100 | 0.590 | 240/400 | 183/400 |
| 64:128 | interpolate | 97/100 | 0.785 | 268/400 | 280/400 |
| 64:128 | hard | 58/100 | 0.555 | 363/400 | 85/400 |

interpolate auc=0.870 mean_pos=0.3006 mean_neg=-0.1857 diff=0.4862 pos>0=346/400 neg<=0=274/400 perm_p=0.0004998 (file-level, descriptive) binom_p=1.517e-53 (file-level, descriptive) youden_t=0.1091 youden_sens=0.790 youden_spec=0.850 J=0.640
interpolate prompts_marked_above=96/100 ranking_without_isolated_tp=0/96 ranking_losses_with_isolated_tp=4 instance=key-free-interpolate used_keys=False
hard auc=0.562 mean_pos=0.0373 mean_neg=-0.0265 diff=0.0638 pos>0=290/400 neg<=0=140/400 perm_p=0.0004998 (file-level, descriptive) binom_p=4.143e-20 (file-level, descriptive) youden_t=-0.0554 youden_sens=0.830 youden_spec=0.300 J=0.130
hard prompts_marked_above=63/100 ranking_without_isolated_tp=2/63 ranking_losses_with_isolated_tp=37 instance=key-free-counts used_keys=False
