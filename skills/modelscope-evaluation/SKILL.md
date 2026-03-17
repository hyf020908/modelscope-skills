---
name: modelscope-evaluation
description: Manage benchmark results for ModelScope model repositories, including README extraction, score normalization, and metadata publishing.
---

# ModelScope Evaluation

Use this skill when users need to add, normalize, or publish evaluation results for model repositories on ModelScope.

## Capabilities

- Extract benchmark tables from README markdown.
- Normalize benchmark names and metric units.
- Merge multiple score sources into a single structured record.
- Publish evaluation artifacts to model repositories.

## Included Scripts

- `scripts/evaluation_manager.py`: end-to-end extraction/import/update workflow.
- `scripts/run_eval_job.py`: local inspect-style evaluation launcher.
- `scripts/run_vllm_eval_job.py`: local vLLM/lighteval wrapper.
- `scripts/inspect_eval_uv.py`, `scripts/inspect_vllm_uv.py`, `scripts/lighteval_vllm_uv.py`: evaluation runtime entrypoints.

## Typical Workflow

1. Pull or load model README.
2. Extract candidate evaluation tables.
3. Map metrics to canonical benchmark keys.
4. Validate score ranges and units.
5. Write `eval/leaderboard.json` and update README section.
6. Upload artifacts to ModelScope model repo.

## Commands

```bash
# Extract benchmark tables from markdown and print normalized output
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id your-org/your-model \
  --dry-run

# Import external benchmark rows from a JSON file
uv run scripts/evaluation_manager.py import-json \
  --input ./examples/metric_mapping.json \
  --repo-id your-org/your-model \
  --dry-run

# Run a local inspect-style evaluation
uv run scripts/run_eval_job.py --model Qwen/Qwen2.5-7B-Instruct --task mmlu --limit 100
```

## Authentication

- Export `MODELSCOPE_API_TOKEN` for upload/update operations.
- Use `--dry-run` first when modifying repository content.

## Quality Rules

- Keep benchmark naming stable across runs.
- Preserve original source links when importing third-party scores.
- Prefer machine-readable artifacts under `eval/`.
- Always include timestamp and evaluator metadata.

## Guardrails

- Do not fabricate benchmark values.
- Do not overwrite existing metrics without explicit merge policy.
- Do not mix incompatible metric units (for example `%` and raw fractions) in one field.
