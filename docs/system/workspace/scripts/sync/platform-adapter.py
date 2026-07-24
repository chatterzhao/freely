#!/usr/bin/env python3
"""Unified platform adapter — Handler registry pattern.

How to add a new platform (e.g. GitLab):

  1. Subclass PlatformHandler:
     class GitLabHandler(PlatformHandler):
         name = "gitlab"
         def detect(self) -> bool: ...                    # mandatory
         def detect_repo(self) -> str: ...                # optional, for repo detection
         def create_issue(self, title, body) -> dict: ... # mandatory
         def close_issue(self, issue_number) -> dict: ... # mandatory
         # Override other methods as needed. Default: {"status":"error","error":"not implemented"}

  2. Register it:
     register(GitLabHandler())

  3. That's it. Every public function (create_issue, close_issue, search_raw_issue,
     create_pr, ...) automatically iterates all registered handlers via the registry.
     No if/elif chains to modify. No caller changes needed.

  Mandatory methods (abstract — must implement):
    name, detect, create_issue, close_issue

  Optional methods (override if platform supports it):
    add_comment, update_issue, get_issue_state, search_raw_issue, fetch_issue,
    create_pr, merge_pr, close_pr, get_assignees, set_assignee, list_open_issues

Usage:
  from platform_adapter import create_issue, close_issue, create_pr, ...
  result = create_issue(local_id="I-xxx", title="...", body="...")
  # -> {"github": {"issue_id": "42", ...}, "gitee": {"issue_id": "17", ...}}
"""
from __future__ import annotations
import json, os, re, subprocess, sys
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

_ADAPTER_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _ADAPTER_DIR.parent
_RUNTIME_DIR = _SCRIPTS_DIR / "runtime"
sys.path.insert(0, str(_ADAPTER_DIR))
sys.path.insert(0, str(_RUNTIME_DIR))
from freely_user_env import value as freely_env_value
from freely_config import read_config

# ══════════════════════════════════════════════
# Abstract PlatformHandler — new platform? subclass this.
# ══════════════════════════════════════════════

