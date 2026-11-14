#!/usr/bin/env python3
"""postmerge_commit_guard.py — classify commits left on a branch after close.

Design (raw-20261114T065554Z)
----------------------------
`wt-close` used to treat ANY `develop..branch` commit as "the PR was never
merged". That is wrong for the common case where the PR *has* been merged and a
later commit was appended to the branch (e.g. a replica-state watermark written
after `pr-merge-guarded`). The old prompt told the operator to conclude "not
merged" and offered only `--force --discard-unmerged`, which silently destroys
correct work (R33.16 / PR #4442 + #4641).

The decision must rest on VERIFIABLE git facts, not on a free-text reason:

  scenario A  never_merged          -> no merge commit for this raw key in the
                                       target; keep the existing --force path.
  scenario B  post_merge_additions  -> the raw was merged; only allow discard
                                       when every appended commit is already
                                       equivalent in the target (patch-id), or
                                       when the work was explicitly extracted
                                       into another raw (checked by wt-close).

Output: one JSON object. No writes, no platform calls.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

RAW_KEY_RE = re.compile(r"\d{8}T\d{6}Z")


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", root, *args], capture_output=True, text=True
    )


def out(root: str, *args: str) -> str:
    return git(root, *args).stdout.strip()


def classify(root: str, branch: str, target: str) -> dict:
    key_match = RAW_KEY_RE.search(branch)
    raw_key = key_match.group(0) if key_match else ""

    # Has this raw already been merged into the target? wt-close:198-201 already
    # used exactly this predicate for a different check.
    merge_count = out(root, "rev-list", target, "--merges",
                      "--grep", f"raw-{raw_key}", "--count") if raw_key else "0"
    has_merge = merge_count.isdigit() and int(merge_count) > 0

    ahead = out(root, "rev-list", "--count", f"{target}..{branch}")
    ahead_n = int(ahead) if ahead.isdigit() else 0

    # git cherry is the standard patch-id equivalence test:
    #   "- <sha>" = an equivalent patch already exists upstream
    #   "+ <sha>" = no equivalent patch
    cherry_map: dict[str, bool] = {}
    for line in out(root, "cherry", target, branch).splitlines():
        if len(line) < 3 or line[0] not in "+-":
            continue
        cherry_map[line[2:].strip()] = line[0] == "-"

    commits = []
    shas = out(root, "rev-list", f"{target}..{branch}").splitlines()
    for sha in shas:
        if not sha:
            continue
        parents = out(root, "show", "-s", "--format=%P", sha)
        is_merge = len(parents.split()) >= 2
        subject = out(root, "show", "-s", "--format=%s", sha)
        # Merge commits and empty commits are absent from `git cherry`; treat
        # them conservatively as NOT equivalent so a discard can never lose
        # conflict resolutions or other unique content.
        equivalent = (not is_merge) and cherry_map.get(sha, False)
        commits.append({
            "sha": sha,
            "subject": subject,
            "is_merge": is_merge,
            "equivalent_in_develop": equivalent,
        })

    all_equivalent = all(c["equivalent_in_develop"] for c in commits) if commits else True
    scenario = "post_merge_additions" if has_merge else "never_merged"

    # Scenario A keeps the original policy (an abandoned plan may be discarded
    # with a reason). Scenario B only allows a zero-loss discard; otherwise the
    # operator must land the work (follow-up PR) or extract it into a new raw.
    allow_discard = (not has_merge) or all_equivalent

    return {
        "project": str(Path(root).resolve()),
        "branch": branch,
        "target": target,
        "raw_key": raw_key,
        "has_merge": has_merge,
        "ahead": ahead_n,
        "scenario": scenario,
        "commits": commits,
        "all_equivalent": all_equivalent,
        "allow_discard": allow_discard,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="git worktree / repo root")
    parser.add_argument("--branch", required=True)
    parser.add_argument("--target", default="develop")
    args = parser.parse_args()

    if not git(args.project, "rev-parse", "--is-inside-work-tree").stdout.strip():
        print(json.dumps({"error": f"not a git work tree: {args.project}"}))
        return 2
    print(json.dumps(classify(args.project, args.branch, args.target),
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
