$transformers.js

You are running inside local codex-cli.
Use this skill to build a JavaScript or TypeScript inference workflow with Transformers.js, using ModelScope-hosted assets through local downloads when needed.

Hard requirements:
1. Prefer a minimal working JS/TS inference pipeline over framework-heavy scaffolding.
2. Reuse existing frontend or Node project structure if available.
3. If the project does not exist yet, scaffold the smallest useful app or script.
4. Keep asset handling explicit and reproducible.
5. Support local development with clear install and run steps.
6. Do not stop because the workspace is empty.

Please do the following:
A. Detect whether this project should be browser-based, Node-based, or both.
B. Scaffold or update the JS/TS project accordingly.
C. Wire in Transformers.js inference with a sensible default task and model choice.
D. Prepare local asset download or loading logic where needed.
E. Add a minimal example input/output flow and error handling.
F. Leave the project runnable with concise documentation.

Output only:
1. Project type built
2. Files created or updated
3. Model/task selected
4. Run instructions
5. Any single blocking issue