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


def list_open_issues(platforms: list[str]) -> dict[str, str]:
    """List OPEN issues across all configured platforms. Returns union {number: state}.
    Used by scan's fetch_open_platform_issues to avoid hardcoding gh CLI.
    """
    result: dict[str, str] = {}
    for p in platforms:
        try:
            if p == "github":
                repo = _gh_repo()
                if not repo:
                    continue
                proc = subprocess.run(
                    ["gh", "issue", "list", "--repo", repo,
                     "--state", "open", "--limit", "200",
                     "--json", "number,state"],
                    capture_output=True, text=True, timeout=30)
                if proc.returncode == 0:
                    for issue in json.loads(proc.stdout):
                        result[str(issue["number"])] = issue.get("state", "OPEN")
            elif p == "gitee":
                proc = subprocess.run(
                    [sys.executable, str(_RUNTIME_DIR / "gitee-issue.py"),
                     "--repo", _gitee_repo(), "list",
                     "--state", "open", "--per-page", "50"],
                    capture_output=True, text=True, timeout=30)
                if proc.returncode == 0:
                    for issue in json.loads(proc.stdout):
                        num = str(issue.get("number", issue.get("id", "")))
                        if num:
                            result[num] = issue.get("state", "OPEN")
        except Exception:
            continue
    return result


def fetch_issue_state(platform: str, issue_number: str) -> Optional[str]:
    """Fetch issue state from a single platform. Returns 'OPEN'/'CLOSED' or None."""
    try:
        if platform == "github":
            proc = subprocess.run(
                ["gh", "issue", "view", str(issue_number), "--json", "state"],
                capture_output=True, text=True, timeout=10)
            if proc.returncode == 0:
                return json.loads(proc.stdout).get("state", "")
        elif platform == "gitee":
            proc = subprocess.run(
                [sys.executable, str(_RUNTIME_DIR / "gitee-issue.py"),
                 "--repo", _gitee_repo(), "get", str(issue_number)],
                capture_output=True, text=True, timeout=10)
            if proc.returncode == 0:
                data = json.loads(proc.stdout)
                return data.get("state", "").upper()
    except Exception:
        pass
    return None


