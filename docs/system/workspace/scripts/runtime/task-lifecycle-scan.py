#!/usr/bin/env python3
"""task-lifecycle-scan: lifecycle-aware scan — one raw→I chain per output item.

Principle: completed items are SILENT. Only items with incomplete steps appear.
For each raw→I lifecycle chain, check 8 completion criteria.
All pass → excluded. Any fail → output with specific blockers listed.

Usage: python3 task-lifecycle-scan.py --project /path/to/project [--json]
"""
from __future__ import annotations
import argparse, json, os, re, sys, subprocess
from datetime import datetime, timezone
from pathlib import Path

TERMINAL_RAW = {"absorbed", "dropped", "completed"}
TERMINAL_CANDIDATE = {"absorbed", "dropped", "promoted"}
ACTIVE_B2 = {"in_b2_ibm", "done_b2_ibm", "in_dev", "blocked_dev"}
COMPLETED = "completed"
DONE_STATES = {"done", "done_ibm", "completed"}  # all mean "implementation finished"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── YAML-lite parsing (no PyYAML dependency) ──────────────

def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fields = {}
    in_platform_ids = False
    current_platform = ""
    for line in parts[1].splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Handle nested platform_ids
        if re.match(r"^\w+:\s*$", stripped) and ":" in stripped and not stripped.split(":")[1].strip():
            in_platform_ids = True
            current_platform = stripped.split(":")[0].strip()
            continue
        if in_platform_ids and stripped.startswith("-"):
            in_platform_ids = False
            current_platform = ""
            continue
        if ":" not in stripped:
            continue
        key, _, val = stripped.partition(":")
        key = key.strip().lstrip("-").strip()
        val = val.strip().strip("`").strip('"').strip("'")
        if in_platform_ids and current_platform:
            key = f"platform_ids.{current_platform}.{key}"
        fields[key] = val
    return fields


def parse_markdown_fields(path: Path) -> dict:
    if not path.is_file():
        return {}
    fields = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^- ([a-z_]+):\s*`?(.*?)`?\s*$", line.rstrip())
            if m:
                fields[m.group(1)] = m.group(2).strip()
    return fields


# ── Item collection ──────────────────────────────────────

