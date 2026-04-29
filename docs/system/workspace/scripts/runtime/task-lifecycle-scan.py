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
    """Collect all raw and I-* items, pair them by shared timestamp key."""
    raw_items: dict[str, dict] = {}
    linked_items: dict[str, dict] = {}
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
                    "absorbed_into": fm.get("absorbed_into", ""),
                    "platform_ids": _extract_platform_ids(fm),
                }
            elif name.startswith("I-"):
                key = name[2:]  # "I-20260428-1737" → "20260428-1737"
                title = fm.get("issue_title", "")
                if not title:
                    body = parts[2] if len(parts := mf.read_text(encoding="utf-8").split("---", 2)) >= 3 else ""
                    m = re.search(r"^# (.+)", body, re.MULTILINE)
                    title = m.group(1) if m else name
                linked_items[key] = {
                    "linked_id": name, "phase_state": fm.get("phase_state", ""),
                    "status": fm.get("status", ""),
                    "title": title,
                    "linked_file": str(mf.relative_to(project)),
                    "promoted_from": fm.get("promoted_from", ""),
                    "canonical_issue_path": fm.get("canonical_issue_path", ""),
                    "platform_ids": _extract_platform_ids(fm),
                    "comment_count": _count_comments(mf),
                    "unsynced_comments": _count_unsynced(mf),
                }

    # Merge: pair raw + linked by shared key
    all_keys = set(raw_items.keys()) | set(linked_items.keys())
    items = []
    for key in sorted(all_keys):
        raw = raw_items.get(key)
        linked = linked_items.get(key)

        # If raw was absorbed into a different I-*, follow the pointer
        if raw and raw.get("absorbed_into"):
            target_iid = raw["absorbed_into"]
            target_key = target_iid[2:] if target_iid.startswith("I-") else target_iid
            if target_key in linked_items and target_key != key:
                linked = linked_items[target_key]
                key = target_key  # reassign key to absorbing I-*

        items.append({"key": key, "raw": raw, "linked": linked})
    return items


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
    linked = item.get("linked")

    if not raw and not linked:
        return "empty"

    # Absorbed raw (pointing to another I-*)
    if raw and raw.get("raw_status") == "absorbed":
        if linked:
            return _stage_from_linked(linked)
        return "absorbed"

    # Dropped raw
    if raw and raw.get("raw_status") == "dropped":
        return "dropped"

    # Raw only, no I-* yet
    if raw and not linked:
        b1_dir = _find_b1_dir(raw.get("raw_id", ""))
        if not b1_dir:
            return "B1_proposed"
        candidates_file = Path(b1_dir) / "candidates.md" if b1_dir else None
        if candidates_file and candidates_file.is_file():
            cfields = parse_markdown_fields(candidates_file)
            if cfields.get("status") not in TERMINAL_CANDIDATE:
                return "B1_candidate"
        return "B1_brainstorming"

    # I-* exists
    if linked:
        return _stage_from_linked(linked)

    return "unknown"


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
    """Return list of incomplete items. Empty list = fully complete (exclude from output)."""
    incomplete = []
    raw = item.get("raw")
    linked = item.get("linked")

    # 1. raw_status_terminal
    if raw and raw.get("raw_status") not in TERMINAL_RAW:
        incomplete.append("raw_not_terminal")

    # 2. linked_exists
    if not linked:
        incomplete.append("not_promoted_to_I")
        return incomplete  # can't check further without I-*

    # 3. phase_completed
    if linked.get("phase_state") != COMPLETED:
        incomplete.append("phase_not_completed")

    # 4-5. platform issue closed
    pids = linked.get("platform_ids", {})
    if pids.get("github"):
        gh_closed = _is_github_closed(pids["github"])
        if gh_closed is False:
            incomplete.append("github_not_closed")
        elif gh_closed is None:
            incomplete.append("github_status_unchecked")
    # Gitee requires API token; mark as unchecked if we have a gitee ID
    if pids.get("gitee"):
        incomplete.append("gitee_status_unchecked")

    # 6. raw platform closed (if raw was synced)
    if raw:
        raw_pids = raw.get("platform_ids", {})
        if raw_pids.get("github"):
            raw_gh = _is_github_closed(raw_pids["github"])
            if raw_gh is False:
                incomplete.append("raw_github_not_closed")

    # 7. comments synced
    if linked.get("unsynced_comments", 0) > 0:
        incomplete.append(f"unsynced_comments:{linked['unsynced_comments']}")

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

        if not incomplete and stage == "收口":
            continue  # fully complete, exclude
        if stage in ("absorbed", "dropped") and not incomplete:
            continue  # terminal raw states, done
        if not incomplete and not item.get("raw") and not item.get("linked"):
            continue  # empty

        raw = item.get("raw") or {}
        linked = item.get("linked") or {}

        output.append({
            "key": item["key"],
            "stage": stage,
            "raw_id": raw.get("raw_id"),
            "linked_id": linked.get("linked_id"),
            "title": linked.get("title") or raw.get("raw_id", ""),
            "incomplete": incomplete,
            "next_action": _derive_action(stage, incomplete),
            "ready": stage not in ("B1_candidate",) and "not_promoted_to_I" not in incomplete,
        })

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


def _derive_action(stage: str, incomplete: list[str]) -> str:
    # Priority order: early-stage blockers first, then platform close, then doc updates
    if "not_promoted_to_I" in incomplete:
        return "完成 B1 预研 → 产出 candidate → 决策 promote"
    if stage == "B1_proposed":
        return "创建 B1 预研目录，开始发散收敛"
    if stage == "B1_brainstorming":
        return "完成 brainstorms.md，产出 candidates.md"
    if stage == "B1_candidate":
        return "决策 candidate：promote（创建 I-*）/ absorb（合并）/ drop（放弃）"
    if "phase_not_completed" in incomplete:
        return "更新 phase_state 为 completed，关闭平台 issue"
    if "github_not_closed" in incomplete:
        return "issue-sync close github"
    if any("gitee" in i and "unchecked" not in i for i in incomplete):
        return "issue-sync close gitee"
    if any("unsynced" in i for i in incomplete):
        return "issue-sync comment 推送未同步评论"
    if any("unchecked" in i for i in incomplete):
        return "运行 SKIP_PLATFORM_CHECK=0 扫描以检查平台状态"
    return "检查并完成收口步骤"


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
