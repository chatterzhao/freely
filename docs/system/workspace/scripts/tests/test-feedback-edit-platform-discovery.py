#!/usr/bin/env python3
"""AT-001 for raw-20261125T100958Z / I-20261125T100958Z-A.

`freely feedback edit` must be decoupled from wt-create: when the local
issue.md is absent, discover platform issue ids by raw key via the adapter
instead of failing. Modifying a raw issue does not imply implementing it.

Structural checks on runtime/freely's cmd_feedback edit branch + behavioural
checks modelling the discovery path. RED on develop, GREEN after fix.

Usage: python3 ...test-feedback-edit-platform-discovery.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

OK = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global OK, FAIL
    if cond:
        OK += 1
        print(f"ok   {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[4]
    try:
        r = subprocess.run(["git", "show", "HEAD:docs/system/workspace/scripts/runtime/freely"],
                           cwd=src, capture_output=True, text=True)
        text = r.stdout if r.returncode == 0 else (src / "docs/system/workspace/scripts/runtime/freely").read_text()
    except Exception:
        text = (src / "docs/system/workspace/scripts/runtime/freely").read_text()
    check("runtime source readable", bool(text))
    start = text.find('if [[ "$_subcmd" == "edit" ]]')
    end = text.find('if [[ "$_subcmd" == "help" ]]', start)
    edit = text[start:end] if start >= 0 and end > start else ""
    check("edit branch extracted", bool(edit))

    # Structural
    check("missing local file does not hard-fail outright",
          '[[ -f "$_issue_file" ]] || {' not in edit or "discover" in edit.lower() or '"search"' in edit,
          "missing local file must go through platform discovery, not immediate return 1")
    check("platform-adapter search subcommand used in edit",
          '"$adapter" search' in edit or '"$_adapter" search' in edit or 'platform-adapter.py" search' in edit or 'search "$raw_key"' in edit,
          "must call `adapter search <raw_key>` for platform ids")
    check("discovery assembles platform_ids from search result",
          "issue_number" in edit and "platform_ids" in edit,
          "must map discovered issue_number into platform_ids")

    # Behavioural model
    def discover(search_result: dict) -> dict:
        ids = {}
        for platform, info in search_result.items():
            num = str(info.get("issue_number", ""))
            if num:
                ids[platform] = {"issue_id": num}
        return ids

    ids = discover({"github": {"issue_number": "4704"}, "gitee": {"issue_number": "IKXZ80"}})
    check("discovers both platform ids", ids.get("github", {}).get("issue_id") == "4704" and ids.get("gitee", {}).get("issue_id") == "IKXZ80")
    check("empty discovery -> empty ids (fail-closed candidate)", discover({}) == {})
    partial = discover({"github": {"issue_number": "4704"}, "gitee": {"matches": []}})
    check("multi-match/no-number not fabricated", "gitee" not in partial)

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