def collect_lifecycle_items(project: Path) -> list[dict]:
    """Collect raw issues + their I-* children, grouped by shared base key."""
    raw_items: dict[str, dict] = {}
    linked_children: dict[str, list[dict]] = {}  # key → list of child dicts
    standalone_linked: list[dict] = []  # I-* with no raw parent
    issues_dir = project / "docs" / "issues"

    if issues_dir.is_dir():
        for d in sorted(issues_dir.iterdir()):
            if not d.is_dir():
                continue
            mf = d / "issue.md"
            if not mf.is_file():
                continue
            fm = parse_frontmatter(mf.read_text(encoding="utf-8"))
            name = d.name

            if name.startswith("raw-"):
                key = name[4:]  # "raw-20260428-1737" → "20260428-1737"
                raw_items[key] = {
                    "raw_id": name, "raw_status": fm.get("status", "proposed"),
                    "raw_file": str(mf.relative_to(project)),
                    "promoted_children": _parse_list(fm.get("promoted_children", "")),
                    "absorbed_into": fm.get("absorbed_into", ""),
                    "platform_ids": _extract_platform_ids(fm),
                }
            elif name.startswith("I-"):
                # I-YYYYMMDD-HHMM-A → base_key="YYYYMMDD-HHMM", suffix="A"
                inner = name[2:]  # "20260428-1737-A"
                # Split off the suffix letter
                m = re.match(r"^(\d{8}-\d{4})-([A-Z])$", inner)
                if m:
                    base_key = m.group(1)
                    suffix = m.group(2)
                else:
                    base_key = inner  # legacy format without suffix
                    suffix = ""
                title = fm.get("issue_title", "")
                if not title:
                    body = parts[2] if len(parts := mf.read_text(encoding="utf-8").split("---", 2)) >= 3 else ""
                    tm = re.search(r"^# (.+)", body, re.MULTILINE)
                    title = tm.group(1) if tm else name
                child = {
                    "linked_id": name, "phase_state": fm.get("phase_state", ""),
                    "status": fm.get("status", ""), "title": title, "suffix": suffix,
                    "linked_file": str(mf.relative_to(project)),
                    "promoted_from": fm.get("promoted_from", ""),
                    "canonical_issue_path": fm.get("canonical_issue_path", ""),
                    "platform_ids": _extract_platform_ids(fm),
                    "comment_count": _count_comments(mf),
                    "unsynced_comments": _count_unsynced(mf),
                }
                # Try to match to a raw parent by promoted_from
                pf = fm.get("promoted_from", "")
                if pf and pf.startswith("raw-"):
                    raw_key = pf[4:]
                    if raw_key in raw_items:
                        linked_children.setdefault(raw_key, []).append(child)
                        continue
                # Try to match by base key
                if base_key in raw_items:
                    linked_children.setdefault(base_key, []).append(child)
                else:
                    standalone_linked.append(child)

    # Follow absorbed_into links: absorbed raw-* items whose children
    # were matched by base_key (not by promoted_from) need the link
    for key, raw in raw_items.items():
        absorbed_into = raw.get("absorbed_into", "")
        if raw.get("raw_status") == "absorbed" and absorbed_into:
            # If children already matched, skip
            if key in linked_children and linked_children[key]:
                continue
            # Try matching by absorbed_into I-* ID
            for child_list in linked_children.values():
                for c in child_list:
                    if c["linked_id"] == absorbed_into:
                        linked_children.setdefault(key, []).append(c)
                        # Remove from standalone if present
                        standalone_linked = [s for s in standalone_linked if s["linked_id"] != absorbed_into]
                        break

    # Build output items — merge standalone I-* that share a key with raw items
    items = []
    standalone_by_key: dict[str, list[dict]] = {}
    for child in standalone_linked:
        base = _base_key(child["linked_id"])
        standalone_by_key.setdefault(base, []).append(child)

    for key, raw in sorted(raw_items.items()):
        children = linked_children.get(key, [])
        # Merge standalone children with matching key
        if key in standalone_by_key:
            existing_ids = {c["linked_id"] for c in children}
            for sc in standalone_by_key[key]:
                if sc["linked_id"] not in existing_ids:
                    children.append(sc)
            del standalone_by_key[key]
        items.append({"key": key, "raw": raw, "children": children})

    # Remaining standalone I-* (no raw parent at all)
    for key, children in sorted(standalone_by_key.items()):
        items.append({"key": key, "raw": None, "children": children})

    return items


def _base_key(local_id: str) -> str:
    """Extract base time key from any issue ID.
    raw-20260428-1737 → 20260428-1737
    I-20260428-1737-A → 20260428-1737
    I-20260428-1737 → 20260428-1737
    """
    inner = local_id
    if inner.startswith("raw-"):
        inner = inner[4:]
    elif inner.startswith("I-"):
        inner = inner[2:]
    # Strip suffix letter: 20260428-1737-A → 20260428-1737
    m = re.match(r"^(\d{8}-\d{4})-[A-Z]$", inner)
    if m:
        inner = m.group(1)
    return inner


def _parse_list(val: str) -> list[str]:
    """Parse a YAML-like list string: "['a', 'b']" or "a, b" into a Python list."""
    if not val:
        return []
    val = val.strip()
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1]
        return [x.strip().strip("'").strip('"') for x in inner.split(",") if x.strip()]
    return [x.strip() for x in val.split(",") if x.strip()]


def _extract_platform_ids(fm: dict) -> dict:
    ids = {}
    for plat in ("github", "gitee"):
        iid = fm.get(f"platform_ids.{plat}.issue_id", "")
        if iid:
            ids[plat] = iid
    return ids


def _count_comments(issue_file: Path) -> int:
    if not issue_file.is_file():
        return 0
    text = issue_file.read_text(encoding="utf-8")
    return len(re.findall(r"^### comment-", text, re.MULTILINE))


