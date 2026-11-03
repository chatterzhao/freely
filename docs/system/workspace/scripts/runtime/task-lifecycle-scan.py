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

import importlib.util
import json, os, re, sqlite3, subprocess, sys, time
import yaml
from pathlib import Path
from datetime import datetime, timezone

_LIFECYCLE_DIR = Path(__file__).resolve().parents[1] / "lifecycle"
sys.path.insert(0, str(_LIFECYCLE_DIR))
from raw_metadata_contract import MetadataValidationError, normalize, validate
from agent_identity_value import first_agent_id


def _bound_worker_agent_id(row: dict | None) -> str:
    """Read the worker identity through the shared wire-value codec."""
    return first_agent_id((row or {}).get("worker_id", "")) or ""


# Raw and linked issues have different lifecycle domains.
RAW_TERMINAL_PHASES = {"absorbed", "dropped"}
LINKED_TERMINAL_PHASES = {"absorbed", "dropped", "completed"}

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

# ── Station-based action mapping ────────────────────────────────────
# Two-level [manager]/[worker] delegation templates.
# {key} replaced with actual raw key at render time.
# {wt} replaced with worktree path (for items with existing worktree).

STATION_ACTIONS = {
    # ── B1 phase ──
    "raw_created": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug b1\n"
        "[worker] cd <wt> && skill:freely-doc-B1_IBM-execution → brainstorms.md → candidates.md"
    ),
    "b1_dir": (
        "[worker] cd <wt> && skill:freely-doc-B1_IBM-execution → 工位已存在，写入 brainstorms.md"
    ),
    "b1_dir_no_wt": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug b1\n"
        "[worker] cd <wt> && skill:freely-doc-B1_IBM-execution → 写入 brainstorms.md"
    ),
    "b1_brainstorm": (
        "[worker] cd <wt> && skill:freely-doc-B1_IBM-execution → 工位已存在，产出 candidates.md"
    ),
    "b1_brainstorm_no_wt": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug b1\n"
        "[worker] cd <wt> && skill:freely-doc-B1_IBM-execution → 产出 candidates.md"
    ),
    "b1_candidate": (
        "[worker] cd <wt> && skill:freely-candidate-acceptance-review → 决策 promote/absorb/drop"
    ),
    # ── B2 / Implementation phase ──
    "candidate_decision": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug impl\n"
        "[worker] cd <wt> && skill:freely-doc-B2_IBM-execution → materialize I-* → dev-loop"
    ),
    "i_created": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug impl\n"
        "[worker] cd <wt> && skill:freely-dev-loop-execution → 推进 phase_state"
    ),
    "dev_worktree": (
        "[worker] cd <wt> && skill:freely-dev-loop-execution → 工位已存在，推进 phase_state"
    ),
    "dev_worktree_no_wt": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug work\n"
        "[worker] cd <wt> && skill:freely-dev-loop-execution → 推进 phase_state"
    ),
    "dev_phase_done": (
        "[worker] cd <wt> && skill:freely-test-execution → freely pr-create-guarded → freely pr-review-guarded → freely pr-merge-guarded → freely wt-close"
    ),
    # ── Close / Sync phase ──
    "platform_create": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug sync\n"
        "[worker] cd <wt> && freely issue-sync create → skill:freely-dev-loop-execution → skill:freely-test-execution → guarded PR lifecycle"
    ),
    "merged_develop": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug close\n"
        "[worker] cd <wt> && freely issue-sync close → skill:freely-dev-loop-execution → skill:freely-test-execution → guarded PR lifecycle"
    ),
    "platform_close": (
        "[manager] freely feedback --title \"Close platform issue\" --body \"Sync close\" --kind fix\n  → wt-create --raw-key {{new_key}} --source platform --kind fix --slug close\n"
        "[worker] cd <wt> && freely issue-sync close → skill:freely-dev-loop-execution → skill:freely-test-execution → guarded PR lifecycle"
    ),
    "branch_deleted": (
        "[manager] freely feedback --title \"Sync after delete\" --body \"Sync close\" --kind fix\n  → wt-create --raw-key {{new_key}} --source platform --kind fix --slug sync\n"
        "[worker] cd <wt> && freely issue-sync close → skill:freely-dev-loop-execution → skill:freely-test-execution → guarded PR lifecycle"
    ),
    # ── Dead agent recovery ──
    "agent_dead": (
        "[manager] 检查 agent-working 表 → 恢复 session 或重新委派 worker\n"
        "[worker] cd <wt> && 继续之前的工作"
    ),
    # ── I-* linked-issue stations ──
    "i_non_terminal": (
        "[manager] freely feedback --title \"Fix I-* state\" --body \"Update I-* issue phase_state\" --kind fix\n  → wt-create --raw-key {{new_key}} --source platform --kind fix --slug fix-i-state\n"
        "[worker] cd <wt> && 更新 I-* issue 的 phase_state 为 completed/absorbed"
    ),
    "i_no_phase": (
        "[manager] freely feedback --title \"Fix I-* state\" --body \"Update I-* issue phase_state\" --kind fix\n  → wt-create --raw-key {{new_key}} --source platform --kind fix --slug fix-i-state\n"
        "[worker] cd <wt> && 调查 I-* issue 缺少 phase_state，补充并更新"
    ),
    # ── Raw-issue stations (no worktree yet) ──
    "raw_not_started": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug b1\n"
        "[worker] cd <wt> && skill:freely-doc-B1_IBM-execution → brainstorms.md → candidates.md"
    ),
    "raw_no_phase": (
        "[manager] wt-create --raw-key {key} --source platform --kind fix --slug b1\n"
        "[worker] cd <wt> && 先补充 issue.md 的 phase_state → B1 预研"
    ),
}


