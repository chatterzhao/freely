#!/usr/bin/env python3
"""
task-lifecycle-scan.py — Freely Manager Task Source Scanner

Scans the project for pending tasks across three categories:

  Category 1 — 未开始 (Not started)
    Platform OPEN issue exists but nothing local: no worktree, no raw dir on develop.
    Sub-types: 1a fresh, 1b reopen.

  Category 2 — 已完成但状态/清理不对齐 (Completed but misaligned)
    Raw/I-* issue exists on develop but state fields are wrong, platform state
    doesn't match, or worktree/branch cleanup missed.

  Category 3 — 进行中但 agent 已死 (In progress but agent dead)
    Worktree exists but the assigned agent's A2A session is not active.

Design principles:
  - No hardcoded platforms — all platform access via platform-adapter
  - Scan is cheap (code), Manager is expensive (AI tokens) — filter aggressively
  - A2A is the arbiter of "in progress" — active sessions are never scanned
  - "Not started" uses three-layer check: worktree → develop dir → neither

Usage:
  python3 task-lifecycle-scan.py <project_root> [--json]
"""

import json, os, re, sqlite3, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone


# ── Terminal phase states (lifecycle complete) ──────────────────────
TERMINAL_PHASES = {"absorbed", "dropped", "completed"}

# ── Timing ──────────────────────────────────────────────────────────

class Timer:
    def __init__(self):
        self.marks: dict[str, float] = {}
        self._start = time.time()
    def mark(self, name: str):
        self.marks[name] = time.time() - self._start
        return self.marks[name]
    def report(self) -> str:
        lines = []
        prev = 0.0
        for name, t in self.marks.items():
            lines.append(f"  {name}: {t-prev:.3f}s (total {t:.3f}s)")
            prev = t
        return "\n".join(lines)

# ── Helpers ─────────────────────────────────────────────────────────

def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def cache_get(cache_file: Path, ttl: int = 300) -> dict | None:
    """Read cache if fresh. Returns dict or None."""
    if cache_file.exists():
        try:
            data = json.loads(cache_file.read_text())
            age = time.time() - data.get("_cached_at", 0)
            if age < ttl:
                return data
        except Exception:
            pass
    return None

def cache_put(cache_file: Path, payload: dict):
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        payload["_cached_at"] = time.time()
        cache_file.write_text(json.dumps(payload))
    except Exception:
        pass

def parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from issue.md, returning flat dict."""
    fm = {}
    lines = text.split("\n")
    in_fm = False
    for line in lines:
        s = line.strip()
        if s == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                break
        if in_fm and ":" in s:
            k, v = s.split(":", 1)
            fm[k.strip()] = v.strip().strip("'\"")
    # Also try bullet format (- key: value)
    if not fm:
        for line in lines:
            m = re.match(r"^-\s*(\w[\w_]*):\s*(.*)", line)
            if m:
                fm[m.group(1)] = m.group(2).strip().strip("`'\"")
    return fm

def extract_raw_key(text: str) -> str | None:
    """Extract raw-{timestamp} key from text (title + body)."""
    m = re.search(r"(?:^|\W)(raw-(\d{8}T\d{4,6}Z))", text, re.MULTILINE)
    return m.group(2) if m else None

def extract_github_id(fm: dict, text: str) -> str:
    """Extract github issue id from frontmatter (nested or flat)."""
    # Nested: github:\n  issue_id: '123'
    m = re.search(r"github:\s*\n\s*issue_id:\s*['\"]?(\d+)", text)
    if m:
        return m.group(1)
    # Flat: github: '123'
    m = re.search(r"github:\s*['\"]?(\d+)", text)
    if m:
        return m.group(1)
    return ""

def find_worktree(project: Path, raw_key: str) -> Path | None:
    """Find worktree path whose branch/dir name contains the raw key."""
    try:
        result = subprocess.run(
            ["git", "-C", str(project), "worktree", "list", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        for line in result.stdout.split("\n"):
            if line.startswith("worktree "):
                wt = Path(line.split(" ", 1)[1].strip())
                name = wt.name
                if raw_key in name:
                    return wt
    except Exception:
        pass
    # Also check filesystem
    wt_root = project.parent / f"{project.name}-worktrees"
    if wt_root.is_dir():
        for d in wt_root.iterdir():
            if d.is_dir() and raw_key in d.name:
                return d
    return None

def list_all_worktrees(project: Path) -> list[dict]:
    """List all worktrees with metadata."""
    wts = []
    try:
        result = subprocess.run(
            ["git", "-C", str(project), "worktree", "list", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        current_wt = None
        for line in result.stdout.split("\n"):
            if line.startswith("worktree "):
                current_wt = {"path": Path(line.split(" ", 1)[1].strip())}
            elif line.startswith("branch ") and current_wt:
                current_wt["branch"] = line.split("refs/heads/", 1)[-1].strip()
            elif line.startswith("HEAD ") and current_wt:
                current_wt["head"] = line.split(" ", 1)[1].strip()
                wts.append(current_wt)
                current_wt = None
    except Exception:
        pass
    return wts


# ── Platform access (via platform-adapter, no hardcoding) ───────────


def _detect_platforms(project: Path) -> list[str]:
    """Detect configured platforms from git remotes (no hardcoded API calls)."""
    platforms = []
    try:
        r = subprocess.run(["git", "-C", str(project), "remote", "-v"],
                          capture_output=True, text=True, timeout=5)
        remotes = r.stdout
        if re.search(r'github', remotes):
            platforms.append("github")
        if re.search(r'gitee', remotes):
            platforms.append("gitee")
    except Exception:
        pass
    return platforms or ["github"]  # fallback

def _gh_repo(project: Path) -> str:
    """Detect GitHub repo from gh CLI."""
    try:
        r = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                          capture_output=True, text=True, timeout=5, cwd=str(project))
        return r.stdout.strip()
    except Exception:
        return ""

def _gitee_repo(project: Path) -> str:
    """Detect Gitee repo from git remotes."""
    try:
        r = subprocess.run(["git", "-C", str(project), "remote", "-v"],
                          capture_output=True, text=True, timeout=5)
        m = re.search(r'gitee[^:/]*[:/]([^/\s]+/[^/\s]+)', r.stdout)
        return m.group(1).replace('.git', '') if m else ""
    except Exception:
        return ""

def get_platform_open_issues(project: Path) -> dict[str, dict]:
    """Return {issue_number: {state, title, body, platform}} for all OPEN issues.
    Queries all detected platforms. Cached (5min TTL)."""
    cache_file = project / ".freely" / "run" / "platform-open-cache.json"
    cached = cache_get(cache_file, ttl=300)
    if cached is not None:
        return cached.get("B1-docs", {})

    issues: dict[str, dict] = {}
    platforms = _detect_platforms(project)

    for p in platforms:
        try:
            if p == "github":
                repo = _gh_repo(project)
                if not repo:
                    continue
                r = subprocess.run(
                    ["gh", "issue", "list", "--repo", repo, "--state", "open",
                     "--limit", "200", "--json", "number,state,title,body"],
                    capture_output=True, text=True, timeout=15, cwd=str(project))
                if r.returncode == 0 and r.stdout.strip():
                    for item in json.loads(r.stdout):
                        num = str(item.get("number", ""))
                        if num:
                            issues[num] = {
                                "state": "OPEN", "title": item.get("title", ""),
                                "body": item.get("body", ""), "platform": p}
            elif p == "gitee":
                repo = _gitee_repo(project)
                if not repo:
                    continue
                r = subprocess.run(
                    [sys.executable, str(project / "docs" / "system" / "workspace" / "scripts" / "runtime" / "gitee-issue.py"),
                     "--repo", repo, "list", "--state", "open", "--per-page", "100"],
                    capture_output=True, text=True, timeout=20)
                if r.returncode == 0 and r.stdout.strip():
                    for item in json.loads(r.stdout):
                        num = str(item.get("number", item.get("id", "")))
                        if num:
                            issues[num] = {
                                "state": "OPEN", "title": item.get("title", ""),
                                "body": item.get("body", ""), "platform": p}
        except Exception:
            continue

    cache_put(cache_file, {"B1-docs": issues})
    return issues

def get_all_platform_issue_states(project: Path, open_issues: dict[str, dict]) -> dict[str, str]:
    """Batch-fetch CLOSED states, merging with already-fetched OPEN.
    Cached (5min TTL). Only queries GitHub CLOSED; Gitee too slow for batch."""
    cache_file = project / ".freely" / "run" / "platform-all-cache.json"
    cached = cache_get(cache_file, ttl=300)
    if cached is not None:
        return cached.get("states", {})

    states: dict[str, str] = {num: "OPEN" for num in open_issues}

    platforms = _detect_platforms(project)
    if "github" in platforms:
        try:
            repo = _gh_repo(project)
            if repo:
                r = subprocess.run(
                    ["gh", "issue", "list", "--repo", repo, "--state", "closed",
                     "--limit", "500", "--json", "number,state"],
                    capture_output=True, text=True, timeout=15, cwd=str(project))
                if r.returncode == 0 and r.stdout.strip():
                    for item in json.loads(r.stdout):
                        num = str(item.get("number", ""))
                        if num and num not in states:
                            states[num] = "CLOSED"
        except Exception:
            pass
    # Gitee: skip batch. Individual state queries too slow for 500+ issues.

    cache_put(cache_file, {"states": states})
    return states


# ── A2A liveness (SQLite) ───────────────────────────────────────────

class A2AChecker:
    """Check agent liveness via A2A database."""
    def __init__(self, project: Path):
        self.db_path = project / ".freely" / "freely.db"
        self._conn = None

    @property
    def conn(self):
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
        return self._conn

    def agent_session_active(self, agent_id: str) -> bool:
        """Check if agent has an active A2A session."""
        try:
            row = self.conn.execute(
                # sessions.role currently stores generic roles ('worker').
                # agent_working table stores specific IDs ('worker_03').
                # Extract role prefix for query compatibility.
                "SELECT COUNT(*) FROM sessions WHERE (role=? OR role=?) AND status='active'",
                (agent_id, agent_id.split('_')[0] if '_' in agent_id else agent_id)
            ).fetchone()
            return row[0] > 0 if row else False
        except Exception:
            return False

    def acp_pid_alive(self) -> bool:
        """Check if claude-agent-acp process is running."""
        try:
            r = subprocess.run(
                ["pgrep", "-f", "claude-agent-acp"],
                capture_output=True, text=True, timeout=5
            )
            return r.returncode == 0 and r.stdout.strip() != ""
        except Exception:
            return False

    def agent_task_state(self, agent_id: str, worktree: str) -> str | None:
        """Get A2A task state for agent on this worktree."""
        try:
            row = self.conn.execute(
                "SELECT state, session_id FROM a2a_tasks WHERE agent_id=? AND worktree=? ORDER BY updated_at DESC LIMIT 1",
                (agent_id, worktree)
            ).fetchone()
            return {"state": row[0], "session_id": row[1]} if row else None
        except Exception:
            return None

    def agent_dead_detail(self, agent_id: str, worktree: str) -> dict:
        """Return death detail: reason, session_id, whether resume-able."""
        pid_alive = self.acp_pid_alive()
        if not pid_alive:
            return {"reason": "acp_pid_dead", "resumable": False, "session_id": ""}

        task = self.agent_task_state(agent_id, worktree)
        if task:
            return {
                "reason": f"session_not_active_task_{task['state']}",
                "resumable": task["state"] == "working",
                "session_id": task["session_id"],
            }
        return {"reason": "no_a2a_record", "resumable": False, "session_id": ""}




# ── Local issue reader ──────────────────────────────────────────────

def read_issues_dir(project: Path) -> list[dict]:
    """Read all raw-* and I-* issues from docs/B1-docs/ and docs/B2-docs/."""
    issues = []
    issues_dir = project / "docs" / "B1-docs"
    if issues_dir.is_dir():
        for d in sorted(issues_dir.iterdir()):
            if not d.is_dir():
                continue
            mf = d / "issue.md"
            if not mf.is_file():
                continue
            try:
                text = mf.read_text(encoding="utf-8")
            except Exception:
                continue
            fm = parse_frontmatter(text)
            name = d.name
            kind = "raw" if name.startswith("raw-") else "linked" if name.startswith("I-") else "other"
            issues.append({
                "name": name,
                "kind": kind,
                "path": str(d),
                "phase_state": fm.get("phase_state", ""),
                "platform_state": fm.get("platform_state", ""),
                "absorbed_into": fm.get("absorbed_into", ""),
                "github_id": extract_github_id(fm, text),
                "source_raw": fm.get("source_raw", ""),
                "source_candidate": fm.get("source_candidate", ""),
                "frontmatter": fm,
            })

    # Also scan I-* issues under new structure: docs/B2-docs/{epic}/{story}/raw-{raw key}/issues/
    epics_dir = project / "docs" / "B2-docs"
    if epics_dir.is_dir():
        for mf in sorted(epics_dir.glob("*/*/raw-*/issues/I-*.md")):
            try:
                text = mf.read_text(encoding="utf-8")
            except Exception:
                continue
            fm = parse_frontmatter(text)
            name = mf.stem  # e.g. I-20260628T005815Z-A
            issues.append({
                "name": name,
                "kind": "linked",
                "path": str(mf.parent),
                "phase_state": fm.get("phase_state", ""),
                "platform_state": fm.get("platform_state", ""),
                "absorbed_into": fm.get("absorbed_into", ""),
                "github_id": extract_github_id(fm, text),
                "source_raw": fm.get("source_raw", ""),
                "source_candidate": fm.get("source_candidate", ""),
                "frontmatter": fm,
            })
    return issues


# ── Main scan logic ──────────────────────────────────────────────────

def scan(project: Path) -> dict:
    """Run the full scan and return structured result."""
    timer = Timer()
    items: list[dict] = []
    seen_keys: set[str] = set()
    raw_key_pattern = re.compile(r"raw-(\d{8}T\d{4,6}Z)")

    # ── Load data ──────────────────────────────────────────────────
    # HEAD check for incremental skip
    current_head = ""
    try:
        r = subprocess.run(["git", "-C", str(project), "rev-parse", "HEAD"],
                          capture_output=True, text=True, timeout=5)
        current_head = r.stdout.strip()
    except Exception:
        pass
    scan_state_file = project / ".freely" / "run" / "manager-task-source-scan-state.env"
    last_head = ""
    if scan_state_file.exists():
        try:
            for line in scan_state_file.read_text().split("\n"):
                if line.startswith("LAST_TASK_SOURCE_SCAN_PROJECT_HEAD="):
                    last_head = line.split("=", 1)[1].strip().strip('"')
        except Exception:
            pass
    head_changed = (current_head != last_head)
    timer.mark("head_check")

    platform_issues = get_platform_open_issues(project)
    timer.mark("platform_open")

    all_platform_states = get_all_platform_issue_states(project, platform_issues)
    timer.mark("platform_all_states")

    # File scan: skip if HEAD unchanged
    if head_changed:
        local_issues = read_issues_dir(project)
    else:
        local_issues = []
    timer.mark("file_scan")

    worktrees = list_all_worktrees(project)
    timer.mark("worktree_list")


    a2a = A2AChecker(project)
    timer.mark("a2a_init")

    # Index local issues by raw key
    issues_by_raw: dict[str, dict] = {}
    i_issues: list[dict] = []
    for iss in local_issues:
        if iss["kind"] == "raw":
            # Extract key from directory name
            m = raw_key_pattern.search(iss["name"])
            if m:
                key = m.group(1)
                issues_by_raw[key] = iss
        elif iss["kind"] == "linked":
            i_issues.append(iss)

    # Index worktrees by raw key
    wt_by_raw: dict[str, dict] = {}
    for wt in worktrees:
        branch = wt.get("branch", "")
        path_name = wt["path"].name
        m = raw_key_pattern.search(branch + path_name)
        if m:
            key = m.group(1)
            wt_by_raw[key] = wt

    # ── Collect all raw keys from all sources ──────────────────────
    all_keys: set[str] = set()

    # From platform OPEN issues
    for num, pi in platform_issues.items():
        rk = extract_raw_key(pi.get("title", "") + "\n" + pi.get("body", ""))
        if rk:
            all_keys.add(rk)

    # From local raw issues
    all_keys.update(issues_by_raw.keys())

    # From worktrees
    all_keys.update(wt_by_raw.keys())


    # ── Apply decision tree for each key ───────────────────────────
    for raw_key in sorted(all_keys):
        wt = wt_by_raw.get(raw_key)
        raw_issue = issues_by_raw.get(raw_key)
        wt_exists = wt is not None
        raw_on_develop = raw_issue is not None
        platform_open = any(
            extract_raw_key(pi.get("title", "") + "\n" + pi.get("body", "")) == raw_key
            for pi in platform_issues.values()
        )

        # ── Category 3: worktree exists → check agent liveness ────
        if wt_exists:
            wt_path = wt["path"]
            # Query agent_working table first (preferred), fallback to agent-id.env
            agent_id = ""
            try:
                from agent_working import agent_list_by_raw_key
                row = agent_list_by_raw_key(str(project), f"raw-{raw_key}")
                if row:
                    wid = row.get("worker_id", "")
                    if wid:
                        agent_id = wid.split(":")[0] if ":" in str(wid) else str(wid)
            except Exception:
                pass

            # Fallback: legacy agent-id.env file
            if not agent_id:
                agent_env_file = project / ".freely" / "agent-id.env"
                if agent_env_file.exists():
                    try:
                        wt_path_str = str(wt_path)
                        for line in agent_env_file.read_text().split("\n"):
                            if wt_path_str in line:
                                parts = line.strip().split("=")
                                if len(parts) >= 3:
                                    agent_id = parts[-1]
                                break
                    except Exception:
                        pass

            if not agent_id:
                items.append({
                    "category": "3_dead_agent",
                    "subcategory": "3a_never_bound",
                    "key": raw_key,
                    "worktree": str(wt_path),
                    "branch": wt.get("branch", ""),
                    "agent_id": "",
                    "ready": True,
                    "detail": "agent_working + agent-id.env both missing — delegated but never bound",
                    "next_action": "[manager] re-delegate worker for this raw key",
                })
            elif not a2a.agent_session_active(agent_id):
                death = a2a.agent_dead_detail(agent_id, str(wt_path))
                items.append({
                    "category": "3_dead_agent",
                    "subcategory": "3b_session_dead",
                    "key": raw_key,
                    "worktree": str(wt_path),
                    "branch": wt.get("branch", ""),
                    "agent_id": agent_id,
                    "ready": True,
                    "death_reason": death["reason"],
                    "session_id": death["session_id"],
                    "resumable": death["resumable"],
                    "next_action": f"[manager] resume session {death['session_id']} + '继续'" if death["resumable"]
                                   else "[manager] re-delegate worker",
                })
            else:
                # Agent alive — skip
                pass
            continue  # worktree exists → done with this key

        # ── Category 2: raw on develop → check alignment ──────────
        if raw_on_develop:
            phase = raw_issue["phase_state"]
            plat_state = raw_issue["platform_state"]
            gh_id = raw_issue["github_id"]

            # Subcategory 2a: non-terminal phase
            if phase not in TERMINAL_PHASES:
                items.append({
                    "category": "2_document_misaligned",
                    "subcategory": "2a_non_terminal",
                    "key": raw_key,
                    "issue_path": raw_issue["path"],
                    "phase_state": phase,
                    "platform_state": plat_state,
                    "ready": True,
                    "detail": f"phase_state='{phase}' not terminal (expected: absorbed/dropped/completed)",
                    "next_action": "[manager] 创建 raw issue → 工位 → 修正本地文档状态为 terminal",
                })
            else:
                # Terminal — check platform_state alignment
                actual_state = ""
                if gh_id:
                    actual_state = all_platform_states.get(gh_id, "")

                if not plat_state:
                    # Only flag if we actually have platform data to compare against
                    if gh_id and all_platform_states and gh_id in all_platform_states:
                        items.append({
                            "category": "2_document_misaligned",
                            "subcategory": "2a_missing_platform_state",
                            "key": raw_key,
                            "issue_path": raw_issue["path"],
                            "phase_state": phase,
                            "platform_state": "",
                            "actual_platform_state": actual_state,
                            "ready": True,
                            "detail": "platform_state not set in frontmatter",
                            "next_action": f"[manager] 创建 raw issue → 填上 platform_state (platform actual={actual_state})",
                        })
                elif actual_state and plat_state.upper() != actual_state.upper() and gh_id in all_platform_states:
                    items.append({
                        "category": "2_document_misaligned",
                        "subcategory": "2a_state_mismatch",
                        "key": raw_key,
                        "issue_path": raw_issue["path"],
                        "phase_state": phase,
                        "platform_state": plat_state,
                        "actual_platform_state": actual_state,
                        "ready": True,
                        "detail": f"local platform_state='{plat_state}' != actual='{actual_state}'",
                        "next_action": "[manager] 创建 raw issue → 工位 → 对齐 platform_state",
                    })

            continue  # raw on develop → done with this key

        # ── Category 1: not started ────────────────────────────────
        if platform_open:
            # Check if it's a reopen (raw on develop exists from previous round)
            # Already checked above — if raw_on_develop is True, we'd be in Cat 2
            items.append({
                "category": "1_not_started",
                "subcategory": "1a_fresh",
                "key": raw_key,
                "ready": True,
                "detail": "Platform OPEN, no local worktree or raw directory",
                "next_action": f"[manager] wt-create --raw-key {raw_key} --source platform --skill freely-workflow-guarded-execution",
            })
        # ── Reopen case (1b): platform OPEN + raw on develop with terminal phase ──
        # This is handled above: if raw_on_develop and phase is terminal,
        # we check platform alignment. If actual state is OPEN, it's in 2a_state_mismatch.
        # But the user said reopen should be Category 1, not 2.
        # Let me add a separate check:
        if raw_on_develop and raw_issue["phase_state"] in TERMINAL_PHASES and platform_open:
            gh_id = raw_issue["github_id"]
            actual = all_platform_states.get(gh_id, "") if gh_id else ""
            if actual == "OPEN":
                items.append({
                    "category": "1_not_started",
                    "subcategory": "1b_reopen",
                    "key": raw_key,
                    "issue_path": raw_issue["path"],
                    "phase_state": raw_issue["phase_state"],
                    "ready": True,
                    "detail": f"Previous round completed (phase={raw_issue['phase_state']}), platform issue REOPENED",
                    "next_action": f"[manager] wt-create --raw-key {raw_key} --source platform --skill freely-workflow-guarded-execution (reopen)",
                })

    # ── Also check I-* issues for non-terminal state ────────────────
    for i_iss in i_issues:
        phase = i_iss["phase_state"]
        if phase not in TERMINAL_PHASES:
            items.append({
                "category": "2_document_misaligned",
                "subcategory": "2a_non_terminal",
                "key": i_iss["name"],
                "issue_path": i_iss["path"],
                "phase_state": phase,
                "ready": True,
                "detail": f"I-* issue phase_state='{phase}' not terminal",
                "next_action": "[manager] 创建 raw issue → 工位 → 修正 I-* 文档状态",
            })

    # ── Check for orphan worktrees (2b) ─────────────────────────────
    for wt in worktrees:
        branch = wt.get("branch", "")
        path_name = wt["path"].name
        m = raw_key_pattern.search(branch + path_name)
        if not m:
            continue
        key = m.group(1)
        raw_issue = issues_by_raw.get(key)

        if raw_issue and raw_issue["phase_state"] in TERMINAL_PHASES:
            items.append({
                "category": "2_document_misaligned",
                "subcategory": "2b_worktree_not_cleaned",
                "key": key,
                "worktree": str(wt["path"]),
                "branch": branch,
                "ready": True,
                "detail": f"Raw issue terminal (phase={raw_issue['phase_state']}) but worktree still exists",
                "next_action": f"wt-close {branch}",
            })

    # ── Check chat inbox for unconsumed messages (1c/2d) ────────────

    # ── Summary ─────────────────────────────────────────────────────
    by_cat = {}
    ready_count = 0
    for item in items:
        cat = item.get("category", "unknown")
        by_cat[cat] = by_cat.get(cat, 0) + 1
        if item.get("ready"):
            ready_count += 1

    # ── Persist scan state ────────────────────────────────────────
    scan_state_file = project / ".freely" / "run" / "manager-task-source-scan-state.env"
    scan_state_file.parent.mkdir(parents=True, exist_ok=True)
    scan_state_file.write_text(f"""LAST_TASK_SOURCE_SCAN_JSON="{project}/.freely/run/manager-task-source-scan-latest.json"
