#!/usr/bin/env python3
# DEPRECATED: replaced by task-lifecycle-scan.py (lifecycle-aware, parent-child model).
# This file is kept for reference. New code should use task-lifecycle-scan.py.
from __future__ import annotations

import argparse
import functools
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from freely_user_env import bootstrap_path_hint as freely_bootstrap_env_path_hint
from freely_user_env import checked_paths_hint as freely_checked_paths_hint
from freely_user_env import default_path_hint as freely_default_env_path_hint
from freely_user_env import path_hint as freely_env_path_hint
from freely_user_env import value as freely_env_value


TERMINAL_PROGRESS_CLOSURE_STATUSES = {
    "merged-and-verified",
    "completed-on-develop",
    "closed",
    "implemented-and-verified",
    "completed-reusable-gate",
    "contract-frozen",
}
TERMINAL_PROGRESS_PHASES = {"completed"}
TERMINAL_CANDIDATE_STATUSES = {"absorbed", "dropped", "completed", "retired"}
FOLLOWTHROUGH_CANDIDATE_STATUSES = {"promoted", "materialized"}
TERMINAL_MILESTONE_STATES = {"completed", "delivered"}
DEFAULT_PROVIDER_TIMEOUT_SECS = 15


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def shell_value(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
        return raw[1:-1]
    return raw


def parse_env_file(path: Path) -> dict:
    values = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue
        key, raw = line.split("=", 1)
        values[key.strip()] = shell_value(raw)
    return values


def parse_simple_markdown_fields(path: Path, *, stop_at_h2: bool = True) -> dict:
    values = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        if stop_at_h2 and line.startswith("## "):
            break
        match = re.match(r"^- ([^:]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        cooked = value.strip().strip("`")
        values[key] = cooked
        normalized = key.strip().lower().replace(" ", "_").replace("-", "_")
        values.setdefault(normalized, cooked)
    return values


def parse_markdown_h3_sections(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^###\s+(.+)$", text, flags=re.MULTILINE)
    sections = []
    for index in range(1, len(parts), 2):
        title = parts[index].strip()
        body = parts[index + 1]
        fields = {}
        for line in body.splitlines():
            match = re.match(r"^- ([^:]+):\s*(.*)$", line)
            if not match:
                continue
            key, value = match.groups()
            cooked = value.strip().strip("`")
            fields[key] = cooked
            normalized = key.strip().lower().replace(" ", "_").replace("-", "_")
            fields.setdefault(normalized, cooked)
        if fields:
            fields["_section_title"] = title
            sections.append(fields)
    return sections


def relative_to_project(project: Path, path: Path) -> str:
    try:
        return str(path.relative_to(project))
    except ValueError:
        return str(path)


@functools.lru_cache(maxsize=None)
def repo_root_for_project(project: str) -> Path | None:
    try:
        output = subprocess.check_output(
            ["git", "-C", project, "rev-parse", "--show-toplevel"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return None
    return Path(output) if output else None


@functools.lru_cache(maxsize=None)
def authoritative_develop_worktree(project: str) -> Path | None:
    repo_root = repo_root_for_project(project)
    if repo_root is None:
        return None
    try:
        current_branch = subprocess.check_output(
            ["git", "-C", str(repo_root), "branch", "--show-current"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        current_branch = ""
    if current_branch == "develop":
        return repo_root

    try:
        output = subprocess.check_output(
            ["git", "-C", str(repo_root), "worktree", "list", "--porcelain"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None

    worktree = None
    for line in output.splitlines():
        if line.startswith("worktree "):
            worktree = Path(line[9:].strip())
        elif line.startswith("branch refs/heads/") and line.strip() == "branch refs/heads/develop":
            return worktree
    return None


@functools.lru_cache(maxsize=None)
def branch_is_merged_into_authoritative_develop(project: str, branch: str) -> bool:
    if not branch:
        return False
    develop_worktree = authoritative_develop_worktree(project)
    if develop_worktree is None:
        return False
    try:
        branch_head = subprocess.check_output(
            ["git", "-C", str(develop_worktree), "rev-parse", branch],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        develop_head = subprocess.check_output(
            ["git", "-C", str(develop_worktree), "rev-parse", "develop"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return False
    if not branch_head or branch_head == develop_head:
        return False
    try:
        subprocess.check_call(
            ["git", "-C", str(develop_worktree), "merge-base", "--is-ancestor", branch, "develop"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return False
    return True


def worktree_has_runtime_history(worktree_path: Path) -> bool:
    run_dir = worktree_path / ".freely" / "run"
    return any(
        candidate.exists()
        for candidate in (
            run_dir / "workcell-state.env",
            run_dir / "session-state.env",
            run_dir / "manager-worker-launch-state.env",
        )
    )


def progress_item_is_absorbed_merged_lane(project: Path, fields: dict) -> bool:
    branch = fields.get("branch", "")
    worktree_path = fields.get("worktree_path", "")
    if not branch or not worktree_path:
        return False
    worktree = Path(worktree_path)
    if not worktree.is_dir():
        return False
    if not worktree_has_runtime_history(worktree):
        return False
    return branch_is_merged_into_authoritative_develop(str(project), branch)


def restart_point_for_interruption(classification: str) -> str:
    mapping = {
        "control": "runtime_supervision",
        "continuation": "continuation",
        "verification": "verification",
        "cleanup": "cleanup",
    }
    return mapping.get(classification or "", "pre_brainstorm")


def scan_intake(project: Path) -> list[dict]:
    # DEPRECATED: .freely/intake/ scan is no longer called from build_payload.
    # Replaced by scan_raw_issues() and scan_linked_issues().
    # This function remains for historical data access only.
    items = []
    intake_root = project / ".freely" / "intake"
    if not intake_root.is_dir():
        return items
    for item_dir in sorted([p for p in intake_root.iterdir() if p.is_dir()], reverse=True):
        meta = parse_env_file(item_dir / "meta.env")
        status = meta.get("STATUS", "")
        if status in {"absorbed", "dropped", "delegated"}:
            continue
        message = ""
        message_file = item_dir / "message.txt"
        if message_file.is_file():
            content = message_file.read_text(encoding="utf-8")
            message = content.splitlines()[0] if content else ""
        classification = meta.get("CLASSIFICATION", "")
        items.append(
            {
                "source_family": "human interruption",
                "source_type": "intake_item",
                "source_ref": f"intake://{meta.get('INTAKE_ID', item_dir.name)}",
                "artifact_path": relative_to_project(project, item_dir),
                "status_markers": {
                    "status": status or "new",
                    "classification": classification or "unclassified",
                    "reaction": meta.get("REACTION", "") or "pending",
                    "claimed_by": meta.get("CLAIMED_BY", "") or "unclaimed",
                    "linked_artifact": meta.get("LINKED_ARTIFACT", "") or "pending://unclassified",
                },
                "needs_action": True,
                "restart_point": restart_point_for_interruption(classification),
                "owner_hint": "manager",
                "next_action": "Classify the interruption and either absorb it into an existing owner or route it into pre-brainstorm.",
                "message_preview": message,
            }
        )
    return items


def scan_raw_issues(project: Path) -> list[dict]:
    """Scan docs/issues/raw-*/ for unprocessed raw issues (new chat→issue model)."""
    items = []
    issues_root = project / "docs" / "issues"
    if not issues_root.is_dir():
        return items
    for entry_dir in sorted([p for p in issues_root.iterdir() if p.is_dir() and p.name.startswith("raw-")]):
        issue_file = entry_dir / "issue.md"
        if not issue_file.is_file():
            continue
        content = issue_file.read_text(encoding="utf-8")
        # Check if already linked to a candidate
        if "canonical_issue_path:" in content:
            canonical = ""
            for line in content.splitlines():
                if line.startswith("canonical_issue_path:"):
                    canonical = line.split('"')[1] if '"' in line else ""
            if canonical and canonical.strip():
                continue  # Already processed through B1
        items.append({
            "source_family": "raw issue",
            "source_type": "raw_issue",
            "source_ref": f"issue://{entry_dir.name}",
            "artifact_path": str(issue_file.relative_to(project)),
            "status_markers": {
                "status": "new",
                "classification": "discovery",
            },
            "needs_action": True,
            "restart_point": "pre_brainstorm",
            "owner_hint": "worker",
            "next_action": "Consume the raw issue into B1_IBM pre-brainstorm and produce a candidate.",
            "message_preview": content.split("\n")[-1][:200] if content.split("\n") else "",
        })
    return items


def scan_linked_issues(project: Path) -> list[dict]:
    """Scan docs/issues/I-*/ for linked issues with new comments that need attention."""
    items = []
    issues_root = project / "docs" / "issues"
    if not issues_root.is_dir():
        return items
    for entry_dir in sorted([p for p in issues_root.iterdir() if p.is_dir() and p.name.startswith("I-")]):
        issue_file = entry_dir / "issue.md"
        if not issue_file.is_file():
            continue
        content = issue_file.read_text(encoding="utf-8")
        # Check for unprocessed comments (### sections without status: resolved)
        comments_section = content.split("## Comments", 1)
        if len(comments_section) < 2:
            continue
        comment_lines = comments_section[1]
        unresolved = 0
        for line in comment_lines.split("\\n"):
            if line.startswith("### comment-") and "status: resolved" not in comment_lines:
                unresolved += 1
        if unresolved == 0:
            continue
        # Check if issue is active
        canonical = ""
        for line in content.splitlines():
            if line.startswith("canonical_issue_path:"):
                canonical = line.split('"')[1] if '"' in line else ""
        items.append({
            "source_family": "linked issue",
            "source_type": "linked_issue_comments",
            "source_ref": f"issue://{entry_dir.name}",
            "artifact_path": str(issue_file.relative_to(project)),
            "status_markers": {
                "status": "active",
                "unresolved_comments": unresolved,
                "canonical_issue_path": canonical,
            },
            "needs_action": unresolved > 0,
            "restart_point": "cleanup",
            "owner_hint": "manager",
            "next_action": f"Review {unresolved} unresolved comment(s) on linked issue {entry_dir.name}.",
            "message_preview": f"{unresolved} unresolved comments",
        })
    return items


def scan_pre_brainstorms(project: Path) -> list[dict]:
    items = []
    root = project / "docs" / "pre-brainstorms"
    if not root.is_dir():
        return items
    for entry in sorted([p for p in root.iterdir() if p.is_dir()]):
        brainstorm = entry / "brainstorms.md"
        if not brainstorm.is_file():
            continue
        candidates = entry / "candidates.md"
        if not candidates.is_file():
            items.append(
                {
                    "source_family": "pre-brainstorm",
                    "source_type": "pre_brainstorm_missing_candidates",
                    "source_ref": relative_to_project(project, brainstorm),
                    "artifact_path": relative_to_project(project, brainstorm),
                    "status_markers": {"brainstorm": "present", "candidates": "missing"},
                    "needs_action": True,
                    "restart_point": "pre_brainstorm",
                    "owner_hint": "manager",
                    "next_action": "Materialize candidates.md so the brainstorm can enter the active candidate queue.",
                }
            )
            continue
        sections = parse_markdown_h3_sections(candidates)
        if not sections:
            continue
        for fields in sections:
            status = fields.get("status") or fields.get("candidate_status") or ""
            promoted_issue_path = fields.get("promoted_issue_path", "")
            milestone = fields.get("milestone", "")
            if status in TERMINAL_CANDIDATE_STATUSES:
                continue
            if status in FOLLOWTHROUGH_CANDIDATE_STATUSES:
                needs_action = (
                    not promoted_issue_path
                    or promoted_issue_path.startswith("pending://")
                    or not milestone
                    or milestone.startswith("pending://")
                )
                if not needs_action:
                    continue
            items.append(
                {
                    "source_family": "pre-brainstorm",
                    "source_type": "candidate_packet",
                    "source_ref": f"{relative_to_project(project, candidates)}#{fields.get('_section_title', 'candidate')}",
                    "artifact_path": relative_to_project(project, candidates),
                    "status_markers": {
                        "candidate_id": fields.get("_section_title", "unknown"),
                        "candidate_status": status or "unknown",
                        "promoted_issue_path": promoted_issue_path or "missing",
                        "milestone": milestone or "missing",
                    },
                    "needs_action": True,
                    "restart_point": "pre_brainstorm",
                    "owner_hint": "manager",
                    "next_action": fields.get("next_action") or "Advance the candidate to a concrete milestone/issue decision or explicitly discard it.",
                }
            )
    return items


def parse_milestone_blocks(project: Path) -> list[dict]:
    path = project / "docs" / "milestones.md"
    if not path.is_file():
        return []
    entries = []
    content = path.read_text(encoding="utf-8")
    parts = re.split(r"^###\s+(.+)$", content, flags=re.MULTILINE)
    for index in range(1, len(parts), 2):
        section = parts[index].strip()
        body = parts[index + 1]
        for paragraph in re.split(r"\n\s*\n", body):
            fields = {}
            for line in paragraph.splitlines():
                match = re.match(r"^- ([A-Za-z0-9_]+):\s*(.*)$", line)
                if match:
                    key, value = match.groups()
                    fields[key] = value.strip().strip("`")
            if not fields:
                continue
            fields["_section"] = section
            entries.append(fields)
    return entries


def scan_milestones(project: Path) -> list[dict]:
    items = []
    for fields in parse_milestone_blocks(project):
        state = fields.get("milestone_state", "")
        phase_state = fields.get("phase_state", "")
        promoted_issue_path = fields.get("promoted_issue_path", "")
        next_action = fields.get("next_action", "")
        is_candidate_mirror = (
            fields.get("_section") == "candidate_issues"
            and promoted_issue_path
            and not promoted_issue_path.startswith("pending://")
            and next_action.lower().startswith("candidate mirror only")
        )
        needs_action = (
            state not in TERMINAL_MILESTONE_STATES
            and phase_state != "completed"
            and not is_candidate_mirror
        )
        if not needs_action:
            continue
        source_ref = fields.get("issue_path") or fields.get("source_candidates") or "milestone://unresolved"
        items.append(
            {
                "source_family": "milestone",
                "source_type": "milestone_queue_item",
                "source_ref": source_ref,
                "artifact_path": "docs/milestones.md",
                "status_markers": {
                    "section": fields.get("_section", "unknown"),
                    "milestone_id": fields.get("milestone_id", "unknown"),
                    "milestone_state": state or "unknown",
                    "phase_state": phase_state or "unknown",
                },
                "needs_action": True,
                "restart_point": "candidate_milestone_intake" if fields.get("_section") == "candidate_issues" else "continuation",
                "owner_hint": fields.get("issue_path") or fields.get("progress_path") or "manager",
                "next_action": next_action or "Resume the unresolved milestone queue item and move it toward issue execution or closeout.",
            }
        )
    return items


def scan_progress(project: Path) -> list[dict]:
    items = []
    progress_root = project / "docs" / "progress"
    if not progress_root.is_dir():
        return items
    for path in sorted(progress_root.rglob("*.md")):
        fields = parse_simple_markdown_fields(path)
        if not fields:
            continue
        phase_state = fields.get("phase_state", "")
        closure_status = fields.get("closure_status", "")
        next_action = fields.get("next_action", "")
        if phase_state in TERMINAL_PROGRESS_PHASES and (
            not next_action or next_action.lower() == "completed"
        ) and (
            not closure_status or closure_status in TERMINAL_PROGRESS_CLOSURE_STATUSES
        ):
            continue
        absorbed_merged_lane = progress_item_is_absorbed_merged_lane(project, fields)
        restart_point = "verification" if phase_state == "in_verification" else "continuation"
        owner_hint = fields.get("issue_path") or "manager"
        if absorbed_merged_lane:
            restart_point = "cleanup"
            owner_hint = "manager"
            next_action = (
                "Finish cleanup/closeout followthrough for the already absorbed merged lane instead "
                "of routing it back into verification execution."
            )
        items.append(
            {
                "source_family": "progress",
                "source_type": "progress_item",
                "source_ref": relative_to_project(project, path),
                "artifact_path": relative_to_project(project, path),
                "status_markers": {
                    "issue_id": fields.get("issue_id", "unknown"),
                    "phase_state": phase_state or "unknown",
                    "runtime_state": fields.get("runtime_state", "unknown"),
                    "closure_status": closure_status or "open",
                    "verification_status": fields.get("verification_status", "unknown"),
                    "lane_state": "absorbed_merged" if absorbed_merged_lane else "active_or_unclassified",
                },
                "needs_action": True,
                "restart_point": restart_point,
                "owner_hint": owner_hint,
                "next_action": next_action or "Resume the active owner or finish its closeout followthrough.",
            }
        )
    return items


def detect_github_repo(project: Path) -> str | None:
    override = os.environ.get("FREELY_TASK_SOURCE_SCAN_GITHUB_REPO") or os.environ.get("GH_REPO")
    if override:
        return override
    try:
        output = subprocess.check_output(
            ["git", "-C", str(project), "remote", "-v"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        url = parts[1]
        match = re.search(r"github\.com[:/]([^/\s]+/[^/\s]+?)(?:\.git)?$", url)
        if match:
            return match.group(1)
    return None


def detect_gitee_repo(project: Path) -> str | None:
    override = os.environ.get("FREELY_TASK_SOURCE_SCAN_GITEE_REPO") or os.environ.get("GITEE_REPO")
    if override:
        return override
    try:
        output = subprocess.check_output(
            ["git", "-C", str(project), "remote", "-v"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        url = parts[1]
        match = re.search(r"gitee[^:/]*[:/]([^/\s]+/[^/\s]+?)(?:\.git)?$", url)
        if match:
            return match.group(1)
    return None


def repo_markdown_files(project: Path) -> list[Path]:
    docs_root = project / "docs"
    if not docs_root.is_dir():
        return []
    return sorted(docs_root.rglob("*.md"))


def linked_paths_for_url(project: Path, url: str, files: list[Path]) -> list[str]:
    linked = []
    for path in files:
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if url in content:
            linked.append(relative_to_project(project, path))
    return linked


def provider_timeout_secs() -> int:
    raw = os.environ.get("FREELY_TASK_SOURCE_SCAN_PROVIDER_TIMEOUT_SECS")
    if not raw:
        return DEFAULT_PROVIDER_TIMEOUT_SECS
    try:
        return int(raw)
    except ValueError:
        return DEFAULT_PROVIDER_TIMEOUT_SECS


def github_provider_hint(provider: dict) -> str | None:
    state = provider.get("support_state")
    repo = provider.get("repo") or "<owner/repo>"
    if state == "unavailable_in_this_repo":
        return (
            "GitHub external issue scan unavailable: add a GitHub remote or set "
            "FREELY_TASK_SOURCE_SCAN_GITHUB_REPO/GH_REPO, then ensure `gh auth login` succeeds."
        )
    if state == "gh_query_timeout":
        return (
            f"GitHub external issue scan timed out for {repo}: verify network access and `gh auth status`, "
            "or raise FREELY_TASK_SOURCE_SCAN_PROVIDER_TIMEOUT_SECS."
        )
    if state == "gh_unavailable_or_query_failed":
        return (
            f"GitHub external issue scan query failed for {repo}: verify `gh auth status` and that "
            "`gh issue list --repo {repo}` succeeds."
        )
    return None


def gitee_provider_hint(provider: dict) -> str | None:
    state = provider.get("support_state")
    repo = provider.get("repo") or "<owner/repo>"
    if state == "gitee_issue_auth_unconfigured":
        return (
            f"Gitee external issue scan for {repo} is available, but writeback/create/close flows still need credentials: "
            "create a personal access token at "
            "https://gitee.com/profile/personal_access_tokens with `issues` scope, then store "
            f"`GITEE_ACCESS_TOKEN=<token>` in `{freely_default_env_path_hint()}`. "
            f"Freely checked: {freely_checked_paths_hint()}. "
            f"If you need a custom credentials path, set `FREELY_ENV_FILE=/abs/path/to/credentials.env` in `{freely_bootstrap_env_path_hint()}`."
        )
    if state == "unavailable_in_this_repo":
        return (
            "Gitee external issue scan unavailable: add a Gitee remote or set "
            "FREELY_TASK_SOURCE_SCAN_GITEE_REPO/GITEE_REPO."
        )
    if state == "gitee_issue_cli_missing":
        return "Gitee external issue scan unavailable: missing local `gitee-issue` CLI wrapper."
    if state == "gitee_issue_query_failed_missing_token":
        return (
            f"Gitee external issue scan needs API access for {repo}: create a personal access token at "
            "https://gitee.com/profile/personal_access_tokens with `issues` scope, then store "
            f"`GITEE_ACCESS_TOKEN=<token>` in `{freely_default_env_path_hint()}`. "
            f"Freely checked: {freely_checked_paths_hint()}. "
            f"If you need a custom credentials path, set `FREELY_ENV_FILE=/abs/path/to/credentials.env` in `{freely_bootstrap_env_path_hint()}`."
        )
    if state == "gitee_issue_query_timeout":
        return (
            f"Gitee external issue scan timed out for {repo}: verify network/API reachability and "
            "that Gitee credentials are configured. If missing, create a personal access token at "
            "https://gitee.com/profile/personal_access_tokens with `issues` scope, then store "
            f"`GITEE_ACCESS_TOKEN=<token>` in `{freely_default_env_path_hint()}`. "
            f"Freely checked: {freely_checked_paths_hint()}. "
            f"Custom path override lives in `{freely_bootstrap_env_path_hint()}` as `FREELY_ENV_FILE=...`. "
            "You can also raise FREELY_TASK_SOURCE_SCAN_PROVIDER_TIMEOUT_SECS."
        )
    if state == "gitee_issue_query_failed":
        return (
            f"Gitee external issue scan query failed for {repo}: verify `GITEE_ACCESS_TOKEN` from the environment or `{freely_env_path_hint()}` "
            f"(checked: {freely_checked_paths_hint()}) and that "
            "`bin/gitee-issue list --repo {repo}` succeeds."
        )
    return None


def scan_external_github(project: Path) -> tuple[list[dict], dict]:
    repo = detect_github_repo(project)
    provider = {
        "family": "external issue",
        "platform": "github",
        "enabled": bool(repo),
        "repo": repo,
        "support_state": "github_first_slice" if repo else "unavailable_in_this_repo",
    }
    provider["availability_hint"] = github_provider_hint(provider)
    if not repo:
        return [], provider
    try:
        raw = subprocess.check_output(
            [
                "gh",
                "issue",
                "list",
                "--repo",
                repo,
                "--state",
                "open",
                "--limit",
                "100",
                "--json",
                "number,title,url,labels,createdAt,updatedAt",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=provider_timeout_secs(),
        )
    except subprocess.TimeoutExpired:
        provider["enabled"] = False
        provider["support_state"] = "gh_query_timeout"
        provider["availability_hint"] = github_provider_hint(provider)
        return [], provider
    except (subprocess.CalledProcessError, FileNotFoundError):
        provider["enabled"] = False
        provider["support_state"] = "gh_unavailable_or_query_failed"
        provider["availability_hint"] = github_provider_hint(provider)
        return [], provider

    issues = json.loads(raw)
    docs_files = repo_markdown_files(project)
    items = []
    for issue in issues:
        labels = [entry.get("name", "") for entry in issue.get("labels", [])]
        linked_paths = linked_paths_for_url(project, issue["url"], docs_files)
        if linked_paths:
            source_type = "github_linked_open_issue"
            restart_point = "cleanup"
            next_action = "Reconcile external closeout/writeback drift for the already-linked source issue."
        else:
            source_type = "github_raw_issue"
            restart_point = "pre_brainstorm"
            next_action = "Consume the raw external source issue into pre-brainstorm without treating GitHub labels as canonical truth."
        items.append(
            {
                "source_family": "external issue",
                "source_type": source_type,
                "source_ref": issue["url"],
                "artifact_path": issue["url"],
                "status_markers": {
                    "platform": "github",
                    "number": issue["number"],
                    "labels": labels,
                    "canonical_linkage": "present" if linked_paths else "missing",
                    "created_at": issue.get("createdAt"),
                    "updated_at": issue.get("updatedAt"),
                },
                "needs_action": True,
                "restart_point": restart_point,
                "owner_hint": linked_paths[0] if linked_paths else "manager",
                "next_action": next_action,
                "title": issue["title"],
                "linked_paths": linked_paths,
            }
        )
    return items, provider


def gitee_issue_cli_path() -> Path:
    return Path(__file__).with_name("gitee-issue.py")


def scan_external_gitee(project: Path) -> tuple[list[dict], dict]:
    repo = detect_gitee_repo(project)
    token_configured = bool(freely_env_value("GITEE_ACCESS_TOKEN", "GITEE_TOKEN"))
    provider = {
        "family": "external issue",
        "platform": "gitee",
        "enabled": bool(repo),
        "repo": repo,
        "token_configured": token_configured,
        "support_state": (
            "gitee_issue_auth_unconfigured"
            if repo and not token_configured
            else "implemented" if repo else "unavailable_in_this_repo"
        ),
    }
    provider["availability_hint"] = gitee_provider_hint(provider)
    if not repo:
        return [], provider
    cli_path = gitee_issue_cli_path()
    if not cli_path.is_file():
        provider["enabled"] = False
        provider["support_state"] = "gitee_issue_cli_missing"
        provider["availability_hint"] = gitee_provider_hint(provider)
        return [], provider
    try:
        raw = subprocess.check_output(
            [
                "python3",
                str(cli_path),
                "--repo",
                repo,
                "list",
                "--state",
                "open",
                "--per-page",
                "100",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
            cwd=str(project),
            timeout=provider_timeout_secs(),
        )
    except subprocess.TimeoutExpired:
        provider["enabled"] = False
        provider["support_state"] = "gitee_issue_query_timeout"
        provider["availability_hint"] = gitee_provider_hint(provider)
        return [], provider
    except subprocess.CalledProcessError:
        provider["enabled"] = False
        provider["support_state"] = (
            "gitee_issue_query_failed_missing_token"
            if not token_configured
            else "gitee_issue_query_failed"
        )
        provider["availability_hint"] = gitee_provider_hint(provider)
        return [], provider

    issues = json.loads(raw)
    docs_files = repo_markdown_files(project)
    items = []
    for issue in issues:
        source_url = (
            issue.get("html_url")
            or issue.get("htmlUrl")
            or issue.get("url")
            or f"https://gitee.com/{repo}/issues/{issue.get('number') or issue.get('id')}"
        )
        labels = []
        for entry in issue.get("labels", []):
            if isinstance(entry, dict):
                labels.append(entry.get("name", ""))
            else:
                labels.append(str(entry))
        linked_paths = linked_paths_for_url(project, source_url, docs_files)
        if linked_paths:
            source_type = "gitee_linked_open_issue"
            restart_point = "cleanup"
            next_action = "Reconcile external closeout/writeback drift for the already-linked Gitee source issue."
        else:
            source_type = "gitee_raw_issue"
            restart_point = "pre_brainstorm"
            next_action = "Consume the raw Gitee source issue into pre-brainstorm without treating platform labels as canonical truth."
        items.append(
            {
                "source_family": "external issue",
                "source_type": source_type,
                "source_ref": source_url,
                "artifact_path": source_url,
                "status_markers": {
                    "platform": "gitee",
                    "number": issue.get("number", issue.get("id")),
                    "labels": labels,
                    "canonical_linkage": "present" if linked_paths else "missing",
                    "created_at": issue.get("created_at") or issue.get("createdAt"),
                    "updated_at": issue.get("updated_at") or issue.get("updatedAt"),
                },
                "needs_action": True,
                "restart_point": restart_point,
                "owner_hint": linked_paths[0] if linked_paths else "manager",
                "next_action": next_action,
                "title": issue.get("title", ""),
                "linked_paths": linked_paths,
            }
        )
    return items, provider


def scan_chat_inbox(project: Path) -> list[dict]:
    """Scan .freely/chat-inbox.db for unconsumed chat intakes."""
    items = []
    db_path = project / ".freely" / "chat-inbox.db"
    if not db_path.is_file():
        return items
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM chats WHERE consumed = 0 ORDER BY id ASC LIMIT 50"
        ).fetchall()
        conn.close()
    except Exception:
        return items

    for r in rows:
        chat = dict(r)
        chat_type = chat.get("chat_type", "")
        issue_id = chat.get("issue_id", "")
        msg = chat.get("message", "")[:200]
        if chat_type == "new-issue":
            restart_point = "pre_brainstorm"
            next_action = (
                f"Create worktree feature/{issue_id}-{{slug}}, "
                "wt-create will auto-materialize from chat-inbox."
            )
        else:
            restart_point = "continuation"
            next_action = (
                f"Deliver comment to {issue_id}. "
                "If worktree exists, append there. Otherwise AI decides."
            )
        items.append({
            "source_family": "human interruption",
            "source_type": "chat_intake",
            "source_ref": f"intake://{issue_id}",
            "artifact_path": str(db_path.relative_to(project)),
            "chat_type": chat_type,
            "chat_id": chat["id"],
            "status_markers": {"status": "new", "classification": "discovery"},
            "needs_action": True,
            "restart_point": restart_point,
            "owner_hint": "worker",
            "next_action": next_action,
            "message_preview": msg,
        })
    return items


def build_payload(project: Path) -> dict:
    sources = []
    sources.extend(scan_chat_inbox(project))
    sources.extend(scan_raw_issues(project))
    sources.extend(scan_linked_issues(project))
    sources.extend(scan_pre_brainstorms(project))
    sources.extend(scan_milestones(project))
    sources.extend(scan_progress(project))
    github_sources, github_provider = scan_external_github(project)
    gitee_sources, gitee_provider = scan_external_gitee(project)
    sources.extend(github_sources)
    sources.extend(gitee_sources)

    summary = {}
    for item in sources:
        family = item["source_family"]
        summary[family] = summary.get(family, 0) + 1

    return {
        "scan_version": "task-source-scan-v1",
        "generated_at": now_iso(),
        "project_root": str(project),
        "recommended_skill": "auto-loop-orchestrator",
        "routing_skill": "context-source-skill",
        "trigger_policy": {
            "run_when": [
                "startup_patrol",
                "after_closeout_or_verification_updates_canonical_truth",
                "when_worker_capacity_is_available",
                "when_no_worker_is_currently_running",
            ],
            "avoid_when": [
                "all_worker_slots_are_busy_on_unresolved_active_lanes",
                "a_fresh_scan_would_only_restate_the_same_in_flight_lane_without_new_truth",
            ],
        },
        "providers": {
            "external_issue": {
                "github": github_provider,
                "gitee": gitee_provider,
            }
        },
        "summary": {
            "actionable_count": len(sources),
            "by_family": summary,
        },
        "sources": sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()
    project = Path(args.project).resolve()
    payload = build_payload(project)
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
