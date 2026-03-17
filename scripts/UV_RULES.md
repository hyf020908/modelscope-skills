# UV rules

Use these rules for Python scripts in this repository:

1. Use PEP 723 inline dependencies in each runnable script.
2. Run scripts with `uv run`, not `python` directly.
3. Avoid `pip install -r requirements.txt` for repo scripts unless a fallback is required.
4. Avoid virtualenv activation instructions for skill scripts; prefer `uv run`.
5. If manual install is needed, use `uv pip install ...`.
6. Keep command examples consistent with ModelScope SDK/CLI workflows.
