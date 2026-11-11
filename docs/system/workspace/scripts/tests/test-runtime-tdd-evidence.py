#!/usr/bin/env python3
"""AT-001 — raw-20261104T080007Z / #4165.

The core runtime is a 27k-line library with no function-level tests, so every
runtime PR could only be reviewed by its result: nothing recorded that a test
was red before the fix. This AT pins the three mechanics that close that gap:

1. `tests/unit/` — a function-level harness that sources the runtime exactly
   the way `bin/freely` does, with ≥10 tests over the state machine, the locks
   and the exit contracts, and a runner that can actually fail.
2. `worktree/pr_body.py` — every PR body carries a `## RED 证据` section, filled
   from the owner pre-tests, and refuses (exit 3) when a runtime change has no
   failing-test record.
3. `quality/runtime_red_gate.py` — `pr-review-guarded` refuses a runtime change
   that ships no unit test and no RED→GREEN evidence (exit 1), skips a diff that
   does not touch the runtime (exit 2).

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (old behaviour -> FAIL)
  GREEN : --source-dir <this worktree>
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("RUNTIME_TDD_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        SRC = Path(sys.argv[_i + 1]).resolve()

UNIT_DIR = SRC / "docs/system/workspace/scripts/tests/unit"
RUNNER = UNIT_DIR / "run.sh"
HARNESS = UNIT_DIR / "harness.sh"
PR_BODY = SRC / "docs/system/workspace/scripts/worktree/pr_body.py"
RED_GATE = SRC / "docs/system/workspace/scripts/quality/runtime_red_gate.py"
PR_CREATE = SRC / "docs/system/workspace/scripts/worktree/pr-create-guarded"
# #4175 moved the implementation into workspace/scripts/; bin/ is a projection
# now, so the gate call must be asserted on the real source.
PR_REVIEW = SRC / "docs/system/workspace/scripts/worktree/pr-review-guarded"
RED_HEADER = "## RED 证据"

OK = 0
BAD = 0


def ok(label: str) -> None:
    global OK
    OK += 1
    print(f"  [ok] {label}")


def bad(label: str) -> None:
    global BAD
    BAD += 1
    print(f"  [FAIL] {label}")


def expect(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.is_file() else ""


# ── STATIC ───────────────────────────────────────────────────────────────

def static_checks() -> None:
    print("=== STATIC: unit corpus exists and covers the three contracts ===")
    expect(HARNESS.is_file(), "tests/unit/harness.sh exists")
    expect(RUNNER.is_file(), "tests/unit/run.sh exists")

    tests = sorted(UNIT_DIR.glob("t-*.sh")) if UNIT_DIR.is_dir() else []
    expect(len(tests) >= 10, f"at least 10 function-level tests (got {len(tests)})")

    missing_harness = [t.name for t in tests if "harness.sh" not in read(t)]
    expect(not missing_harness,
           f"every test sources the harness ({missing_harness})")

    # Shell-runtime contracts must load the library; the DB probe drives python.
    shell_tests = [t for t in tests if re.match(r"t-(state|lock|exit|event)-", t.name)]
    missing_load = [t.name for t in shell_tests if "ut_load_runtime" not in read(t)]
    expect(not missing_load,
           f"every shell-runtime test loads the runtime ({missing_load})")

    for category in ("state", "lock", "exit"):
        count = len([t for t in tests if t.name.startswith(f"t-{category}-")])
        expect(count >= 3, f"{category} contract has >= 3 tests (got {count})")

    print("=== STATIC: RED evidence is wired into PR create + review ===")
    expect(PR_BODY.is_file(), "worktree/pr_body.py exists")
    expect(RED_GATE.is_file(), "quality/runtime_red_gate.py exists")

    pr_create = read(PR_CREATE)
    expect("pr_body.py" in pr_create and "render --project" in pr_create,
           "pr-create-guarded composes the body through pr_body.py")
    composer_at = pr_create.find("pr_body.py")
    fallback_at = pr_create.find('body="See commits for details."')
    expect(composer_at != -1 and fallback_at != -1 and composer_at < fallback_at,
           "the RED-evidence composer runs before the bare-body fallback")

    pr_review = read(PR_REVIEW)
    expect("runtime_red_gate.py" in pr_review,
           "pr-review-guarded calls the core-runtime RED gate")


# ── BEHAVIOR: the unit corpus ────────────────────────────────────────────

def runner_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: unit runner ===")
    if not RUNNER.is_file():
        bad("unit runner discovers and passes every test")
        bad("unit runner fails when a test fails")
        return

    proc = subprocess.run(["bash", str(RUNNER)], capture_output=True, text=True, timeout=600)
    tail = (proc.stdout or "").strip().splitlines()[-1] if proc.stdout.strip() else ""
    match = re.search(r"(\d+) file\(s\), (\d+) ok, (\d+) failed", tail)
    files, passed, failed = (int(match.group(1)), int(match.group(2)), int(match.group(3))) if match else (0, 0, 0)
    expect(proc.returncode == 0 and files >= 10 and passed >= 10 and failed == 0,
           f"unit runner discovers and passes every test ({tail or proc.stdout[-200:]})")

    # A green run only means something if the runner can go red.
    probe_dir = tmp / "unit-probe"
    shutil.copytree(UNIT_DIR, probe_dir)
    (probe_dir / "t-zz-probe.sh").write_text(
        "#!/usr/bin/env bash\n"
        'source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"\n'
        'ut_ok "probe passes"\n'
        'ut_bad "probe fails on purpose"\n'
        "ut_report\n"
    )
    probe = subprocess.run(["bash", str(probe_dir / "run.sh")], capture_output=True,
                           text=True, timeout=600)
    expect(probe.returncode != 0 and "probe fails on purpose" in probe.stdout,
           "unit runner fails when a test fails")


# ── BEHAVIOR: PR body composer ───────────────────────────────────────────

PRE_TESTS = """# Pre-Tests: probe
- issue_id: I-20260101T000000Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: probe contract
- test_command: python3 docs/system/workspace/scripts/tests/test-probe.py
- expected_RED_output: SUMMARY: 0 ok, 3 failed
- actual_RED_output: SUMMARY: 0 ok, 3 failed (claim refused by stale lock)
- actual_output: SUMMARY: 3 ok, 0 failed
- evidence_file: docs/B2-docs/probe/story/raw-20260101T000000Z/verification/test-evidence/AT-001-RED.log
- red-green-status: green
"""


def make_project(root: Path, pre_tests: str = PRE_TESTS) -> Path:
    base = root / "project"
    raw_dir = base / "docs/B2-docs/probe/story/raw-20260101T000000Z"
    (raw_dir / "verification" / "test-evidence").mkdir(parents=True)
    (raw_dir / "verification" / "pre-tests.md").write_text(pre_tests)
    (raw_dir / "verification" / "test-evidence" / "AT-001-RED.log").write_text(
        "SUMMARY: 0 ok, 3 failed\n")
    subprocess.run(["git", "init", "-q", str(base)], check=False)
    return base


NO_RED_PRE_TESTS = "\n".join(
    line for line in PRE_TESTS.splitlines() if not line.startswith("- actual_RED_output:")
) + "\n"


def pr_body_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: PR body carries RED evidence ===")
    if not PR_BODY.is_file():
        for label in ("non-runtime diff marks RED as not applicable",
                      "runtime diff without evidence refuses the PR",
                      "runtime diff with evidence quotes the RED output"):
            bad(label)
        return

    with_evidence = make_project(tmp / "body", PRE_TESTS)
    without_evidence = make_project(tmp / "body-no-red", NO_RED_PRE_TESTS)

    def render(project: Path, touches: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(PR_BODY), "render", "--project", str(project),
             "--raw-key", "20260101T000000Z", "--touches-runtime", touches],
            capture_output=True, text=True, timeout=120,
        )

    skip = render(without_evidence, "0")
    expect(skip.returncode == 0 and RED_HEADER in skip.stdout and "不适用" in skip.stdout,
           "non-runtime diff marks RED as not applicable")

    refuse = render(without_evidence, "1")
    expect(refuse.returncode == 3 and "RED evidence missing" in (refuse.stdout + refuse.stderr),
           "runtime diff without evidence refuses the PR")

    quoted = render(with_evidence, "1")
    expect(quoted.returncode == 0
           and "claim refused by stale lock" in quoted.stdout
           and "test-probe.py" in quoted.stdout
           and "AT-001-RED.log" in quoted.stdout,
           "runtime diff with evidence quotes the RED output")


# ── BEHAVIOR: review gate ────────────────────────────────────────────────

def gate_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: review gate refuses runtime changes without RED ===")
    if not RED_GATE.is_file():
        for label in ("non-runtime diff is skipped", "runtime diff without unit test is refused",
                      "runtime diff with unit test + evidence passes"):
            bad(label)
        return

    project = make_project(tmp / "gate")

    def run(files: list[str]) -> subprocess.CompletedProcess:
        listing = tmp / "changed.txt"
        listing.write_text("\n".join(files) + "\n")
        return subprocess.run(
            [sys.executable, str(RED_GATE), "--project", str(project),
             "--raw-key", "20260101T000000Z", "--changed-files", str(listing), "--json"],
            capture_output=True, text=True, timeout=120,
        )

    skip = run(["docs/system/workspace/scripts/sync/platform-adapter.py"])
    expect(skip.returncode == 2 and json.loads(skip.stdout)["verdict"] == "skip",
           "non-runtime diff is skipped")

    refuse = run(["docs/system/workspace/scripts/runtime/freely"])
    payload = json.loads(refuse.stdout)
    expect(refuse.returncode == 1 and payload["verdict"] == "refuse"
           and "tests/unit" in payload["reason"],
           "runtime diff without unit test is refused")

    passing = run(["docs/system/workspace/scripts/runtime/freely",
                   "docs/system/workspace/scripts/tests/unit/t-state-01-paths.sh"])
    payload = json.loads(passing.stdout)
    expect(passing.returncode == 0 and payload["verdict"] == "pass",
           "runtime diff with unit test + evidence passes")


def main() -> int:
    print(f"AT-001 source: {SRC}")
    with tempfile.TemporaryDirectory(prefix="freely-runtime-tdd-") as directory:
        tmp = Path(directory).resolve()
        static_checks()
        runner_checks(tmp)
        pr_body_checks(tmp)
        gate_checks(tmp)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
