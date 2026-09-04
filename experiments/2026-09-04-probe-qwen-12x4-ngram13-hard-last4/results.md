# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-qwen-12x4-ngram13 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 4/12 | 0.415 | 16/48 | 31/48 | 0.965 | -0.0324 |
| interpolate | 4/12 | 0.400 | 14/48 | 27/48 | 0.9635 | -0.0833 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 4/12 | 1/4 (04-market) | 7 |
| interpolate | 4/12 | 0/4 | 6 (01-harbour, 02-night-bus, 03-library, 05-kitchen, 09-workshop, 12-ferry-queue) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 16/32 | 17/31 | 0.485 |
| interpolate | 0/48 | 0/48 | 14/34 | 21/27 | 0.400 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 9/48 | 27/48 | 0.0894 | 0.188 | 0.562 |
| interpolate | 44/48 | 3/48 | -0.4132 | 0.917 | 0.062 |

hard auc=0.415 mean_pos=-0.0389 mean_neg=-0.0065 diff=-0.0324 pos>0=16/48 neg<=0=31/48 perm_p=0.965 (file-level, descriptive) binom_p=0.9934 (file-level, descriptive) youden_t=0.2323 youden_sens=0.000 youden_spec=1.000 J=0.000
hard prompts_marked_above=4/12 ranking_without_isolated_tp=1/4 ranking_losses_with_isolated_tp=7 instance=key-free-counts used_keys=False
interpolate auc=0.400 mean_pos=-0.1105 mean_neg=-0.0272 diff=-0.0833 pos>0=14/48 neg<=0=27/48 perm_p=0.9635 (file-level, descriptive) binom_p=0.999 (file-level, descriptive) youden_t=-0.4325 youden_sens=0.958 youden_spec=0.083 J=0.042
interpolate prompts_marked_above=4/12 ranking_without_isolated_tp=0/4 ranking_losses_with_isolated_tp=6 instance=key-free-interpolate used_keys=False
