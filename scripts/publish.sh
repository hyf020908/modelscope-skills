#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

run_generate() {
  uv run scripts/generate_agents.py
  uv run scripts/generate_cursor_plugin.py
}

run_check() {
  # No side effects in check mode.
  uv run scripts/generate_agents.py --check
  uv run scripts/generate_cursor_plugin.py --check

  echo "All generated artifacts are up to date."
}

case "${1:-}" in
  "")
    run_generate
    echo "Publish artifacts generated successfully."
    ;;
  "--check")
    run_check
    ;;
  "-h"|"--help")
    cat <<'EOF'
Usage:
  ./scripts/publish.sh         Generate all publish artifacts
  ./scripts/publish.sh --check Verify generated artifacts are up to date

This script regenerates:
  - agents/AGENTS.md
  - README.md (skills table section)
  - .cursor-plugin/plugin.json
  - .mcp.json
EOF
    ;;
  *)
    echo "Unknown option: $1" >&2
    echo "Use --help for usage." >&2
    exit 2
    ;;
esac
