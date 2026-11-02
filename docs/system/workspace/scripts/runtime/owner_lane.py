#!/usr/bin/env python3
"""Owner-lane identity claim.

An owner-created worktree has no `agent_working` row: the row is normally
written when a manager dispatches a worker.  Without it the daemon cannot
resolve which agent it is and refuses to start (fail-closed), which makes the
owner lane unable to run at all.

The claim below is deliberately narrow:

* it only fills a **missing** row -- an existing binding is returned untouched;
* it only ever claims the **single** configured manager;
* it only accepts a path that git itself reports as a worktree of this project;
* it requires the raw key to come from the branch name instead of guessing.

Anything else returns `agent_id = None` with a reason, and the caller keeps its
original fail-closed behaviour.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROLES = ("worker", "manager", "reviewer")
RAW_KEY = re.compile(r"raw-(\d{8}T\d{4,6}Z)(?:-|$)")


def _runtime(project: str) -> Path:
    return Path(project) / "docs" / "system" / "workspace" / "scripts" / "runtime"


def _rows(project: str) -> list:
    sys.path.insert(0, str(_runtime(project)))
    from agent_working import _db_rpc  # noqa: WPS433 (runtime import by design)

    return _db_rpc(project, "agent_working.get_all", {}).get("rows", []) or []


def _managers(project: str) -> list:
    query = Path(project) / "bin" / "agent-table-query"
    if not query.is_file():
        return []
    result = subprocess.run(
        [str(query), "--project", project, "--list", "manager"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _worktrees(project: str) -> dict:
    result = subprocess.run(
        ["git", "-C", project, "worktree", "list", "--porcelain"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return {}
    mapping: dict = {}
    current = ""
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            current = line[len("worktree "):].strip()
        elif line.startswith("branch ") and current:
            mapping[current] = line[len("branch "):].strip().replace("refs/heads/", "")
    return mapping


def _writer(project: str):
    sys.path.insert(0, str(_runtime(project)))
    from agent_working import agent_assign  # noqa: WPS433

    def write(raw_key: str, path: str, role: str, agent_id: str, branch: str):
        return agent_assign(project, raw_key, role, agent_id, worktree=path, branch=branch)

    return write


def _bound_agent(row: dict) -> str:
    for role in ROLES:
        value = row.get(f"{role}_id") or ""
        if value:
            return str(value).split(":", 1)[0]
    return ""


def _result(**kwargs) -> dict:
    payload = {"agent_id": None, "raw_key": "", "branch": "", "created": False, "reason": ""}
    payload.update(kwargs)
    return payload


def claim(*, project: str, path: str, rows=None, managers=None, worktrees=None, write=None) -> dict:
    """Return the agent that owns `path`, claiming it as manager only if unbound."""
    target = os.path.normpath(path)
    if rows is None:
        try:
            rows = _rows(project)
        except Exception as error:  # no DB socket, broken RPC: we cannot see bindings
            return _result(reason=f"rows_unreadable: {type(error).__name__}")
    for row in rows:
        if not isinstance(row, dict):
            continue
        owned = {os.path.normpath(str(row.get(key) or "")) for key in ("worktree", "test_worktree")}
        owned.discard("")
        if target in owned:
            agent = _bound_agent(row)
            if agent:
                return _result(agent_id=agent, reason="existing")

    managers = _managers(project) if managers is None else managers
    if len(managers) != 1:
        return _result(reason="manager_not_unique")

    worktrees = _worktrees(project) if worktrees is None else worktrees
    branch = ""
    for candidate, name in worktrees.items():
        if os.path.normpath(candidate) == target:
            branch = name
            break
    if not branch:
        return _result(reason="not_a_worktree")

    match = RAW_KEY.search(branch)
    if not match:
        return _result(reason="raw_key_unresolved", branch=branch)
    raw_key = match.group(1)

    writer = _writer(project) if write is None else write
    writer(raw_key, target, "manager", managers[0], branch)
    return _result(agent_id=managers[0], raw_key=raw_key, branch=branch, created=True, reason="claimed")


def main() -> int:
    parser = argparse.ArgumentParser(description="resolve or claim the owner-lane agent identity")
    parser.add_argument("command", choices=["claim", "inspect"])
    parser.add_argument("--project", required=True)
    parser.add_argument("--path", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.command == "inspect":
        result = claim(project=args.project, path=args.path, write=lambda *a, **k: {"dry_run": True})
    else:
        result = claim(project=args.project, path=args.path)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    elif result["agent_id"]:
        print(result["agent_id"])
    if not result["agent_id"]:
        print(f"[owner-lane] no claim: {result['reason']}", file=sys.stderr)
    elif result["created"]:
        print(
            f"[owner-lane] claim: {args.path} → {result['agent_id']} "
            f"(raw {result['raw_key']}, branch {result['branch']})",
            file=sys.stderr,
        )
    return 0 if result["agent_id"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
