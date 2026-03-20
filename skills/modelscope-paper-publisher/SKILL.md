---
name: modelscope-paper-publisher
description: Draft and publish model-related research summaries to ModelScope repositories.
---

# ModelScope Paper Publisher

Use this skill when users need a structured research-style write-up to accompany a model, dataset, benchmark, or release note on ModelScope.

## Operating Mode

- Treat local experiment artifacts and README files as the evidence base.
- Use templates to impose consistent structure and metadata.
- Draft locally first, then upload only after claims and links are checked.
- Keep unsupported claims out of the document even if the template has space for them.

## What It Does

- Generate paper-style markdown from templates.
- Standardize metadata such as title, authors, abstract, date, and links.
- Save local drafts and optionally upload them to ModelScope repos.

## Included Assets

- Templates: `templates/standard.md`, `templates/arxiv.md`, `templates/ml-report.md`, `templates/modern.md`
- Script: `scripts/paper_manager.py`
- Example: `examples/example_usage.md`

## Typical Workflow

1. Collect source materials from the current workspace.
2. Choose the closest template.
3. Fill metadata fields and render a first draft.
4. Verify claims, links, and benchmark references.
5. Upload the final markdown into a model repo path such as `reports/papers/<slug>.md`.

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

## AI Execution Contract

When using this skill, the agent should:

1. Ground every major claim in local files, metrics, or explicitly provided citations.
2. Infer the key contribution, setup, and limitations from available evidence.
3. Choose the closest template instead of inventing an ad hoc structure.
4. Produce publication-ready markdown even when upload is blocked.

## Guardrails

- Keep claims evidence-backed and reproducible.
- Preserve citation links exactly as provided.
- Avoid unsupported benchmark conclusions or fabricated ablation results.
