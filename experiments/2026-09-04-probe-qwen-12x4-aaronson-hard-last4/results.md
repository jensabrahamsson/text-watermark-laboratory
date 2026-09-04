# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-qwen-12x4-aaronson context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 12/12 | 0.911 | 24/48 | 48/48 | 0.0004998 | 0.6014 |
| interpolate | 12/12 | 0.993 | 12/48 | 48/48 | 0.0004998 | 1.4448 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 12/12 | 6/12 (04-market, 06-station, 07-rain, 08-letter, 09-workshop, 11-garden) | 0 |
| interpolate | 12/12 | 9/12 | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 24/24 | 0/48 | 1.000 |
| interpolate | 0/48 | 0/48 | 12/36 | 0/48 | 1.000 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 36/48 | 47/48 | -0.2050 | 0.750 | 0.979 |
| interpolate | 44/48 | 43/48 | -1.0710 | 0.917 | 0.896 |

hard auc=0.911 mean_pos=0.1032 mean_neg=-0.4982 diff=0.6014 pos>0=24/48 neg<=0=48/48 perm_p=0.0004998 (file-level, descriptive) binom_p=0.5573 (file-level, descriptive) youden_t=-0.2045 youden_sens=0.750 youden_spec=1.000 J=0.750
hard prompts_marked_above=12/12 ranking_without_isolated_tp=6/12 ranking_losses_with_isolated_tp=0 instance=key-free-counts used_keys=False
interpolate auc=0.993 mean_pos=-0.1570 mean_neg=-1.6018 diff=1.4448 pos>0=12/48 neg<=0=48/48 perm_p=0.0004998 (file-level, descriptive) binom_p=0.9999 (file-level, descriptive) youden_t=-1.0126 youden_sens=0.917 youden_spec=1.000 J=0.917
interpolate prompts_marked_above=12/12 ranking_without_isolated_tp=9/12 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
