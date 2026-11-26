#!/usr/bin/env python3
"""AT-001 for raw-20261126T114403Z / #4722.

Batch mode must read platform OPEN records once, close every terminal local id,
and preserve the 0/3/1 exit-code contract with an actionable retry command.

Usage: python3 ...test-close-orphans-batch.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
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


def run_batch(root: Path, source: Path, fixture: Path, stub_rc: int) -> subprocess.CompletedProcess:
    script = f"""
set -u
source "{source}"
ROOT_DIR="{fixture}"
ISSUES_DIR="{fixture / 'issues'}"
STUB_RC={stub_rc}
cmd_close_orphans_all linked
"""
    env = dict(os.environ, STUB_RC=str(stub_rc))
    return subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env)


def write_fixture(fixture: Path, source: Path) -> None:
    issues = fixture / "issues"
    issues.mkdir(parents=True, exist_ok=True)
    adapter_dir = fixture / "docs/system/workspace/scripts/sync"
    adapter_dir.mkdir(parents=True)
    stub = adapter_dir / "platform-adapter.py"
    stub.write_text(
        "import json, os, sys\n"
        "ids = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []\n"
        "calls = os.environ['FIXTURE_CALL_LOG']\n"
        "open(calls, 'a').write('x\\n')\n"
        "open(os.environ['FIXTURE_IDS'], 'w').write(json.dumps(ids))\n"
        "print(json.dumps({i: {'github': {'status': 'closed', 'issue_ids': []}, "
        "'gitee': {'status': 'closed', 'issue_ids': []}} for i in ids}))\n"
        "raise SystemExit(int(os.environ.get('STUB_RC', '0')))\n",
        encoding="utf-8",
    )
    specs = [
        ("raw-20260101T000001Z", "completed"),
        ("raw-20260101T000002Z", "dropped"),
        ("raw-20260101T000003Z", "proposed"),
    ]
    for local_id, phase in specs:
        folder = issues / local_id
        folder.mkdir(parents=True)
        (folder / "issue.md").write_text(
            f"---\nschema_version: '1'\nlocal_id: {local_id}\nkind: raw\nphase_state: {phase}\n---\n\n# {local_id}\n",
            encoding="utf-8",
        )
    b2 = fixture / "docs/B2-docs/demo/raw-20260101T000001Z/issues/I-20260101T000001Z-A.md"
    b2.parent.mkdir(parents=True)
    b2.write_text(
        "---\nschema_version: '1'\nlocal_id: I-20260101T000001Z-A\nkind: linked\nphase_state: completed\n---\n\n# linked\n",
        encoding="utf-8",
    )


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    cmd = root / "bin/issue-sync.d/cmd-close.sh"
    dispatcher = root / "bin/issue-sync"
    adapter = root / "docs/system/workspace/scripts/sync/platform-adapter.py"
    docs = root / "docs/system/workspace/commands.md"
    text = cmd.read_text(encoding="utf-8") if cmd.is_file() else ""

    check("batch helper defined", "cmd_close_orphans_all()" in text)
    check("dispatcher registers --all-completed", "--all-completed" in dispatcher.read_text(encoding="utf-8"))
    check("commands.md documents --all-completed", "--all-completed" in docs.read_text(encoding="utf-8"))
    check("adapter registers close-local-ids", "close-local-ids" in adapter.read_text(encoding="utf-8"))
    check("no caller-side adapter import", "import platform_adapter" not in text)
    check("single-id mode preserved", "cmd_close_orphans()" in text)

    with tempfile.TemporaryDirectory(prefix="freely-close-orphans-batch-") as td:
        fixture = Path(td)
        write_fixture(fixture, root)
        call_log = fixture / "calls.log"
        ids_out = fixture / "ids.json"
        for rc in (0, 3, 1):
            call_log.write_text("", encoding="utf-8")
            env_extra = dict(os.environ, FIXTURE_CALL_LOG=str(call_log), FIXTURE_IDS=str(ids_out))
            os.environ.update(env_extra)
            result = run_batch(root, cmd, fixture, rc)
            os.environ.pop("FIXTURE_CALL_LOG", None)
            os.environ.pop("FIXTURE_IDS", None)
            os.environ.pop("STUB_RC", None)
            tag = f"rc={rc}"
            check(f"{tag} exit code propagates", result.returncode == rc,
                  f"got {result.returncode}: {result.stderr[:200]}")
            check(f"{tag} platform records read once", len(call_log.read_text().splitlines()) == 1)
            ids = json.loads(ids_out.read_text(encoding="utf-8")) if ids_out.exists() else []
            check(f"{tag} only terminal ids sent", "raw-20260101T000001Z" in ids
                  and "raw-20260101T000002Z" in ids
                  and "raw-20260101T000003Z" not in ids, str(ids))
            if rc == 0:
                check(f"{tag} success receipt", "close-orphans --all-completed" in result.stdout)
            else:
                check(f"{tag} actionable retry",
                      "retry: freely issue-sync close-orphans --all-completed" in result.stderr,
                      result.stderr[:200])

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
