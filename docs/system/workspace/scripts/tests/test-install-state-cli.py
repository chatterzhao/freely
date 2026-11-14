#!/usr/bin/env python3
"""AT-001 (raw-20261114T080106Z): install-state self-check must be a real command.

`.freely/goal-arch-debt.md` declared `install-state-check --json` as the
"eat-your-own-dogfood precondition", but `./bin/freely install-state-check`
returns `unknown command`; the real logic lives in quality/install_state.py
(called by `freely doctor`). An operator copying the documented command cannot
tell whether the installed nightly is stale.

Pinned here:
  * a thin `bin/install-state-check` projection forwards to the one true source
    (no second copy of the decision logic);
  * it is deliberately NOT wired into runtime/freely, which sits exactly at its
    27158-line budget;
  * commands.md documents the executable command;
  * forwarding is byte-faithful for both the healthy and the mismatched case.

Baseline (develop) has none of it -> red.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

CLI = SRC / "bin/install-state-check"
TRUTH = SRC / "docs/system/workspace/scripts/quality/install-state-check.py"
RUNTIME = SRC / "docs/system/workspace/scripts/runtime/freely"
COMMANDS = SRC / "docs/system/workspace/commands.md"
BUDGET = 27158

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


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=str(cwd), capture_output=True, text=True)


def static_checks() -> None:
    print("=== STATIC: thin projection, one source of truth ===")
    check(CLI.is_file(), "S1 bin/install-state-check exists")
    text = read(CLI)
    check(len(text.splitlines()) <= 40,
          "S2 projection stays under the check-bin-projection threshold")
    check("quality/install-state-check.py" in text,
          "S3 it forwards to the existing wrapper")
    check("from install_state" not in text and "check_state(" not in text,
          "S4 it does NOT copy the decision logic (no second source)")
    check("exec python3" in text, "S5 forwarding uses exec (no wrapper semantics)")

    check(len(read(RUNTIME).splitlines()) <= BUDGET,
          f"S6 runtime/freely stays within its {BUDGET}-line budget")
    check("install-state-check)" not in read(RUNTIME),
          "S7 no dispatch line was added to the monolith")

    commands = read(COMMANDS)
    check("./bin/install-state-check --json" in commands,
          "S8 commands.md documents the executable command")
    check("freely doctor" in commands and "唯一真源" in commands,
          "S9 the doctor/true-source relationship is explained")
    check("27158" in commands,
          "S10 the budget rationale is recorded, so nobody re-adds a dispatch line")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: byte-faithful forwarding ===")
    if not CLI.is_file() or not TRUTH.is_file():
        bad("B1-B4 skipped: projection or true source missing")
        return

    # Healthy path: compare the projection's JSON with the true source's JSON
    # under identical cwd/env. It must be identical whatever ok happens to be.
    a = run([str(CLI), "--json"], SRC)
    b = run([sys.executable, str(TRUTH), "--json"], SRC)
    check(a.returncode == b.returncode and a.stdout == b.stdout,
          "B1 --json output is identical to the true source (faithful forwarding)")
    try:
        payload = json.loads(a.stdout)
        check("details" in payload and "project_head" in payload["details"],
              "B2 JSON carries project_head / packaged_from details")
    except json.JSONDecodeError:
        bad("B2 projection did not emit valid JSON")

    # Mismatched state: empty install home -> non-zero + explicit fix hint.
    with tempfile.TemporaryDirectory(prefix="at-install-empty-") as td:
        c = run([str(CLI), "--json", "--home", td], SRC)
        check(c.returncode != 0, "B3 a stale/missing install state is rejected")
        try:
            bad_json = json.loads(c.stdout)
            check(bad_json.get("ok") is False and bool(bad_json.get("errors")),
                  "B4 --json reports ok:false with an error")
        except json.JSONDecodeError:
            bad("B4 no JSON on mismatch")
        d = run([str(CLI), "--home", td], SRC)
        check("freely-package --version auto --activate" in d.stderr,
              "B5 non-json output gives the repair command")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
