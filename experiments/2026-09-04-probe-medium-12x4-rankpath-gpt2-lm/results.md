# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-09-01-pair-gpt2-medium-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 8/12 | 0.619 | 20/48 | 32/48 | 0.002999 | 0.3329 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| rankpath | 8/12 | 1/8 (08-letter) | 1 (05-kitchen) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 20/28 | 16/32 | 0.556 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| rankpath | 17/48 | 47/48 | 0.7843 | 0.354 | 0.979 |

rankpath auc=0.619 mean_pos=0.1101 mean_neg=-0.2228 diff=0.3329 pos>0=20/48 neg<=0=32/48 perm_p=0.002999 (file-level, descriptive) binom_p=0.9033 (file-level, descriptive) youden_t=0.7888 youden_sens=0.354 youden_spec=1.000 J=0.354
rankpath prompts_marked_above=8/12 ranking_without_isolated_tp=1/8 ranking_losses_with_isolated_tp=1 instance=key-free-rankpath used_keys=False
