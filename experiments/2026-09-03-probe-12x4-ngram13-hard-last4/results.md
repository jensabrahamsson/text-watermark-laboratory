# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-03-pair-12x4-ngram13 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 6/12 | 0.544 | 22/48 | 30/48 | 0.2879 | 0.0092 |
| interpolate | 6/12 | 0.541 | 20/48 | 31/48 | 0.2934 | 0.0213 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 6/12 | 0/6 | 5 (02-night-bus, 03-library, 05-kitchen, 10-office, 11-garden) |
| interpolate | 6/12 | 0/6 | 6 (01-harbour, 02-night-bus, 05-kitchen, 07-rain, 10-office, 11-garden) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 22/26 | 18/30 | 0.550 |
| interpolate | 0/48 | 0/48 | 20/28 | 17/31 | 0.541 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 24/48 | 21/48 | -0.0185 | 0.500 | 0.438 |
| interpolate | 24/48 | 22/48 | -0.0642 | 0.500 | 0.458 |

hard auc=0.544 mean_pos=-0.0134 mean_neg=-0.0226 diff=0.0092 pos>0=22/48 neg<=0=30/48 perm_p=0.2879 (file-level, descriptive) binom_p=0.7646 (file-level, descriptive) youden_t=-0.0437 youden_sens=0.708 youden_spec=0.438 J=0.146
hard prompts_marked_above=6/12 ranking_without_isolated_tp=0/6 ranking_losses_with_isolated_tp=5 instance=key-free-counts used_keys=False
interpolate auc=0.541 mean_pos=-0.0468 mean_neg=-0.0681 diff=0.0213 pos>0=20/48 neg<=0=31/48 perm_p=0.2934 (file-level, descriptive) binom_p=0.9033 (file-level, descriptive) youden_t=-0.1015 youden_sens=0.667 youden_spec=0.479 J=0.146
interpolate prompts_marked_above=6/12 ranking_without_isolated_tp=0/6 ranking_losses_with_isolated_tp=6 instance=key-free-interpolate used_keys=False
