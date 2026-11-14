#!/usr/bin/env python3
"""AT-001 (raw-20261114T033013Z): the merge hook must see linked documents.

Design (docs/system/workspace/ibm-framework.md): "merge 到 develop -> issue-sync
close（关闭已完成的 I-*）", driven by pr-merge-guarded's post-merge hook, before
the merge completes.

The previous hook diffed only docs/B1-docs, while linked documents live under
docs/B2-docs/**/issues/. Every linked case was therefore dead code: completed
I-* were never closed at merge, their documents were never committed, and the
hook called 'issue-sync close <I-*>' (refused by design).

This AT pins the three fixes of the closeout chain:
  1. discovery covers B1 + B2, scoped to the lane raw key (merge_issue_sync.py);
  2. cmd-create writes platform_state for linked too;
  3. wt-close keeps checking the children against develop: it runs AFTER the
     merge (commands.md), so develop is the truth; reading the worktree would
     let an unmerged branch state pass the pre-check.

Baseline (develop) has no module and none of the three behaviours -> red.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

MODULE = SRC / "docs/system/workspace/scripts/worktree/merge_issue_sync.py"
HOOK = SRC / "docs/system/workspace/scripts/worktree/pr-merge-guarded"
CREATE = SRC / "bin/issue-sync.d/cmd-create.sh"
WT_CLOSE = SRC / "docs/system/workspace/scripts/worktree/wt-close"
KEY = "20261114T033013Z"
OTHER = "20260101T000000Z"

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


def load_module():
    if not MODULE.is_file():
        return None
    spec = importlib.util.spec_from_file_location("merge_issue_sync_under_test", MODULE)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


RAW_DOC = """---
schema_version: '1'
local_id: raw-{key}
kind: raw
phase_state: {phase}
updated_at: '2026-11-14T00:00:00Z'
---

# raw {key}
"""

LINKED_DOC = """---
schema_version: '1'
issue_id: I-{key}-1
kind: linked
phase_state: {phase}
platform_state: closed
updated_at: '2026-11-14T00:00:00Z'
pre_tests_path: docs/B2-docs/e/s/raw-{key}/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/e/s/raw-{key}/code-reviews
---

