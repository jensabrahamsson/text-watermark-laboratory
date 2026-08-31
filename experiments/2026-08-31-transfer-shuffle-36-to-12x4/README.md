# Negative control: 50% train-label shuffle

Same 36→12×4 split. Exactly half of the 24 training stems have marked and
unmarked sides swapped (`--shuffle-labels --shuffle-seed 0`). Test labels
are real. Nested thresholds skipped. Frozen tables omitted: this is not a
detector.

| Method | Prompt wins | File AUC | Marked `> 0` | perm p |
|---|---|---|---|---|
| hits | 7/12 | 0.611 | 19/48 | 0.052 |
| hitmass | 11/12 | 0.615 | 19/48 | 0.0045 |
| hashpool | 9/12 | 0.639 | 20/48 | 0.010 |

Isolated sign at 0 falls to chance (19–20/48). File AUC drops from ~0.77 to
~0.61–0.64. Residual ranking is not zero: 50% correct training labels still
leave a weak direction. Prompt-grain wins on n=12 are noisy (hitmass 11/12
here is **not** a detection result). Compare with the unshuffled nested run
in `../2026-08-31-transfer-nested-36-to-12x4/`.