def _detect_station(item: dict, issues_by_raw: dict, wt_by_raw: dict) -> str:
    """Detect which lifecycle station an item is at.

    Returns a station key from STATION_ACTIONS, or a raw stage name
    (close_local, close_platform, B1_proposed, 收口, 恢复) for items
    that don't fit the station pipeline.
    """
    subcategory = item.get("subcategory", "")
    raw_key = item.get("key", "")
    raw_issue = issues_by_raw.get(raw_key)
    wt = wt_by_raw.get(raw_key)
    # For linked (I-*) items, phase_state is on the item itself from read_issues_dir
    phase = item.get("phase_state", "")
    if raw_issue and not phase:
        phase = raw_issue.get("phase_state", "")
    issue_kind = item.get("kind", "")
    is_linked = raw_key.startswith("I-") or issue_kind == "linked"

    # ── Category 3: dead agent on existing worktree ──
    if subcategory in ("3a_never_bound", "3b_session_dead"):
        return "agent_dead"

    # ── Category 2b: worktree not cleaned ──
    if subcategory == "2b_worktree_not_cleaned":
        return "收口"

    # ── Category 1: not started ──
    if subcategory in ("1a_fresh", "1b_reopen"):
        return "B1_proposed"

    # ── Category 2: document misaligned ──
    if subcategory == "2a_state_mismatch":
        return "platform_close"

    # Non-terminal phase or missing platform_state
    if subcategory in ("2a_non_terminal", "2a_missing_platform_state"):
        if is_linked:
            # I-* linked issue with non-terminal or empty phase_state
            if not phase or phase == "":
                return "i_no_phase"
            return "i_non_terminal"
        # Raw issue classification
        if not raw_issue:
            return "raw_not_started"
        if phase in ("proposed", ""):
            # Platform state determines the right action:
            # - platform closed → work was done externally, just fix local doc
            # - platform open/unknown → truly not started, needs worktree
            plat = item.get("platform_state", "")
            if plat == "closed":
                return "merged_develop"
            return "raw_not_started"
        if phase in RAW_TERMINAL_PHASES:
            return "merged_develop"
        return "close_local"

    return "收口"


def _render_next_action(station: str, key: str, worktree: str = "") -> str:
    """Render two-level [manager]/[worker] next_action for a station."""
    template = STATION_ACTIONS.get(station, STATION_ACTIONS.get("raw_created", ""))
    if not template:
        return f"[manager] 检查 {key} 状态并决定下一步"
    result = template.replace("{key}", key)
    if worktree:
        result = result.replace("<wt>", worktree)
    return result


