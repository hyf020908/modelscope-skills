#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Generate and validate repository skill indexes.

Outputs:
- agents/AGENTS.md
- README.md skills table section

Validates:
- .claude-plugin/marketplace.json is in sync with discovered skills
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT / "scripts" / "AGENTS_TEMPLATE.md"
OUTPUT_PATH = ROOT / "agents" / "AGENTS.md"
MARKETPLACE_PATH = ROOT / ".claude-plugin" / "marketplace.json"
README_PATH = ROOT / "README.md"

README_TABLE_START = "<!-- BEGIN_SKILLS_TABLE -->"
README_TABLE_END = "<!-- END_SKILLS_TABLE -->"


def load_template() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.search(r"^---\s*\n(.*?)\n---\s*", text, re.DOTALL)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def collect_skills() -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    for skill_md in ROOT.glob("skills/*/SKILL.md"):
        meta = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = meta.get("name")
        description = meta.get("description")
        if not name or not description:
            continue
        skills.append(
            {
                "name": name,
                "description": description,
                "path": str(skill_md.parent.relative_to(ROOT)),
            }
        )
    return sorted(skills, key=lambda s: s["name"].lower())


def render_agents(template: str, skills: list[dict[str, str]]) -> str:
    def repl(match: re.Match[str]) -> str:
        block = match.group(1).strip("\n")
        rendered_blocks = []
        for skill in skills:
            rendered = (
                block.replace("{{name}}", skill["name"])
                .replace("{{description}}", skill["description"])
                .replace("{{path}}", skill["path"])
            )
            rendered_blocks.append(rendered)
        return "\n".join(rendered_blocks)

    return re.sub(r"{{#skills}}(.*?){{/skills}}", repl, template, flags=re.DOTALL)


def load_marketplace() -> dict:
    if not MARKETPLACE_PATH.exists():
        raise FileNotFoundError(f"marketplace.json not found at {MARKETPLACE_PATH}")
    return json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))


def generate_readme_table(skills: list[dict[str, str]]) -> str:
    marketplace = load_marketplace()
    plugins = {p["source"]: p for p in marketplace.get("plugins", [])}

    lines = [
        "| Name | Description | Documentation |",
        "|------|-------------|---------------|",
    ]

    for skill in skills:
        source = f"./{skill['path']}"
        plugin = plugins.get(source, {})
        name = plugin.get("name", skill["name"])
        description = plugin.get("description", skill["description"])
        doc_link = f"[SKILL.md]({skill['path']}/SKILL.md)"
        lines.append(f"| `{name}` | {description} | {doc_link} |")

    return "\n".join(lines)


def build_readme_content(skills: list[dict[str, str]]) -> str:
    if not README_PATH.exists():
        raise FileNotFoundError(f"README.md not found at {README_PATH}")

    content = README_PATH.read_text(encoding="utf-8")
    start_idx = content.find(README_TABLE_START)
    end_idx = content.find(README_TABLE_END)

    if start_idx == -1 or end_idx == -1:
        raise ValueError(
            f"README markers not found. Expected {README_TABLE_START} and {README_TABLE_END}."
        )
    if end_idx < start_idx:
        raise ValueError("README marker order is invalid.")

    table = generate_readme_table(skills)
    return (
        content[: start_idx + len(README_TABLE_START)]
        + "\n"
        + table
        + "\n"
        + content[end_idx:]
    )


def validate_marketplace(skills: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    marketplace = load_marketplace()
    plugins = marketplace.get("plugins", [])

    skill_by_source = {f"./{s['path']}": s for s in skills}
    plugin_by_source = {p["source"]: p for p in plugins}

    for skill in skills:
        expected_source = f"./{skill['path']}"
        plugin = plugin_by_source.get(expected_source)
        if not plugin:
            errors.append(
                f"Skill '{skill['name']}' at '{skill['path']}' is missing from marketplace.json"
            )
            continue
        if plugin.get("name") != skill["name"]:
            errors.append(
                f"Name mismatch at '{expected_source}': "
                f"SKILL.md='{skill['name']}', marketplace.json='{plugin.get('name')}'"
            )

    for plugin in plugins:
        if plugin.get("source") not in skill_by_source:
            errors.append(
                f"Marketplace plugin '{plugin.get('name')}' at '{plugin.get('source')}' has no SKILL.md"
            )

    return errors


def write_if_changed(path: Path, content: str) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AGENTS and README skill table artifacts.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check that generated outputs are up to date without writing files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    template = load_template()
    skills = collect_skills()

    errors = validate_marketplace(skills)
    if errors:
        print("\nMarketplace.json validation errors:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    agents_content = render_agents(template, skills)
    readme_content = build_readme_content(skills)

    if args.check:
        stale: list[str] = []
        current_agents = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        current_readme = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""

        if current_agents != agents_content:
            stale.append(str(OUTPUT_PATH.relative_to(ROOT)))
        if current_readme != readme_content:
            stale.append(str(README_PATH.relative_to(ROOT)))

        if stale:
            print("Generated artifacts are out of date:", file=sys.stderr)
            for item in stale:
                print(f"  - {item}", file=sys.stderr)
            print("Run: uv run scripts/generate_agents.py", file=sys.stderr)
            sys.exit(1)

        print(f"Marketplace.json validation passed ({len(skills)} skills).")
        print("AGENTS/README artifacts are up to date.")
        return

    changed_agents = write_if_changed(OUTPUT_PATH, agents_content)
    changed_readme = write_if_changed(README_PATH, readme_content)

    print(f"Marketplace.json validation passed ({len(skills)} skills).")
    print(("Wrote" if changed_agents else "Unchanged"), OUTPUT_PATH)
    print(("Updated" if changed_readme else "Unchanged"), README_PATH)


if __name__ == "__main__":
    main()
