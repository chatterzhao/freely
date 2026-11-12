#!/usr/bin/env python3
"""AT-001 (raw-20261112T131150Z): preview/recovery paths must not mutate state.

Two defects, one shared root cause: a path documented as read-only ran the real
effect.

  1. wt-close --dry-run deleted the companion test-pre-merge worktree/branch
     (and released agent_working rows) - Phase 6b had no DRY_RUN branch while
     Phase 5/6/7 did.
  2. wt-create unconditionally rewrote an absorbed raw back to "proposed"
     before creating the worktree, i.e. it wrote into the caller's tree
     (develop) - the comment claimed "never on develop".

The behavioural check is not a source grep: it extracts the real Phase 6b block
from the source tree under test, runs it with DRY_RUN=true against a stub git,
and asserts no destructive verb reached git. The negative control runs the same
block with DRY_RUN=false and asserts the verbs DO arrive - otherwise the check
would pass by accident.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import stat
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

WT_CLOSE = SRC / "docs/system/workspace/scripts/worktree/wt-close"
WT_CREATE = SRC / "docs/system/workspace/scripts/worktree/wt-create"
KEY = "20261112T131150Z"

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


def phase6b_block(text: str) -> str:
    start = text.find("Phase 6b")
    if start < 0:
        return ""
    end = text.find("Phase 7", start)
    if end < 0:
        return text[start:]
    line_start = text.rfind("\n", start, end)
    return text[start:line_start if line_start > start else end]


def run_block(block: str, dry: bool) -> tuple[str, str]:
    """Execute the extracted block with a stub git; return (stdout, git log)."""
    with tempfile.TemporaryDirectory(prefix="at-preview-") as td:
        root = Path(td)
        (root / "bin").mkdir()
        (root / "wts" / ("test-pre-merge-" + KEY + "-at-probe")).mkdir(parents=True)
        (root / "root").mkdir()
        git_log = root / "git.log"
        stub = root / "bin/git"
        stub.write_text(
            "#!/usr/bin/env bash\n"
            'printf "%s\\n" "$*" >> "' + str(git_log) + '"\n'
            'case "$1" in show-ref) exit 0 ;; esac\n'
            "exit 0\n",
            encoding="utf-8",
        )
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
        script = root / "block.sh"
        script.write_text(
            "set -uo pipefail\n"
            "_dry() { printf '[DRY-RUN] %s\\n' \"$*\"; }\n"
            "DRY_RUN=" + ("true" if dry else "false") + "\n"
            "FORCE=false\n"
            "DISCARD_UNMERGED=false\n"
            "branch='fix/raw-" + KEY + "-at-probe'\n"
            "PROJECT_WORKTREES_ROOT='" + str(root / "wts") + "'\n"
            "PROJECT_ROOT='" + str(root / "root") + "'\n"
            + block
            + "\nexit 0\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            ["bash", str(script)],
            capture_output=True,
            text=True,
            timeout=120,
            env={"PATH": str(root / "bin") + ":/usr/bin:/bin", "HOME": str(root)},
        )
        return proc.stdout + proc.stderr, read(git_log)


def static_checks() -> None:
    print("=== STATIC: dry-run guard and explicit reopen ===")
    close_text = read(WT_CLOSE)
    block = phase6b_block(close_text)
    create_text = read(WT_CREATE)

    check(bool(block), "S1 Phase 6b block found in wt-close")
    check("DRY_RUN" in block, "S2 Phase 6b consults DRY_RUN")
    positions = [i for i in (block.find("git worktree remove"), block.find("git branch -D")) if i >= 0]
    first_destructive = min(positions) if positions else -1
    guard_at = block.find('DRY_RUN" == true')
    check(
        guard_at >= 0 and first_destructive > guard_at,
        "S3 destructive verbs come after the DRY_RUN branch",
    )
    check("_dry " in block, "S4 dry branch prints the planned actions via _dry")

    check("--reopen" in create_text, "S5 wt-create documents --reopen")
    check("_reopen" in create_text, "S6 wt-create parses a reopen switch")
    rewrites = [
        ln.strip()
        for ln in create_text.splitlines()
        if "sed -i" in ln and "phase_state:" in ln
    ]
    check(
        bool(rewrites) and all('_reopen_file' in ln for ln in rewrites),
        "S7 every phase rewrite targets the dev worktree copy (_reopen_file)",
    )
    check(
        not any('_issue_file' in ln for ln in rewrites),
        "S7b the caller-tree path (_issue_file) is never rewritten",
    )
    check("resume_mode" in create_text, "S8 resume path is still a first-class branch")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: extracted Phase 6b block ===")
    block = phase6b_block(read(WT_CLOSE))
    if not block:
        bad("B1 block extractable")
        return

    dry_out, dry_log = run_block(block, True)
    destructive = [ln for ln in dry_log.splitlines() if "worktree remove" in ln or "branch -D" in ln]
    check(not destructive, "B1 DRY_RUN=true sends no destructive verb to git (got=" + str(destructive) + ")")
    check("DRY-RUN" in dry_out, "B2 DRY_RUN=true still reports the planned actions")

    _real_out, real_log = run_block(block, False)
    real = [ln for ln in real_log.splitlines() if "worktree remove" in ln or "branch -D" in ln]
    check(len(real) >= 2, "B3 negative control: DRY_RUN=false still performs cleanup (got=" + str(real) + ")")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
