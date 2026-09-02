# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-09-01-pair-100x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=['0:4', '4:16', '16:32', '32:64'] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| interpolate | 99/100 | 0.898 | 352/400 | 290/400 | 0.0004998 | 0.5201 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| interpolate | 99/100 | 0/99 | 1 (088) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| interpolate | 0/400 | 0/400 | 352/48 | 110/290 | 0.762 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| interpolate | 322/400 | 338/400 | 0.0876 | 0.805 | 0.845 |

| window tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 0:4 | interpolate | 99/100 | 0.885 | 361/400 | 311/400 |
| 4:16 | interpolate | 94/100 | 0.803 | 253/400 | 361/400 |
| 16:32 | interpolate | 87/100 | 0.695 | 215/400 | 313/400 |
| 32:64 | interpolate | 85/100 | 0.680 | 187/400 | 320/400 |

interpolate auc=0.898 mean_pos=0.4027 mean_neg=-0.1174 diff=0.5201 pos>0=352/400 neg<=0=290/400 perm_p=0.0004998 (file-level, descriptive) binom_p=1.513e-58 (file-level, descriptive) youden_t=0.0889 youden_sens=0.815 youden_spec=0.865 J=0.680
interpolate prompts_marked_above=99/100 ranking_without_isolated_tp=0/99 ranking_losses_with_isolated_tp=1 instance=key-free-interpolate used_keys=False