class PlatformHandler(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def detect(self) -> bool: ...
    def detect_repo(self) -> str: return ""
    @abstractmethod
    def create_issue(self, title: str, body: str) -> dict: ...
    @abstractmethod
    def close_issue(self, issue_number: str) -> dict: ...
    def add_comment(self, issue_number: str, comment_body: str) -> dict:
        return {"status": "error", "error": "not implemented"}
    def update_issue(self, issue_number: str, title: str = "", body: str = "") -> dict:
        return {"status": "error", "error": "not implemented"}
    def get_issue_state(self, issue_number: str) -> Optional[str]: return None
    def search_raw_issue(self, raw_key: str) -> Optional[dict]: return None
    def fetch_issue(self, issue_number: str) -> dict: return {}
    def create_pr(self, branch: str, base: str, title: str, body: str) -> dict:
        return {"status": "error", "error": "not implemented"}
    def ensure_pr(self, branch: str, base: str, title: str, body: str) -> dict:
        return self.create_pr(branch, base, title, body)
    def remote_name(self) -> str:
        try:
            remotes = subprocess.run(
                ["git", "remote"], capture_output=True, text=True, check=True
            ).stdout.splitlines()
            fallback = ""
            for remote in remotes:
                url = subprocess.run(
                    ["git", "remote", "get-url", remote], capture_output=True, text=True
                ).stdout.strip()
                if self.name in remote.lower() or self.name in url.lower():
                    return remote
                if not fallback and remote != "all":
                    fallback = remote
            return fallback if len([r for r in remotes if r != "all"]) == 1 else ""
        except Exception:
            return ""
    def fetch_branch_head(self, branch: str) -> Optional[str]:
        remote = self.remote_name()
        if not remote:
            return None
        ref = f"refs/remotes/{remote}/{branch}"
        fetched = subprocess.run(
            ["git", "fetch", remote, f"+refs/heads/{branch}:{ref}"],
            capture_output=True,
            text=True,
        )
        if fetched.returncode != 0:
            probe = subprocess.run(
                ["git", "ls-remote", "--heads", remote, branch],
                capture_output=True,
                text=True,
            )
            if probe.returncode == 0 and not probe.stdout.strip():
                return None
            raise RuntimeError((fetched.stderr or probe.stderr).strip()[:300])
        resolved = subprocess.run(
            ["git", "rev-parse", ref], capture_output=True, text=True, check=True
        )
        return resolved.stdout.strip()
    def push_branch(self, branch: str) -> dict:
        remote = self.remote_name()
        if not remote:
            return {"status": "error", "error": f"no remote for {self.name}"}
        pushed = subprocess.run(
            ["git", "push", remote, f"{branch}:refs/heads/{branch}"],
            capture_output=True,
            text=True,
        )
        if pushed.returncode != 0:
            return {"status": "error", "error": pushed.stderr.strip()[:300]}
        return {"status": "pushed", "remote": remote}
    def merge_pr(self, pr_number: str) -> dict:
        return {"status": "error", "error": "not implemented"}
    def close_pr(self, pr_number: str) -> dict:
        return {"status": "error", "error": "not implemented"}
    def get_assignees(self, issue_number: str) -> list[str]: return []
    def set_assignee(self, issue_number: str, login: str) -> tuple[bool, str]:
        return False, "not implemented"
    def list_open_issues(self) -> dict[str, str]: return {}

# ══════════════════════════════════════════════
# Registry
# ══════════════════════════════════════════════

_registry: list[PlatformHandler] = []

def register(handler: PlatformHandler):
    _registry.append(handler)

def _handlers() -> list[PlatformHandler]:
    return [h for h in _registry if h.detect()]

def _handler_for(platform: str) -> Optional[PlatformHandler]:
    for h in _registry:
        if h.name == platform and h.detect():
            return h
    return None

# ══════════════════════════════════════════════
# GitHub Handler
# ══════════════════════════════════════════════

class GitHubHandler(PlatformHandler):
    name = "github"

    def detect(self) -> bool:
        try:
            subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner"],
                          capture_output=True, timeout=10, check=True)
            return True
        except Exception:
            return False

    def detect_repo(self) -> str:
        try:
            r = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner",
                               "-q", ".nameWithOwner"], capture_output=True, text=True, timeout=10)
            return r.stdout.strip()
        except Exception:
            return ""

    def _repo(self) -> str: return self.detect_repo()

    def create_issue(self, title, body):
        r = subprocess.run(["gh", "issue", "create", "--repo", self._repo(), "--title", title, "--body", body],
                          capture_output=True, text=True)
        if r.returncode != 0:
            return {"status": "error", "error": r.stderr[:200]}
        url = r.stdout.strip()
        return {"issue_id": url.split("/")[-1], "url": url, "status": "created"}

    def close_issue(self, issue_number):
        r = subprocess.run(["gh", "issue", "close", "--repo", self._repo(), issue_number],
                          capture_output=True, text=True)
        return {"status": "closed" if r.returncode == 0 else "error",
                "error": r.stderr[:200] if r.returncode != 0 else ""}

    def add_comment(self, issue_number, comment_body):
        r = subprocess.run(["gh", "issue", "comment", "--repo", self._repo(), issue_number, "--body", comment_body],
                          capture_output=True, text=True)
        return {"status": "created" if r.returncode == 0 else "error"}

    def update_issue(self, issue_number, title="", body=""):
        args = ["gh", "issue", "edit", "--repo", self._repo(), issue_number]
        if title: args += ["--title", title]
        if body: args += ["--body", body]
        r = subprocess.run(args, capture_output=True, text=True)
        return {"status": "updated" if r.returncode == 0 else "error"}

    def get_issue_state(self, issue_number):
        try:
            r = subprocess.run(["gh", "issue", "view", issue_number, "--repo", self._repo(),
                               "--json", "state", "--jq", ".state"],
                              capture_output=True, text=True, timeout=10)
            return r.stdout.strip() if r.returncode == 0 else None
        except Exception:
            return None

    def search_raw_issue(self, raw_key):
        repo = self._repo()
        if not repo: return None
        try:
            r = subprocess.run(["gh", "issue", "list", "--repo", repo, "--state", "open",
                               "--search", f"raw-{raw_key} in:title", "--limit", "5",
                               "--json", "number,title,url"],
                              capture_output=True, text=True, timeout=15)
            if r.returncode == 0 and r.stdout.strip():
                for issue in json.loads(r.stdout):
                    title = issue.get("title", "")
                    if f"RAW-{raw_key}" in title or f"raw-{raw_key}" in title:
                        return {"issue_number": str(issue["number"]), "title": title, "url": issue.get("url", "")}
            r2 = subprocess.run(["gh", "issue", "list", "--repo", repo, "--state", "open",
                                "--search", f"raw-{raw_key} in:body", "--limit", "5",
                                "--json", "number,title,url"],
                               capture_output=True, text=True, timeout=15)
            if r2.returncode == 0 and r2.stdout.strip():
                for issue in json.loads(r2.stdout):
                    return {"issue_number": str(issue["number"]),
                            "title": issue.get("title", ""), "url": issue.get("url", "")}
        except Exception:
            pass
        return None

    def fetch_issue(self, issue_number):
        try:
            r = subprocess.run(["gh", "issue", "view", issue_number, "--repo", self._repo(),
                               "--json", "title,body,createdAt,updatedAt,labels,state"],
                              capture_output=True, text=True, timeout=15)
            if r.returncode == 0 and r.stdout.strip():
                data = json.loads(r.stdout)
                return {"title": data.get("title", ""), "body": data.get("body", ""),
                        "created_at": data.get("createdAt", ""), "updated_at": data.get("updatedAt", ""),
                        "labels": [l["name"] for l in data.get("labels", [])],
                        "state": data.get("state", "").upper()}
        except Exception:
            pass
        return {}

    def create_pr(self, branch, base, title, body):
        cmd = ["gh", "pr", "create", "--repo", self._repo(), "--head", branch, "--base", base]
        if title: cmd.extend(["--title", title])
        if body: cmd.extend(["--body", body])
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0:
            url = r.stdout.strip()
            return {"url": url, "number": url.split("/")[-1] if url else "", "status": "created"}
        return {"status": "error", "error": r.stderr[:200]}

    def ensure_pr(self, branch, base, title, body):
        listed = subprocess.run(
            ["gh", "pr", "list", "--repo", self._repo(), "--head", branch,
             "--base", base, "--state", "open", "--json", "number,url,title,body"],
            capture_output=True,
            text=True,
        )
        if listed.returncode != 0:
            return {"status": "error", "error": listed.stderr.strip()[:200]}
        try:
            matches = json.loads(listed.stdout or "[]")
        except json.JSONDecodeError as exc:
            return {"status": "error", "error": f"invalid GitHub PR response: {exc}"}
        if not matches:
            return self.create_pr(branch, base, title, body)
        existing = matches[0]
        number = str(existing.get("number", ""))
        changed = existing.get("title", "") != title or existing.get("body", "") != body
        if changed:
            edited = subprocess.run(
                ["gh", "pr", "edit", number, "--repo", self._repo(),
                 "--title", title, "--body", body],
                capture_output=True,
                text=True,
            )
            if edited.returncode != 0:
                return {"status": "error", "error": edited.stderr.strip()[:200]}
        return {
            "status": "updated" if changed else "reused",
            "number": number,
            "url": existing.get("url", ""),
        }

    def merge_pr(self, pr_number):
        r = subprocess.run(["gh", "pr", "merge", pr_number, "--repo", self._repo(),
                           "--squash", "--delete-branch"], capture_output=True, text=True)
        return {"status": "merged", "platform": self.name, "number": pr_number} if r.returncode == 0 else {"status": "error", "error": r.stderr[:200]}

    def close_pr(self, pr_number):
        r = subprocess.run(["gh", "pr", "close", pr_number, "--repo", self._repo()],
                          capture_output=True, text=True)
        return {"status": "closed", "platform": self.name, "number": pr_number} if r.returncode == 0 else {"status": "error", "error": r.stderr[:200]}

    def get_assignees(self, issue_number):
        try:
            r = subprocess.run(["gh", "issue", "view", issue_number, "--repo", self._repo(),
                               "--json", "assignees", "--jq", ".[].login"],
                              capture_output=True, text=True)
            if r.returncode != 0:
                return []
            return [line.strip() for line in r.stdout.splitlines() if line.strip()]
        except Exception:
            return []

    def set_assignee(self, issue_number, login):
        try:
            subprocess.run(["gh", "api", "--method", "POST",
                           f"repos/{self._repo()}/issues/{issue_number}/assignees", "--input", "-"],
                          input=f'{{"assignees":["{login}"]}}', text=True, check=True, capture_output=True)
            return True, f"Assigned {login} to GitHub #{issue_number}"
        except Exception as e:
            return False, f"Failed to assign on GitHub: {e}"

    def list_open_issues(self):
        repo = self._repo()
        if not repo: return {}
        try:
            r = subprocess.run(["gh", "issue", "list", "--repo", repo, "--state", "open", "--limit", "200",
                               "--json", "number,state"], capture_output=True, text=True, timeout=30)
            return {str(i["number"]): i.get("state", "OPEN") for i in json.loads(r.stdout)} if r.returncode == 0 and r.stdout.strip() else {}
        except Exception:
            return {}

