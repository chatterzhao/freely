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
import concurrent.futures
import json, os, random, re, subprocess, sys, time
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

_ADAPTER_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _ADAPTER_DIR.parent
_RUNTIME_DIR = _SCRIPTS_DIR / "runtime"
# Single source of truth for git transport timeouts (#4250). A half-open
# network used to hang `git fetch` indefinitely and stall the whole guarded
# command for minutes with no diagnostic. Keep this in one place; do not
# sprinkle literals across the three git calls in fetch_branch_head().
GIT_FETCH_TIMEOUT_SECS = 30
sys.path.insert(0, str(_ADAPTER_DIR))
sys.path.insert(0, str(_RUNTIME_DIR))
from freely_user_env import value as freely_env_value
from freely_config import read_config
from raw_title_contract import (canonical_raw_title, find_local_heading,
                               is_canonical_raw_title, local_heading_title)

# ══════════════════════════════════════════════
# Abstract PlatformHandler — new platform? subclass this.
# ══════════════════════════════════════════════

class PlatformHandler(ABC):
    # Read-channel health for the most recent list_open_issue_records() call.
    # A read FAILURE must never be reported as a clean empty list; handlers set
    # ok=False / error / partial=True so the aggregator can emit a degraded
    # marker instead of dropping the whole platform silently.
    read_health: dict = {"ok": True, "error": "", "partial": False}

    @property
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def detect(self) -> bool: ...
    def detect_repo(self) -> str: return ""
    @abstractmethod
    def create_issue(self, title: str, body: str, labels: str = "") -> dict: ...
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

        def run_git(args: list[str], *, check: bool = False):
            try:
                return subprocess.run(
                    args, capture_output=True, text=True,
                    timeout=GIT_FETCH_TIMEOUT_SECS, check=check,
                )
            except subprocess.TimeoutExpired as exc:
                # Normalise to an environment error that names the platform
                # and the remote, so the plan can show a real cause instead of
                # a bare "branch_state: error" (#4250).
                raise RuntimeError(
                    f"{self.name}: `{' '.join(args[:3])}` timed out after "
                    f"{GIT_FETCH_TIMEOUT_SECS}s (remote={remote}, branch={branch}); "
                    f"platform is unavailable"
                ) from exc

        fetched = run_git(["git", "fetch", remote, f"+refs/heads/{branch}:{ref}"])
        if fetched.returncode != 0:
            probe = run_git(["git", "ls-remote", "--heads", remote, branch])
            if probe.returncode == 0 and not probe.stdout.strip():
                return None
            raise RuntimeError((fetched.stderr or probe.stderr).strip()[:300])
        resolved = run_git(["git", "rev-parse", ref], check=True)
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
    def list_open_issue_records(self) -> dict[str, dict]: return {}
    def list_issue_comments(self, issue_number: str) -> list[dict]: return []
    def list_pr_reviews(self, pr_number: str) -> list[dict]: return []
    def list_pr_review_comments(self, pr_number: str) -> list[dict]: return []
    def list_ci_checks(self, pr_number: str) -> list[dict]: return []

# ══════════════════════════════════════════════
# Registry
# ══════════════════════════════════════════════

_registry: list[PlatformHandler] = []

def register(handler: PlatformHandler):
    _registry.append(handler)

# Successful probe results are cached for the life of the process: detection is a
# network read (e.g. `gh repo view`), and one PR flow asks for the same handler
# several times.  Failures are never cached so a later call can recover.
_HANDLER_PROBE_CACHE: dict[str, PlatformHandler] = {}

# Why the last probe of a platform failed. "not installed" / "not authenticated" /
# "timed out" / "no repo permission" are four different operator actions; folding
# them into one False is what made a missing `gh` binary look like an
# unsupported platform (#4149).
_HANDLER_PROBE_ERRORS: dict[str, str] = {}


def _probe_failure_reason(platform: str) -> str:
    return _HANDLER_PROBE_ERRORS.get(platform, "unavailable (probe did not run)")


def _probe_handler(platform: str) -> Optional[PlatformHandler]:
    cached = _HANDLER_PROBE_CACHE.get(platform)
    if cached is not None:
        return cached
    for handler in _registry:
        if handler.name != platform:
            continue
        reason = ""
        if hasattr(handler, "detect_reason"):
            probe = {"ok": False, "reason": ""}

            def _do_probe():
                ok_now, why = handler.detect_reason()
                probe["ok"], probe["reason"] = ok_now, why
                return True if ok_now else None

            value, _error = _retry_read(_do_probe)
            ok, reason = bool(value), probe["reason"]
        else:  # pragma: no cover - third-party handler without detect_reason
            value, _error = _retry_read(lambda: True if handler.detect() else None)
            ok = bool(value)
            if not ok:
                reason = "unavailable"
        if ok:
            _HANDLER_PROBE_CACHE[platform] = handler
            _HANDLER_PROBE_ERRORS.pop(platform, None)
            return handler
        _HANDLER_PROBE_ERRORS[platform] = reason or "unavailable"
        return None
    _HANDLER_PROBE_ERRORS[platform] = "not a registered platform"
    return None


