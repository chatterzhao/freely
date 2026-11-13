#!/usr/bin/env python3
"""AT-001 (raw-20261113T084813Z): restore the protected-branch gate; retire
orphan test sandboxes through a companion-only path.

Design intent (project sources, not guesses):
  * `test-wt-close-protected-branch-guard` Test 1-3 assert main/develop/
    test-pre-merge-* are ALL blocked; Test 4 allows only fix/feature/hotfix.
  * `AGENTS.md.example`: test-pre-merge-* is a disposable sandbox, "用完即删,
    不可 commit/push".
  * `wt-close` Phase 6b is the designed companion cleanup, but it only runs for
    fix/feature branches - leaving orphan sandboxes when the dev branch is gone.

R33.9/R33.10 regression: to retire one orphan sandbox, branch resolution was
taught to resolve test-pre-merge-* AND the protected guard was widened with a
--force --discard-unmerged exception. The sandbox then ran the FULL raw
lifecycle (platform close + Phase 7 develop sync). That was fixing an
implementation gap by weakening a gate.

This fix restores the gate and adds a dedicated companion-only retirement that
inherits the reason gate but performs NO platform/develop side effects.

The behavioural check extracts the REAL guard block and companion function from
the source under test and runs them in sandbox git repos. develop (baseline)
must demonstrate the widened gate.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()
BASE = Path(sys.argv[sys.argv.index("--baseline") + 1]) if "--baseline" in sys.argv else None

WT_CLOSE = "docs/system/workspace/scripts/worktree/wt-close"
KEY = "20261113T084813Z"

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


def guard_block(text: str) -> str:
    start = text.find("# ── Guard: protected branch")
    if start < 0:
        return ""
    end = text.find("# ── Resolve worktree path", start)
    return text[start:end] if end > start else ""


def protected_helper(text: str) -> str:
    start = text.find("_is_protected_branch() {")
    if start < 0:
        return ""
    end = text.find("\n}\n", start)
    return text[start:end + 3] if end > start else ""


def companion_fn(text: str) -> str:
    start = text.find("_wt_retire_orphan_test_sandbox() {")
    if start < 0:
        return ""
    end = text.find("\n}\n", start)
    return text[start:end + 3] if end > start else ""


def run_guard(source: Path, branch: str, force: bool, discard: bool) -> subprocess.CompletedProcess:
    text = read(source / WT_CLOSE)
    helper, block = protected_helper(text), guard_block(text)
    if not helper or not block:
        return subprocess.CompletedProcess([], 99, "", "guard/helper not found")
    with tempfile.TemporaryDirectory(prefix="at-guard-") as td:
        script = Path(td) / "probe.sh"
        script.write_text(
            "set -uo pipefail\n" + helper + "\n"
            + f"branch='{branch}'\n"
            + f"FORCE={'true' if force else 'false'}\n"
            + f"DISCARD_UNMERGED={'true' if discard else 'false'}\n"
            + block + "\necho GUARD_PASSED\n",
            encoding="utf-8",
        )
        return subprocess.run(["bash", str(script)], capture_output=True, text=True, timeout=60)


def run_companion(source: Path, force: bool = True, discard: bool = True,
                  dry: bool = False) -> tuple[subprocess.CompletedProcess, str, str]:
    text = read(source / WT_CLOSE)
    fn = companion_fn(text)
    with tempfile.TemporaryDirectory(prefix="at-companion-") as td:
        root = Path(td) / "repo"
        subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=at",
                        "-c", "user.email=at@local", "commit", "--allow-empty",
                        "-q", "-m", "init"], check=True, capture_output=True)
        branch = f"test-pre-merge-{KEY}-probe"
        subprocess.run(["git", "-C", str(root), "branch", branch], check=True, capture_output=True)
        wt = Path(td) / "sandbox-wt"
        subprocess.run(["git", "-C", str(root), "worktree", "add", "-q",
                        str(wt), branch], check=True, capture_output=True)
        script = Path(td) / "probe.sh"
        script.write_text(
            "set -uo pipefail\n"
            + "_dry() { printf '[DRY-RUN] %s\\n' \"$*\"; }\n"
            + f"FORCE={'true' if force else 'false'}\n"
            + f"DISCARD_UNMERGED={'true' if discard else 'false'}\n"
            + f"DRY_RUN={'true' if dry else 'false'}\n"
            + fn + f"\n_wt_retire_orphan_test_sandbox '{KEY}'\n",
            encoding="utf-8",
        )
        env = dict(__import__("os").environ)
        env["GIT_CONFIG_GLOBAL"] = "/dev/null"
        proc = subprocess.run(["bash", str(script)], cwd=str(root),
                              capture_output=True, text=True, timeout=60, env=env)
        # Snapshot INSIDE the sandbox's lifetime: the temp dir is removed on
        # return, and querying a deleted repo would silently produce empty
        # branch/worktree lists (a false-green).
        branches = subprocess.run(["git", "-C", str(root), "branch", "--list"],
                                  capture_output=True, text=True).stdout
        worktrees = subprocess.run(["git", "-C", str(root), "worktree", "list"],
                                   capture_output=True, text=True).stdout
        return proc, branches, worktrees


def static_checks() -> None:
    print("=== STATIC: gate restored, companion-only path ===")
    text = read(SRC / WT_CLOSE)
    block = guard_block(text)
    check(bool(block), "S1 protected guard block found")
    check('$FORCE" == true' not in block and "$DISCARD_UNMERGED" not in block,
          "S2 guard has NO --force/--discard-unmerged exception")
    check("is a protected branch, cannot close" in block,
          "S3 guard still emits the refusal message")
    check("main / develop / test-pre-merge-* are ALL protected" in text,
          "S4 all three protected classes documented")
    check("_wt_retire_orphan_test_sandbox() {" in text,
          "S5 a dedicated companion-only retirement exists")
    check("no platform close / no Phase 7 develop sync" in text,
          "S6 companion path declares zero platform/develop side effects")
    check("test-pre-merge-${raw_key}-*" not in text.split("_resolve_branch_from_raw_key() {")[1].split("\n}")[0],
          "S7 branch resolver no longer resolves test-pre-merge sandboxes")
    check("ORPHAN_SANDBOX_KEY" in text,
          "S8 orphan sandbox leaves the main lifecycle before the guard")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: extracted guard + companion function ===")
    tp = f"test-pre-merge-{KEY}-probe"
    for branch in (tp, "develop", "main"):
        p = run_guard(SRC, branch, True, True)
        check(p.returncode != 0 and "cannot close" in (p.stdout + p.stderr),
              f"B1 {branch} refused even with both flags")

    p = run_guard(SRC, f"fix/raw-{KEY}-slug", True, True)
    check(p.returncode == 0 and "GUARD_PASSED" in p.stdout,
          "B2 fix branch is unaffected by the guard")

    p, branches, worktrees = run_companion(SRC)
    check(p.returncode == 0 and "companion-only" in p.stdout,
          "B3 companion retirement succeeds (rc=" + str(p.returncode) + ")")
    check(tp not in branches and branches.strip() != "",
          "B4 orphan sandbox branch is really deleted (branches queried in-sandbox)")
    check("sandbox-wt" not in worktrees and "repo" in worktrees,
          "B5 orphan sandbox worktree is really removed (worktrees queried in-sandbox)")
    check("closing platform issue" not in p.stdout and "syncing develop" not in p.stdout,
          "B6 no platform close / develop sync side effects")

    p, _, _ = run_companion(SRC, force=False)
    check(p.returncode != 0 and "requires --force" in (p.stdout + p.stderr),
          "B7 companion retirement is refused without --force")

    p, dry_branches, _ = run_companion(SRC, dry=True)
    check(p.returncode == 0 and tp in dry_branches and "[DRY-RUN]" in p.stdout,
          "B8 dry-run companion retirement is side-effect free")


def baseline_checks() -> None:
    if BASE is None:
        return
    print("=== BASELINE CONTROL: develop widened gate ===")
    p = run_guard(BASE, f"test-pre-merge-{KEY}-probe", True, True)
    check(p.returncode == 0 and "GUARD_PASSED" in p.stdout,
          "R1 develop guard really had the --force exception (RED is real)")
    text = read(BASE / WT_CLOSE)
    check("_wt_retire_orphan_test_sandbox() {" not in text,
          "R2 develop really had no companion-only path")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    baseline_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
