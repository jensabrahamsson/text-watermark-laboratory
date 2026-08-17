# Claude pre-mark (2026-08)

Control pile **before** announced marking. Sonnet 5 (30 Jun) is not day-one (2 Aug). Retrofit unpublished.

Protocol: [research/paired-corpus.md](../../research/paired-corpus.md).

**A/B core: 40 texts, ~120k characters.** All strings in `PROMPTS` have been run. The exact prompt (plus any “chat only” line) is in `manifest.jsonl`.

## Not A/B

| Files | What |
|---|---|
| 0001–0006 | Duplicates of two T′ (GPT-2→Sonnet). No rerunnable prompt |
| 0014, 0017, 0026, 0027 | Short UI junk from CDP (artifact-chrome). Re-run as 0029–0032 |

## Collect more

Add **new** rows at the bottom of `PROMPTS`. Do not change old strings.

```bash
source .venv/bin/activate
python scripts/collect_claude_premark.py --via applescript --n 0 --pause 25
```

After announced marking: same `PROMPTS` → `experiments/claude-mark-<date>/`. Do not train a detector on this pile alone.

## A/B files

| File | Characters | Topic |
|---|---|---|
| 0007 | 3296 | harbour at dusk |
| 0008 | 3990 | city library |
| 0009 | 2864 | apple tree |
| 0010 | 3502 | rainy commute |
| 0011 | 3796 | houseplants |
| 0012 | 2693 | ferry captain |
| 0013 | 2928 | sourdough |
| 0015 | 2944 | night shift |
| 0016 | 2919 | hardware store |
| 0018 | 2838 | moving house |
| 0019 | 2753 | community radio |
| 0020 | 2711 | bakery |
| 0021 | 2804 | waiting room |
| 0022 | 2958 | ice fishing |
| 0023 | 2761 | bus |
| 0024 | 3120 | fire station |
| 0025 | 2912 | allotment |
| 0028 | 2909 | laundry room |
| 0029 | 3307 | book box |
| 0030 | 3117 | chess club |
| 0031 | 2768 | lighthouse keeper |
| 0032 | 3182 | small-town museum |
| 0033 | 3039 | hotel night |
| 0034 | 3221 | bike repair |
| 0035 | 3046 | choir |
| 0036 | 2994 | caretaker |
| 0037 | 2619 | market stall |
| 0038 | 2906 | rest hut |
| 0039 | 2952 | university corridor |
| 0040 | 2892 | swimming hall in winter |
| 0041 | 2978 | newspaper press |
| 0042 | 2916 | dog walk |
| 0043 | 2966 | fishing village in January |
| 0044 | 2776 | night train |
| 0045 | 2899 | second-hand shop closing |
| 0046 | 2912 | broken piano |
| 0047 | 2935 | rooftop greenhouse |
| 0048 | 3025 | clothesline |
| 0049 | 3090 | ferry in wind |
| 0050 | 2651 | teacher letter |
