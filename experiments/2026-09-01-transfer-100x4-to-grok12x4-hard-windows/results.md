# Key-free transfer

transfer n_methods=1 train=experiments/2026-09-01-pair-100x4 test=experiments/2026-09-01-pair-grok12x4 n_train=100 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. ranking_without_isolated_tp counts prompt wins with no marked file lr>0; do not read prompt wins as isolated recall. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| interpolate | 11/12 | 0.683 | 27/48 | 28/48 | 0.002999 | 0.1264 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| interpolate | 11/12 | 0/11 | 1 (112-taxi-rank) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| interpolate | 0/48 | 0/48 | 27/21 | 20/28 | 0.574 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| interpolate | in-sample-youden | 0.0000 | 27/48 | 28/48 | 0.562 | 0.583 |
| interpolate | nested-youden | 0.0889 | 22/48 | 41/48 | 0.458 | 0.854 |
| interpolate | nested-fpr10 | 0.1452 | 17/48 | 45/48 | 0.354 | 0.938 |

| window tokens | method | prompt wins | file auc | marked>0 | unmarked<=0 |
|---|---|---|---|---|---|
| 0:4 | interpolate | 7/12 | 0.619 | 23/48 | 31/48 |
| 4:16 | interpolate | 4/12 | 0.467 | 21/48 | 26/48 |
| 16:32 | interpolate | 8/12 | 0.497 | 23/48 | 23/48 |
| 32:64 | interpolate | 9/12 | 0.630 | 26/48 | 28/48 |
| 64:128 | interpolate | 9/12 | 0.616 | 26/48 | 31/48 |

interpolate auc=0.683 mean_pos=0.0450 mean_neg=-0.0814 diff=0.1264 pos>0=27/48 neg<=0=28/48 perm_p=0.002999 binom_p=0.2354 youden_t=0.0942 youden_sens=0.458 youden_spec=0.896 J=0.354
interpolate zeros=0/48 vs 0/48 decided_tp=27 fn=21 fp=20 tn=28 precision=0.574 decided_acc=0.573
interpolate prompts_marked_above=11/12 ranking_without_isolated_tp=0/11 ranking_losses_with_isolated_tp=1 instance=key-free-interpolate used_keys=False
