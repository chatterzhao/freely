#!/usr/bin/env python3
"""AT-001 for raw-20261125T094104Z / I-20261125T094104Z-A.

`pr-merge-guarded` auto-commits issue-sync changes before merge and must push
the SOURCE branch to every configured platform. The buggy version used
`git push all <branch> 2>/dev/null || true` followed by an unconditional
"committed + pushed" echo — a silent partial-success receipt.

Structural checks assert the source has a per-remote helper with aggregated
failure handling and no unconditional echo. Behavioural checks exercise a
harness that models per-remote push outcomes (one platform fails -> nonzero +
failed list; all succeed -> per-remote ok).

RED on develop: helper absent, push-all || true present, unconditional echo.
GREEN after the fix.

Usage:
  python3 docs/system/workspace/scripts/tests/test-pr-merge-push-receipt.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

OK = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global OK, FAIL
    if cond:
        OK += 1
        print(f"ok   {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def git_show(src: Path, rel: str) -> str:
    try:
        r = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=src,
                           capture_output=True, text=True)
        if r.returncode == 0:
            return r.stdout
    except Exception:
        pass
    p = src / rel
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""


def extract_block(text: str, start_marker: str, end_marker: str) -> str:
    i = text.find(start_marker)
    if i < 0:
        return ""
    j = text.find(end_marker, i + len(start_marker))
    return text[i:j if j > 0 else len(text)]


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[4]
    rel = "docs/system/workspace/scripts/worktree/pr-merge-guarded"
    text = git_show(src, rel)
    check("pr-merge-guarded source readable", bool(text), rel)

    # --- Structural: old buggy pattern gone ---
    block = extract_block(text, "_sync_issues_changed_in_merge()", "_update_issue_phase()")
    check("helper _push_source_branch_to_all_remotes defined",
          "_push_source_branch_to_all_remotes" in text,
          "per-remote push helper must exist")
    check("no `push all ... || true` in issue-sync block",
          "push all" not in block and "|| true" not in block.replace("git -C \"$_wt_path\" add", "").replace("commit -m", "").replace("git fetch", ""),
          "push all + || true swallows failures")
    check("no unconditional committed+pushed echo",
          "committed + pushed" not in block,
          "unconditional success echo must be removed")
    helper = extract_block(text, "_push_source_branch_to_all_remotes()", "\n}")
    check("helper body extracted", bool(helper), "helper function body must exist")
    check("helper iterates git remote skipping all",
          'grep -v "^all$"' in helper or 'grep -v "^all"' in helper or '"all"' in helper,
          "helper must iterate remotes excluding 'all'")
    check("helper aggregates failed remotes",
          "failed_remote" in helper.lower() or "push_failed" in helper.lower(),
          "helper must track failed remotes")
    check("helper returns nonzero on failure",
          "return 1" in helper and "failed" in helper.lower(),
          "helper must return nonzero when any remote fails")
    check("helper pushes per remote (not push all)",
          "push all" not in helper and "git push" in helper,
          "helper must push each remote individually")
    check("caller propagates push failure (merge aborted)",
          "_push_source_branch_to_all_remotes" in block,
          "issue-sync block must call the helper")

    # --- Behavioural: model per-remote outcomes (pure python harness) ---
    def model_push(remotes: list[str], fail: set[str]) -> tuple[int, list[str], list[str]]:
        ok_list, failed = [], []
        for r in remotes:
            (failed if r in fail else ok_list).append(r)
        return (1 if failed else 0, ok_list, failed)

    remotes = ["github", "origin"]
    rc, ok_list, failed = model_push(remotes, set())
    check("all remotes succeed -> rc 0, no failed", rc == 0 and not failed and len(ok_list) == 2)
    rc, ok_list, failed = model_push(remotes, {"github"})
    check("github fails -> rc 1, failed lists github", rc == 1 and failed == ["github"])
    rc, ok_list, failed = model_push(remotes, {"origin"})
    check("origin fails -> rc 1, failed lists origin", rc == 1 and failed == ["origin"])
    rc, ok_list, failed = model_push(remotes, {"github", "origin"})
    check("both fail -> rc 1, failed lists both", rc == 1 and len(failed) == 2)

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
