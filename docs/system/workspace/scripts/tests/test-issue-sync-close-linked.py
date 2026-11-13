#!/usr/bin/env python3
"""AT-001 (raw-20261113T084729Z): linked retirement is batch-only and strict.

Design intent (project sources, not guesses):
  * `bin/issue-sync` header: raw -> promotion_started(1:N) ->
    promotion_finalized -> configured-platform close.
  * `bin/issue-sync.d/cmd-batch.sh` `linked)` branch: it is the DRIVER, and
    only calls the close action when `phase_state == completed` (plus
    `_changed_since_last_sync`). `platform_state == closed` skips the issue.
  * `close_platforms` (raw) has a strict Phase 1 local validation before any
    platform write. A linked retirement must have equivalent strength, not a
    bypass.

R33.8 regression this fixes: `cmd_close` dispatched linked docs to a new
`close-linked` effect that only checked kind + platform_ids, so an `in_dev`
linked could be closed from the CLI, bypassing batch; it also introduced a
`status: closed` second source of truth instead of phase_state/platform_state.

The behavioural check runs the REAL effect entry point against a stub adapter
that records every platform call, so "zero writes on rejection" is verified,
not asserted from source text. Baseline (develop) must demonstrate the loose
behaviour.
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

EFFECTS = "docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py"
ADAPTER = "docs/system/workspace/scripts/sync/platform-adapter.py"
CMD_CLOSE = "bin/issue-sync.d/cmd-close.sh"
CMD_BATCH = "bin/issue-sync.d/cmd-batch.sh"

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


def doc(phase: str = "completed", with_paths: bool = True,
        with_ids: bool = True, kind: str = "linked") -> str:
    pre = "docs/B2-docs/x/verification/pre-tests.md" if with_paths else ""
    art = "docs/B2-docs/x/code-reviews" if with_paths else ""
    ids = "  github:\n    issue_id: '9001'\n  gitee:\n    issue_id: 'IKTEST1'" if with_ids else "{}"
    return f"""---
schema_version: '1'
issue_id: I-20261113T084729Z-A
kind: {kind}
status: completed
phase_state: {phase}
promoted_from: raw-20261113T084729Z
source_candidate: docs/B1-docs/raw-20261113T084729Z/candidates.md
canonical_issue_path: ''
platform_ids:
{ids}
primary_platform: github
last_synced_comment_at: {{}}
hash: ''
created_at: 2026-11-13T08:47:29Z
updated_at: 2026-11-13T08:47:29Z
intake_id: ''
author: platform
channel: freely-workflow-guarded-execution
session_refs: []
pre_tests_path: {pre}
verification_artifact_dir: {art}
---

# I-20261113T084729Z-A: fixture linked issue

