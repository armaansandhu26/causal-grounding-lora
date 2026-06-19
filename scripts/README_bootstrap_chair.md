# CHAIR Bootstrap / Significance

Run this locally after copying SPIN outputs into `results/`:

```bash
./.venv/bin/python scripts/bootstrap_chair_significance.py --scorer spacy
```

If the SPIN caption files are still in `cache/`, pass:

```bash
./.venv/bin/python scripts/bootstrap_chair_significance.py --scorer spacy --caption-dir cache
```

Required SPIN files:

```text
results/baseline_captions_budget64.json
results/spin_captions_budget64.json
results/baseline_captions_budget128.json
results/spin_captions_budget128.json
```

Outputs:

```text
results/bootstrap_chair_significance.json
results/bootstrap_chair_significance.md
```

Use `--scorer spacy` for paper numbers. It matches the notebook CHAIR scorer's noun/proper-noun filtering. If local spaCy is missing, install spaCy and the English model in the active environment, or run on Colab after the captions are generated.

For a quick file-plumbing smoke test only:

```bash
./.venv/bin/python scripts/bootstrap_chair_significance.py --scorer regex --n-boot 500 --n-perm 1000
```