def _stage_action(station: str) -> str:
    """Map station to human-readable stage description."""
    actions = {
        "raw_created": "创建工位 → B1 预研",
        "b1_dir": "B1 预研（工位已存在）",
        "b1_dir_no_wt": "创建工位 → B1 预研",
        "b1_brainstorm": "B1 brainstorms（工位已存在）",
        "b1_brainstorm_no_wt": "创建工位 → B1 brainstorms",
        "b1_candidate": "B1 candidate 决策",
        "candidate_decision": "创建工位 → B2 物化",
        "i_created": "创建工位 → dev-loop",
        "dev_worktree": "dev-loop（工位已存在）",
        "dev_worktree_no_wt": "创建工位 → dev-loop",
        "dev_phase_done": "freely pr-create-guarded → freely pr-review-guarded → freely pr-merge-guarded → freely wt-close",
        "platform_create": "创建工位 → freely issue-sync create → guarded PR lifecycle",
        "merged_develop": "创建工位 → freely issue-sync close → guarded PR lifecycle",
        "platform_close": "freely feedback --kind fix → wt-create → freely issue-sync close → guarded PR lifecycle",
        "branch_deleted": "freely feedback --kind fix → wt-create → freely issue-sync close → guarded PR lifecycle",
        "agent_dead": "恢复 worker session / 重新委派",
        "B1_proposed": "创建工位 → B1 预研",
        "close_local": "更新本地 phase_state",
        "close_platform": "freely issue-sync close → 关闭配置平台 issue",
        "收口": "检查并完成收口步骤",
        "恢复": "恢复 worker session 或重新委派",
    }
    return actions.get(station, "检查并完成")


def _build_sync_batch(items: list[dict], project_path, ts: str, platforms: list[str] = None) -> list[dict]:
    """Collect platform sync items into one deduplicated batch.

    Cross-scan dedup: if the same set of sync keys was already batched
    in a previous scan, produce a noop entry instead of a new actionable one.
    """
    sync_stages = {"platform_close", "close_platform", "close_local", "merged_develop"}
    sync_items = [it for it in items if it.get("station") in sync_stages
                  or it.get("stage") in sync_stages]
    remaining = [it for it in items if it not in sync_items]

    if not sync_items:
        return items

    # Keep individual items visible — batch is an ADDITIONAL summary, not a replacement.
    # Individual items are needed for traceability and testing.

    close_platform_count = sum(1 for it in sync_items if it.get("station") == "platform_close"
                               or it.get("stage") == "close_platform")
    close_local_count = sum(1 for it in sync_items if it.get("station") == "close_local"
                            or it.get("stage") == "close_local")
    merged_count = sum(1 for it in sync_items if it.get("station") == "merged_develop")
    total_sync = len(sync_items)

    # Cross-scan dedup via fingerprint
    sync_keys = sorted([it.get("key", "") for it in sync_items])
    fingerprint = json.dumps({"keys": sync_keys, "total": total_sync}, sort_keys=True)
    state_dir = project_path / ".freely" / "run"
    state_file = state_dir / "platform-sync-batch-state.json"

    noop = False
    if state_file.exists():
        try:
            prev = json.loads(state_file.read_text())
            if prev.get("fingerprint") == fingerprint:
                noop = True
        except (json.JSONDecodeError, KeyError):
            pass

    if not noop:
        state_dir.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps({"fingerprint": fingerprint, "last_ts": ts}, indent=2))

    batch_item = {
        "key": f"platform-sync-batch-{ts}",
        "station": "platform_sync_batch",
        "source_family": "platform_sync",
        "ready": not noop,
        "priority": "P0_highest",
        "noop": noop,
        "sync_summary": {
            "total": total_sync,
            "close_platform": close_platform_count,
            "close_local": close_local_count,
            "merged_develop": merged_count,
            "platforms": platforms if platforms else _detect_platforms(project_path),
        },
    }

    if not noop:
        batch_item["next_action"] = (
            f"[manager] freely feedback --title \"Platform sync batch: sync {total_sync} items\" "
            f"--body \"Batch sync: close_platform={close_platform_count} close_local={close_local_count} merged={merged_count}\" --kind fix\n"
            f"  → wt-create --raw-key {{new_key}} --source platform --kind fix --slug platform-sync\n"
            f"[worker] cd <wt> && freely issue-sync close → skill:freely-dev-loop-execution → skill:freely-test-execution → guarded PR lifecycle"
        )
    else:
        batch_item["next_action"] = "noop — same batch already processed in previous scan"

    # Prepend batch summary, keep individual items for traceability
    return [batch_item] + items


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
    fm_block = []
    in_fm = False
    for line in text.split("\n"):
        s = line.strip()
        if s == "---":
            if not in_fm:
                in_fm = True
                continue
            break
        if in_fm:
            fm_block.append(line)
    if fm_block:
        try:
            data = yaml.safe_load("\n".join(fm_block))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
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
      # Also scan bullet format (- key: value). Many I-* issues
    # use mixed format: YAML has kind/local_id, bullet has phase_state.
    for line in lines:
        m = re.match(r"^-\s*(\w[\w_]*):\s*(.*)", line)
        if m:
            k = m.group(1)
            if k not in fm:  # bullet supplements YAML, does not overwrite
                fm[k] = m.group(2).strip().strip("`'\"")
    return fm
