#!/usr/bin/env python3
"""Execute strict raw lifecycle effects for shell command adapters."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from raw_metadata_contract import MetadataValidationError, read_issue, transition_issue


def _primary_child(metadata: dict[str, object], root_dir: str) -> tuple[str, str]:
    children = metadata.get("promoted_children")
    if not isinstance(children, list) or not children:
        raise MetadataValidationError("promotion finalize requires promoted children")
    issue_root = Path(root_dir) / "docs/B2-docs"
    for child in children:
        issue_id = str(child)
        if not issue_id.startswith("I-"):
            continue
        matches = sorted(issue_root.rglob(f"{issue_id}*.md"))
        if matches:
            return issue_id, matches[0].relative_to(root_dir).as_posix()
    raise MetadataValidationError("no promoted child has a canonical issue file")


def transition(arguments: list[str]) -> int:
    file_path, event, root_dir, issue_id, issue_path, source_candidate, at, note = arguments
    payload = {"at": at}
    for key, value in (
        ("issue_id", issue_id),
        ("issue_path", issue_path),
        ("source_candidate", source_candidate),
        ("note", note),
    ):
        if value:
            payload[key] = value
    transition_issue(file_path, event, base_dir=root_dir, **payload)
    return 0


def finalize(arguments: list[str]) -> int:
    file_path, root_dir, at = arguments
    metadata, _ = read_issue(file_path)
    issue_id, issue_path = _primary_child(metadata, root_dir)
    transition_issue(
        file_path,
        "promotion_finalized",
        base_dir=root_dir,
        issue_id=issue_id,
        issue_path=issue_path,
        at=at,
    )
    return 0


def close_platforms(arguments: list[str]) -> int:
    file_path, root_dir = arguments
    metadata, _ = read_issue(file_path)
    platform_ids = metadata.get("platform_ids")
    if not isinstance(platform_ids, dict) or not platform_ids:
        raise ValueError("strict raw has no platform_ids")

    adapter = Path(root_dir) / "docs/system/workspace/scripts/sync/platform-adapter.py"
    environment = dict(os.environ, FREELY_PROJECT_ROOT=root_dir)
    result = subprocess.run(
        [sys.executable, str(adapter), "close-multi", json.dumps(platform_ids)],
        env=environment,
    )
    if result.returncode != 0:
        return result.returncode

    from datetime import datetime, timezone

    closed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    transition_issue(file_path, "platform_closed", base_dir=root_dir, at=closed_at)
    return 0


def main(arguments: list[str]) -> int:
    if not arguments:
        raise SystemExit("usage: raw_lifecycle_effects.py transition|finalize|close-platforms ...")
    command, *payload = arguments
    try:
        if command == "transition" and len(payload) == 8:
            return transition(payload)
        if command == "finalize" and len(payload) == 3:
            return finalize(payload)
        if command == "close-platforms" and len(payload) == 2:
            return close_platforms(payload)
    except (MetadataValidationError, ValueError) as error:
        print(f"[raw-lifecycle] {error}", file=sys.stderr)
        return 1
    raise SystemExit(f"invalid raw lifecycle effect arguments: {command}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
