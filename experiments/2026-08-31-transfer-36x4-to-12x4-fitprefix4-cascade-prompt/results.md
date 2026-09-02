# Key-free transfer

transfer n_methods=6 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=True
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 6/12 | 0.597 | 16/48 | 44/48 | 0.003998 | 0.8095 |
| pivot-lda | 8/12 | 0.509 | 24/48 | 25/48 | 0.6922 | -0.0013 |
| pivot-rank | 6/12 | 0.517 | 20/48 | 24/48 | 0.4168 | 0.3229 |
| pivot-lda-entropy | 5/12 | 0.432 | 22/48 | 23/48 | 0.8981 | -0.0013 |
| pivot-rank-entropy | 4/12 | 0.466 | 32/48 | 15/48 | 0.5357 | -0.0323 |
| cascade | 10/12 | 0.616 | 25/48 | 28/48 | 0.0004998 | 1.1710 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 9/48 | 16/48 | 16/23 | 4/28 | 0.800 |
| pivot-lda | 0/48 | 0/48 | 24/24 | 23/25 | 0.511 |
| pivot-rank | 0/48 | 0/48 | 20/28 | 24/24 | 0.455 |
| pivot-lda-entropy | 0/48 | 0/48 | 22/26 | 25/23 | 0.468 |
| pivot-rank-entropy | 0/48 | 0/48 | 32/16 | 33/15 | 0.492 |
| cascade | 0/48 | 0/48 | 25/23 | 20/28 | 0.556 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff | in-sample-youden | 0.5100 | 16/48 | 44/48 | 0.333 | 0.917 |
| pivot-lda | in-sample-youden | 0.0000 | 24/48 | 25/48 | 0.500 | 0.521 |
| pivot-rank | in-sample-youden | 0.8932 | 18/48 | 25/48 | 0.375 | 0.521 |
| pivot-lda-entropy | in-sample-youden | -0.0032 | 29/48 | 9/48 | 0.604 | 0.188 |
| pivot-rank-entropy | in-sample-youden | 3.1963 | 22/48 | 20/48 | 0.458 | 0.417 |
| cascade | in-sample-youden | 0.2162 | 16/48 | 48/48 | 0.333 | 1.000 |
| postokbackoff | nested-youden | 0.9358 | 15/48 | 48/48 | 0.312 | 1.000 |
| postokbackoff | nested-fpr10 | 0.9046 | 15/48 | 48/48 | 0.312 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

Cascade: count LR when n_used>0, unmarked-LM pivot otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff pivot_weight=uniform prompt_context=True used_keys=False
count covered marked 16/48 >0 16/16 unmarked<=0 4/4 precision=1.000
pivot fallback marked 32/48 >0 9/32 unmarked<=0 24/44
combined marked>0 25/48 unmarked<=0 28/48
Pivot-fallback marked files:
- `01-harbour` draw 1: The ferry was so lr<=0=-0.0182
- `01-harbour` draw 2: The ferry was over lr<=0=-0.0187
- `01-harbour` draw 3: The ferry was in lr<=0=-0.0172
- `01-harbour` draw 4: The ferry was in lr<=0=-0.0172
- `02-night-bus` draw 1: The bus is a lr<=0=-0.0066
- `02-night-bus` draw 2: The bus is all lr<=0=-0.0112
- `02-night-bus` draw 3: After two and a lr<=0=-0.0214
- `02-night-bus` draw 4: The bus is all lr<=0=-0.0112
- `03-library` draw 1: Closing is the lr<=0=-0.0460
- `03-library` draw 2: Closing is the lr<=0=-0.0460
- `03-library` draw 3: Closing is the lr<=0=-0.0460
- `03-library` draw 4: Closing is the lr<=0=-0.0460
- `04-market` draw 1: The dog gave me lr>0=0.0020
- `04-market` draw 2: The dog gave me lr>0=0.0020
- `04-market` draw 3: The dog gave me lr>0=0.0020
- `04-market` draw 4: The dog gave me lr>0=0.0020
- `06-station` draw 4: The conductor turned and lr>0=0.0014
- `08-letter` draw 1: The second version is lr>0=0.0088
- `08-letter` draw 2: Now in the second lr>0=0.0050
- `08-letter` draw 3: While working on the lr>0=0.0007
- `08-letter` draw 4: The second version is lr>0=0.0088
- `10-office` draw 1: The printer worked. lr<=0=-0.0005
- `10-office` draw 3: The printer worked. lr<=0=-0.0005
- `10-office` draw 4: The printer worked better lr<=0=-0.0026
- `11-garden` draw 1: Now a little after lr<=0=-0.0082
- `11-garden` draw 2: The car is really lr<=0=-0.0071
- `11-garden` draw 3: The car is really lr<=0=-0.0071
- `11-garden` draw 4: Now a little after lr<=0=-0.0082
- `12-ferry-queue` draw 1: The ferry was so lr<=0=-0.0051
- `12-ferry-queue` draw 2: The ferry was so lr<=0=-0.0051
- `12-ferry-queue` draw 3: The ferry was so lr<=0=-0.0051
- `12-ferry-queue` draw 4: The ferry was waiting lr<=0=-0.0067