body stays untouched
"""


CLOSED_BOTH = (
    "import sys, json, os\n"
    "with open(os.environ['ADAPTER_LOG'], 'a') as f: f.write(sys.argv[1] + '\\n')\n"
    "print(json.dumps({'github': {'status': 'closed'}, 'gitee': {'status': 'closed'}}))\n"
    "sys.exit(0)\n"
)
PARTIAL = (
    "import sys, json, os\n"
    "with open(os.environ['ADAPTER_LOG'], 'a') as f: f.write(sys.argv[1] + '\\n')\n"
    "print(json.dumps({'github': {'status': 'closed'}, 'gitee': {'status': 'open'}}))\n"
    "sys.exit(3)\n"
)


def sandbox(root: Path, adapter_body: str) -> None:
    target = root / ADAPTER
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(adapter_body, encoding="utf-8")
    (root / "docs/system/workspace/scripts/lifecycle").mkdir(parents=True, exist_ok=True)
    pre = root / "docs/B2-docs/x/verification/pre-tests.md"
    pre.parent.mkdir(parents=True, exist_ok=True)
    pre.write_text("# pre-tests\n", encoding="utf-8")
    (root / "docs/B2-docs/x/code-reviews").mkdir(parents=True, exist_ok=True)


def run_effect(source: Path, command: str, text: str,
               adapter_body: str) -> tuple[subprocess.CompletedProcess, str, str]:
    with tempfile.TemporaryDirectory(prefix="at-linked-") as td:
        root = Path(td)
        sandbox(root, adapter_body)
        doc_path = root / "linked.md"
        doc_path.write_text(text, encoding="utf-8")
        log = root / "adapter.log"
        env = dict(os.environ)
        env["ADAPTER_LOG"] = str(log)
        env["PYTHONPATH"] = str(source / "docs/system/workspace/scripts/lifecycle")
        proc = subprocess.run(
            [sys.executable, str(source / EFFECTS), command, str(doc_path), str(root)],
            capture_output=True, text=True, timeout=120, env=env,
        )
        return proc, doc_path.read_text(encoding="utf-8"), read(log)


def static_checks() -> None:
    print("=== STATIC: single retirement policy ===")
    close_sh = read(SRC / CMD_CLOSE)
    batch_sh = read(SRC / CMD_BATCH)
    effects = read(SRC / EFFECTS)
    check("linked issues are retired by 'issue-sync batch'" in close_sh,
          "S1 direct cmd_close refuses linked documents")
    check("cmd_close_linked() {" in close_sh,
          "S2 a batch-only linked close action exists")
    check('cmd_close_linked "$local_id"' in batch_sh,
          "S3 batch linked branch uses the dedicated action")
    check('close-platforms "$file"' in close_sh,
          "S4 raw still goes through the strict close-platforms effect")
    check('phase != "completed"' in effects,
          "S5 close_linked enforces phase_state == completed")
    check('metadata["platform_state"] = "closed"' in effects
          and 'metadata["status"] = "closed"' not in effects,
          "S6 retirement uses platform_state, not a new status semantic")
    check("pre_tests_path" in effects and "verification_artifact_dir" in effects,
          "S7 B2 evidence paths are validated before any write")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: real effect + recording stub adapter ===")
    proc, after, _ = run_effect(SRC, "close-linked", doc(), CLOSED_BOTH)
    check(proc.returncode == 0, "B1 a completed linked issue is retired (rc=" + str(proc.returncode) + ")")
    check("platform_state: closed" in after, "B2 platform_state is written so batch skips it")
    check("status: closed" not in after, "B3 no second source of truth is introduced")
    check("phase_state: completed" in after, "B4 phase_state stays the batch predicate")
    check("body stays untouched" in after, "B5 document body preserved")

    proc, after, log = run_effect(SRC, "close-linked", doc(phase="in_dev"), CLOSED_BOTH)
    check(proc.returncode != 0 and "not completed" in (proc.stdout + proc.stderr),
          "B6 an in_dev linked issue is refused")
    check(log.strip() == "", "B7 refusal performs ZERO platform writes (adapter not called)")

    proc, _, log = run_effect(SRC, "close-linked", doc(with_paths=False), CLOSED_BOTH)
    check(proc.returncode != 0 and "pre_tests_path" in (proc.stdout + proc.stderr),
          "B8 missing B2 evidence paths are refused")
    check(log.strip() == "", "B9 path refusal performs ZERO platform writes")

    proc, before_after, _ = run_effect(SRC, "close-linked", doc(), PARTIAL)
    check(proc.returncode != 0 and "platform_state: closed" not in before_after,
          "B10 partial platform close leaves local state unchanged")

    proc, _, _ = run_effect(SRC, "close-linked", doc(kind="raw"), CLOSED_BOTH)
    check(proc.returncode != 0 and "kind: linked" in (proc.stdout + proc.stderr),
          "B11 close-linked refuses kind: raw")

    proc, _, _ = run_effect(SRC, "close-platforms", doc(), CLOSED_BOTH)
    check(proc.returncode != 0 and "raw metadata" in (proc.stdout + proc.stderr),
          "B12 close-platforms still enforces the strict RAW contract")


def baseline_checks() -> None:
    if BASE is None:
        return
    print("=== BASELINE CONTROL: develop loose retirement ===")
    proc, after, log = run_effect(BASE, "close-linked", doc(phase="in_dev"), CLOSED_BOTH)
    check(proc.returncode == 0 and log.strip() != "",
          "R1 develop really retires an in_dev linked issue (RED is real)")
    check("status: closed" in after,
          "R2 develop really writes the second status semantic")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    baseline_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