def _count_unsynced(issue_file: Path) -> int:
    """Count comments missing platform_ids for either github or gitee."""
    if not issue_file.is_file():
        return 0
    text = issue_file.read_text(encoding="utf-8")
    unsynced = 0
    comments = re.split(r"^### (?=comment-)", text, flags=re.MULTILINE)
    for c in comments[1:]:  # skip pre-comments section
        has_gh = "github" in c and "comment_id" in c[c.find("github"):c.find("github")+80] if "github" in c else False
        has_gt = "gitee" in c and "comment_id" in c[c.find("gitee"):c.find("gitee")+80] if "gitee" in c else False
        if not has_gh or not has_gt:
            unsynced += 1
    return unsynced


# ── Stage determination ──────────────────────────────────

def determine_stage(item: dict) -> str:
    raw = item.get("raw")
    children = item.get("children", [])

    if not raw and not children:
        return "empty"

    # Absorbed raw
    if raw and raw.get("raw_status") == "absorbed":
        if children:
            return _stage_from_children(children)
        return "absorbed"

    # Dropped raw
    if raw and raw.get("raw_status") == "dropped":
        return "dropped"

    # Raw only, no children promoted yet
    if raw and not children:
        b1_dir = _find_b1_dir(raw.get("raw_id", ""))
        if not b1_dir:
            return "B1_proposed"
        candidates_file = Path(b1_dir) / "candidates.md" if b1_dir else None
        if candidates_file and candidates_file.is_file():
            cfields = parse_markdown_fields(candidates_file)
            if cfields.get("status") not in TERMINAL_CANDIDATE:
                return "B1_candidate"
        return "B1_brainstorming"

    # Have children in various stages
    if children:
        return _stage_from_children(children)

    return "unknown"


def _stage_from_children(children: list[dict]) -> str:
    phases = {c.get("phase_state", "") for c in children}
    if not phases or phases == {""}:
        has_platforms = any(c.get("platform_ids") for c in children)
        if has_platforms:
            return "B2_active"
        return "promoting"
    if phases & ACTIVE_B2:
        return "B2_active"
    if "in_verification" in phases:
        return "B2_verifying"
    # done/done_ibm: implementation finished, awaiting merge/verification/closeout
    if phases & DONE_STATES or COMPLETED in phases:
        if phases & DONE_STATES and COMPLETED not in phases:
            return "B2_done"  # implementation done, not yet marked completed
        return "收口"
    return "promoting"


def _find_b1_dir(raw_id: str) -> Path | None:
    """Find pre-brainstorm directory matching raw timestamp."""
    key = raw_id[4:] if raw_id.startswith("raw-") else raw_id
    # Search for directories starting with the key
    cwd = Path.cwd()
    b1_root = cwd / "docs" / "pre-brainstorms"
    if not b1_root.is_dir():
        return None
    for d in sorted(b1_root.iterdir(), reverse=True):
        if d.is_dir() and d.name.startswith(key):
            return d
    return None


def _stage_from_linked(linked: dict) -> str:
    phase = linked.get("phase_state", "")
    if not phase:
        return "B2_active"  # no phase = assume active
    if phase in ACTIVE_B2:
        return "B2_active"
    if phase == "in_verification":
        return "B2_verifying"
    if phase == COMPLETED:
        return "收口"  # still needs platform close check
    return "B2_active"


# ── Completion checklist ─────────────────────────────────

