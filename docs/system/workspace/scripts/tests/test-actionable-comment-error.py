#!/usr/bin/env python3
"""AT-001 for raw-20261127T110239Z / I-20261127T110239Z-A (#4737).

A closed Gitee issue must not be commented blindly, and the failure must be
explained as "issue is closed + repo issue_comment=false", not a bare HTTP 401.
promote-finalize must be idempotent across retries.

Usage: python3 ...test-actionable-comment-error.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading
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


class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)
        body = json.dumps({"error": "当前issue已关闭评论功能"}, ensure_ascii=False).encode("utf-8")
        self.send_response(401)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]

    comment = (root / "bin/issue-sync.d/cmd-comment.sh").read_text(encoding="utf-8")
    finalize = (root / "bin/issue-sync.d/cmd-promote-finalize.sh").read_text(encoding="utf-8")
    runtime = (root / "docs/system/workspace/scripts/runtime/gitee-issue.py").read_text(encoding="utf-8")

    check("cmd-comment source readable", bool(comment))
    check("Gitee closed state checked before comment", '_gitee_cli get "$gitee_id"' in comment)
    check("actionable closed-issue guidance printed",
          "issue is CLOSED and repo setting issue_comment=false" in comment)
    check("last_synced only records successful platforms", "synced_gh" in comment and "synced_gitee" in comment)
    check("promote-finalize guards duplicate comment", "closing comment already synced" in finalize)
    check("Gitee 401 translated with cause", "issue_comment` setting is false" in runtime)

    # Behavioral: real Gitee handler + stub API returning the exact 401.
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        env = dict(os.environ,
                   GITEE_API_BASE=f"http://127.0.0.1:{server.server_port}",
                   GITEE_ACCESS_TOKEN="stub-token")
        proc = subprocess.run(
            [sys.executable, str(root / "docs/system/workspace/scripts/runtime/gitee-issue.py"),
             "--repo", "zhaoquan/freely", "comment", "IKYK8N", "--body", "probe"],
            capture_output=True, text=True, env=env, timeout=20,
        )
        combined = proc.stdout + proc.stderr
        check("closed-issue POST is refused", proc.returncode != 0)
        check("error names the real cause",
              "CLOSED" in combined and "issue_comment" in combined and "can_comment" in combined,
              combined[:300])
        check("error gives an actionable fix",
              "reopen" in combined.lower() and "PATCH /repos/{owner}/{repo}" in combined,
              combined[:300])
    finally:
        server.shutdown()
        server.server_close()

    # Behavioral: promote-finalize must not push the same comment twice.
    with tempfile.TemporaryDirectory(prefix="freely-finalize-") as td:
        tmp = Path(td)
        issues = tmp / "issues" / "raw-20261127T110239Z"
        issues.mkdir(parents=True)
        doc = issues / "issue.md"
        doc.write_text(
            "---\nschema_version: '1'\nlocal_id: raw-20261127T110239Z\n"
            "promoted_children: [\"I-20261127T110239Z-A\"]\n"
            "last_synced_comment_at: {}\n---\n\n# fix: probe\n"
        )
        calls = tmp / "calls.txt"
        script = f'''
set -u
ROOT_DIR="{tmp}"
ISSUES_DIR="{tmp / 'issues'}"
_synced_state="{{}}"
_fm_get() {{
  case "$2" in
    schema_version) echo 1 ;;
    promoted_children) echo '["I-20261127T110239Z-A"]' ;;
    last_synced_comment_at) echo "$_synced_state" ;;
  esac
}}
_raw_effect() {{ :; }}
cmd_comment() {{ echo called >> "{calls}"; _synced_state="{{'github': 'x'}}"; }}
cmd_close() {{ :; }}
source "{root / 'bin/issue-sync.d/cmd-promote-finalize.sh'}"
cmd_promote_finalize raw-20261127T110239Z
cmd_promote_finalize raw-20261127T110239Z
'''
        result = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
        count = calls.read_text().count("called") if calls.exists() else 0
        check("promote-finalize comment pushed once on retry", count == 1,
              f"count={count}; stderr={result.stderr[:200]}")
        check("retry prints skip guidance", "closing comment already synced" in result.stdout,
              result.stdout[:300])

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