def configured_platforms() -> list[str]:
    """Read FREELY_REPO_PLATFORMS from config/env. Falls back to auto-detection."""
    csv = os.environ.get("FREELY_REPO_PLATFORMS", "")
    platforms = [p.strip() for p in csv.split(",") if p.strip()]
    if not platforms:
        platforms = available_platforms()
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
    """Add a comment to an issue on all configured platforms.

    Blocks new comments on closed issues (#3302). Comment sync (issue-sync)
    is exempt — it pushes locally-recorded comments made while the issue was open.
    """
    results = {}
    for platform in available_platforms():
        try:
            # Check if platform issue is closed before commenting (#3302)
            issue_state = _get_issue_state(platform, platform_issue_id)
            if issue_state and issue_state.lower() == "closed":
                results[platform] = {
                    "status": "blocked",
                    "error": (
                        f"Issue #{platform_issue_id} is CLOSED on {platform}. "
                        "Cannot create new comments on closed issues. "
                        "Re-open the issue first, or create a new raw issue via 'freely feedback'."
                    ),
                }
                continue

            if platform == "github":
                _gh("issue", "comment", "--repo", _gh_repo(),
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


def _get_issue_state(platform: str, issue_id: str) -> Optional[str]:
    """Get the state (open/closed) of a platform issue. Returns None if unknown."""
    try:
        if platform == "github":
            result = subprocess.run(
                ["gh", "issue", "view", issue_id, "--repo", _gh_repo(),
                 "--json", "state", "--jq", ".state"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        elif platform == "gitee":
            # Gitee: use 'get' subcommand and parse JSON state field
            result = subprocess.run(
                [sys.executable, str(RUNTIME_DIR / "gitee-issue.py"),
                 "--repo", _gitee_repo(), "get", issue_id],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return str(data.get("state", "")).lower()
    except Exception:
        pass
    return None


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


# ---- raw-issue-pull: find and materialize raw issues from platforms ----

def search_raw_issue(raw_key: str) -> dict[str, dict]:
    """Search all platforms for an OPEN issue matching raw-{key}.
    Returns {platform: {issue_number, title, url}} or empty dict if not found.
    """
    results = {}
    for platform in available_platforms():
        try:
            if platform == "github":
                repo = _gh_repo()
                if not repo:
                    continue
                result = _gh("issue", "list", "--repo", repo, "--state", "open",
                           "--search", f"raw-{raw_key} in:title", "--limit", "5",
                           "--json", "number,title,url", check=False)
                if result.returncode == 0 and result.stdout.strip():
                    issues = json.loads(result.stdout)
                    for issue in issues:
                        title = issue.get("title", "")
                        if f"RAW-{raw_key}" in title or f"raw-{raw_key}" in title:
                            results[platform] = {
                                "issue_number": str(issue["number"]),
                                "title": title,
                                "url": issue.get("url", ""),
                            }
                            break
                # Fallback: search raw_key in body
                if platform not in results:
                    result = _gh("issue", "list", "--repo", repo, "--state", "open",
                               "--search", f"raw-{raw_key} in:body", "--limit", "5",
                               "--json", "number,title,url", check=False)
                    if result.returncode == 0 and result.stdout.strip():
                        issues = json.loads(result.stdout)
                        for issue in issues:
                            results[platform] = {
                                "issue_number": str(issue["number"]),
                                "title": issue.get("title", ""),
                                "url": issue.get("url", ""),
                            }
                            break
            elif platform == "gitee":
                result = subprocess.run(
                    [sys.executable, str(RUNTIME_DIR / "gitee-issue.py"),
                     "--repo", _gitee_repo(), "list", "--state", "open", "--limit", "50"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    try:
                        issues = json.loads(result.stdout)
                    except Exception:
                        issues = []
                    for issue in issues:
                        title = issue.get("title", "")
                        if f"RAW-{raw_key}" in title or f"raw-{raw_key}" in title:
                            results[platform] = {
                                "issue_number": str(issue.get("number", issue.get("id", ""))),
                                "title": title,
                                "url": issue.get("html_url", issue.get("url", "")),
                            }
                            break
                    # Fallback: search raw_key in body
                    if platform not in results:
                        for issue in issues:
                            body = issue.get("body", "") or ""
                            if f"raw-{raw_key}" in body:
                                results[platform] = {
                                    "issue_number": str(issue.get("number", issue.get("id", ""))),
                                    "title": issue.get("title", ""),
                                    "url": issue.get("html_url", issue.get("url", "")),
                                }
                                break
        except Exception:
            continue
    return results


def fetch_issue(platform: str, issue_number: str) -> dict:
    """Fetch full issue details from a platform.
    Returns dict with title, body, created_at, updated_at, labels, state or empty dict on failure.
    """
    try:
        if platform == "github":
            repo = _gh_repo()
            result = _gh("issue", "view", issue_number, "--repo", repo,
                       "--json", "title,body,createdAt,updatedAt,labels,state",
                       check=False)
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                return {
                    "title": data.get("title", ""),
                    "body": data.get("body", ""),
                    "created_at": data.get("createdAt", ""),
                    "updated_at": data.get("updatedAt", ""),
                    "labels": [l["name"] for l in data.get("labels", [])],
                    "state": data.get("state", "").upper(),
                }
        elif platform == "gitee":
            result = subprocess.run(
                [sys.executable, str(RUNTIME_DIR / "gitee-issue.py"),
                 "--repo", _gitee_repo(), "get", issue_number],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {
                    "title": data.get("title", ""),
                    "body": data.get("body", ""),
                    "created_at": data.get("created_at", ""),
                    "updated_at": data.get("updated_at", ""),
                    "labels": [l.get("name", "") for l in data.get("labels", [])],
                    "state": data.get("state", "").upper(),
                }
    except Exception:
        pass
    return {}


def _created_at_to_key(created_at: str) -> Optional[str]:
    """Convert platform created_at to standard raw key.
    "2026-05-06T10:00:35Z" → "20260506T100035Z"
    """
    try:
        from datetime import datetime, timezone
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        return dt.strftime("%Y%m%dT%H%M%SZ")
    except Exception:
        return None


def _update_issue_title(platform: str, issue_number: str, new_title: str) -> bool:
    """Update issue title on platform. Returns True on success."""
    try:
        if platform == "github":
            _gh("issue", "edit", "--repo", _gh_repo(), issue_number, "--title", new_title)
            return True
        elif platform == "gitee":
            result = subprocess.run(
                [sys.executable, str(_RUNTIME_DIR / "gitee-issue.py"),
                 "--repo", _gitee_repo(), "update", issue_number,
                 "--title", new_title],
                capture_output=True, text=True
            )
            return result.returncode == 0
    except Exception:
        pass
    return False


def pull_raw_issue(raw_key: str, target_dir: Path) -> Optional[dict]:
    """Find raw issue on platform, fetch it, and materialize to target_dir/issue.md.
    Returns the materialized issue dict with path and platform_ids, or None if not found.
    """
    # 1. Search on all platforms
    results = search_raw_issue(raw_key)
    if not results:
        return None

    # 2. Use primary platform first, fall back to any
    platform = "github" if "github" in results else next(iter(results))
    info = results[platform]
    issue_number = info["issue_number"]

    # 3. Fetch full issue details
    details = fetch_issue(platform, issue_number)
    if not details:
        return None

    # 3a. Standardize title only when it lacks the canonical raw-key.
    # If title already has raw-{raw_key}, it is the truth source — skip.
    title = info.get("title", "")
    title_has_key = f"raw-{raw_key}" in title or f"RAW-{raw_key}" in title
    if not title_has_key:
        created_at = details.get("created_at", "")
        standard_key = _created_at_to_key(created_at) if created_at else None
        if standard_key and standard_key != raw_key:
            new_title = title.replace(f"raw-{raw_key}", f"raw-{standard_key}")
            if new_title != title:
                _update_issue_title(platform, issue_number, new_title)
                raw_key = standard_key
                target_dir = target_dir.parent / f"raw-{raw_key}"

    # 4. Materialize to docs/issues/raw-{key}/issue.md
    target_dir.mkdir(parents=True, exist_ok=True)
    issue_file = target_dir / "issue.md"

    # Build platform_ids
    platform_ids = {}
    for plat, plat_info in results.items():
        platform_ids[plat] = {
            "issue_id": plat_info["issue_number"],
            "url": plat_info.get("url", ""),
            "synced_at": "",
        }

    # Parse phase from labels
    phase = "proposed"
    for label in details.get("labels", []):
        if label.startswith("phase/"):
            phase = label.replace("phase/", "")
            break

    # Write issue.md with proper frontmatter
    frontmatter = {
        "local_id": f"raw-{raw_key}",
        "kind": "raw",
        "phase_state": phase,
        "platform_ids": platform_ids,
        "primary_platform": platform,
        "canonical_issue_path": "",
        "last_synced_comment_at": {},
        "hash": "",
        "created_at": details.get("created_at", ""),
        "updated_at": details.get("updated_at", ""),
        "intake_id": "",
        "author": "platform",
        "channel": platform,
        "session_refs": [],
    }

    import yaml
    yaml.SafeLoader.yaml_implicit_resolvers.pop('tag:yaml.org,2002:timestamp', None)
    fm_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
    body = details.get("body", "")
    # Remove frontmatter from body if present (GH issue body may contain old frontmatter)
    if body.startswith("---"):
        parts = body.split("---", 2)
        body = parts[2].strip() if len(parts) >= 3 else body

    issue_file.write_text(f"---\n{fm_str}\n---\n\n{body}\n", encoding="utf-8")

    return {
        "path": str(issue_file),
        "local_id": f"raw-{raw_key}",
        "platform": platform,
        "issue_number": issue_number,
        "platform_ids": platform_ids,
    }


# ── PR Operations (#3340) ────────────────────────────────────────────

def create_pr(branch: str, base: str = "develop", title: str = "", body: str = "") -> dict:
    """Create a PR on all configured platforms. Returns {platform: {url, number}}."""
    results = {}
    for platform in available_platforms():
        try:
            if platform == "github":
                cmd = ["gh", "pr", "create", "--repo", _gh_repo(),
                       "--head", branch, "--base", base]
                if title:
                    cmd.extend(["--title", title])
                if body:
                    cmd.extend(["--body", body])
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    # Extract PR URL from stdout
                    url = result.stdout.strip()
                    number = url.split("/")[-1] if url else ""
                    results[platform] = {"url": url, "number": number, "status": "created"}
                else:
                    results[platform] = {"status": "error", "error": result.stderr[:200]}
            elif platform == "gitee":
                # Gitee: push branch first, then API create PR
                results[platform] = {"status": "skipped", "error": "gitee PR creation via API not yet implemented"}
        except Exception as e:
            results[platform] = {"status": "error", "error": str(e)[:200]}
    return results


def merge_pr(platform: str, pr_number: str) -> dict:
    """Merge a PR on the specified platform."""
    try:
        if platform == "github":
            result = subprocess.run(
                ["gh", "pr", "merge", pr_number, "--repo", _gh_repo(),
                 "--squash", "--delete-branch"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return {"status": "merged", "platform": platform, "number": pr_number}
            return {"status": "error", "error": result.stderr[:200]}
        elif platform == "gitee":
            return {"status": "skipped", "error": "gitee PR merge via API not yet implemented"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:200]}


def close_pr(platform: str, pr_number: str) -> dict:
    """Close a PR without merging on the specified platform."""
    try:
        if platform == "github":
            result = subprocess.run(
                ["gh", "pr", "close", pr_number, "--repo", _gh_repo()],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return {"status": "closed", "platform": platform, "number": pr_number}
            return {"status": "error", "error": result.stderr[:200]}
        elif platform == "gitee":
            return {"status": "skipped", "error": "gitee PR close via API not yet implemented"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:200]}


# CLI entry point for testing
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        raw_key = sys.argv[2] if len(sys.argv) > 2 else ""
        result = search_raw_issue(raw_key)
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "fetch":
        platform, num = sys.argv[2], sys.argv[3]
        result = fetch_issue(platform, num)
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "close":
        platform, issue_number = sys.argv[2], sys.argv[3]
        result = close_issue("", issue_number)
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "pull":
        raw_key = sys.argv[2]
        target = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(f"docs/issues/raw-{raw_key}")
        result = pull_raw_issue(raw_key, target)
        print(json.dumps(result, indent=2, default=str))
    elif len(sys.argv) > 1 and sys.argv[1] == "create-pr":
        branch, base = sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "develop"
        title = sys.argv[4] if len(sys.argv) > 4 else ""
        body = sys.argv[5] if len(sys.argv) > 5 else ""
        result = create_pr(branch, base, title, body)
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "merge-pr":
        platform, pr_number = sys.argv[2], sys.argv[3]
        result = merge_pr(platform, pr_number)
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "close-pr":
        platform, pr_number = sys.argv[2], sys.argv[3]
    elif len(sys.argv) > 1 and sys.argv[1] == "create-issue":
        local_id, title, body = sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else ""
        result = create_issue(local_id, title, body)
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "comment":
        local_id, comment_body = sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ""
        result = sync_comment(local_id, comment_body)
        print(json.dumps(result, indent=2))
        result = close_pr(platform, pr_number)
        print(json.dumps(result, indent=2))
    else:
        print(f"Available platforms: {available_platforms()}")
        print(f"GitHub repo: {_gh_repo()}")
        print(f"Gitee repo: {_gitee_repo()}")
