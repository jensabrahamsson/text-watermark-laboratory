# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-03-pair-distil-12x4-kgw context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 11/12 | 0.780 | 34/48 | 32/48 | 0.0004998 | 0.0936 |
| interpolate | 12/12 | 0.947 | 42/48 | 43/48 | 0.0004998 | 0.5042 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 11/12 | 0/11 | 1 (07-rain) |
| interpolate | 12/12 | 0/12 | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 34/14 | 16/32 | 0.680 |
| interpolate | 0/48 | 0/48 | 42/6 | 5/43 | 0.894 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 31/48 | 25/48 | -0.0216 | 0.646 | 0.521 |
| interpolate | 41/48 | 43/48 | 0.0173 | 0.854 | 0.896 |

hard auc=0.780 mean_pos=0.0462 mean_neg=-0.0474 diff=0.0936 pos>0=34/48 neg<=0=32/48 perm_p=0.0004998 (file-level, descriptive) binom_p=0.002758 (file-level, descriptive) youden_t=-0.0621 youden_sens=0.958 youden_spec=0.458 J=0.417
hard prompts_marked_above=11/12 ranking_without_isolated_tp=0/11 ranking_losses_with_isolated_tp=1 instance=key-free-counts used_keys=False
interpolate auc=0.947 mean_pos=0.2575 mean_neg=-0.2466 diff=0.5042 pos>0=42/48 neg<=0=43/48 perm_p=0.0004998 (file-level, descriptive) binom_p=5.044e-08 (file-level, descriptive) youden_t=0.0182 youden_sens=0.875 youden_spec=0.917 J=0.792
interpolate prompts_marked_above=12/12 ranking_without_isolated_tp=0/12 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
