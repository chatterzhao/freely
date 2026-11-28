#!/usr/bin/env python3
"""AT-001 (raw-20261113T110656Z batch 1): sync+skills implementations become projections."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

TARGETS = {
    "raw-issue-pull": "docs/system/workspace/scripts/sync/raw-issue-pull",
    "issue-sync-bootstrap": "docs/system/workspace/scripts/sync/issue-sync-bootstrap",
    "deploy-skills": "docs/system/workspace/scripts/skills/deploy-skills",
}
REGISTRY = SRC / "docs/system/workspace/scripts/bin-projections.yaml"

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
    for name, rel in TARGETS.items():
        wrapper = SRC / "bin" / name
        truth = SRC / rel
        text = wrapper.read_text(encoding="utf-8", errors="replace") if wrapper.is_file() else ""
        check(len(text.splitlines()) <= 8, f"S-{name}-1 bin projection <=8 lines",
              f"got {len(text.splitlines())}")
        check(rel in text and "exec " in text, f"S-{name}-2 projection execs new truth")
        check(truth.is_file(), f"S-{name}-3 truth exists at {rel}")
        if truth.is_file():
            check(truth.stat().st_mode & 0o111 != 0, f"S-{name}-4 truth executable")

    reg = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.is_file() else {}
    paths = {e.get("path") for e in reg.get("entries", [])}
    for name in TARGETS:
        check(f"bin/{name}" not in paths, f"S-{name}-5 registry entry removed")

    r = subprocess.run([str(SRC / "bin/check-bin-projection"), "--project", str(SRC)],
                       capture_output=True, text=True, timeout=60)
    check(r.returncode == 0, "S6 check-bin-projection green", r.stderr.strip()[:200])

    parity = SRC / "docs/system/workspace/scripts/tests/test-raw-issue-pull-parity.py"
    r2 = subprocess.run([sys.executable, str(parity), "--source-dir", str(SRC)],
                        capture_output=True, text=True, timeout=120)
    check(r2.returncode == 0, "S7 raw-issue-pull parity green", r2.stdout[-200:])

    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
