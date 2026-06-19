# Paper-Ready Result Tables

Percent reduction is computed as `(baseline - method) / baseline * 100`.
Positive values mean lower hallucination than baseline (**good**). Negative values mean the method increased hallucination (**bad**).

## Main 400-Image Comparison

Source: `results/stage4_400img_results.json`. All methods are evaluated on the same 400 held-out COCO val2014 images.

| Method | CHAIRs | CHAIRs reduction vs baseline | CHAIRi | CHAIRi reduction vs baseline |
|---|---:|---:|---:|---:|
| Baseline | 0.3700 | 0.0% (reference) | 0.1558 | 0.0% (reference) |
| Stage 2: LoRA | 0.2650 | 28.4% (good) | 0.1043 | 33.1% (good) |
| Stage 3: Grounding | 0.3100 | 16.2% (good) | 0.1407 | 9.7% (good) |
| Stage 4: LoRA + Grounding | 0.2300 | 37.8% (good) | 0.0958 | 38.5% (good) |

### Main Comparison With Bootstrap CIs

Source: `results/bootstrap_chair_significance.json`. Scorer: spaCy notebook-matching CHAIR scorer. Bootstrap resamples: 5000.

| Method | n | CHAIRs 95% CI | CHAIRi 95% CI | Avg length |
|---|---:|---:|---:|---:|
| Baseline | 400 | 0.3700 [0.3225, 0.4175] | 0.1558 [0.1327, 0.1800] | 61.1 |
| Stage 2: LoRA | 400 | 0.2650 [0.2225, 0.3075] | 0.1043 [0.0857, 0.1245] | 27.6 |
| Stage 3: Grounding | 400 | 0.3100 [0.2650, 0.3575] | 0.1407 [0.1174, 0.1654] | 62.1 |
| Stage 4: LoRA + Grounding | 400 | 0.2300 [0.1900, 0.2700] | 0.0958 [0.0761, 0.1163] | 29.6 |

### Main Paired Deltas vs Baseline

Negative deltas are good because lower CHAIR is better. P-values are paired sign-flip permutation tests with 10000 resamples.

| Method | Delta CHAIRs | Delta CHAIRi |
|---|---:|---:|
| Stage 2: LoRA | -0.1050 [-0.1575, -0.0550], p=0.0002 | -0.0515 [-0.0738, -0.0295], p=0.0001 |
| Stage 3: Grounding | -0.0600 [-0.1125, -0.0075], p=0.0287 | -0.0151 [-0.0386, +0.0082], p=0.2096 |
| Stage 4: LoRA + Grounding | -0.1400 [-0.1900, -0.0900], p=0.0001 | -0.0601 [-0.0837, -0.0369], p=0.0001 |

Suggested sentence:

> On the 400-image held-out split, Stage 4 reduces CHAIRs by 37.8% and CHAIRi by 38.5% relative to the greedy LLaVA baseline. The paired reduction is significant for both CHAIRs (delta=-0.1400, 95% CI [-0.1900, -0.0900], p=0.0001) and CHAIRi (delta=-0.0601, 95% CI [-0.0837, -0.0369], p=0.0001).

## SPIN Fixed-Budget Comparison

Source: `results/spin_comparison.json`. SPIN uses the paper-style LLaVA-1.5-7B configuration: layers 0-32, suppressed-head ratio r=0.05, alpha=0.08. All budgets use the same 400 held-out images as the main Stage 4 comparison.

| Max new tokens | Method | CHAIRs | CHAIRs reduction vs baseline | CHAIRi | CHAIRi reduction vs baseline | Avg length |
|---:|---|---:|---:|---:|---:|---:|
| 64 | Baseline | 0.2800 | 0.0% (reference) | 0.1066 | 0.0% (reference) | 49.5 |
| 64 | SPIN | 0.3025 | -8.0% (bad) | 0.1216 | -14.1% (bad) | 48.8 |
| 80 | Baseline | 0.3650 | 0.0% (reference) | 0.1382 | 0.0% (reference) | 60.8 |
| 80 | SPIN | 0.3675 | -0.7% (bad) | 0.1419 | -2.7% (bad) | 58.4 |
| 128 | Baseline | 0.5125 | 0.0% (reference) | 0.1794 | 0.0% (reference) | 84.2 |
| 128 | SPIN | 0.4750 | 7.3% (good) | 0.1786 | 0.5% (good) | 78.2 |

Suggested sentence:

> SPIN did not consistently reduce hallucination under our fixed-budget protocol: it increased CHAIRs/CHAIRi at 64 and 80 tokens, while at 128 tokens it reduced CHAIRs by 7.3% but left CHAIRi nearly unchanged (0.5% reduction). This suggests that SPIN is weaker than our Stage 4 intervention on this held-out evaluation.

## SPIN With Bootstrap CIs