# {key}
"""


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def build_repo(root: Path) -> None:
    (root / "docs/B1-docs" / f"raw-{KEY}").mkdir(parents=True)
    (root / "docs/B1-docs" / f"raw-{OTHER}").mkdir(parents=True)
    for sub in (KEY, OTHER):
        (root / "docs/B2-docs/e/s" / f"raw-{sub}" / "issues").mkdir(parents=True)
        (root / "docs/B2-docs/e/s" / f"raw-{sub}" / "verification").mkdir(parents=True)
        (root / "docs/B2-docs/e/s" / f"raw-{sub}" / "code-reviews").mkdir(parents=True)
    (root / "docs/B1-docs" / f"raw-{KEY}" / "issue.md").write_text(RAW_DOC.format(key=KEY, phase="proposed"))
    (root / "docs/B1-docs" / f"raw-{OTHER}" / "issue.md").write_text(RAW_DOC.format(key=OTHER, phase="proposed"))
    (root / "docs/B2-docs/e/s" / f"raw-{KEY}" / "issues" / f"I-{KEY}-1.md").write_text(LINKED_DOC.format(key=KEY, phase="completed"))
    (root / "docs/B2-docs/e/s" / f"raw-{OTHER}" / "issues" / f"I-{OTHER}-1.md").write_text(LINKED_DOC.format(key=OTHER, phase="completed"))
    git(root, "init", "-q")
    git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    git(root, "config", "user.email", "at@example.invalid")
    git(root, "config", "user.name", "AT")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    git(root, "checkout", "-q", "-b", "feature")
    for rel in ("docs/B1-docs", "docs/B2-docs"):
        for path in (root / rel).rglob("*.md"):
            path.write_text(path.read_text() + "\n<!-- touched -->\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "work")


def module_checks() -> None:
    print("=== MODULE: discovery + decision + apply ===")
    mod = load_module()
    check(mod is not None, "S1 merge_issue_sync.py exists")
    if mod is None:
        bad("S2-S13 skipped: module missing")
        return

    check(mod.classify_path(f"docs/B1-docs/raw-{KEY}/issue.md") == ("raw", f"raw-{KEY}"),
          "S2 B1 raw document is classified as raw")
    check(mod.classify_path(f"docs/B2-docs/e/s/raw-{KEY}/issues/I-{KEY}-1.md") == ("linked", f"I-{KEY}-1"),
          "S3 B2 linked document is classified as linked")
    check(mod.classify_path("docs/B1-docs/raw-x/notes.md") == ("", ""),
          "S4 unrelated markdown is ignored")

    table = [
        ("raw", "proposed", "advance:absorbed"),
        ("raw", "", "advance:absorbed"),
        ("raw", "absorbed", "close"),
        ("raw", "dropped", "close"),
        ("linked", "in_dev", "advance:in_verification"),
        ("linked", "done_b2_ibm", "advance:in_verification"),
        ("linked", "completed", "close"),
        ("linked", "in_verification", "update"),
        ("linked", "", "none"),
    ]
    for kind, phase, want in table:
        got = mod.decide(kind, phase)
        check(got == want, f"S5 decide({kind!r},{phase!r}) -> {got!r} (want {want!r})")

    with tempfile.TemporaryDirectory(prefix="at-closeout-") as td:
        root = Path(td)
        build_repo(root)
        proc = subprocess.run(
            [sys.executable, str(MODULE), "--project", str(root), "--target", "main",
             "--src", "feature", "--raw-key", KEY, "--apply"],
            capture_output=True, text=True,
        )
        rows = [r.split("\t") for r in proc.stdout.strip().splitlines() if r.strip()]
        paths = {r[0] for r in rows}
        check(proc.returncode == 0, f"S6 module runs (rc={proc.returncode})")
        check(f"docs/B1-docs/raw-{KEY}/issue.md" in paths,
              "S7 the lane B1 raw document is discovered")
        check(f"docs/B2-docs/e/s/raw-{KEY}/issues/I-{KEY}-1.md" in paths,
              "S8 the lane B2 linked document is discovered")
        check(not any(OTHER in p for p in paths),
              "S9 documents of another raw are excluded by --raw-key")

        raw_after = (root / "docs/B1-docs" / f"raw-{KEY}" / "issue.md").read_text()
        linked_after = (root / "docs/B2-docs/e/s" / f"raw-{KEY}" / "issues" / f"I-{KEY}-1.md").read_text()
        other_after = (root / "docs/B1-docs" / f"raw-{OTHER}" / "issue.md").read_text()
        check("phase_state: absorbed" in raw_after, "S10 raw proposed is advanced to absorbed")
        check("updated_at: '2026-11-14T00:00:00Z'" in raw_after,
              "S11 apply preserves every other frontmatter field")
        check("phase_state: completed" in linked_after,
              "S12 a completed linked document keeps its phase (batch closes it)")
        check("phase_state: proposed" in other_after, "S13 other raws are untouched")


def wiring_checks() -> None:
    print("=== WIRING: hook, create, wt-close ===")
    hook = read(HOOK)
    create = read(CREATE)
    wtc = read(WT_CLOSE)

    check("merge_issue_sync.py" in hook, "S14 hook uses the discovery helper")
    check("--raw-key" in hook, "S15 hook scopes discovery to the lane raw key")
    check('batch "$_raw_key"' in hook, "S16 hook retires linked through issue-sync batch")
    check("changed_issues" not in hook, "S17 the dead B1-only loop is gone")
    check('add -- "${_touched[@]}"' in hook, "S18 hook stages only the documents it changed")
    check("add docs/B1-docs/" not in hook, "S19 hook no longer stages a whole tree")

    check('_fm_has_key "$file" "platform_state"' not in create,
          "S20 cmd-create no longer guards platform_state behind _fm_has_key")
    check('_fm_set_str "$file" "platform_state" "open"' in create,
          "S21 cmd-create writes platform_state for every created issue")

    # DESIGN REFERENCE: wt-close runs in the project root AFTER the PR merged
    # (commands.md), so develop is the merged truth.  Reading the worktree copy
    # would let an unmerged branch state pass the pre-check - a downgrade this
    # round explicitly rejected.  Pin the design instead of the shortcut.
    check('_wt_children_report="$(python3 - "$PROJECT_ROOT"' in wtc,
          "S22 wt-close checks the children against develop (post-merge truth)")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    module_checks()
    wiring_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
