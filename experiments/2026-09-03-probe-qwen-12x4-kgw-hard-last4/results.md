# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-03-pair-qwen-12x4-kgw context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 8/12 | 0.566 | 19/48 | 31/48 | 0.09195 | 0.0165 |
| interpolate | 12/12 | 0.814 | 35/48 | 33/48 | 0.0004998 | 0.2242 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 8/12 | 2/8 (02-night-bus, 04-market) | 3 (05-kitchen, 07-rain, 09-workshop) |
| interpolate | 12/12 | 1/12 (03-library) | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 19/29 | 17/31 | 0.528 |
| interpolate | 0/48 | 0/48 | 35/13 | 15/33 | 0.700 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 17/48 | 30/48 | -0.0027 | 0.354 | 0.625 |
| interpolate | 40/48 | 29/48 | -0.0787 | 0.833 | 0.604 |

hard auc=0.566 mean_pos=-0.0134 mean_neg=-0.0299 diff=0.0165 pos>0=19/48 neg<=0=31/48 perm_p=0.09195 (file-level, descriptive) binom_p=0.9443 (file-level, descriptive) youden_t=-0.0106 youden_sens=0.521 youden_spec=0.625 J=0.146
hard prompts_marked_above=8/12 ranking_without_isolated_tp=2/8 ranking_losses_with_isolated_tp=3 instance=key-free-counts used_keys=False
interpolate auc=0.814 mean_pos=0.1097 mean_neg=-0.1144 diff=0.2242 pos>0=35/48 neg<=0=33/48 perm_p=0.0004998 (file-level, descriptive) binom_p=0.001044 (file-level, descriptive) youden_t=-0.0800 youden_sens=0.875 youden_spec=0.646 J=0.521
interpolate prompts_marked_above=12/12 ranking_without_isolated_tp=1/12 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
