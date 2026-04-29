#!/usr/bin/env python3
"""task-lifecycle-scan: unified lifecycle-aware task scanner.

Replaces task-source-scan.py with cross-referenced, stage-aware scanning.
One item = one work item tracked through its full lifecycle (raw → B1 → I-* → B2 → done).

Output: JSON with lifecycle_stage, next_action, next_action_kind, ready_for_worker.
"""
from __future__ import annotations
import argparse, json, os, re, sys, subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

TERMINAL_PHASES = {"completed", "absorbed", "dropped", "delivered"}
TERMINAL_CANDIDATE = {"absorbed", "dropped", "promoted"}
ACTIVE_B2_PHASES = {"in_b2_ibm", "done_b2_ibm", "in_dev", "blocked_dev"}
VERIFYING_PHASES = {"in_verification"}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter fields without PyYAML dependency."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1]
    fields = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip().lstrip("-").strip()
        val = val.strip().strip("`").strip('"').strip("'")
        fields[key] = val
    return fields


def parse_markdown_fields(path: Path) -> dict:
    """Parse `- key: value` fields from markdown."""
    if not path.is_file():
        return {}
    fields = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            m = re.match(r"^- ([a-z_]+):\s*`?(.*?)`?\s*$", line)
            if m:
                fields[m.group(1)] = m.group(2).strip()
    return fields


def scan_all_items(project: Path) -> list[dict]:
    """Collect all work items from all sources."""
    items = []
    issues_dir = project / "docs" / "issues"
    b1_dir = project / "docs" / "pre-brainstorms"
    progress_dir = project / "docs" / "progress"
    milestones_file = project / "docs" / "milestones.md"

    # ── Raw issues ──
    if issues_dir.is_dir():
        for d in sorted(issues_dir.iterdir()):
            if not d.is_dir() or not d.name.startswith("raw-"):
                continue
            mf = d / "issue.md"
            if not mf.is_file():
                continue
            fm = parse_frontmatter(mf.read_text(encoding="utf-8"))
            status = fm.get("status", "proposed")
            if status in TERMINAL_PHASES:
                continue
            items.append({
                "item_id": d.name,
                "kind": "raw",
                "status": status,
                "phase_state": fm.get("phase_state", ""),
                "absorbed_into": fm.get("absorbed_into", ""),
                "platform_ids": _parse_platform_ids(fm),
                "raw_file": str(mf.relative_to(project)),
            })

    # ── Linked issues ──
    if issues_dir.is_dir():
        for d in sorted(issues_dir.iterdir()):
            if not d.is_dir() or not d.name.startswith("I-"):
                continue
            mf = d / "issue.md"
            if not mf.is_file():
                continue
            fm = parse_frontmatter(mf.read_text(encoding="utf-8"))
            phase = fm.get("phase_state", "")
            status = fm.get("status", "")
            if phase in TERMINAL_PHASES or (status in TERMINAL_PHASES and not phase):
                continue
            items.append({
                "item_id": d.name,
                "kind": "linked",
                "status": status,
                "phase_state": phase,
                "issue_title": fm.get("issue_title", ""),
                "promoted_from": fm.get("promoted_from", ""),
                "canonical_issue_path": fm.get("canonical_issue_path", ""),
                "platform_ids": _parse_platform_ids(fm),
                "raw_file": str(mf.relative_to(project)),
            })

    # ── Pre-brainstorms ──
    if b1_dir.is_dir():
        for d in sorted(b1_dir.iterdir()):
            if not d.is_dir():
                continue
            cf = d / "candidates.md"
            if not cf.is_file():
                # No candidate yet — B1 in progress
                bf = d / "brainstorms.md"
                items.append({
                    "item_id": d.name,
                    "kind": "pre_brainstorm",
                    "phase_state": "brainstorming",
                    "candidate_status": "",
                    "raw_file": str(d.relative_to(project)) + "/",
                })
                continue
            # Parse candidates
            fields = parse_markdown_fields(cf)
            c_status = fields.get("status", fields.get("candidate_status", "unspecified"))
            if c_status in TERMINAL_CANDIDATE:
                continue
            items.append({
                "item_id": d.name,
                "kind": "pre_brainstorm",
                "phase_state": "candidate",
                "candidate_status": c_status,
                "next_action": fields.get("next_action", ""),
                "raw_file": str(d.relative_to(project)) + "/",
            })

    # ── Milestone queue items ──
    if milestones_file.is_file():
        items.extend(_scan_milestones(milestones_file, issues_dir))

    # ── Progress items ──
    if progress_dir.is_dir():
        items.extend(_scan_progress(progress_dir))

    return items