def check_completion(item: dict) -> list[str]:
    """Return list of incomplete items. Empty list = fully complete (exclude from output).

    Highest authority: platform CLOSED. If all platform issues are confirmed closed,
    the item is complete regardless of local state.
    """
    incomplete = []
    raw = item.get("raw")
    children = item.get("children", [])

    # Raw checks
    if raw:
        if raw.get("raw_status") not in TERMINAL_RAW:
            raw_pids = raw.get("platform_ids", {})
            if raw_pids.get("github"):
                raw_gh = _is_github_closed(raw_pids["github"])
                if raw_gh is True:
                    pass  # closed = done, skip all checks
                elif raw_gh is False:
                    incomplete.append("raw_github_not_closed")
                # None = unchecked, don't flag
            if not incomplete:
                pass  # raw is done

    # Child checks
    if not children:
        incomplete.append("not_promoted_to_I")
        return incomplete

    for child in children:
        cid = child.get("linked_id", "?")
        pfx = f"{cid}:"
        pids = child.get("platform_ids", {})

        # Rule: if ALL platforms with IDs are confirmed CLOSED → item is complete.
        # Don't check phase_state, comments, or anything else.
        all_confirmed_closed = True
        has_any_platform = False
        if pids.get("github"):
            has_any_platform = True
            gh_closed = _is_github_closed(pids["github"])
            if gh_closed is not True:  # False or None
                all_confirmed_closed = False
                if gh_closed is False:
                    incomplete.append(f"{pfx}github_not_closed")
        if pids.get("gitee"):
            has_any_platform = True
            # Gitee check requires API; skip for now
            all_confirmed_closed = False

        if has_any_platform and all_confirmed_closed:
            continue  # platform says done → skip all other checks

        # Platform not confirmed closed → check local state
        if child.get("phase_state") not in DONE_STATES and child.get("phase_state") != COMPLETED:
            incomplete.append(f"{pfx}phase_not_completed")
        if not pids and child.get("phase_state") not in DONE_STATES and child.get("phase_state") != COMPLETED:
            incomplete.append(f"{pfx}not_on_any_platform")
        if child.get("unsynced_comments", 0) > 0:
            incomplete.append(f"{pfx}unsynced_comments:{child['unsynced_comments']}")

    return incomplete


def _is_github_closed(issue_number: str) -> bool | None:
    """Check if a GitHub issue is closed. Returns None if can't check (no gh CLI or timeout)."""
    # Skip if gh not available or running in background
    if os.environ.get("SKIP_PLATFORM_CHECK"):
        return None
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(issue_number),
             "--repo", "chatterzhao/freely", "--json", "state"],
            capture_output=True, text=True, timeout=5
        )
        return '"CLOSED"' in result.stdout
    except Exception:
        return None  # unknown, don't flag as incomplete


# ── Main ─────────────────────────────────────────────────

def build_payload(project: Path) -> dict:
    items = collect_lifecycle_items(project)
    output = []

    for item in items:
        stage = determine_stage(item)
        incomplete = check_completion(item)
        if _should_exclude(stage, incomplete, item):
            continue
        raw = item.get("raw") or {}
        children = item.get("children", [])
        output.append(_format_item(item, stage, incomplete, raw, children))

    # Add worktree governance items
    gov_items = scan_worktree_governance(project)
    output.extend(gov_items)

    by_stage = {}
    for o in output:
        by_stage[o["stage"]] = by_stage.get(o["stage"], 0) + 1

    return {
        "scan_version": "lifecycle-v2",
        "generated_at": now_iso(),
        "project_root": str(project),
        "summary": {
            "total_incomplete": len(output),
            "by_stage": by_stage,
            "ready": sum(1 for o in output if o["ready"]),
        },
        "items": output,
    }


def _should_exclude(stage: str, incomplete: list[str], item: dict) -> bool:
    if not incomplete and stage == "收口":
        return True
    if stage in ("absorbed", "dropped") and not incomplete:
        return True
    if not incomplete and not item.get("raw") and not item.get("children"):
        return True
    return False


def _format_item(item: dict, stage: str, incomplete: list[str], raw: dict, children: list[dict]) -> dict:
    return {
        "key": item["key"],
        "stage": stage,
        "raw_id": raw.get("raw_id"),
        "title": raw.get("raw_id", "") or (children[0].get("title", "") if children else ""),
        "children": [
            {
                "id": c["linked_id"],
                "phase": c.get("phase_state") or None,
                "pids": c.get("platform_ids", {}),
                "unsynced": c.get("unsynced_comments", 0),
            }
            for c in children
        ],
        "incomplete": incomplete,
        "next_action": _derive_action(stage, incomplete),
        "ready": "not_promoted_to_I" not in incomplete,
    }