# ══════════════════════════════════════════════
# Gitee Handler
# ══════════════════════════════════════════════

class GiteeHandler(PlatformHandler):
    name = "gitee"

    def detect(self) -> bool:
        return bool(freely_env_value("GITEE_ACCESS_TOKEN", "GITEE_TOKEN")) and bool(self.detect_repo())

    def detect_repo(self) -> str:
        try:
            r = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
            for line in r.stdout.splitlines():
                m = re.search(r"gitee[^:/]*[:/]([^/\s]+/[^/\s]+)", line)
                if m: return m.group(1).replace('.git', '')
        except Exception:
            pass
        return ""

    def _repo(self) -> str: return self.detect_repo()

    def _run(self, *args):
        return subprocess.run([sys.executable, str(_RUNTIME_DIR / "gitee-issue.py"),
                               "--repo", self._repo(), *args], capture_output=True, text=True)

    def create_issue(self, title, body):
        r = self._run("create", "--title", title, "--body", body)
        if r.returncode != 0: return {"status": "error", "error": r.stderr.strip()[:200]}
        m = re.search(r'"number"\s*:\s*"?([^"\s,]+)"?', r.stdout.strip())
        return {"issue_id": m.group(1) if m else "?", "status": "created"}

    def close_issue(self, issue_number):
        r = self._run("close", issue_number)
        return {"status": "closed" if r.returncode == 0 else "error"}

    def add_comment(self, issue_number, comment_body):
        r = self._run("comment", issue_number, "--body", comment_body)
        return {"status": "created" if r.returncode == 0 else "error"}

    def update_issue(self, issue_number, title="", body=""):
        args = ["update", issue_number]
        if title: args += ["--title", title]
        if body: args += ["--body", body]
        r = self._run(*args)
        return {"status": "updated" if r.returncode == 0 else "error"}

    def get_issue_state(self, issue_number):
        try:
            r = self._run("get", issue_number)
            if r.returncode == 0 and r.stdout.strip():
                return str(json.loads(r.stdout).get("state", "")).lower()
        except Exception:
            pass
        return None

    def search_raw_issue(self, raw_key):
        r = self._run("list", "--state", "open", "--per-page", "50")
        if r.returncode != 0: return None
        try:
            issues = json.loads(r.stdout)
        except Exception:
            return None
        for issue in issues:
            title, body = issue.get("title", ""), issue.get("body", "") or ""
            if f"RAW-{raw_key}" in title or f"raw-{raw_key}" in title:
                return {"issue_number": str(issue.get("number", issue.get("id", ""))),
                        "title": title, "url": issue.get("html_url", issue.get("url", ""))}
        for issue in issues:
            if f"raw-{raw_key}" in (issue.get("body", "") or ""):
                return {"issue_number": str(issue.get("number", issue.get("id", ""))),
                        "title": issue.get("title", ""), "url": issue.get("html_url", issue.get("url", ""))}
        return None

    def fetch_issue(self, issue_number):
        r = self._run("get", issue_number)
        if r.returncode == 0 and r.stdout.strip():
            try:
                data = json.loads(r.stdout)
                return {"title": data.get("title", ""), "body": data.get("body", ""),
                        "created_at": data.get("created_at", ""), "updated_at": data.get("updated_at", ""),
                        "labels": [l.get("name", "") for l in data.get("labels", [])],
                        "state": data.get("state", "").upper()}
            except Exception: pass
        return {}

    def _api(self, method, path, payload=None):
        token = freely_env_value("GITEE_ACCESS_TOKEN", "GITEE_TOKEN")
        url = f"https://gitee.com/api/v5/repos/{self._repo()}{path}"
        values = dict(payload or {})
        values["access_token"] = token
        data = urllib.parse.urlencode(values).encode("utf-8") if method != "GET" else None
        if method == "GET":
            url = f"{url}?{urllib.parse.urlencode(values)}"
        request = urllib.request.Request(url, data=data, method=method)
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return response.status, json.loads(response.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:300]
            raise RuntimeError(f"Gitee API {exc.code}: {detail}") from exc

    def create_pr(self, branch, base, title, body):
        try:
            _, result = self._api(
                "POST",
                "/pulls",
                {"head": branch, "base": base, "title": title, "body": body},
            )
            return {
                "status": "created",
                "number": str(result.get("number", "")),
                "url": result.get("html_url", ""),
            }
        except Exception as exc:
            return {"status": "error", "error": str(exc)[:300]}

    def ensure_pr(self, branch, base, title, body):
        try:
            _, pulls = self._api("GET", "/pulls", {"state": "open", "per_page": "100"})
            owner = self._repo().split("/", 1)[0]
            matches = [
                pull for pull in pulls
                if pull.get("base", {}).get("ref") == base
                and pull.get("head", {}).get("ref") == branch
                and pull.get("head", {}).get("user", {}).get("login", owner) == owner
            ]
            if not matches:
                return self.create_pr(branch, base, title, body)
            existing = matches[0]
            number = str(existing.get("number", ""))
            changed = existing.get("title", "") != title or existing.get("body", "") != body
            if changed:
                self._api("PATCH", f"/pulls/{number}", {"title": title, "body": body})
            return {
                "status": "updated" if changed else "reused",
                "number": number,
                "url": existing.get("html_url", ""),
            }
        except Exception as exc:
            return {"status": "error", "error": str(exc)[:300]}

    def merge_pr(self, pr_number):
        return {"status": "skipped", "error": "gitee PR merge via API not yet implemented"}
    def close_pr(self, pr_number):
        return {"status": "skipped", "error": "gitee PR close via API not yet implemented"}

    def get_assignees(self, issue_number):
        try:
            r = self._run("get", str(issue_number))
            if r.returncode != 0: return []
            issue = json.loads(r.stdout)
            a = (issue or {}).get("assignee") or {}
            login = (a or {}).get("login", "")
            return [login] if login else []
        except Exception:
            return []

    def set_assignee(self, issue_number, login):
        try:
            r = self._run("update", str(issue_number), "--assignee", login)
            return (r.returncode == 0, f"Failed on Gitee: {r.stderr.strip()}" if r.returncode else f"Assigned {login} to Gitee #{issue_number}")
        except Exception as e:
            return False, f"Failed on Gitee: {e}"

    def list_open_issues(self):
        try:
            r = self._run("list", "--state", "open", "--per-page", "50")
            if r.returncode == 0 and r.stdout.strip():
                return {str(i.get("number", i.get("id", ""))): i.get("state", "OPEN") for i in json.loads(r.stdout)}
        except Exception: pass
        return {}

