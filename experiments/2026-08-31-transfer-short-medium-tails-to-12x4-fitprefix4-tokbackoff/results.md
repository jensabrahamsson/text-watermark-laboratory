# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-short-medium-tails test=experiments/2026-08-17-pair-12x4 n_train=48 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 11/12 | 0.770 | 30/48 | 48/48 | 0.0004998 | 2.6143 |
| postokhits | 12/12 | 0.832 | 30/48 | 48/48 | 0.0004998 | 2.6167 |
| postokbackoff | 12/12 | 0.888 | 36/48 | 48/48 | 0.0004998 | 2.7671 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 6/48 | 33/48 | 30/12 | 0/15 | 1.000 |
| postokhits | 18/48 | 43/48 | 30/0 | 0/5 | 1.000 |
| postokbackoff | 12/48 | 43/48 | 36/0 | 0/5 | 1.000 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; it is not key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | 0.4260 | 30/48 | 48/48 | 0.625 | 1.000 |
| postokhits | in-sample-youden | 0.4260 | 30/48 | 48/48 | 0.625 | 1.000 |
| postokbackoff | in-sample-youden | 0.0000 | 36/48 | 48/48 | 0.750 | 1.000 |
| poshits | nested-youden | 0.1359 | 30/48 | 48/48 | 0.625 | 1.000 |
| poshits | nested-fpr10 | 0.0000 | 30/48 | 48/48 | 0.625 | 1.000 |
| postokhits | nested-youden | 0.4512 | 30/48 | 48/48 | 0.625 | 1.000 |
| postokhits | nested-fpr10 | 0.0000 | 30/48 | 48/48 | 0.625 | 1.000 |
| postokbackoff | nested-youden | 0.4512 | 36/48 | 48/48 | 0.750 | 1.000 |
| postokbackoff | nested-fpr10 | 0.0000 | 36/48 | 48/48 | 0.750 | 1.000 |

poshits auc=0.770 mean_pos=2.1033 mean_neg=-0.5110 diff=2.6143 pos>0=30/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.0000 youden_sens=0.625 youden_spec=1.000 J=0.625
poshits zeros=6/48 vs 33/48 decided_tp=30 fn=12 fp=0 tn=15 precision=1.000 decided_acc=0.789
poshits prompts_marked_above=11/12 instance=key-free-poshits used_keys=False
postokhits auc=0.832 mean_pos=2.2061 mean_neg=-0.4106 diff=2.6167 pos>0=30/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.0000 youden_sens=0.625 youden_spec=1.000 J=0.625
postokhits zeros=18/48 vs 43/48 decided_tp=30 fn=0 fp=0 tn=5 precision=1.000 decided_acc=1.000
postokhits prompts_marked_above=12/12 instance=key-free-postokhits used_keys=False
postokbackoff auc=0.888 mean_pos=2.3565 mean_neg=-0.4106 diff=2.7671 pos>0=36/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=0.0000 youden_sens=0.750 youden_spec=1.000 J=0.750
postokbackoff zeros=12/48 vs 43/48 decided_tp=36 fn=0 fp=0 tn=5 precision=1.000 decided_acc=1.000
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
