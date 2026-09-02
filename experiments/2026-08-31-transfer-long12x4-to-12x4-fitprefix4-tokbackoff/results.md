# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-long12x4 test=experiments/2026-08-17-pair-12x4 n_train=12 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 8/12 | 0.621 | 19/48 | 48/48 | 0.0004998 | 1.6026 |
| postokhits | 12/12 | 0.729 | 19/48 | 48/48 | 0.0004998 | 1.6726 |
| postokbackoff | 12/12 | 0.748 | 21/48 | 48/48 | 0.0004998 | 1.7125 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 9/48 | 33/48 | 19/20 | 0/15 | 1.000 |
| postokhits | 29/48 | 43/48 | 19/0 | 0/5 | 1.000 |
| postokbackoff | 27/48 | 43/48 | 21/0 | 0/5 | 1.000 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; it is not key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | 0.0000 | 19/48 | 48/48 | 0.396 | 1.000 |
| postokhits | in-sample-youden | 0.0000 | 19/48 | 48/48 | 0.396 | 1.000 |
| postokbackoff | in-sample-youden | 0.0000 | 21/48 | 48/48 | 0.438 | 1.000 |
| poshits | nested-youden | 0.0402 | 19/48 | 48/48 | 0.396 | 1.000 |
| poshits | nested-fpr10 | 0.0000 | 19/48 | 48/48 | 0.396 | 1.000 |
| postokhits | nested-youden | 0.1232 | 19/48 | 48/48 | 0.396 | 1.000 |
| postokhits | nested-fpr10 | 0.0000 | 19/48 | 48/48 | 0.396 | 1.000 |
| postokbackoff | nested-youden | 0.1232 | 21/48 | 48/48 | 0.438 | 1.000 |
| postokbackoff | nested-fpr10 | 0.0000 | 21/48 | 48/48 | 0.438 | 1.000 |

poshits auc=0.621 mean_pos=1.2303 mean_neg=-0.3723 diff=1.6026 pos>0=19/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9443 youden_t=0.0000 youden_sens=0.396 youden_spec=1.000 J=0.396
poshits zeros=9/48 vs 33/48 decided_tp=19 fn=20 fp=0 tn=15 precision=1.000 decided_acc=0.630
poshits prompts_marked_above=8/12 instance=key-free-poshits used_keys=False
postokhits auc=0.729 mean_pos=1.3844 mean_neg=-0.2882 diff=1.6726 pos>0=19/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9443 youden_t=0.0000 youden_sens=0.396 youden_spec=1.000 J=0.396
postokhits zeros=29/48 vs 43/48 decided_tp=19 fn=0 fp=0 tn=5 precision=1.000 decided_acc=1.000
postokhits prompts_marked_above=12/12 instance=key-free-postokhits used_keys=False
postokbackoff auc=0.748 mean_pos=1.4243 mean_neg=-0.2882 diff=1.7125 pos>0=21/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.8438 youden_t=0.0000 youden_sens=0.438 youden_spec=1.000 J=0.438
postokbackoff zeros=27/48 vs 43/48 decided_tp=21 fn=0 fp=0 tn=5 precision=1.000 decided_acc=1.000
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
