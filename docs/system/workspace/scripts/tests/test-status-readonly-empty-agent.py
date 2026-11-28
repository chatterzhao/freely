#!/usr/bin/env python3
"""AT-001 (raw-20261113T141512Z): read-only status must tolerate empty agent_working.

Baseline: `freely status --view live --project <tree>` exits 1 because
load_config() applies the write-path identity fail-closed rule to a read-only
view. GREEN: rc=0 with issue sections, while write paths stay fail-closed.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

RUNTIME = SRC / "docs/system/workspace/scripts/runtime/freely"
SCAN = SRC / "bin/issue-sync.d/cmd-scan.sh"

OK = 0
BAD = 0


def check(cond: bool, label: str, detail: str = "") -> None:
    global OK, BAD
    if cond:
        OK += 1
        print("  [ok] " + label)
    else:
        BAD += 1
        print("  [FAIL] " + label + (" — " + detail if detail else ""))


def main() -> None:
    print("AT-001 source: " + str(SRC))
    text = RUNTIME.read_text(encoding="utf-8", errors="replace") if RUNTIME.is_file() else ""

    print("=== source contract ===")
    check("FREELY_READONLY_VIEW" in text, "S1 read-only view marker exists")
    lines = text.splitlines()
    guarded = any("agent_working empty" in ln and i + 1 < len(lines)
                  and "FREELY_READONLY_VIEW" in lines[i - 1]
                  for i, ln in enumerate(lines))
    check(guarded, "S2 load_config empty-table guard is read-only-aware")
    check("agent-table: unable to resolve agent identity for $project — fail-closed" in text,
          "S3 write-path identity fail-closed preserved")
    scan_text = SCAN.read_text(encoding="utf-8", errors="replace") if SCAN.is_file() else ""
    check("_already_on_platform" in scan_text,
          "S4 scan uses platform truth for raw CREATE judgment (#4699)")

    print("=== behaviour ===")
    r = subprocess.run([str(SRC / "bin/freely"), "status", "--view", "live",
                        "--project", str(SRC)], capture_output=True, text=True, timeout=120)
    check(r.returncode == 0, "B1 status --view live returns 0 on empty agent_working",
          f"rc={r.returncode} stderr={r.stderr.strip()[:200]}")
    check("project:" in r.stdout and "branch:" in r.stdout,
          "B2 read-only view still prints status sections")

    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
