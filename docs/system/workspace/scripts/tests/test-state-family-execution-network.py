#!/usr/bin/env python3
"""AT-001 — raw-20261110T081029Z / #4261 (family 2: execution-network-recovery.env).

Second concrete migration of the state-file protocol delivered in #4252 and
first migrated in #4258. `persist_execution_network_state` used to write a
shell-assignment heredoc (interpolating a log-derived reason), and two readers
(`runtime_network_failure_reason_from_log`, `execution_network_launch_block_active`)
used `source`. A value containing `"`, `$()` or a backtick therefore executes
in the daemon's context.

This family now writes TAB + JSON via `state_file.py write --kv` and reads via
`state_file.py values`. The legacy KEY=value shape is still readable, verbatim
and WITHOUT expansion, so a rolling upgrade needs no manual cleanup.

The AT sources the REAL `runtime/freely` and calls the real functions, so it
covers the whole shell <-> python boundary, not just the module.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>  (heredoc + source -> FAIL)
  GREEN : --source-dir <this worktree>
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[5]
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


def _block(text: str, start: str, end: str) -> str:
    if start not in text:
        return ""
    return text.split(start, 1)[-1].split(end, 1)[0]


def static_checks(src: Path) -> None:
    print("=== STATIC: family migrated, global count dropped ===")
    freely_path = src / "docs/system/workspace/scripts/runtime/freely"
    freely = freely_path.read_text(errors="replace") if freely_path.is_file() else ""

    write_block = _block(freely, "persist_execution_network_state() {",
                         "clear_execution_network_state()")
    expect(bool(write_block) and "cat >" not in write_block
           and "STATE_FILE_PY" in write_block and "--kv" in write_block,
           "writer no longer interpolates a heredoc; writes via state_file.py --kv")

    reader_block = _block(freely, "execution_network_launch_block_active() {",
                          "log_has_codex_usage_limit()")
    expect(bool(reader_block) and "source \"$state_file\"" not in reader_block
           and "STATE_FILE_PY" in reader_block and "values" in reader_block,
           "launch-block reader no longer sources the state file")

    # This span contains BOTH readers (failure-reason and launch-block); both
    # must be free of `source` and use `values`.
    reason_block = _block(freely, "runtime_network_failure_reason_from_log() {",
                          "log_has_codex_usage_limit()")
    expect("source \"$state_file\"" not in reason_block and "values" in reason_block,
           "failure-reason reader no longer sources the state file")

    lint = src / "bin/check-state-file-sources"
    if not lint.is_file():
        bad("boundary lint passes and count dropped 54 -> 52 (lint missing)")
        return
    r = subprocess.run([sys.executable, str(lint), "--project", str(src)],
                       capture_output=True, text=True, timeout=120)
    count = re.search(r"call sites:\s*(\d+)", r.stdout)
    got = int(count.group(1)) if count else -1
    # Monotone guard: strictly below the 54 inherited from #4258, not pinned to
    # 52. Later family migrations lower it further without turning this AT red.
    expect(r.returncode == 0 and 0 < got < 54,
           f"boundary lint passes and global state sources dropped below 54 "
           f"(got {got}, rc={r.returncode})")

    # the one coupled regression must be format-agnostic (assert values, not shape)
    test = src / "docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification"
    if test.is_file():
        t = test.read_text(errors="replace")
        expect("grep -q '^EXECUTION_NETWORK_REASON=" not in t
               and "state_file.py" in t and "values" in t,
               "coupled regression asserts values through the protocol, not grep on KEY=\"...\"")
    else:
        bad("coupled regression asserts values through the protocol (test missing)")


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
    state = root / ".freely" / "run" / "execution-network-recovery.env"
    marker = root / "marker"
    module = src / "docs/system/workspace/scripts/runtime/state_file.py"

    # 1) normal values round-trip through the real writer and the real reader
    rc, out = _run_shell(src, root, """
persist_execution_network_state "$PROJECT_ROOT" "execution_network_persistent" 3 9999999999 1700000000
execution_network_launch_block_active "$PROJECT_ROOT" "execution_network_persistent"
echo "BLOCK_RC=$?"
""")
    expect("BLOCK_RC=0" in out,
           f"normal values round-trip; future retry epoch keeps block active (out={out.strip()[-90:]!r})")

    if state.exists():
        body = state.read_text(encoding="utf-8")
        expect("\t" in body
               and re.search(r'EXECUTION_NETWORK_REASON\t"execution_network_persistent"', body) is not None,
               "written file uses the non-executable TAB + JSON format")
    else:
        bad("written file uses the non-executable TAB + JSON format (file missing)")

    # 2) legacy KEY=value is still readable during rolling upgrade
    state.write_text(
        'EXECUTION_NETWORK_REASON="proxy_config_invalid"\n'
        'EXECUTION_NETWORK_NEXT_RETRY_EPOCH=9999999999\n', encoding="utf-8")
    rc, out = _run_shell(src, root, """
execution_network_launch_block_active "$PROJECT_ROOT" "proxy_config_invalid"
echo "LEGACY_BLOCK_RC=$?"
""")
    expect("LEGACY_BLOCK_RC=0" in out,
           f"legacy KEY=value file still reads during rolling upgrade (out={out.strip()[-90:]!r})")

    # 3) legacy injected text must be DATA, never executed
    state.write_text(
        f'EXECUTION_NETWORK_REASON="$(touch {marker})"\n'
        'EXECUTION_NETWORK_NEXT_RETRY_EPOCH=9999999999\n', encoding="utf-8")
    if marker.exists():
        marker.unlink()
    rc, out = _run_shell(src, root, """
execution_network_launch_block_active "$PROJECT_ROOT" "execution_network_transient"
echo "INJECTED_RC=$?"
""")
    expect(not marker.exists(),
           f"legacy injected text is read as data, not executed (marker={marker.exists()})")

    # 4) a hostile value written by the new writer survives verbatim, no execution
    if marker.exists():
        marker.unlink()
    payload = f'x"$(touch {marker})"`id`y'
    escaped = payload.replace("'", "'\\''")
    rc, out = _run_shell(src, root, f"""
persist_execution_network_state "$PROJECT_ROOT" '{escaped}' 1 9999999999 1700000000
""")
    if module.is_file():
        r = subprocess.run([sys.executable, str(module), "values", str(state),
                            "EXECUTION_NETWORK_REASON"], capture_output=True, text=True, timeout=60)
        got = r.stdout.rstrip("\n")
        expect(not marker.exists() and got == payload,
               f"hostile value survives write/read verbatim without execution "
               f"(marker={marker.exists()}, got={got[:60]!r})")
    else:
        bad("hostile value survives write/read verbatim (module missing)")

    # 5) `values` rejects a newline instead of silently splitting (guard)
    if module.is_file():
        state.write_text('EXECUTION_NETWORK_REASON\t"a\\nb"\n', encoding="utf-8")
        r = subprocess.run([sys.executable, str(module), "values", str(state),
                            "EXECUTION_NETWORK_REASON"], capture_output=True, text=True, timeout=60)
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
    tmp = Path(tempfile.mkdtemp(prefix="state-family-en-"))
    try:
        behavior_checks(src, tmp)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
