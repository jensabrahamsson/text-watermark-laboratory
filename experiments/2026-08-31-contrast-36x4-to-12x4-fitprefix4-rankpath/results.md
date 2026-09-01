# Key-free instance contrast

instance-contrast n_rows=6 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 control=/workspace/experiments/2026-08-31-pair-12x4-controlkeys n_control=48 n_aligned=48 fit_prefix=4 rankpath_pos_bucket=1 rankpath_end=None used_keys=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | comparison | prompt wins | file auc | pos>0 | neg<=0 | perm p | brier |
|---|---|---|---|---|---|---|---|
| rankpath | control-vs-unmarked | 8/12 | 0.498 | 17/48 | 33/48 | 0.4208 | 0.3140 |
| rankpath | public-vs-control | 9/12 | 0.694 | 28/48 | 31/48 | 0.0009995 | 0.2353 |
| rankpath | public-vs-unmarked | 10/12 | 0.683 | 28/48 | 33/48 | 0.001999 | 0.2383 |
| rankuni | control-vs-unmarked | 9/12 | 0.613 | 30/48 | 25/48 | 0.02499 | 0.2406 |
| rankuni | public-vs-control | 5/12 | 0.502 | 29/48 | 18/48 | 0.4938 | 0.2540 |
| rankuni | public-vs-unmarked | 8/12 | 0.628 | 29/48 | 25/48 | 0.01899 | 0.2396 |

public-vs-unmarked: can the key-free reader still see the public mark. control-vs-unmarked: does a *different* key instance look marked. public-vs-control: can it tell the two instances apart. pos is the first class in each name (control, public, public).

rankpath control-vs-unmarked auc=0.498 mean_pos=-0.6901 mean_neg=-0.7227 diff=0.0325 pos>0=17/48 neg<=0=33/48 perm_p=0.4208 binom_p=0.9853 youden_t=-0.6715 youden_sens=0.625 youden_spec=0.542 J=0.167 brier=0.3140 prompts=8/12
rankpath public-vs-control auc=0.694 mean_pos=-0.0881 mean_neg=-0.6901 diff=0.6021 pos>0=28/48 neg<=0=31/48 perm_p=0.0009995 binom_p=0.1562 youden_t=0.0817 youden_sens=0.583 youden_spec=0.812 J=0.396 brier=0.2353 prompts=9/12
rankpath public-vs-unmarked auc=0.683 mean_pos=-0.0881 mean_neg=-0.7227 diff=0.6346 pos>0=28/48 neg<=0=33/48 perm_p=0.001999 binom_p=0.1562 youden_t=-0.8521 youden_sens=0.854 youden_spec=0.500 J=0.354 brier=0.2383 prompts=10/12
rankuni control-vs-unmarked auc=0.613 mean_pos=0.0882 mean_neg=-0.0321 diff=0.1203 pos>0=30/48 neg<=0=25/48 perm_p=0.02499 binom_p=0.0557 youden_t=-0.1487 youden_sens=0.938 youden_spec=0.375 J=0.312 brier=0.2406 prompts=9/12
rankuni public-vs-control auc=0.502 mean_pos=0.0907 mean_neg=0.0882 diff=0.0025 pos>0=29/48 neg<=0=18/48 perm_p=0.4938 binom_p=0.09671 youden_t=0.0642 youden_sens=0.583 youden_spec=0.688 J=0.271 brier=0.2540 prompts=5/12
rankuni public-vs-unmarked auc=0.628 mean_pos=0.0907 mean_neg=-0.0321 diff=0.1228 pos>0=29/48 neg<=0=25/48 perm_p=0.01899 binom_p=0.09671 youden_t=0.0642 youden_sens=0.583 youden_spec=0.708 J=0.292 brier=0.2396 prompts=8/12

transfer n_methods=2 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 10/12 | 0.683 | 28/48 | 33/48 | 0.001999 | 0.6346 |
| rankuni | 8/12 | 0.628 | 29/48 | 25/48 | 0.01899 | 0.1228 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 28/20 | 15/33 | 0.651 |
| rankuni | 0/48 | 0/48 | 29/19 | 23/25 | 0.558 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

rankpath auc=0.683 mean_pos=-0.0881 mean_neg=-0.7227 diff=0.6346 pos>0=28/48 neg<=0=33/48 perm_p=0.001999 binom_p=0.1562 youden_t=-0.8521 youden_sens=0.854 youden_spec=0.500 J=0.354
rankpath zeros=0/48 vs 0/48 decided_tp=28 fn=20 fp=15 tn=33 precision=0.651 decided_acc=0.635
rankpath prompts_marked_above=10/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.628 mean_pos=0.0907 mean_neg=-0.0321 diff=0.1228 pos>0=29/48 neg<=0=25/48 perm_p=0.01899 binom_p=0.09671 youden_t=0.0642 youden_sens=0.583 youden_spec=0.708 J=0.292
rankuni zeros=0/48 vs 0/48 decided_tp=29 fn=19 fp=23 tn=25 precision=0.558 decided_acc=0.562
rankuni prompts_marked_above=8/12 instance=key-free-rankuni used_keys=False
