#!/usr/bin/env python3
"""AT-001 for raw-20261104T075849Z / #4160 (R31, first stage).

The 27k-line `scripts/runtime/freely` monolith keeps a `file-size: skip` marker,
so nothing stops it from growing. This AT pins the first real split:

* `bin/test-gate` and `bin/evidence` own three command bodies that used to be
  inline, and the monolith keeps only a three-line `exec` projection;
* `runtime/lib/common.sh` becomes the single owner of the helpers the extracted
  commands need, so an extraction never has to copy or source the monolith;
* `bin/check-runtime-size` + `runtime/.size-budget` make the line count
  monotonically decreasing instead of merely skipped;
* `split-plan.md` and `rust-migration-poc.md` record the split order and the
  Rust boundary/cost/rollback, without claiming the migration happened.

Runs against `git archive develop` to prove RED.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AT_NAME = "test-runtime-split.py"
MONOLITH = "docs/system/workspace/scripts/runtime/freely"
COMMON_LIB = "docs/system/workspace/scripts/runtime/lib/common.sh"
BUDGET = "docs/system/workspace/scripts/runtime/.size-budget"
SPLIT_PLAN = "docs/system/workspace/scripts/runtime/split-plan.md"
RUST_POC = "docs/system/workspace/scripts/runtime/rust-migration-poc.md"
EXTRACTED = ["bin/test-gate", "bin/evidence"]
MOVED_HELPERS = ["_log_ts", "log_info", "log_warn", "log_error",
                 "current_timestamp_utc_for_machine", "state_dir", "run_dir_for_project"]
MOVED_PRIVATE = ["_test_gate_file", "_test_gate_write"]
PROJECTIONS = {
    "cmd_test_gate_run": "bin/test-gate\" run",
    "cmd_test_gate_record": "bin/test-gate\" record",
    "cmd_evidence_add": "bin/evidence\" add",
}
# develop baseline when this round started; the split must go below it.
BASELINE_LINES = 27272

def array_has(text: str, marker: str, entry: str) -> bool:
    """True when `entry` is a line of the array that starts at `marker`.

    Matching adjacency to `CORE=(` instead would break the moment another test
    is prepended - which is exactly what happened when R31 added one (#4160).
    """
    i = text.index(marker) + len(marker)
    j = text.index(")", i)
    return entry in [line.strip() for line in text[i:j].splitlines()]

OK: list[str] = []
FAIL: list[str] = []


def check(name: str, fn):
    try:
        ok, detail = fn()
    except Exception as exc:  # noqa: BLE001 - report, never abort the suite
        ok, detail = False, f"exception: {type(exc).__name__}: {exc}"
    (OK if ok else FAIL).append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + ("" if ok else f" — {detail}"))


def body_of(text: str, name: str) -> str | None:
    m = re.search(rf"^{re.escape(name)}\(\) \{{\n", text, re.MULTILINE)
    if not m:
        return None
    end = text.find("\n}\n", m.end())
    return text[m.start():end + 3] if end != -1 else None


def probe_repo(tmp: Path, branch: str) -> Path:
    """A throwaway git repo so `test-gate` sees a real branch name."""
    subprocess.run(["git", "init", "-q", "-b", branch, str(tmp)], check=True)
    (tmp / "seed").write_text("x", encoding="utf-8")
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
           "PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(tmp)}
    subprocess.run(["git", "-C", str(tmp), "add", "seed"], check=True, env=env)
    subprocess.run(["git", "-C", str(tmp), "commit", "-qm", "seed"], check=True, env=env)
    return tmp


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="", help="root to inspect (RED: a develop snapshot)")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else ROOT

    print(f"source: {src}")
    mono_path = src / MONOLITH
    mono = mono_path.read_text(encoding="utf-8", errors="replace") if mono_path.is_file() else ""

    # ---- static ----
    def c01():
        missing = [p for p in EXTRACTED if not (src / p).is_file()]
        noexec = [p for p in EXTRACTED
                  if (src / p).is_file() and not (src / p).stat().st_mode & 0o111]
        return not missing and not noexec, f"missing={missing} not-executable={noexec}"

    def c02():
        lib = src / COMMON_LIB
        if not lib.is_file():
            return False, f"missing {COMMON_LIB}"
        text = lib.read_text(encoding="utf-8")
        missing = [h for h in MOVED_HELPERS if not re.search(rf"^{h}\(\)", text, re.MULTILINE)]
        return not missing, f"lib does not define {missing}"

    def c03():
        return 'RUNTIME_COMMON_LIB=' in mono and 'source "$RUNTIME_COMMON_LIB"' in mono, \
            "monolith does not source runtime/lib/common.sh"

    def c04():
        dup = [h for h in MOVED_HELPERS if re.search(rf"^{h}\(\)", mono, re.MULTILINE)]
        return not dup, f"monolith still defines moved helpers: {dup}"

    def c05():
        dup = [h for h in MOVED_PRIVATE if re.search(rf"^{h}\(\)", mono, re.MULTILINE)]
        return not dup, f"monolith still defines: {dup}"

    def c06():
        bad = []
        for cmd, want in PROJECTIONS.items():
            body = body_of(mono, cmd)
            if body is None:
                bad.append(f"{cmd} missing")
            elif f'exec bash "$SELF_ROOT/{want}' not in body:
                bad.append(f"{cmd} is not a projection")
        return not bad, "; ".join(bad)

    def c07():
        watcher = src / "bin/check-runtime-size"
        return (watcher.is_file() and bool(watcher.stat().st_mode & 0o111)
                and (src / BUDGET).is_file()), "check-runtime-size or budget file missing"

    def c08():
        plan = src / SPLIT_PLAN
        if not plan.is_file():
            return False, f"missing {SPLIT_PLAN}"
        text = plan.read_text(encoding="utf-8")
        rows = re.findall(r"^\| \d+ \|", text, re.MULTILINE)
        cmds = set(re.findall(r"`(cmd_[a-z0-9_]+)`", text))
        return len(rows) >= 50 and len(cmds) >= 50, \
            f"matrix has {len(rows)} rows / {len(cmds)} distinct cmd_*"

    def c09():
        poc = src / RUST_POC
        if not poc.is_file():
            return False, f"missing {RUST_POC}"
        text = poc.read_text(encoding="utf-8")
        need = ["边界", "成本", "回滚", "未迁移"]
        missing = [n for n in need if n not in text]
        return not missing, f"PoC doc lacks {missing}"

    def c10():
        ta = (src / "bin/test-all").read_text(encoding="utf-8")
        wired = array_has(ta, "\nCORE=(", AT_NAME) and array_has(ta, "\nCI_CORE=(", AT_NAME)
        return wired, "AT not wired into both CORE and CI_CORE"

    def c11():
        svg = (src / "docs/epics-map.svg").read_text(encoding="utf-8")
        return 'id="story-runtime-split"' in svg, "story not registered in epics-map"

    def c12():
        """The budget must be a real promise: below baseline and not above actual."""
        budget_path = src / BUDGET
        if not budget_path.is_file() or not mono:
            return False, "budget file or monolith missing"
        budget = int(re.sub(r"\D", "", budget_path.read_text(encoding="utf-8")) or 0)
        actual = len(mono.splitlines())
        return budget < BASELINE_LINES and actual <= budget, \
            f"budget={budget} actual={actual} baseline={BASELINE_LINES}"

    check("extracted commands exist and are executable", c01)
    check("runtime/lib/common.sh defines the moved helpers", c02)
    check("monolith sources the shared lib", c03)
    check("monolith no longer defines moved helpers", c04)
    check("monolith no longer defines moved private helpers", c05)
    check("three commands are exec projections", c06)
    check("check-runtime-size and budget file exist", c07)
    check("split-plan matrix covers every cmd_*", c08)
    check("Rust PoC documents boundary/cost/rollback", c09)
    check("AT wired into CORE and CI_CORE", c10)
    check("story registered in epics-map", c11)
    check("budget is below baseline and not above actual", c12)

    # ---- behaviour: the extracted commands keep their contract ----
    def b13():
        """check-runtime-size reports the real count and passes within budget."""
        if not (src / "bin/check-runtime-size").is_file():
            return False, "check-runtime-size missing"
        proc = subprocess.run(["bash", str(src / "bin/check-runtime-size"), "--json"],
                              capture_output=True, text=True, timeout=60)
        try:
            data = json.loads(proc.stdout)
        except Exception:  # noqa: BLE001
            return False, f"rc={proc.returncode} stdout={proc.stdout[:120]}"
        actual = len(mono.splitlines()) if mono else -1
        return proc.returncode == 0 and data.get("ok") is True and data.get("lines") == actual, \
            f"rc={proc.returncode} data={data} actual={actual}"

    def b14():
        """test-gate refuses a non-test worktree and accepts a test-pre-merge one."""
        gate = src / "bin/test-gate"
        if not gate.is_file():
            return False, "bin/test-gate missing"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dev = probe_repo(root / "dev", "feature/probe")
            refused = subprocess.run(["bash", str(gate), "record", "--worktree", str(dev),
                                      "--status", "started"], capture_output=True, text=True,
                                     timeout=60)
            if refused.returncode != 2:
                return False, f"non-test worktree rc={refused.returncode}, expected 2"
            test = probe_repo(root / "test", "test-pre-merge-probe")
            accepted = subprocess.run(["bash", str(gate), "record", "--worktree", str(test),
                                       "--status", "started"], capture_output=True, text=True,
                                      timeout=60)
            env_file = test / ".freely/run/test-gate.env"
            if accepted.returncode != 0 or not env_file.is_file():
                return False, f"test worktree rc={accepted.returncode} env={env_file.is_file()}"
            return 'TEST_STATUS="started"' in env_file.read_text(encoding="utf-8"), \
                "gate env file does not record the status"

    def b15():
        """evidence add refuses a missing file instead of recording a phantom."""
        ev = src / "bin/evidence"
        if not ev.is_file():
            return False, "bin/evidence missing"
        proc = subprocess.run(["bash", str(ev), "add", "--file", "/no/such/file.log"],
                              capture_output=True, text=True, timeout=60)
        return proc.returncode == 2 and "no such file" in proc.stderr, \
            f"rc={proc.returncode} stderr={proc.stderr.strip()[:120]}"

    def b16():
        """The projections still dispatch: an unknown subcommand must not silently pass."""
        for rel, sub in (("bin/test-gate", "bogus"), ("bin/evidence", "bogus")):
            path = src / rel
            if not path.is_file():
                return False, f"{rel} missing"
            proc = subprocess.run(["bash", str(path), sub], capture_output=True, text=True,
                                  timeout=60)
            if proc.returncode == 0:
                return False, f"{rel} {sub} exited 0"
        return True, ""

    check("check-runtime-size honours the budget", b13)
    check("test-gate refuses non-test worktrees", b14)
    check("evidence add refuses a missing file", b15)
    check("extracted entrypoints reject unknown subcommands", b16)

    print(f"\nSUMMARY: {len(OK)} ok, {len(FAIL)} failed")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
