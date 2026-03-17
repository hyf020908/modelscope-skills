$modelscope-mcp

You are running inside local codex-cli.
Use this skill to configure and use the official ModelScope MCP server for model search, dataset discovery, and repository metadata workflows.

Hard requirements:
1. Prefer official MCP-based discovery workflows where appropriate.
2. Detect existing MCP configuration before creating new files.
3. If MCP is not configured, generate the minimal valid configuration and continue.
4. Reuse MODELSCOPE token settings if already present.
5. Do not stop just because MCP is missing at the start.
6. Keep the setup simple, explicit, and reproducible.

Please do the following:
A. Check whether ModelScope MCP is already configured in this workspace or user environment.
B. If not, create the minimal MCP client configuration needed for local use.
C. Verify the expected command, arguments, and token wiring.
D. Use MCP-driven discovery to search for relevant models, datasets, or repo metadata for this project.
E. Save the configuration and a short usage note in the workspace.

Output only:
1. MCP configuration status
2. Files created or updated
3. Searches performed
4. Useful discovered resources
5. Any single blocking issue