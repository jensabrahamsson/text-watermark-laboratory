# Key-free instance contrast

instance-contrast n_rows=6 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 control=/workspace/experiments/2026-08-31-pair-12x4-controlkeys n_control=48 n_aligned=48 fit_prefix=5 rankpath_pos_bucket=0 rankpath_end=None used_keys=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | comparison | prompt wins | file auc | pos>0 | neg<=0 | perm p | brier |
|---|---|---|---|---|---|---|---|
| rankpath | control-vs-unmarked | 6/12 | 0.511 | 6/48 | 43/48 | 0.2664 | 0.2837 |
| rankpath | public-vs-control | 9/12 | 0.752 | 25/48 | 42/48 | 0.0004998 | 0.2143 |
| rankpath | public-vs-unmarked | 11/12 | 0.759 | 25/48 | 43/48 | 0.0004998 | 0.2111 |
| rankuni | control-vs-unmarked | 7/12 | 0.557 | 22/48 | 27/48 | 0.1694 | 0.2478 |
| rankuni | public-vs-control | 7/12 | 0.594 | 31/48 | 26/48 | 0.03398 | 0.2424 |
| rankuni | public-vs-unmarked | 10/12 | 0.653 | 31/48 | 27/48 | 0.004998 | 0.2366 |

public-vs-unmarked: can the key-free reader still see the public mark. control-vs-unmarked: does a *different* key instance look marked. public-vs-control: can it tell the two instances apart. pos is the first class in each name (control, public, public).

rankpath control-vs-unmarked auc=0.511 mean_pos=-0.6418 mean_neg=-0.7208 diff=0.0789 pos>0=6/48 neg<=0=43/48 perm_p=0.2664 binom_p=1 youden_t=-0.3419 youden_sens=0.375 youden_spec=0.792 J=0.167 brier=0.2837 prompts=6/12
rankpath public-vs-control auc=0.752 mean_pos=-0.0622 mean_neg=-0.6418 diff=0.5796 pos>0=25/48 neg<=0=42/48 perm_p=0.0004998 binom_p=0.4427 youden_t=0.1008 youden_sens=0.500 youden_spec=0.938 J=0.438 brier=0.2143 prompts=9/12
rankpath public-vs-unmarked auc=0.759 mean_pos=-0.0622 mean_neg=-0.7208 diff=0.6586 pos>0=25/48 neg<=0=43/48 perm_p=0.0004998 binom_p=0.4427 youden_t=-0.1442 youden_sens=0.625 youden_spec=0.875 J=0.500 brier=0.2111 prompts=11/12
rankuni control-vs-unmarked auc=0.557 mean_pos=-0.0202 mean_neg=-0.0669 diff=0.0468 pos>0=22/48 neg<=0=27/48 perm_p=0.1694 binom_p=0.7646 youden_t=0.0282 youden_sens=0.458 youden_spec=0.708 J=0.167 brier=0.2478 prompts=7/12
rankuni public-vs-control auc=0.594 mean_pos=0.0668 mean_neg=-0.0202 diff=0.0870 pos>0=31/48 neg<=0=26/48 perm_p=0.03398 binom_p=0.02973 youden_t=0.1087 youden_sens=0.500 youden_spec=0.792 J=0.292 brier=0.2424 prompts=7/12
rankuni public-vs-unmarked auc=0.653 mean_pos=0.0668 mean_neg=-0.0669 diff=0.1338 pos>0=31/48 neg<=0=27/48 perm_p=0.004998 binom_p=0.02973 youden_t=0.0806 youden_sens=0.500 youden_spec=0.771 J=0.271 brier=0.2366 prompts=10/12

transfer n_methods=2 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 11/12 | 0.759 | 25/48 | 43/48 | 0.0004998 | 0.6586 |
| rankuni | 10/12 | 0.653 | 31/48 | 27/48 | 0.004998 | 0.1338 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 25/23 | 5/43 | 0.833 |
| rankuni | 0/48 | 0/48 | 31/17 | 21/27 | 0.596 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

rankpath auc=0.759 mean_pos=-0.0622 mean_neg=-0.7208 diff=0.6586 pos>0=25/48 neg<=0=43/48 perm_p=0.0004998 binom_p=0.4427 youden_t=-0.1442 youden_sens=0.625 youden_spec=0.875 J=0.500
rankpath zeros=0/48 vs 0/48 decided_tp=25 fn=23 fp=5 tn=43 precision=0.833 decided_acc=0.708
rankpath prompts_marked_above=11/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.653 mean_pos=0.0668 mean_neg=-0.0669 diff=0.1338 pos>0=31/48 neg<=0=27/48 perm_p=0.004998 binom_p=0.02973 youden_t=0.0806 youden_sens=0.500 youden_spec=0.771 J=0.271
rankuni zeros=0/48 vs 0/48 decided_tp=31 fn=17 fp=21 tn=27 precision=0.596 decided_acc=0.604
rankuni prompts_marked_above=10/12 instance=key-free-rankuni used_keys=False
