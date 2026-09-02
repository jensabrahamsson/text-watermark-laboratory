# Key-free transfer

transfer n_methods=1 train=experiments/2026-09-01-pair-grok12x4 test=experiments/2026-08-31-pair-36x4 n_train=12 n_test=36 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. ranking_without_isolated_tp counts prompt wins with no marked file lr>0; do not read prompt wins as isolated recall. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| interpolate | 24/36 | 0.611 | 78/144 | 95/144 | 0.001499 | 0.0844 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| interpolate | 24/36 | 0/24 | 11 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| interpolate | 0/144 | 0/144 | 78/66 | 49/95 | 0.614 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| interpolate | in-sample-youden | 0.0000 | 78/144 | 95/144 | 0.542 | 0.660 |
| interpolate | nested-youden | 0.1088 | 50/144 | 115/144 | 0.347 | 0.799 |
| interpolate | nested-fpr10 | 0.1382 | 44/144 | 123/144 | 0.306 | 0.854 |

interpolate auc=0.611 mean_pos=0.0295 mean_neg=-0.0549 diff=0.0844 pos>0=78/144 neg<=0=95/144 perm_p=0.001499 binom_p=0.1797 youden_t=0.0126 youden_sens=0.528 youden_spec=0.715 J=0.243
interpolate zeros=0/144 vs 0/144 decided_tp=78 fn=66 fp=49 tn=95 precision=0.614 decided_acc=0.601
interpolate prompts_marked_above=24/36 ranking_without_isolated_tp=0/24 ranking_losses_with_isolated_tp=11 instance=key-free-interpolate used_keys=False
