#!/usr/bin/env python3
"""AT-001 (raw-20261108T134701Z): documented command names must exist.

`bin/freely` used to promise `freely install` and automatic removal of the
`# @freely-dev-path` marker. Neither command exists: the real activation path
is `freely-package --version auto --activate`. This test pins both the
documentation fix and a reusable, fail-closed static contract checker.

Baseline (develop) still carries the false promise -> RED.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

BIN_FREELY = SRC / "bin/freely"
COMMANDS = SRC / "docs/system/workspace/commands.md"
RUNTIME = SRC / "docs/system/workspace/scripts/runtime/freely"
CHECKER = SRC / "docs/system/workspace/scripts/quality/command_name_contract.py"
BUDGET = 27166

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


def main() -> None:
    print("AT-001 source: " + str(SRC))
    header = read(BIN_FREELY)
    commands = read(COMMANDS)

    print("=== STATIC: no unimplemented command promise ===")
    check("freely install" not in header,
          "S1 bin/freely no longer promises 'freely install'")
    check("freely-package --activate" in header or "freely-package --version" in header,
          "S2 prod-mode comment points at the real activation command")
    marker_lines = [ln for ln in header.splitlines() if "@freely-dev-path" in ln]
    check(bool(marker_lines) and all("auto-remove" not in ln.lower() and "自动移除" not in ln
                                     for ln in marker_lines),
          "S3 dev-path marker no longer promises automatic removal")
    check("freely-package --version auto --activate" in commands,
          "S4 commands.md documents the real activation command")

    print("=== CONTRACT: reusable checker exists and is fail-closed ===")
    check(CHECKER.is_file(), "S5 command_name_contract.py exists")
    if CHECKER.is_file():
        self_test = subprocess.run([sys.executable, str(CHECKER), "--self-test"],
                                   capture_output=True, text=True)
        check(self_test.returncode == 0,
              "S6 checker self-test passes (valid command accepted, fake one rejected)")
        live = subprocess.run([sys.executable, str(CHECKER), "--root", str(SRC)],
                              capture_output=True, text=True)
        check(live.returncode == 0,
              "S7 checker passes on the current repository: " + live.stderr.strip()[:160])
    else:
        bad("S6 checker self-test skipped: checker missing")
        bad("S7 checker live run skipped: checker missing")

    print("=== REGRESSION: runtime budget untouched ===")
    check(len(read(RUNTIME).splitlines()) <= BUDGET,
          f"S8 runtime/freely stays within {BUDGET} lines")
    check("install)" not in read(RUNTIME),
          "S9 no install dispatch was added to runtime/freely")

    # Guard against a checker that hard-codes only the known-bad token.
    check(bool(re.search(r"freely\s+[a-z][a-z0-9-]*", header + commands)),
          "S10 there are real 'freely <cmd>' promises to check")

    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