# ══════════════════════════════════════════════
# REGISTRATION — new platform? add ONE line here.
# ══════════════════════════════════════════════

register(GitHubHandler())
register(GiteeHandler())
# register(GitLabHandler())   ← example: new platform goes here

# ══════════════════════════════════════════════
# Public API — iterates registry, zero platform hardcoding
# ══════════════════════════════════════════════

def available_platforms() -> list[str]:
    return [h.name for h in _handlers()]

def configured_platforms() -> list[str]:
    configured = os.environ.get("FREELY_REPO_PLATFORMS", "").strip()
    if not configured:
        project = os.environ.get("FREELY_PROJECT_ROOT", "").strip()
        if not project:
            resolved = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
            )
            project = resolved.stdout.strip() if resolved.returncode == 0 else os.getcwd()
        configured = str(read_config(project).get("FREELY_REPO_PLATFORMS", "")).strip()
    return list(dict.fromkeys(p.strip() for p in configured.split(",") if p.strip()))

def create_issue(local_id: str, title: str, body: str) -> dict[str, dict]:
    results = {}
    for platform in configured_platforms():
        handler = _handler_for(platform)
        results[platform] = (
            _safe(handler.create_issue, title, body)
            if handler
            else {"status": "error", "error": f"unsupported platform: {platform}"}
        )
    return results

