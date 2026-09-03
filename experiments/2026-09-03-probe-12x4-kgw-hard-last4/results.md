# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-03-pair-12x4-kgw context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 12/12 | 0.703 | 35/48 | 25/48 | 0.0004998 | 0.0696 |
| interpolate | 12/12 | 0.947 | 44/48 | 41/48 | 0.0004998 | 0.4367 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 12/12 | 0/12 | 0 |
| interpolate | 12/12 | 0/12 | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 35/13 | 23/25 | 0.603 |
| interpolate | 0/48 | 0/48 | 44/4 | 7/41 | 0.863 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 30/48 | 30/48 | 0.0256 | 0.625 | 0.625 |
| interpolate | 42/48 | 42/48 | 0.0068 | 0.875 | 0.875 |

hard auc=0.703 mean_pos=0.0596 mean_neg=-0.0100 diff=0.0696 pos>0=35/48 neg<=0=25/48 perm_p=0.0004998 (file-level, descriptive) binom_p=0.001044 (file-level, descriptive) youden_t=0.0290 youden_sens=0.625 youden_spec=0.729 J=0.354
hard prompts_marked_above=12/12 ranking_without_isolated_tp=0/12 ranking_losses_with_isolated_tp=0 instance=key-free-counts used_keys=False
interpolate auc=0.947 mean_pos=0.2717 mean_neg=-0.1650 diff=0.4367 pos>0=44/48 neg<=0=41/48 perm_p=0.0004998 (file-level, descriptive) binom_p=7.569e-10 (file-level, descriptive) youden_t=0.0059 youden_sens=0.917 youden_spec=0.896 J=0.812
interpolate prompts_marked_above=12/12 ranking_without_isolated_tp=0/12 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
