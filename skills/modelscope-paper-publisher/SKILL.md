---
name: modelscope-paper-publisher
description: Draft and publish model-related research summaries to ModelScope repositories.
---

# ModelScope Paper Publisher

Use this skill when users want structured research write-ups alongside model or dataset releases.

## What It Does

- Generate paper-style markdown from templates.
- Standardize metadata (title, authors, links, abstract).
- Save local drafts and optionally upload to ModelScope Hub repos.

## Included Assets

- Templates: `templates/standard.md`, `templates/arxiv.md`, `templates/ml-report.md`, `templates/modern.md`
- Script: `scripts/paper_manager.py`
- Example: `examples/example_usage.md`

## Typical Workflow

1. Select a template.
2. Fill metadata fields.
3. Render markdown draft.
4. Review and edit claims/citations.
5. Upload final markdown to repo path like `reports/papers/<slug>.md`.

## Command Example

```bash
uv run scripts/paper_manager.py create \
  --title "Efficient Long-Context Fine-Tuning" \
  --authors "A. Researcher,B. Engineer" \
  --template modern \
  --output ./papers/efficient-long-context.md
```

Optional upload:

```bash
uv run scripts/paper_manager.py upload \
  --repo-id your-org/your-model \
  --input ./papers/efficient-long-context.md \
  --path-in-repo reports/papers/efficient-long-context.md
```

## Guardrails

- Keep claims evidence-backed and reproducible.
- Preserve citation links exactly as provided.
- Avoid generating unsupported benchmark conclusions.
