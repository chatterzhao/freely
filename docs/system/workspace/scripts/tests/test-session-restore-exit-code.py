#!/usr/bin/env python3
"""AT-001 — raw-20261124T054241Z / #4672.

agent_session_restore.main() must exit non-zero when any session resume fails,
and must print a structured health summary; it must not silently return 0 on
partial failure.

Run:
  RED   : python3 test-session-restore-exit-code.py --source-dir <develop>
  GREEN : python3 test-session-restore-exit-code.py
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
ROOT = Path(os.environ.get("SESSION_RESTORE_SOURCE_ROOT", str(PROJECT))).resolve()
for _i, _arg in enumerate(sys.argv):
    if _arg == "--source-dir" and _i + 1 < len(sys.argv):
        ROOT = Path(sys.argv[_i + 1]).resolve()

MODULE = ROOT / "docs/system/workspace/scripts/runtime/agent_session_restore.py"
OK = 0
BAD = 0


def check(cond: bool, label: str) -> None:
    global OK, BAD
    if cond:
        OK += 1
        print(f"  ok   {label}")
    else:
        BAD += 1
        print(f"  FAIL {label}")


def load_module():
    spec = importlib.util.spec_from_file_location("asr_under_test", MODULE)
    mod = importlib.util.module_from_spec(spec)
    # Stub dependencies that need the runtime environment.
    sys.modules.setdefault("agent_identity_value", type(sys)("agent_identity_value"))
    sys.modules["agent_identity_value"].parse_agent_entries = lambda s: {}
    aw = type(sys)("agent_working")
    aw._acp_bridge_call = lambda *a, **k: None
    aw._db_rpc = lambda *a, **k: {"rows": []}
    sys.modules.setdefault("agent_working", aw)
    spec.loader.exec_module(mod)
    return mod


def capture_main(mod, outcomes):
    mod.resume_persisted_sessions = lambda project: outcomes
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        rc = mod.main(["/some/project"])
    return rc, buf.getvalue()


def main() -> int:
    print(f"source: {ROOT}")
    check(MODULE.is_file(), "agent_session_restore.py exists")
    if not MODULE.is_file():
        print("SUMMARY: 0 ok, 1 failed")
        return 1
    mod = load_module()
    # 1. failed outcome must produce non-zero exit
    rc_fail, out_fail = capture_main(mod, [
        {"status": "resumed", "role": "worker"},
        {"status": "failed", "role": "reviewer", "error": "boom"},
    ])
    check(rc_fail != 0, "failed outcome → non-zero exit")
    # 2. structured summary present
    check(
        bool(re.search(r'"resumed"\s*:\s*1', out_fail)) and
        bool(re.search(r'"failed"\s*:\s*1', out_fail)) and
        bool(re.search(r'health', out_fail, re.I)),
        "structured summary with counts and health printed",
    )
    # 3. all resumed → 0, per-outcome lines preserved
    rc_ok, out_ok = capture_main(mod, [
        {"status": "resumed", "role": "manager"},
    ])
    check(rc_ok == 0, "all resumed → exit 0")
    check('"status": "resumed"' in out_ok, "per-outcome JSON line preserved")
    # 4. usage error still 2
    with contextlib.redirect_stderr(io.StringIO()):
        rc_usage = mod.main([])
    check(rc_usage == 2, "usage error still returns 2")
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 0 if BAD == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
