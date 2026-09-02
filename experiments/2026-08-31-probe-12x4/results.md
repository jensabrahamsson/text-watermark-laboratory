# Key-free probe

probe n_methods=9 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| unigram | 11/12 | 0.592 | 26/48 | 24/48 | 0.03148 | 0.0243 |
| hard | 10/12 | 0.626 | 29/48 | 23/48 | 0.007496 | 0.0362 |
| backoff | 7/12 | 0.521 | 29/48 | 21/48 | 0.2764 | 0.0120 |
| interpolate | 7/12 | 0.524 | 24/48 | 24/48 | 0.3558 | 0.0155 |
| hits | 11/12 | 0.737 | 28/48 | 30/48 | 0.0004998 | 1.1283 |
| gated | 10/12 | 0.717 | 27/48 | 31/48 | 0.0004998 | 1.2684 |
| shrinkage | 11/12 | 0.734 | 28/48 | 30/48 | 0.0004998 | 1.2017 |
| mix | 6/12 | 0.520 | 25/48 | 21/48 | 0.3293 | 0.0057 |
| hashpool | 11/12 | 0.716 | 35/48 | 29/48 | 0.0004998 | 0.0392 |

unigram auc=0.592 mean_pos=0.0153 mean_neg=-0.0090 diff=0.0243 pos>0=26/48 neg<=0=24/48 perm_p=0.03148 binom_p=0.3327 youden_t=-0.0297 youden_sens=0.792 youden_spec=0.458 J=0.250
unigram prompts_marked_above=11/12 instance=key-free-unigram used_keys=False
hard auc=0.626 mean_pos=0.0328 mean_neg=-0.0034 diff=0.0362 pos>0=29/48 neg<=0=23/48 perm_p=0.007496 binom_p=0.09671 youden_t=-0.0308 youden_sens=0.875 youden_spec=0.458 J=0.333
hard prompts_marked_above=10/12 instance=key-free-counts used_keys=False
backoff auc=0.521 mean_pos=0.0295 mean_neg=0.0175 diff=0.0120 pos>0=29/48 neg<=0=21/48 perm_p=0.2764 binom_p=0.09671 youden_t=0.0930 youden_sens=0.312 youden_spec=0.854 J=0.167
backoff prompts_marked_above=7/12 instance=key-free-backoff used_keys=False
interpolate auc=0.524 mean_pos=0.0070 mean_neg=-0.0085 diff=0.0155 pos>0=24/48 neg<=0=24/48 perm_p=0.3558 binom_p=0.5573 youden_t=0.0658 youden_sens=0.438 youden_spec=0.729 J=0.167
interpolate prompts_marked_above=7/12 instance=key-free-interpolate used_keys=False
hits auc=0.737 mean_pos=1.0491 mean_neg=-0.0793 diff=1.1283 pos>0=28/48 neg<=0=30/48 perm_p=0.0004998 binom_p=0.1562 youden_t=0.0080 youden_sens=0.562 youden_spec=0.854 J=0.417
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
gated auc=0.717 mean_pos=1.1572 mean_neg=-0.1112 diff=1.2684 pos>0=27/48 neg<=0=31/48 perm_p=0.0004998 binom_p=0.2354 youden_t=0.5224 youden_sens=0.500 youden_spec=0.917 J=0.417
gated prompts_marked_above=10/12 instance=key-free-gated used_keys=False
shrinkage auc=0.734 mean_pos=1.1038 mean_neg=-0.0979 diff=1.2017 pos>0=28/48 neg<=0=30/48 perm_p=0.0004998 binom_p=0.1562 youden_t=0.0100 youden_sens=0.542 youden_spec=0.875 J=0.417
shrinkage prompts_marked_above=11/12 instance=key-free-shrinkage used_keys=False
mix auc=0.520 mean_pos=0.0134 mean_neg=0.0077 diff=0.0057 pos>0=25/48 neg<=0=21/48 perm_p=0.3293 binom_p=0.4427 youden_t=0.0412 youden_sens=0.375 youden_spec=0.771 J=0.146
mix prompts_marked_above=6/12 instance=key-free-mix used_keys=False
hashpool auc=0.716 mean_pos=0.0355 mean_neg=-0.0037 diff=0.0392 pos>0=35/48 neg<=0=29/48 perm_p=0.0004998 binom_p=0.001044 youden_t=0.0258 youden_sens=0.500 youden_spec=0.938 J=0.438
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
