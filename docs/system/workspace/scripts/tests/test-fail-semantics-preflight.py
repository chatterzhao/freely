#!/usr/bin/env python3
"""AT-001 — raw-20261103T132644Z / #4157 (round 1).

Scope of this round: the two #4157 items that are both "a failure is recorded
as a normal end" and have a checkable acceptance in the issue.

1. `runtime/freely` supervisor: when no auto-recovery path is ready it logs
   "local runtime will now stop" and then `exit 0`. systemd/tmux see a clean
   exit and never apply a restart policy, so the workcell silently disappears.

2. No Python preflight. 13 modules import `tomllib` (3.11+); on 3.8/3.9 the
   first symptom is a `ModuleNotFoundError` from deep inside the runtime, far
   from the real cause. `bin/freely` is the single entry point, so the check
   belongs there.

The remaining #4157 items (watchdog supervision, severity/trace_id in
append_runtime_event, log rotation, credentials in argv/URL, packaging
`__pycache__`/`*.bak.py`, .env.example/skills README) are tracked by a
follow-up raw issue rather than silently dropped.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (old behaviour -> FAIL)
  GREEN : --source-dir <this worktree>
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("FAIL_SEMANTICS_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        SRC = Path(sys.argv[_i + 1]).resolve()

RUNTIME = SRC / "docs/system/workspace/scripts/runtime"
REAL_PYTHON = shutil.which("python3") or "/usr/bin/python3"

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


# ── STATIC: failure must not look like success; preflight must exist ─────

def static_checks() -> None:
    print("=== STATIC: failure semantics + Python preflight ===")
    freely = read(RUNTIME / "freely")
    entry = read(SRC / "bin/freely")

    idx = freely.find("will now stop")
    window = freely[idx:idx + 700] if idx >= 0 else ""
    expect(idx >= 0 and "exit 1" in window and "exit 0" not in window,
           "supervisor 'will now stop' branch exits non-zero")

    expect("version_info" in entry and ("(3, 11)" in entry or "(3,11)" in entry),
           "bin/freely checks Python >= 3.11 before exec")
    expect("Python >= 3.11" in entry,
           "preflight message names the required version")


# ── BEHAVIOR: old Python fails early with a precise message ─────────────

def _stub_python(tmp: Path) -> Path:
    bindir = tmp / "bin"
    bindir.mkdir(parents=True, exist_ok=True)
    stub = bindir / "python3"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        'if [[ "$*" == *version_info* ]]; then echo "${STUB_PY_OK:-0}"; exit 0; fi\n'
        'if [[ "$*" == *realpath* ]]; then printf \'%s\\n\' "$3"; exit 0; fi\n'
        f'exec "{REAL_PYTHON}" "$@"\n'
    )
    stub.chmod(0o755)
    return bindir


def preflight_checks(tmp: Path) -> None:
    print("=== BEHAVIOR: entrypoint preflight ===")
    entry = SRC / "bin/freely"
    if not entry.is_file():
        bad("old Python is rejected with a precise message")
        bad("supported Python still reaches the runtime")
        bad("real environment still starts normally")
        return
    bindir = _stub_python(tmp)
    base_env = dict(os.environ)
    base_env["PATH"] = f"{bindir}:" + base_env.get("PATH", "")

    old = dict(base_env)
    old["STUB_PY_OK"] = "0"
    old_run = subprocess.run(["bash", str(entry), "--help"], env=old,
                             capture_output=True, text=True, timeout=90)
    expect(old_run.returncode != 0 and "Python >= 3.11" in (old_run.stdout + old_run.stderr),
           "old Python is rejected with a precise message")

    new = dict(base_env)
    new["STUB_PY_OK"] = "1"
    new_run = subprocess.run(["bash", str(entry), "--help"], env=new,
                             capture_output=True, text=True, timeout=90)
    expect(new_run.returncode == 0 and "Usage" in new_run.stdout,
           "supported Python still reaches the runtime")

    real_run = subprocess.run(["bash", str(entry), "--help"], env=dict(os.environ),
                              capture_output=True, text=True, timeout=90)
    expect(real_run.returncode == 0 and "Usage" in real_run.stdout,
           "real environment still starts normally")


def main() -> int:
    print(f"AT-001 source: {SRC}")
    with tempfile.TemporaryDirectory(prefix="freely-fail-semantics-") as d:
        tmp = Path(d)
        static_checks()
        preflight_checks(tmp)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
