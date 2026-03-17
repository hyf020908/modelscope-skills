# Quest 3: Supervised Fine-Tuning on ModelScope

Fine-tune language models with reproducible training configuration and publish checkpoints on ModelScope Hub.

## Why This Matters

Fine-tuned checkpoints plus transparent training metadata help teams quickly adopt and improve strong open models.

## Skill To Use

Use `skills/modelscope-model-trainer/`.

Core capabilities:

- Supervised Fine-Tuning (SFT)
- Direct Preference Optimization (DPO)
- Group Relative Policy Optimization (GRPO)
- Cost estimation and dataset inspection
- Optional GGUF conversion for local inference

## Suggested Workflow

### 1) Inspect dataset quality

```bash
uv run skills/modelscope-model-trainer/scripts/dataset_inspector.py \
  --data-file ./data/train.jsonl
```

### 2) Run SFT training

```bash
uv run skills/modelscope-model-trainer/scripts/train_sft_example.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --dataset ./data/train.jsonl \
  --output-dir ./outputs/qwen-sft
```

### 3) (Optional) Convert checkpoint to GGUF

```bash
uv run skills/modelscope-model-trainer/scripts/convert_to_gguf.py \
  --checkpoint ./outputs/qwen-sft \
  --output ./outputs/qwen-sft.gguf
```

### 4) Publish artifacts to Hub

```bash
modelscope create your-name/qwen-sft --repo_type model --visibility public
modelscope upload your-name/qwen-sft ./outputs/qwen-sft checkpoints --repo-type model
```

## XP Tiers

- Starter: Train and publish one SFT checkpoint with README metadata.
- Standard: Compare two training settings and publish benchmark deltas.
- Advanced: Add DPO or GRPO run with reproducible scripts and reports.

## Resources

- [Skill guide](../../skills/modelscope-model-trainer/SKILL.md)
- [SFT script](../../skills/modelscope-model-trainer/scripts/train_sft_example.py)
- [DPO script](../../skills/modelscope-model-trainer/scripts/train_dpo_example.py)
- [GRPO script](../../skills/modelscope-model-trainer/scripts/train_grpo_example.py)
- [Training methods](../../skills/modelscope-model-trainer/references/training_methods.md)
- [Hardware guide](../../skills/modelscope-model-trainer/references/hardware_guide.md)
