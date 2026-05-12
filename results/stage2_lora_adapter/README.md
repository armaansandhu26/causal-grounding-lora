---
base_model: llava-hf/llava-1.5-7b-hf
library_name: peft
tags:
- base_model:adapter:llava-hf/llava-1.5-7b-hf
- lora
- transformers
---

# LLaVA-1.5-7B — hallucination-targeted LoRA adapter

PEFT adapter produced by **Stage 2** in this project (`stage2_lora.ipynb`).

## What it is

- **Base model:** `llava-hf/llava-1.5-7b-hf`
- **Method:** QLoRA-style training with LoRA applied to **attention Q/K/V** in the transformer layers that contain the **32 hallucination-linked heads** identified in Stage 1 (`results/final_hallucination_heads.json`).
- **Objective:** contrastive caption pairs to reduce **object hallucinations** (evaluated with CHAIR in Stage 2 and Stage 4 notebooks).

## How to use

Load with Hugging Face `transformers` + `peft` the same way as any LLaVA PEFT adapter: load the base LLaVA weights, then `PeftModel.from_pretrained(..., this adapter directory)`.

## Evaluation

See the main [README.md](../../README.md) and `results/stage4_all_results.json` / `results/stage4_400img_results.json` for CHAIR numbers with and without the Stage 3–4 inference controller.

## Training stack

Adapter saved with **PEFT** (see `adapter_config.json` in this folder for exact adapter hyperparameters).
