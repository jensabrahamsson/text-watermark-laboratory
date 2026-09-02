# Key-free transfer

transfer n_methods=2 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=True
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 12/12 | 0.635 | 13/48 | 48/48 | 0.0004998 | 0.9937 |
| poshits | 12/12 | 0.635 | 13/48 | 48/48 | 0.0004998 | 0.9937 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.5100 | 13/48 | 48/48 | 0.271 | 1.000 |
| poshits | in-sample-youden | 0.5100 | 13/48 | 48/48 | 0.271 | 1.000 |
| hits | nested-youden | 0.0000 | 13/48 | 48/48 | 0.271 | 1.000 |
| hits | nested-fpr10 | 0.0000 | 13/48 | 48/48 | 0.271 | 1.000 |
| poshits | nested-youden | 0.0000 | 13/48 | 48/48 | 0.271 | 1.000 |
| poshits | nested-fpr10 | 0.0000 | 13/48 | 48/48 | 0.271 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.635 mean_pos=0.9937 mean_neg=0.0000 diff=0.9937 pos>0=13/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9996 youden_t=0.0000 youden_sens=0.271 youden_spec=1.000 J=0.271
hits prompts_marked_above=12/12 instance=key-free-hits used_keys=False
poshits auc=0.635 mean_pos=0.9937 mean_neg=0.0000 diff=0.9937 pos>0=13/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9996 youden_t=0.0000 youden_sens=0.271 youden_spec=1.000 J=0.271
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
