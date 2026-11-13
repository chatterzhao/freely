#!/usr/bin/env python3
"""Execute strict raw lifecycle effects for shell command adapters."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from raw_metadata_contract import (
    MetadataValidationError,
    read_issue,
    transition as contract_transition,
    transition_issue,
    write_issue,
)


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


def _report_platform_statuses(results: object) -> None:
    if not isinstance(results, dict):
        return
    for platform in sorted(results):
        item = results[platform] if isinstance(results[platform], dict) else {}
        status = item.get("status", "unknown")
        detail = item.get("error", "")
        suffix = f" ({detail})" if detail else ""
        print(f"[raw-lifecycle] close {platform}: {status}{suffix}", file=sys.stderr)


def close_platforms(arguments: list[str]) -> int:
    file_path, root_dir = arguments
    metadata, body = read_issue(file_path)
    platform_ids = metadata.get("platform_ids")
    if not isinstance(platform_ids, dict) or not platform_ids:
        raise ValueError("strict raw has no platform_ids")

    from datetime import datetime, timezone

    closed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Phase 1 — validate locally, without any side effect. Running the pure
    # transition produces both the verdict and the exact metadata to persist,
    # so a non-terminal raw fails here and no platform is touched.
    target = contract_transition(
        metadata, "platform_closed", base_dir=root_dir, at=closed_at
    )

    # Phase 2 — perform the platform write.
    adapter = Path(root_dir) / "docs/system/workspace/scripts/sync/platform-adapter.py"
    environment = dict(os.environ, FREELY_PROJECT_ROOT=root_dir)
    result = subprocess.run(
        [sys.executable, str(adapter), "close-multi", json.dumps(platform_ids)],
        env=environment,
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)

    try:
        payload = json.loads(result.stdout.strip() or "{}")
    except json.JSONDecodeError:
        payload = {}

    # The adapter owns the 0/3/1 classification (`_close_exit_code`). Here we
    # only refuse to certify success it cannot back up: rc 0 must come with
    # every platform actually closed.
    all_closed = (
        isinstance(payload, dict)
        and payload
        and all(
            isinstance(item, dict) and item.get("status") == "closed"
            for item in payload.values()
        )
    )
    code = result.returncode
    if code == 0 and not all_closed:
        code = 1

    if code != 0:
        _report_platform_statuses(payload)
        if code == 3:
            print(
                "[raw-lifecycle] platform close is PARTIAL: at least one platform "
                "is still open; platform_state left unchanged for an idempotent retry",
                file=sys.stderr,
            )
        else:
            print(
                "[raw-lifecycle] platform close failed on every platform; "
                "platform_state left unchanged",
                file=sys.stderr,
            )
        return code

    # Phase 3 — persist the state computed before the platform write, then
    # phase 4 — report through the exit code returned above.
    write_issue(file_path, target, body, base_dir=root_dir)
    return 0


def close_linked(arguments: list[str]) -> int:
    """Close every platform replica of a kind=linked (I-*) document.

    A linked document carries its own field set (kind: linked, promoted_from,
    pre_tests_path, ...), so it cannot go through the strict RAW validator that
    close-platforms uses - that mismatch made every "`issue-sync close I-*`"
    fail with "raw metadata fields are missing, extra, or reordered" and left
    every linked replica OPEN forever.

    The platform write is identical (adapter close-multi); the only local state
    that changes is status: closed (+ updated_at), written back without
    re-validating the raw schema.
    """
    file_path, root_dir = arguments
    metadata, body = read_issue(file_path)
    if str(metadata.get("kind")) != "linked":
        raise ValueError("close-linked requires a kind: linked document")
    platform_ids = metadata.get("platform_ids")
    if not isinstance(platform_ids, dict) or not platform_ids:
        raise ValueError("linked issue has no platform_ids to close")

    from datetime import datetime, timezone

    adapter = Path(root_dir) / "docs/system/workspace/scripts/sync/platform-adapter.py"
    environment = dict(os.environ, FREELY_PROJECT_ROOT=root_dir)
    result = subprocess.run(
        [sys.executable, str(adapter), "close-multi", json.dumps(platform_ids)],
        env=environment,
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)

    try:
        payload = json.loads(result.stdout.strip() or "{}")
    except json.JSONDecodeError:
        payload = {}

    all_closed = (
        isinstance(payload, dict)
        and payload
        and all(
            isinstance(item, dict) and item.get("status") == "closed"
            for item in payload.values()
        )
    )
    code = result.returncode
    if code == 0 and not all_closed:
        code = 1
    if code != 0:
        _report_platform_statuses(payload)
        print(
            "[raw-lifecycle] linked platform close did not finish; local status left unchanged",
            file=sys.stderr,
        )
        return code

    import yaml

    metadata["status"] = "closed"
    metadata["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rendered = yaml.safe_dump(
        dict(metadata), default_flow_style=False, allow_unicode=True, sort_keys=False
    ).strip()
    Path(file_path).write_text(f"---\n{rendered}\n---{body}", encoding="utf-8")
    return 0


def main(arguments: list[str]) -> int:
    if not arguments:
        raise SystemExit("usage: raw_lifecycle_effects.py transition|finalize|close-platforms|close-linked ...")
    command, *payload = arguments
    try:
        if command == "transition" and len(payload) == 8:
            return transition(payload)
        if command == "finalize" and len(payload) == 3:
            return finalize(payload)
        if command == "close-platforms" and len(payload) == 2:
            return close_platforms(payload)
        if command == "close-linked" and len(payload) == 2:
            return close_linked(payload)
    except (MetadataValidationError, ValueError) as error:
        print(f"[raw-lifecycle] {error}", file=sys.stderr)
        return 1
    raise SystemExit(f"invalid raw lifecycle effect arguments: {command}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
