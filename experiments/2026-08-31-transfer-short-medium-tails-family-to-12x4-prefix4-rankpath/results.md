# Key-free transfer

transfer n_methods=2 train=/workspace/experiments/2026-08-31-pair-36x4+/workspace/experiments/2026-08-31-pair-long12x4+/workspace/experiments/2026-08-31-pair-tails12x4+/workspace/experiments/2026-08-31-pair-family12x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=0 cascade_rankpath_end=None
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 10/12 | 0.770 | 28/48 | 40/48 | 0.0004998 | 0.5349 |
| rankuni | 11/12 | 0.761 | 39/48 | 32/48 | 0.0004998 | 0.1584 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 28/20 | 8/40 | 0.778 |
| rankuni | 0/48 | 0/48 | 39/9 | 16/32 | 0.709 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| rankpath | in-sample-youden | 0.0777 | 28/48 | 40/48 | 0.583 | 0.833 |
| rankuni | in-sample-youden | 0.0762 | 23/48 | 38/48 | 0.479 | 0.792 |
| rankpath | nested-youden | -0.0307 | 28/48 | 37/48 | 0.583 | 0.771 |
| rankpath | nested-fpr10 | 0.6410 | 11/48 | 47/48 | 0.229 | 0.979 |
| rankuni | nested-youden | 0.0627 | 27/48 | 37/48 | 0.562 | 0.771 |
| rankuni | nested-fpr10 | 0.1382 | 11/48 | 44/48 | 0.229 | 0.917 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

rankpath auc=0.770 mean_pos=0.1090 mean_neg=-0.4260 diff=0.5349 pos>0=28/48 neg<=0=40/48 perm_p=0.0004998 binom_p=0.1562 youden_t=-0.3582 youden_sens=0.833 youden_spec=0.625 J=0.458
rankpath zeros=0/48 vs 0/48 decided_tp=28 fn=20 fp=8 tn=40 precision=0.778 decided_acc=0.708
rankpath prompts_marked_above=10/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.761 mean_pos=0.0696 mean_neg=-0.0888 diff=0.1584 pos>0=39/48 neg<=0=32/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.667 J=0.479
rankuni zeros=0/48 vs 0/48 decided_tp=39 fn=9 fp=16 tn=32 precision=0.709 decided_acc=0.740
rankuni prompts_marked_above=11/12 instance=key-free-rankuni used_keys=False
