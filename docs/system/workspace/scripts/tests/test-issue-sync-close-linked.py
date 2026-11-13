#!/usr/bin/env python3
"""AT-001 (raw-20261112T131115Z): issue-sync close must work for kind=linked.

Every I-* close used to run through the strict RAW validator inside
close-platforms, which rejects a linked field set ("raw metadata fields are
missing, extra, or reordered"). Linked replicas therefore stayed OPEN forever
and the goal's final sweep step was impossible.

The check runs the real effect entry point (raw_lifecycle_effects.py) against a
fixture tree with a stub platform adapter:
  * linked + all platforms closed -> status becomes closed, every other field
    and its order preserved, adapter actually called with the platform ids;
  * partial close -> non-zero exit, document left byte-identical;
  * raw document -> close-linked refuses (kind guard);
  * close-platforms on a linked document still fails (the RAW contract was not
    relaxed to make this pass).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()

EFFECTS = "docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py"
ADAPTER = "docs/system/workspace/scripts/sync/platform-adapter.py"

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


LINKED_DOC = """---
schema_version: '1'
issue_id: I-20261112T000000Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20261112T000000Z
source_candidate: docs/B1-docs/raw-20261112T000000Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '9001'
  gitee:
    issue_id: 'IKTEST1'
primary_platform: github
created_at: '2026-11-12T00:00:00Z'
updated_at: '2026-11-12T00:00:00Z'
---

# I-20261112T000000Z-A: fixture linked issue

body stays untouched
"""

RAW_DOC = """---
schema_version: '1'
local_id: raw-20261112T000000Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261112T000000Z-A
platform_ids:
  github:
    issue_id: '9002'
primary_platform: github
canonical_issue_path: docs/B2-docs/x/issues/I-20261112T000000Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-12T00:00:00Z'
updated_at: '2026-11-12T00:00:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261112T000000Z-A
source_candidate: ''
completed_at: '2026-11-12T00:00:00Z'
closeout_note: ''
---

# fixture raw issue
"""


def sandbox(root: Path, adapter_body: str) -> None:
    target = root / ADAPTER
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(adapter_body, encoding="utf-8")
    (root / "docs/system/workspace/scripts/lifecycle").mkdir(parents=True, exist_ok=True)


def run_effect(root: Path, command: str, doc: Path) -> subprocess.CompletedProcess:
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "PYTHONPATH": str(SRC / "docs/system/workspace/scripts/lifecycle")}
    return subprocess.run(
        [sys.executable, str(SRC / EFFECTS), command, str(doc), str(root)],
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
    )


CLOSED_BOTH = "import sys, json\nprint(json.dumps({'github': {'status': 'closed'}, 'gitee': {'status': 'closed'}}))\nsys.exit(0)\n"
PARTIAL = "import sys, json\nprint(json.dumps({'github': {'status': 'closed'}, 'gitee': {'status': 'open'}}))\nsys.exit(3)\n"


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: close-linked effect ===")
    with tempfile.TemporaryDirectory(prefix="at-linked-close-") as td:
        root = Path(td)
        sandbox(root, CLOSED_BOTH)
        doc = root / "linked.md"
        doc.write_text(LINKED_DOC, encoding="utf-8")
        proc = run_effect(root, "close-linked", doc)
        text = doc.read_text(encoding="utf-8")
        check(proc.returncode == 0, "B1 close-linked succeeds when every platform closes (rc=" + str(proc.returncode) + ")")
        check("status: closed" in text, "B2 linked document records status: closed")
        check("phase_state: completed" in text, "B3 phase_state is preserved (dev completion is history)")
        check("body stays untouched" in text, "B4 body is preserved verbatim")
        check("promoted_from: raw-20261112T000000Z" in text, "B5 linked-only fields survive the rewrite")

    with tempfile.TemporaryDirectory(prefix="at-linked-partial-") as td:
        root = Path(td)
        sandbox(root, PARTIAL)
        doc = root / "linked.md"
        doc.write_text(LINKED_DOC, encoding="utf-8")
        before = doc.read_text(encoding="utf-8")
        proc = run_effect(root, "close-linked", doc)
        after = doc.read_text(encoding="utf-8")
        check(proc.returncode != 0, "B6 partial platform close exits non-zero (rc=" + str(proc.returncode) + ")")
        check(before == after, "B7 partial close leaves the document byte-identical")

    with tempfile.TemporaryDirectory(prefix="at-linked-kind-") as td:
        root = Path(td)
        sandbox(root, CLOSED_BOTH)
        raw = root / "raw.md"
        raw.write_text(RAW_DOC, encoding="utf-8")
        proc = run_effect(root, "close-linked", raw)
        check(proc.returncode != 0 and "kind: linked" in (proc.stdout + proc.stderr),
              "B8 close-linked refuses a kind: raw document")

        linked = root / "linked.md"
        linked.write_text(LINKED_DOC, encoding="utf-8")
        proc = run_effect(root, "close-platforms", linked)
        check(proc.returncode != 0 and "raw metadata" in (proc.stdout + proc.stderr),
              "B9 close-platforms still enforces the strict RAW contract")


def static_checks() -> None:
    print("=== STATIC: dispatch and wiring ===")
    close_sh = (SRC / "bin/issue-sync.d/cmd-close.sh").read_text(encoding="utf-8")
    effects = (SRC / EFFECTS).read_text(encoding="utf-8")
    check('_effect_kind' in close_sh and '"linked"' in close_sh, "S1 cmd-close branches on kind")
    check("close-linked" in close_sh, "S2 cmd-close calls the linked effect")
    check("close-platforms" in close_sh, "S3 raw still routes to close-platforms")
    check("def close_linked" in effects, "S4 close-linked effect exists")
    check('command == "close-linked"' in effects, "S5 effect is dispatched by the CLI")
    segment = ""
    if "def close_linked" in effects:
        segment = effects.split("def close_linked")[1].split("\ndef ")[0]
    check(bool(segment) and "validate(" not in segment,
          "S6 close-linked never runs the strict raw validator")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
