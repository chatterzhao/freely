#!/usr/bin/env python3
"""AT-001 (raw-20261114T065554Z): merge 后的追加提交不得被默认丢弃.

Context
-------
`wt-close` used to treat ANY `develop..branch` commit as "the PR was never
merged" and offered only `--force --discard-unmerged`. R33.16 (PR #4442 merged,
commit 712e7550c appended with a correct `platform_state: closed`) was nearly
discarded; the right fix was follow-up PR #4641 and a normal wt-close.

Pinned here:
  * a standalone classifier that distinguishes "never merged" from
    "post-merge additions" and uses patch-id equivalence (git cherry) as the
    verifiable fact, not a free-text reason;
  * wt-close refuses to discard non-equivalent post-merge additions and points
    at the follow-up PR path / two-dot diff caveat;
  * `--extracted-into` is only honoured when the receiving raw really exists;
  * skill / commands.md / reason list carry the same rule;
  * the protected-branch guard keeps its "no --force exception" strength.

Baseline (develop) has none of it -> red.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

GUARD = SRC / "docs/system/workspace/scripts/worktree/postmerge_commit_guard.py"
WT_CLOSE = SRC / "docs/system/workspace/scripts/worktree/wt-close"
SKILL = SRC / "docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md"
COMMANDS = SRC / "docs/system/workspace/commands.md"
KEY = "20261114T065554Z"
BRANCH = f"fix/raw-{KEY}-postmerge-commit-guard"

OK = 0
BAD = 0


def ok(label: str) -> None:
    global OK
    OK += 1
    print("  [ok] " + label)


def bad(label: str) -> None:
    global BAD
    BAD += 1
    print("  [FAIL] " + label)


def check(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args],
                       capture_output=True, text=True)
    return p.stdout.strip()


def init_repo(root: Path) -> None:
    git(root, "init", "-q")
    git(root, "symbolic-ref", "HEAD", "refs/heads/develop")
    git(root, "config", "user.email", "at@example.invalid")
    git(root, "config", "user.name", "AT")
    (root / "docs/B1-docs" / f"raw-{KEY}").mkdir(parents=True)
    (root / "docs/B1-docs" / f"raw-{KEY}" / "issue.md").write_text(
        f"---\nlocal_id: raw-{KEY}\nphase_state: absorbed\n---\n# raw\n")
    (root / "base.txt").write_text("base\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    git(root, "checkout", "-q", "-b", BRANCH)


def add_commit(root: Path, name: str, text: str) -> None:
    (root / name).write_text(text)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", f"post-merge addition: {name}")


def mark_merged(root: Path) -> None:
    """Create a real merge commit in develop whose message carries the raw key."""
    git(root, "checkout", "-q", "-b", "side", "develop")
    (root / "side.txt").write_text("side\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "side work")
    git(root, "checkout", "-q", "develop")
    git(root, "merge", "--no-ff", "-q", "side", "-m",
        f"Merge branch '{BRANCH}' into develop")


def classify(root: Path) -> dict:
    if not GUARD.is_file():
        return {}
    p = subprocess.run(
        [sys.executable, str(GUARD), "--project", str(root),
         "--branch", BRANCH, "--target", "develop"],
        capture_output=True, text=True,
    )
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {}


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: classifier scenarios ===")
    if not GUARD.is_file():
        bad("B0-B5 skipped: postmerge_commit_guard.py missing")
        return

    # A: never merged -> keep the original discard policy.
    with tempfile.TemporaryDirectory(prefix="at-pm-a-") as td:
        root = Path(td)
        init_repo(root)
        add_commit(root, "a.txt", "useful\n")
        d = classify(root)
        check(d.get("has_merge") is False, "B1 never_merged: has_merge=false")
        check(d.get("scenario") == "never_merged", "B2 never_merged scenario")
        check(d.get("allow_discard") is True,
              "B3 never_merged keeps the original --force policy")

    # B: merged, then a non-equivalent appended commit -> refuse discard.
    with tempfile.TemporaryDirectory(prefix="at-pm-b-") as td:
        root = Path(td)
        init_repo(root)
        add_commit(root, "b.txt", "unique post-merge work\n")
        mark_merged(root)
        d = classify(root)
        check(d.get("has_merge") is True, "B4 post-merge: has_merge=true")
        check(d.get("scenario") == "post_merge_additions",
              "B5 post-merge scenario is NOT reported as 'not merged'")
        check(d.get("allow_discard") is False,
              "B6 non-equivalent additions cannot be discarded")
        check(any(not c["equivalent_in_develop"] for c in d.get("commits", [])),
              "B7 the non-equivalent commit is identified per-commit")

    # C: merged, appended commit already landed in develop (cherry-pick) -> OK.
    with tempfile.TemporaryDirectory(prefix="at-pm-c-") as td:
        root = Path(td)
        init_repo(root)
        add_commit(root, "c.txt", "already landed\n")
        sha = git(root, "rev-parse", "HEAD")
        mark_merged(root)
        git(root, "cherry-pick", sha)
        d = classify(root)
        check(d.get("allow_discard") is True,
              "B8 patch-id-equivalent additions are zero-loss and may be discarded")
        check(d.get("all_equivalent") is True, "B9 all_equivalent reported")
        check(all(c["equivalent_in_develop"] for c in d.get("commits", [])),
              "B10 evidence lists every commit as equivalent")


def static_checks() -> None:
    print("=== STATIC: rule lives in skill, wt-close and commands.md ===")
    wt = read(WT_CLOSE)
    skill = read(SKILL)
    commands = read(COMMANDS)

    check(GUARD.is_file(), "S1 standalone classifier exists")
    check("post_merge_additions" in wt,
          "S2 wt-close distinguishes post-merge additions")
    check("postmerge_commit_guard.py" in wt,
          "S3 wt-close calls the classifier")
    check("equivalent" in wt and "NOT-EQUIV" in wt,
          "S4 per-commit equivalence is printed")
    check("补合并 PR" in wt and "pr-merge-guarded develop <branch>" in wt,
          "S5 follow-up PR is the preferred path")
    check("two-dot diff" in wt,
          "S6 the develop..HEAD two-dot caveat is documented")
    check("--extracted-into" in wt and "EXTRACTED_INTO" in wt,
          "S7 --extracted-into is wired and validated")
    check('docs/B1-docs/raw-$EXTRACTED_INTO/issue.md' in wt,
          "S8 the receiving raw must really exist")
    check("内容已等价落盘" in wt,
          "S9 reason list no longer equates discard with 'plan rejected'")
    check("顺序铁律：先落盘、再丢弃" in wt,
          "S10 land-then-discard ordering is stated")
    check("大概率是 pr-merge-guarded 还没执行成功" in wt,
          "S11 never-merged branch keeps its original refusal strength")

    check("merge 后残留提交" in skill and "B 已 merge + 追加提交" in skill,
          "S12 skill stage 9 declares the decision tree")
    check("two-dot diff 坑" in skill and "补合并 PR" in skill,
          "S13 skill carries the follow-up PR and the two-dot caveat")
    check("--extracted-into" in commands and "patch-id" in commands,
          "S14 commands.md documents the option and the fact-based rule")

    # The protected-branch guard must NOT gain a --force exception.
    pgb = read(SRC / "docs/system/workspace/scripts/tests/test-wt-close-test-premerge-guard.py")
    check("guard has NO --force/--discard-unmerged exception" in pgb,
          "S15 protected-branch guard test unchanged")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    behaviour_checks()
    static_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
