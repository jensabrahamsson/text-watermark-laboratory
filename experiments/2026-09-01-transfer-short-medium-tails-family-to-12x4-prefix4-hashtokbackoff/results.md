# Key-free transfer

transfer n_methods=6 train=experiments/2026-08-31-pair-36x4+experiments/2026-08-31-pair-long12x4+experiments/2026-08-31-pair-tails12x4+experiments/2026-08-31-pair-family12x4 test=experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashpool | 10/12 | 0.887 | 38/48 | 37/48 | 0.0004998 | 1.9105 |
| hashtok | 10/12 | 0.844 | 35/48 | 39/48 | 0.0004998 | 2.3996 |
| hashtokbackoff | 10/12 | 0.780 | 31/48 | 33/48 | 0.0004998 | 1.9262 |
| hashtokbackoff2 | 10/12 | 0.760 | 31/48 | 33/48 | 0.0004998 | 1.7839 |
| postokbackoff | 10/12 | 0.800 | 34/48 | 43/48 | 0.0004998 | 2.3297 |
| postokbackoff2 | 12/12 | 0.642 | 15/48 | 46/48 | 0.0004998 | 1.1721 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashpool | 0/48 | 0/48 | 38/10 | 11/37 | 0.776 |
| hashtok | 5/48 | 21/48 | 35/8 | 9/18 | 0.795 |
| hashtokbackoff | 4/48 | 8/48 | 31/13 | 15/25 | 0.674 |
| hashtokbackoff2 | 4/48 | 10/48 | 31/13 | 15/23 | 0.674 |
| postokbackoff | 6/48 | 31/48 | 34/8 | 5/12 | 0.872 |
| postokbackoff2 | 33/48 | 46/48 | 15/0 | 2/0 | 0.882 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtokbackoff/hashtokbackoff2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtok is the hashpool analog of tokhits. None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashpool | in-sample-youden | 0.0405 | 38/48 | 37/48 | 0.792 | 0.771 |
| hashtok | in-sample-youden | 0.0405 | 35/48 | 40/48 | 0.729 | 0.833 |
| hashtokbackoff | in-sample-youden | 0.3192 | 31/48 | 35/48 | 0.646 | 0.729 |
| hashtokbackoff2 | in-sample-youden | 0.3192 | 31/48 | 35/48 | 0.646 | 0.729 |
| postokbackoff | in-sample-youden | 0.0000 | 34/48 | 43/48 | 0.708 | 0.896 |
| postokbackoff2 | in-sample-youden | 0.0000 | 15/48 | 46/48 | 0.312 | 0.958 |
| hashpool | nested-youden | 0.3974 | 35/48 | 46/48 | 0.729 | 0.958 |
| hashpool | nested-fpr10 | 0.2444 | 35/48 | 44/48 | 0.729 | 0.917 |
| hashtok | nested-youden | 0.8216 | 33/48 | 45/48 | 0.688 | 0.938 |
| hashtok | nested-fpr10 | 0.6732 | 35/48 | 44/48 | 0.729 | 0.917 |
| hashtokbackoff | nested-youden | 0.8416 | 31/48 | 42/48 | 0.646 | 0.875 |
| hashtokbackoff | nested-fpr10 | 1.0614 | 30/48 | 44/48 | 0.625 | 0.917 |
| hashtokbackoff2 | nested-youden | 0.8416 | 31/48 | 42/48 | 0.646 | 0.875 |
| hashtokbackoff2 | nested-fpr10 | 1.0614 | 30/48 | 44/48 | 0.625 | 0.917 |
| postokbackoff | nested-youden | 0.5924 | 34/48 | 45/48 | 0.708 | 0.938 |
| postokbackoff | nested-fpr10 | 0.0000 | 34/48 | 43/48 | 0.708 | 0.896 |
| postokbackoff2 | nested-youden | 0.0000 | 15/48 | 46/48 | 0.312 | 0.958 |
| postokbackoff2 | nested-fpr10 | 0.0000 | 15/48 | 46/48 | 0.312 | 0.958 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashpool auc=0.887 mean_pos=1.4247 mean_neg=-0.4859 diff=1.9105 pos>0=38/48 neg<=0=37/48 perm_p=0.0004998 binom_p=3.085e-05 youden_t=0.3190 youden_sens=0.729 youden_spec=0.958 J=0.688
hashpool zeros=0/48 vs 0/48 decided_tp=38 fn=10 fp=11 tn=37 precision=0.776 decided_acc=0.781
hashpool prompts_marked_above=10/12 instance=key-free-hashpool used_keys=False
hashtok auc=0.844 mean_pos=1.8408 mean_neg=-0.5588 diff=2.3996 pos>0=35/48 neg<=0=39/48 perm_p=0.0004998 binom_p=0.001044 youden_t=0.7445 youden_sens=0.729 youden_spec=0.938 J=0.667
hashtok zeros=5/48 vs 21/48 decided_tp=35 fn=8 fp=9 tn=18 precision=0.795 decided_acc=0.757
hashtok prompts_marked_above=10/12 instance=key-free-hashtok used_keys=False
hashtokbackoff auc=0.780 mean_pos=1.4141 mean_neg=-0.5121 diff=1.9262 pos>0=31/48 neg<=0=33/48 perm_p=0.0004998 binom_p=0.02973 youden_t=0.8429 youden_sens=0.646 youden_spec=0.896 J=0.542
hashtokbackoff zeros=4/48 vs 8/48 decided_tp=31 fn=13 fp=15 tn=25 precision=0.674 decided_acc=0.667
hashtokbackoff prompts_marked_above=10/12 instance=key-free-hashtokbackoff used_keys=False
hashtokbackoff2 auc=0.760 mean_pos=1.3693 mean_neg=-0.4145 diff=1.7839 pos>0=31/48 neg<=0=33/48 perm_p=0.0004998 binom_p=0.02973 youden_t=0.8429 youden_sens=0.646 youden_spec=0.896 J=0.542
hashtokbackoff2 zeros=4/48 vs 10/48 decided_tp=31 fn=13 fp=15 tn=23 precision=0.674 decided_acc=0.659
hashtokbackoff2 prompts_marked_above=10/12 instance=key-free-hashtokbackoff2 used_keys=False
postokbackoff auc=0.800 mean_pos=1.7413 mean_neg=-0.5884 diff=2.3297 pos>0=34/48 neg<=0=43/48 perm_p=0.0004998 binom_p=0.002758 youden_t=1.1849 youden_sens=0.688 youden_spec=0.979 J=0.667
postokbackoff zeros=6/48 vs 31/48 decided_tp=34 fn=8 fp=5 tn=12 precision=0.872 decided_acc=0.780
postokbackoff prompts_marked_above=10/12 instance=key-free-postokbackoff used_keys=False
postokbackoff2 auc=0.642 mean_pos=1.2075 mean_neg=0.0354 diff=1.1721 pos>0=15/48 neg<=0=46/48 perm_p=0.0004998 binom_p=0.9972 youden_t=0.8494 youden_sens=0.312 youden_spec=1.000 J=0.312
postokbackoff2 zeros=33/48 vs 46/48 decided_tp=15 fn=0 fp=2 tn=0 precision=0.882 decided_acc=0.882
postokbackoff2 prompts_marked_above=12/12 instance=key-free-postokbackoff2 used_keys=False
