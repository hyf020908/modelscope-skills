# Quest 1: Evaluate a Hub Model

Add structured benchmark results to ModelScope model repositories and help maintain a shared leaderboard dataset.

## Why This Matters

Consistent evaluation metadata makes model selection faster and more reliable. Publishing benchmark evidence in model cards improves transparency and reuse.

## Goals

- Add benchmark results to trending ModelScope models.
- Normalize benchmark naming and score formats.
- Publish machine-readable evaluation outputs for leaderboard apps.

## XP Tiers

| Tier | XP | Description | What Counts |
|------|----|-------------|-------------|
| Contributor | 25 | Add one validated benchmark result to a model card. | A merged PR or accepted direct update. |
| Evaluator | 75 | Import multiple benchmarks with proper source attribution. | Correct metadata and score mapping. |
| Advanced | 150 | Run your own evaluation and publish method + results. | Reproducible run config and uploaded outputs. |
| Bonus | 200 | Improve leaderboard tooling in `apps/evals-leaderboard/`. | Merged tooling or UX improvements. |

## Skill To Use

Use `skills/modelscope-evaluation/`.

Core capabilities:

- Extract evaluation tables from existing README files.
- Normalize benchmark keys and metric formats.
- Import third-party benchmark sources.
- Publish structured JSON output for leaderboard pipelines.

## Workflow

### 1) Extract README Evaluation Tables

```bash
uv run skills/modelscope-evaluation/scripts/evaluation_manager.py extract-readme \
  --repo-id "your-org/your-model" \
  --dry-run
```

### 2) Import External Scores

```bash
uv run skills/modelscope-evaluation/scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" \
  --model-name "claude-sonnet-4" \
  --repo-id "your-org/target-model" \
  --dry-run
```

### 3) Run Your Own Evaluation

```bash
uv run skills/modelscope-evaluation/scripts/inspect_eval_uv.py \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --task "mmlu"
```

For scheduled or remote execution, pair this with `skills/modelscope-jobs/`.

## Quality Checklist

- Use `--dry-run` before pushing updates.
- Verify benchmark names and metric units.
- Include data source links in metadata fields.
- Keep model-card tables and JSON artifacts in sync.

## Resources

- [Skill guide](../../skills/modelscope-evaluation/SKILL.md)
- [Usage examples](../../skills/modelscope-evaluation/examples/USAGE_EXAMPLES.md)
- [Metric mapping](../../skills/modelscope-evaluation/examples/metric_mapping.json)
