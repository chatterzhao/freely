#!/usr/bin/env python3
"""Deterministic planning and aggregation for guarded PR lifecycle updates."""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any

SAFE_BRANCH_STATES = {"absent", "behind", "equal"}
BLOCKED_BRANCH_STATES = {"ahead", "diverged"}
SUCCESS_PR_STATES = {"created", "reused", "updated"}

# Recovery text is a single source of truth: the same plan that decided
# fail-closed must also decide which hint the operator gets (#4250).
BRANCH_SYNC_RECOVERY = "同步本地分支与对应平台远端后重试；禁止 force push 或原始 push 绕过。"
ENVIRONMENT_RECOVERY = (
    "平台观测失败（网络/认证/权限/远端不可用）：先用 "
    "`git ls-remote --heads <remote> <branch>` 与 `ssh -T git@<host>` 探测可达性与认证，"
    "恢复后重跑同一封装命令；禁止 force push 或原始 push 绕过。"
)


def recovery_for_plan(plan: Mapping[str, Any]) -> str:
    """Pick the recovery hint from the plan's own failure classification.

    A platform with a divergent/ahead branch needs a branch sync. A platform
    whose observation failed (error / unknown / unsupported, or carrying a
    real error detail) needs an environment probe instead. Pointing the latter
    at "sync your branches" is misleading: the branches were never read.
    """
    details = plan.get("platforms", {}) if isinstance(plan, Mapping) else {}
    for detail in details.values():
        if not isinstance(detail, Mapping):
            continue
        if detail.get("error") or detail.get("branch_state") in {
            "error", "unknown", "unsupported"
        }:
            return ENVIRONMENT_RECOVERY
    return BRANCH_SYNC_RECOVERY


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
        observation = observations.get(platform, {})
        state = observation.get("branch_state", "unknown")
        if state in BLOCKED_BRANCH_STATES:
            action = "fail_closed"
            blocked = True
        elif state in SAFE_BRANCH_STATES:
            action = "push_then_ensure_pr" if state in {"absent", "behind"} else "ensure_pr"
        else:
            action = "fail_closed"
            blocked = True
        details[platform] = {"branch_state": state, "action": action}
        # Keep the real cause. Dropping it leaves the operator with only
        # "branch_state: error" and no way to tell a network outage from a
        # missing remote (#4250). Truncate to match the producer's bound.
        error = observation.get("error")
        if error:
            details[platform]["error"] = str(error)[:300]

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
