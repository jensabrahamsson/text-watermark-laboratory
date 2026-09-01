# Key-free transfer

transfer n_methods=4 train=experiments/2026-08-31-pair-36x4+experiments/2026-08-31-pair-long12x4+experiments/2026-08-31-pair-tails12x4+experiments/2026-08-31-pair-family12x4 test=experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashtok | 10/12 | 0.844 | 35/48 | 39/48 | 0.0004998 | 2.3996 |
| hashtoklen | 12/12 | 0.500 | 0/48 | 48/48 | 1 | 0.0000 |
| hashtoklenbackoff | 11/12 | 0.826 | 35/48 | 38/48 | 0.0004998 | 2.1100 |
| hashtoklenbackoff2 | 9/12 | 0.732 | 30/48 | 42/48 | 0.0004998 | 1.4491 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashtok | 5/48 | 21/48 | 35/8 | 9/18 | 0.795 |
| hashtoklen | 48/48 | 48/48 | 0/0 | 0/0 | nan |
| hashtoklenbackoff | 4/48 | 12/48 | 35/9 | 10/26 | 0.778 |
| hashtoklenbackoff2 | 8/48 | 31/48 | 30/10 | 6/11 | 0.833 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashtok is the hashpool analog of tokhits. None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashtok | in-sample-youden | 0.0405 | 35/48 | 40/48 | 0.729 | 0.833 |
| hashtoklen | in-sample-youden | 0.0000 | 0/48 | 48/48 | 0.000 | 1.000 |
| hashtoklenbackoff | in-sample-youden | 0.0300 | 35/48 | 39/48 | 0.729 | 0.812 |
| hashtoklenbackoff2 | in-sample-youden | 0.6221 | 29/48 | 44/48 | 0.604 | 0.917 |
| hashtok | nested-youden | 0.8216 | 33/48 | 45/48 | 0.688 | 0.938 |
| hashtok | nested-fpr10 | 0.6732 | 35/48 | 44/48 | 0.729 | 0.917 |
| hashtoklen | nested-youden | 0.0000 | 0/48 | 48/48 | 0.000 | 1.000 |
| hashtoklen | nested-fpr10 | 0.0000 | 0/48 | 48/48 | 0.000 | 1.000 |
| hashtoklenbackoff | nested-youden | 0.1574 | 35/48 | 40/48 | 0.729 | 0.833 |
| hashtoklenbackoff | nested-fpr10 | 0.8405 | 29/48 | 44/48 | 0.604 | 0.917 |
| hashtoklenbackoff2 | nested-youden | 0.2528 | 30/48 | 43/48 | 0.625 | 0.896 |
| hashtoklenbackoff2 | nested-fpr10 | 0.2528 | 30/48 | 43/48 | 0.625 | 0.896 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashtok auc=0.844 mean_pos=1.8408 mean_neg=-0.5588 diff=2.3996 pos>0=35/48 neg<=0=39/48 perm_p=0.0004998 binom_p=0.001044 youden_t=0.7445 youden_sens=0.729 youden_spec=0.938 J=0.667
hashtok zeros=5/48 vs 21/48 decided_tp=35 fn=8 fp=9 tn=18 precision=0.795 decided_acc=0.757
hashtok prompts_marked_above=10/12 instance=key-free-hashtok used_keys=False
hashtoklen auc=0.500 mean_pos=0.0000 mean_neg=0.0000 diff=0.0000 pos>0=0/48 neg<=0=48/48 perm_p=1 binom_p=1 youden_t=0.0000 youden_sens=0.000 youden_spec=1.000 J=0.000
hashtoklen zeros=48/48 vs 48/48 decided_tp=0 fn=0 fp=0 tn=0 precision=nan decided_acc=nan
hashtoklen prompts_marked_above=12/12 instance=key-free-hashtoklen used_keys=False
hashtoklenbackoff auc=0.826 mean_pos=1.4961 mean_neg=-0.6139 diff=2.1100 pos>0=35/48 neg<=0=38/48 perm_p=0.0004998 binom_p=0.001044 youden_t=0.7349 youden_sens=0.688 youden_spec=0.917 J=0.604
hashtoklenbackoff zeros=4/48 vs 12/48 decided_tp=35 fn=9 fp=10 tn=26 precision=0.778 decided_acc=0.762
hashtoklenbackoff prompts_marked_above=11/12 instance=key-free-hashtoklenbackoff used_keys=False
hashtoklenbackoff2 auc=0.732 mean_pos=1.2069 mean_neg=-0.2422 diff=1.4491 pos>0=30/48 neg<=0=42/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.1383 youden_sens=0.625 youden_spec=0.896 J=0.521
hashtoklenbackoff2 zeros=8/48 vs 31/48 decided_tp=30 fn=10 fp=6 tn=11 precision=0.833 decided_acc=0.719
hashtoklenbackoff2 prompts_marked_above=9/12 instance=key-free-hashtoklenbackoff2 used_keys=False
