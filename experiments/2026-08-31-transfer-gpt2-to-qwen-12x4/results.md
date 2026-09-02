# Key-free transfer

transfer n_methods=4 train=experiments/2026-08-17-pair-12x4 test=experiments/2026-08-31-pair-qwen-12x4 n_train=12 n_test=12 overlap_mode=keep dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 5/12 | 0.355 | 5/48 | 29/48 | 0.2124 | 0.1838 |
| hitmass | 5/12 | 0.356 | 5/48 | 29/48 | 0.2484 | 0.0013 |
| hashpool | 8/12 | 0.568 | 17/48 | 32/48 | 0.06847 | 0.0067 |
| logit | 5/12 | 0.451 | 4/48 | 46/48 | 0.2004 | 0.1838 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | -0.2541 | 35/48 | 5/48 | 0.729 | 0.104 |
| hitmass | in-sample-youden | -0.0086 | 45/48 | 4/48 | 0.938 | 0.083 |
| hashpool | in-sample-youden | 0.0000 | 17/48 | 32/48 | 0.354 | 0.667 |
| logit | in-sample-youden | 0.0000 | 4/48 | 46/48 | 0.083 | 0.958 |
| hits | nested-youden | 0.0080 | 4/48 | 34/48 | 0.083 | 0.708 |
| hits | nested-fpr10 | 0.5048 | 4/48 | 47/48 | 0.083 | 0.979 |
| hitmass | nested-youden | 0.0089 | 4/48 | 47/48 | 0.083 | 0.979 |
| hitmass | nested-fpr10 | 0.0088 | 4/48 | 46/48 | 0.083 | 0.958 |
| hashpool | nested-youden | 0.0258 | 4/48 | 47/48 | 0.083 | 0.979 |
| hashpool | nested-fpr10 | 0.0251 | 4/48 | 47/48 | 0.083 | 0.979 |
| logit | nested-youden | 0.7935 | 4/48 | 47/48 | 0.083 | 0.979 |
| logit | nested-fpr10 | 0.3785 | 4/48 | 47/48 | 0.083 | 0.979 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.355 mean_pos=0.0868 mean_neg=-0.0970 diff=0.1838 pos>0=5/48 neg<=0=29/48 perm_p=0.2124 binom_p=1 youden_t=-1.2164 youden_sens=1.000 youden_spec=0.083 J=0.083
hits prompts_marked_above=5/12 instance=key-free-hits used_keys=False
hitmass auc=0.356 mean_pos=0.0003 mean_neg=-0.0009 diff=0.0013 pos>0=5/48 neg<=0=29/48 perm_p=0.2484 binom_p=1 youden_t=-0.0151 youden_sens=1.000 youden_spec=0.083 J=0.083
hitmass prompts_marked_above=5/12 instance=key-free-hitmass used_keys=False
hashpool auc=0.568 mean_pos=-0.0026 mean_neg=-0.0093 diff=0.0067 pos>0=17/48 neg<=0=32/48 perm_p=0.06847 binom_p=0.9853 youden_t=-0.0138 youden_sens=0.688 youden_spec=0.500 J=0.188
hashpool prompts_marked_above=8/12 instance=key-free-hashpool used_keys=False
logit auc=0.451 mean_pos=-0.2647 mean_neg=-0.4485 diff=0.1838 pos>0=4/48 neg<=0=46/48 perm_p=0.2004 binom_p=1 youden_t=-0.3581 youden_sens=0.500 youden_spec=0.583 J=0.083
logit prompts_marked_above=5/12 instance=key-free-logit used_keys=False
