$modelscope-evaluation

You are running inside local codex-cli.
Use this skill to collect, normalize, organize, and publish benchmark or evaluation results for a ModelScope model repository.

Hard requirements:
1. Do not stop because evaluation files are messy or incomplete.
2. Reuse existing logs, tables, README content, and result artifacts when possible.
3. If metrics are scattered, consolidate them into a clean evaluation summary.
4. Normalize score names, formats, and benchmark metadata.
5. Generate missing evaluation documentation if needed.
6. Prefer reproducible summaries over hand-written one-off edits.
7. If publishing is blocked by credentials, still prepare all files for immediate upload.

Please do the following:
A. Scan the workspace and current repo for evaluation outputs, logs, README sections, and metric files.
B. Extract the benchmark names, task types, score values, and any model/version metadata.
C. Normalize the results into a consistent structure.
D. Generate or update evaluation summary files and README sections.
E. If appropriate, prepare Hub-ready metadata for publishing the evaluation results.
F. Upload or stage the outputs for ModelScope publication.

Output only:
1. Benchmarks detected
2. Metrics normalized
3. Files generated or updated
4. Publication status
5. Any single blocking issue