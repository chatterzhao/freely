#!/usr/bin/env python3
"""AT-001 — raw-20261110T060553Z / #4252 (phase 1: safe state protocol).

State files are written as shell assignments and read back with `source`. A
value containing `"` / `$()` / a backtick / a newline can execute code in the
daemon's context or kill the supervisor under `set -e`. AI-generated summaries,
reasons and branch names flow into those values.

Phase 1 delivers the single-owner reader/writer and freezes the migration
boundary; per-family rewriting of the 55 `source` sites is a follow-up issue.

Run against two roots:
  RED   : --source-dir /tmp/<develop-baseline>  (no safe module -> FAIL)
  GREEN : --source-dir <this worktree>
"""
from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("STATE_FILE_SOURCE_ROOT", str(PROJECT))).resolve()

PAYLOAD = 'say "hi"; $(touch {marker}); `id`\nsecond\tline'

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


def expect_plain(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


def _load(src: Path):
    path = src / "docs/system/workspace/scripts/runtime/state_file.py"
    spec = importlib.util.spec_from_file_location("state_file_probe", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["state_file_probe"] = module
    spec.loader.exec_module(module)
    return module


def static_checks(src: Path) -> None:
    print("=== STATIC: safe module and boundary lint ===")
    module = src / "docs/system/workspace/scripts/runtime/state_file.py"
    lint = src / "bin/check-state-file-sources"
    text = module.read_text(errors="replace") if module.is_file() else ""
    expect_plain(all(name in text for name in
                     ("def read_state", "def write_state", "def to_shell", "ALLOWED_KEYS"))
                 and not any(token in text for token in
                             ("eval(", "exec(", "os.system", "subprocess")),
                 "safe state module exists and contains no evaluation primitive")
    if not lint.is_file():
        bad("boundary lint passes (lint missing)")
        return
    r = subprocess.run([sys.executable, str(lint), "--project", str(src)],
                       capture_output=True, text=True, timeout=120)
    expect_plain(r.returncode == 0,
                 f"boundary lint passes on this project (rc={r.returncode})")


def behavior_checks(src: Path, tmp: Path) -> None:
    print("=== BEHAVIOR: old format injects, new protocol does not ===")
    marker = tmp / "pwned"

    # PoC 1: the legacy `source` path really executes attacker-controlled text.
    legacy = tmp / "legacy.env"
    legacy.write_text(f'LAST_EXIT_REASON="$(touch {marker})"\n', encoding="utf-8")
    subprocess.run(["bash", "-c", f'source "{legacy}"'], capture_output=True, timeout=60)
    expect_plain(marker.exists(),
                 "PoC: sourcing a legacy state file executes an injected command")

    try:
        module = _load(src)
    except Exception as exc:
        for label in ("round-trip preserves hostile values byte-for-byte",
                      "new reader does not execute injected text",
                      "unknown keys are rejected",
                      "legacy format is read verbatim without expansion",
                      "to-shell renders inert assignments"):
            bad(f"{label} (safe module unavailable: {type(exc).__name__})")
        return

    if marker.exists():
        marker.unlink()
    value = PAYLOAD.format(marker=marker)
    state = tmp / "state.tsv"
    module.write_state(state, {"LAST_EXIT_REASON": value})
    got = module.read_state(state).get("LAST_EXIT_REASON")
    expect_plain(got == value,
                 f"round-trip preserves hostile values byte-for-byte (got {got!r})")
    expect_plain(not marker.exists(),
                 "new reader does not execute injected text")

    try:
        module.write_state(tmp / "bad.tsv", {"NOT_A_REAL_KEY": "x"})
        bad("unknown keys are rejected (write accepted one)")
    except module.StateFileError:
        ok("unknown keys are rejected (write raises StateFileError)")
    (tmp / "bad.env").write_text("NOT_A_REAL_KEY=x\n", encoding="utf-8")
    try:
        module.read_state(tmp / "bad.env")
        bad("unknown keys are rejected (read accepted one)")
    except module.StateFileError:
        ok("unknown keys are rejected (read raises StateFileError)")

    legacy_raw = 'LAST_ROLE_HINT="$HOME $(id) `whoami` \'quoted\'"\n'
    (tmp / "old.env").write_text(legacy_raw, encoding="utf-8")
    old_value = module.read_state(tmp / "old.env").get("LAST_ROLE_HINT")
    expect_plain(old_value == '$HOME $(id) `whoami` \'quoted\'',
                 f"legacy format is read verbatim without expansion (got {old_value!r})")

    if marker.exists():
        marker.unlink()
    shell = module.to_shell(state)
    rendered = tmp / "rendered.sh"
    rendered.write_text(shell, encoding="utf-8")
    r = subprocess.run(["bash", "-c",
                        f'source "{rendered}"; printf "%s" "$LAST_EXIT_REASON"'],
                       capture_output=True, timeout=60)
    expect_plain(not marker.exists() and r.stdout.decode(errors="replace") == value,
                 "to-shell renders inert assignments (sourced, no execution, value intact)")


def main() -> int:
    src = SRC
    if "--source-dir" in sys.argv:
        idx = sys.argv.index("--source-dir")
        if idx + 1 < len(sys.argv):
            src = Path(sys.argv[idx + 1]).resolve()

    static_checks(src)
    tmp = Path(tempfile.mkdtemp(prefix="state-file-"))
    try:
        behavior_checks(src, tmp)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
