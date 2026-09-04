# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-09-01-pair-gpt2-medium-12x4 context_len=4 model=distilgpt2 max_draws=None prefix_lens=[] windows=['4:16'] fit_prefix=16 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 11/12 | 0.783 | 33/48 | 33/48 | 0.0004998 | 0.3033 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| rankpath | 11/12 | 0/11 | 1 (01-harbour) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 33/15 | 15/33 | 0.688 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| rankpath | 29/48 | 35/48 | 0.0375 | 0.604 | 0.729 |

| window tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 4:16 | rankpath | 11/12 | 0.646 | 36/48 | 16/48 |

rankpath auc=0.783 mean_pos=0.1122 mean_neg=-0.1911 diff=0.3033 pos>0=33/48 neg<=0=33/48 perm_p=0.0004998 (file-level, descriptive) binom_p=0.006642 (file-level, descriptive) youden_t=0.0299 youden_sens=0.688 youden_spec=0.750 J=0.438
rankpath prompts_marked_above=11/12 ranking_without_isolated_tp=0/11 ranking_losses_with_isolated_tp=1 instance=key-free-rankpath used_keys=False