def extract_raw_key(text: str) -> str | None:
    """Extract raw-{timestamp} key from text (title + body)."""
    m = re.search(r"(?:^|\W)(raw-(\d{8}T\d{4,6}Z))", text, re.MULTILINE | re.IGNORECASE)
    return m.group(2) if m else None

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
# The module file is named platform-adapter.py — the hyphen is a deliberate
# convention (avoids clashing with an installed `platform_adapter` package),
# but it is not a legal Python identifier, so `import platform_adapter`
# always raises ModuleNotFoundError. Load the real file explicitly via
# importlib and register it under the module name 'platform_adapter'.

_PA_MODULE = None
_PA_PROJECT = None


def _get_pa(project: Path):
    """Cached loader for docs/system/workspace/scripts/sync/platform-adapter.py.

    Returns the loaded module. Cached per project because scan may be invoked
    against different project roots within one process.
    """
    global _PA_MODULE, _PA_PROJECT
    sync_dir = project / "docs" / "system" / "workspace" / "scripts" / "sync"
    if _PA_MODULE is None or _PA_PROJECT != project:
        spec = importlib.util.spec_from_file_location(
            "platform_adapter", str(sync_dir / "platform-adapter.py")
        )
        _PA_MODULE = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_PA_MODULE)
        _PA_PROJECT = project
    return _PA_MODULE


def _detect_platforms(project: Path) -> list[str]:
    """Detect configured platforms from config.toml, fallback to git remotes."""
    try:
        platforms = _get_pa(project).configured_platforms()
        if platforms:
            return platforms
    except Exception:
        pass
    # Fallback: scan git remotes for known platform patterns
    platforms = []
    try:
        r = subprocess.run(["git", "-C", str(project), "remote", "-v"],
                          capture_output=True, text=True, timeout=5)
        remotes = r.stdout.lower()
        if "github" in remotes:
            platforms.append("github")
        if "gitee" in remotes:
            platforms.append("gitee")
    except Exception:
        pass
    if not platforms:
        print("[SCAN] FATAL: no platforms configured.", file=sys.stderr)
        print("[SCAN] Configure platforms in .freely/config.toml:", file=sys.stderr)
        print("[SCAN]   FREELY_REPO_PLATFORMS = \"github,gitee\"", file=sys.stderr)
        print("[SCAN] Or add remotes to .git/config.", file=sys.stderr)
        sys.exit(1)
    return platforms

