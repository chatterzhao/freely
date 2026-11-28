#!/usr/bin/env python3
"""AT-001 (raw-20261113T141456Z): governance-only lane must be executable.

Pins: config.toml is the single allowlist source; GATE 1 mismatch diagnosis
names the lane and the exact skip command; issue-sync batch accepts --raw-key
and warns that an unscoped sweep is a cross-raw governance write.
"""
from __future__ import annotations

import importlib.util
from importlib.machinery import SourceFileLoader
import os
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

GATE = SRC / "docs/system/workspace/scripts/quality/governance-merge-gate"
BATCH = SRC / "bin/issue-sync.d/cmd-batch.sh"
DISPATCH = SRC / "bin/issue-sync"

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
    gate_text = GATE.read_text(encoding="utf-8", errors="replace")
    batch_text = BATCH.read_text(encoding="utf-8", errors="replace")
    dispatch_text = DISPATCH.read_text(encoding="utf-8", errors="replace")

    print("=== source contract ===")
    check("L2: hardcoded defaults" not in gate_text,
          "S1 hardcoded fallback allowlist removed")
    check("FREELY_SKIP_IBM_GATE" in gate_text[gate_text.find("_gate1_mismatch_msg"):gate_text.find("_gate1_mismatch_msg")+1800],
          "S2 GATE 1 mismatch diagnosis names the skip command")
    check("--raw-key" in batch_text, "S3 batch accepts --raw-key")
    check("governance-only lane" in batch_text, "S4 unscoped batch warns about governance lane")
    check("cmd_batch \"$local_id\" \"$extra\"" in dispatch_text,
          "S5 batch dispatcher forwards the second argument")

    print("=== behavioural ===")
    os.chdir(SRC)
    spec = importlib.util.spec_from_loader("gate_mod", SourceFileLoader("gate_mod", str(GATE)))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    check(mod.is_governance_only_path("docs/B1-docs/raw-x/issue.md"),
          "B1 configured governance path allowed")
    check(not mod.is_governance_only_path("docs/system/workspace/skills/foo.md"),
          "B2 unconfigured hardcoded path rejected (single source)")
    check(not mod.is_governance_only_path("bin/freely"),
          "B3 implementation path never allowed")

    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