def _derive_action(stage: str, incomplete: list[str]) -> str:
    # Priority: doc updates first (cheapest), then platform close, then investigation
    inc_str = " ".join(incomplete)

    if "not_promoted_to_I" in inc_str:
        return "完成 B1 预研 → 产出 candidate → 决策 promote"
    if stage == "B1_proposed":
        return "创建 B1 预研目录，开始发散收敛"
    if stage == "B1_brainstorming":
        return "完成 brainstorms.md，产出 candidates.md"
    if stage == "B1_candidate":
        return "决策 candidate：promote（创建 I-*）/ absorb（合并）/ drop（放弃）"
    if stage == "B2_done":
        return "实现已完成：merge 到 develop → 标记 completed → platform close"
    if "phase_not_completed" in inc_str:
        return "更新 phase_state 为 completed"
    if "not_on_any_platform" in inc_str:
        return "issue-sync create 推送 I-* 到平台"
    if "github_not_closed" in inc_str:
        return "issue-sync close github"
    if any("gitee" in i and "unchecked" not in i for i in incomplete):
        return "issue-sync close gitee"
    if any("unsynced" in i for i in incomplete):
        return "issue-sync comment 推送未同步评论"
    if any("unchecked" in i for i in incomplete):
        return "运行完整 scan 检查平台状态"
    return "检查并完成收口步骤"


# ── Branch / worktree governance scan ───────────────────

def _is_protected_branch(branch: str) -> bool:
    """main, develop, and tags are permanent — everything else should correspond to an issue."""
    if branch in ("main", "develop"):
        return True
    if branch.startswith("refs/tags/"):
        return True
    return False


def _extract_issue_key_from_branch(branch: str) -> str | None:
    """Extract raw-xxx or I-xxx key from branch name.
    feature/raw-20260428-1737-foo → raw-20260428-1737
    hotfix/I-20260428-1737-A-bar → I-20260428-1737-A
    test-pre-merge-scan-v3 → None (no issue key)
    """
    for pattern in [r"(raw-\d{8}-\d{4})", r"(I-\d{8}-\d{4}(?:-[A-Z0-9]+)?)"]:
        m = re.search(pattern, branch)
        if m:
            return m.group(1)
    return None


def _issue_is_done(project: Path, issue_key: str) -> bool:
    """Check if an issue's phase_state indicates it's done/completed."""
    issue_dir = project / "docs" / "issues" / issue_key
    if not issue_dir.is_dir():
        return False
    issue_file = issue_dir / "issue.md"
    if not issue_file.is_file():
        return False
    fm = parse_frontmatter(issue_file.read_text(encoding="utf-8"))
    phase = fm.get("phase_state", "")
    status = fm.get("status", "")
    return phase in DONE_STATES or status in DONE_STATES


