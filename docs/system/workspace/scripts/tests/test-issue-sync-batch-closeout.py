#!/usr/bin/env python3
"""AT-001 (raw-20261113T130925Z): issue-sync batch must actually process linked
documents and close completed ones regardless of the change hash.

Two real defects it pins:
  1. local_id for a B2 document was basename(dirname(file)) == "issues", so the
     raw-*/I-* guard skipped EVERY linked document. batch never processed one.
  2. close was nested inside _changed_since_last_sync, which returns unchanged
     when no hash exists - so a completed linked was never closed on first sync.

Baseline (develop) must call __none__ of the close hooks.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()
BASE = Path(sys.argv[sys.argv.index("--baseline") + 1]) if "--baseline" in sys.argv else None

BATCH = "bin/issue-sync.d/cmd-batch.sh"
KEY = "20261113T130925Z"
CHILD = f"I-{KEY}-A"

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


def raw_doc() -> str:
    return f"""---
schema_version: '1'
local_id: raw-{KEY}
kind: raw
phase_state: absorbed
absorbed_into: {CHILD}
platform_state: closed
platform_ids:
  github:
    issue_id: '9000'
promoted_children:
- {CHILD}
---

# raw fixture
"""


def child_doc(phase: str, pstate: str) -> str:
    ps = f"platform_state: {pstate}\n" if pstate else ""
    return f"""---
schema_version: '1'
issue_id: {CHILD}
kind: linked
phase_state: {phase}
{ps}platform_ids:
  github:
    issue_id: '9001'
---

# child fixture
"""


def run(source: Path, phase="completed", pstate="", changed=False) -> tuple:
    text = read(source / BATCH)
    body = fn(text, "cmd_batch")
    fmg = fn(read(source / "docs/system/workspace/scripts/worktree/wt-close"), "_fm_get")
    if not body or not fmg:
        return subprocess.CompletedProcess([], 99, "", "cmd_batch/_fm_get not found"), 0
    with tempfile.TemporaryDirectory(prefix="at-batch-") as td:
        root = Path(td)
        rdir = root / "docs/B1-docs" / f"raw-{KEY}"
        rdir.mkdir(parents=True)
        (rdir / "issue.md").write_text(raw_doc(), encoding="utf-8")
        cdir = root / "docs/B2-docs/epic/story" / f"raw-{KEY}" / "issues"
        cdir.mkdir(parents=True)
        (cdir / f"{CHILD}.md").write_text(child_doc(phase, pstate), encoding="utf-8")
        log = root / "calls.log"
        probe = root / "probe.sh"
        probe.write_text(
            "set -uo pipefail\n"
            + fmg + "\n"
            + f"ROOT_DIR='{root}'\n"
            + f"ISSUES_DIR='{root / 'docs/B1-docs'}'\n"
            + f"SCAN_STATE='{root / '.scan-state'}'\n"
            + f"CALL_LOG='{log}'\n"
            + "_scan_state_get(){ echo ''; }\n"
            + "_scan_state_set(){ :; }\n"
            + "_already_on_platform(){ return 0; }\n"
            + f"_changed_since_last_sync(){{ return {'0' if changed else '1'}; }}\n"
            + "cmd_create(){ echo \"CREATE $1\" >> \"$CALL_LOG\"; }\n"
            + "cmd_update(){ echo \"UPDATE $1\" >> \"$CALL_LOG\"; }\n"
            + "cmd_comment(){ :; }\n"
            + "cmd_close(){ echo \"CLOSE $1\" >> \"$CALL_LOG\"; }\n"
            + "cmd_close_linked(){ echo \"CLOSE_LINKED $1\" >> \"$CALL_LOG\"; }\n"
            + body + "\ncmd_batch\n",
            encoding="utf-8",
        )
        proc = subprocess.run(["bash", str(probe)], capture_output=True, text=True,
                              timeout=120, env=dict(os.environ), cwd=str(root))
        calls = [x for x in read(log).splitlines() if x.strip()]
        return proc, calls


def static_checks() -> None:
    print("=== STATIC: linked ids + state predicate ===")
    text = read(SRC / BATCH)
    check("*/issues/I-*.md) local_id=$(basename \"$issue_file\" .md)" in text,
          "S1 linked document id is derived from the file name")
    linked = text.split("linked)")[1] if "linked)" in text else ""
    close_pos = linked.find("cmd_close_linked")
    hash_pos = linked.find("_changed_since_last_sync")
    check(close_pos >= 0 and hash_pos >= 0 and close_pos < hash_pos,
          "S2 close is decided before (and independently of) the change hash")
    check('"$phase" == "completed" && "$pstate" != "closed"' in linked.replace("  ", " "),
          "S3 the closure predicate is completed && platform_state != closed")
    check("batch: close" in linked, "S4 the close is reported with its id")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: real cmd_batch in a sandbox project ===")
    p, calls = run(SRC)
    check(p.returncode == 0 and any(c.startswith("CLOSE_LINKED " + CHILD) for c in calls),
          "B1 completed linked is closed on first sync (no hash): " + str(calls))

    p, calls = run(SRC, phase="in_dev")
    check(not any(c.startswith("CLOSE_LINKED") for c in calls),
          "B2 an in_dev linked is not closed: " + str(calls))

    p, calls = run(SRC, pstate="closed")
    check(not any(c.startswith("CLOSE_LINKED") for c in calls),
          "B3 an already-closed linked is not re-closed: " + str(calls))

    p, calls = run(SRC, changed=True)
    check(any(c.startswith("UPDATE " + CHILD) for c in calls)
          and any(c.startswith("CLOSE_LINKED " + CHILD) for c in calls),
          "B4 changed content still updates, and close still happens: " + str(calls))


def baseline_checks() -> None:
    if BASE is None:
        return
    print("=== BASELINE CONTROL: develop batch ===")
    p, calls = run(BASE)
    check(not any(c.startswith("CLOSE_LINKED") for c in calls),
          "R1 develop never processes the linked document (id guard skipped it): " + str(calls))


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    baseline_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