def extract_platform_ids(text: str) -> dict[str, str]:
    """Extract per-platform issue IDs from frontmatter platform_ids block.
    Returns dict like {'github': '3833', 'gitee': 'IJZS1G'}."""
    ids = {}
    # Parse YAML-like: platform_ids:\n  github:\n    issue_id: '123'\n  gitee:\n    issue_id: ABC
    current_platform = None
    for line in text.split("\n"):
        s = line.strip()
        # Match top-level platform key under platform_ids
        if not s.startswith("-") and ":" in s and not s.startswith("issue_id") and not s.startswith("url") and not s.startswith("synced_at"):
            # Check if this is a platform name (not indented, or indented once)
            m = re.match(r"^\s*(\w+):\s*$", line)
            if m and m.group(1) not in ("platform_ids",):
                current_platform = m.group(1)
        # Match issue_id under a platform
        m = re.match(r"\s*issue_id:\s*['\"]?([^'\"]+)['\"]?", line)
        if m and current_platform:
            ids[current_platform] = m.group(1)
            current_platform = None  # reset after capturing
    return ids


def get_platform_open_issues(project: Path) -> dict[str, dict]:
    try:
        return _get_pa(project).list_open_issue_records()
    except Exception as exc:
        return {"__degraded__": {"platform": "adapter", "error": str(exc)[:200]}}


def _build_raw_key_index(platform_issues: dict[str, dict]) -> dict[str, dict[str, str]]:
    """Build raw_key → {platform_name: issue_id} mapping from platform issues.

    When local frontmatter lacks platform_ids, this index provides a fallback:
    extract raw_key from platform issue title (e.g. [RAW-20260429T000000Z])
    and match it to the local raw-{key} directory.

    Returns {raw_key: {pname: issue_id}} — one raw_key can map to
    multiple platforms (e.g. github: #123, gitee: ABC456).
    """
    index: dict[str, dict[str, str]] = {}
    for platform_issue_key, info in platform_issues.items():
        issue_id = str(info.get("issue_id", platform_issue_key))
        title = info.get("title", "")
        raw_key = extract_raw_key(title)
        if raw_key:
            if raw_key not in index:
                index[raw_key] = {}
            # Determine platform from issue_id format or info
            pname = info.get("platform", "")
            if not pname:
                # Heuristic: numeric → github, alphanumeric-starting-with-letter → gitee
                pname = "github" if issue_id.isdigit() else "gitee"
            index[raw_key][pname] = issue_id
    return index

