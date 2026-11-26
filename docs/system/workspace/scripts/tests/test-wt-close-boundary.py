#!/usr/bin/env python3
"""AT-001 for raw-20261125T065112Z / I-20261125T065112Z-A.

wt-close is a terminal gate plus an irreversible cleanup: the normal path is
write-free. Guidance must say so, the batch hint must be raw-key scoped, and a
touched linked issue must carry a real YAML frontmatter block.

Usage: python3 ...test-wt-close-boundary.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

OK = FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global OK, FAIL
    if cond:
        OK += 1
        print(f"ok   {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]

    commands = (root / "docs/system/workspace/commands.md").read_text(encoding="utf-8")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    skill = (root / "docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md").read_text(encoding="utf-8")
    runtime = (root / "docs/system/workspace/scripts/runtime/freely").read_text(encoding="utf-8")
    gate = (root / "docs/system/workspace/scripts/quality/governance-merge-gate").read_text(encoding="utf-8")

    check("commands.md states write-free normal path", "正常路径 write-free" in commands)
    check("AGENTS.md states write-free normal path", "正常路径不写平台" in agents)
    check("workflow skill uses single --raw-key entry",
          "freely wt-close --raw-key <key>" in skill and "先关测试工位" not in skill)
    check("workflow skill no longer claims platform close on normal path",
          "双平台 close issue" not in skill)
    check("runtime hint uses scoped batch", "batch --auto" in runtime or 'batch "$_raw_key"' in runtime)

    check("gate defines linked frontmatter validator", "_validate_linked_strict_frontmatter" in gate)
    check("gate requires schema_version on touched linked docs",
          "schema_version" in gate and "touched linked issue must declare" in gate)

    # Behavioral: the validator must reject bullet-only / non-YAML frontmatter
    # and accept a strict one. Run the gate module's helper in isolation via
    # source extraction (pure stdlib + yaml, no repo-wide state).
    class Issue:
        issue_id = "I-99999999T000000Z-A"
        path = "docs/B2-docs/demo/story/raw-x/issues/I-99999999T000000Z-A.md"

    ns: dict = {"read_repo_text": lambda p: ns["_text"], "yaml": __import__("yaml"), "IssueRecord": object, "_text": ""}
    try:
        start = gate.index("def _validate_linked_strict_frontmatter")
        end = gate.index("\n\ndef ", start + 10)
    except ValueError:
        for name in ("strict linked frontmatter accepted",
                     "bullet-only frontmatter rejected",
                     "untouched legacy linked doc not blocked"):
            check(name, False, "validator missing on develop")
        print(f"SUMMARY: {OK} ok, {FAIL} failed")
        return 1
    exec(compile(gate[start:end], "<validator>", "exec"), ns)
    validate = ns["_validate_linked_strict_frontmatter"]

    ns["_text"] = "---\nschema_version: '1'\nissue_id: I-99999999T000000Z-A\n---\n\n# demo\n"
    check("strict linked frontmatter accepted",
          validate(Issue(), [Issue.path]) == [])
    ns["_text"] = "---\n- schema_version: '1'\n- issue_id: I-99999999T000000Z-A\n---\n\n# demo\n"
    check("bullet-only frontmatter rejected", bool(validate(Issue(), [Issue.path])))
    check("untouched legacy linked doc not blocked", validate(Issue(), []) == [])

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
