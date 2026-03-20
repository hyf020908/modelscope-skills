---
name: modelscope-dataset-explorer
description: Explore ModelScope datasets using Hub metadata APIs, local snapshot downloads, and SQL analysis with DuckDB.
---

# ModelScope Dataset Explorer

Use this skill when the main task is understanding an existing dataset before training, evaluation, cleaning, or publication.

## Operating Mode

- Start with metadata and lightweight inspection before downloading large artifacts.
- Download only the smallest useful subset when a local snapshot is needed.
- Prefer structured findings over generic dataset summaries.
- Keep all exploration outputs inside the current project so downstream steps stay reproducible.

## What This Skill Covers

- Hub metadata discovery.
- Split, schema, modality, and file-format inspection.
- Lightweight sample preview and quality checks.
- Local SQL profiling with DuckDB after selective download.
- Recommendations for dataset selection or cleanup.

## Standard Workflow

1. Inspect dataset metadata from ModelScope Hub.
2. Identify likely data files and split layout.
3. Download only the required subset when local inspection is necessary.
4. Run SQL or file-based profiling on parquet/json/jsonl/csv files.
5. Summarize schema, data quality, and downstream suitability.

## Metadata Discovery

```python
from modelscope.hub.api import HubApi

api = HubApi()
result = api.list_datasets(owner_or_group="AI-ModelScope", page_number=1, page_size=20)
print(result)
```

## Snapshot Download

```bash
modelscope download --dataset your-org/your-dataset --local_dir ./data/your-dataset
modelscope download --dataset your-org/your-dataset --include "*.parquet" --local_dir ./data/your-dataset
```

Python alternative:

```python
from modelscope.hub.snapshot_download import dataset_snapshot_download

local_dir = dataset_snapshot_download("your-org/your-dataset", local_dir="./data/your-dataset")
print(local_dir)
```

## Query With DuckDB

```bash
duckdb -c "SELECT count(*) FROM read_parquet('./data/your-dataset/**/*.parquet');"
```

Typical profiling query:

```sql
SELECT
  count(*) AS rows,
  approx_count_distinct(label) AS distinct_labels,
  avg(length(text)) AS avg_text_len
FROM read_parquet('./data/your-dataset/**/*.parquet');
```

## AI Execution Contract

When using this skill, the agent should:

1. Infer the most likely relevant dataset if the user does not provide one.
2. Confirm schema, split names, file formats, and representative samples.
3. Highlight concrete risks such as missing fields, split imbalance, duplicated rows, or license ambiguity.
4. Recommend the best immediate dataset choice for the current project.
5. Save a concise inspection report if the task is part of a larger workflow.

## Output Expectations

Provide:

- Dataset identifiers inspected.
- Schema summary with inferred column roles.
- Split statistics and file-format layout.
- At least 3 representative samples when data access is available.
- Concrete transformation or filtering recommendations.

## Guardrails

- Do not assume a public remote SQL endpoint exists.
- Do not expose private or sensitive rows in logs or markdown.
- Keep downloaded data inside project-scoped directories.
- Avoid downloading full snapshots when metadata or a filtered subset is enough.
