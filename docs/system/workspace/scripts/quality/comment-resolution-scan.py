#!/usr/bin/env python3
"""Single-process replacement for pr-create-guarded Step 2e.

Historical implementation::

    for _raw_file in $(find docs/B1-docs -maxdepth 2 -name issue.md -path "*/raw-*"); do
      _raw_text="$(cat "$_raw_file")"
      _unresolved=$(echo "$_raw_text" | grep -c "^### comment-" || true)
      _resolved=$(echo "$_raw_text" | grep -c "^#### resolution-" || true)
      ...
    done

That is ~5 subprocesses per file (803 files = ~4000 processes, ~188s here).
This module does the same scan in one process (measured 0.22s).

Zero-semantics-change contract:
  * file set is ``docs/B1-docs/raw-*/issue.md`` (verified identical to find)
  * counts are line-matching counts of ``^### comment-`` / ``^#### resolution-``
    (``grep -c`` counts matching *lines*, so startswith is exactly equivalent)
  * verdict is ``unresolved > resolved``
  * output line format and the em-dash are byte-identical to the shell version
  * exit 1 iff at least one raw issue has unresolved comments
"""

from __future__ import annotations

import sys
from pathlib import Path

COMMENT_PREFIX = "### comment-"
RESOLUTION_PREFIX = "#### resolution-"


def scan(b1_docs: Path) -> list[tuple[str, int, int]]:
    unresolved: list[tuple[str, int, int]] = []
    for issue_file in sorted(b1_docs.glob("raw-*/issue.md")):
        with issue_file.open("r", encoding="utf-8", errors="replace") as handle:
            lines = handle.read().splitlines()
        comments = sum(1 for line in lines if line.startswith(COMMENT_PREFIX))
        resolutions = sum(1 for line in lines if line.startswith(RESOLUTION_PREFIX))
        if comments > resolutions:
            unresolved.append((issue_file.parent.name, comments, resolutions))
    return unresolved


def main() -> int:
    b1_docs = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/B1-docs")
    unresolved = scan(b1_docs)
    for raw_id, comments, resolutions in unresolved:
        print(
            f"  {raw_id}: {comments} comments, {resolutions} resolutions"
            f" — {comments - resolutions} unresolved"
        )
    return 1 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
