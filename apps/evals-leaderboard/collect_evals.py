#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["modelscope>=1.16.0", "packaging>=23.2", "pyyaml>=6.0.0"]
# ///

"""Collect evaluation rows from model README tables and optionally publish to a dataset repo."""

from __future__ import annotations

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml
from modelscope.hub.api import HubApi
from modelscope.hub.file_download import model_file_download

BENCHMARK_KEYS = ["mmlu", "gsm8k", "arc", "humaneval", "mbpp"]


def parse_front_matter(text: str) -> dict:
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1]) or {}
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}


def extract_scores_from_model_index(meta: dict) -> list[dict]:
    rows: list[dict] = []
    model_index = meta.get("model-index")
    if not isinstance(model_index, list):
        return rows

    for entry in model_index:
        if not isinstance(entry, dict):
            continue
        for result in entry.get("results", []):
            dataset = (result.get("dataset") or {}).get("name") or "unknown"
            for metric in result.get("metrics", []):
                value = metric.get("value")
                try:
                    score = float(str(value).replace("%", ""))
                except Exception:
                    continue
                benchmark = (metric.get("name") or metric.get("type") or dataset or "unknown")
                key = benchmark.lower().replace(" ", "_")
                rows.append({"benchmark": benchmark, "benchmark_key": key, "score": score})
    return rows


def collect_for_owner(owner: str, page_size: int, api: HubApi, token: str | None) -> list[dict]:
    payload = api.list_models(owner, page_number=1, page_size=page_size, token=token)
    models = payload.get("Models") or payload.get("models") or []

    rows: list[dict] = []
    for model in models:
        repo_id = model.get("Name") or model.get("ModelId") or model.get("model_id")
        if not repo_id:
            continue
        if "/" not in repo_id:
            repo_id = f"{owner}/{repo_id}"

        with tempfile.TemporaryDirectory() as tmp:
            try:
                readme = model_file_download(repo_id, "README.md", local_dir=tmp, token=token)
            except Exception:
                continue
            text = Path(readme).read_text(encoding="utf-8", errors="ignore")
            meta = parse_front_matter(text)
            scores = extract_scores_from_model_index(meta)
            for score in scores:
                rows.append(
                    {
                        "model_id": repo_id,
                        "benchmark": score["benchmark"],
                        "benchmark_key": score["benchmark_key"],
                        "score": score["score"],
                        "source_type": "model-card",
                        "source_url": f"https://www.modelscope.cn/models/{repo_id}/summary",
                        "contributor": owner,
                        "collected_at": datetime.now(timezone.utc).isoformat(),
                    }
                )
    return rows


def save_outputs(rows: list[dict], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    leaderboard = output_dir / "leaderboard.jsonl"
    metadata = output_dir / "metadata.json"

    leaderboard.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + ("\n" if rows else ""), encoding="utf-8")
    metadata.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "total_entries": len(rows),
                "models_with_scores": len({r['model_id'] for r in rows}),
                "benchmarks": sorted({r["benchmark_key"] for r in rows}),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return leaderboard, metadata


def push_to_dataset(api: HubApi, repo_id: str, leaderboard: Path, metadata: Path, token: str | None) -> None:
    api.create_repo(repo_id, repo_type="dataset", token=token, exist_ok=True)
    api.upload_file(
        path_or_fileobj=str(leaderboard),
        path_in_repo="data/leaderboard.jsonl",
        repo_id=repo_id,
        repo_type="dataset",
        token=token,
        commit_message="Update eval leaderboard",
    )
    api.upload_file(
        path_or_fileobj=str(metadata),
        path_in_repo="data/metadata.json",
        repo_id=repo_id,
        repo_type="dataset",
        token=token,
        commit_message="Update eval metadata",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect eval leaderboard rows from ModelScope model cards")
    parser.add_argument("--owners", nargs="+", default=["Qwen", "AI-ModelScope"], help="Owner/org list")
    parser.add_argument("--limit-per-owner", type=int, default=30)
    parser.add_argument("--output-dir", default="./data")
    parser.add_argument("--push-to", default=None, help="Dataset repo id to publish results")
    parser.add_argument("--token", default=None)
    args = parser.parse_args()

    api = HubApi()
    rows: list[dict] = []
    for owner in args.owners:
        rows.extend(collect_for_owner(owner, args.limit_per_owner, api, args.token))

    leaderboard, metadata = save_outputs(rows, Path(args.output_dir))
    print(f"Saved {len(rows)} rows to {leaderboard}")

    if args.push_to:
        push_to_dataset(api, args.push_to, leaderboard, metadata, args.token)
        print(f"Published leaderboard to {args.push_to}")


if __name__ == "__main__":
    main()
