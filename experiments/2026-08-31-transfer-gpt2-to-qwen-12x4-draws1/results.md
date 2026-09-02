# Key-free transfer

transfer n_methods=2 train=experiments/2026-08-17-pair-12x4 test=experiments/2026-08-31-pair-qwen-12x4 n_train=12 n_test=12 overlap_mode=keep dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 6/12 | 0.455 | 1/12 | 7/12 | 0.3113 | 0.0583 |
| hashpool | 7/12 | 0.507 | 5/12 | 7/12 | 0.3523 | 0.0021 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0000 | 1/12 | 7/12 | 0.083 | 0.583 |
| hashpool | in-sample-youden | 0.0000 | 5/12 | 7/12 | 0.417 | 0.583 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.455 mean_pos=0.2255 mean_neg=0.1672 diff=0.0583 pos>0=1/12 neg<=0=7/12 perm_p=0.3113 binom_p=0.9998 youden_t=-0.0425 youden_sens=0.833 youden_spec=0.333 J=0.167
hits prompts_marked_above=6/12 instance=key-free-hits used_keys=False
hashpool auc=0.507 mean_pos=-0.0007 mean_neg=-0.0029 diff=0.0021 pos>0=5/12 neg<=0=7/12 perm_p=0.3523 binom_p=0.8062 youden_t=-0.0196 youden_sens=1.000 youden_spec=0.250 J=0.250
hashpool prompts_marked_above=7/12 instance=key-free-hashpool used_keys=False
