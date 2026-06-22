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

# IBM Framework §89: raw.phase_state ∈ {proposed, absorbed, dropped}
# IBM Framework §89: I-*.phase_state ∈ {in_b2_ibm → done_b2_ibm → in_dev → blocked_dev → in_verification → completed}
TERMINAL_RAW = {"absorbed", "dropped"}
TERMINAL_CANDIDATE = {"absorbed", "dropped", "promoted"}
ACTIVE_B2 = {"in_b2_ibm", "done_b2_ibm", "in_dev", "blocked_dev"}
COMPLETED = "completed"
DONE_STATES = {"done_b2_ibm", "completed"}  # implementation finished (B2 done or fully complete)
TERMINAL_CHILD = {"absorbed", "dropped", "completed"}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── YAML-lite parsing (no PyYAML dependency) ──────────────

def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return _parse_legacy_frontmatter(text)
    parts = text.split("---", 2)
    # Accept 2 parts (opening --- without closing ---) or 3 parts (both delimiters)
    if len(parts) < 2:
        return {}
    yaml_text = parts[1] if len(parts) >= 2 else ""
    if not yaml_text.strip():
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
        # Root-level line (no leading whitespace) exits platform_ids nesting
        if in_platform_ids and line and not line[0].isspace():
            in_platform_ids = False
            current_platform = ""
        if ":" not in stripped:
            continue
        key, _, val = stripped.partition(":")
        key = key.strip().lstrip("-").strip()
        val = val.strip().strip("`").strip('"').strip("'")
        if in_platform_ids and current_platform:
            key = f"platform_ids.{current_platform}.{key}"
        fields[key] = val
    return fields


