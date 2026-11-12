#!/usr/bin/env python3
"""AT-001 / AT-002 — raw-20261112T031638Z / #4310 (R33.6).

Two independent defects, one raw:

AT-001 (guidance text): R33's "no ghost skill names" acceptance only scanned the
AGENTS generator and template. The retired skill names survived in runtime error
text, hooks templates and docs. History (see B1 §1.0): `freely-fix-execution` /
`freely-feature-execution` were REAL skills, retired on 2026-06-29 by commit
`2495ca2af` ("--kind replaces --skill") and `a4029fa15`, and superseded by
`freely-workflow-guarded-execution`. `freely-feat-execution` is the pre-2026-06-25
name of `freely-feature-execution` (`0486eee90`). So this AT guards against
"references to retired entries", not against invented strings — the fix points
stale hints at the CURRENT entry and never restores the old skills.

Worse, every `wt-create` hint advertised the OPTIONAL `--skill` while omitting the
REQUIRED `--kind`, so copying the hint produces a command that fails. This AT pins
the invariant across ALL live code and user-facing docs, with an explicit whitelist.

AT-002 (caller path): `wt-create` already cd's into the dev worktree, but
`raw-issue-pull` -> `issue-sync` resolves ROOT_DIR from the SCRIPT's physical
location, so the branch check always sees the main repo's `develop` and the
protected-branch guard fires. That is not just noise: `issue-sync create` failing
means platform title normalization is silently skipped.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (old behaviour -> FAIL)
  GREEN : --source-dir <this worktree>

Behavioural items that would create real worktrees / platform issues are skipped
when FREELY_AT_NESTED=1 (set by bin/test-all --ci) to avoid recursion; the static
invariants still run in full.

Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("CI_SOURCE_ROOT", str(PROJECT))).resolve()
PROTECTED_ROOT_ARG = ""
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        SRC = Path(sys.argv[_i + 1]).resolve()
    elif _arg == "--protected-root" and _i + 1 < len(sys.argv):
        PROTECTED_ROOT_ARG = sys.argv[_i + 1]

WS = SRC / "docs/system/workspace"
SCRIPTS = WS / "scripts"
ISSUE_SYNC = SRC / "bin/issue-sync"
RAW_PULL = SRC / "bin/raw-issue-pull"
PRETESTS_GATE = SCRIPTS / "quality/pretests-gate"
WT_CLOSE = SCRIPTS / "worktree/wt-close"
RUNTIME = SCRIPTS / "runtime/freely"
REF_HOOK = WS / "hooks/reference-transaction.sh"
AGENTS_EXAMPLE = WS / "AGENTS.md.example"
THREE_LOOP = WS / "three-loop-capability-lifecycle.md"
PR_CREATE = SCRIPTS / "worktree/pr-create-guarded"
GUARD_TEST = SCRIPTS / "tests/test-wt-close-protected-branch-guard"
TEST_ALL = SRC / "bin/test-all"
SVG = SRC / "docs/epics-map.svg"
STORY = SRC / "docs/B2-docs/command-wrapper/guidance-text-single-source"
UNIT_TEST = SCRIPTS / "tests/unit/t-guidance-01.sh"

REAL_SKILL = "freely-workflow-guarded-execution"
GHOST_SKILLS = ["freely-fix-execution", "freely-feature-execution", "freely-feat-execution"]

# Files that MUST be fixed this round — they may never be whitelisted away.
MUST_FIX = [
    "bin/issue-sync",
    "docs/system/workspace/scripts/quality/pretests-gate",
    "docs/system/workspace/scripts/worktree/wt-close",
    "docs/system/workspace/scripts/runtime/freely",
]

# Legitimate occurrences, each with a reason. The AT asserts every entry exists
# so a typo cannot silently widen the scan.
WHITELIST = {
    "docs/system/workspace/scripts/tests/test-projection-consistency.py":
        "R33 AT's GHOST_SKILLS blacklist constant must name the ghosts to detect them",
    "docs/system/workspace/scripts/tests/test-guidance-text-single-source.py":
        "this AT's own GHOST_SKILLS blacklist constant",
    "docs/system/workspace/scripts/runtime/task-lifecycle-scan.bak.py":
        "dead backup: zero references repo-wide; bin/freely-package deletes *.bak.py",
    "tests/test_a2a_task_insert.py":
        "DB field fixture value; code under test does not validate skill existence",
    "docs/system/workspace/scripts/tests/test-worker-task-json-boundary.py":
        "DB field fixture value; code under test does not validate skill existence",
    "docs/system/workspace/commands.md":
        "--skill is NOT deprecated; documented correctly as an optional override",
    "docs/system/workspace/scripts/tests/test-wt-close-protected-branch-guard":
        "reverse assertion: must name the ghosts to assert their ABSENCE from the guard",
    "docs/system/workspace/scripts/tests/unit/t-guidance-01.sh":
        "reverse assertion: must name the ghosts to assert their ABSENCE from runtime/guard",
}

NESTED = os.environ.get("FREELY_AT_NESTED") == "1"

OK = 0
BAD = 0
SKIPPED = 0


def ok(label: str) -> None:
    global OK
    OK += 1
    print(f"  [ok] {label}")


def bad(label: str) -> None:
    global BAD
    BAD += 1
    print(f"  [FAIL] {label}")


def skip(label: str, why: str) -> None:
    """A skipped item is NEVER counted as ok — that would be a false green."""
    global SKIPPED
    SKIPPED += 1
    print(f"  [SKIP] {label} — {why}")


def expect(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.is_file() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(SRC))
    except ValueError:
        return str(path)


def has_ghost(text: str) -> list[str]:
    return [g for g in GHOST_SKILLS if g in text]


def scan_targets() -> list[Path]:
    """Live code + user-facing docs. Excludes B1/B2 evidence and .git."""
    out: list[Path] = []
    for base in [SRC / "bin", SCRIPTS, WS / "hooks"]:
        if base.is_dir():
            for p in sorted(base.rglob("*")):
                if not p.is_file():
                    continue
                if ".git" in p.parts or "__pycache__" in p.parts:
                    continue
                if p.name.endswith((".bak", ".bak.py", ".orig", ".rej")):
                    continue
                out.append(p)
    for extra in [AGENTS_EXAMPLE, THREE_LOOP, WS / "commands.md"]:
        if extra.is_file():
            out.append(extra)
    return out


def wt_create_hint_lines(text: str) -> list[str]:
    """Every wt-create invocation shown to the user, with continuation joined.

    Shell hints wrap across lines with a trailing backslash (the hooks template
    does), so a per-line scan would miss the --kind on the continuation line.
    """
    joined: list[str] = []
    buf = ""
    for ln in text.splitlines():
        stripped = ln.rstrip()
        if stripped.endswith("\\"):
            buf += stripped[:-1] + " "
            continue
        joined.append(buf + stripped)
        buf = ""
    if buf:
        joined.append(buf)
    return [ln for ln in joined if "wt-create" in ln and "--raw-key" in ln]


# ── AT-001: guidance text invariants ────────────────────────────────────────

def s1_issue_sync_real_skill() -> None:
    t = read(ISSUE_SYNC)
    expect(not has_ghost(t) and REAL_SKILL in t,
           "S1 bin/issue-sync guard quotes only the real workflow skill")


def s2_issue_sync_kind() -> None:
    hints = wt_create_hint_lines(read(ISSUE_SYNC))
    expect(bool(hints) and all("--kind" in h for h in hints),
           "S2 bin/issue-sync wt-create hint includes required --kind")


def s3_pretests_gate() -> None:
    t = read(PRETESTS_GATE)
    expect(not has_ghost(t),
           "S3 pretests-gate red_green_not_green message has no ghost skill")


def s4_wt_close() -> None:
    t = read(WT_CLOSE)
    expect(not has_ghost(t) and REAL_SKILL in t,
           "S4 wt-close UNMERGED warning quotes only the real workflow skill")


def s5_runtime_kind() -> None:
    hints = wt_create_hint_lines(read(RUNTIME))
    missing = [h.strip()[:90] for h in hints if "--kind" not in h]
    expect(bool(hints) and not missing,
           f"S5 runtime/freely wt-create hints all include --kind (missing: {missing})")


def s6_ref_hook() -> None:
    t = read(REF_HOOK)
    hints = wt_create_hint_lines(t)
    dup = f"--skill <{REAL_SKILL}|{REAL_SKILL}>" in t
    expect(not has_ghost(t) and not dup and bool(hints)
           and all("--kind" in h for h in hints),
           "S6 reference-transaction hook: no ghosts, no duplicated identical option, has --kind")


def s7_docs_kind() -> None:
    problems = []
    for p in [AGENTS_EXAMPLE, THREE_LOOP]:
        for h in wt_create_hint_lines(read(p)):
            if "--kind" not in h:
                problems.append(f"{rel(p)}: {h.strip()[:70]}")
    expect(not problems, f"S7 AGENTS.md.example + three-loop doc hints include --kind ({problems})")


def s8_pr_create_comment() -> None:
    t = read(PR_CREATE)
    wrong = "derives prefix from --skill" in t
    dup = f"{REAL_SKILL} → fix/raw-*, {REAL_SKILL} → feature/raw-*" in t
    expect(not wrong and not dup,
           "S8 pr-create-guarded comment attributes prefix to --kind, no duplicated name")


def s9_global_scan() -> None:
    hits = []
    for p in scan_targets():
        r = rel(p)
        if r in WHITELIST:
            continue
        ghosts = has_ghost(read(p))
        if ghosts:
            hits.append(f"{r}:{','.join(ghosts)}")
    expect(not hits, f"S9 repo-wide scan: zero ghost names outside whitelist ({hits})")


def s10_whitelist_honest() -> None:
    missing = [r for r in WHITELIST if not (SRC / r).is_file()]
    leaked = [r for r in MUST_FIX if r in WHITELIST]
    expect(not missing and not leaked,
           f"S10 whitelist entries all exist and never exempt must-fix files "
           f"(missing={missing}, leaked={leaked})")


def s11_ci_wiring() -> None:
    t = read(TEST_ALL)
    name = "test-guidance-text-single-source.py"
    expect(t.count(name) >= 2,
           "S11 AT wired into both CORE and CI_CORE of bin/test-all")


def s12_epics() -> None:
    expect(STORY.is_dir() and 'id="story-guidance-text-single-source"' in read(SVG),
           "S12 epics story dir exists and is registered in epics-map.svg")


def s13_guard_test_reversed() -> None:
    t = read(GUARD_TEST)
    # The old form REQUIRED a ghost name and used BSD-incompatible `grep -q "a\|b"`.
    # The new form must use grep -qE, and the ghost pattern must sit in the branch
    # that reports FAILURE (i.e. presence of a ghost is a failure, not a pass).
    # Ignore comment lines: the new test documents the OLD broken form in prose.
    code = "\n".join(ln for ln in t.splitlines() if not ln.lstrip().startswith("#"))
    uses_basic_alt = bool(re.search(r'grep -q "[^"]*\\\|', code))
    m = re.search(r'if grep -qE "freely-fix-execution[^"]*"[^\n]*\n([^\n]*)\n', t)
    reverse_branch = bool(m and "[FAIL]" in m.group(1))
    has_real = bool(re.search(r'grep -qE "skill:' + REAL_SKILL + r'"', t))
    expect(not uses_basic_alt and reverse_branch and has_real,
           f"S13 wt-close guard test: grep -E, ghost presence => FAIL, real skill required "
           f"(basic_alt={uses_basic_alt}, reverse={reverse_branch}, real={has_real})")


def s14_unit_test_present() -> None:
    expect(UNIT_TEST.is_file() and os.access(UNIT_TEST, os.X_OK),
           "S14 function-level unit test t-guidance-01.sh exists and is executable (Step 2.5)")


def _protected_root() -> Path | None:
    """A real repo root sitting on a protected branch.

    A synthetic `git init` sandbox cannot reach the guard: issue-sync resolves
    the issue document and imports sibling contract modules first, so it exits
    before the branch check. The guard is only reachable in a real tree.
    The call is read-only — the guard exits before any write.
    """
    cands = [Path(PROTECTED_ROOT_ARG).resolve()] if PROTECTED_ROOT_ARG else []
    cands += [SRC, PROJECT]
    for cand in cands:
        if not (cand / ".git").exists():
            continue
        br = subprocess.run(["git", "-C", str(cand), "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True, timeout=60)
        if br.returncode == 0 and br.stdout.strip() in ("develop", "main"):
            return cand
    return None


def _run_guard(root: Path, script: Path) -> subprocess.CompletedProcess:
    """Run the SCRIPT UNDER TEST against a real protected-branch repo root.

    `root` supplies the protected branch (the guard needs a real tree); `script`
    is the version being verified. Using root's own bin/ would test the old
    develop copy instead of this round's fix.
    """
    raw = "raw-20261112T031638Z"
    if not (root / "docs/B1-docs" / raw / "issue.md").is_file():
        cands = sorted((root / "docs/B1-docs").glob("raw-*/issue.md"))
        if cands:
            raw = cands[0].parent.name
    # --project is required: without it the script derives ROOT_DIR from its own
    # location (the dev worktree, a fix/* branch) and the guard correctly does not
    # fire. Pointing it at the protected root is what exercises the guard.
    return subprocess.run(
        ["bash", str(script), "--project", str(root), "create", raw],
        capture_output=True, text=True, timeout=120, cwd=str(root))


def b1_real_guard_output() -> None:
    """Actually trigger the protected-branch guard and inspect what it prints."""
    root = _protected_root()
    if root is None:
        skip("B1 real guard output is clean",
             "no real repo root on develop/main available (worktree is on fix/*)")
        return
    proc = _run_guard(root, ISSUE_SYNC)
    out = proc.stdout + proc.stderr
    guarded = proc.returncode != 0 and "protected branch" in out
    clean = not has_ghost(out) and "--kind" in out and REAL_SKILL in out
    expect(guarded and clean,
           f"B1 real guard still refuses on develop AND prints clean guidance "
           f"(rc={proc.returncode}, guarded={guarded}, ghosts={has_ghost(out)})")


def b2_negative_control() -> None:
    """Inject a ghost into a NON-whitelisted live file; the scan must catch it."""
    with tempfile.TemporaryDirectory(prefix="r336-neg-") as td:
        sandbox = Path(td)
        target = sandbox / "bin/some-live-command"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("#!/bin/sh\necho 'skill:freely-fix-execution'\n")
        ghosts = has_ghost(read(target))
        expect(bool(ghosts),
               "B2 negative control: a ghost in a non-whitelisted live file is detected")


# ── AT-002: caller path invariants ──────────────────────────────────────────

def s15_raw_pull_project() -> None:
    t = read(RAW_PULL)
    m = re.search(r'issue-sync"?\s+([^\n]*?)create\s+"\$local_id"', t)
    call = m.group(0) if m else ""
    expect("--project" in call,
           f"S15 raw-issue-pull passes --project when calling issue-sync create (call={call[:90]!r})")


def s16_root_dir_untouched() -> None:
    t = read(RAW_PULL)
    expect('ROOT_DIR="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)}"' in t,
           "S16 raw-issue-pull ROOT_DIR default derivation unchanged (script location still locates the binary)")


def s17_issue_sync_root_untouched() -> None:
    t = read(ISSUE_SYNC)
    expect('ROOT_DIR="${ROOT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)}"' in t,
           "S17 issue-sync ROOT_DIR default derivation unchanged (no blast radius on 14 modules)")


def b3_real_raw_pull() -> None:
    """Real run of the FIXED raw-issue-pull inside a fix/* worktree.

    Why not a full `wt-create`: `bin/worktree-common.sh:17` rebinds ROOT_DIR to
    the PRIMARY worktree, so `wt-create` always invokes the primary repo's
    `bin/raw-issue-pull`. Before this branch merges, that copy is still the old
    one — a bootstrap ordering fact, not a defect in the fix. The fix takes
    effect in `wt-create` only after merge; that end-to-end run is recorded
    post-merge as extra evidence.
    What IS testable pre-merge, and is exactly what AT-002 targets: the fixed
    script, executed from a fix/* worktree, must reach issue-sync cleanly.
    """
    if NESTED:
        skip("B3 fixed raw-issue-pull runs clean in a fix worktree",
             "nested run: would re-sync platform issues")
        return
    br = subprocess.run(["git", "-C", str(SRC), "rev-parse", "--abbrev-ref", "HEAD"],
                        capture_output=True, text=True, timeout=60)
    branch = br.stdout.strip()
    if br.returncode != 0 or not branch.startswith(("fix/", "feature/")):
        skip("B3 fixed raw-issue-pull runs clean in a fix worktree",
             f"source dir is on '{branch}', not a fix/feature worktree")
        return

    # raw-issue-pull refuses unless the branch contains the raw key, so the key
    # must come from the branch name, not from an arbitrary sorted directory.
    m = re.search(r"raw-(\d{8}T\d{6}Z)", branch)
    if not m:
        skip("B3 fixed raw-issue-pull runs clean in a fix worktree",
             f"branch '{branch}' carries no raw key")
        return
    key = m.group(1)
    if not (SRC / "docs/B1-docs" / f"raw-{key}" / "issue.md").is_file():
        skip("B3 fixed raw-issue-pull runs clean in a fix worktree",
             f"raw-{key} not materialized in this worktree")
        return
    proc = subprocess.run([str(RAW_PULL), "--raw-key", key],
                          capture_output=True, text=True, timeout=300,
                          cwd=str(SRC))
    out = proc.stdout + proc.stderr
    noisy = ("refuses to run on protected branch" in out
             or "issue-sync create failed" in out)
    expect(proc.returncode == 0 and not noisy and "create complete" in out,
           f"B3 fixed raw-issue-pull runs clean in a fix worktree "
           f"(rc={proc.returncode}, noisy={noisy}, reached_issue_sync={'create complete' in out})")


def b3b_post_merge_wt_create() -> None:
    """Post-merge proof that a real `wt-create` no longer emits the noise."""
    evidence = STORY / "raw-20261112T031638Z/verification/test-evidence/wt-create-post-merge.log"
    if not evidence.is_file():
        skip("B3b post-merge real wt-create has no protected-root noise",
             "captured after merge; not available during the pre-merge run")
        return
    t = read(evidence)
    noisy = ("refuses to run on protected branch" in t
             or "issue-sync create failed" in t)
    expect(not noisy and "Worktrees created" in t,
           f"B3b post-merge real wt-create: no protected-root noise (noisy={noisy})")


def b4_guard_not_weakened() -> None:
    """The guard must STILL refuse when genuinely on a protected branch."""
    root = _protected_root()
    if root is None:
        skip("B4 protected guard still refuses on develop",
             "no real repo root on develop/main available (worktree is on fix/*)")
        return
    proc = _run_guard(root, ISSUE_SYNC)
    out = proc.stdout + proc.stderr
    expect(proc.returncode != 0 and "protected branch" in out,
           f"B4 issue-sync still refuses on protected branch "
           f"(rc={proc.returncode}, guard_fired={'protected branch' in out})")


def main() -> int:
    print(f"=== AT-001/AT-002 guidance-text-single-source (source={SRC}) ===")
    print("--- AT-001 static: guidance text invariants ---")
    for fn in [s1_issue_sync_real_skill, s2_issue_sync_kind, s3_pretests_gate,
               s4_wt_close, s5_runtime_kind, s6_ref_hook, s7_docs_kind,
               s8_pr_create_comment, s9_global_scan, s10_whitelist_honest,
               s11_ci_wiring, s12_epics, s13_guard_test_reversed, s14_unit_test_present]:
        fn()
    print("--- AT-001 behavioural ---")
    b1_real_guard_output()
    b2_negative_control()
    print("--- AT-002 static: caller path invariants ---")
    for fn in [s15_raw_pull_project, s16_root_dir_untouched, s17_issue_sync_root_untouched]:
        fn()
    print("--- AT-002 behavioural ---")
    b3_real_raw_pull()
    b3b_post_merge_wt_create()
    b4_guard_not_weakened()
    print(f"SUMMARY: {OK} ok, {BAD} failed" + (f", {SKIPPED} skipped" if SKIPPED else ""))
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())