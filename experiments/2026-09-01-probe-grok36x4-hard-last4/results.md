# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-09-01-pair-grok36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| interpolate | 35/36 | 0.823 | 114/144 | 98/144 | 0.0004998 | 0.3196 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| interpolate | 35/36 | 0/35 | 1 (222-warehouse-shift) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| interpolate | 0/144 | 0/144 | 114/30 | 46/98 | 0.713 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| interpolate | 93/144 | 110/144 | 0.0769 | 0.646 | 0.764 |

interpolate auc=0.823 mean_pos=0.2320 mean_neg=-0.0876 diff=0.3196 pos>0=114/144 neg<=0=98/144 perm_p=0.0004998 binom_p=4.966e-13 youden_t=0.0484 youden_sens=0.750 youden_spec=0.771 J=0.521
interpolate prompts_marked_above=35/36 ranking_without_isolated_tp=0/35 ranking_losses_with_isolated_tp=1 instance=key-free-interpolate used_keys=False
