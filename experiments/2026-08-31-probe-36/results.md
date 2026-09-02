# Key-free probe

probe n_methods=9 pair_dir=experiments/2026-08-17-pair-36 context_len=4 model=gpt2 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| unigram | 22/36 | 0.590 | 18/36 | 21/36 | 0.06697 | 0.0177 |
| hard | 20/36 | 0.549 | 20/36 | 18/36 | 0.1594 | 0.0125 |
| backoff | 22/36 | 0.623 | 26/36 | 20/36 | 0.06797 | 0.0293 |
| interpolate | 29/36 | 0.796 | 26/36 | 26/36 | 0.0004998 | 0.1980 |
| hits | 30/36 | 0.886 | 33/36 | 16/36 | 0.0004998 | 0.9062 |
| gated | 31/36 | 0.856 | 32/36 | 16/36 | 0.0004998 | 0.8811 |
| shrinkage | 31/36 | 0.875 | 33/36 | 18/36 | 0.0004998 | 0.9414 |
| mix | 22/36 | 0.628 | 19/36 | 22/36 | 0.04298 | 0.0219 |
| hashpool | 31/36 | 0.877 | 32/36 | 22/36 | 0.0004998 | 0.0533 |

unigram auc=0.590 mean_pos=0.0030 mean_neg=-0.0147 diff=0.0177 pos>0=18/36 neg<=0=21/36 perm_p=0.06697 binom_p=0.566 youden_t=-0.0396 youden_sens=0.861 youden_spec=0.333 J=0.194
unigram prompts_marked_above=22/36 instance=key-free-unigram used_keys=False
hard auc=0.549 mean_pos=0.0142 mean_neg=0.0017 diff=0.0125 pos>0=20/36 neg<=0=18/36 perm_p=0.1594 binom_p=0.3089 youden_t=0.0287 youden_sens=0.389 youden_spec=0.778 J=0.167
hard prompts_marked_above=20/36 instance=key-free-counts used_keys=False
backoff auc=0.623 mean_pos=0.0205 mean_neg=-0.0088 diff=0.0293 pos>0=26/36 neg<=0=20/36 perm_p=0.06797 binom_p=0.005665 youden_t=-0.0131 youden_sens=0.833 youden_spec=0.500 J=0.333
backoff prompts_marked_above=22/36 instance=key-free-backoff used_keys=False
interpolate auc=0.796 mean_pos=0.1190 mean_neg=-0.0790 diff=0.1980 pos>0=26/36 neg<=0=26/36 perm_p=0.0004998 binom_p=0.005665 youden_t=-0.0202 youden_sens=0.778 youden_spec=0.722 J=0.500
interpolate prompts_marked_above=29/36 instance=key-free-interpolate used_keys=False
hits auc=0.886 mean_pos=0.8941 mean_neg=-0.0120 diff=0.9062 pos>0=33/36 neg<=0=16/36 perm_p=0.0004998 binom_p=1.136e-07 youden_t=0.3935 youden_sens=0.833 youden_spec=0.889 J=0.722
hits prompts_marked_above=30/36 instance=key-free-hits used_keys=False
gated auc=0.856 mean_pos=0.8787 mean_neg=-0.0024 diff=0.8811 pos>0=32/36 neg<=0=16/36 perm_p=0.0004998 binom_p=9.708e-07 youden_t=0.5413 youden_sens=0.778 youden_spec=0.917 J=0.694
gated prompts_marked_above=31/36 instance=key-free-gated used_keys=False
shrinkage auc=0.875 mean_pos=0.9316 mean_neg=-0.0098 diff=0.9414 pos>0=33/36 neg<=0=18/36 perm_p=0.0004998 binom_p=1.136e-07 youden_t=0.3778 youden_sens=0.833 youden_spec=0.861 J=0.694
shrinkage prompts_marked_above=31/36 instance=key-free-shrinkage used_keys=False
mix auc=0.628 mean_pos=0.0075 mean_neg=-0.0144 diff=0.0219 pos>0=19/36 neg<=0=22/36 perm_p=0.04298 binom_p=0.434 youden_t=0.0330 youden_sens=0.361 youden_spec=0.889 J=0.250
mix prompts_marked_above=22/36 instance=key-free-mix used_keys=False
hashpool auc=0.877 mean_pos=0.0488 mean_neg=-0.0045 diff=0.0533 pos>0=32/36 neg<=0=22/36 perm_p=0.0004998 binom_p=9.708e-07 youden_t=0.0219 youden_sens=0.722 youden_spec=0.972 J=0.694
hashpool prompts_marked_above=31/36 instance=key-free-hashpool used_keys=False
