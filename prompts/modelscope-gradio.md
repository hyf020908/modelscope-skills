$modelscope-gradio

You are running inside local codex-cli.
Use this skill to build or update a Gradio demo for the current ModelScope-related project.

Hard requirements:
1. Prefer a minimal, working Gradio app over an overengineered demo.
2. If the project has no UI yet, create one from scratch.
3. Reuse local models, configs, or inference code when available.
4. If backend logic is missing, scaffold the smallest working placeholder pipeline.
5. Keep the app runnable locally with clear structure and sensible defaults.
6. Do not stop because the current workspace is incomplete.
7. Focus on usability: inputs, outputs, examples, and error handling.
8. Keep the demo honest: clearly separate real model inference from placeholder logic.

Please do the following:
A. Inspect the workspace and infer the most likely demo type.
B. Create or update a Gradio app with a clean layout and basic UX.
C. Wire the UI to existing inference logic if present; otherwise generate a minimal stub.
D. Add example inputs and lightweight validation.
E. Ensure the project has the files needed to run the demo.
F. Leave clear run instructions in the workspace.

Output only:
1. Demo type built
2. Main files created or updated
3. Input/output flow
4. Run command
5. Any single blocking issue