def _parse_platform_ids(fm: dict) -> dict:
    """Extract platform IDs from frontmatter."""
    ids = {}
    for plat in ("github", "gitee"):
        key = f"platform_ids.{plat}.issue_id"
        # Simple extraction from raw frontmatter text
        ids[plat] = fm.get(f"{plat}_issue_id", "")
    return ids


def _scan_milestones(milestones_file: Path, issues_dir: Path) -> list[dict]:
    """Parse milestones.md for queue items not yet completed."""
    items = []
    if not milestones_file.is_file():
        return items
    text = milestones_file.read_text(encoding="utf-8")
    current_section = ""
    current_milestone = ""
    for line in text.splitlines():
        line = line.rstrip()
        if line.startswith("## "):
            current_milestone = line[3:].strip()
            continue
        if re.match(r"^###\s+(candidate_issues|committed_issues|completed_issues)", line):
            current_section = line.split()[0][3:]
            continue
        # Look for I-* references
        for m in re.finditer(r"`(I-\d{8}-\d{4}[A-Za-z0-9-]*)`", line):
            iid = m.group(1)
            # Skip if already captured from issues dir above
            if (issues_dir / iid).is_dir():
                continue
            if current_section == "completed_issues":
                continue
            items.append({
                "item_id": iid,
                "kind": "milestone_ref",
                "status": current_section,
                "phase_state": "",
                "raw_file": f"docs/milestones.md ({current_section})",
            })
    return items


def _scan_progress(progress_dir: Path) -> list[dict]:
    """Scan progress docs for non-terminal items."""
    items = []
    if not progress_dir.is_dir():
        return items
    for path in sorted(progress_dir.rglob("*.md")):
        fields = parse_markdown_fields(path)
        if not fields:
            continue
        phase = fields.get("phase_state", "")
        cstatus = fields.get("closure_status", "")
        naction = fields.get("next_action", "")
        if phase in TERMINAL_PHASES and (not naction or naction.lower() == "completed"):
            continue
        items.append({
            "item_id": fields.get("issue_id", path.stem),
            "kind": "progress",
            "phase_state": phase,
            "closure_status": cstatus,
            "runtime_state": fields.get("runtime_state", "unknown"),
            "next_action": naction,
            "raw_file": str(path.relative_to(progress_dir.parent)),
        })
    return items


# ── Stage resolution ────────────────────────────────────

