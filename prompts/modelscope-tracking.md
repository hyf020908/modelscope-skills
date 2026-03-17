$modelscope-tracking

You are running inside local codex-cli.
Use this skill to create or improve local experiment tracking with run manifests, metric logs, artifact catalogs, and summary exports for a ModelScope workflow.

Hard requirements:
1. Do not stop because current experiment records are messy or missing.
2. If no tracking structure exists, create one from scratch.
3. Reuse existing logs, checkpoints, result files, and config files.
4. Normalize run names, timestamps, metrics, and artifact references.
5. Keep tracking lightweight and file-based unless the workspace already uses something else.
6. Produce summaries that are easy to publish or compare later.

Please do the following:
A. Scan the workspace for experiment outputs, configs, checkpoints, and metrics.
B. Build or update a local tracking structure.
C. Create run manifests and artifact catalogs.
D. Normalize metric logs and generate a concise summary export.
E. Leave the project ready for future runs to append new results cleanly.

Output only:
1. Tracking structure created
2. Runs discovered
3. Metrics normalized
4. Summary files exported
5. Any single blocking issue