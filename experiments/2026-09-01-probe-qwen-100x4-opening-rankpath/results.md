# Key-free probe

probe n_methods=15 pair_dir=experiments/2026-09-01-pair-qwen-100x4 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| unigram | 86/100 | 0.775 | 268/400 | 302/400 | 0.0004998 | 0.9267 |
| hard | 92/100 | 0.843 | 306/400 | 299/400 | 0.0004998 | 1.8482 |
| backoff | 92/100 | 0.818 | 307/400 | 272/400 | 0.0004998 | 1.6951 |
| interpolate | 92/100 | 0.830 | 276/400 | 323/400 | 0.0004998 | 3.2054 |
| hits | 95/100 | 0.873 | 333/400 | 307/400 | 0.0004998 | 2.2916 |
| freqhits | 96/100 | 0.828 | 284/400 | 323/400 | 0.0004998 | 1.9587 |
| hitmass | 93/100 | 0.870 | 333/400 | 307/400 | 0.0004998 | 1.0041 |
| gated | 95/100 | 0.862 | 322/400 | 313/400 | 0.0004998 | 2.2446 |
| shrinkage | 95/100 | 0.872 | 333/400 | 305/400 | 0.0004998 | 2.2992 |
| mix | 92/100 | 0.836 | 302/400 | 289/400 | 0.0004998 | 1.7706 |
| hashpool | 94/100 | 0.864 | 307/400 | 302/400 | 0.0004998 | 1.8373 |
| rankpath | 84/100 | 0.706 | 275/400 | 259/400 | 0.0004998 | 0.3822 |
| rankuni | 53/100 | 0.512 | 188/400 | 234/400 | 0.1609 | 0.0047 |
| stack | 95/100 | 0.864 | 277/400 | 391/400 | 0.0004998 | 0.0037 |
| logit | 95/100 | 0.863 | 286/400 | 376/400 | 0.0004998 | 3.4720 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| unigram | 8/400 | 14/400 | 268/124 | 96/290 | 0.736 |
| hard | 0/400 | 1/400 | 306/94 | 101/298 | 0.752 |
| backoff | 0/400 | 1/400 | 307/93 | 128/271 | 0.706 |
| interpolate | 0/400 | 1/400 | 276/124 | 77/322 | 0.782 |
| hits | 14/400 | 141/400 | 333/53 | 93/166 | 0.782 |
| freqhits | 71/400 | 178/400 | 284/45 | 77/145 | 0.787 |
| hitmass | 14/400 | 141/400 | 333/53 | 93/166 | 0.782 |
| gated | 26/400 | 158/400 | 322/52 | 87/155 | 0.787 |
| shrinkage | 14/400 | 141/400 | 333/53 | 95/164 | 0.778 |
| mix | 0/400 | 1/400 | 302/98 | 111/288 | 0.731 |
| hashpool | 0/400 | 0/400 | 307/93 | 98/302 | 0.758 |
| rankpath | 0/400 | 0/400 | 275/125 | 141/259 | 0.661 |
| rankuni | 0/400 | 0/400 | 188/212 | 166/234 | 0.531 |
| stack | 0/400 | 0/400 | 277/123 | 9/391 | 0.969 |
| logit | 0/400 | 0/400 | 286/114 | 24/376 | 0.923 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| unigram | 220/400 | 350/400 | 0.4256 | 0.550 | 0.875 |
| hard | 261/400 | 366/400 | 0.5540 | 0.652 | 0.915 |
| backoff | 245/400 | 354/400 | 0.6930 | 0.613 | 0.885 |
| interpolate | 254/400 | 367/400 | 0.4094 | 0.635 | 0.917 |
| hits | 331/400 | 347/400 | 0.0192 | 0.828 | 0.868 |
| freqhits | 284/400 | 357/400 | 0.0192 | 0.710 | 0.892 |
| hitmass | 331/400 | 346/400 | 0.0064 | 0.828 | 0.865 |
| gated | 322/400 | 351/400 | 0.0192 | 0.805 | 0.877 |
| shrinkage | 331/400 | 345/400 | 0.0192 | 0.828 | 0.863 |
| mix | 254/400 | 380/400 | 0.6716 | 0.635 | 0.950 |
| hashpool | 277/400 | 373/400 | 0.3937 | 0.693 | 0.932 |
| rankpath | 315/400 | 232/400 | -0.1117 | 0.787 | 0.580 |
| rankuni | 157/400 | 278/400 | 0.0291 | 0.393 | 0.695 |
| stack | 282/400 | 390/400 | -0.0001 | 0.705 | 0.975 |
| logit | 283/400 | 386/400 | 0.1556 | 0.708 | 0.965 |

