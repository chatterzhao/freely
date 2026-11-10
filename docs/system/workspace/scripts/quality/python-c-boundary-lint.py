#!/usr/bin/env python3
"""Boundary lint: reject external values interpolated into `python3 -c` bodies.

R22 (raw-20261103T132636Z) proved that a branch name interpolated into
`python3 -c "... '$branch' ..."` is remote code execution on the maintainer's
machine, and converted the two known sites to heredoc + sys.argv. This lint is
the recurrence guard: it detects the *shape* (a shell variable inside a
single-quoted string inside a `python3 -c` body) without flagging the safe
argv/heredoc form.

It deliberately does NOT try to rewrite the ~154 remaining `python3 -c` calls.
Most are static scripts with no external values; the lint gives a countable
baseline so the number can only go down (raw-20261109T085539Z / #4246).

Usage: python3 python-c-boundary-lint.py --path <file-or-dir>
Exit 0: no violations. Exit 1: violations found. Exit 2: bad arguments.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# `python3 -c "..."` with a $VAR (or ${VAR}) inside a single-quoted string.
# Conservative by design: only the shape R22 proved exploitable.
PY_C = re.compile(r'\bpython3\s+-c\s+(["\'])(?:(?!\1).)*\1', re.DOTALL)
SINGLE_QUOTED_VAR = re.compile(r"'[^']*\$(?:\{)?[A-Za-z_][A-Za-z0-9_]*(?:\})?[^']*'")
SCAN_SUFFIXES = {".sh", ".py", ""}  # "" covers extension-less runtime scripts


def scan_text(text: str) -> list[tuple[int, str]]:
    findings = []
    for match in PY_C.finditer(text):
        body = match.group(0)
        var = SINGLE_QUOTED_VAR.search(body)
        if var:
            line = text.count("\n", 0, match.start()) + 1
            findings.append((line, var.group(0)[:120]))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", required=True, help="file or directory to scan")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    target = Path(args.path)
    if not target.exists():
        print(f"[boundary-lint] path not found: {target}", file=sys.stderr)
        return 2
    files = ([target] if target.is_file()
             else sorted(p for p in target.rglob("*")
                         if p.is_file() and p.suffix in SCAN_SUFFIXES
                         and "node_modules" not in p.parts
                         and "/tests/" not in str(p)))
    violations = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # Skip this lint's own source (it documents the pattern).
        if path.name == Path(__file__).name:
            continue
        for line, snippet in scan_text(text):
            violations.append({"file": str(path), "line": line, "snippet": snippet})
    count = len(violations)
    if args.json:
        print(json.dumps({"count": count, "violations": violations},
                         ensure_ascii=False, indent=2))
    else:
        print(f"[boundary-lint] count={count}")
        for item in violations:
            print(f"  {item['file']}:{item['line']}: {item['snippet']}")
    return 1 if count else 0


if __name__ == "__main__":
    sys.exit(main())
