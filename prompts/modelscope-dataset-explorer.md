$modelscope-dataset-explorer

You are running inside local codex-cli.
Use this skill to explore ModelScope datasets through metadata inspection, local snapshot analysis, and structured data profiling.

Hard requirements:
1. Do not stop just because the dataset is unfamiliar.
2. If no dataset is explicitly specified, infer a reasonable candidate from the current project.
3. Prefer lightweight exploration before downloading large artifacts.
4. If a local snapshot is useful, download only the minimal subset needed.
5. Use structured inspection where possible, including schema checks, split discovery, and sample previews.
6. Surface actionable findings rather than generic descriptions.
7. Keep everything reproducible inside the current workspace.

Please do the following:
A. Detect whether the current project already references a ModelScope dataset.
B. If not, identify one or more likely public datasets relevant to this project.
C. Inspect dataset metadata, splits, schema, modalities, licenses, and sample records.
D. If helpful, download a lightweight local snapshot for deeper inspection.
E. Analyze the dataset structure and identify any obvious quality or usability issues.
F. Recommend the most suitable dataset for immediate use in this project.
G. Save a concise exploration report inside the workspace.

Output only:
1. Dataset(s) inspected
2. Key schema and split findings
3. Data quality observations
4. Best recommended dataset
5. Local artifacts created
6. Any single blocking issue