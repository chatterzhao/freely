#!/usr/bin/env python3
"""Unified platform adapter for GitHub/Gitee issue sync.
Usage:
  from platform_adapter import sync_create, sync_comment, sync_close

  # Each function takes identical params, dispatches to all configured platforms
  result = sync_create(local_id="I-xxx", title="...", body="...")
  # -> {"github": {"issue_id": "42", "url": "..."}, "gitee": {"issue_id": "17", "url": "..."}}
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

_ADAPTER_DIR = Path(__file__).resolve().parent       # .../scripts/sync/
_SCRIPTS_DIR = _ADAPTER_DIR.parent                    # .../scripts/
_RUNTIME_DIR = _SCRIPTS_DIR / "runtime"              # .../scripts/runtime/
sys.path.insert(0, str(_RUNTIME_DIR))

from freely_user_env import value as freely_env_value


def _gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run gh CLI command."""
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def _gitee_api(method: str, path: str, data: Optional[dict] = None) -> dict:
    """Call Gitee API via the project's gitee-issue module."""
    result = subprocess.run(
        [sys.executable, str(RUNTIME_DIR / "gitee-issue.py"),
         "--repo", _gitee_repo(),
         method, *([json.dumps(data)] if data else [])],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Gitee {method} failed: {result.stderr.strip()}")
    return {"ok": True, "output": result.stdout.strip()}


def _gh_repo() -> str:
    """Detect GitHub repo from gh CLI."""
    try:
        return _gh("repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner").stdout.strip()
    except Exception:
        return ""


def _gitee_repo() -> str:
    """Detect Gitee repo from git remotes."""
    try:
        result = subprocess.run(
            ["git", "remote", "-v"], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            m = re.search(r"gitee[^:/]*[:/]([^/\s]+/[^/\s]+)", line)
            if m:
                repo = m.group(1); return repo.replace('.git', '')
    except Exception:
        pass
    return ""


def available_platforms() -> list[str]:
    """Return list of platforms that are configured and accessible."""
    platforms = []
    if _gh_repo():
        platforms.append("github")
    if _gitee_repo() and freely_env_value("GITEE_ACCESS_TOKEN", "GITEE_TOKEN"):
        platforms.append("gitee")
    return platforms


# ---- Unified public API ----

def create_issue(local_id: str, title: str, body: str) -> dict[str, dict]:
    """Create an issue on all configured platforms. Returns per-platform results."""
    results = {}
    for platform in available_platforms():
        try:
            if platform == "github":
                result = _gh("issue", "create", "--repo", _gh_repo(),
                            "--title", title, "--body", body)
                url = result.stdout.strip()
                num = url.split("/")[-1]
                results[platform] = {"issue_id": num, "url": url, "status": "created"}
            elif platform == "gitee":
                # Use gitee-issue.py CLI
                result = subprocess.run(
                    [sys.executable, str(RUNTIME_DIR / "gitee-issue.py"),
                     "--repo", _gitee_repo(), "create",
                     "--title", title, "--body", body],
                    capture_output=True, text=True
                )
                if result.returncode != 0:
                    results[platform] = {"status": "error", "error": result.stderr.strip()[:200]}
                else:
                    # Parse issue number from response
                    output = result.stdout.strip()
                    m = re.search(r'"number"\s*:\s*(\d+)', output)
                    num = m.group(1) if m else "?"
                    results[platform] = {"issue_id": num, "status": "created"}
        except Exception as e:
            results[platform] = {"status": "error", "error": str(e)[:200]}
    return results


def add_comment(local_id: str, platform_issue_id: str, comment_body: str) -> dict[str, dict]:
    """Add a comment to an issue on all configured platforms."""
    results = {}
    for platform in available_platforms():
        try:
            if platform == "github":
                result = _gh("issue", "comment", "--repo", _gh_repo(),
                            platform_issue_id, "--body", comment_body)
                results[platform] = {"status": "created"}
            elif platform == "gitee":
                result = subprocess.run(
                    [sys.executable, str(RUNTIME_DIR / "gitee-issue.py"),
                     "--repo", _gitee_repo(), "comment", platform_issue_id, comment_body],
                    capture_output=True, text=True
                )
                results[platform] = {"status": "created" if result.returncode == 0 else "error"}
        except Exception as e:
            results[platform] = {"status": "error", "error": str(e)[:200]}
    return results


def close_issue(local_id: str, platform_issue_id: str) -> dict[str, dict]:
    """Close an issue on all configured platforms."""
    results = {}
    for platform in available_platforms():
        try:
            if platform == "github":
                _gh("issue", "close", "--repo", _gh_repo(), platform_issue_id)
                results[platform] = {"status": "closed"}
            elif platform == "gitee":
                result = subprocess.run(
                    [sys.executable, str(RUNTIME_DIR / "gitee-issue.py"),
                     "--repo", _gitee_repo(), "close", platform_issue_id],
                    capture_output=True, text=True
                )
                results[platform] = {"status": "closed" if result.returncode == 0 else "error"}
        except Exception as e:
            results[platform] = {"status": "error", "error": str(e)[:200]}
    return results


def update_issue(local_id: str, platform_issue_id: str, title: str = "", body: str = "") -> dict[str, dict]:
    """Update an issue on all configured platforms."""
    results = {}
    for platform in available_platforms():
        try:
            if platform == "github":
                args = ["issue", "edit", "--repo", _gh_repo(), platform_issue_id]
                if title:
                    args += ["--title", title]
                if body:
                    args += ["--body", body]
                _gh(*args)
                results[platform] = {"status": "updated"}
            elif platform == "gitee":
                result = subprocess.run(
                    [sys.executable, str(RUNTIME_DIR / "gitee-issue.py"),
                     "--repo", _gitee_repo(), "update", platform_issue_id,
                     *(["--title", title] if title else []),
                     *(["--body", body] if body else [])],
                    capture_output=True, text=True
                )
                results[platform] = {"status": "updated" if result.returncode == 0 else "error"}
        except Exception as e:
            results[platform] = {"status": "error", "error": str(e)[:200]}
    return results


# CLI entry point for testing
if __name__ == "__main__":
    print(f"Available platforms: {available_platforms()}")
    print(f"GitHub repo: {_gh_repo()}")
    print(f"Gitee repo: {_gitee_repo()}")