def _branch_merged_to_develop(project: Path, branch: str) -> bool | None:
    """Check if branch is merged into develop. None if can't determine."""
    try:
        subprocess.check_call(
            ["git", "-C", str(project), "merge-base", "--is-ancestor", branch, "develop"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def _worktree_dirty(worktree_path: Path) -> bool:
    """Check if a worktree has uncommitted changes."""
    try:
        result = subprocess.check_output(
            ["git", "-C", str(worktree_path), "status", "--porcelain"],
            text=True, stderr=subprocess.DEVNULL,
        )
        return bool(result.strip())
    except subprocess.CalledProcessError:
        return False


def _worktree_has_runtime(worktree_path: Path) -> bool:
    """Check if worktree has .freely/run/ with runtime history."""
    run_dir = worktree_path / ".freely" / "run"
    return run_dir.is_dir() and any(run_dir.iterdir())


def _worktree_branch(worktree_path: Path) -> str | None:
    """Get the checked-out branch for a worktree."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(worktree_path), "branch", "--show-current"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return None


def scan_worktree_governance(project: Path) -> list[dict]:
    """Scan branches and worktrees for governance issues.

    Principle:
    - main/develop/tags are permanent — excluded
    - All other branches must correspond to an issue (raw-xxx or I-xxx in name)
    - If the issue is done → branch/worktree is "未收口" (needs cleanup)
    - If the issue is NOT done → skip (covered by issue lifecycle scan)
    - If no matching issue → "孤儿" (orphan branch)
    """
    items = []

    # Get all worktrees
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(project), "worktree", "list", "--porcelain"],
            text=True, stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return items

    # Parse worktree list
    worktrees: dict[str, dict] = {}  # path → {branch, ...}
    current_wt = None
    for line in raw.splitlines():
        if line.startswith("worktree "):
            current_wt = line[9:]
            worktrees[current_wt] = {"path": current_wt, "branch": None}
        elif line.startswith("branch ") and current_wt:
            branch_ref = line[7:]
            if branch_ref.startswith("refs/heads/"):
                worktrees[current_wt]["branch"] = branch_ref[11:]

    # Get all local branches
    try:
        branches_raw = subprocess.check_output(
            ["git", "-C", str(project), "branch", "--format=%(refname:short)"],
            text=True, stderr=subprocess.DEVNULL,
        )
        all_branches = [b.strip() for b in branches_raw.splitlines() if b.strip()]
    except subprocess.CalledProcessError:
        all_branches = []

    # Build worktree index by branch
    worktree_by_branch: dict[str, dict] = {}
    project_wt_path = str(project.resolve())
    for wt_path, wt_info in worktrees.items():
        branch = wt_info.get("branch")
        if branch:
            worktree_by_branch[branch] = wt_info

    # Scan each non-protected branch
    for branch in all_branches:
        if _is_protected_branch(branch):
            continue

        issue_key = _extract_issue_key_from_branch(branch)
        wt_info = worktree_by_branch.get(branch, {})
        wt_path = wt_info.get("path", "")
        wt_path_obj = Path(wt_path) if wt_path else None

        # Determine worktree state
        is_dirty = _worktree_dirty(wt_path_obj) if wt_path_obj else False
        has_runtime = _worktree_has_runtime(wt_path_obj) if wt_path_obj else False
        merged_to_develop = _branch_merged_to_develop(project, branch)

        # If this is the project's own worktree, skip
        if wt_path and str(Path(wt_path).resolve()) == project_wt_path:
            continue

        # Determine stage and incomplete reasons
        if not issue_key:
            # Orphan: branch without issue key
            items.append({
                "source_family": "worktree_governance",
                "key": branch,
                "branch": branch,
                "worktree_path": wt_path or "无工位",
                "issue_key": None,
                "stage": "orphan_branch",
                "dirty": is_dirty,
                "has_runtime": has_runtime,
                "merged_to_develop": merged_to_develop,
                "incomplete": ["no_issue_key"],
                "next_action": "无对应 issue：判断是否误创建或需补充 issue",
                "ready": False,
            })
            continue

        issue_done = _issue_is_done(project, issue_key)

        if not issue_done:
            # Issue not done → skip (covered by issue lifecycle scan)
            continue

        # Issue is done → 未收口: needs cleanup
        incomplete = []
        if is_dirty:
            incomplete.append("worktree_dirty")
        if merged_to_develop is False:
            incomplete.append("branch_not_merged_to_develop")
        if has_runtime and merged_to_develop:
            incomplete.append("worktree_not_retired")

        if not incomplete and not is_dirty and merged_to_develop:
            # Fully clean — just needs retirement
            incomplete.append("ready_to_retire")

        items.append({
            "source_family": "worktree_governance",
            "key": branch,
            "branch": branch,
            "worktree_path": wt_path or "无工位",
            "issue_key": issue_key,
            "stage": "未收口",
            "dirty": is_dirty,
            "has_runtime": has_runtime,
            "merged_to_develop": merged_to_develop,
            "incomplete": incomplete,
            "next_action": _derive_governance_action(is_dirty, merged_to_develop, has_runtime),
            "ready": not is_dirty,
        })

    return items


def _derive_governance_action(dirty: bool, merged: bool | None, has_runtime: bool) -> str:
    if dirty:
        return "提交或丢弃 dirty 修改 → merge 到 develop → 退役工位 → 删分支"
    if merged is False:
        return "merge 到 develop → 退役工位 → 删分支"
    if has_runtime:
        return "已 merge，退役工位并删除分支"
    return "工位已退役但分支仍存在：删除分支"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--json", action="store_true", default=True)
    args = parser.parse_args()
    project = Path(args.project).resolve()
    payload = build_payload(project)
    json.dump(payload, sys.stdout, indent=2, sort_keys=True, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
