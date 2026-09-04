# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-distil-100x4-ngram13 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 89/100 | 0.829 | 354/400 | 190/400 | 0.0004998 | 0.3336 |
| interpolate | 88/100 | 0.785 | 325/400 | 232/400 | 0.0004998 | 0.3216 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 89/100 | 0/89 | 10 |
| interpolate | 88/100 | 0/88 | 10 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/400 | 0/400 | 354/46 | 210/190 | 0.628 |
| interpolate | 0/400 | 0/400 | 325/75 | 168/232 | 0.659 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 253/400 | 359/400 | 0.1400 | 0.632 | 0.897 |
| interpolate | 274/400 | 280/400 | 0.1190 | 0.685 | 0.700 |

hard auc=0.829 mean_pos=0.1720 mean_neg=-0.1615 diff=0.3336 pos>0=354/400 neg<=0=190/400 perm_p=0.0004998 (file-level, descriptive) binom_p=2.712e-60 (file-level, descriptive) youden_t=0.1400 youden_sens=0.632 youden_spec=0.902 J=0.535
hard prompts_marked_above=89/100 ranking_without_isolated_tp=0/89 ranking_losses_with_isolated_tp=10 instance=key-free-counts used_keys=False
interpolate auc=0.785 mean_pos=0.2826 mean_neg=-0.0390 diff=0.3216 pos>0=325/400 neg<=0=232/400 perm_p=0.0004998 (file-level, descriptive) binom_p=1.743e-38 (file-level, descriptive) youden_t=0.1317 youden_sens=0.682 youden_spec=0.772 J=0.455
interpolate prompts_marked_above=88/100 ranking_without_isolated_tp=0/88 ranking_losses_with_isolated_tp=10 instance=key-free-interpolate used_keys=False