def _parse_legacy_frontmatter(text: str) -> dict:
    """Parse old-format frontmatter without YAML --- delimiters.
    Lines start with "- key: value".
    """
    fields = {}
    for line in text.splitlines():
        m = re.match(r"^\s*- ([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip().strip("`").strip('"').strip("'")
            fields[key] = val
        elif fields:
            break
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
                    "raw_id": name, "raw_status": fm.get("phase_state") or fm.get("status", "proposed"),
                    "raw_file": str(mf.relative_to(project)),
                    "promoted_children": _parse_list(fm.get("promoted_children", "")),
                    "absorbed_into": fm.get("absorbed_into", ""),
                    "platform_ids": _extract_platform_ids(fm),
                }
            elif name.startswith("I-"):
                # I-YYYYMMDDTHHMMZ-A (new) or I-YYYYMMDD-HHMM-A (old)
                # → base_key="YYYYMMDDTHHMMZ" or "YYYYMMDD-HHMM", suffix="A"
                inner = name[2:]
                m = re.match(r"^(\d{8}[-T]\d{4,6}Z?)-([A-Z])$", inner)
                if m:
                    base_key = m.group(1)
                    suffix = m.group(2)
                else:
                    # Legacy format without suffix, or non-standard
                    base_key = inner
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
    raw-20260504T1132Z → 20260504T1132Z
    I-20260428-1737-A → 20260428-1737
    I-20260504T1132Z-A → 20260504T1132Z
    """
    inner = local_id
    if inner.startswith("raw-"):
        inner = inner[4:]
    elif inner.startswith("I-"):
        inner = inner[2:]
    # Strip suffix letter (old: 20260428-1737-A, new: 20260504T1132Z-A)
    m = re.match(r"^(\d{8}[-T]\d{4,6}Z?)-[A-Z]$", inner)
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

def check_completion(item: dict, platform_data: dict) -> list[str]:
    incomplete = []
    raw = item.get("raw")
    children = item.get("children", [])

    # Raw checks
    if raw:
        if raw.get("raw_status") not in TERMINAL_RAW:
            raw_pids = raw.get("platform_ids", {})
            if raw_pids.get("github"):
                raw_gh = _is_github_closed_lookup(raw_pids["github"], platform_data)
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
            gh_closed = _is_github_closed_lookup(pids["github"], platform_data)
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


def fetch_open_platform_issues(project: Path) -> dict:
    """Fetch ALL GitHub issues in a single batch call.
    Returns {
      "all": dict[str, str],      # number → state (e.g. "OPEN", "CLOSED")
      "open_set": set[str],        # numbers of open issues
      "open_issues": list[dict],   # open issue objects
      "issues": list[dict],        # all issue objects with number, title, body, state
    }
    """
    result = {
        "all": {},
        "open_set": set(),
        "open_issues": [],
        "issues": [],
    }
    try:
        proc = subprocess.run(
            ["gh", "issue", "list", "--state", "all", "--limit", "5000",
             "--json", "number,title,body,state"],
            capture_output=True, text=True, timeout=30
        )
        if proc.returncode == 0:
            for issue in json.loads(proc.stdout):
                num = str(issue.get("number", ""))
                state = issue.get("state", "")
                result["all"][num] = state
                result["issues"].append(issue)
                if state == "OPEN":
                    result["open_set"].add(num)
                    result["open_issues"].append(issue)
    except Exception:
        pass  # fallback: empty platform_data, downstream checks will return None
    return result


def _is_github_closed_lookup(issue_number: str, platform_data: dict) -> bool | None:
    """Check issue state from platform_all dict — zero API calls.
    Returns True if CLOSED/MERGED, False if OPEN, None if unknown."""
    platform_all: dict = platform_data.get("all", {})
    state = platform_all.get(str(issue_number))
    if state is not None:
        return state != "OPEN"
    return None


def scan_classification(project: Path, platform_data: dict) -> list[dict]:
    """Phase 1+2: Classify local issues vs platform state + reverse discovery.

    Phase 1: Local vs platform classification:
      - pid in platform_all with matching state → consistent (skip)
      - pid in platform_all with different state → state_mismatch
      - pid not in platform_all → local_only

    Phase 2: Reverse discovery — platform issues referencing raw-{key} not in local.
    """
    platform_all: dict = platform_data.get("all", {})
    seen_in_local: set = set()
    items = []
    issues_dir = project / "docs" / "issues"
    if not issues_dir.is_dir():
        return items

    for d in sorted(issues_dir.iterdir()):
        if not d.is_dir():
            continue
        mf = d / "issue.md"
        if not mf.is_file():
            continue
        fm = parse_frontmatter(mf.read_text(encoding="utf-8"))
        pids = _extract_platform_ids(fm)
        gh_id = pids.get("github", "")
        name = d.name
        phase = fm.get("phase_state", "") or fm.get("status", "")
        source = "raw" if name.startswith("raw-") else "linked" if name.startswith("I-") else "other"
        local_platform_state = fm.get("platform_state", "").upper()

        if gh_id:
            seen_in_local.add(gh_id)
            plat_state = platform_all.get(gh_id, "").upper()
            if plat_state:
                if local_platform_state and local_platform_state != plat_state:
                    # Check if either side is terminal → resolve instead of sync
                    local_terminal = (phase in TERMINAL_RAW) or (phase in ("absorbed", "dropped"))
                    platform_closed = (plat_state == "CLOSED" or plat_state == "MERGED")

                    if local_terminal and not platform_closed:
                        items.append({
                            "source_family": "classification", "key": name,
                            "stage": "close_platform",
                            "detail": f"本地已 terminal ({phase}), 平台仍 {plat_state}",
                            "platform_issue": gh_id,
                            "incomplete": ["platform_not_closed"],
                            "ready": True,
                            "next_action": f"关闭平台 issue #{gh_id}（本地已 terminal: {phase}）",
                        })
                    elif platform_closed and not local_terminal:
                        items.append({
                            "source_family": "classification", "key": name,
                            "stage": "close_local",
                            "detail": f"平台已 {plat_state}, 本地仍 {local_platform_state}",
                            "platform_issue": gh_id,
                            "incomplete": ["local_not_closed"],
                            "ready": True,
                            "next_action": f"标记本地为 dropped（平台 issue #{gh_id} 已 {plat_state}）",
                        })
                    else:
                        # Both non-terminal → real mismatch
                        items.append({
                            "source_family": "classification", "key": name,
                            "stage": "state_mismatch",
                            "detail": f"本地状态={local_platform_state}, 平台状态={plat_state}",
                            "platform_issue": gh_id,
                            "incomplete": ["platform_state_mismatch"],
                            "ready": False,
                            "next_action": "同步本地平台状态或关闭平台 issue",
                        })
                # Consistent state → no action
            else:
                # gh_id not in platform_all → local_only
                if source in ("raw", "linked") and phase not in TERMINAL_RAW and phase not in ("absorbed", "dropped"):
                    items.append({
                        "source_family": "classification", "key": name,
                        "stage": "local_only",
                        "detail": "本地有 issue 但平台无对应",
                        "incomplete": ["no_platform_counterpart"],
                        "ready": True,
                        "next_action": "推送到平台建立对应",
                    })
        else:
            if source == "raw" and phase not in TERMINAL_RAW and phase not in ("absorbed", "dropped"):
                items.append({
                    "source_family": "classification", "key": name,
                    "stage": "local_only",
                    "detail": "本地有 raw 但平台无对应 issue",
                    "incomplete": ["no_platform_counterpart"],
                    "ready": True, "next_action": "推送到平台建立对应",
                })

    # Phase 2: Reverse discovery — platform issues with raw-{key} not in local
    for issue in platform_data.get("issues", []):
        num = str(issue.get("number", ""))
        if num in seen_in_local:
            continue
        if issue.get("state") != "OPEN":
            continue  # closed platform issues need no local counterpart
        title = issue.get("title", "")
        body = issue.get("body", "")
        combined = f"{title}\n{body}"
        raw_key = None
        for m in re.finditer(r"(?:^|\W)(raw-(\d{8}T\d{4,6}Z))", combined, re.MULTILINE):
            raw_key = m.group(2)
            break
        if raw_key:
            raw_dir = project / "docs" / "issues" / f"raw-{raw_key}"
            if raw_dir.is_dir():
                continue  # raw exists locally → skip
        items.append({
            "source_family": "classification",
            "key": f"gh-{num}",
            "stage": "platform_only",
            "detail": f"#{num}: {title[:60]}",
            "platform_issue": num,
            "incomplete": ["no_local_raw"],
            "ready": True,
            "next_action": f"raw-issue-pull --raw-key {raw_key}" if raw_key else f"issue-sync create raw-{num} ; gh issue view {num}",
        })

    # Dedup: same base key + same stage → one record
    deduped: dict = {}
    for it in items:
        base = _base_key(it["key"])
        stage = it["stage"]
        dedup_key = f"{base}|{stage}"
        if dedup_key in deduped:
            continue
        deduped[dedup_key] = it
    return list(deduped.values())


# ── Main ─────────────────────────────────────────────────

def _set_scan_states(items: list[dict], project: Path) -> None:
    """Set scan_state on each item based on worktree existence.

    pending  — default, no worktree found for this item's raw_key
    working  — a worktree exists for this raw_key (via wt-create)
    closed   — preserved from previous scan if raw issue still closed
    """
    import subprocess
    import re

    # Collect all existing worktree paths
    try:
        wt_list = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            capture_output=True, text=True, cwd=project, timeout=5
        ).stdout
        wt_paths = re.findall(r"^worktree (.+)$", wt_list, re.MULTILINE)
    except Exception:
        wt_paths = []

    for item in items:
        key = item.get("key", "")
        na = item.get("next_action", "")

        # Extract raw_key from key or next_action
        rk = ""
        for src in (key, na):
            m = re.search(r"(?:raw-)?(\d{8}T\d{6}Z)", src)
            if m:
                rk = m.group(1)
                break

        # Default: pending
        state = "pending"

        # Check worktree existence
        if rk:
            for wt in wt_paths:
                if rk in wt:
                    state = "working"
                    item["scan_state_worktree"] = wt
                    break

        item["scan_state"] = state

def build_payload(project: Path, raw_key: str = "") -> dict:
    output = []

    # Phase 0: Batch OPEN platform issues (1 API)
    platform_data = fetch_open_platform_issues(project)

    # Phase 0: Input gate — chat inbox
    chat_items = scan_chat_inbox(project)
    output.extend(chat_items)

    # Phase 1: Local vs Platform classification
    class_items = scan_classification(project, platform_data)
    output.extend(class_items)

    # Phase 3: Lifecycle chain trace (zero API — uses platform_data)
    chain_items = scan_chain_trace(project, platform_data, raw_key_filter=raw_key)
    for c in chain_items:
        # Derive title from available station data
        title = f"raw-{c['key']}"
        st = c.get("stations", {})
        if st.get("i_created") and st["i_created"].get("children"):
            title = st["i_created"]["children"][0].get("id", title)
        output.append({
            "source_family": "chain_trace",
            "key": c["key"],
            "stage": c["stage"],
            "next_station": c["next_station"],
            "blockers": c["blockers"],
            "ready": c["ready"],
            "next_action": c["next_action"],
            "incomplete": c["blockers"],
            "advisory": c.get("advisory", []),
            "children": [],
            "title": title,
            "paths": c.get("paths", {}),
            "pending_comments": c.get("pending_comments", 0),
        })

    # Phase: Platform open issues (GitHub/Gitee) — source_family=platform
    platform_items = scan_platform_issues(project, platform_data)
    output.extend(platform_items)

    # Add worktree governance items
    gov_items = scan_worktree_governance(project)
    output.extend(gov_items)

    # Add remote branch governance items
    remote_items = scan_remote_branch_governance(project)
    output.extend(remote_items)

    # Platform sync batch grouping — combine all sync-related items into one batch
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = add_platform_sync_batch(output, ts, project)

    # ── scan_state: set per-item lifecycle state from worktree existence ──
    _set_scan_states(output, project)

    # When raw_key is specified, filter output to only items matching this key.
    # This ensures the prompt builder gets only the targeted raw→I chain.
    if raw_key:
        output = [o for o in output if _matches_raw_key_filter(o, raw_key)]

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

    # Terminal resolution actions
    if stage == "close_platform":
        return "关闭平台侧 issue（本地已 terminal）"
    if stage == "close_local":
        return "标记本地 issue 为 dropped（平台已关闭）"
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


# ── Phase 0: Input gate (chat inbox + platform) ──────

def scan_chat_inbox(project: Path) -> list[dict]:
    """Scan .freely/freely.db for unconsumed chats.

    Trigger point 3 from chat-inbox-sqlite design:
    - SELECT consumed=0 AND (conversation_id=0 OR conversation_id IS NULL) → individual chats
    - SELECT conversation_id > 0 GROUP BY conversation_id → conversation groups
    - AI decides: create worktree (wt-create auto-materializes) |
                  add as comment to existing issue |
                  consume_conversation() for conversation batch |
                  discard as noise (consumed=-1)
    """
    items = []
    db_path = project / ".freely" / "freely.db"
    if not db_path.is_file():
        return items
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row

        # ── Individual chats (exclude conversation messages) ──
        rows = conn.execute(
            "SELECT * FROM chats WHERE consumed = 0 "
            "AND (conversation_id = 0 OR conversation_id IS NULL) "
            "ORDER BY id ASC LIMIT 50"
        ).fetchall()

        # ── Conversation groups (conversation_id > 0, unconsumed) ──
        conv_rows = conn.execute(
            "SELECT conversation_id, COUNT(*) as msg_count, "
            "MIN(created_at) as first_msg, MIN(id) as first_id "
            "FROM chats WHERE consumed = 0 AND conversation_id > 0 "
            "GROUP BY conversation_id ORDER BY MIN(id) ASC"
        ).fetchall()

        conn.close()
    except Exception:
        return items

    # Process conversation groups first
    for cr in conv_rows:
        conv = dict(cr)
        items.append({
            "source_family": "chat_conversation_pending",
            "key": f"conv-{conv['conversation_id']}",
            "stage": "chat_conversation_pending",
            "conversation_id": conv["conversation_id"],
            "message_count": conv["msg_count"],
            "first_message_at": conv["first_msg"] or "",
            "incomplete": ["conversation_unconsumed"],
            "ready": True,
            "next_action": "AI 判断 → consume_conversation() 批量消费 → materialize / comment / discard",
        })

    # Process individual chats

    for r in rows:
        chat = dict(r)
        chat_type = chat.get("chat_type", "")
        issue_id = chat.get("issue_id", "")
        msg = (chat.get("message", "") or "")[:200]

        # Check if a worktree exists for this issue (cross-format matching)
        worktree_exists = False
        if issue_id:
            key = issue_id.replace("raw-", "")
            variants = _normalize_key_variants(key)
            try:
                branches = subprocess.check_output(
                    ["git", "-C", str(project), "branch", "--format=%(refname:short)"],
                    text=True, stderr=subprocess.DEVNULL,
                )
                for branch in branches.splitlines():
                    for v in variants:
                        if v in branch:
                            worktree_exists = True
                            break
                    if worktree_exists:
                        break
            except subprocess.CalledProcessError:
                pass

        if chat_type == "new-issue":
            stage = "chat_waiting_worktree" if not worktree_exists else "chat_ready"
            next_action = (
                "AI 判断价值 → 创建工位 feature/raw-{ts}-{slug}（wt-create 自动 materialize）"
                if not worktree_exists
                else "工位已存在，chat 应已同步到 worktree docs/issues/"
            )
            incomplete = ["chat_unconsumed"]
        elif chat_type == "chat-message":
            # chat-message with conversation_id=0 or NULL shouldn't normally appear
            # (auto-updated to own id), but handle defensively
            stage = "chat_conversation_pending"
            next_action = "AI 判断 → 关联到现有对话或标记为单条消息处理"
            incomplete = ["chat_unconsumed"]
        else:
            # Check if the target issue exists (for comments, the issue may not exist yet)
            target_issue_dir = project / "docs" / "issues" / issue_id if issue_id else None
            issue_exists = target_issue_dir and target_issue_dir.is_dir() if target_issue_dir else False
            stage = "chat_comment_pending"
            if worktree_exists:
                next_action = f"AI 在对应工位追加评论到 docs/issues/{issue_id}/issue.md → chat-inbox consume"
                incomplete = ["chat_unconsumed"]
            elif not issue_exists:
                next_action = f"目标 issue {issue_id} 不存在——需先创建工位和 raw issue，评论才能消费"
                incomplete = ["chat_unconsumed", "target_issue_missing"]
            else:
                next_action = f"无工位：等待工位创建后同步评论到 docs/issues/{issue_id}/"
                incomplete = ["chat_unconsumed"]

        # Convert bare-numeric DB id to ISO key for system-wide compatibility
        bare_id = str(chat["id"])
        iso_key = f"{bare_id[:8]}T{bare_id[8:]}Z" if len(bare_id) == 14 and bare_id.isdigit() else bare_id
        items.append({
            "source_family": "chat-inbox",
            "key": iso_key,
            "stage": stage,
            "chat_type": chat_type,
            "issue_id": issue_id,
            "worktree_exists": worktree_exists,
            "incomplete": incomplete,
            "ready": worktree_exists,
            "next_action": next_action,
            "message_preview": msg,
            "issue_exists": issue_exists if chat_type == "comment" else None,
        })
    return items


# ── Full lifecycle chain trace ──────────────────────────
# The invariant key (YYYYMMDDTHHMM[SS]Z or YYYYMMDD-HHMM[SS]) flows through every station:
#   raw-{key} → {key}--* (B1 dir) → C-{key}-* (candidate) → I-{key}-* (issue)
#   → M-* (milestone) → branch → platform → closeout

CHAIN_STATIONS = [
    # (station_name, description, what_to_check)
    ("raw_created",     "raw-{key} 创建",         "docs/issues/raw-{key}/issue.md"),
    ("b1_dir",          "B1 预研目录",             "docs/pre-brainstorms/{key}--*/"),
    ("b1_brainstorm",   "B1 brainstorms.md",      "brainstorms.md in B1 dir"),
    ("b1_candidate",    "B1 candidates.md",        "candidates.md with entries"),
    ("candidate_decision", "C-{key} 决策",         "candidate status: promoted|absorbed|dropped"),
    ("i_created",       "I-{key} 创建",            "docs/issues/I-{key}-*/issue.md"),
    ("b2_design",       "B2 epic/design docs",     "canonical_issue_path → epic/"),
    ("b2_phase_done",   "B2 phase done_b2_ibm",   "I-*.phase_state >= done_b2_ibm"),
    ("dev_worktree",    "开发工位",                 "branch containing {key}"),
    ("dev_phase_in",    "phase in_dev",            "I-*.phase_state >= in_dev"),
    ("dev_phase_done",  "phase done/completed",    "I-*.phase_state in DONE_STATES"),
    ("code_review",     "code-review 证据",         "code-reviews/*.md in epic"),
    ("platform_create", "平台 issue 创建",          "platform_ids has values"),
    ("merged_develop",  "merge 到 develop",         "branch merged to develop"),
    ("platform_close",  "平台 issue 关闭",          "GitHub/Gitee CLOSED"),
    ("branch_deleted",  "分支删除",                 "branch no longer exists"),
    ("worktree_retired","工位退役",                 "worktree removed"),
]

def _all_base_keys(project: Path, raw_key_filter: str = "") -> set[str]:
    """Collect base keys from true origins only.

    When raw_key_filter is set, only return that one key — used by --raw-key scan.
    """
    if raw_key_filter:
        return {raw_key_filter}

    keys = set()

    # Source 1: SQLite chat inbox (unconsumed new-issue entries)
    db_path = project / ".freely" / "freely.db"
    if db_path.is_file():
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            rows = conn.execute(
                "SELECT issue_id FROM chats WHERE consumed = 0 AND chat_type = 'new-issue'"
            ).fetchall()
            conn.close()
            for (issue_id,) in rows:
                if issue_id.startswith("raw-"):
                    keys.add(issue_id[4:])
        except Exception:
            pass

    # Source 2: Milestone committed_issues — extract parent keys from I-* entries.
    # Once a key is discovered (from any source), the chain trace finds ALL
    # project artifacts matching that key: raw dirs, I-* dirs, B1 dirs,
    # branches, platform issues. The milestone is where active I-* items
    # that predate chat_inbox are tracked.
    mf = project / "docs" / "milestones.md"
    if mf.is_file():
        for m in re.finditer(r'I-(\d{8}[-T]\d{4,6}Z?)-[A-Z]', mf.read_text(encoding="utf-8")):
            keys.add(m.group(1))

    return keys


def scan_platform_issues(project: Path, platform_data: dict) -> list[dict]:
    """Scan platform data for OPEN issues containing raw-{key} or I-{key}.
    Uses pre-loaded batch data instead of per-item API calls.
    """
    items: list[dict] = []
    seen: set[str] = set()

    # ── GitHub (from batch data — zero API calls) ──
    for issue in platform_data.get("open_issues", []):
        title = issue.get("title", "")
        body = issue.get("body", "")
        number = str(issue.get("number", ""))
        combined = f"{title}\n{body}"
        raw_key = None
        for m in re.finditer(r"(?:^|\W)(raw-(\d{8}T\d{4,6}Z))", combined, re.MULTILINE):
            raw_key = m.group(2)
            break
        key = raw_key if raw_key else f"gh-{number}"
        if key not in seen:
            seen.add(key)
            items.append({
                "source_family": "platform",
                "key": key,
                "stage": "platform_open",
                "platform": "github",
                "issue_number": number,
                "title": title,
                "ready": True,
                "incomplete": [],
                "next_action": f"raw-issue-pull --raw-key {raw_key} ; wt-create --source platform --raw-key {raw_key}" if raw_key else f"issue-sync create raw-{number}",
                "next_station": "raw_created" if raw_key else "",
            })

    # ── Gitee ──
    try:
        gitee_py = str(Path(__file__).resolve().parent / "gitee-issue.py")
        if os.path.isfile(gitee_py):
            result = subprocess.run(
                [sys.executable, gitee_py, "list", "--state", "open", "--per-page", "50"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                issues = json.loads(result.stdout)
                for issue in issues:
                    title = issue.get("title", "")
                    body = issue.get("body", "")
                    number = str(issue.get("number", issue.get("id", "")))
                    combined = f"{title}\n{body}"
                    for m in re.finditer(r"(?:^|\W)(raw-(\d{8}T\d{4,6}Z))", combined, re.MULTILINE):
                        key = m.group(2)
                        if key not in seen:
                            seen.add(key)
                            items.append({
                                "source_family": "platform",
                                "key": key,
                                "stage": "platform_open",
                                "platform": "gitee",
                                "issue_number": number,
                                "title": title,
                                "ready": True,
                                "next_action": "wt-create --source platform --raw-key " + key,
                                "next_station": "raw_created",
                            })
    except Exception:
        pass

    return items


def _trace_chain(project: Path, key: str, platform_data: dict) -> dict:
    """Trace one key through all lifecycle stations.

    Returns dict with:
      - current_station: furthest reached
      - next_station: first missing or incomplete
      - stations: status of each station
      - blockers: what's preventing progress
    """
    stations = {}
    blockers = []

    # Station 0: raw-{key} created
    raw_dir = project / "docs" / "issues" / f"raw-{key}"
    raw_file = raw_dir / "issue.md" if raw_dir.is_dir() else None
    if raw_file and raw_file.is_file():
        fm = parse_frontmatter(raw_file.read_text(encoding="utf-8"))
        raw_status = fm.get("phase_state") or fm.get("status", "proposed")
        absorbed_into = fm.get("absorbed_into", "")
        stations["raw_created"] = {"reached": True, "status": raw_status, "absorbed_into": absorbed_into}
    else:
        # Raw file missing. If B1 or I-* children exist, the raw was once created
        # (key came from milestone or platform) — infer and continue tracing.
        i_dirs = list((project / "docs" / "issues").glob(f"I-{key}-*"))
        b1_dirs = list((project / "docs" / "pre-brainstorms").glob(f"{key}--*")) if (project / "docs" / "pre-brainstorms").is_dir() else []
        if i_dirs or b1_dirs:
            raw_status = "inferred"
            absorbed_into = ""
            # Check if any I-* child has terminal phase_state
            for i_dir in i_dirs:
                i_file = i_dir / "issue.md"
                if i_file.is_file():
                    cfm = parse_frontmatter(i_file.read_text(encoding="utf-8"))
                    cp = cfm.get("phase_state", "")
                    if cp in TERMINAL_CHILD:
                        raw_status = cp
                        absorbed_into = cfm.get("absorbed_into", "")
                        break
            note = "raw file missing" if raw_status == "inferred" else f"inferred from I-* child ({raw_status})"
            stations["raw_created"] = {"reached": True, "status": raw_status, "note": note}
        else:
            stations["raw_created"] = {"reached": False}
            blockers.append("raw_not_created")
            return _finalize_chain(key, stations, blockers, "raw_created", "raw_created")

    # Station 1: B1 pre-brainstorm directory
    # If raw is absorbed or dropped, B1 phase is complete regardless of directory existence
    raw_is_absorbed = raw_status in TERMINAL_RAW or raw_status in TERMINAL_CHILD
    pb_dirs = sorted((project / "docs" / "pre-brainstorms").glob(f"{key}--*")) if (project / "docs" / "pre-brainstorms").is_dir() else []
    b1_dir = pb_dirs[0] if pb_dirs else None

    if raw_is_absorbed:
        # Absorbed raw: B1 was completed before promotion, skip all B1 checks
        stations["b1_dir"] = {"reached": True, "note": "absorbed — B1 phase complete", "path": str(b1_dir.relative_to(project)) if b1_dir else ""}
        stations["b1_brainstorm"] = {"reached": True, "note": "absorbed"}
        stations["b1_candidate"] = {"reached": True, "note": "absorbed"}
        stations["candidate_decision"] = {"reached": True, "note": "absorbed"}
    elif b1_dir:
        stations["b1_dir"] = {"reached": True, "path": str(b1_dir.relative_to(project))}
    else:
        stations["b1_dir"] = {"reached": False}
        blockers.append("b1_dir_missing")
        return _finalize_chain(key, stations, blockers, "raw_created", "b1_dir")

    # Station 2-4: B1 brainstorm / candidates / decision
    if not raw_is_absorbed:
        brainstorm_file = b1_dir / "brainstorms.md" if b1_dir else None
        if brainstorm_file and brainstorm_file.is_file():
            stations["b1_brainstorm"] = {"reached": True}
        else:
            stations["b1_brainstorm"] = {"reached": False}
            blockers.append("b1_brainstorm_missing")
            return _finalize_chain(key, stations, blockers, "b1_dir", "b1_brainstorm")

        candidates_file = b1_dir / "candidates.md" if b1_dir else None
        candidate_entries = []
        all_terminal = True
        if candidates_file and candidates_file.is_file():
            sections = _parse_h3_sections(candidates_file)
            for s in sections:
                c_status = s.get("status") or s.get("candidate_status", "")
                candidate_entries.append({
                    "id": s.get("_section_title", "?"),
                    "status": c_status,
                })
                if c_status not in TERMINAL_CANDIDATE:
                    all_terminal = False
        # b1_candidate reached if candidates file has entries (even if all terminal)
        if candidate_entries:
            stations["b1_candidate"] = {"reached": True, "entries": candidate_entries}
        else:
            stations["b1_candidate"] = {"reached": False}
            blockers.append("b1_candidate_missing")
            return _finalize_chain(key, stations, blockers, "b1_brainstorm", "b1_candidate")

        c_entries = candidate_entries
        decided = [c for c in c_entries if c.get("status") in ("promoted", "absorbed", "dropped")]
        if decided:
            stations["candidate_decision"] = {"reached": True, "entries": c_entries}
        else:
            stations["candidate_decision"] = {"reached": True, "pending": True}
            blockers.append("candidate_not_decided")
            return _finalize_chain(key, stations, blockers, "b1_candidate", "candidate_decision")

    # Station 5: I-{key}-* created — try both format variants
    variants = _normalize_key_variants(key)
    i_dirs = []
    for v in variants:
        i_dirs.extend(sorted((project / "docs" / "issues").glob(f"I-{v}-*")))
    # Deduplicate (same dir matched by multiple variants)
    seen = set()
    i_dirs = [d for d in i_dirs if not (d.name in seen or seen.add(d.name))]
    i_children = []
    for i_dir in i_dirs:
        i_file = i_dir / "issue.md"
        if i_file.is_file():
            fm = parse_frontmatter(i_file.read_text(encoding="utf-8"))
            i_children.append({
                "id": i_dir.name,
                "phase_state": fm.get("phase_state", ""),
                "status": fm.get("status", ""),
                "canonical": fm.get("canonical_issue_path", ""),
                "platform_ids": _extract_platform_ids(fm),
            })

    # Dropped/completed raw: terminal, no further action needed
    if raw_status in ("dropped", "completed"):
        return _finalize_chain(key, stations, blockers, "dropped_complete", None)

    # Absorbed raw: chain may be complete, but cross-validate with children.
    # Don't let a single absorbed flag suppress active children or missing targets.
    if raw_is_absorbed:
        if absorbed_into:
            target_dir = project / "docs" / "issues" / absorbed_into
            if (target_dir / "issue.md").is_file():
                target_fm = parse_frontmatter((target_dir / "issue.md").read_text(encoding="utf-8"))
                target_phase = target_fm.get("phase_state", "")
                if target_phase in DONE_STATES or target_phase == COMPLETED or target_phase in TERMINAL_CHILD:
                    # Target is done — absorption is fully resolved.
                    stations["i_created"] = {"reached": True, "note": f"absorbed into {absorbed_into} (done)"}
                    if i_children:
                        stations["i_created"]["children"] = i_children
                    return _finalize_chain(key, stations, blockers, "absorbed_complete", None)
                else:
                    # Target exists but is NOT done — surface the inconsistency.
                    blockers.append(f"absorbed_target_not_done:{absorbed_into}={target_phase}")
                    if i_children:
                        stations["i_created"] = {"reached": True, "children": i_children}
                        # Continue tracing children normally — they carry the real lifecycle.
                    else:
                        stations["i_created"] = {"reached": False}
                        return _finalize_chain(key, stations, blockers, "candidate_decision", "i_created")
            else:
                blockers.append("absorbed_target_missing")
                stations["i_created"] = {"reached": False}
                return _finalize_chain(key, stations, blockers, "candidate_decision", "i_created")
        else:
            # Absorbed without target — don't assume terminal.
            # If I-* children exist, they carry the real lifecycle. Trace them.
            if not i_children:
                blockers.append("absorbed_no_target_no_children")
                stations["i_created"] = {"reached": False}
                return _finalize_chain(key, stations, blockers, "candidate_decision", "i_created")
            # Has children — fall through to normal tracing below.
            stations["i_created"] = {"reached": True, "children": i_children, "note": "raw=absorbed but children exist — tracing children"}

    if i_children:
        stations["i_created"] = {"reached": True, "children": i_children}
    else:
        stations["i_created"] = {"reached": False}
        blockers.append("i_not_created")
        return _finalize_chain(key, stations, blockers, "candidate_decision", "i_created")

    # ── Phase 4-6: Post-B1 stations ──
    best_child = _best_child(i_children)
    canonical = best_child.get("canonical", "")
    phase = best_child.get("phase_state", "")
    pids = best_child.get("platform_ids", {})

    branches = _find_all_branches_for_key(project, key)
    worktrees = _find_worktrees_for_key(project, key)
    has_worktree = len(worktrees) > 0  # physical worktree dir, not just branch ref
    # Check merge status of each branch individually — any unmerged branch
    # is a signal worth surfacing, not a false positive to suppress.
    branch_statuses = {}
    any_merged = False
    for b in branches:
        b_merged = _branch_merged_to_develop(project, b)
        branch_statuses[b] = b_merged
        if b_merged:
            any_merged = True

    # Check every station. Each call: (name, reached, required, detail_dict)
    _st = lambda name, reached, required, **kw: stations.update({name: {"reached": reached, "required": required, **kw}})

    # dev_worktree reached if: worktree exists now, OR was merged OR phase_state proves implementation happened
    dev_wt_reached = has_worktree or any_merged or (not has_worktree and (phase in DONE_STATES or phase in ACTIVE_B2 or phase in TERMINAL_CHILD))
    _st("dev_worktree", dev_wt_reached, True,
        branches=branch_statuses if branch_statuses else None,
        branch_hint="已退役" if not has_worktree else None)

    _st("dev_phase_done", phase in DONE_STATES or phase in TERMINAL_CHILD, True, phase=phase or "empty")

    # Optional: code review evidence (not all issues need formal review)
    has_cr = False
    if canonical:
        ep = (project / canonical).parent if (project / canonical).is_file() else project / canonical
        crd = ep / "code-reviews" if ep.is_dir() else None
        has_cr = crd and crd.is_dir() and any(crd.iterdir()) if crd else False
    _st("code_review", has_cr, False, canonical=canonical)

    _st("platform_create", bool(pids.get("github")) or bool(pids.get("gitee")), True, pids=pids)

    # merged_develop: when branches exist, trust their merge status (at least
    # one merged = reached). When no branches exist, infer from phase_state.
    if has_worktree:
        merged_reached = any_merged
    else:
        merged_reached = phase in DONE_STATES or phase in ACTIVE_B2 or phase in TERMINAL_CHILD
    _st("merged_develop", merged_reached, True,
        branches=branch_statuses if branch_statuses else None,
        reason=("at least one branch merged" if any_merged else
                "no branch merged to develop" if has_worktree else
                "branches deleted — inferred from phase_state"))

    # Platform close (best-effort check from batch data)
    gh_issue = pids.get("github", "")
    gh_closed = _is_github_closed_lookup(gh_issue, platform_data) if gh_issue else None
    _st("platform_close", gh_closed is True, True, github_issue=gh_issue, gh_closed=gh_closed)

    # branch_deleted: reached when no branches remain for this key.
    # If branches exist (even stale ones), surface them so the user can decide.
    branch_existed = any_merged or (not has_worktree and phase in DONE_STATES.union(ACTIVE_B2))
    _st("branch_deleted", not has_worktree and branch_existed, True,
        branches=branch_statuses if branch_statuses else None)

    # Optional: milestone entry
    mf = project / "docs" / "milestones.md"
    in_milestone = key in mf.read_text(encoding="utf-8") if mf.is_file() else False
    _st("milestone_entry", in_milestone, False)

    # Determine current/next from mandatory stations in order
    mandatory_order = [
        "raw_created", "b1_dir", "b1_brainstorm", "b1_candidate", "candidate_decision",
        "i_created", "dev_worktree", "dev_phase_done", "platform_create",
        "merged_develop", "platform_close", "branch_deleted",
    ]
    current = "raw_created"
    next_station = None
    for st in mandatory_order:
        s = stations.get(st, {})
        if s.get("reached"):
            current = st
        elif next_station is None:
            next_station = st
            if s.get("required", True):
                blockers.append(f"{st}_missing")

    return _finalize_chain(key, stations, blockers, current, next_station)


def _best_child(children: list[dict]) -> dict:
    """Pick the most advanced I-* child by phase_state."""
    phase_order = {"": 0, "in_b2_ibm": 1, "done_b2_ibm": 2, "in_dev": 3, "blocked_dev": 3, "done": 4, "done_ibm": 4, "in_verification": 5, "completed": 6}
    best = children[0] if children else {}
    for c in children[1:]:
        if phase_order.get(c.get("phase_state", ""), 0) > phase_order.get(best.get("phase_state", ""), 0):
            best = c
    return best


def _normalize_key_variants(key: str) -> list[str]:
    """Return all format variants of a date-time key for cross-format matching.

    Old format:    YYYYMMDD-HHMM    (e.g. 20260503-0915)
    Old w/ secs:   YYYYMMDD-HHMMSS  (e.g. 20260503-091530)
    New format:    YYYYMMDDTHHMM[SS]Z (e.g. 20260503T0915Z or 20260503T091530Z)
    Bare:          YYYYMMDDHHMMSS   (e.g. 20260430222144)

    Returns [key] plus any reasonable variants so substring matches work
    across format migration boundaries (old↔new, bare↔new, with/without seconds).
    """
    variants = [key]
    # Old → New: 20260503-0915 → 20260503T0915Z, 20260503-091530 → 20260503T091530Z
    m = re.match(r'^(\d{8})-(\d{4,6})$', key)
    if m:
        variants.append(f"{m.group(1)}T{m.group(2)}Z")
        return variants
    # New → Old: 20260503T0915Z → 20260503-0915, 20260503T091530Z → 20260503-091530
    m = re.match(r'^(\d{8})T(\d{4,6})Z$', key)
    if m:
        variants.append(f"{m.group(1)}-{m.group(2)}")
        return variants
    # Bare → New: 20260430222144 → 20260430T222144Z
    m = re.match(r'^(\d{8})(\d{6})$', key)
    if m:
        variants.append(f"{m.group(1)}T{m.group(2)}Z")
    return variants


def _find_all_branches_for_key(project: Path, key: str) -> list[str]:
    """Find ALL git branches containing this key (multiple branches sharing
    a key is correct — each branch serves a specific purpose for the same issue).
    Tries both old and new format variants for cross-format matching."""
    variants = _normalize_key_variants(key)
    branches = []
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(project), "branch", "--format=%(refname:short)"],
            text=True, stderr=subprocess.DEVNULL,
        )
        for line in raw.splitlines():
            for v in variants:
                if v in line.strip():
                    branches.append(line.strip())
                    break
    except subprocess.CalledProcessError:
        pass
    return branches


def _find_worktrees_for_key(project: Path, key: str) -> list[str]:
    """Find actual git worktree directories containing this key.
    Unlike _find_all_branches_for_key, this only checks physical worktree
    directories (git worktree list), not branches that may exist without
    a worktree directory."""
    variants = _normalize_key_variants(key)
    worktrees = []
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(project), "worktree", "list", "--porcelain"],
            text=True, stderr=subprocess.DEVNULL,
        )
        for line in raw.splitlines():
            if line.startswith("branch refs/heads/"):
                branch = line.replace("branch refs/heads/", "").strip()
                for v in variants:
                    if v in branch:
                        worktrees.append(branch)
                        break
    except subprocess.CalledProcessError:
        pass
    return worktrees


def _parse_h3_sections(path: Path) -> list[dict]:
    """Parse #, ## and ### sections from a markdown file, extracting key-value fields.

    candidates.md uses #/## for candidate entries (with status/priority/scope fields)
    and ### for subsections. All three levels must be parsed to find promoted/absorbed/dropped.
    Older candidates use flat `# Title` format; newer ones use `##`/`###` sections.
    """
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^(?:#{1,3})\s+(.+)$", text, flags=re.MULTILINE)
    sections = []
    for idx in range(1, len(parts), 2):
        title = parts[idx].strip()
        body = parts[idx + 1]
        fields = {}
        for line in body.splitlines():
            m = re.match(r"^-\s+([A-Za-z0-9_]+):\s*(.*)$", line.strip())
            if m:
                key, value = m.groups()
                fields[key] = value.strip().strip("`").strip('"').strip("'")
                fields.setdefault(key.lower().replace(" ", "_"), fields[key])
        if fields:
            fields["_section_title"] = title
            sections.append(fields)
    return sections


def _finalize_chain(key: str, stations: dict, blockers: list[str], current: str, next_station: str | None) -> dict:
    """Package chain trace result including optional station status."""
    advisory = []
    # Collect optional stations that are not reached
    for st_name, st_info in stations.items():
        if not st_info.get("required", True) and not st_info.get("reached"):
            advisory.append(f"{st_name}_missing")
    return {
        "key": key,
        "current_station": current,
        "next_station": next_station,
        "stations": stations,
        "blockers": blockers,
        "advisory": advisory,
        "complete": len(blockers) == 0 and current in ("branch_deleted", "absorbed_complete", "dropped_complete"),
    }


# ── Branch / worktree governance scan ───────────────────

def _is_protected_branch(branch: str) -> bool:
    """Permanent branches exempt from issue-key naming convention."""
    if branch in ("main", "develop"):
        return True
    if branch.startswith(("refs/tags/", "release/", "test-pre-merge-")):
        return True
    return False


def _extract_issue_key_from_branch(branch: str) -> str | None:
    """Extract raw-xxx or I-xxx key from branch name.
    feature/raw-20260428-1737-foo → raw-20260428-1737
    feature/raw-20260504T1132Z-foo → raw-20260504T1132Z
    hotfix/I-20260428-1737-A-bar → I-20260428-1737-A
    test-pre-merge-scan-v3 → None (no issue key)
    """
    for pattern in [r"(raw-\d{8}[-T]\d{4,6}Z?)", r"(I-\d{8}[-T]\d{4,6}Z?(?:-[A-Z0-9]+)?)"]:
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


def _pending_comments_for_key(project: Path, key: str) -> int:
    """Count unconsumed comments in chats table targeting raw-{key} or I-{key}-*."""
    db_path = project / ".freely" / "freely.db"
    if not db_path.is_file():
        return 0
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        # Match raw-{key} exactly, or I-{key}-* pattern, or any issue_id containing the key
        count = conn.execute(
            "SELECT COUNT(*) FROM chats WHERE consumed = 0 AND chat_type = 'comment' AND (issue_id = ? OR issue_id LIKE ?)",
            (f"raw-{key}", f"I-{key}-%")
        ).fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0


def scan_chain_trace(project: Path, platform_data: dict, raw_key_filter: str = "") -> list[dict]:
    """Trace the full lifecycle chain for every unique base key.

    Returns one item per key with:
      - current_station: furthest reached station
      - next_station: first missing/incomplete station
      - blockers: what's preventing progress
      - ready: whether the item can be worked on (past candidate_decision)
      - paths: file paths for quick location (raw_file, b1_dir, i_files)
      - pending_comments: count of unconsumed comments for this key
    """
    keys = _all_base_keys(project, raw_key_filter=raw_key_filter)
    results = []
    for key in sorted(keys):
        trace = _trace_chain(project, key, platform_data)
        if trace["complete"]:
            continue  # fully closed — silent
        # Detect actual worktree existence for this key
        wt_branches = _find_worktrees_for_key(project, key)
        has_actual_wt = len(wt_branches) > 0
        # Collect file paths from station data for quick location
        paths = _collect_paths(key, trace["stations"], project)
        # Check for unconsumed comments targeting this issue
        pending = _pending_comments_for_key(project, key)
        # Pick worktree-aware next_action template
        current_station = trace["current_station"]
        wt_suffixed_stages = {"b1_dir", "b1_brainstorm", "dev_worktree"}
        if current_station in wt_suffixed_stages and not has_actual_wt:
            wt_key = current_station + "_no_wt"
            next_action = CHAIN_ACTIONS.get(wt_key, "").replace("{key}", key) if wt_key in CHAIN_ACTIONS else ""
        else:
            next_action = _derive_chain_action(current_station, trace["next_station"], trace["blockers"], key)
        results.append({
            "key": key,
            "stage": current_station,
            "next_station": trace["next_station"],
            "blockers": trace["blockers"],
            "ready": current_station not in ("raw_created", "b1_dir", "b1_brainstorm", "b1_candidate", "candidate_decision"),
            "next_action": next_action,
            "stations": {k: v for k, v in trace["stations"].items() if v.get("reached")},
            "paths": paths,
            "pending_comments": pending,
        })
    return results


CHAIN_ACTIONS = {
    "raw_created": "[manager] wt-create --raw-key {key} --source platform --skill freely-fix-execution --slug b1\n[worker] skill:freely-doc-B1_IBM-execution → brainstorms.md → candidates.md",
    "b1_dir": "[worker] skill:freely-doc-B1_IBM-execution → 工位已存在，写入 brainstorms.md",
    "b1_dir_no_wt": "[manager] wt-create --raw-key {key} --source local --skill freely-fix-execution --slug b1\n[worker] skill:freely-doc-B1_IBM-execution → 写入 brainstorms.md",
    "b1_brainstorm": "[worker] skill:freely-doc-B1_IBM-execution → 工位已存在，产出 candidates.md",
    "b1_brainstorm_no_wt": "[manager] wt-create --raw-key {key} --source local --skill freely-fix-execution --slug b1\n[worker] skill:freely-doc-B1_IBM-execution → 产出 candidates.md",
    "b1_candidate": "[worker] skill:freely-candidate-acceptance-review → 决策 promote/absorb/drop",
    "candidate_decision": "[manager] wt-create --raw-key {key} --source platform --skill freely-feat-execution --slug impl\n[worker] skill:freely-feat-execution → materialize I-* → dev-loop",
    "i_created": "[manager] wt-create --raw-key {key} --source platform --skill freely-feat-execution --slug impl\n[worker] skill:freely-dev-loop-execution → 推进 phase_state",
    "dev_worktree": "[worker] skill:freely-dev-loop-execution → 工位已存在，推进 phase_state",
    "dev_worktree_no_wt": "[manager] wt-create --raw-key {key} --source local --skill freely-fix-execution --slug work\n[worker] skill:freely-dev-loop-execution → 推进 phase_state",
    "dev_phase_done": "[worker] skill:freely-dev-loop-execution → issue-sync create → git commit → wt-close",
    "platform_create": "[manager] wt-create --raw-key {key} --source platform --skill freely-fix-execution --slug sync\n[worker] issue-sync create → git commit → wt-close",
    "merged_develop": "[manager] wt-create --raw-key {key} --source platform --skill freely-fix-execution --slug close\n[worker] issue-sync close → wt-close",
    "platform_close": "[manager] freely feedback --repo chatterzhao/freely --title \"Close platform issue: {key}\" --body \"Close the platform issue corresponding to the locally completed issue {key}.\"\n  → 拿到 raw-{key} → wt-create --raw-key {key} --source platform --skill freely-fix-execution --slug close\n[worker] issue-sync close → git commit → wt-close",
    "branch_deleted": "[manager] freely feedback --repo chatterzhao/freely --title \"Sync close after branch deletion: {key}\" --body \"Sync and close the platform issue for {key} after local branch has been deleted.\"\n  → 拿到 raw-{key} → wt-create --raw-key {key} --source platform --skill freely-fix-execution --slug sync\n[worker] issue-sync close → git commit → wt-close",
}


def add_platform_sync_batch(items: list[dict], ts: str, project: Path) -> list[dict]:
    """Collect platform sync items into one batch entry.

    Stages that belong to platform_sync_batch:
      - platform_open: platform has an issue not yet in local
      - platform_only: platform issue with raw key but no local raw
      - state_mismatch: local and platform states differ
      - local_only: local issue not yet on platform

    Removes individual items and creates a single batch item as the
    first (highest priority) result. Uses cross-scan dedup: if the
    same set of sync items was already batched, produces a noop entry
    instead of a new actionable batch.
    """
    sync_stages = {"platform_open", "platform_only", "state_mismatch", "local_only", "platform_close", "branch_deleted"}
    sync_items = [it for it in items if it.get("stage") in sync_stages]
    remaining = [it for it in items if it.get("stage") not in sync_stages]

    if not sync_items:
        return items

    pull_count = sum(1 for it in sync_items if it.get("stage") in ("platform_open", "platform_only"))
    push_count = sum(1 for it in sync_items if it.get("stage") == "local_only")
    reconcile_count = sum(1 for it in sync_items if it.get("stage") == "state_mismatch")
    close_count = sum(1 for it in sync_items if it.get("stage") in ("platform_close", "branch_deleted"))
    comment_count = sum(1 for it in sync_items if it.get("stage") == "pending_comments")
    total_sync = pull_count + push_count + reconcile_count + close_count

    # Cross-scan dedup: compare fingerprint of this batch vs previous
    sync_keys = sorted([it.get("key", "") for it in sync_items])
    fingerprint = json.dumps({"keys": sync_keys, "total": total_sync}, sort_keys=True)
    state_dir = project / ".freely" / "run"
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
        "stage": "platform_sync_batch",
        "source_family": "platform_sync",
        "ready": not noop,
        "priority": "P0_highest",
        "incomplete": [] if not noop else ["noop"],
        "noop": noop,
        "sync_summary": {
            "total": total_sync,
            "pull": pull_count,
            "push": push_count,
            "reconcile_state": reconcile_count,
            "close": close_count,
            "pending_comments": comment_count,
            "platforms": ["github", "gitee"],
        },
    }

    if not noop:
        batch_item["next_action"] = (
            f"[manager] freely feedback --repo chatterzhao/freely --title \"Platform sync batch: sync {total_sync} items\" --body \"Batch sync task discovered by scan.\\npull={pull_count} push={push_count} reconcile={reconcile_count} close={close_count}\\nplatforms: github, gitee\"\n"
            "  → 拿到 raw-{{real_key}} → wt-create --raw-key {{real_key}} --source platform --skill freely-fix-execution --slug platform-sync\n"
            "[worker] issue-sync batch → git commit → wt-close"
        )

    return [batch_item] + remaining


def _derive_chain_action(current: str, next_station: str | None, blockers: list[str], key: str = "") -> str:
    template = ""
    if current in CHAIN_ACTIONS:
        template = CHAIN_ACTIONS[current]
    elif next_station and next_station in CHAIN_ACTIONS:
        template = CHAIN_ACTIONS[next_station]
    elif blockers:
        return f"解决阻塞: {', '.join(blockers)}"
    else:
        return ""
    # Substitute {key} placeholder with actual key value
    if key and "{key}" in template:
        template = template.replace("{key}", key)
    return template


def _collect_paths(key: str, stations: dict, project: Path) -> dict:
    """Extract file paths from station data so scan output includes location info."""
    paths = {}
    # Raw issue
    raw_dir = project / "docs" / "issues" / f"raw-{key}"
    if (raw_dir / "issue.md").is_file():
        paths["raw_file"] = str((raw_dir / "issue.md").relative_to(project))
    # B1 directory
    b1_info = stations.get("b1_dir", {})
    if b1_info.get("path"):
        paths["b1_dir"] = b1_info["path"]
    # I-* issue files
    i_dirs = sorted((project / "docs" / "issues").glob(f"I-{key}-*"))
    if i_dirs:
        paths["i_files"] = [str((d / "issue.md").relative_to(project)) for d in i_dirs if (d / "issue.md").is_file()]
    return paths
    return "收口完成"


def scan_worktree_governance(project: Path) -> list[dict]:
    """Scan branches and worktrees for naming convention and cleanup.

    Principle (no exceptions):
    - main/develop/tags are permanent — excluded
    - ALL other branches MUST contain raw-xxx or I-xxx in the name
    - If no issue key → 命名不规范，需重命名
    - If issue key found → check if issue done → 未收口
    - If issue not done → skip (covered by lifecycle chain trace)
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

    worktrees: dict[str, dict] = {}
    current_wt = None
    for line in raw.splitlines():
        if line.startswith("worktree "):
            current_wt = line[9:]
            worktrees[current_wt] = {"path": current_wt, "branch": None}
        elif line.startswith("branch ") and current_wt:
            branch_ref = line[7:]
            if branch_ref.startswith("refs/heads/"):
                worktrees[current_wt]["branch"] = branch_ref[11:]

    try:
        branches_raw = subprocess.check_output(
            ["git", "-C", str(project), "branch", "--format=%(refname:short)"],
            text=True, stderr=subprocess.DEVNULL,
        )
        all_branches = [b.strip() for b in branches_raw.splitlines() if b.strip()]
    except subprocess.CalledProcessError:
        all_branches = []

    worktree_by_branch: dict[str, dict] = {}
    project_wt_path = str(project.resolve())
    for wt_path, wt_info in worktrees.items():
        branch = wt_info.get("branch")
        if branch:
            worktree_by_branch[branch] = wt_info

    for branch in all_branches:
        if _is_protected_branch(branch):
            continue

        issue_key = _extract_issue_key_from_branch(branch)
        wt_info = worktree_by_branch.get(branch, {})
        wt_path = wt_info.get("path", "")
        wt_path_obj = Path(wt_path) if wt_path else None

        if wt_path and str(Path(wt_path).resolve()) == project_wt_path:
            continue

        is_dirty = _worktree_dirty(wt_path_obj) if wt_path_obj else False
        merged_to_develop = _branch_merged_to_develop(project, branch)

        # Check worktree directory name too
        wt_dir_ok = True
        if wt_path_obj:
            wt_dir_name = wt_path_obj.name
            if issue_key:
                wt_dir_ok = issue_key.replace("raw-", "") in wt_dir_name or issue_key in wt_dir_name
            # If no issue_key, wt_dir_ok stays True (flagging branch name is enough)

        if not issue_key:
            incomplete = ["branch_name_no_issue_key"]
            if not wt_dir_ok:
                incomplete.append("worktree_dir_name_no_issue_key")
            items.append({
                "source_family": "worktree_governance",
                "key": branch,
                "branch": branch,
                "worktree_path": wt_path or "无工位",
                "issue_key": None,
                "stage": "命名不规范",
                "dirty": is_dirty,
                "merged_to_develop": merged_to_develop,
                "incomplete": incomplete,
                "next_action": "确定对应 issue → git branch -m 重命名为 feature/raw-{ts}-{slug} 格式",
                "ready": False,
            })
            continue

        # Has issue key: check if issue is done
        if not _issue_is_done(project, issue_key):
            continue  # not done → lifecycle chain trace covers it

        incomplete = []
        if is_dirty:
            incomplete.append("worktree_dirty")
        if merged_to_develop is False:
            incomplete.append("branch_not_merged_to_develop")
        if not incomplete and merged_to_develop:
            incomplete.append("ready_to_retire")

        items.append({
            "source_family": "worktree_governance",
            "key": branch,
            "branch": branch,
            "worktree_path": wt_path or "无工位",
            "issue_key": issue_key,
            "stage": "未收口",
            "dirty": is_dirty,
            "merged_to_develop": merged_to_develop,
            "incomplete": incomplete,
            "next_action": _derive_governance_action(is_dirty, merged_to_develop),
            "ready": not is_dirty,
        })

    return items


def _derive_governance_action(dirty: bool, merged: bool | None) -> str:
    if dirty:
        return "提交或丢弃 dirty 修改 → merge 到 develop → 退役工位 → 删分支"
    if merged is False:
        return "merge 到 develop → 退役工位 → 删分支"
    return "已 merge，退役工位并删除分支"


def _matches_raw_key_filter(item: dict, raw_key: str) -> bool:
    """Check if an item belongs to the specified raw_key."""
    # Direct key match
    if item.get("key") == raw_key:
        return True
    # raw_id match (raw_id = "raw-20260518T040847Z")
    rid = item.get("raw_id", "")
    if rid.startswith("raw-") and rid[4:] == raw_key:
        return True
    # platform items store key as gh-{number}, match via raw_id
    return False


# ── Remote branch governance scan ─────────────────────

def _configured_remotes(project: Path) -> list[str]:
    """Return list of configured git remotes (github, gitee, etc.)."""
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(project), "remote"], text=True, stderr=subprocess.DEVNULL
        )
        return [r.strip() for r in raw.splitlines() if r.strip()]
    except subprocess.CalledProcessError:
        return []


