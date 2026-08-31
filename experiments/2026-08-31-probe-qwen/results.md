# Key-free probe

probe n_methods=9 pair_dir=experiments/2026-08-17-pair-qwen context_len=4 model=Qwen/Qwen2-1.5B-Instruct used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| unigram | 7/12 | 0.590 | 4/12 | 10/12 | 0.1224 | 0.0382 |
| hard | 6/12 | 0.625 | 4/12 | 10/12 | 0.1059 | 0.0404 |
| backoff | 5/12 | 0.542 | 5/12 | 8/12 | 0.2789 | 0.0251 |
| interpolate | 5/12 | 0.535 | 4/12 | 7/12 | 0.2789 | 0.0547 |
| hits | 8/12 | 0.417 | 1/12 | 7/12 | 0.8921 | -0.0931 |
| gated | 8/12 | 0.417 | 1/12 | 7/12 | 0.8921 | -0.0931 |
| shrinkage | 8/12 | 0.417 | 1/12 | 7/12 | 0.8921 | -0.0931 |
| mix | 6/12 | 0.590 | 4/12 | 10/12 | 0.1929 | 0.0299 |
| hashpool | 10/12 | 0.750 | 11/12 | 6/12 | 0.01699 | 0.0101 |

unigram auc=0.590 mean_pos=-0.0440 mean_neg=-0.0822 diff=0.0382 pos>0=4/12 neg<=0=10/12 perm_p=0.1224 binom_p=0.927 youden_t=-0.0231 youden_sens=0.500 youden_spec=0.833 J=0.333
unigram prompts_marked_above=7/12 instance=key-free-unigram used_keys=False
hard auc=0.625 mean_pos=-0.0409 mean_neg=-0.0813 diff=0.0404 pos>0=4/12 neg<=0=10/12 perm_p=0.1059 binom_p=0.927 youden_t=-0.0231 youden_sens=0.500 youden_spec=0.833 J=0.333
hard prompts_marked_above=6/12 instance=key-free-counts used_keys=False
backoff auc=0.542 mean_pos=0.0035 mean_neg=-0.0216 diff=0.0251 pos>0=5/12 neg<=0=8/12 perm_p=0.2789 binom_p=0.8062 youden_t=-0.0117 youden_sens=0.583 youden_spec=0.667 J=0.250
backoff prompts_marked_above=5/12 instance=key-free-backoff used_keys=False
interpolate auc=0.535 mean_pos=-0.0030 mean_neg=-0.0576 diff=0.0547 pos>0=4/12 neg<=0=7/12 perm_p=0.2789 binom_p=0.927 youden_t=0.1091 youden_sens=0.250 youden_spec=0.917 J=0.167
interpolate prompts_marked_above=5/12 instance=key-free-interpolate used_keys=False
hits auc=0.417 mean_pos=0.0011 mean_neg=0.0942 diff=-0.0931 pos>0=1/12 neg<=0=7/12 perm_p=0.8921 binom_p=0.9998 youden_t=-0.0018 youden_sens=1.000 youden_spec=0.167 J=0.167
hits prompts_marked_above=8/12 instance=key-free-hits used_keys=False
gated auc=0.417 mean_pos=0.0011 mean_neg=0.0942 diff=-0.0931 pos>0=1/12 neg<=0=7/12 perm_p=0.8921 binom_p=0.9998 youden_t=-0.0018 youden_sens=1.000 youden_spec=0.167 J=0.167
gated prompts_marked_above=8/12 instance=key-free-gated used_keys=False
shrinkage auc=0.417 mean_pos=0.0011 mean_neg=0.0942 diff=-0.0931 pos>0=1/12 neg<=0=7/12 perm_p=0.8921 binom_p=0.9998 youden_t=-0.0018 youden_sens=1.000 youden_spec=0.167 J=0.167
shrinkage prompts_marked_above=8/12 instance=key-free-shrinkage used_keys=False
mix auc=0.590 mean_pos=-0.0218 mean_neg=-0.0518 diff=0.0299 pos>0=4/12 neg<=0=10/12 perm_p=0.1929 binom_p=0.927 youden_t=0.0122 youden_sens=0.333 youden_spec=1.000 J=0.333
mix prompts_marked_above=6/12 instance=key-free-mix used_keys=False
hashpool auc=0.750 mean_pos=0.0078 mean_neg=-0.0024 diff=0.0101 pos>0=11/12 neg<=0=6/12 perm_p=0.01699 binom_p=0.003174 youden_t=0.0010 youden_sens=0.917 youden_spec=0.583 J=0.500
hashpool prompts_marked_above=10/12 instance=key-free-hashpool used_keys=False
