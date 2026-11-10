#!/usr/bin/env python3
"""AT-001 — raw-20261110T074344Z / #4258 (family 1: cooldown-state.env).

First concrete migration of the state-file protocol delivered in #4252.
`_read_cooldown_state` used to `source` a shell-assignment file and
`_write_cooldown_state` interpolated values with printf. This family now goes
through `runtime/state_file.py` (TAB + JSON, argv-safe writes, line-oriented
reads), while the reader still accepts legacy KEY=value without expanding it.

The AT sources the REAL `runtime/freely` and calls the real functions, so it
covers the whole shell <-> python boundary, not just the module.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>  (old printf+source -> FAIL)
  GREEN : --source-dir <this worktree>
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
SRC = Path(os.environ.get("FAMILY_SOURCE_ROOT", str(PROJECT))).resolve()

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
    print("=== STATIC: family migrated, global count dropped ===")
    freely = (src / "docs/system/workspace/scripts/runtime/freely").read_text(errors="replace")
    block = freely.split("# ── Cooldown cycle state", 1)[-1].split("SESSION_CACHE_LIB", 1)[0]
    expect("source " not in block and "--kv" in block and "STATE_FILE_PY" in block,
           "cooldown family no longer sources state and writes via --kv")

    lint = src / "bin/check-state-file-sources"
    if not lint.is_file():
        bad("boundary lint passes and count dropped to 54 (lint missing)")
        return
    r = subprocess.run([sys.executable, str(lint), "--project", str(src)],
                       capture_output=True, text=True, timeout=120)
    count = re.search(r"call sites:\s*(\d+)", r.stdout)
    got = int(count.group(1)) if count else -1
    # Monotone guard, NOT an absolute count: #4261 migrated another family and
    # lowered the global number again. Pinning 54 here would make every later
    # family migration turn this AT red for no defect. The real family guard is
    # the static check above (no `source` in the cooldown block).
    expect(r.returncode == 0 and 0 < got < 55,
           f"boundary lint passes and global state sources stay below the 55 baseline "
           f"(got {got}, rc={r.returncode})")


def _run_shell(src: Path, root: Path, body: str) -> tuple[int, str]:
    script = f'source "{src}/docs/system/workspace/scripts/runtime/freely"\n{body}\n'
    env = dict(os.environ)
    env["PROJECT_ROOT"] = str(root)
    r = subprocess.run(["bash", "-c", script], env=env, capture_output=True,
                       text=True, timeout=120)
    return r.returncode, r.stdout + r.stderr


def behavior_checks(src: Path, tmp: Path) -> None:
    print("=== BEHAVIOR: real freely functions across shell/python boundary ===")
    root = tmp / "project"
    (root / ".freely" / "run").mkdir(parents=True)
    state = root / ".freely" / "run" / "cooldown-state.env"
    marker = root / "marker"

    rc, out = _run_shell(src, root, """
_write_cooldown_state 1730000000 7
_read_cooldown_state
echo "ROUNDTRIP AT=$CROSS_TOOL_SWITCH_AT IDX=$CROSS_TOOL_SWITCH_INDEX"
""")
    expect("ROUNDTRIP AT=1730000000 IDX=7" in out,
           f"normal values round-trip through the real functions (rc={rc}, out={out.strip()[:70]!r})")

    if state.exists():
        body = state.read_text(encoding="utf-8")
        expect("\t" in body and re.search(r'COOLDOWN_SWITCH_AT\t"', body) is not None,
               "written file uses the non-executable TAB + JSON format")

    state.write_text("COOLDOWN_SWITCH_AT=99\nCOOLDOWN_SWITCH_INDEX=3\n", encoding="utf-8")
    rc, out = _run_shell(src, root, """
_read_cooldown_state
echo "LEGACY AT=$CROSS_TOOL_SWITCH_AT IDX=$CROSS_TOOL_SWITCH_INDEX"
""")
    expect("LEGACY AT=99 IDX=3" in out,
           f"legacy KEY=value file still reads during rolling upgrade (out={out.strip()[:70]!r})")

    state.write_text(
        f'COOLDOWN_SWITCH_AT="$(touch {marker})"\nCOOLDOWN_SWITCH_INDEX=1\n',
        encoding="utf-8")
    if marker.exists():
        marker.unlink()
    rc, out = _run_shell(src, root, """
_read_cooldown_state
echo "INJECTED AT=$CROSS_TOOL_SWITCH_AT"
""")
    expect(not marker.exists() and "$(touch" in out,
           f"legacy injected text is read as data, not executed (marker={marker.exists()})")

    if marker.exists():
        marker.unlink()
    payload = f'x"$(touch {marker})"y'
    rc, out = _run_shell(src, root, f"""
_write_cooldown_state '{payload.replace("'", "'\\''")}' 2
_read_cooldown_state
echo "HOSTILE AT=$CROSS_TOOL_SWITCH_AT IDX=$CROSS_TOOL_SWITCH_INDEX"
""")
    expect(not marker.exists() and payload in out and "HOSTILE AT=" in out,
           f"hostile value survives write/read verbatim without execution (marker={marker.exists()})")

    module = src / "docs/system/workspace/scripts/runtime/state_file.py"
    if module.is_file():
        state.write_text('COOLDOWN_SWITCH_AT\t"a\\nb"\n', encoding="utf-8")
        r = subprocess.run([sys.executable, str(module), "values", str(state),
                            "COOLDOWN_SWITCH_AT"], capture_output=True, text=True, timeout=60)
        expect(r.returncode != 0 and "newline" in (r.stdout + r.stderr).lower(),
               "`values` rejects newline values instead of silently splitting")
    else:
        bad("`values` rejects newline values (module missing)")


def main() -> int:
    src = SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()
    static_checks(src)
    tmp = Path(tempfile.mkdtemp(prefix="state-family-"))
    try:
        behavior_checks(src, tmp)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
