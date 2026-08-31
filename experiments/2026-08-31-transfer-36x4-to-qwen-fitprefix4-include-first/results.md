# Key-free transfer

transfer n_methods=2 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-31-pair-qwen-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=True prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| first | 7/12 | 0.561 | 0/48 | 48/48 | 0.1344 | 0.2171 |
| poshits | 8/12 | 0.584 | 0/48 | 48/48 | 0.1224 | 0.2275 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| first | in-sample-youden | 0.0000 | 0/48 | 48/48 | 0.000 | 1.000 |
| poshits | in-sample-youden | 0.4216 | 0/48 | 48/48 | 0.000 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

first auc=0.561 mean_pos=-1.0516 mean_neg=-1.2686 diff=0.2171 pos>0=0/48 neg<=0=48/48 perm_p=0.1344 binom_p=1 youden_t=-2.1972 youden_sens=0.917 youden_spec=0.333 J=0.250
first prompts_marked_above=7/12 instance=key-free-first used_keys=False
poshits auc=0.584 mean_pos=-0.8415 mean_neg=-1.0690 diff=0.2275 pos>0=0/48 neg<=0=48/48 perm_p=0.1224 binom_p=1 youden_t=-2.0948 youden_sens=0.917 youden_spec=0.354 J=0.271
poshits prompts_marked_above=8/12 instance=key-free-poshits used_keys=False
