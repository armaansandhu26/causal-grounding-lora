# Hallucination Head Analysis: Implementation Checklist

Status key:

- `[ ]` not started
- `[-]` in progress
- `[x]` done

Tracking note:

- For this board, `[x]` means the step has been implemented in code or notebook cells.
- Runtime verification on Colab is tracked separately when we actually execute the notebook.

## 1. Define the experimental scope

- [x] Pick one base model for Week 1: `llava-hf/llava-1.5-7b-hf`
- [x] Fix decoding setup: greedy decoding, max token length, prompt template
- [x] Decide evaluation subset size: `10-15` COCO validation images

## 2. Set up the Colab runtime

- [x] Install `transformers`, `accelerate`, `datasets`, `pandas`, `seaborn`, `scikit-learn`
- [x] Enable BF16 / FP16 on A100
- [x] Create output folders for traces, labels, plots, and ablation results

## 3. Load data

- [x] Download COCO `val2017` images and `instances_val2017.json`
- [x] Build `image_id -> ground truth objects` mapping
- [x] Sample a small reproducible subset of images

## 4. Load and verify the VLM

- [x] Load processor + model on GPU
- [x] Run one sanity-check caption generation
- [x] Confirm we can request attention outputs during generation

## 5. Implement step-level tracing

- [x] Generate captions token by token
- [x] Log `step_idx`, generated token, prefix text, token probability
- [x] Save per-step attention tensors or reduced per-head features

## 6. Implement head-level feature extraction

- [x] For every layer/head/token step, compute `visual_mass`
- [x] For every layer/head/token step, compute `text_mass`
- [x] For every layer/head/token step, compute `visual_to_text_ratio`
- [x] For every layer/head/token step, compute `attention_entropy`
- [x] Store all features in a table

## 7. Identify image-token positions

- [x] Find where visual tokens sit in the merged sequence
- [x] Build masks for visual vs text attention mass
- [ ] Sanity-check masks with a few printed examples

## 8. Build token/object labeling

- [x] Extract object mentions from generated captions
- [x] Match mentions against COCO object vocabulary
- [x] Create weak labels for `grounded` vs `hallucinated`
- [x] Flag uncertain cases for optional manual review

## 9. Add manual-label workflow

- [x] Export a small labeling sheet for `10-15` images
- [x] Add a simple correction path for weak labels
- [x] Re-import corrected labels for analysis

## 10. Rank suspicious heads

- [x] Compare grounded vs hallucinated token behavior per head
- [x] Compute per-head separation metrics
- [x] Compute AUROC or mean-difference score
- [x] Produce a ranked head table

## 11. Visualize the evidence

- [x] Create heatmap: layer x head separation score
- [x] Create histograms for top heads: grounded vs hallucinated ratios
- [ ] Add optional entropy vs ratio scatterplots

## 12. Implement causal validation

- [ ] Add one-head-at-a-time ablation
- [ ] Add top-k head ablation
- [ ] Add random-head ablation baseline
- [ ] Re-run generation on the same image subset

## 13. Compare ablation outcomes

- [ ] Measure hallucination count before and after ablation
- [ ] Compare baseline vs top-head ablation vs random-head ablation
- [ ] Save summary tables and plots

## 14. Package everything into a Colab notebook

- [x] Add one-click install cell
- [x] Add one config cell
- [x] Add one run cell for baseline tracing
- [x] Add one labeling/export cell
- [x] Add one ranking/plotting cell
- [ ] Add one ablation/evaluation cell

## 15. Add guardrails and notes

- [ ] Document that attention alone is not causal
- [ ] Document COCO label incompleteness
- [ ] Document multi-token object-name and tokenization issues
- [ ] Keep code modular so a different VLM can be swapped in later

## Deliverables

- [x] `week1_hallucination_heads_colab.ipynb`
- [x] Attention and feature extraction utilities
- [x] Manual label template CSV
- [x] Head ranking CSV
- [x] Heatmap and histogram plots
- [ ] Ablation comparison table
