# Key-free transfer

transfer n_methods=5 train=experiments/2026-08-31-pair-36x4+experiments/2026-08-31-pair-long12x4+experiments/2026-08-31-pair-tails12x4+experiments/2026-08-31-pair-family12x4 test=experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashtok | 9/12 | 0.761 | 30/48 | 36/48 | 0.0004998 | 1.6830 |
| hashtoklen | 12/12 | 0.701 | 21/48 | 45/48 | 0.0004998 | 0.7758 |
| hashtoklenbackoff | 11/12 | 0.822 | 36/48 | 34/48 | 0.0004998 | 1.9507 |
| hashtoklenbackoff2 | 10/12 | 0.769 | 36/48 | 35/48 | 0.0004998 | 1.6141 |
| postokbackoff2 | 12/12 | 0.642 | 15/48 | 46/48 | 0.0004998 | 1.1095 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashtok | 5/48 | 11/48 | 30/13 | 12/25 | 0.714 |
| hashtoklen | 27/48 | 44/48 | 21/0 | 3/1 | 0.875 |
| hashtoklenbackoff | 3/48 | 6/48 | 36/9 | 14/28 | 0.720 |
| hashtoklenbackoff2 | 3/48 | 17/48 | 36/9 | 13/18 | 0.735 |
| postokbackoff2 | 33/48 | 46/48 | 15/0 | 2/0 | 0.882 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashtok is the hashpool analog of tokhits. None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashtok | in-sample-youden | 0.3098 | 30/48 | 37/48 | 0.625 | 0.771 |
| hashtoklen | in-sample-youden | 0.3881 | 21/48 | 45/48 | 0.438 | 0.938 |
| hashtoklenbackoff | in-sample-youden | 0.0000 | 36/48 | 34/48 | 0.750 | 0.708 |
| hashtoklenbackoff2 | in-sample-youden | 0.2155 | 35/48 | 36/48 | 0.729 | 0.750 |
| postokbackoff2 | in-sample-youden | 0.7784 | 15/48 | 46/48 | 0.312 | 0.958 |
| hashtok | nested-youden | 0.9174 | 26/48 | 42/48 | 0.542 | 0.875 |
| hashtok | nested-fpr10 | 0.8561 | 26/48 | 41/48 | 0.542 | 0.854 |
| hashtoklen | nested-youden | 0.1962 | 21/48 | 45/48 | 0.438 | 0.938 |
| hashtoklen | nested-fpr10 | 0.0000 | 21/48 | 45/48 | 0.438 | 0.938 |
| hashtoklenbackoff | nested-youden | 1.1025 | 33/48 | 42/48 | 0.688 | 0.875 |
| hashtoklenbackoff | nested-fpr10 | 1.0909 | 33/48 | 42/48 | 0.688 | 0.875 |
| hashtoklenbackoff2 | nested-youden | 1.1025 | 28/48 | 43/48 | 0.583 | 0.896 |
| hashtoklenbackoff2 | nested-fpr10 | 1.6036 | 23/48 | 46/48 | 0.479 | 0.958 |
| postokbackoff2 | nested-youden | 0.0000 | 15/48 | 46/48 | 0.312 | 0.958 |
| postokbackoff2 | nested-fpr10 | 0.0000 | 15/48 | 46/48 | 0.312 | 0.958 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashtok auc=0.761 mean_pos=1.2750 mean_neg=-0.4080 diff=1.6830 pos>0=30/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.7031 youden_sens=0.625 youden_spec=0.833 J=0.458
hashtok zeros=5/48 vs 11/48 decided_tp=30 fn=13 fp=12 tn=25 precision=0.714 decided_acc=0.688
hashtok prompts_marked_above=9/12 instance=key-free-hashtok used_keys=False
hashtoklen auc=0.701 mean_pos=0.8070 mean_neg=0.0312 diff=0.7758 pos>0=21/48 neg<=0=45/48 perm_p=0.0004998 binom_p=0.8438 youden_t=0.0000 youden_sens=0.438 youden_spec=0.938 J=0.375
hashtoklen zeros=27/48 vs 44/48 decided_tp=21 fn=0 fp=3 tn=1 precision=0.875 decided_acc=0.880
hashtoklen prompts_marked_above=12/12 instance=key-free-hashtoklen used_keys=False
hashtoklenbackoff auc=0.822 mean_pos=1.5510 mean_neg=-0.3997 diff=1.9507 pos>0=36/48 neg<=0=34/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=1.3150 youden_sens=0.667 youden_spec=0.938 J=0.604
hashtoklenbackoff zeros=3/48 vs 6/48 decided_tp=36 fn=9 fp=14 tn=28 precision=0.720 decided_acc=0.736
hashtoklenbackoff prompts_marked_above=11/12 instance=key-free-hashtoklenbackoff used_keys=False
hashtoklenbackoff2 auc=0.769 mean_pos=1.4982 mean_neg=-0.1159 diff=1.6141 pos>0=36/48 neg<=0=35/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=1.0761 youden_sens=0.667 youden_spec=0.854 J=0.521
hashtoklenbackoff2 zeros=3/48 vs 17/48 decided_tp=36 fn=9 fp=13 tn=18 precision=0.735 decided_acc=0.711
hashtoklenbackoff2 prompts_marked_above=10/12 instance=key-free-hashtoklenbackoff2 used_keys=False
postokbackoff2 auc=0.642 mean_pos=1.1468 mean_neg=0.0373 diff=1.1095 pos>0=15/48 neg<=0=46/48 perm_p=0.0004998 binom_p=0.9972 youden_t=0.8946 youden_sens=0.312 youden_spec=1.000 J=0.312
postokbackoff2 zeros=33/48 vs 46/48 decided_tp=15 fn=0 fp=2 tn=0 precision=0.882 decided_acc=0.882
postokbackoff2 prompts_marked_above=12/12 instance=key-free-postokbackoff2 used_keys=False
