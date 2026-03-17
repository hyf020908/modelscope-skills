---
name: modelscope-mcp
description: Configure and use the official ModelScope MCP server for model search, dataset discovery, and repository metadata workflows.
---

# ModelScope MCP

Use this skill when an agent runtime supports MCP tools and you want ModelScope Hub capabilities exposed through MCP.

## Verified Setup

The official local setup uses `uvx modelscope-mcp-server`.

Minimal MCP server entry:

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

Set authentication in your shell before launching the MCP client:

```bash
export MODELSCOPE_API_TOKEN="<your-token>"
```

## When To Use

- Model and dataset search from MCP-enabled clients.
- Repository metadata lookup without custom API scripts.
- Tool-augmented agent workflows where MCP is preferred over direct SDK calls.

## Mode Separation

- Local mode: `command` + `args` (recommended default).
- Remote mode: use only when your organization provides a documented MCP HTTP endpoint.

## Fallbacks

If MCP is unavailable, switch to:

- `modelscope` CLI for create/download/upload tasks.
- `HubApi` in Python scripts for automation.

## Guardrails

- Do not assume undocumented tool names.
- Validate tool availability before calling MCP tools.
- Keep token management outside repository files.
