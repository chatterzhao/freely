#!/usr/bin/env python3
"""AT-001 for raw-20261127T120426Z / I-20261127T120426Z-A (#4740).

A packaged comment-delete command must require explicit platform + comment id,
validate the local platform mapping before any write, and propagate platform
errors with an actionable retry. Callers must not use gh/curl directly.

Usage: python3 ...test-comment-delete-command.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import importlib.util
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


def load_adapter(root: Path):
    path = root / "docs/system/workspace/scripts/sync/platform-adapter.py"
    spec = importlib.util.spec_from_file_location("platform_adapter_at", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]

    def read(rel: str) -> str:
        path = root / rel
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return ""

    wrapper = read("bin/issue-sync")
    module = read("bin/issue-sync.d/cmd-comment-delete.sh")
    adapter = read("docs/system/workspace/scripts/sync/platform-adapter.py")
    gitee = read("docs/system/workspace/scripts/runtime/gitee-issue.py")
    docs = read("docs/system/workspace/commands.md")

    check("dispatcher registers comment-delete", "comment-delete) cmd_comment_delete" in wrapper)
    check("wrapper module loaded", "cmd-comment-delete.sh" in wrapper)
    check("wrapper requires explicit platform/id", "github|gitee" in module and "comment_id" in module)
    check("wrapper prints actionable retry", "retry: freely issue-sync comment-delete" in module)
    check("no caller-side gh/curl in wrapper", "gh api" not in module and "curl" not in module)
    check("adapter owns GitHub comment delete", "gh\", \"api" in adapter and "-X\", \"DELETE" in adapter)
    check("adapter validates local mapping", "no {platform} issue_id mapped" in adapter)
    check("Gitee delete-comment CLI exists", "delete-comment" in gitee)
    check("commands.md documents command", "comment-delete" in docs)

    # Behavioral: adapter refuses unmatched mapping, deletes only after validation.
    try:
        mod = load_adapter(root)
    except Exception:
        mod = None
    if mod is None or not hasattr(mod, "delete_comment"):
        for name in ("mapped platform delete succeeds", "delete called with mapped issue id",
                     "non-numeric comment id refused", "refusal did not delete",
                     "unavailable handler refused", "no extra delete on refusal"):
            check(name, False, "adapter function missing on develop")
        print(f"SUMMARY: {OK} ok, {FAIL} failed")
        return 1
    with tempfile.TemporaryDirectory(prefix="freely-comment-delete-") as td:
        tmp = Path(td)
        doc = tmp / "docs/B1-docs/raw-20261127T120426Z/issue.md"
        doc.parent.mkdir(parents=True)
        doc.write_text(
            "---\nschema_version: '1'\nlocal_id: raw-20261127T120426Z\n"
            "platform_ids:\n  github:\n    issue_id: '4740'\n"
            "  gitee:\n    issue_id: IKYKS3\n---\n\n# fix: probe\n"
        )
        os.environ["FREELY_PROJECT_ROOT"] = str(tmp)
        mod.configured_platforms = lambda: ["github", "gitee"]
        mod.search_raw_issue = lambda key: {}
        calls = []
        class Fake:
            name = "github"
            def delete_comment(self, issue_number, comment_id):
                calls.append((issue_number, comment_id))
                return {"status": "deleted"}
        mod._handler_for = lambda platform: Fake() if platform == "github" else None

        ok = mod.delete_comment("raw-20261127T120426Z", "github", "7216177311")
        check("mapped platform delete succeeds", ok.get("status") == "deleted", str(ok))
        check("delete called with mapped issue id", calls == [("4740", "7216177311")], str(calls))

        bad = mod.delete_comment("raw-20261127T120426Z", "github", "abc")
        check("non-numeric comment id refused", bad.get("status") == "error", str(bad))
        check("refusal did not delete", len(calls) == 1, str(calls))

        missing = mod.delete_comment("raw-20261127T120426Z", "gitee", "123")
        check("unavailable handler refused", missing.get("status") == "error", str(missing))
        check("no extra delete on refusal", len(calls) == 1, str(calls))

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
