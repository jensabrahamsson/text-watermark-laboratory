# Key-free transfer

transfer n_methods=6 train=experiments/2026-08-31-pair-36x4+experiments/2026-08-31-pair-long12x4+experiments/2026-08-31-pair-tails12x4+experiments/2026-08-31-pair-family12x4 test=experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashpool | 11/12 | 0.841 | 34/48 | 34/48 | 0.0004998 | 1.4703 |
| hashtok | 9/12 | 0.761 | 30/48 | 36/48 | 0.0004998 | 1.6830 |
| hashtokbackoff | 10/12 | 0.836 | 38/48 | 35/48 | 0.0004998 | 1.9081 |
| hashtokbackoff2 | 10/12 | 0.818 | 36/48 | 34/48 | 0.0004998 | 1.8336 |
| postokbackoff | 10/12 | 0.782 | 34/48 | 40/48 | 0.0004998 | 2.2018 |
| postokbackoff2 | 12/12 | 0.642 | 15/48 | 46/48 | 0.0004998 | 1.1095 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashpool | 0/48 | 0/48 | 34/14 | 14/34 | 0.708 |
| hashtok | 5/48 | 11/48 | 30/13 | 12/25 | 0.714 |
| hashtokbackoff | 3/48 | 3/48 | 38/7 | 13/32 | 0.745 |
| hashtokbackoff2 | 3/48 | 5/48 | 36/9 | 14/29 | 0.720 |
| postokbackoff | 4/48 | 24/48 | 34/10 | 8/16 | 0.810 |
| postokbackoff2 | 33/48 | 46/48 | 15/0 | 2/0 | 0.882 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtokbackoff/hashtokbackoff2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtok is the hashpool analog of tokhits. None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashpool | in-sample-youden | 0.3098 | 31/48 | 43/48 | 0.646 | 0.896 |
| hashtok | in-sample-youden | 0.3098 | 30/48 | 37/48 | 0.625 | 0.771 |
| hashtokbackoff | in-sample-youden | 0.7244 | 30/48 | 40/48 | 0.625 | 0.833 |
| hashtokbackoff2 | in-sample-youden | 0.7244 | 30/48 | 42/48 | 0.625 | 0.875 |
| postokbackoff | in-sample-youden | 0.0071 | 34/48 | 40/48 | 0.708 | 0.833 |
| postokbackoff2 | in-sample-youden | 0.7784 | 15/48 | 46/48 | 0.312 | 0.958 |
| hashpool | nested-youden | 0.4055 | 30/48 | 43/48 | 0.625 | 0.896 |
| hashpool | nested-fpr10 | 0.1597 | 31/48 | 40/48 | 0.646 | 0.833 |
| hashtok | nested-youden | 0.9174 | 26/48 | 42/48 | 0.542 | 0.875 |
| hashtok | nested-fpr10 | 0.8561 | 26/48 | 41/48 | 0.542 | 0.854 |
| hashtokbackoff | nested-youden | 0.8804 | 30/48 | 40/48 | 0.625 | 0.833 |
| hashtokbackoff | nested-fpr10 | 0.8036 | 30/48 | 40/48 | 0.625 | 0.833 |
| hashtokbackoff2 | nested-youden | 0.8804 | 30/48 | 42/48 | 0.625 | 0.875 |
| hashtokbackoff2 | nested-fpr10 | 0.8804 | 30/48 | 42/48 | 0.625 | 0.875 |
| postokbackoff | nested-youden | 0.6355 | 33/48 | 42/48 | 0.688 | 0.875 |
| postokbackoff | nested-fpr10 | 0.0000 | 34/48 | 40/48 | 0.708 | 0.833 |
| postokbackoff2 | nested-youden | 0.0000 | 15/48 | 46/48 | 0.312 | 0.958 |
| postokbackoff2 | nested-fpr10 | 0.0000 | 15/48 | 46/48 | 0.312 | 0.958 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashpool auc=0.841 mean_pos=1.1822 mean_neg=-0.2881 diff=1.4703 pos>0=34/48 neg<=0=34/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.6705 youden_sens=0.625 youden_spec=1.000 J=0.625
hashpool zeros=0/48 vs 0/48 decided_tp=34 fn=14 fp=14 tn=34 precision=0.708 decided_acc=0.708
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
hashtok auc=0.761 mean_pos=1.2750 mean_neg=-0.4080 diff=1.6830 pos>0=30/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.7031 youden_sens=0.625 youden_spec=0.833 J=0.458
hashtok zeros=5/48 vs 11/48 decided_tp=30 fn=13 fp=12 tn=25 precision=0.714 decided_acc=0.688
hashtok prompts_marked_above=9/12 instance=key-free-hashtok used_keys=False
hashtokbackoff auc=0.836 mean_pos=1.4101 mean_neg=-0.4981 diff=1.9081 pos>0=38/48 neg<=0=35/48 perm_p=0.0004998 binom_p=3.085e-05 youden_t=0.0076 youden_sens=0.792 youden_spec=0.750 J=0.542
hashtokbackoff zeros=3/48 vs 3/48 decided_tp=38 fn=7 fp=13 tn=32 precision=0.745 decided_acc=0.778
hashtokbackoff prompts_marked_above=10/12 instance=key-free-hashtokbackoff used_keys=False
hashtokbackoff2 auc=0.818 mean_pos=1.4176 mean_neg=-0.4160 diff=1.8336 pos>0=36/48 neg<=0=34/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=0.2741 youden_sens=0.750 youden_spec=0.812 J=0.562
hashtokbackoff2 zeros=3/48 vs 5/48 decided_tp=36 fn=9 fp=14 tn=29 precision=0.720 decided_acc=0.739
hashtokbackoff2 prompts_marked_above=10/12 instance=key-free-hashtokbackoff2 used_keys=False
postokbackoff auc=0.782 mean_pos=1.6496 mean_neg=-0.5522 diff=2.2018 pos>0=34/48 neg<=0=40/48 perm_p=0.0004998 binom_p=0.002758 youden_t=1.4224 youden_sens=0.667 youden_spec=0.958 J=0.625
postokbackoff zeros=4/48 vs 24/48 decided_tp=34 fn=10 fp=8 tn=16 precision=0.810 decided_acc=0.735
postokbackoff prompts_marked_above=10/12 instance=key-free-postokbackoff used_keys=False
postokbackoff2 auc=0.642 mean_pos=1.1468 mean_neg=0.0373 diff=1.1095 pos>0=15/48 neg<=0=46/48 perm_p=0.0004998 binom_p=0.9972 youden_t=0.8946 youden_sens=0.312 youden_spec=1.000 J=0.312
postokbackoff2 zeros=33/48 vs 46/48 decided_tp=15 fn=0 fp=2 tn=0 precision=0.882 decided_acc=0.882
postokbackoff2 prompts_marked_above=12/12 instance=key-free-postokbackoff2 used_keys=False
