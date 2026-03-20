---
name: modelscope-evaluation
description: Manage benchmark results for ModelScope model repositories, including README extraction, score normalization, and metadata publishing.
---

# ModelScope Evaluation

Use this skill when the task is to collect, normalize, run, or publish model evaluation results for ModelScope repositories.

## Operating Mode

- Metadata extraction and normalization can run locally.
- Heavy or long-running evaluation should run remotely on PAI DLC, with the local machine acting as control plane only.
- Reuse existing logs, result tables, and README sections before generating anything new.
- Keep evaluation outputs machine-readable so they can be merged, published, or rechecked later.

## Credential Gate

Before the first real PAI DLC submission, generate `configs/pai.required.env` if any required PAI field is missing or unconfirmed. The file should contain:

```bash
ALIBABA_CLOUD_ACCESS_KEY_ID=
ALIBABA_CLOUD_ACCESS_KEY_SECRET=
PAI_REGION=
PAI_WORKSPACE_ID=
```

After writing the file:

1. Tell the user to fill the four fields.
2. Tell the user to reply with exactly `continue`.
3. Resume remote evaluation only after the user continues.

`MODELSCOPE_API_TOKEN` can be gathered separately when remote assets or publication need it.

## Capabilities

- Extract benchmark tables from README markdown.
- Normalize benchmark names, aliases, and metric units.
- Merge multiple score sources into one structured artifact.
- Run lightweight evaluation wrappers or submit them to PAI DLC.
- Publish evaluation artifacts back to ModelScope model repositories.

## Included Scripts

- `scripts/evaluation_manager.py`
  Supports `extract-readme`, `import-json`, `to-yaml`.
- `scripts/run_eval_job.py`
  Inspect-style evaluation wrapper.
- `scripts/run_vllm_eval_job.py`
  vLLM or lighteval wrapper.
- `scripts/inspect_eval_uv.py`
- `scripts/inspect_vllm_uv.py`
- `scripts/lighteval_vllm_uv.py`
- `scripts/submit_pai_dlc.py`
  Generic PAI DLC submission and polling helper.

## Standard Workflow

1. Discover existing README tables, JSON, YAML, or log outputs.
2. Normalize benchmark names and score units.
3. Decide whether the task is metadata-only or needs actual remote evaluation.
4. If remote execution is needed, upload required local scripts or config files as remote assets and submit to PAI DLC.
5. Write clean machine-readable outputs under `eval/` or a similar folder.
6. Publish or stage results for ModelScope Hub.

## Local Commands

```bash
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id your-org/your-model \
  --dry-run

uv run scripts/evaluation_manager.py import-json \
  --input ./examples/metric_mapping.json \
  --repo-id your-org/your-model \
  --dry-run

uv run scripts/run_eval_job.py --model Qwen/Qwen2.5-7B-Instruct --task mmlu --limit 100
```

## Remote Execution Pattern

For remote evaluation, generate a config set with at least:

- `USER_COMMAND`
- `REMOTE_BOOTSTRAP_COMMAND`
- `REMOTE_ASSET_PATHS` when local scripts or local config files are needed remotely
- `MODELSCOPE_API_TOKEN` when assets or outputs must be published through ModelScope
- `PAI_REGION`, `PAI_WORKSPACE_ID`, and DLC resource settings

Then submit with:

```bash
uv run scripts/submit_pai_dlc.py --env-file configs/remote.auto.env --mode pilot --wait
```

## AI Execution Contract

When using this skill, the agent should:

1. Distinguish between extracting existing metrics and running new evaluations.
2. Generate `configs/pai.required.env` and wait for `continue` before any real remote submission when the four required PAI fields are not yet available.
3. Normalize names and units before writing summary files.
4. Keep provenance: source file, evaluator, timestamp, model identifier.
5. Use remote execution for heavy runs or anything likely to exceed local limits.
6. Publish only supported metrics and never fabricate missing values.

## Output Expectations

Provide:

- Benchmarks detected or executed.
- Metrics normalized and how they were mapped.
- Files created, updated, or staged.
- Publication status.
- One blocking issue if the workflow cannot complete.

## Guardrails

- Do not fabricate benchmark values.
- Do not merge incompatible units into the same field.
- Do not overwrite existing scores without an explicit merge policy.
- Prefer `--dry-run` first when mutating repository content.
