#!/usr/bin/env python3
"""Run `uv run <script> --help` checks for repository scripts.

This utility is intended for CI/local validation and returns a non-zero exit
code when any selected script fails the help check.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INCLUDE = ["skills/**/*.py", "apps/**/*.py"]
DEFAULT_EXCLUDE_PARTS = {"__pycache__", ".venv", "venv"}


def discover_scripts(patterns: list[str]) -> list[Path]:
    scripts: list[Path] = []
    seen: set[Path] = set()

    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            if any(part in DEFAULT_EXCLUDE_PARTS for part in path.parts):
                continue
            if path in seen:
                continue
            seen.add(path)
            scripts.append(path)

    return sorted(scripts)


def run_help_check(script: Path, timeout: int) -> tuple[bool, str]:
    cmd = ["uv", "run", str(script), "--help"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=ROOT,
        )
    except subprocess.TimeoutExpired:
        return False, "Timed out while running help command."
    except FileNotFoundError:
        return False, "uv is not installed or not available on PATH."
    except Exception as exc:  # pragma: no cover - defensive path
        return False, f"Unexpected error: {exc}"

    if result.returncode == 0:
        return True, ""

    details = result.stderr.strip() or result.stdout.strip() or "No output captured."
    return False, details


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that repository scripts respond to `uv run <script> --help`."
    )
    parser.add_argument(
        "--include",
        nargs="+",
        default=DEFAULT_INCLUDE,
        help="Glob patterns relative to repo root (default: skills/**/*.py apps/**/*.py).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Per-script timeout in seconds.",
    )
    parser.add_argument(
        "--summary-json",
        default=None,
        help="Optional path to write machine-readable summary JSON.",
    )
    parser.add_argument(
        "--max-error-lines",
        type=int,
        default=20,
        help="Maximum number of error lines printed per failed script.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scripts = discover_scripts(args.include)

    if not scripts:
        print("No scripts matched the selected patterns.", file=sys.stderr)
        return 2

    failures: list[dict[str, str]] = []
    print(f"Checking {len(scripts)} scripts with uv help mode...")

    for script in scripts:
        ok, message = run_help_check(script, timeout=args.timeout)
        rel = script.relative_to(ROOT).as_posix()
        if ok:
            print(f"[OK]   {rel}")
            continue

        lines = message.splitlines()
        preview = "\n".join(lines[: args.max_error_lines])
        print(f"[FAIL] {rel}\n{preview}\n")
        failures.append({"script": rel, "error": message})

    summary = {
        "checked": len(scripts),
        "failed": len(failures),
        "failures": failures,
    }

    if args.summary_json:
        out = Path(args.summary_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"Wrote summary: {out}")

    if failures:
        print(f"Help check failed: {len(failures)}/{len(scripts)} scripts.")
        return 1

    print("All script help checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
