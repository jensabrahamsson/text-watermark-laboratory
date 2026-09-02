# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-09-02-pair-12x4-control-as-marked context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| interpolate | 7/12 | 0.590 | 30/48 | 25/48 | 0.1349 | 0.0509 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| interpolate | 7/12 | 1/7 (11-garden) | 5 (01-harbour, 02-night-bus, 08-letter, 09-workshop, 12-ferry-queue) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| interpolate | 0/48 | 0/48 | 30/18 | 23/25 | 0.566 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| interpolate | 33/48 | 20/48 | -0.0361 | 0.688 | 0.417 |

interpolate auc=0.590 mean_pos=0.0571 mean_neg=0.0061 diff=0.0509 pos>0=30/48 neg<=0=25/48 perm_p=0.1349 (file-level, descriptive) binom_p=0.0557 (file-level, descriptive) youden_t=-0.0354 youden_sens=0.708 youden_spec=0.479 J=0.188
interpolate prompts_marked_above=7/12 ranking_without_isolated_tp=1/7 ranking_losses_with_isolated_tp=5 instance=key-free-interpolate used_keys=False
