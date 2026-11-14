#!/usr/bin/env python3
"""merge_issue_sync.py — issue-document transitions triggered by a merge.

Design (docs/system/workspace/ibm-framework.md):

    merge to develop -> issue-sync close (completed I-*) + phase advance,
    driven by pr-merge-guarded's post-merge hook, BEFORE the merge completes,
    and committed in the worktree so develop carries platform_state.

Why this module exists (raw-20261114T033013Z)
---------------------------------------------
The hook used to run `git diff -- docs/B1-docs` only. Linked documents live under
`docs/B2-docs/**/issues/I-*.md`, so every `linked/*` case in that hook was dead
code: completed I-* were never closed at merge time and their document updates
were never committed. The hook also called `issue-sync close <I-*>`, which
cmd_close refuses on purpose (batch is the single retirement driver).

Contract
--------
input   : a git range (--target .. --src) inside --project
scope   : the lane's raw key (--raw-key); without it only B1 documents are handled
output  : TSV  <path>\t<kind>\t<phase>\t<action>   (path is relative to --project)
actions : advance:absorbed | advance:in_verification | close | update | none
--apply : rewrite phase_state in place with a line replacement. Never round-trip
          YAML: raw documents have a strict field set and order, and yaml.dump
          would silently reorder them (which the strict validator rejects).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - the repo already depends on PyYAML
    yaml = None  # type: ignore[assignment]

RAW_DOC_SUFFIX = "/issue.md"
LINKED_MARKER = "/issues/"

# kind/phase -> action. Mirrors the lifecycle in ibm-framework.md:
#   raw    proposed -> absorbed (merge); absorbed/dropped -> close
#   linked in_dev|in_b2_ibm|done_b2_ibm -> in_verification (merge)
#          completed -> close (batch owns the predicate)
RAW_ACTIONS = {
    "proposed": "advance:absorbed",
    "": "advance:absorbed",
    "absorbed": "close",
    "dropped": "close",
}
LINKED_ADVANCE = {"in_dev", "in_b2_ibm", "done_b2_ibm"}
LINKED_CLOSE = {"completed"}


def classify_path(path: str) -> tuple[str, str]:
    """Return (kind, local_id) for a B1/B2 issue document path."""
    norm = path.replace("\\", "/")
    if norm.endswith(RAW_DOC_SUFFIX):
        return "raw", Path(norm).parent.name
    if LINKED_MARKER in norm and norm.endswith(".md"):
        name = Path(norm).name
        if name.startswith("I-"):
            return "linked", name[:-3]
    return "", ""


def decide(kind: str, phase: str) -> str:
    """Return the lifecycle action for one document."""
    phase = (phase or "").strip()
    if kind == "raw":
        return RAW_ACTIONS.get(phase, "none")
    if kind == "linked":
        if phase in LINKED_CLOSE:
            return "close"
        if phase in LINKED_ADVANCE:
            return "advance:in_verification"
        return "none" if not phase else "update"
    return "none"


def read_frontmatter(path: Path) -> dict:
    if yaml is None:
        return {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except Exception:
        return {}


def apply_phase(path: Path, new_phase: str) -> bool:
    """Replace the phase_state line inside the first frontmatter block.

    Line-level so every other field keeps its exact order and quoting.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    parts = text.split("---", 2)
    if len(parts) < 3:
        return False
    head, fm, body = parts
    lines = fm.splitlines(keepends=True)
    replaced = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("phase_state:"):
            indent = line[: len(line) - len(line.lstrip())]
            lines[i] = f"{indent}phase_state: {new_phase}\n"
            replaced = True
            break
    if not replaced:
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines.append(f"phase_state: {new_phase}\n")
    path.write_text(head + "---" + "".join(lines) + "---" + body, encoding="utf-8")
    return True


def discover(project: Path, target: str, src: str) -> list[str]:
    """Paths changed between target and src under the two issue trees."""
    proc = subprocess.run(
        ["git", "-C", str(project), "diff", "--name-only", target, src,
         "--", "docs/B1-docs", "docs/B2-docs"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--target", default="develop")
    parser.add_argument("--src", required=True)
    parser.add_argument("--raw-key", default="")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    rows = []
    for rel in discover(project, args.target, args.src):
        kind, local_id = classify_path(rel)
        if not kind:
            continue
        if args.raw_key and args.raw_key not in rel:
            continue
        path = project / rel
        phase = str(read_frontmatter(path).get("phase_state", "") or "")
        action = decide(kind, phase)
        rows.append((rel, kind, phase, action, path))

    for rel, kind, phase, action, path in rows:
        if args.apply and action.startswith("advance:"):
            apply_phase(path, action.split(":", 1)[1])
        print(f"{rel}\t{kind}\t{phase}\t{action}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