LAST_TASK_SOURCE_SCAN_REASON="scheduled_scan"
LAST_TASK_SOURCE_SCAN_GENERATED_AT="{now_utc()}"
LAST_TASK_SOURCE_SCAN_PROJECT_HEAD="{current_head}"
""")
    timer.mark("write_state")

    # ── Timing report (stderr) ─────────────────────────────────────
    print(f"[scan] total={timer.marks['write_state']:.3f}s head_changed={head_changed}", file=sys.stderr)
    print(timer.report(), file=sys.stderr)

    return {
        "generated_at": now_utc(),
        "project_root": str(project),
        "scan_version": "lifecycle-v3",
        "head_changed": head_changed,
        "_timing": {k: round(v, 3) for k, v in timer.marks.items()},
        "summary": {
            "total": len(items),
            "ready": ready_count,
            "by_category": by_cat,
        },
        "items": items,
    }


# ── CLI ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    project = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    result = scan(project)

    output_flags = sys.argv[2:] if len(sys.argv) > 2 else []
    if "--json" in output_flags or "-j" in output_flags:
        # Write to stdout and also to the scan file
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    # Also write to the standard location
    out_file = project / ".freely" / "run" / "manager-task-source-scan-latest.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nWritten to {out_file}", file=sys.stderr)