postokbackoff auc=0.597 mean_pos=-0.0717 mean_neg=-0.8812 diff=0.8095 pos>0=16/48 neg<=0=44/48 perm_p=0.003998 binom_p=0.9934 youden_t=0.8723 youden_sens=0.312 youden_spec=1.000 J=0.312
postokbackoff zeros=9/48 vs 16/48 decided_tp=16 fn=23 fp=4 tn=28 precision=0.800 decided_acc=0.620
postokbackoff prompts_marked_above=6/12 instance=key-free-postokbackoff used_keys=False
pivot-lda auc=0.509 mean_pos=-0.0047 mean_neg=-0.0035 diff=-0.0013 pos>0=24/48 neg<=0=25/48 perm_p=0.6922 binom_p=0.5573 youden_t=0.0019 youden_sens=0.458 youden_spec=0.646 J=0.104
pivot-lda zeros=0/48 vs 0/48 decided_tp=24 fn=24 fp=23 tn=25 precision=0.511 decided_acc=0.510
pivot-lda prompts_marked_above=8/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.517 mean_pos=-0.5547 mean_neg=-0.8776 diff=0.3229 pos>0=20/48 neg<=0=24/48 perm_p=0.4168 binom_p=0.9033 youden_t=4.3932 youden_sens=0.292 youden_spec=0.875 J=0.167
pivot-rank zeros=0/48 vs 0/48 decided_tp=20 fn=28 fp=24 tn=24 precision=0.455 decided_acc=0.458
pivot-rank prompts_marked_above=6/12 instance=key-free-pivot-rank used_keys=False
pivot-lda-entropy auc=0.432 mean_pos=-0.0016 mean_neg=-0.0003 diff=-0.0013 pos>0=22/48 neg<=0=23/48 perm_p=0.8981 binom_p=0.7646 youden_t=0.0025 youden_sens=0.333 youden_spec=0.771 J=0.104
pivot-lda-entropy zeros=0/48 vs 0/48 decided_tp=22 fn=26 fp=25 tn=23 precision=0.468 decided_acc=0.469
pivot-lda-entropy prompts_marked_above=5/12 instance=key-free-pivot-lda-entropy used_keys=False
pivot-rank-entropy auc=0.466 mean_pos=1.9244 mean_neg=1.9568 diff=-0.0323 pos>0=32/48 neg<=0=15/48 perm_p=0.5357 binom_p=0.01465 youden_t=-3.6443 youden_sens=0.875 youden_spec=0.188 J=0.062
pivot-rank-entropy zeros=0/48 vs 0/48 decided_tp=32 fn=16 fp=33 tn=15 precision=0.492 decided_acc=0.490
pivot-rank-entropy prompts_marked_above=4/12 instance=key-free-pivot-rank-entropy used_keys=False
cascade auc=0.616 mean_pos=0.9634 mean_neg=-0.2077 diff=1.1710 pos>0=25/48 neg<=0=28/48 perm_p=0.0004998 binom_p=0.4427 youden_t=0.0081 youden_sens=0.375 youden_spec=0.979 J=0.354
cascade zeros=0/48 vs 0/48 decided_tp=25 fn=23 fp=20 tn=28 precision=0.556 decided_acc=0.552
cascade prompts_marked_above=10/12 instance=key-free-cascade used_keys=False
