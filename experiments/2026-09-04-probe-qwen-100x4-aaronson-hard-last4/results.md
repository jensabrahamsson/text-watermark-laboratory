# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-qwen-100x4-aaronson context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 97/100 | 0.949 | 268/400 | 397/400 | 0.0004998 | 0.6642 |
| interpolate | 100/100 | 0.999 | 216/400 | 400/400 | 0.0004998 | 2.5882 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 97/100 | 30/97 | 0 |
| interpolate | 100/100 | 46/100 | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/400 | 0/400 | 268/132 | 3/397 | 0.989 |
| interpolate | 0/400 | 0/400 | 216/184 | 0/400 | 1.000 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 364/400 | 354/400 | -0.1126 | 0.910 | 0.885 |
| interpolate | 388/400 | 389/400 | -1.2869 | 0.970 | 0.973 |

hard auc=0.949 mean_pos=0.3305 mean_neg=-0.3337 diff=0.6642 pos>0=268/400 neg<=0=397/400 perm_p=0.0004998 (file-level, descriptive) binom_p=4.7e-12 (file-level, descriptive) youden_t=-0.1126 youden_sens=0.910 youden_spec=0.887 J=0.797
hard prompts_marked_above=97/100 ranking_without_isolated_tp=30/97 ranking_losses_with_isolated_tp=0 instance=key-free-counts used_keys=False
interpolate auc=0.999 mean_pos=0.5401 mean_neg=-2.0482 diff=2.5882 pos>0=216/400 neg<=0=400/400 perm_p=0.0004998 (file-level, descriptive) binom_p=0.06052 (file-level, descriptive) youden_t=-1.2938 youden_sens=1.000 youden_spec=0.975 J=0.975
interpolate prompts_marked_above=100/100 ranking_without_isolated_tp=46/100 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