def close_issue(local_id: str, platform_ids: dict = None) -> dict[str, dict]:
    results = {}
    for platform in configured_platforms():
        h = _handler_for(platform)
        if not h:
            results[platform] = {"status": "error", "error": f"unsupported platform: {platform}"}
            continue
        pid = (platform_ids or {}).get(platform, {})
        issue_id = pid.get('issue_id', '') if isinstance(pid, dict) else str(pid or '')
        if not issue_id:
            results[platform] = {'status': 'error', 'error': f'no issue_id for {platform}'}
            continue
        results[platform] = _safe(h.close_issue, issue_id)
    return results

def add_comment(local_id: str, platform_ids: dict = None, comment_body: str = "") -> dict[str, dict]:
    results = {}
    for h in _handlers():
        pid = (platform_ids or {}).get(h.name, {})
        issue_id = pid.get('issue_id', '') if isinstance(pid, dict) else str(pid or '')
        if not issue_id:
            results[h.name] = {'status': 'skipped', 'error': f'no issue_id for {h.name}'}
            continue
        try:
            state = h.get_issue_state(issue_id)
            if state and state.lower() == "closed":
                results[h.name] = {"status": "blocked", "error": f"Issue #{issue_id} is CLOSED on {h.name}."}
                continue
            results[h.name] = _safe(h.add_comment, issue_id, comment_body)
        except Exception as e:
            results[h.name] = {"status": "error", "error": str(e)[:200]}
    return results

def update_issue(local_id: str, platform_ids: dict, title: str = "", body: str = "") -> dict[str, dict]:
    results = {}
    for platform in configured_platforms():
        handler = _handler_for(platform)
        if not handler:
            results[platform] = {"status": "error", "error": f"unsupported platform: {platform}"}
            continue
        reference = (platform_ids or {}).get(platform, {})
        issue_id = reference.get("issue_id", "") if isinstance(reference, dict) else str(reference or "")
        if not issue_id:
            results[platform] = {"status": "error", "error": f"no issue_id for {platform}"}
            continue
        results[platform] = _safe(handler.update_issue, issue_id, title, body)
    return results

def search_raw_issue(raw_key: str) -> dict[str, dict]:
    results = {}
    for h in _handlers():
        info = _safe(h.search_raw_issue, raw_key)
        if info and isinstance(info, dict):
            results[h.name] = info
    return results

def fetch_issue(platform: str, issue_number: str) -> dict:
    h = _handler_for(platform)
    return h.fetch_issue(issue_number) if h else {}

def fetch_issue_state(platform: str, issue_number: str) -> Optional[str]:
    h = _handler_for(platform)
    return h.get_issue_state(issue_number) if h else None

def list_open_issues(platforms: list[str] = None) -> dict[str, str]:
    result = {}
    targets = [h for h in _handlers() if platforms is None or h.name in platforms]
    for h in targets:
        result.update(_safe(h.list_open_issues) or {})
    return result

def get_assignees(platform: str, issue_number: str) -> list[str]:
    h = _handler_for(platform)
    return h.get_assignees(issue_number) if h else []

def set_assignee(platform: str, issue_number: str, login: str) -> tuple[bool, str]:
    h = _handler_for(platform)
    return h.set_assignee(issue_number, login) if h else (False, f"Unknown platform: {platform}")

def check_and_claim_assignee(platform: str, issue_number: str, my_login: str) -> tuple[bool, str]:
    current = get_assignees(platform, issue_number)
    if current:
        others = [a for a in current if a != my_login]
        if others:
            return False, f"Issue #{issue_number} on {platform} already assigned to {', '.join(others)}"
        return True, f"Already assigned to {my_login}"
    return set_assignee(platform, issue_number, my_login)

