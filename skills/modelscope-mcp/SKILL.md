---
name: modelscope-mcp
description: Configure and use the official ModelScope MCP server for model search, dataset discovery, and repository metadata workflows.
---

# ModelScope MCP

Use this skill when the runtime supports MCP and ModelScope Hub access should be exposed as tools instead of direct shell or SDK calls.

## Operating Mode

- Prefer the official `modelscope-mcp-server`.
- Detect existing MCP client configuration before writing a new one.
- Reuse `MODELSCOPE_API_TOKEN` from shell or runtime configuration instead of storing secrets in files.
- Fall back to CLI or SDK only when MCP is unavailable or unsupported by the client.

## Verified Setup

The official local launch pattern is:

```json
{
  "mcpServers": {
    "modelscope-mcp": {
      "command": "uvx",
      "args": ["modelscope-mcp-server"]
    }
  }
}
```

Authentication:

```bash
export MODELSCOPE_API_TOKEN="<your-token>"
```

## When To Use

- Model and dataset search from MCP-enabled clients.
- Repository metadata lookup without writing custom scripts.
- Tool-driven agent workflows that already rely on MCP.

## When Not To Use

- Simple upload or download tasks that are faster with the CLI.
- Workflows that require capabilities the MCP server does not expose.

## AI Execution Contract

When using this skill, the agent should:

1. Verify whether MCP config already exists.
2. Add the minimal valid config if it is missing.
3. Confirm the expected server command and argument list.
4. Use discovered MCP tools conservatively and verify they exist before calling them.
5. Save a short usage note when creating fresh config files.

## Fallbacks

If MCP is unavailable, switch to:

- `modelscope` CLI for create, download, and upload tasks.
- `HubApi` in Python for scripted automation.

## Guardrails

- Do not assume undocumented tool names.
- Validate tool availability before invoking MCP tools.
- Keep token management outside repository files.
