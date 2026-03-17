#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["modelscope>=1.16.0", "packaging>=23.2"]
# ///

"""Build a contributor leaderboard from ModelScope owner activity summaries."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from modelscope.hub.api import HubApi


def owner_stats(api: HubApi, owner: str, limit: int, token: str | None) -> dict:
    models_payload = api.list_models(owner, page_number=1, page_size=limit, token=token)
    datasets_payload = api.list_datasets(owner, page_number=1, page_size=limit, token=token)

    models = models_payload.get("Models") or models_payload.get("models") or []
    datasets = datasets_payload.get("datasets") or datasets_payload.get("Datasets") or []

    model_count = len(models)
    dataset_count = len(datasets)
    total_points = model_count + dataset_count

    return {
        "username": owner,
        "total_points": total_points,
        "models": model_count,
        "datasets": dataset_count,
    }


def save_outputs(rows: list[dict], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    leaderboard_file = output_dir / "leaderboard.jsonl"
    metadata_file = output_dir / "metadata.json"

    leaderboard_file.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + ("\n" if rows else ""), encoding="utf-8")
    metadata_file.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "total_participants": len(rows),
                "total_points": sum(r["total_points"] for r in rows),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return leaderboard_file, metadata_file


def push(api: HubApi, repo_id: str, leaderboard: Path, metadata: Path, token: str | None) -> None:
    api.create_repo(repo_id, repo_type="dataset", token=token, exist_ok=True)
    api.upload_file(
        path_or_fileobj=str(leaderboard),
        path_in_repo="data/leaderboard.jsonl",
        repo_id=repo_id,
        repo_type="dataset",
        token=token,
        commit_message="Update hackers leaderboard",
    )
    api.upload_file(
        path_or_fileobj=str(metadata),
        path_in_repo="data/metadata.json",
        repo_id=repo_id,
        repo_type="dataset",
        token=token,
        commit_message="Update hackers metadata",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect owner activity summary for leaderboard")
    parser.add_argument("--owners", nargs="+", default=["Qwen", "AI-ModelScope", "iic"])
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output-dir", default="./data")
    parser.add_argument("--push-to", default=None)
    parser.add_argument("--token", default=None)
    args = parser.parse_args()

    api = HubApi()
    rows = [owner_stats(api, owner, args.limit, args.token) for owner in args.owners]
    rows.sort(key=lambda r: r["total_points"], reverse=True)

    leaderboard, metadata = save_outputs(rows, Path(args.output_dir))
    print(f"Saved leaderboard with {len(rows)} owners to {leaderboard}")

    if args.push_to:
        push(api, args.push_to, leaderboard, metadata, args.token)
        print(f"Published leaderboard to {args.push_to}")


if __name__ == "__main__":
    main()
