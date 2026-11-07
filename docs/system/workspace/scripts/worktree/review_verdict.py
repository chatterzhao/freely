#!/usr/bin/env python3
"""Single source of truth for the PR review `verdict` contract (#4150).

Consumers (all must use THIS module, never a second parser):
  - docs/system/workspace/scripts/worktree/review-verdict.sh  (bash wrapper)
  - docs/system/workspace/scripts/worktree/pr-merge-guarded   (read side)
  - bin/pr-review-guarded                                    (write side)
  - docs/system/workspace/scripts/quality/governance-merge-gate (audit side)

Contract: a review document declares exactly one verdict line, either as a
bare frontmatter key (`verdict: pass`) or a list item (`- verdict: **pass**`).
Historical documents use both forms and bold markers; all must parse.

Only the literal `pass` is a passing verdict. `fail`, `needs_changes`,
missing or unparseable declarations resolve to `unknown` (callers MUST
fail closed). The field name `verdict` is the sole contract between the
review writer and the merge reader; #4154 registers it in the contract index.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VALID = {"pass", "fail", "needs_changes"}
VERDICT_LINE = re.compile(r"^\s*[-*+]?\s*verdict\s*:\s*(.+?)\s*$", re.IGNORECASE)


def parse_verdict(text: str) -> str:
    """Return pass / fail / needs_changes / unknown (first declaration wins)."""
    for line in text.splitlines():
        match = VERDICT_LINE.match(line)
        if not match:
            continue
        value = match.group(1).strip()
        # Strip markdown emphasis, inline code, and surrounding quotes.
        value = value.replace("**", "").replace("`", "").strip()
        value = value.strip("'\"").strip().lower()
        value = value.replace(" ", "_").replace("-", "_")
        if value in VALID:
            return value
        return "unknown"
    return "unknown"


def parse_file(path: str) -> str:
    try:
        return parse_verdict(Path(path).read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", default="", help="review document path")
    parser.add_argument("--stdin", action="store_true", help="read document from stdin")
    args = parser.parse_args()
    if args.stdin:
        print(parse_verdict(sys.stdin.read()))
    elif args.file:
        print(parse_file(args.file))
    else:
        print("unknown")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
