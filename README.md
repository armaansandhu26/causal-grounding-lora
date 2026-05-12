# Hallucination mitigation for LLaVA-1.5-7B

This repository is the **final** course implementation: we locate attention heads correlated with object hallucinations, fine-tune those heads with **targeted LoRA**, add an **inference-time grounding penalty** on weakly grounded tokens, and evaluate **baseline vs LoRA-only vs controller-only vs combined** on CHAIR (and POPE where noted).

---

## Pipeline at a glance

| Stage | What it does | Main artifact |
|-------|----------------|---------------|
| **1** | Screen COCO val images, trace generation, rank heads, **causal validation** → shortlist of hallucination-linked heads | `stage1_hallucination_heads.ipynb` → `results/final_hallucination_heads.json` |
| **2** | QLoRA on Q/K/V in layers that contain the shortlist (32 heads) using contrastive caption pairs | `stage2_lora.ipynb` → `results/stage2_lora_adapter/` |
| **3** | At decode time, compute a **visual grounding score** from attention in those heads; penalize risky content-word logits | `stage3_inference_grounding.ipynb` |
| **4** | **Four-way eval**: baseline / LoRA / controller / LoRA+controller; optional θ and head-count ablations | `stage4_comparison.ipynb` (40 images, CHAIR + POPE), `stage4_final_1.ipynb` (400 images, CHAIR + ablations) |

Optional exploratory notebook: `validation_Experiments.ipynb`.

---

## How to run

Notebooks assume a **GPU runtime** (e.g. Colab A100) and paths under a working directory such as Google Drive (`WORK_DIR` in each notebook). Typical order:

1. Run **Stage 1** once (or skip if you only change LoRA/controller hyperparameters and keep `final_hallucination_heads.json`).
2. Run **Stage 2** to train or refresh the LoRA adapter.
3. Run **Stage 3** to develop or inspect the grounding controller.
4. Run **Stage 4** notebooks for published metrics; they load the base model, optional LoRA, and the controller flags as configured in the notebook.

There is no root `requirements.txt`; dependencies match a standard LLaVA + `transformers` + `peft` + `bitsandbytes` stack used in the notebooks.

---

## Results (from checked-in JSON)

### CHAIR — 40-image suite (`results/stage4_all_results.json`, θ = 0.08, α = 8)

| Condition | CHAIRs | CHAIRi |
|-----------|--------|--------|
| Baseline | 0.30 | 0.109 |
| Stage 2 (LoRA only) | 0.05 | 0.025 |
| Stage 3 (controller only) | 0.325 | 0.107 |
| **Stage 4 (LoRA + controller)** | **0.025** | **0.0125** |

### CHAIR — 400-image suite (`results/stage4_400img_results.json`, same θ, α)

| Condition | CHAIRs | CHAIRi |
|-----------|--------|--------|
| Baseline | 0.363 | 0.137 |
| Stage 2 (LoRA only) | 0.073 | 0.039 |
| Stage 3 (controller only) | 0.350 | 0.134 |
| **Stage 4 (LoRA + controller)** | **0.070** | **0.039** |

On the 40-image run, **LoRA alone** already improves CHAIR strongly; **adding the controller** lowers CHAIR further (Stage 4 best). Controller-only (Stage 3) is **not** meant as a standalone win on CHAIR in this setup—it is the piece that combines with LoRA in Stage 4.

### POPE (40-image run in `stage4_all_results.json`)

POPE is mostly driven by the **yes/no** answer behavior of the LoRA checkpoint in this pipeline. The Stage 4 notebook notes that the grounding penalty targets **object-like content words**, not short “yes”/“no” tokens, so interpret Stage 2 vs Stage 4 POPE together with that caveat.

---

## Key files

| Path | Role |
|------|------|
| `results/final_hallucination_heads.json` | 32-head shortlist from Stage 1 |
| `results/stage2_lora_adapter/` | Saved PEFT adapter after Stage 2 |
| `results/stage2_baseline_eval.json`, `results/stage2_lora_eval.json` | Early baseline vs LoRA snapshot evals |
| `results/stage2_training_log.json` | Training run metadata |
| `results/stage4_all_results.json` | Full 40-image comparison + ablation slices |
| `results/stage4_400img_results.json` | 400-image CHAIR, θ/head ablations, sample captions |
| `682_project_proposal.pdf` | Original project proposal |

---

## Limitations (brief)

- CHAIR uses COCO objects as reference; **missing labels** and **multi-token object names** affect weak labels and scores.
- Attention-based scores are **heuristic**; causal ablation in Stage 1 motivates which heads to edit, but the controller is still a engineered signal, not a full causal proof at inference.

For adapter-specific metadata, see `results/stage2_lora_adapter/README.md`.