def _remote_branches(project: Path, remote: str) -> list[dict]:
    """List branches on a remote, excluding main/develop."""
    try:
        raw = subprocess.check_output(
            ["git", "ls-remote", "--heads", remote], text=True, stderr=subprocess.DEVNULL, cwd=str(project)
        )
    except subprocess.CalledProcessError:
        return []
    branches = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        ref = parts[1]
        name = ref.replace("refs/heads/", "")
        if name in ("main", "develop"):
            continue
        branches.append({"name": name, "sha": parts[0], "remote": remote})
    return branches


def scan_remote_branch_governance(project: Path) -> list[dict]:
    """Scan remote branches for governance gaps.

    Checks each remote (github, gitee, etc.):
      - If branch is merged to develop → ready_to_delete
      - If branch has issue key and issue is done → stale (unmerged)
      - If branch has no issue key → 命名不规范
    """
    items = []
    remotes = _configured_remotes(project)
    for remote in remotes:
        for rb in _remote_branches(project, remote):
            branch = rb["name"]
            issue_key = _extract_issue_key_from_branch(branch)
            merged_to_develop = _branch_merged_to_develop(project, branch)

            if merged_to_develop:
                items.append({
                    "source_family": "remote_branch_governance",
                    "key": f"{remote}/{branch}",
                    "remote": remote,
                    "branch": branch,
                    "stage": "已合并未清理",
                    "issue_key": issue_key,
                    "merged_to_develop": True,
                    "incomplete": ["remote_branch_not_deleted"],
                    "ready": True,
                    "next_action": f"删除远端分支: git push {remote} --delete {branch}",
                })
                continue

            # Not merged to develop
            if not issue_key:
                items.append({
                    "source_family": "remote_branch_governance",
                    "key": f"{remote}/{branch}",
                    "remote": remote,
                    "branch": branch,
                    "stage": "命名不规范",
                    "issue_key": None,
                    "merged_to_develop": False,
                    "incomplete": ["branch_name_no_issue_key"],
                    "ready": False,
                    "next_action": f"确定对应 issue → 重命名或删除远端分支 {remote}/{branch}",
                })
                continue

            # Has issue key, not merged — check if issue is done
            if _issue_is_done(project, issue_key):
                items.append({
                    "source_family": "remote_branch_governance",
                    "key": f"{remote}/{branch}",
                    "remote": remote,
                    "branch": branch,
                    "stage": "未收口",
                    "issue_key": issue_key,
                    "merged_to_develop": False,
                    "incomplete": ["remote_branch_not_merged", "issue_done_branch_stale"],
                    "ready": False,
                    "next_action": f"issue 已完成但分支未合并: 评估合入 develop 或删除 git push {remote} --delete {branch}",
                })

    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--json", action="store_true", default=True)
    parser.add_argument("--raw-key", default="", help="只扫描指定 raw key（如 20260518T040847Z），不传时全量扫描")
    args = parser.parse_args()
    project = Path(args.project).resolve()
    raw_key = args.raw_key
    # Strip raw- prefix if present
    if raw_key.startswith("raw-"):
        raw_key = raw_key[4:]
    payload = build_payload(project, raw_key=raw_key)
    json.dump(payload, sys.stdout, indent=2, sort_keys=True, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