def _handlers() -> list[PlatformHandler]:
    return [h for h in _registry if _probe_handler(h.name) is h]


def _handler_for(platform: str) -> Optional[PlatformHandler]:
    return _probe_handler(platform)


def _ensure_handler(platform: str):
    """Resolve a handler for an execution step, failing closed with a receipt."""
    handler = _handler_for(platform)
    if handler is None:
        return None, {
            "status": "error",
            "stage": "execute",
            "error": f"platform handler unavailable: {platform} ({_probe_failure_reason(platform)})",
        }
    return handler, None

# ══════════════════════════════════════════════
# GitHub Handler
# ══════════════════════════════════════════════

class GitHubHandler(PlatformHandler):
    name = "github"

    def detect(self) -> bool:
        return self.detect_reason()[0]

    def detect_reason(self) -> tuple[bool, str]:
        """Probe `gh` and say WHY it is unusable, not just that it is."""
        try:
            r = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner"],
                               capture_output=True, text=True, timeout=10)
        except FileNotFoundError:
            return False, "gh not installed (gh: command not found)"
        except subprocess.TimeoutExpired:
            return False, "gh timed out after 10s"
        except Exception as exc:
            return False, f"gh probe failed: {exc.__class__.__name__}"
        if r.returncode != 0:
            detail = ((r.stderr or "") + (r.stdout or "")).strip()
            line = detail.splitlines()[-1][:200] if detail else f"gh exited {r.returncode}"
            if re.search(r"auth|login|credential|token", line, re.IGNORECASE):
                return False, f"gh not authenticated ({line})"
            if re.search(r"timed? ?out|timeout", line, re.IGNORECASE):
                return False, f"gh timed out ({line})"
            if re.search(r"not found|could not resolve|permission|403|404", line, re.IGNORECASE):
                return False, f"gh has no access to the repository ({line})"
            return False, f"gh unavailable ({line})"
        return True, ""

    def detect_repo(self) -> str:
        try:
            r = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner",
                               "-q", ".nameWithOwner"], capture_output=True, text=True, timeout=10)
            return r.stdout.strip()
        except Exception:
            return ""

    def _repo(self) -> str: return self.detect_repo()

    @staticmethod
    def _label_names(labels: str) -> list[str]:
        return [name.strip() for name in labels.split(",") if name.strip()]

    def ensure_github_labels(self, labels: str) -> None:
        """Create labels that `gh issue create --label` refuses to add.

        GitHub does NOT auto-create labels, so a fresh repo (or a new label
        family such as severity/*) makes the entire issue create fail. This is
        called only after such a failure: the healthy path costs zero extra API
        calls, and an already-existing label simply returns a harmless error.
        """
        repo = self._repo()
        for name in self._label_names(labels):
            subprocess.run(
                ["gh", "label", "create", name, "--repo", repo,
                 "--color", "0E8A16", "--description", "Freely issue label"],
                capture_output=True, text=True,
            )

    def create_issue(self, title, body, labels=""):
        args = ["gh", "issue", "create", "--repo", self._repo(), "--title", title, "--body", body]
        if labels:
            args += ["--label", labels]
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0 and labels:
            detail = ((r.stderr or "") + (r.stdout or "")).lower()
            # Only a missing-label failure is recoverable. Auth / permission /
            # network errors must stay visible instead of being masked by a retry.
            if "not found" in detail and "label" in detail:
                self.ensure_github_labels(labels)
                # Retry exactly once after bootstrapping the labels.
                r = subprocess.run(args, capture_output=True, text=True)
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
        if not repo:
            return None
        try:
            matches = {}
            for field in ("title", "body"):
                result = subprocess.run(
                    ["gh", "issue", "list", "--repo", repo, "--state", "all",
                     "--search", f"raw-{raw_key} in:{field}", "--limit", "20",
                     "--json", "number,title,url,body"],
                    capture_output=True, text=True, timeout=15,
                )
                if result.returncode != 0 or not result.stdout.strip():
                    continue
                for issue in json.loads(result.stdout):
                    haystack = str(issue.get(field, "") or "")
                    needle = f"raw-{raw_key}".lower()
                    if needle not in haystack.lower():
                        continue
                    issue_id = str(issue.get("number", "") or "")
                    if issue_id:
                        matches[issue_id] = {
                            "issue_number": issue_id,
                            "title": issue.get("title", ""),
                            "url": issue.get("url", ""),
                        }
            candidates = list(matches.values())
            if len(candidates) == 1:
                return {**candidates[0], "matches": candidates}
            return {"matches": candidates}
        except Exception:
            return None

    def fetch_issue(self, issue_number):
        try:
            r = subprocess.run(["gh", "issue", "view", issue_number, "--repo", self._repo(),
                               "--json", "title,body,createdAt,updatedAt,labels,state,comments"],
                              capture_output=True, text=True, timeout=15)
            if r.returncode == 0 and r.stdout.strip():
                data = json.loads(r.stdout)
                return {"title": data.get("title", ""), "body": data.get("body", ""),
                        "created_at": data.get("createdAt", ""), "updated_at": data.get("updatedAt", ""),
                        "labels": [l["name"] for l in data.get("labels", [])],
                        "comments": [c.get("body", "") for c in data.get("comments", [])],
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

    def _open_issue_records_via_rest(self):
        """Open issues via the REST endpoint.

        `gh issue list --json` goes through GraphQL, which intermittently
        answers 504.  REST is independent and stays available, so it is the
        fallback instead of returning {} (which callers read as "no open
        issues" and misdiagnose platform parity/scan).
        """
        repo = self._repo()
        if not repo:
            self.read_health = {"ok": False, "error": "REST fallback: repo unresolved", "partial": True}
            return {}
        try:
            r = subprocess.run(["gh", "api", "--paginate", "--slurp",
                                f"repos/{repo}/issues?state=open&per_page=100"],
                               capture_output=True, text=True, timeout=30)
            if r.returncode != 0 or not r.stdout.strip():
                self.read_health = {"ok": False, "partial": True,
                                    "error": f"REST fallback failed: {(r.stderr or 'empty response')[:200]}"}
                return {}
            pages = json.loads(r.stdout)
        except Exception as exc:
            self.read_health = {"ok": False, "partial": True,
                                "error": f"REST fallback failed: {str(exc)[:200]}"}
            return {}
        # A valid (possibly empty) REST response means the read succeeded.
        self.read_health = {"ok": True, "error": "", "partial": False}
        records = {}
        page_list = pages if isinstance(pages, list) else [pages]
        for page in page_list:
            if not isinstance(page, list):
                continue
            for issue in page:
                if "pull_request" in issue:
                    continue
                number = str(issue.get("number", ""))
                if not number:
                    continue
                records[number] = {
                    "platform": self.name,
                    "title": issue.get("title", "") or "",
                    "body": issue.get("body", "") or "",
                    "state": (issue.get("state", "open") or "open").upper(),
                }
        return records

    def list_open_issues(self):
        records = self.list_open_issue_records()
        return {number: record.get("state", "OPEN") for number, record in records.items()}

    def list_open_issue_records(self):
        self.read_health = {"ok": True, "error": "", "partial": False}
        repo = self._repo()
        if not repo:
            self.read_health = {"ok": False, "error": "github repo unresolved", "partial": True}
            return {}
        errors: list[str] = []
        for attempt in range(2):
            try:
                r = subprocess.run(["gh", "issue", "list", "--repo", repo, "--state", "open", "--limit", "200",
                                    "--json", "number,title,body,state"], capture_output=True, text=True, timeout=30)
                if r.returncode == 0 and r.stdout.strip():
                    self.read_health = {"ok": True, "error": "", "partial": False}
                    return {str(issue["number"]): {"platform": self.name, "title": issue.get("title", ""),
                                                   "body": issue.get("body", ""),
                                                   "state": issue.get("state", "OPEN")}
                            for issue in json.loads(r.stdout or "[]")}
                errors.append((r.stderr or "empty response")[:180])
            except Exception as exc:
                errors.append(str(exc)[:180])
            if attempt == 0:
                time.sleep(0.3)
        # GraphQL failed twice; the REST fallback is preserved (never removed).
        fallback = self._open_issue_records_via_rest()
        if not self.read_health.get("ok"):
            self.read_health = {"ok": False, "partial": True,
                                "error": ("GraphQL: " + "; ".join(errors) + " | REST: "
                                          + str(self.read_health.get("error", "")))[:400]}
        return fallback

    def _gh_json(self, args: list[str], timeout: int = 30):
        repo = self._repo()
        if not repo:
            return None
        r = subprocess.run(["gh", *args, "--repo", repo], capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0 or not r.stdout.strip():
            return None
        try:
            return json.loads(r.stdout)
        except Exception:
            return None

    def list_issue_comments(self, issue_number: str) -> list[dict]:
        data = self._gh_json(["issue", "view", str(issue_number), "--json", "comments"])
        out = []
        for c in (data or {}).get("comments", []) or []:
            out.append({"id": c.get("id"), "author": c.get("author") or {},
                        "association": c.get("authorAssociation", ""),
                        "body": c.get("body", ""), "created_at": c.get("createdAt", "")})
        return out

    def list_pr_reviews(self, pr_number: str) -> list[dict]:
        data = self._gh_json(["pr", "view", str(pr_number), "--json", "reviews"])
        out = []
        for r in (data or {}).get("reviews", []) or []:
            out.append({"id": r.get("id"), "author": r.get("author") or {},
                        "state": r.get("state", ""), "body": r.get("body", ""),
                        "submitted_at": r.get("submittedAt", ""), "commit": r.get("commit", {})})
        return out

    def list_pr_review_comments(self, pr_number: str) -> list[dict]:
        repo = self._repo()
        if not repo:
            return []
        r = subprocess.run(["gh", "api", f"repos/{repo}/pulls/{pr_number}/comments", "--paginate"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0 or not r.stdout.strip():
            return []
        try:
            rows = json.loads(r.stdout)
        except Exception:
            return []
        return [{"id": c.get("id"), "author": c.get("user") or {}, "body": c.get("body", ""),
                 "path": c.get("path", ""), "line": c.get("line"), "created_at": c.get("created_at", "")}
                for c in rows or []]

    def list_ci_checks(self, pr_number: str) -> list[dict]:
        data = self._gh_json(["pr", "checks", str(pr_number), "--json", "name,state,bucket,link"])
        out = []
        for c in data or []:
            link = c.get("link", "")
            cid = link.rstrip("/").split("/")[-1] if link else c.get("name", "")
            out.append({"id": cid, "name": c.get("name", ""), "state": c.get("state", ""),
                        "conclusion": c.get("state", ""), "link": link})
        return out

# ══════════════════════════════════════════════
# Gitee Handler
# ══════════════════════════════════════════════

class GiteeHandler(PlatformHandler):
    name = "gitee"

    def detect(self) -> bool:
        return self.detect_reason()[0]

    def detect_reason(self) -> tuple[bool, str]:
        if not freely_env_value("GITEE_ACCESS_TOKEN", "GITEE_TOKEN"):
            return False, "gitee token not configured (GITEE_ACCESS_TOKEN / GITEE_TOKEN)"
        repo = self.detect_repo()
        if not repo:
            return False, "gitee repo not detectable from git remotes"
        return True, ""

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

    def create_issue(self, title, body, labels=""):
        args = ["create", "--title", title, "--body", body]
        if labels:
            args += ["--labels", labels]
        r = self._run(*args)
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
        # Gitee has no server-side raw-key search: enumerate every page and
        # match locally.  A single page silently hides older replicas, which
        # breaks identity resolution and platform parity for historical issues.
        needle = f"raw-{raw_key}".lower()
        matches = {}
        page = 1
        while page <= 20:
            r = self._run("list", "--state", "all", "--per-page", "100", "--page", str(page))
            if r.returncode != 0:
                return None
            try:
                issues = json.loads(r.stdout)
            except Exception:
                return None
            if not isinstance(issues, list):
                return None
            for issue in issues:
                title = issue.get("title", "") or ""
                body = issue.get("body", "") or ""
                if needle not in title.lower() and needle not in body.lower():
                    continue
                issue_id = str(issue.get("number", issue.get("id", "")) or "")
                if issue_id:
                    matches[issue_id] = {
                        "issue_number": issue_id,
                        "title": title,
                        "url": issue.get("html_url", issue.get("url", "")),
                    }
            if len(issues) < 100:
                break
            page += 1
        candidates = list(matches.values())
        if len(candidates) == 1:
            return {**candidates[0], "matches": candidates}
        return {"matches": candidates}

    def fetch_issue(self, issue_number):
        r = self._run("get", issue_number)
        if r.returncode == 0 and r.stdout.strip():
            try:
                data = json.loads(r.stdout)
                comments = data.get("comments", [])
                comments = comments if isinstance(comments, list) else []
                return {"title": data.get("title", ""), "body": data.get("body", ""),
                        "created_at": data.get("created_at", ""), "updated_at": data.get("updated_at", ""),
                        "labels": [l.get("name", "") for l in data.get("labels", [])],
                        "comments": [c.get("body", "") for c in comments],
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

    def list_open_issue_records(self):
        self.read_health = {"ok": True, "error": "", "partial": False}
        try:
            r = self._run("list", "--state", "open", "--per-page", "50")
            if r.returncode != 0:
                self.read_health = {"ok": False, "partial": True,
                                    "error": f"gitee CLI list failed: {(r.stderr or 'empty response')[:200]}"}
                return {}
            return {str(issue.get("number", issue.get("id", ""))): {"platform": self.name, "title": issue.get("title", ""), "body": issue.get("body", ""), "state": issue.get("state", "OPEN")} for issue in json.loads(r.stdout or "[]")}
        except Exception as exc:
            self.read_health = {"ok": False, "partial": True,
                                "error": f"gitee CLI list failed: {str(exc)[:200]}"}
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

def _unavailable_error(platform: str) -> str:
    """Diagnostic text for a platform we cannot reach — never a bare 'unsupported'."""
    return f"{platform} unavailable: {_probe_failure_reason(platform)}"


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

def create_issue(local_id: str, title: str, body: str, labels: str = "") -> dict[str, dict]:
    results = {}
    for platform in configured_platforms():
        handler = _handler_for(platform)
        if not handler:
            results[platform] = {"status": "error", "error": _unavailable_error(platform)}
            continue
        # Keep the 2-arg call intact when no labels were supplied: custom
        # handlers and existing integrations must not see a new positional arg.
        results[platform] = (
            _safe(handler.create_issue, title, body, labels)
            if labels else _safe(handler.create_issue, title, body)
        )
    return results

def close_issue(local_id: str, platform_ids: dict = None) -> dict[str, dict]:
    results = {}
    for platform in configured_platforms():
        h = _handler_for(platform)
        if not h:
            results[platform] = {"status": "error", "error": _unavailable_error(platform)}
            continue
        pid = (platform_ids or {}).get(platform, {})
        issue_id = pid.get('issue_id', '') if isinstance(pid, dict) else str(pid or '')
        if not issue_id:
            results[platform] = {'status': 'error', 'error': f'no issue_id for {platform}'}
            continue
        results[platform] = _safe(h.close_issue, issue_id)
    return results


def _issue_id(reference: object) -> str:
    value = reference.get("issue_id", "") if isinstance(reference, dict) else reference
    value = str(value or "").strip()
    return value if value and value != "?" else ""



_RAW_TITLE_IDENTITY = re.compile(r"^\[raw-([0-9]{8}T[0-9]{4,6}Z)\]", re.IGNORECASE)


def _resolve_raw_identity(matches, raw_key: str):
    """Resolve one canonical raw replica identity from search matches.

    Identity is the issue title prefix ``[RAW-<key>]``; a body reference from
    another issue is not an identity declaration.  Prefer a unique
    title-prefix match, keep several genuine identities fail-closed as
    ``ambiguous``, and preserve the historical single-match fallback for
    legacy issues that do not carry the canonical prefix.
    """
    key = str(raw_key or "").strip().lower()
    candidates = [match for match in matches if isinstance(match, dict)]
    prefixed = []
    for match in candidates:
        title = str(match.get("title") or "").strip()
        found = _RAW_TITLE_IDENTITY.match(title)
        if found and found.group(1).lower() == key:
            prefixed.append(match)
    if len(prefixed) == 1:
        return prefixed[0], ""
    if len(prefixed) > 1:
        return None, f"raw key {raw_key} is ambiguous: {len(prefixed)} canonical title matches"
    if len(candidates) == 1:
        return candidates[0], ""
    if not candidates:
        return None, f"raw key {raw_key} not found"
    return None, f"raw key {raw_key} is ambiguous: {len(candidates)} matches"


def _unique_raw_issue(handler: PlatformHandler, raw_key: str) -> tuple[str, str]:
    found = _safe(handler.search_raw_issue, raw_key)
    if not isinstance(found, dict):
        return "", f"raw key {raw_key} not found"
    matches = found.get("matches")
    if matches is not None:
        if not isinstance(matches, list):
            return "", f"raw key {raw_key} not found"
        match, error = _resolve_raw_identity(matches, raw_key)
        if match is None:
            return "", error
        found = match
    issue_id = str(found.get("issue_number", found.get("issue_id", "")) or "").strip()
    if not issue_id or issue_id == "?":
        return "", f"raw key {raw_key} did not resolve uniquely"
    return issue_id, ""


def close_issue_by_raw_key(raw_key: str, platform_ids: dict = None) -> dict[str, dict]:
    """Close all configured copies after completing the raw-key identity mapping.

    `platform_ids` is only a cache.  Resolution happens for every missing cache
    entry before any platform close, preventing a partial lookup from becoming a
    single-platform guess.
    """
    resolved = {}
    failures = {}
    platforms = configured_platforms()
    for platform in platforms:
        handler = _handler_for(platform)
        if not handler:
            failures[platform] = {"status": "error", "error": _unavailable_error(platform)}
            continue
        issue_id, error = _unique_raw_issue(handler, raw_key)
        if error:
            failures[platform] = {"status": "error", "error": error}
            continue
        resolved[platform] = {"issue_id": issue_id}
    if failures:
        return {
            platform: failures.get(
                platform,
                {"status": "blocked", "error": "raw key resolution failed on another configured platform"},
            )
            for platform in platforms
        }
    return close_issue(f"raw-{raw_key}", resolved)

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
            results[platform] = {"status": "error", "error": _unavailable_error(platform)}
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


# ── Bounded, jittered reads ──
#
# A transport failure is not an observation: the platform may be fine and the
# path to it may not.  We retry a few times with jittered backoff before we
# report `unknown`, and we never retry terminal answers (auth / not found),
# because retrying those only adds latency and hides the real cause.

_READ_ATTEMPTS = 3
_READ_BACKOFF = (0.5, 1.5)
_TERMINAL_MARKERS = ("authentication", "bad credentials", "401 unauthorized", "not found", "404")


def _retryable(message: str) -> bool:
    lowered = (message or "").lower()
    return not any(marker in lowered for marker in _TERMINAL_MARKERS)


def _retry_read(operation, attempts: int | None = None):
    """Run one transport read, retrying transient failures. Returns (value, error)."""
    budget = attempts or _READ_ATTEMPTS
    last = ""
    for index in range(budget):
        try:
            value = operation()
        except Exception as exc:  # transport exceptions are not observations
            last = (str(exc) or exc.__class__.__name__)[:200]
        else:
            if value is not None:
                return value, ""
            last = last or "empty response"
        if index + 1 >= budget or not _retryable(last):
            break
        time.sleep(_READ_BACKOFF[min(index, len(_READ_BACKOFF) - 1)] + random.uniform(0, 0.15))
    return None, last or "unreadable"


def _discover_one(platform: str, raw_key: str) -> dict:
    """Read a single platform replica. Uncertainty is `unknown`, never `missing`."""
    handler = _handler_for(platform)
    if handler is None:
        return {"status": "unknown", "reason": "transport_unavailable",
                "error": "configured platform unavailable"}

    found, error = _retry_read(lambda: handler.search_raw_issue(raw_key))
    if not isinstance(found, dict):
        return {"status": "unknown", "reason": "search_unreadable", "error": error or "raw search failed"}
    matches = found.get("matches")
    if not isinstance(matches, list):
        return {"status": "unknown", "reason": "search_unreadable", "error": "raw search returned no match set"}
    issue, identity_error = _resolve_raw_identity(matches, raw_key)
    if issue is None:
        if "not found" in identity_error:
            return {"status": "missing", "reason": "absent", "error": identity_error}
        return {"status": "ambiguous", "reason": "duplicate_matches", "error": identity_error}
    issue_id = str(issue.get("issue_number", issue.get("issue_id", "")) or "")
    if not issue_id:
        return {"status": "unknown", "reason": "fetch_unreadable", "error": "raw replica fetch failed"}
    details, error = _retry_read(lambda: handler.fetch_issue(issue_id))
    if not isinstance(details, dict) or not details:
        return {"status": "unknown", "reason": "fetch_unreadable", "error": error or "raw replica fetch failed"}
    return {
        "status": "ok", "raw_key": f"raw-{raw_key}", "issue_id": issue_id,
        "url": issue.get("url", ""), **details,
    }


def discover_raw_replicas(raw_key: str) -> dict[str, dict]:
    """Read every configured platform once; never convert uncertainty into absence.

    Platforms are read concurrently so one slow path cannot delay the others.
    """
    platforms = configured_platforms()
    if len(platforms) <= 1:
        return {platform: _discover_one(platform, raw_key) for platform in platforms}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(platforms))) as pool:
        futures = {platform: pool.submit(_discover_one, platform, raw_key) for platform in platforms}
        return {platform: futures[platform].result() for platform in platforms}

def fetch_issue_state(platform: str, issue_number: str) -> Optional[str]:
    h = _handler_for(platform)
    return h.get_issue_state(issue_number) if h else None

def list_open_issues(platforms: list[str] = None) -> dict[str, str]:
    result = {}
    targets = [h for h in _handlers() if platforms is None or h.name in platforms]
    for h in targets:
        result.update(_safe(h.list_open_issues) or {})
    return result

def list_open_issue_records(platforms: list[str] = None) -> dict[str, dict]:
    """Merge per-platform OPEN issue records, preserving read-failure signals.

    Healthy path is unchanged: a plain ``{platform:issue_id -> record}`` dict
    (e.g. 57 GitHub + 50 Gitee = 107) with no extra keys. On ANY read failure
    the result additionally carries ``__degraded__`` with the failing platform
    and its error, so the existing consumer in task-lifecycle-scan.py can set
    platform_health=degraded instead of acting on a partial list.
    """
    records: dict[str, dict] = {}
    degraded: list[dict] = []
    targets = [h for h in _handlers() if platforms is None or h.name in platforms]
    for h in targets:
        try:
            result = h.list_open_issue_records() or {}
        except Exception as exc:
            # _safe() used to turn an exception into {'status': 'error', ...},
            # which the old loop then expanded as issue records (TypeError or
            # fabricated entries). Record the failure explicitly instead.
            degraded.append({"platform": h.name, "error": str(exc)[:200]})
            continue
        if not isinstance(result, dict):
            degraded.append({"platform": h.name, "error": "read returned a non-dict"})
            continue
        health = getattr(h, "read_health", None)
        if isinstance(health, dict) and health.get("ok") is False:
            degraded.append({"platform": h.name,
                             "error": str(health.get("error") or "unreadable")[:200]})
        for issue_id, record in result.items():
            if not isinstance(record, dict):
                continue  # never treat an error/status object as an issue
            records[f"{h.name}:{issue_id}"] = {"issue_id": str(issue_id), **record}
    if degraded:
        records["__degraded__"] = {
            "platform": ",".join(item["platform"] for item in degraded),
            "platforms": [item["platform"] for item in degraded],
            "error": "; ".join(f"{item['platform']}: {item['error']}" for item in degraded)[:400],
            "ok": False,
            "partial": True,
        }
    return records

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
    from pr_lifecycle import (aggregate_results, classify_branch,
                              plan_platform_updates, recovery_for_plan)

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
            "recovery": recovery_for_plan(plan),
        }

    results = {}
    for item in plan["actions"]:
        platform = item["platform"]
        result = dict(observations[platform])
        handler, handler_error = _ensure_handler(platform)
        if handler is None:
            result.update({"branch_state": "unsupported", "pr_state": "error", **handler_error})
            results[platform] = result
            continue
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

def severity_from_replicas(readable: dict[str, dict]) -> tuple[Optional[str], list[str]]:
    """Resolve the one authoritative severity from platform labels (#4231).

    `freely feedback --severity` writes the priority into BOTH the raw
    frontmatter and a `severity/Pn` label on every platform. Materialization
    used to drop it, so the local read view fell back to P2 while the platforms
    still showed P0/P1.

    Two different *explicit* values are a hard conflict: guessing one would
    hide a real replica divergence, so the caller must fail closed. A platform
    with no severity label is reported as a warning but does not block — legacy
    and partial replicas legitimately lack it (R16.5 / R59).
    """
    values: dict[str, set[str]] = {}
    for plat, info in readable.items():
        found: set[str] = set()
        for label in info.get("labels") or []:
            name = str(label).strip().lower()
            if name.startswith("severity/"):
                value = name.split("/", 1)[1].upper()
                if value in ("P0", "P1", "P2"):
                    found.add(value)
        values[plat] = found
    distinct: set[str] = set().union(*values.values()) if values else set()
    if len(distinct) > 1:
        raise ValueError(f"severity label conflict across platforms: {values}")
    warnings = [f"{plat}: no severity/* label" for plat, found in values.items() if not found]
    return (next(iter(distinct)) if distinct else None), warnings


def pull_raw_issue(raw_key: str, target_dir: Path,
                   preferred_platform: str = "") -> Optional[dict]:
    """Materialize a raw issue from the first READABLE configured platform.

    A transient failure on one platform is uncertainty, not absence: it must
    not block materialization when another replica is readable. Unreadable
    platforms are returned as ``degraded_platforms`` so the caller can record
    sync debt and use the partial-success exit code. ``preferred_platform``
    pins the read source; an explicitly requested but unreadable platform is
    an error (never a silent fallback).

    The pre-flight raw-reconciliation gate already decides whether an
    unreadable replica is a *fact* that must block; this function only chooses
    a usable read source, so any non-ok replica is treated as degraded here.
    """
    replicas = discover_raw_replicas(raw_key)
    readable = {p: i for p, i in replicas.items() if i.get("status") == "ok"}
    degraded = [p for p, i in replicas.items() if i.get("status") != "ok"]
    if not readable:
        print(f"FATAL: raw-{raw_key} replicas are unresolved: {replicas}", file=sys.stderr)
        return None

    if preferred_platform:
        if preferred_platform not in readable:
            print(f"FATAL: requested platform '{preferred_platform}' is not readable "
                  f"for raw-{raw_key}; configured={list(replicas)}", file=sys.stderr)
            return None
        platform = preferred_platform
    else:
        # dict order == configured_platforms() order, so "first ok" keeps the
        # historical primary when every replica is healthy.
        platform = next(iter(readable))

    my_login = os.environ.get("GIT_AUTHOR_NAME", "") or os.environ.get("USER", "unknown")
    for plat, info in readable.items():
        ok, msg = check_and_claim_assignee(plat, info["issue_id"], my_login)
        print(f"[assignee] {plat}: {msg}", file=sys.stderr)
        if not ok and "already assigned to" in msg.lower():
            print(f"FATAL: {msg}", file=sys.stderr)
            return None
        if not ok:
            print(f"WARNING: Cannot claim assignee on {plat}, continuing anyway.", file=sys.stderr)

    info = readable[platform]
    issue_number = info["issue_id"]
    details = info

    title = info.get("title", "")
    if not (is_canonical_raw_title(title, raw_key)
            or f"raw-{raw_key}" in title
            or f"RAW-{raw_key}" in title):
        # Compatibility branch — KEPT ON PURPOSE. A platform-created or
        # hand-edited title may not declare a canonical identity. Deriving the
        # platform's own key from created_at is a *diagnostic* signal only:
        # the caller-supplied raw_key stays the single source of local truth,
        # so neither raw_key nor target_dir may be rewritten here.
        created_at = details.get("created_at", "")
        if (suggested := _created_at_to_key(created_at)) and suggested != raw_key:
            print(
                f"[compat] raw-{raw_key}: platform created_at suggests raw-{suggested}; "
                "keeping caller key as local identity",
                file=sys.stderr,
            )
        canonical = canonical_raw_title(raw_key, title)
        for plat, replica in readable.items():
            if replica.get("title", "") == canonical:
                continue
            if _update_issue_title(plat, replica["issue_id"], canonical):
                print(f"[title] {plat}: normalized to {canonical}", file=sys.stderr)
            else:
                print(f"[title] WARNING {plat}: failed to normalize title to {canonical}",
                      file=sys.stderr)

    target_dir.mkdir(parents=True, exist_ok=True)
    # Only readable replicas have an issue_id. Writing an entry for an
    # unreadable one would either KeyError or poison platform_ids with a
    # fabricated identity; _fill_platform_ids / issue-sync fill it later.
    platform_ids = {p: {"issue_id": i["issue_id"], "url": i.get("url", ""), "synced_at": ""}
                    for p, i in readable.items()}
    phase = "proposed"
    for label in details.get("labels", []):
        if label.startswith("phase/"): phase = label.replace("phase/", ""); break

    # Priority must survive materialization: platform severity/* labels are the
    # authoritative source. A cross-platform conflict is fatal (never guess).
    severity, severity_warnings = severity_from_replicas(readable)
    for warning in severity_warnings:
        print(f"[severity] raw-{raw_key}: {warning}", file=sys.stderr)
    if severity:
        print(f"[severity] raw-{raw_key}: materialized as {severity}", file=sys.stderr)

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
        if severity:
            fm["severity"] = severity
        validate(fm, require_canonical_file=False)
    else:
        fm = {"local_id": f"raw-{raw_key}", "kind": "raw", "phase_state": phase,
              "platform_ids": platform_ids, "primary_platform": platform,
              "canonical_issue_path": "", "last_synced_comment_at": {}, "hash": "",
              "created_at": details.get("created_at", ""), "updated_at": details.get("updated_at", ""),
              "intake_id": "", "author": "platform", "channel": platform, "session_refs": []}
        if severity:
            fm["severity"] = severity
    fm_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
    # Materialization must carry an H1: raw-reconciliation-gate derives the
    # LOCAL title from the first '# ' line, and _platform_title()/_issue_title()
    # fall back to the same heading. Without it every first PR of a new raw
    # issue is blocked with content_diverged. The H1 is the human part of the
    # canonical platform title (via the shared contract), and is idempotent:
    # a body that already declares a heading keeps exactly that one.
    if find_local_heading(body) is not None:
        rendered_body = body.strip()
    else:
        heading = local_heading_title(raw_key, title)
        rendered_body = f"# {heading}\n\n{body.strip()}" if body.strip() else f"# {heading}"
    (target_dir / "issue.md").write_text(
        f"---\n{fm_str}\n---\n\n{rendered_body}\n", encoding="utf-8"
    )
    return {"path": str(target_dir / "issue.md"), "local_id": f"raw-{raw_key}",
            "platform": platform, "issue_number": issue_number, "platform_ids": platform_ids,
            "degraded_platforms": degraded, "partial": bool(degraded)}

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


def _close_exit_code(results: object) -> int:
    """Per-platform close accounting: 0 all closed, 3 partial, 1 nothing closed.

    `create-issue` already distinguishes these three states; close used to collapse
    "closed half of them" into the same exit code as "closed none", which made
    a retry indistinguishable from a first attempt.
    """
    if not isinstance(results, dict) or not results:
        return 1
    statuses = [
        item.get("status") if isinstance(item, dict) else None
        for item in results.values()
    ]
    closed = [status for status in statuses if status == "closed"]
    if len(closed) == len(statuses):
        return 0
    return 3 if closed else 1

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
    elif len(a) > 1 and a[1] == "discover-raw":
        print(json.dumps(discover_raw_replicas(a[2]) if len(a) > 2 else {}, indent=2))
    elif len(a) > 1 and a[1] == "fetch":
        print(json.dumps(fetch_issue(a[2], a[3]), indent=2))
    elif len(a) > 1 and a[1] == "close-multi":
        platform_ids = json.loads(a[2]) if len(a) > 2 else {}
        result = close_issue("", platform_ids)
        print(json.dumps(result, indent=2))
        raise SystemExit(_close_exit_code(result))
    elif len(a) > 1 and a[1] == "close-raw":
        raw_key = a[2] if len(a) > 2 else ""
        platform_ids = json.loads(a[3]) if len(a) > 3 else {}
        result = close_issue_by_raw_key(raw_key, platform_ids)
        print(json.dumps(result, indent=2))
        raise SystemExit(_close_exit_code(result))
    elif len(a) > 1 and a[1] == "close":
        print(json.dumps(close_issue("", a[3]), indent=2))
    elif len(a) > 1 and a[1] == "pull":
        raw_key = a[2]; target = Path(a[3]) if len(a) > 3 else Path(f"docs/B1-docs/raw-{raw_key}")
        preferred = a[4] if len(a) > 4 else ""
        result = pull_raw_issue(raw_key, target, preferred)
        print(json.dumps(result, indent=2, default=str))
        if result is None:
            raise SystemExit(1)
        if result.get("partial"):
            # Distinct from failure (1): materialization succeeded but at
            # least one configured platform could not be read. The caller
            # records sync debt and continues worktree creation.
            raise SystemExit(3)
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
        result = create_issue(a[2], a[3], a[4] if len(a) > 4 else "", a[5] if len(a) > 5 else "")
        print(json.dumps(result, indent=2))
        # Per-platform accounting: 0 = every configured platform created,
        # 3 = partial (at least one created, at least one failed),
        # 1 = nothing created. A partial success used to surface as a plain
        # failure, which invited a retry that duplicated the created issue.
        created = [p for p, item in (result or {}).items() if item.get("status") == "created"]
        if result and len(created) == len(result):
            raise SystemExit(0)
        raise SystemExit(3 if created else 1)
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
