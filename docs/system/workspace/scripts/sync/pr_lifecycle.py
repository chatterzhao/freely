#!/usr/bin/env python3
"""Deterministic planning and aggregation for guarded PR lifecycle updates."""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any

SAFE_BRANCH_STATES = {"absent", "behind", "equal"}
BLOCKED_BRANCH_STATES = {"ahead", "diverged"}
SUCCESS_PR_STATES = {"created", "reused", "updated"}


def classify_branch(
    local_head: str,
    remote_head: str | None,
    is_ancestor: Callable[[str, str], bool],
) -> str:
    """Classify one platform branch relative to the local candidate."""
    if not remote_head:
        return "absent"
    if local_head == remote_head:
        return "equal"
    if is_ancestor(remote_head, local_head):
        return "behind"
    if is_ancestor(local_head, remote_head):
        return "ahead"
    return "diverged"


def _unique_platforms(configured_platforms: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(platform for platform in configured_platforms if platform))


def plan_platform_updates(
    *,
    configured_platforms: Iterable[str],
    observations: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Build an all-or-nothing execution plan before any platform mutation."""
    platforms = _unique_platforms(configured_platforms)
    details: dict[str, dict[str, Any]] = {}
    blocked = False

    for platform in platforms:
        state = observations.get(platform, {}).get("branch_state", "unknown")
        if state in BLOCKED_BRANCH_STATES:
            action = "fail_closed"
            blocked = True
        elif state in SAFE_BRANCH_STATES:
            action = "push_then_ensure_pr" if state in {"absent", "behind"} else "ensure_pr"
        else:
            action = "fail_closed"
            blocked = True
        details[platform] = {"branch_state": state, "action": action}

    if blocked:
        for detail in details.values():
            if detail["action"] != "fail_closed":
                detail["action"] = "blocked_by_aggregate"
        actions: list[dict[str, str]] = []
    else:
        actions = [
            {"platform": platform, "action": details[platform]["action"]}
            for platform in platforms
        ]

    return {
        "safe_to_execute": not blocked and bool(platforms),
        "actions": actions,
        "platforms": details,
    }


def aggregate_results(
    configured_platforms: Iterable[str],
    results: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Accept only when every configured platform reached local equality and a PR."""
    platforms = _unique_platforms(configured_platforms)
    details: dict[str, dict[str, Any]] = {}
    failed: list[str] = []

    for platform in platforms:
        result = dict(results.get(platform, {}))
        success = (
            result.get("branch_state") == "equal"
            and result.get("pr_state") in SUCCESS_PR_STATES
        )
        result["success"] = success
        details[platform] = result
        if not success:
            failed.append(platform)

    return {
        "success": bool(platforms) and not failed,
        "failed_platforms": failed,
        "platforms": details,
    }
