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

Suggested sentence:

> On the 400-image held-out split, Stage 4 reduces CHAIRs by 37.8% and CHAIRi by 38.5% relative to the greedy LLaVA baseline, outperforming either LoRA-only or grounding-only intervention.

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

These CIs are from `results/spin_comparison.json`.

| Max new tokens | Method | CHAIRs 95% CI | CHAIRi 95% CI | Avg length |
|---:|---|---:|---:|---:|
| 64 | Baseline | 0.2800 [0.2375, 0.3225] | 0.1066 [0.0863, 0.1266] | 49.5 |
| 64 | SPIN | 0.3025 [0.2600, 0.3475] | 0.1216 [0.0999, 0.1438] | 48.8 |
| 80 | Baseline | 0.3650 [0.3175, 0.4125] | 0.1382 [0.1155, 0.1601] | 60.8 |
| 80 | SPIN | 0.3675 [0.3225, 0.4125] | 0.1419 [0.1207, 0.1651] | 58.4 |
| 128 | Baseline | 0.5125 [0.4650, 0.5600] | 0.1794 [0.1565, 0.2040] | 84.2 |
| 128 | SPIN | 0.4750 [0.4275, 0.5225] | 0.1786 [0.1552, 0.2023] | 78.2 |

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