# ── PR ──

def create_pr(branch: str, base: str = "develop", title: str = "", body: str = "") -> dict:
    return {h.name: _safe(h.create_pr, branch, base, title, body) for h in _handlers()}


def guarded_pr_update(
    branch: str, base: str = "develop", title: str = "", body: str = ""
) -> dict:
    from pr_lifecycle import aggregate_results, classify_branch, plan_platform_updates

    platforms = configured_platforms()
    local = subprocess.run(
        ["git", "rev-parse", branch], capture_output=True, text=True
    )
    if local.returncode != 0:
        return {"success": False, "error": local.stderr.strip()[:300], "platforms": {}}
    local_head = local.stdout.strip()
    observations = {}

    def is_ancestor(left, right):
        return subprocess.run(
            ["git", "merge-base", "--is-ancestor", left, right],
            capture_output=True,
        ).returncode == 0

    for platform in platforms:
        handler = _handler_for(platform)
        if not handler:
            observations[platform] = {"branch_state": "unsupported"}
            continue
        try:
            remote_head = handler.fetch_branch_head(branch)
            observations[platform] = {
                "branch_state": classify_branch(local_head, remote_head, is_ancestor),
                "local_head": local_head,
                "remote_head": remote_head or "",
                "remote": handler.remote_name(),
            }
        except Exception as exc:
            observations[platform] = {
                "branch_state": "error",
                "error": str(exc)[:300],
            }

    plan = plan_platform_updates(
        configured_platforms=platforms, observations=observations
    )
    if not plan["safe_to_execute"]:
        return {
            "success": False,
            "stage": "plan",
            "plan": plan,
            "recovery": "同步本地分支与对应平台远端后重试；禁止 force push 或原始 push 绕过。",
        }

    results = {}
    for item in plan["actions"]:
        platform = item["platform"]
        handler = _handler_for(platform)
        result = dict(observations[platform])
        if item["action"] == "push_then_ensure_pr":
            pushed = handler.push_branch(branch)
            if pushed.get("status") != "pushed":
                result.update({"branch_state": "error", "pr_state": "error", "push": pushed})
                results[platform] = result
                continue
            try:
                remote_head = handler.fetch_branch_head(branch)
            except Exception as exc:
                result.update({"branch_state": "error", "pr_state": "error", "error": str(exc)[:300]})
                results[platform] = result
                continue
            result["branch_state"] = classify_branch(local_head, remote_head, is_ancestor)
            result["remote_head"] = remote_head or ""
            result["push"] = pushed
        pr = _safe(handler.ensure_pr, branch, base, title, body)
        result["pr_state"] = pr.get("status", "error")
        result["pr"] = pr
        results[platform] = result

    aggregate = aggregate_results(platforms, results)
    aggregate["stage"] = "complete"
    return aggregate

def merge_pr(platform: str, pr_number: str) -> dict:
    h = _handler_for(platform)
    return h.merge_pr(pr_number) if h else {"status": "error", "error": f"unknown: {platform}"}

def close_pr(platform: str, pr_number: str) -> dict:
    h = _handler_for(platform)
    return h.close_pr(pr_number) if h else {"status": "error", "error": f"unknown: {platform}"}

# ── Discussion ──

def create_discussion(session_id: str, title: str, body: str = "") -> dict[str, dict]:
    results = {}
    for h in _handlers():
        if h.name != "github":
            results[h.name] = {"status": "skipped", "reason": "平台不支持 Discussions"}
            continue
        try:
            repo = h.detect_repo()
            owner, name = repo.split("/") if "/" in repo else ("", "")
            gh_id = subprocess.run(["gh", "api", f"repos/{repo}", "--jq", ".node_id"],
                                   capture_output=True, text=True).stdout.strip()
            subprocess.run(["gh", "api", "graphql", "-f",
                f"query={{repository(owner:\"{owner}\",name:\"{name}\")"
                f"{{createDiscussion(input:{{repositoryId:\"{gh_id}\","
                f"categoryId:\"DIC_kwDOORxFVs4ClJqg\",title:\"{title}\","
                f"body:\"{body}\"}}){{discussion{{id number}}}}}}}}"],
                capture_output=True, text=True)
            results[h.name] = {"status": "created"}
        except Exception as e:
            results[h.name] = {"status": "error", "error": str(e)[:200]}
    return results

def close_discussion(session_id: str, platform_ids: dict) -> dict[str, dict]:
    results = {}
    for h in _handlers():
        if h.name != "github": continue
        info = platform_ids.get(h.name, {})
        disc_id = info.get("discussion_id", "") if isinstance(info, dict) else info
        if disc_id: results[h.name] = {"status": "closed"}
    return results

# ── Comment via local issue (multi-platform) ──

