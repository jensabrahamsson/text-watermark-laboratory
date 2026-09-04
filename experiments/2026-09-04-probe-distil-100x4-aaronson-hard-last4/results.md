# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-distil-100x4-aaronson context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 91/100 | 0.899 | 308/400 | 346/400 | 0.0004998 | 1.8595 |
| interpolate | 96/100 | 0.902 | 252/400 | 349/400 | 0.0004998 | 3.6164 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 91/100 | 17/91 | 0 |
| interpolate | 96/100 | 36/96 | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/400 | 0/400 | 308/92 | 54/346 | 0.851 |
| interpolate | 0/400 | 0/400 | 252/148 | 51/349 | 0.832 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 356/400 | 328/400 | -0.5665 | 0.890 | 0.820 |
| interpolate | 368/400 | 340/400 | -2.2707 | 0.920 | 0.850 |

hard auc=0.899 mean_pos=0.9739 mean_neg=-0.8856 diff=1.8595 pos>0=308/400 neg<=0=346/400 perm_p=0.0004998 (file-level, descriptive) binom_p=1.252e-28 (file-level, descriptive) youden_t=-0.5676 youden_sens=0.910 youden_spec=0.823 J=0.732
hard prompts_marked_above=91/100 ranking_without_isolated_tp=17/91 ranking_losses_with_isolated_tp=0 instance=key-free-counts used_keys=False
interpolate auc=0.902 mean_pos=0.3277 mean_neg=-3.2887 diff=3.6164 pos>0=252/400 neg<=0=349/400 perm_p=0.0004998 (file-level, descriptive) binom_p=1.121e-07 (file-level, descriptive) youden_t=-2.2695 youden_sens=0.920 youden_spec=0.853 J=0.772
interpolate prompts_marked_above=96/100 ranking_without_isolated_tp=36/96 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
