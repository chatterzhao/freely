#!/usr/bin/env python3
"""AT-001 for raw-20261124T131119Z / I-20261124T131119Z-A.

A packaged command must exist to close every OPEN platform replica of a local
id — including stale linked orphans absent from the document mapping — without
callers importing the adapter or hand-assembling platform_ids. Partial results
must stay non-zero and print the exact retry command.

Usage: python3 ...test-close-orphans-command.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

OK = FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global OK, FAIL
    if cond:
        OK += 1
        print(f"ok   {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def run_bash(fixture: Path, root: Path, source: Path, stub_rc: int) -> subprocess.CompletedProcess:
    script = f"""
set -u
source "{source}"
_issue_file_for() {{ printf '%s\\n' "{fixture / 'issue.md'}"; }}
ROOT_DIR="{fixture}"
STUB_RC={stub_rc}
cmd_close_orphans I-20261124T054201Z-A linked
"""
    env = dict(os.environ, STUB_RC=str(stub_rc))
    return subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env)


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    cmd = root / "bin/issue-sync.d/cmd-close.sh"
    dispatcher = root / "bin/issue-sync"
    docs = root / "docs/system/workspace/commands.md"
    text = cmd.read_text(encoding="utf-8")

    check("command module readable", bool(text))
    check("packaged close-orphans defined", "cmd_close_orphans()" in text)
    check("dispatcher registers close-orphans", "close-orphans) cmd_close_orphans" in dispatcher.read_text(encoding="utf-8"))
    check("commands.md documents close-orphans", "close-orphans" in docs.read_text(encoding="utf-8"))
    check("no caller-side adapter import", "import platform_adapter" not in text)
    check("delegates to adapter close-local-id", "close-local-id" in text)
    check("retry command is actionable", "retry: freely issue-sync close-orphans" in text)

    with tempfile.TemporaryDirectory(prefix="freely-close-orphans-") as td:
        fixture = Path(td)
        adapter_dir = fixture / "docs/system/workspace/scripts/sync"
        adapter_dir.mkdir(parents=True)
        (adapter_dir / "platform-adapter.py").write_text(
            "import json, os\n"
            "print(json.dumps({'github': {'status': 'closed', 'issue_ids': ['4678']},"
            " 'gitee': {'status': 'absent', 'issue_ids': []}}))\n"
            "raise SystemExit(int(os.environ.get('STUB_RC', '0')))\n"
        )
        (fixture / "issue.md").write_text(
            "---\nschema_version: '1'\nlocal_id: I-20261124T054201Z-A\nkind: linked\n"
            "platform_ids:\n  github:\n    issue_id: '4678'\n"
            "    url: https://github.com/chatterzhao/freely/issues/4678\n"
            "    synced_at: ''\n---\n\n# stale orphan\n"
        )
        for rc, expected in ((0, 0), (3, 3), (1, 1)):
            result = run_bash(fixture, root, cmd, rc)
            check(f"adapter rc={rc} propagates", result.returncode == expected,
                  f"got {result.returncode}: {result.stderr[:120]}")
            if rc == 0:
                check("success receipt", "close-orphans complete" in result.stdout)
            else:
                check(f"rc={rc} prints actionable retry",
                      "retry: freely issue-sync close-orphans I-20261124T054201Z-A linked" in result.stderr)

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
