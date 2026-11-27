#!/usr/bin/env python3
"""AT-001 for raw-20261127T131717Z / I-20261127T131717Z-A (#4743).

Platform identity is defined by canonical title prefixes, not by any mention
of a raw key in an issue body. Body references must never create false
ambiguity that blocks issue-sync create.

Usage: python3 ...test-title-only-identity.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
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


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    path = root / "docs/system/workspace/scripts/sync/platform-adapter.py"
    source = path.read_text(encoding="utf-8")

    check("adapter source readable", bool(source))
    check("identity helper defined", "def is_identity_title" in source)
    check("GitHub title query only", '"raw-{raw_key} in:title"' in source)
    check("no body search in identity path", "needle not in body.lower()" not in source
          and 'for field in ("title", "body")' not in source)

    spec = importlib.util.spec_from_file_location("platform_adapter_identity_at", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    key = "20261108T134701Z"
    if not hasattr(mod, "is_identity_title"):
        for name in ("canonical RAW prefix accepted", "canonical linked prefix accepted",
                     "case-insensitive prefix accepted", "body mention with no prefix rejected",
                     "different key rejected", "only canonical title matches returned",
                     "body-only candidate ignored"):
            check(name, False, "identity helper missing on develop")
        print(f"SUMMARY: {OK} ok, {FAIL} failed")
        return 1

    check("canonical RAW prefix accepted",
          mod.is_identity_title(f"[RAW-{key}] fix: install parity", key))
    check("canonical linked prefix accepted",
          mod.is_identity_title(f"[I-{key}-A] fix: install parity", key))
    check("case-insensitive prefix accepted",
          mod.is_identity_title(f"[raw-{key}] fix", key))
    check("body mention with no prefix rejected",
          not mod.is_identity_title("fix: see raw-" + key + " in body", key))
    check("different key rejected",
          not mod.is_identity_title("[RAW-20261127T100325Z] fix", key))

    # Behavioral: GitHub handler must filter fp gh candidates by title identity.
    handler = mod.GitHubHandler()
    handler._repo = lambda: "chatterzhao/freely"
    import subprocess
    original_run = subprocess.run
    payload = json.dumps([
        {"number": 1, "title": f"[RAW-{key}] fix: real", "url": "u1"},
        {"number": 2, "title": "fix: mentions raw-" + key, "url": "u2"},
        {"number": 3, "title": f"[I-{key}-A] linked", "url": "u3"},
    ])
    class Result:
        returncode = 0
        stdout = payload
    mod.subprocess.run = lambda *a, **k: Result()
    try:
        found = handler.search_raw_issue(key)
    finally:
        mod.subprocess.run = original_run
    ids = sorted(str(x.get("issue_number", "")) for x in (found.get("matches") or []))
    check("only canonical title matches returned", ids == ["1", "3"], str(ids))
    check("body-only candidate ignored", "2" not in ids, str(ids))

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
