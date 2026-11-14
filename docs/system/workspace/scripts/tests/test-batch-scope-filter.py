#!/usr/bin/env python3
"""AT-001 (raw-20261114T031043Z): --raw-key must actually scope the batch.

The filter used to match the ABSOLUTE path. A lane worktree is named
fix-raw-<key>-<slug>, so the prefix of every path inside it contains the key and
EVERY document looked like "this lane": one scoped run processed 288 documents
belonging to other raws (and the daemon's unscoped sweep rewrote 100+).

Fixes pinned here:
  1. the filter compares the path below /docs/, not the absolute path;
  2. batch prints its scope so the scoping is observable;
  3. the daemon's pre-scan batch passes the lane's raw key and skips entirely on
     protected branches / keyless branches (a full sweep is the governance lane's
     job, never a side effect of running 'freely').

Baseline (develop) fails all three.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

BATCH = SRC / "bin/issue-sync.d/cmd-batch.sh"
RUNTIME = SRC / "docs/system/workspace/scripts/runtime/freely"
KEY = "20261114T031043Z"
OTHER = "20260101T000000Z"

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


def fn(text: str, name: str) -> str:
    start = text.find(name + "() {")
    if start < 0:
        return ""
    end = text.find("\n}\n", start)
    return text[start:end + 3] if end > start else ""


def raw_doc(key: str) -> str:
    return f"""---
schema_version: '1'
local_id: raw-{key}
kind: raw
phase_state: absorbed
platform_state: open
---
# raw {key}
"""


def build_tree(root: Path) -> None:
    for key in (KEY, OTHER):
        d = root / "docs/B1-docs" / f"raw-{key}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "issue.md").write_text(raw_doc(key), encoding="utf-8")


def run(source: Path, filter_key: str, worktree_name: str) -> tuple:
    body = fn(read(source / BATCH), "cmd_batch")
    if not body:
        return subprocess.CompletedProcess([], 99, "", "cmd_batch not found"), []
    with tempfile.TemporaryDirectory(prefix="at-scope-") as td:
        # The crux: the project root itself carries the raw key.
        root = Path(td) / worktree_name
        build_tree(root)
        log = root / "calls.log"
        probe = root / "probe.sh"
        probe.write_text(
            "set -uo pipefail\n"
            + f"ROOT_DIR='{root}'\n"
            + f"ISSUES_DIR='{root}/docs/B1-docs'\n"
            + f"SCAN_STATE='{root}/.scan-state'\n"
            + f"CALL_LOG='{log}'\n"
            + "_fm_get() { grep -m1 \"^$2:\" \"$1\" 2>/dev/null | sed 's/^[^:]*: *//'; }\n"
            + "_scan_state_get() { echo ''; }\n"
            + "_scan_state_set() { :; }\n"
            + "_already_on_platform() { return 0; }\n"
            + "_changed_since_last_sync() { return 1; }\n"
            + "cmd_create() { echo \"CREATE $1\" >> \"$CALL_LOG\"; }\n"
            + "cmd_update() { echo \"UPDATE $1\" >> \"$CALL_LOG\"; }\n"
            + "cmd_comment() { :; }\n"
            + "cmd_close() { echo \"CLOSE $1\" >> \"$CALL_LOG\"; }\n"
            + "cmd_close_linked() { echo \"CLOSE_LINKED $1\" >> \"$CALL_LOG\"; }\n"
            + body
            + f"\ncmd_batch '{filter_key}'\n",
            encoding="utf-8",
        )
        proc = subprocess.run(["bash", str(probe)], capture_output=True, text=True,
                              timeout=120, env=dict(os.environ))
        calls = [x for x in read(log).splitlines() if x.strip()]
        return proc, calls


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: the worktree name must not defeat the scope ===")
    proc, calls = run(SRC, KEY, f"fix-raw-{KEY}-batch-scope-filter")
    check(proc.returncode == 0, f"B0 batch runs (rc={proc.returncode})")
    check(any(KEY in c for c in calls),
          "B1 the lane's own raw is processed: " + str(calls))
    check(not any(OTHER in c for c in calls),
          "B2 another raw is NOT processed even though the worktree name carries the key: " + str(calls))
    check(f"scope={KEY}" in proc.stdout, "B3 the batch prints its scope")


def static_checks() -> None:
    print("=== STATIC: daemon sweep is scoped or skipped ===")
    batch_text = read(BATCH)
    runtime = read(RUNTIME)
    check("${issue_file#*/docs/}" in batch_text,
          "S1 the filter compares the path below /docs/")
    check("scope=${filter_key:-ALL}" in batch_text, "S2 batch prints scope=<key|ALL>")
    check('batch --auto' in runtime,
          "S3 the daemon delegates scope resolution to batch --auto")
    check("main|develop|test-pre-merge-*)" in batch_text.replace(" ", ""),
          "S4 protected branches are refused inside batch --auto")
    check("governance lane" in batch_text,
          "S5 the skip message names the governance lane")
    bare = re.findall(r'bash "\$_sync_bin" batch(?![ \t]+-\-auto)', runtime)
    check(not bare, "S6 no unscoped batch call remains in the daemon hook")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    behaviour_checks()
    static_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
