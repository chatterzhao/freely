#!/usr/bin/env python3
"""Static contract: every documented `freely <cmd>` must be callable.

Read-only and dependency-free. Two sources of commands are checked:
  * bin/freely header comments (quoted `freely <cmd>` / 'freely <cmd>')
  * docs/system/workspace/commands.md (same quoting forms)

A promised command resolves when it is a first-level case label in the
runtime/freely main() dispatcher, or an executable bin/<cmd>. Anything else is
reported with its source and the checker exits non-zero (fail-closed).

Use --self-test to prove the checker rejects a synthetic unknown command.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

PROMISE_RE = re.compile(r"[`']freely\s+([a-z][a-z0-9-]*)\b")
DISPATCH_RE = re.compile(r'^    ([a-z][a-z0-9-]*)\)\s', re.M)
MAIN_BLOCK_RE = re.compile(
    r'(?:^|\n)main\(\) \{.*?\n  case "\$cmd" in\n(.*?)\n  esac', re.S
)


def dispatch_commands(runtime_text: str) -> set[str]:
    match = MAIN_BLOCK_RE.search(runtime_text)
    if not match:
        raise ValueError("runtime/freely: main() case \"$cmd\" block not found")
    return set(DISPATCH_RE.findall(match.group(1)))


def promised_commands(text: str, source: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        for name in PROMISE_RE.findall(line):
            found.setdefault(name, []).append(f"{source}:{lineno}")
    return found


def find_missing(
    promises: dict[str, list[str]], available: set[str], bin_names: set[str]
) -> list[tuple[str, list[str]]]:
    return [
        (name, refs)
        for name, refs in sorted(promises.items())
        if name not in available and name not in bin_names
    ]


def self_test() -> int:
    runtime = 'main() {\n  case "$cmd" in\n    status) cmd_status "$@" ;;\n  esac\n}\n'
    available = dispatch_commands(runtime)
    assert "status" in available, "self-test: dispatcher extraction failed"
    promises = promised_commands("# use `freely status`\n# then 'freely install' here\n", "synthetic")
    missing = find_missing(promises, available, set())
    assert [name for name, _ in missing] == ["install"], (
        "self-test: checker must reject only the synthetic unknown command, got " + str(missing)
    )
    print("SELF-TEST: ok (status accepted, install rejected)")
    return 0


def check_root(root: Path) -> int:
    runtime = (root / "docs/system/workspace/scripts/runtime/freely").read_text(
        encoding="utf-8", errors="replace"
    )
    available = dispatch_commands(runtime)
    bin_names = {
        p.name for p in (root / "bin").iterdir()
        if p.is_file() and os.access(p, os.X_OK)
    }

    promises: dict[str, list[str]] = {}
    header = root / "bin/freely"
    if header.is_file():
        promises.update(promised_commands(
            header.read_text(encoding="utf-8", errors="replace"), "bin/freely"
        ))
    commands = root / "docs/system/workspace/commands.md"
    if commands.is_file():
        promises.update(promised_commands(
            commands.read_text(encoding="utf-8", errors="replace"),
            "docs/system/workspace/commands.md",
        ))

    missing = find_missing(promises, available, bin_names)
    if missing:
        for name, refs in missing:
            print(f"[FAIL] documented command '{name}' has no dispatcher/bin entry ({', '.join(refs)})",
                  file=sys.stderr)
        print(f"CONTRACT: {len(missing)} unresolved command name(s)", file=sys.stderr)
        return 1
    print(f"CONTRACT: ok ({len(promises)} documented commands resolve to dispatcher or bin/)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    return check_root(args.root.resolve())


if __name__ == "__main__":
    sys.exit(main())
