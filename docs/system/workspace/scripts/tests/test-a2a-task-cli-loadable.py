#!/usr/bin/env python3
"""AT-001 — raw-20261110T101358Z / #4272 (a2a_task.py CLI loadability).

`runtime/a2a_task.py:435` annotates `_sse_pool() -> SSEPool` BEFORE
`class SSEPool` is defined (:446), with no `from __future__ import
annotations`. On Python 3.13 the annotation is evaluated at definition time,
so simply importing the module raises `NameError: name 'SSEPool' is not
defined`. Every `python3 "$_a2a_task_py" ... 2>/dev/null || true` in the
dispatch loop therefore fails silently and worker dispatch stalls.

Fix: one line `from __future__ import annotations` + a CLI smoke test in CI.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>  (NameError -> FAIL)
  GREEN : --source-dir <this worktree>
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[5]
SRC = Path(os.environ.get("A2A_SOURCE_ROOT", str(PROJECT))).resolve()

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


def static_checks(src: Path) -> None:
    print("=== STATIC: forward reference is deferred, smoke test exists ===")
    module = src / "docs/system/workspace/scripts/runtime/a2a_task.py"
    text = module.read_text(encoding="utf-8") if module.is_file() else ""
    expect("from __future__ import annotations" in text,
           "a2a_task.py defers annotation evaluation")

    # The smoke test must actually be reachable from the CI aggregate.
    smoke = src / "docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py"
    expect(smoke.is_file(), "CLI smoke AT exists")
    aggregate = src / "bin/test-all"
    aggregate_text = aggregate.read_text(encoding="utf-8", errors="replace") if aggregate.is_file() else ""
    expect("test-a2a-task-cli-loadable" in aggregate_text,
           "CLI smoke AT is wired into bin/test-all (no more silent CLI breakage)")


def behavior_checks(src: Path, tmp: Path) -> None:
    print("=== BEHAVIOR: real CLI entry point, isolated project ===")
    module = src / "docs/system/workspace/scripts/runtime/a2a_task.py"
    if not module.is_file():
        for label in ("module imports without NameError", "CLI list returns business error",
                      "CLI update returns business error", "SSEPool class still defined"):
            bad(f"{label} (module missing)")
        return

    isolated = tmp / "project"
    isolated.mkdir(parents=True)
    tmp_module = tmp / "a2a_task_probe.py"
    tmp_module.write_text(module.read_text(encoding="utf-8"), encoding="utf-8")
    env = dict(os.environ)
    env["PROJECT_ROOT"] = str(isolated)
    env.pop("SESSION_PARENT_PROJECT", None)

    # 1) import must succeed (the exact failure on develop)
    r = subprocess.run(
        [sys.executable, "-c",
         "import importlib.util,sys;"
         f"s=importlib.util.spec_from_file_location('a2a_probe',{str(tmp_module)!r});"
         "m=importlib.util.module_from_spec(s);sys.modules['a2a_probe']=m;"
         "s.loader.exec_module(m);print('IMPORT_OK')"],
        capture_output=True, text=True, cwd=isolated, env=env, timeout=60)
    expect(r.returncode == 0 and "IMPORT_OK" in r.stdout and "NameError" not in r.stderr,
           f"module imports without NameError (rc={r.returncode}, err={r.stderr.strip()[-70:]!r})")

    # 2) `list` must fail for a BUSINESS reason, not a syntax/name error
    r = subprocess.run([sys.executable, str(tmp_module), "list", "--role", "worker",
                        "--status", "submitted"],
                       capture_output=True, text=True, cwd=isolated, env=env, timeout=60)
    combined = r.stdout + r.stderr
    name_error = "NameError" in combined or "Traceback" in combined
    expect(not name_error,
           f"CLI list returns business error, not NameError "
           f"(got {combined.strip()[:90]!r})")
    business_error = ("error" in combined.lower() or combined.strip().startswith("{")
                      or combined.strip() == "" or combined.strip() == "[]")
    expect(business_error,
           "CLI list produces a normal empty/error result when A2A Server is absent")

    # 3) `update` must likewise reach business logic
    r = subprocess.run([sys.executable, str(tmp_module), "update", "--task-id", "fake",
                        "--status", "launched"],
                       capture_output=True, text=True, cwd=isolated, env=env, timeout=60)
    combined = r.stdout + r.stderr
    expect("NameError" not in combined and "Traceback" not in combined,
           f"CLI update returns business error, not NameError "
           f"(got {combined.strip()[:90]!r})")

    # 4) guard: SSEPool itself and its semantics are untouched
    try:
        spec = importlib.util.spec_from_file_location("a2a_probe_static", tmp_module)
        m = importlib.util.module_from_spec(spec)
        sys.modules["a2a_probe_static"] = m
        spec.loader.exec_module(m)
        has_pool = hasattr(m, "SSEPool") and hasattr(m, "_sse_pool")
        has_client = hasattr(m, "A2AClient")
    except Exception:
        has_pool = has_client = False
    expect(has_pool and has_client,
           "SSEPool / _sse_pool / A2AClient remain defined (no semantics change)")


def main() -> int:
    src = SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="a2a-cli-at-"))
    try:
        static_checks(src)
        behavior_checks(src, tmp)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
