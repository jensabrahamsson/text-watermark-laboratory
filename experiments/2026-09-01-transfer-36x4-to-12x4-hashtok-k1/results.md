# Key-free transfer

transfer n_methods=1 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=1 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashtok | 7/12 | 0.651 | 25/48 | 35/48 | 0.002999 | 0.0650 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashtok | 0/48 | 0/48 | 25/23 | 13/35 | 0.658 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashtok | in-sample-youden | 0.0000 | 25/48 | 35/48 | 0.521 | 0.729 |
| hashtok | nested-youden | 0.0664 | 18/48 | 45/48 | 0.375 | 0.938 |
| hashtok | nested-fpr10 | 0.1528 | 8/48 | 46/48 | 0.167 | 0.958 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashtok auc=0.651 mean_pos=0.0232 mean_neg=-0.0418 diff=0.0650 pos>0=25/48 neg<=0=35/48 perm_p=0.002999 binom_p=0.4427 youden_t=0.0582 youden_sens=0.375 youden_spec=0.938 J=0.312
hashtok zeros=0/48 vs 0/48 decided_tp=25 fn=23 fp=13 tn=35 precision=0.658 decided_acc=0.625
hashtok prompts_marked_above=7/12 instance=key-free-hashtok used_keys=False
