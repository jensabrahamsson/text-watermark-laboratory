# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-03-pair-100x4-kgw context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 62/100 | 0.573 | 209/400 | 231/400 | 0.0004998 | 0.0298 |
| interpolate | 100/100 | 0.982 | 376/400 | 371/400 | 0.0004998 | 0.7450 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 62/100 | 0/62 | 33 |
| interpolate | 100/100 | 0/100 | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/400 | 0/400 | 209/191 | 169/231 | 0.553 |
| interpolate | 0/400 | 0/400 | 376/24 | 29/371 | 0.928 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 190/400 | 245/400 | 0.0119 | 0.475 | 0.613 |
| interpolate | 368/400 | 379/400 | 0.0498 | 0.920 | 0.948 |

hard auc=0.573 mean_pos=0.0047 mean_neg=-0.0250 diff=0.0298 pos>0=209/400 neg<=0=231/400 perm_p=0.0004998 (file-level, descriptive) binom_p=0.1977 (file-level, descriptive) youden_t=0.0121 youden_sens=0.485 youden_spec=0.632 J=0.117
hard prompts_marked_above=62/100 ranking_without_isolated_tp=0/62 ranking_losses_with_isolated_tp=33 instance=key-free-counts used_keys=False
interpolate auc=0.982 mean_pos=0.4184 mean_neg=-0.3266 diff=0.7450 pos>0=376/400 neg<=0=371/400 perm_p=0.0004998 (file-level, descriptive) binom_p=9.279e-83 (file-level, descriptive) youden_t=0.0495 youden_sens=0.927 youden_spec=0.950 J=0.877
interpolate prompts_marked_above=100/100 ranking_without_isolated_tp=0/100 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
