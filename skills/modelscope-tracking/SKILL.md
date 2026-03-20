---
name: modelscope-tracking
description: Track experiments with local run manifests, metric logs, artifact catalogs, and summary exports for ModelScope workflows.
---

# ModelScope Tracking

Use this skill when users need structured experiment or evaluation tracking that stays local, reproducible, scriptable, and easy to publish.

## Operating Mode

- Keep tracking file-based unless the project already uses another tracker.
- Record lifecycle, metrics, and artifacts separately.
- Make summaries easy to compare across runs and easy to upload later.
- Prefer append-only logs plus stable manifests over opaque binary state.

## Scope

This skill provides project-local tracking for:

- Run lifecycle metadata (`create-run`, `complete-run`)
- Metric logging (`metrics.jsonl`)
- Artifact registration (`artifacts.jsonl`)
- Run indexing and summaries (table, JSON, Markdown, CSV)

It is designed for ModelScope workflows where training, evaluation, or batch jobs produce outputs that may later be published to Hub repos.

## Primary CLI

- `scripts/run_tracker.py`

## Standard Workflow

```bash
# 1) Initialize workspace
uv run scripts/run_tracker.py init --project qwen-sft --owner ml-team

# 2) Create run
RUN_ID=$(uv run scripts/run_tracker.py create-run \
  --model-id Qwen/Qwen2.5-7B-Instruct \
  --dataset-id your-org/sft-data \
  --task sft \
  --tags "baseline,fp16")

# 3) Log metrics during execution
uv run scripts/run_tracker.py log-metric --run-id "$RUN_ID" --name train_loss --value 1.23 --step 1
uv run scripts/run_tracker.py log-metric --run-id "$RUN_ID" --name eval_accuracy --value 0.71 --step 100 --split validation

# 4) Register produced artifacts
uv run scripts/run_tracker.py add-artifact --run-id "$RUN_ID" --path ./outputs/checkpoint-100 --kind checkpoint

# 5) Complete run and save summary
uv run scripts/run_tracker.py complete-run \
  --run-id "$RUN_ID" \
  --status succeeded \
  --summary-json '{"best_eval_accuracy":0.71,"notes":"baseline config"}'

# 6) Export reports
uv run scripts/run_tracker.py summarize --format markdown --output .modelscope-tracking/reports/summary.md
uv run scripts/run_tracker.py export-metrics-csv --run-id "$RUN_ID" --output .modelscope-tracking/reports/${RUN_ID}.csv
```

## ModelScope Integration Pattern

After generating tracking reports, publish them to ModelScope using standard Hub workflows:

```bash
modelscope upload your-org/your-model .modelscope-tracking/reports reports --repo-type model
```

## Directory Layout

```text
.modelscope-tracking/
  project.json
  runs/
    <run-id>/
      run.json
      metrics.jsonl
      artifacts.jsonl
  artifacts/
  reports/
```

## References

- `references/logging_metrics.md`
- `references/alerts.md`
- `references/retrieving_metrics.md`

## Guardrails

- Use stable metric names across runs (`train_loss`, `eval_accuracy`, `latency_ms`).
- Keep `summary-json` concise and machine-readable.
- Register artifact paths explicitly so downstream automation can discover outputs.
- Do not store secrets in run manifests.
