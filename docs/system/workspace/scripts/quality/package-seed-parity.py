#!/usr/bin/env python3
"""Fail-closed consistency check: packaging allowlist vs worktree seeds.

`git worktree add` only checks out tracked files. Any packaging allowlist entry
that lives under a gitignored path is therefore ABSENT from a fresh worktree,
and packaging (or a packaging test) run there fails with a confusing
"missing file" error unrelated to the code under test.

This check compares DECLARATIONS only (it never rewrites either file):

  for each allowlist path that git would ignore:
      the worktree seed manifest must declare that exact path

It is invoked by `bin/freely-package` BEFORE any output cleanup, so a newly
added gitignored allowlist entry that was not seeded is blocked at package
time instead of surfacing as a spurious worktree test failure.

Read-only. Stdlib only. Safe to run from any worktree.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ALLOWLIST = Path("docs/system/workspace/package-allowlist.txt")
SEED_MANIFEST = Path("docs/system/workspace/worktree-seed.toml")


def _allowlist_entries(root: Path) -> list[str]:
    path = root / ALLOWLIST
    if not path.is_file():
        raise RuntimeError(f"allowlist not found: {path}")
    entries: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(line.rstrip("/"))
    return entries


def _seed_paths(root: Path) -> set[str]:
    """Parse the manifest through the project's own seeder (single truth)."""
    seeder = root / "docs/system/workspace/scripts/worktree/worktree_seed.py"
    if seeder.is_file():
        sys.path.insert(0, str(seeder.parent))
        import worktree_seed  # type: ignore
        entries, _ = worktree_seed.load(root)
        return {str(item.get("path", "")).strip().rstrip("/") for item in entries}
    path = root / SEED_MANIFEST
    if not path.is_file():
        raise RuntimeError(f"seed manifest not found: {path}")
    paths: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line.startswith("path"):
            continue
        _, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        if value:
            paths.add(value.rstrip("/"))
    return paths


def _is_gitignored(root: Path, relative: str) -> bool:
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", "--no-index", "--", relative],
            cwd=str(root), capture_output=True, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def check(root: Path) -> tuple[list[str], list[str]]:
    entries = _allowlist_entries(root)
    seeds = _seed_paths(root)
    ignored = [p for p in entries if _is_gitignored(root, p)]
    undeclared = [p for p in ignored if p not in seeds]
    return ignored, undeclared


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="project root (default: cwd)")
    parser.add_argument("--checker", default="", help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    try:
        ignored, undeclared = check(root)
    except Exception as error:
        print(f"[seed-parity] ERROR: {error}", file=sys.stderr)
        return 2
    if args.json:
        import json
        print(json.dumps({"ignored": ignored, "undeclared": undeclared, "ok": not undeclared}))
    if undeclared:
        for path in undeclared:
            print(f"[seed-parity] allowlist gitignored path has no seed declaration: {path}", file=sys.stderr)
        print(f"[seed-parity] {len(undeclared)} undeclared gitignored allowlist path(s) - packaging aborted", file=sys.stderr)
        print("[seed-parity] add a [[seed]] entry to docs/system/workspace/worktree-seed.toml", file=sys.stderr)
        return 1
    print(f"[seed-parity] OK: {len(ignored)} gitignored allowlist path(s) all seeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
