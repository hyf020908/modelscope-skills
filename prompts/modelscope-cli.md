$modelscope-cli

You are running inside local codex-cli.
Use the official ModelScope CLI as the primary interface for authentication, repository creation, download, upload, and repository maintenance.

Hard requirements:
1. Prefer official modelscope CLI commands over ad hoc scripts whenever possible.
2. Reuse existing local files if they are already suitable.
3. If required files are missing, generate the minimal valid files and continue.
4. Do not stop just because the current directory is incomplete.
5. Do not ask me unnecessary questions; make reasonable defaults and keep going.
6. Keep local operations lightweight and reproducible.
7. If authentication is missing, detect it clearly and prepare all remaining steps anyway.
8. At the end, leave the workspace in a usable, publishable state.
9. Prefer explicit repository paths and commit intent over ambiguous default uploads.

Please do the following:
A. Detect whether ModelScope CLI is installed and whether authentication is already configured.
B. Scan the current workspace and infer whether I need a model repo, dataset repo, or both.
C. If the target repo does not exist, create it with a clean name and sensible defaults.
D. If repository metadata files are missing, generate the minimum required files.
E. Download any required upstream assets only if they are truly needed.
F. Upload the prepared local assets to ModelScope Hub.
G. Summarize what was created, uploaded, skipped, and what still needs credentials if anything is blocked.

Output only:
1. Authentication status
2. Repositories created or reused
3. Files generated
4. Files uploaded
5. Any single blocking issue
6. The next minimal action if blocked
