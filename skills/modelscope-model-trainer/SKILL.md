---
name: modelscope-model-trainer
description: Train and align language models with ms-swift and publish checkpoints to ModelScope Hub.
---

# ModelScope Model Trainer

Use this skill when users need practical training workflows for SFT, DPO, and GRPO in the ModelScope ecosystem.

## Stack

- `ms-swift` for training and evaluation orchestration.
- `modelscope` SDK/CLI for repository and artifact operations.
- Optional `llama.cpp` conversion step for GGUF export.

## Included Scripts

- `scripts/train_sft_example.py`
- `scripts/train_dpo_example.py`
- `scripts/train_grpo_example.py`
- `scripts/unsloth_sft_example.py`
- `scripts/convert_to_gguf.py`
- `scripts/dataset_inspector.py`
- `scripts/estimate_cost.py`

## Default Workflow

1. Validate dataset shape and field mapping.
2. Choose training method (SFT, DPO, GRPO).
3. Launch training locally or on cluster runtime.
4. Evaluate checkpoints and keep best revision.
5. Push artifacts to ModelScope Hub.
6. Optionally convert to GGUF for local serving.

## Quick Commands

```bash
# Install training stack
uv pip install ms-swift modelscope

# SFT
swift sft \
  --model Qwen/Qwen2.5-7B-Instruct \
  --dataset AI-ModelScope/alpaca-gpt4-data-en#2000 \
  --output_dir ./outputs/sft

# DPO
swift dpo \
  --model ./outputs/sft \
  --dataset your-org/dpo-preferences \
  --output_dir ./outputs/dpo

# Evaluation
swift eval \
  --model ./outputs/dpo \
  --dataset AI-ModelScope/alpaca-gpt4-data-en#200
```

## Publishing

```bash
modelscope create your-name/qwen2p5-sft --repo_type model --visibility public
modelscope upload your-name/qwen2p5-sft ./outputs/sft checkpoints --repo-type model
```

## Quality Rules

- Always run a small pilot before full training.
- Save config + seed + git SHA for reproducibility.
- Keep train/validation leakage checks explicit.
- Record metric trends per checkpoint.

## Guardrails

- Do not claim unsupported hardware assumptions.
- Do not skip dataset validation.
- Do not overwrite production model repos without explicit user approval.