def _comment_via_local_issue(local_id: str, comment_body: str) -> dict[str, dict]:
    raw_key = local_id[4:] if local_id.startswith("raw-") else local_id
    project_root = Path(os.environ.get("FREELY_PROJECT_ROOT", os.getcwd()))
    issue_file = project_root / "docs" / "B1-docs" / f"raw-{raw_key}" / "issue.md"
    platform_ids = {}
    if issue_file.exists():
        text = issue_file.read_text(encoding="utf-8")
        for h in _handlers():
            m = re.search(rf"{h.name}:\s*\n\s*issue_id:\s*'?([^'\n]+)'?", text)
            if m: platform_ids[h.name] = m.group(1)
    for h in _handlers():
        if h.name not in platform_ids or not platform_ids.get(h.name):
            r = search_raw_issue(raw_key)
            if h.name in r: platform_ids[h.name] = r[h.name].get("issue_number", "")
    if not platform_ids: return {"error": "no platform issue found for " + local_id}
    results = {}
    for h in _handlers():
        num = platform_ids.get(h.name, "")
        if not num or num == "?":
            results[h.name] = {"status": "error", "error": f"no issue_id for {h.name}"}
            continue
        results[h.name] = _safe(h.add_comment, str(num), comment_body)
    return results

# ── Issue state resolution ──

def _resolve_issue_state(local_id: str) -> str:
    raw_key = local_id[4:] if local_id.startswith("raw-") else local_id
    project_root = Path(os.environ.get("FREELY_PROJECT_ROOT", os.getcwd()))
    issue_file = project_root / "docs" / "B1-docs" / f"raw-{raw_key}" / "issue.md"
    platform_ids = {}
    if issue_file.exists():
        text = issue_file.read_text(encoding="utf-8")
        for h in _handlers():
            m = re.search(rf"{h.name}:\s*\n\s*issue_id:\s*'?([^'\n]+)'?", text)
            if m: platform_ids[h.name] = m.group(1)
    if not platform_ids:
        for plat, info in search_raw_issue(raw_key).items():
            platform_ids[plat] = info.get("issue_number", "")
    if not platform_ids: return "unknown"
    for plat, num in platform_ids.items():
        if num and (h := _handler_for(plat)):
            state = h.get_issue_state(str(num))
            if state and state.lower() not in ("closed",): return "open"
    return "closed"

# ── pull_raw_issue ──

def pull_raw_issue(raw_key: str, target_dir: Path) -> Optional[dict]:
    my_login = os.environ.get("GIT_AUTHOR_NAME", "") or os.environ.get("USER", "unknown")
    for plat, info in search_raw_issue(raw_key).items():
        ok, msg = check_and_claim_assignee(plat, info["issue_number"], my_login)
        print(f"[assignee] {plat}: {msg}", file=sys.stderr)
        if not ok and "already assigned to" in msg.lower():
            print(f"FATAL: {msg}", file=sys.stderr); return None
        if not ok:
            print(f"WARNING: Cannot claim assignee on {plat}, continuing anyway.", file=sys.stderr)

    results = search_raw_issue(raw_key)
    if not results: return None
    platform = "github" if "github" in results else next(iter(results))
    info = results[platform]; issue_number = info["issue_number"]
    details = fetch_issue(platform, issue_number)
    if not details: return None

    title = info.get("title", "")
    if not (f"raw-{raw_key}" in title or f"RAW-{raw_key}" in title):
        created_at = details.get("created_at", "")
        if (sk := _created_at_to_key(created_at)) and sk != raw_key:
            _update_issue_title(platform, issue_number, title.replace(f"raw-{raw_key}", f"raw-{sk}"))
            raw_key = sk; target_dir = target_dir.parent / f"raw-{raw_key}"

    target_dir.mkdir(parents=True, exist_ok=True)
    platform_ids = {p: {"issue_id": i["issue_number"], "url": i.get("url", ""), "synced_at": ""}
                    for p, i in results.items()}
    phase = "proposed"
    for label in details.get("labels", []):
        if label.startswith("phase/"): phase = label.replace("phase/", ""); break

    import yaml
    yaml.SafeLoader.yaml_implicit_resolvers.pop('tag:yaml.org,2002:timestamp', None)
    body = details.get("body", "")
    payload = {}
    if body.startswith("---"):
        body_parts = body.split("---", 2)
        if len(body_parts) >= 3:
            payload = yaml.safe_load(body_parts[1]) or {}
            body = body_parts[2].strip()

    if str(payload.get("schema_version", "")) == "1":
        lifecycle_dir = _SCRIPTS_DIR / "lifecycle"
        sys.path.insert(0, str(lifecycle_dir))
        from raw_metadata_contract import RAW_METADATA_FIELDS, validate
        fm = {key: payload.get(key) for key in RAW_METADATA_FIELDS}
        fm["local_id"] = f"raw-{raw_key}"
        fm["platform_ids"] = platform_ids
        fm["primary_platform"] = platform
        fm["phase_state"] = phase
        fm["updated_at"] = details.get("updated_at", "") or fm["updated_at"]
        validate(fm, require_canonical_file=False)
    else:
        fm = {"local_id": f"raw-{raw_key}", "kind": "raw", "phase_state": phase,
              "platform_ids": platform_ids, "primary_platform": platform,
              "canonical_issue_path": "", "last_synced_comment_at": {}, "hash": "",
              "created_at": details.get("created_at", ""), "updated_at": details.get("updated_at", ""),
              "intake_id": "", "author": "platform", "channel": platform, "session_refs": []}
    fm_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
    (target_dir / "issue.md").write_text(f"---\n{fm_str}\n---\n\n{body}\n", encoding="utf-8")
    return {"path": str(target_dir / "issue.md"), "local_id": f"raw-{raw_key}",
            "platform": platform, "issue_number": issue_number, "platform_ids": platform_ids}