def get_all_platform_issue_states(project: Path, open_issues: dict[str, dict]) -> dict[str, str]:
    """Fetch CLOSED states for ALL configured platforms.
    Uses platform-adapter for per-platform individual queries.
    Cached (5min TTL). Returns {issue_id: state} keyed by platform issue ID."""
    cache_file = project / ".freely" / "run" / "platform-all-cache.json"
    cached = cache_get(cache_file, ttl=300)
    if cached is not None:
        return cached.get("states", {})

    states: dict[str, str] = {num: "OPEN" for num in open_issues}

    platforms = _detect_platforms(project)
    try:
        pa = _get_pa(project)
        for h in pa._handlers():
            if h.name not in platforms:
                continue
            try:
                closed = pa._safe(h.list_closed_issues) or {}
                for num in closed:
                    if num not in states:
                        states[num] = "CLOSED"
            except Exception:
                pass
    except Exception:
        pass

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
            view = normalize(fm) if kind == "raw" else fm
            validation_error = ""
            if kind == "raw" and view["strict_schema"]:
                try:
                    validate(fm, base_dir=project)
                except MetadataValidationError as error:
                    validation_error = str(error)
            elif kind == "raw" and view.get("phase_state") == "absorbed":
                target = str(view.get("absorbed_into") or "")
                canonical = str(view.get("canonical_issue_path") or "")
                canonical_file = project / canonical if canonical else None
                if not target and not canonical:
                    validation_error = "legacy absorbed raw requires a canonical id or path"
                elif target and not target.startswith("I-"):
                    validation_error = "legacy absorbed_into must be an I-* id"
                elif canonical_file and not canonical_file.is_file():
                    validation_error = "legacy canonical issue path does not exist"
            issues.append({
                "name": name,
                "kind": kind,
                "path": str(d),
                "phase_state": view.get("phase_state", ""),
                "platform_state": view.get("platform_state", ""),
                "absorbed_into": view.get("absorbed_into", ""),
                "canonical_issue_path": view.get("canonical_issue_path", ""),
                "platform_ids": extract_platform_ids(text),
                "source_raw": fm.get("source_raw", ""),
                "source_candidate": fm.get("source_candidate", ""),
                "frontmatter": fm,
                "metadata_validation_error": validation_error,
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
                "platform_ids": extract_platform_ids(text),
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

    configured_platforms = _detect_platforms(project)
    platform_issues = get_platform_open_issues(project)
    platform_health = "ok"
    platform_degraded_reason = ""
    if "__degraded__" in platform_issues:
        platform_health = "degraded"
        platform_degraded_reason = str(platform_issues.pop("__degraded__").get("error", ""))[:200]
    timer.mark("platform_open")

    all_platform_states = get_all_platform_issue_states(project, platform_issues)

    # Build raw_key → platform_ids fallback index.
    # When local frontmatter lacks platform_ids but the raw_key appears
    # in platform issue titles, this index fills the gap so
    # _sync_platform_direct can still auto-close matching issues.
    raw_key_pid_index = _build_raw_key_index(platform_issues)
    timer.mark("platform_all_states")

    # File scan: always scan for accurate detection
    local_issues = read_issues_dir(project)
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

        if raw_issue and raw_issue.get("metadata_validation_error"):
            items.append({
                "category": "2_document_misaligned",
                "subcategory": "2a_invalid_raw_metadata",
                "key": raw_key,
                "issue_path": raw_issue["path"],
                "ready": False,
                "detail": raw_issue["metadata_validation_error"],
                "next_action": "[worker] repair raw metadata through the canonical lifecycle transition",
            })
            continue

        # ── Category 3: worktree exists → check agent liveness ────
        if wt_exists:
            wt_path = wt["path"]
            # Query agent_working table only (sole identity truth)
            agent_id = ""
            agent_binding_error = ""
            try:
                sys.path.insert(0, str(project / "docs" / "system" / "workspace" / "scripts" / "runtime"))
                from agent_working import agent_list_by_raw_key, AgentWorkingError
                from raw_key_canon import canonicalize_raw_key
                row = agent_list_by_raw_key(str(project), canonicalize_raw_key(raw_key))
                agent_id = _bound_worker_agent_id(row)
            except Exception as exc:
                # An unavailable identity store is not evidence that the worker
                # was never bound; avoid emitting a re-delegation instruction.
                agent_binding_error = str(exc) or type(exc).__name__

            # agent_working is the sole source of truth.
            if agent_binding_error:
                items.append({
                    "category": "3_binding_unavailable",
                    "subcategory": "3c_agent_working_unavailable",
                    "key": raw_key,
                    "worktree": str(wt_path),
                    "branch": wt.get("branch", ""),
                    "agent_id": "",
                    "ready": False,
                    "detail": f"agent_working binding unavailable — retry required: {agent_binding_error}",
                    "next_action": "[manager] retry agent_working lookup; do not re-delegate",
                })
            elif not agent_id:
                items.append({
                    "category": "3_dead_agent",
                    "subcategory": "3a_never_bound",
                    "key": raw_key,
                    "worktree": str(wt_path),
                    "branch": wt.get("branch", ""),
                    "agent_id": "",
                    "ready": True,
                    "detail": "agent_working missing binding — delegated but never bound",
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
            plat_state = raw_issue.get("platform_state", "")
            pids = raw_issue.get("platform_ids", {})

            # Platform-title lookup is an observation fallback only. Scanning must
            # never materialize or rewrite lifecycle metadata.
            if not pids or not any(v for v in pids.values() if v):
                fallback_pids = raw_key_pid_index.get(raw_key, {})
                if fallback_pids:
                    pids = fallback_pids

            # Check per-platform state alignment
            platform_mismatches = {}
            for pname in configured_platforms:
                pid = pids.get(pname, "")
                if pid and pid in all_platform_states:
                    actual = all_platform_states[pid]
                    local_upper = plat_state.upper() if plat_state else ""
                    if actual != local_upper:
                        platform_mismatches[pname] = actual

            # Subcategory 2a: non-terminal phase
            if phase not in RAW_TERMINAL_PHASES:
                items.append({
                    "category": "2_document_misaligned",
                    "subcategory": "2a_non_terminal",
                    "key": raw_key,
                    "issue_path": raw_issue["path"],
                    "phase_state": phase,
                    "platform_state": plat_state,
                    "ready": True,
                    "detail": f"phase_state='{phase}' is not a raw terminal phase (expected: absorbed/dropped)",
                    "next_action": "[manager] 创建 raw issue → 工位 → 通过受控生命周期命令推进状态",
                })
            else:
                # Scanning is observation-only. A mismatch is reported for a
                # controlled lifecycle command; it is never repaired in-place.
                if platform_mismatches:
                    items.append({
                        "category": "2_document_misaligned",
                        "subcategory": "2a_state_mismatch",
                        "key": raw_key,
                        "issue_path": raw_issue["path"],
                        "phase_state": phase,
                        "platform_state": plat_state,
                        "platform_mismatches": platform_mismatches,
                        "ready": True,
                        "detail": f"platform state mismatch for {raw_key}",
                        "next_action": "[manager] 通过 freely issue-sync 对齐配置平台状态",
                    })
                elif not plat_state:
                    # platform_state missing in local frontmatter
                    items.append({
                        "category": "2_document_misaligned",
                        "subcategory": "2a_missing_platform_state",
                        "key": raw_key,
                        "issue_path": raw_issue["path"],
                        "phase_state": phase,
                        "platform_state": "",
                        "ready": True,
                        "detail": "platform_state not set in frontmatter",
                        "next_action": "[manager] 创建 raw issue → 填上 platform_state",
                    })
                else:
                    # Terminal phase with local platform_state set but no
                    # real platform data to verify against.
                    # If platform_state is already "closed", this item is
                    # locally resolved — silently skip (nothing to sync).
                    if plat_state.startswith("closed"):
                        pass
                    else:
                        items.append({
                            "category": "2_document_misaligned",
                            "subcategory": "2a_state_mismatch",
                            "key": raw_key,
                            "issue_path": raw_issue["path"],
                            "phase_state": phase,
                            "platform_state": plat_state,
                            "ready": True,
                            "detail": f"terminal phase={phase} but platform_state={plat_state} — needs alignment",
                            "next_action": "[manager] 创建 raw issue → 工位 → 对齐 platform_state 与 phase_state",
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
                "next_action": f"[manager] wt-create --raw-key {raw_key} --source platform --kind fix",
            })
        # ── Reopen case (1b): platform OPEN + raw on develop with terminal phase ──
        # This is handled above: if raw_on_develop and phase is terminal,
        # we check platform alignment. If actual state is OPEN, it's in 2a_state_mismatch.
        # But the user said reopen should be Category 1, not 2.
        # Let me add a separate check:
        if raw_on_develop and raw_issue["phase_state"] in RAW_TERMINAL_PHASES and platform_open:
            pids = raw_issue.get("platform_ids", {})
            any_platform_open = False
            for pname in configured_platforms:
                pid = pids.get(pname, "")
                state = all_platform_states.get(pid, "") if pid else ""
                if state == "OPEN":
                    any_platform_open = True
                    break
            if any_platform_open:
                items.append({
                    "category": "1_not_started",
                    "subcategory": "1b_reopen",
                    "key": raw_key,
                    "issue_path": raw_issue["path"],
                    "phase_state": raw_issue["phase_state"],
                    "ready": True,
                    "detail": f"Previous round completed (phase={raw_issue['phase_state']}), platform issue REOPENED",
                    "next_action": f"[manager] wt-create --raw-key {raw_key} --source platform --kind fix (reopen)",
                })

    # ── Also check I-* issues for non-terminal state ────────────────
    for i_iss in i_issues:
        phase = i_iss["phase_state"]
        if phase not in LINKED_TERMINAL_PHASES:
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

        if raw_issue and raw_issue["phase_state"] in RAW_TERMINAL_PHASES:
            items.append({
                "category": "2_document_misaligned",
                "subcategory": "2b_worktree_not_cleaned",
                "key": key,
                "worktree": str(wt["path"]),
                "branch": branch,
                "ready": True,
                "detail": f"Raw issue terminal (phase={raw_issue['phase_state']}) but worktree still exists",
                "next_action": f"freely wt-close {branch}",
            })

    # ── 1c: Platform-only issues without local raw dir ──────────
    # Scan all platform OPEN issues and flag those with no local file.
    for num, pi in platform_issues.items():
        rk = extract_raw_key(pi.get("title", "") + "\n" + pi.get("body", ""))
        if not rk:
            continue
        if rk in seen_keys:
            continue
        seen_keys.add(rk)
        # Build per-platform state view from all_platform_states
        platform_states = {}
        # platform_issues is keyed by issue number; check if this num has state
        actual = all_platform_states.get(num, "")
        if actual:
            platform_states["detected"] = actual
        items.append({
            "category": "1_not_started",
            "subcategory": "1c_platform_only",
            "key": rk,
            "ready": True,
            "platform_states": platform_states,
            "detail": f"Platform issue OPEN but no local docs/B1-docs/raw-{rk}/",
            "next_action": f"[manager] raw-issue-pull --raw-key {rk} → 创建本地目录 → 评估状态",
        })

    # ── Post-processing: enrich items with station and next_action ──
    for item in items:
        sub = item.get("subcategory", "")
        key = item.get("key", "")
        wt_path = item.get("worktree", "")
        item["station"] = _detect_station(item, issues_by_raw, wt_by_raw)
        item["source_family"] = "chain_trace" if sub not in ("1a_fresh", "1b_reopen") else "platform_sync"
        # Render two-level next_action
        station = item["station"]
        item["next_action"] = _render_next_action(station, key, wt_path)
        item["stage_action"] = _stage_action(station)
        # Preserve stage for backward compatibility
        item["stage"] = station

    # ── Build sync batch with cross-scan dedup ──
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    batched_items = _build_sync_batch(items, project, ts, configured_platforms)

    # ── Build batches display for Manager ──
    by_station: dict[str, list[dict]] = {}
    for item in batched_items:
        st = item.get("station", item.get("stage", "收口"))
        by_station.setdefault(st, []).append(item)

    batches: list[dict] = []
    individual_stations = {"B1_proposed", "agent_dead", "收口", "恢复"}

    for st, st_items in sorted(by_station.items()):
        if st == "platform_sync_batch":
            # Sync batch is a singleton — keep as-is from _build_sync_batch
            batches.append(st_items[0])
        elif st not in individual_stations and len(st_items) > 1:
            sample_keys = [it["key"] for it in st_items[:5]]
            batches.append({
                "type": "batch",
                "station": st,
                "stage_action": _stage_action(st),
                "count": len(st_items),
                "sample_keys": sample_keys,
                "has_more": len(st_items) > 5,
                "ready": True,
                "next_action": _render_next_action(st, sample_keys[0] if sample_keys else "", ""),
            })
        else:
            for it in st_items:
                batches.append({
                    "type": "individual",
                    "station": it.get("station", it.get("stage", "")),
                    "stage_action": it.get("stage_action", ""),
                    "key": it["key"],
                    "ready": it.get("ready", True),
                    "next_action": it.get("next_action", ""),
                    "worktree": it.get("worktree", ""),
                    "branch": it.get("branch", ""),
                })

    # ── Summary ─────────────────────────────────────────────────────
    by_cat = {}
    ready_count = 0
    for item in batched_items:
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
            "total": len(batched_items),
            "ready": ready_count,
            "platform_health": platform_health,
            "platform_degraded_reason": platform_degraded_reason,
            "by_category": by_cat,
            "by_station": {st: len(si) for st, si in by_station.items()},
            "batch_count": len(batches),
        },
        "batches": batches,
        "items": batched_items,
    }


# ── CLI ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    project = Path(args.project)
    result = scan(project)

    output_flags = ["--json"] if args.json else []
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
