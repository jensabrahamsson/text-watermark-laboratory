# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-08-31-pair-distilgpt2-12x4 context_len=4 model=distilgpt2 max_draws=None prefix_lens=[] windows=['4:16'] fit_prefix=16 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 9/12 | 0.621 | 26/48 | 26/48 | 0.02149 | 0.1009 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| rankpath | 9/12 | 0/9 | 2 (07-rain, 09-workshop) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 26/22 | 22/26 | 0.542 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| rankpath | 35/48 | 19/48 | -0.1220 | 0.729 | 0.396 |

| window tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 4:16 | rankpath | 9/12 | 0.630 | 33/48 | 21/48 |

rankpath auc=0.621 mean_pos=0.0394 mean_neg=-0.0616 diff=0.1009 pos>0=26/48 neg<=0=26/48 perm_p=0.02149 (file-level, descriptive) binom_p=0.3327 (file-level, descriptive) youden_t=-0.1091 youden_sens=0.750 youden_spec=0.479 J=0.229
rankpath prompts_marked_above=9/12 ranking_without_isolated_tp=0/9 ranking_losses_with_isolated_tp=2 instance=key-free-rankpath used_keys=False
