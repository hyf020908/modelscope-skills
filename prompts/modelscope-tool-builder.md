$modelscope-tool-builder

You are running inside local codex-cli.
Use this skill to build reusable automation scripts for ModelScope Hub API and repository workflows.

Hard requirements:
1. Prefer reusable tools over one-off shell commands.
2. If the current workflow is repetitive, turn it into a script or small utility.
3. Generate clear inputs, outputs, and error handling.
4. Reuse official ModelScope APIs or CLI behavior where appropriate.
5. Keep the tool easy to run from the current workspace.
6. Do not stop because the repository is incomplete; scaffold the minimum viable tool and continue.

Please do the following:
A. Inspect the workspace and identify the most useful automation opportunity.
B. Build a reusable script or small utility for that workflow.
C. Add configuration defaults, input validation, and helpful logging.
D. Create minimal documentation and example usage.
E. If appropriate, test the tool on a lightweight local scenario.

Output only:
1. Tool purpose
2. Files created
3. Inputs and outputs
4. How to run it
5. Test status
6. Any single blocking issue