Source: `results/bootstrap_chair_significance.json`. Scorer: spaCy notebook-matching CHAIR scorer. Bootstrap resamples: 5000.

| Max new tokens | Method | CHAIRs 95% CI | CHAIRi 95% CI | Avg length |
|---:|---|---:|---:|---:|
| 64 | Baseline | 0.2800 [0.2350, 0.3250] | 0.1066 [0.0872, 0.1274] | 49.5 |
| 64 | SPIN | 0.3025 [0.2575, 0.3475] | 0.1216 [0.1000, 0.1445] | 48.8 |
| 80 | Baseline | 0.3650 [0.3175, 0.4125] | 0.1382 [0.1167, 0.1609] | 60.8 |
| 80 | SPIN | 0.3675 [0.3200, 0.4150] | 0.1419 [0.1194, 0.1657] | 58.4 |
| 128 | Baseline | 0.5125 [0.4625, 0.5600] | 0.1794 [0.1563, 0.2045] | 84.2 |
| 128 | SPIN | 0.4750 [0.4250, 0.5225] | 0.1786 [0.1551, 0.2033] | 78.2 |

### SPIN Paired Deltas vs Matched Baseline

Negative deltas are good because lower CHAIR is better. P-values are paired sign-flip permutation tests with 10000 resamples.

| Max new tokens | Delta CHAIRs | Delta CHAIRi | Interpretation |
|---:|---:|---:|---|
| 64 | +0.0225 [-0.0150, +0.0600], p=0.2996 | +0.0150 [-0.0011, +0.0326], p=0.0812 | SPIN is numerically worse, not significant |
| 80 | +0.0025 [-0.0400, +0.0450], p=1.0000 | +0.0037 [-0.0128, +0.0195], p=0.6737 | SPIN is essentially tied with baseline |
| 128 | -0.0375 [-0.0875, +0.0125], p=0.1811 | -0.0008 [-0.0192, +0.0181], p=0.9380 | SPIN is numerically better on CHAIRs only, not significant |

## Notes For Paper Text

- Lower CHAIRs and CHAIRi are better.
- Longer token budgets increase CHAIRs because captions mention more objects and therefore have more chances to hallucinate.
- For SPIN, the strongest observed improvement is at 128 tokens: CHAIRs drops from 0.5125 to 0.4750, a 7.3% relative reduction.
- At 64 and 80 tokens, SPIN is slightly worse than baseline on both CHAIRs and CHAIRi.
- The main Stage 4 result remains stronger than SPIN on the same 400-image held-out split.

## Qualitative Example: Image 452793

Existing figure asset:

```text
poster_figures/diagram4_qualitative_452793.png
```

Ground-truth COCO objects:

```text
refrigerator, sink
```

This is a useful qualitative example because Baseline, Grounding-only, and SPIN all hallucinate extra kitchen objects. Stage 4 keeps the main ground-truth objects, though its caption is less fluent.

| Method | Caption | Objects to highlight |
|---|---|---|
| Baseline | The image showcases a large, clean kitchen with wooden cabinets and granite countertops. A refrigerator is situated on the right side of the room, while an oven can be found near the center-left area. There are two sinks located close to each other within the space. | Correct: `refrigerator`, `sink`; hallucinated: `oven` |
| Stage 2: LoRA | A kitchen with a refrigerator and sink. A brown counter top, cabinets and a window above the sink. A green bottle on the countertop. | Correct: `refrigerator`, `sink`; hallucinated: `bottle` |
| Stage 3: Grounding | The image showcases a large, clean kitchen with wooden cabinets and granite countertops. A refrigerator is situated on the right side of the room while an oven can be found in front of it. There are two sinks located near each other within this spacious area. | Correct: `refrigerator`, `sink`; hallucinated: `oven` |
| Stage 4: LoRA + Grounding | A kitchen with a refrigerator and sink. A brown counter top in front of the fridge, cabinets above it, a window behind the stove topside down on its side. | Correct: `refrigerator`, `sink` |
| SPIN, 64-token budget | The image showcases a large, well-lit kitchen with a variety of appliances and furniture. The kitchen features a sink, a refrigerator, and a microwave, all placed in a functional and organized manner. | Correct: `refrigerator`, `sink`; hallucinated: `microwave` |
| SPIN, 128-token budget | The image showcases a large, well-lit kitchen with a variety of appliances and furniture. The kitchen features a sink, a refrigerator, and a microwave. In addition to the main appliances, the kitchen also contains a dining table and several chairs. | Correct: `refrigerator`, `sink`; hallucinated: `microwave`, `dining table`, `chairs` |

Suggested figure caption:

> Qualitative example on a held-out COCO val2014 kitchen image. The baseline and grounding-only captions hallucinate an oven, while SPIN introduces a microwave and, at longer decoding budgets, additional furniture. The combined LoRA + grounding method retains the annotated refrigerator and sink while suppressing the main object hallucinations, though with reduced fluency.