unigram auc=0.775 mean_pos=0.5445 mean_neg=-0.3822 diff=0.9267 pos>0=268/400 neg<=0=302/400 perm_p=0.0004998 binom_p=4.7e-12 youden_t=0.4304 youden_sens=0.552 youden_spec=0.895 J=0.448
unigram prompts_marked_above=86/100 instance=key-free-unigram used_keys=False
hard auc=0.843 mean_pos=1.3249 mean_neg=-0.5234 diff=1.8482 pos>0=306/400 neg<=0=299/400 perm_p=0.0004998 binom_p=1.371e-27 youden_t=0.5521 youden_sens=0.660 youden_spec=0.917 J=0.578
hard prompts_marked_above=92/100 instance=key-free-counts used_keys=False
backoff auc=0.818 mean_pos=1.3042 mean_neg=-0.3909 diff=1.6951 pos>0=307/400 neg<=0=272/400 perm_p=0.0004998 binom_p=4.172e-28 youden_t=0.7097 youden_sens=0.635 youden_spec=0.915 J=0.550
backoff prompts_marked_above=92/100 instance=key-free-backoff used_keys=False
interpolate auc=0.830 mean_pos=2.0281 mean_neg=-1.1772 diff=3.2054 pos>0=276/400 neg<=0=323/400 perm_p=0.0004998 binom_p=1.061e-14 youden_t=0.4096 youden_sens=0.635 youden_spec=0.922 J=0.558
interpolate prompts_marked_above=92/100 instance=key-free-interpolate used_keys=False
hits auc=0.873 mean_pos=1.9200 mean_neg=-0.3717 diff=2.2916 pos>0=333/400 neg<=0=307/400 perm_p=0.0004998 binom_p=8.221e-44 youden_t=0.0192 youden_sens=0.828 youden_spec=0.868 J=0.695
hits prompts_marked_above=95/100 instance=key-free-hits used_keys=False
freqhits auc=0.828 mean_pos=1.6630 mean_neg=-0.2957 diff=1.9587 pos>0=284/400 neg<=0=323/400 perm_p=0.0004998 binom_p=1.147e-17 youden_t=0.0192 youden_sens=0.710 youden_spec=0.892 J=0.603
freqhits prompts_marked_above=96/100 instance=key-free-freqhits used_keys=False
hitmass auc=0.870 mean_pos=0.7936 mean_neg=-0.2105 diff=1.0041 pos>0=333/400 neg<=0=307/400 perm_p=0.0004998 binom_p=8.221e-44 youden_t=0.0064 youden_sens=0.828 youden_spec=0.865 J=0.692
hitmass prompts_marked_above=93/100 instance=key-free-hitmass used_keys=False
gated auc=0.862 mean_pos=1.9163 mean_neg=-0.3283 diff=2.2446 pos>0=322/400 neg<=0=313/400 perm_p=0.0004998 binom_p=1.318e-36 youden_t=0.0192 youden_sens=0.805 youden_spec=0.877 J=0.683
gated prompts_marked_above=95/100 instance=key-free-gated used_keys=False
shrinkage auc=0.872 mean_pos=1.9300 mean_neg=-0.3692 diff=2.2992 pos>0=333/400 neg<=0=305/400 perm_p=0.0004998 binom_p=8.221e-44 youden_t=0.0192 youden_sens=0.828 youden_spec=0.863 J=0.690
shrinkage prompts_marked_above=95/100 instance=key-free-shrinkage used_keys=False
mix auc=0.836 mean_pos=1.2895 mean_neg=-0.4810 diff=1.7706 pos>0=302/400 neg<=0=289/400 perm_p=0.0004998 binom_p=1.393e-25 youden_t=0.6719 youden_sens=0.637 youden_spec=0.953 J=0.590
mix prompts_marked_above=92/100 instance=key-free-mix used_keys=False
hashpool auc=0.864 mean_pos=1.3916 mean_neg=-0.4457 diff=1.8373 pos>0=307/400 neg<=0=302/400 perm_p=0.0004998 binom_p=4.172e-28 youden_t=0.3897 youden_sens=0.710 youden_spec=0.935 J=0.645
hashpool prompts_marked_above=94/100 instance=key-free-hashpool used_keys=False
rankpath auc=0.706 mean_pos=0.1467 mean_neg=-0.2356 diff=0.3822 pos>0=275/400 neg<=0=259/400 perm_p=0.0004998 binom_p=2.365e-14 youden_t=-0.1117 youden_sens=0.787 youden_spec=0.583 J=0.370
rankpath prompts_marked_above=84/100 instance=key-free-rankpath used_keys=False
rankuni auc=0.512 mean_pos=-0.0002 mean_neg=-0.0049 diff=0.0047 pos>0=188/400 neg<=0=234/400 perm_p=0.1609 binom_p=0.8944 youden_t=0.0290 youden_sens=0.400 youden_spec=0.698 J=0.098
rankuni prompts_marked_above=53/100 instance=key-free-rankuni used_keys=False
stack auc=0.864 mean_pos=0.0019 mean_neg=-0.0019 diff=0.0037 pos>0=277/400 neg<=0=391/400 perm_p=0.0004998 binom_p=4.708e-15 youden_t=-0.0001 youden_sens=0.705 youden_spec=0.978 J=0.683
stack prompts_marked_above=95/100 instance=key-free-stack used_keys=False
logit auc=0.863 mean_pos=2.2090 mean_neg=-1.2630 diff=3.4720 pos>0=286/400 neg<=0=376/400 perm_p=0.0004998 binom_p=1.848e-18 youden_t=0.1549 youden_sens=0.715 youden_spec=0.968 J=0.683
logit prompts_marked_above=95/100 instance=key-free-logit used_keys=False