def _created_at_to_key(created_at: str) -> Optional[str]:
    try:
        from datetime import datetime, timezone
        return datetime.fromisoformat(created_at.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M%SZ")
    except Exception: return None

def _update_issue_title(platform: str, issue_number: str, new_title: str) -> bool:
    if h := _handler_for(platform):
        return h.update_issue(issue_number, title=new_title).get("status") == "updated"
    return False

def _safe(fn, *args):
    try: return fn(*args)
    except Exception as e: return {"status": "error", "error": str(e)[:200]}

# Legacy helpers
def _gh(*args, check=True):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)

def _gh_repo():
    for h in _handlers():
        if h.name == "github": return h.detect_repo()
    return ""

def _gitee_repo():
    for h in _handlers():
        if h.name == "gitee": return h.detect_repo()
    return ""

# ══════════════════════════════════════════════
# CLI (unchanged interface)
# ══════════════════════════════════════════════

if __name__ == "__main__":
    a = sys.argv
    if len(a) > 1 and a[1] == "search":
        print(json.dumps(search_raw_issue(a[2]) if len(a) > 2 else {}, indent=2))
    elif len(a) > 1 and a[1] == "fetch":
        print(json.dumps(fetch_issue(a[2], a[3]), indent=2))
    elif len(a) > 1 and a[1] == "close-multi":
        platform_ids = json.loads(a[2]) if len(a) > 2 else {}
        result = close_issue("", platform_ids)
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if result and all(item.get("status") == "closed" for item in result.values()) else 1)
    elif len(a) > 1 and a[1] == "close":
        print(json.dumps(close_issue("", a[3]), indent=2))
    elif len(a) > 1 and a[1] == "pull":
        raw_key = a[2]; target = Path(a[3]) if len(a) > 3 else Path(f"docs/B1-docs/raw-{raw_key}")
        print(json.dumps(pull_raw_issue(raw_key, target), indent=2, default=str))
    elif len(a) > 1 and a[1] == "create-pr":
        print(json.dumps(create_pr(a[2], a[3] if len(a) > 3 else "develop",
                                   a[4] if len(a) > 4 else "", a[5] if len(a) > 5 else ""), indent=2))
    elif len(a) > 1 and a[1] == "guarded-pr-update":
        result = guarded_pr_update(
            a[2], a[3] if len(a) > 3 else "develop",
            a[4] if len(a) > 4 else "", a[5] if len(a) > 5 else "",
        )
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if result.get("success") else 1)
    elif len(a) > 1 and a[1] == "merge-pr":
        print(json.dumps(merge_pr(a[2], a[3]), indent=2))
    elif len(a) > 1 and a[1] == "close-pr":
        print(json.dumps(close_pr(a[2], a[3]), indent=2))
    elif len(a) > 1 and a[1] == "create-issue":
        result = create_issue(a[2], a[3], a[4] if len(a) > 4 else "")
        print(json.dumps(result, indent=2))
        raise SystemExit(
            0 if result and all(item.get("status") == "created" for item in result.values()) else 1
        )
    elif len(a) > 1 and a[1] == "get-issue-state":
        print(_resolve_issue_state(a[2]) if len(a) > 2 else "unknown")
    elif len(a) > 1 and a[1] == "comment":
        print(json.dumps(_comment_via_local_issue(a[2], a[3] if len(a) > 3 else ""), indent=2))
    elif len(a) > 1 and a[1] == "update-issue":
        result = update_issue(
            a[2] if len(a) > 2 else "",
            json.loads(a[3]) if len(a) > 3 else {},
            a[4] if len(a) > 4 else "",
            a[5] if len(a) > 5 else "",
        )
        print(json.dumps(result, indent=2))
        raise SystemExit(
            0 if result and all(item.get("status") == "updated" for item in result.values()) else 1
        )
    elif len(a) > 1 and a[1] == "create-discussion":
        print(json.dumps(create_discussion(a[2], a[3], a[4] if len(a) > 4 else ""), indent=2))
    elif len(a) > 1 and a[1] == "close-discussion":
        print(json.dumps(close_discussion(a[2], json.loads(a[3]) if len(a) > 3 else {}), indent=2))
    else:
        print(f"Available: {available_platforms()}")
        for h in _handlers():
            print(f"  {h.name}: repo={h.detect_repo() or '(not detected)'}")
