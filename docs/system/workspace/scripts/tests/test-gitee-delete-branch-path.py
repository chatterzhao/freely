#!/usr/bin/env python3
"""AT-001 for raw-20261103T083757Z / #4137.

Gitee API v5 deletes a branch at DELETE /repos/{owner}/{repo}/branches/{branch}.
The old helper used the GitHub git-ref path and always returned HTTP 404.

Usage: python3 ...test-gitee-delete-branch-path.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

OK = FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global OK, FAIL
    if cond:
        OK += 1
        print(f"ok   {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def load_module(root: Path):
    path = root / "docs/system/workspace/scripts/runtime/gitee-issue.py"
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("gitee_issue_at", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    mod = load_module(root)
    source = (root / "docs/system/workspace/scripts/runtime/gitee-issue.py").read_text(encoding="utf-8")

    check("helper source readable", bool(source))
    check("no GitHub git-ref path remains", "/git/refs/heads/" not in source)
    check("Gitee branch endpoint present", "/repos/{owner}/{name}/branches/{branch}" in source)

    expected = "/repos/zhaoquan/freely/branches/fix/raw-20261103T083757Z-demo"
    actual = mod.repo_path_branch("zhaoquan/freely", "fix/raw-20261103T083757Z-demo")
    check("repo_path_branch uses canonical endpoint", actual == expected, actual)

    captured = {}

    def fake_api_request(**kwargs):
        captured.update(kwargs)
        return {"status": "204"}

    mod.api_request = fake_api_request
    result = mod.cmd_delete_branch(SimpleNamespace(repo="zhaoquan/freely",
                                                   branch="fix/raw-20261103T083757Z-demo"))
    check("delete-branch sends DELETE", captured.get("method") == "DELETE", str(captured))
    check("delete-branch sends canonical path", captured.get("path") == expected, str(captured))
    check("delete-branch still requires auth", captured.get("auth_required") is True)
    check("delete-branch returns adapter result", result == {"status": "204"})

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
