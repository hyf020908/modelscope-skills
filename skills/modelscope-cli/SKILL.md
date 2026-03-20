---
name: modelscope-cli
description: Use the official `modelscope` CLI for ModelScope Hub authentication, repository creation, download, and upload workflows.
---

# ModelScope CLI

Use this skill when a task is fundamentally a ModelScope Hub repository operation and the CLI is the most direct, deterministic interface.

## Operating Mode

- Prefer official `modelscope` CLI commands over ad hoc HTTP calls.
- Treat the current workspace as the source of truth for files to upload.
- Reuse existing local files and repository names when they are already valid.
- If authentication is missing, detect it early and still prepare the remaining commands.

## When To Use

- Login or token-based authentication.
- Create model or dataset repositories.
- Download full or partial snapshots for models and datasets.
- Upload generated artifacts, reports, checkpoints, or dataset files.
- Mirror a local folder structure into a Hub repository with explicit target paths.

## When Not To Use

- Complex metadata transformation logic that deserves a reusable script.
- Bulk data validation or SQL analysis.
- Remote compute jobs that should run on PAI rather than locally.

## Core Commands

### Authentication

```bash
modelscope login --token "$MODELSCOPE_API_TOKEN"
```

Use direct `--token` only for one-off automation where shell environment injection is not available.

### Create Repository

```bash
modelscope create your-name/your-model --repo_type model --visibility public
modelscope create your-name/your-dataset --repo_type dataset --visibility private
```

### Download

```bash
modelscope download --model Qwen/Qwen2.5-7B-Instruct --local_dir ./artifacts
modelscope download --model Qwen/Qwen2.5-7B-Instruct tokenizer.json config.json --local_dir ./artifacts
modelscope download --dataset your-name/your-dataset --local_dir ./dataset
```

### Upload

```bash
modelscope upload your-name/your-model ./README.md README.md --repo-type model
modelscope upload your-name/your-dataset ./data data --repo-type dataset
```

## AI Execution Contract

When using this skill, the agent should:

1. Detect whether the task needs a model repo, a dataset repo, or both.
2. Check whether `modelscope` is installed and whether `MODELSCOPE_API_TOKEN` is present.
3. Create missing local metadata files only when they are genuinely required for a valid upload.
4. Use explicit destination paths in the repository instead of relying on ambiguous defaults.
5. Leave the workspace in a publishable state even if actual upload is blocked by credentials.

## Python SDK Equivalents

Use SDK calls only when CLI behavior is insufficient:

```python
from modelscope.hub.api import HubApi
from modelscope.hub.snapshot_download import snapshot_download, dataset_snapshot_download

api = HubApi()
api.login("<token>")
api.create_repo("your-name/your-model", repo_type="model", exist_ok=True)

snapshot_download(repo_id="Qwen/Qwen2.5-7B-Instruct", local_dir="./artifacts")
dataset_snapshot_download("your-name/your-dataset", local_dir="./dataset")
```

## Output Expectations

Return:

- Authentication status.
- Repository identifiers created or reused.
- Local files generated or normalized.
- Files uploaded, skipped, or staged.
- The single blocking issue when the workflow cannot finish.

## Guardrails

- Never hardcode tokens in source files, markdown, or shell history examples.
- Prefer `--local_dir` for deterministic downloads.
- Confirm repo type before upload or download.
- Use clear commit messages for scripted uploads.
- Do not overwrite unrelated repository paths just because a local folder exists.

## Troubleshooting

- Unauthorized errors usually mean the token is missing, expired, or does not match the owner namespace.
- Empty downloads usually mean the repo type or revision is wrong.
- Partial uploads usually come from incorrect source paths or incorrect target paths in the repo.