def resolve_lifecycle_stage(item: dict) -> dict:
    """Determine lifecycle stage and next action for one item."""
    kind = item["kind"]
    phase = item.get("phase_state", "")
    status = item.get("status", "")
    cstatus = item.get("candidate_status", "")

    if kind == "raw":
        if item.get("absorbed_into"):
            return _stage("completed", "absorbed", "skip")
        return _stage("B1_proposed", phase or "proposed", "brainstorm",
                      next_action="Consume into B1_IBM pre-brainstorm: read the raw issue, research boundaries, produce a candidate.",
                      ready_for_worker=True)

    if kind == "pre_brainstorm":
        if phase == "brainstorming":
            return _stage("B1_brainstorming", "brainstorming", "brainstorm",
                          next_action="Continue B1 brainstorm: converge on scope, write candidates.md.",
                          ready_for_worker=True)
        if cstatus == "blocked":
            return _stage("B1_candidate", "blocked", "unblock",
                          next_action="Candidate is blocked. Resolve blocker or escalate.",
                          ready_for_worker=False)
        return _stage("B1_candidate", cstatus or "unspecified", "decision",
                      next_action="Decide: promote to I-* (create linked issue), absorb into existing, or drop.",
                      ready_for_worker=False, owner_hint="manager")

    if kind in ("linked", "milestone_ref"):
        if phase in ACTIVE_B2_PHASES:
            return _stage("B2_active", phase, "implementation",
                          next_action="Continue B2 implementation: follow dev-loop, update progress artifacts.",
                          ready_for_worker=True)
        if phase in VERIFYING_PHASES:
            return _stage("B2_verifying", phase, "closeout",
                          next_action="Close out verification: verify merge evidence, update phase_state to completed, close platform issues.",
                          ready_for_worker=True)
        if status == "completed" and not phase:
            return _stage("B2_verifying", "stale_completed", "closeout",
                          next_action="Phase_state missing but status=completed. Update phase_state to completed, close platform issues.",
                          ready_for_worker=True)
        if not phase and not status:
            return _stage("B2_active", "unknown", "investigate",
                          next_action="No phase_state or status. Read linked issue doc to determine current stage.",
                          ready_for_worker=False)
        # Default: treat as active
        return _stage("B2_active", phase or "unknown", "investigate",
                      next_action="Read linked issue doc to determine current stage and next step.",
                      ready_for_worker=False)

    if kind == "progress":
        if phase in ACTIVE_B2_PHASES:
            return _stage("B2_active", phase, "implementation",
                          next_action=item.get("next_action") or "Continue implementation.",
                          ready_for_worker=True)
        if phase in VERIFYING_PHASES:
            return _stage("B2_verifying", phase, "closeout",
                          next_action=item.get("next_action") or "Close out verification.",
                          ready_for_worker=True)
        return _stage("B2_active", phase or "unknown", "investigate",
                      next_action=item.get("next_action") or "Read progress doc to determine stage.",
                      ready_for_worker=False)

    return _stage("unknown", "unknown", "investigate")


def _stage(stage: str, phase_state: str, next_action_kind: str,
           next_action: str = "", ready_for_worker: bool = False,
           owner_hint: str = "worker") -> dict:
    return {
        "lifecycle_stage": stage,
        "phase_state": phase_state,
        "next_action_kind": next_action_kind,
        "next_action": next_action,
        "ready_for_worker": ready_for_worker,
        "owner_hint": owner_hint,
    }


# ── Main ─────────────────────────────────────────────────

def build_payload(project: Path) -> dict:
    raw_items = scan_all_items(project)

    # Resolve stage for each item
    resolved = []
    for item in raw_items:
        stage_info = resolve_lifecycle_stage(item)
        item.update(stage_info)
        # Clean up internal fields
        resolved.append({
            "item_id": item["item_id"],
            "kind": item["kind"],
            "lifecycle_stage": item["lifecycle_stage"],
            "phase_state": item["phase_state"],
            "next_action": item["next_action"],
            "next_action_kind": item["next_action_kind"],
            "ready_for_worker": item["ready_for_worker"],
            "owner_hint": item.get("owner_hint", "worker"),
            "artifact_path": item.get("raw_file", ""),
            "cross_refs": {
                "promoted_from": item.get("promoted_from", ""),
                "absorbed_into": item.get("absorbed_into", ""),
                "canonical_issue_path": item.get("canonical_issue_path", ""),
            },
        })

    # Summary
    by_stage = {}
    for item in resolved:
        s = item["lifecycle_stage"]
        by_stage[s] = by_stage.get(s, 0) + 1

    ready = sum(1 for i in resolved if i["ready_for_worker"])

    return {
        "scan_version": "lifecycle-v2",
        "generated_at": now_iso(),
        "project_root": str(project),
        "routing_skill": "context-source-skill",
        "summary": {
            "total_active": len(resolved),
            "by_stage": by_stage,
            "ready_for_worker": ready,
            "needs_manager": len(resolved) - ready,
        },
        "items": resolved,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--json", action="store_true", default=True)
    args = parser.parse_args()
    project = Path(args.project).resolve()
    payload = build_payload(project)
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
