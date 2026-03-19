---
name: modelscope-model-trainer
description: One-shot remote-first ms-swift trainer for Alibaba Cloud PAI DLC + ModelScope Hub, with automatic fallback and failure recovery.
---

# ModelScope Model Trainer

Use this skill when users need practical language-model training on ModelScope with minimal retries.

## Operating Mode (Default)

- Remote-first: treat local machine as control plane only.
- Never run heavy ms-swift training on local macOS.
- Local actions are limited to scanning files, generating assets/config, submitting jobs, polling, and collecting outputs.
- Preferred runtime is PAI DLC. Reuse DSW only when it is already provisioned and clearly more suitable.
- If assets are missing, generate minimum viable assets and continue.

## Stack

- `ms-swift` for training and evaluation orchestration.
- `modelscope` SDK/CLI for repository and artifact operations.
- `alibabacloud-pai-dlc20201203` SDK for remote DLC submission and polling.
- Optional `llama.cpp` conversion step for GGUF export.

## Included Scripts

- `scripts/train_sft_example.py`
- `scripts/bootstrap_remote_assets.py`
- `scripts/diagnose_dlc_report.py`
- `scripts/train_dpo_example.py`
- `scripts/train_grpo_example.py`
- `scripts/unsloth_sft_example.py`
- `scripts/convert_to_gguf.py`
- `scripts/dataset_inspector.py`
- `scripts/estimate_cost.py`

## One-Shot Workflow

1. Detect credentials/tools/region/workspace (`AK/SK`, `PAI_REGION`, `MODELSCOPE_API_TOKEN`).
2. Scan workspace for existing datasets/config/scripts; reuse them.
3. If no data, create minimal instruction dataset (`train/valid`).
4. Select method:
   - Default `SFT`.
   - Use `DPO` only when preference-pair schema is present (`chosen/rejected` or equivalent).
5. Build lightweight pilot config first (`LoRA` / `QLoRA`).
6. Submit pilot job remotely to PAI DLC.
7. Auto-fix one common failure and resubmit automatically.
8. Submit/upgrade to full run.
9. Track status, extract best checkpoint, publish to ModelScope Hub when token is available.

## Default Resource Policy (Low-Cost First)

- Start with CPU route when budget/quotas are uncertain:
  - `PAI_DLC_GPU=0`
  - `PAI_DLC_CPU=4`
  - `PAI_DLC_MEMORY=16Gi`
- If GPU is used, avoid `bf16` unless the instance definitely supports it.
- For CPU or unknown GPU capability, force:
  - `--bf16 false --fp16 false --torch_dtype float32`

## Command Construction Rules

- Keep remote `user_command` short and deterministic.
- Do not embed large base64 payloads into a single command string.
- Prefer small inline datasets/configs for pilot, or mount assets/object storage.
- Ensure command includes actual training execution (`swift sft/...`), not only dependency installation.

## Quick Bootstrap

```bash
# 1) Prepare minimal remote-ready assets in current workspace
uv run modelscope-model-trainer/scripts/bootstrap_remote_assets.py --root .

# 2) Submit pilot (control plane local, training remote)
.venv/bin/python scripts/submit_pai_dlc.py \
  --env-file configs/remote.auto.env \
  --mode pilot \
  --wait \
  --retry-once

# 3) Submit full run
.venv/bin/python scripts/submit_pai_dlc.py \
  --env-file configs/remote.auto.env \
  --mode full \
  --wait
```

## Failure Auto-Recovery Matrix

- `resourceLimit` / GPU quota exceeded:
  - Switch to CPU: `GPU=0, CPU=4, MEMORY=16Gi`.
- `bf16` unsupported:
  - Add/force `--bf16 false --fp16 false --torch_dtype float32`.
- `enterRunningTimeout` / image pull failures:
  - Use verified image (`pytorch/pytorch:latest` or region-validated mirror).
- Pod exits after pip install with no training logs:
  - Shorten command; ensure explicit `swift sft` execution step.
- transient polling/proxy errors:
  - Continue polling; do not treat as terminal unless remote status is failed/stopped.

## Standard Output Contract

Always return only these 9 items when asked for run result:

1. Training route used
2. Files generated
3. Remote environment used
4. Job ID / workspace / region
5. Pilot result
6. Full training result
7. Best checkpoint path
8. Hub publication result
9. Single blocking issue if interrupted

## Publishing

```bash
modelscope create your-name/qwen2p5-sft --repo_type model --visibility public
modelscope upload your-name/qwen2p5-sft ./outputs/sft checkpoints --repo-type model
```

If token is missing, mark publication as skipped instead of failing training result.

## Quality Rules

- Always run a small pilot before full training.
- Save config + seed + git SHA for reproducibility.
- Keep train/validation leakage checks explicit.
- Record metric trends per checkpoint.

## Guardrails

- Do not claim unsupported hardware assumptions.
- Do not skip dataset validation.
- Do not overwrite production model repos without explicit user approval.
