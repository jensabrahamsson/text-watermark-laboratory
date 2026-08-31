# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-17-pair-36 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=0 used_keys=False hash_iv=False g_values=False
NEGATIVE CONTROL: training marked/unmarked labels were shuffled per stem. Test labels are real. AUC should collapse toward 0.5. Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 7/12 | 0.611 | 19/48 | 32/48 | 0.05197 | 0.1590 |
| hitmass | 11/12 | 0.615 | 19/48 | 32/48 | 0.004498 | 0.0067 |
| hashpool | 9/12 | 0.639 | 20/48 | 37/48 | 0.01049 | 0.0130 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0000 | 19/48 | 32/48 | 0.396 | 0.667 |
| hitmass | in-sample-youden | 0.0000 | 19/48 | 32/48 | 0.396 | 0.667 |
| hashpool | in-sample-youden | 0.0000 | 20/48 | 37/48 | 0.417 | 0.771 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.611 mean_pos=0.0749 mean_neg=-0.0841 diff=0.1590 pos>0=19/48 neg<=0=32/48 perm_p=0.05197 binom_p=0.9443 youden_t=-0.0012 youden_sens=0.771 youden_spec=0.500 J=0.271
hits prompts_marked_above=7/12 instance=key-free-hits used_keys=False
hitmass auc=0.615 mean_pos=0.0039 mean_neg=-0.0028 diff=0.0067 pos>0=19/48 neg<=0=32/48 perm_p=0.004498 binom_p=0.9443 youden_t=-0.0000 youden_sens=0.792 youden_spec=0.500 J=0.292
hitmass prompts_marked_above=11/12 instance=key-free-hitmass used_keys=False
hashpool auc=0.639 mean_pos=-0.0028 mean_neg=-0.0157 diff=0.0130 pos>0=20/48 neg<=0=37/48 perm_p=0.01049 binom_p=0.9033 youden_t=-0.0053 youden_sens=0.521 youden_spec=0.750 J=0.271
hashpool prompts_marked_above=9/12 instance=key-free-hashpool used_keys=False
