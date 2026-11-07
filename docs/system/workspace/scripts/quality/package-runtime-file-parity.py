#!/usr/bin/env python3
"""Fail-closed recurrence guard: runtime-referenced workspace files must be packaged.

`bin/freely-package` copies ONLY the paths listed in package-allowlist.txt.
A tracked file directly under docs/system/workspace/ that is referenced by a
literal path in runtime code but absent from the allowlist silently disappears
from the installed state (e.g. an installed `freely-package` cannot find its
own allowlist, and the worktree seeder falls back to builtin defaults).

This check is deliberately SEPARATE from package-seed-parity.py:
  - package-seed-parity.py  : gitignored allowlist paths  <-> seed manifest
  - this checker            : runtime-referenced tracked top-level files <-> allowlist

It is READ-ONLY and declarative: it never edits either file. It is invoked by
freely-package before any output cleanup, so adding a runtime-referenced file
without updating the allowlist is blocked at package time rather than showing
up as a confusing installed-state failure.

Stdlib only. Works with or without git metadata (an installed state has none).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path("docs/system/workspace")
ALLOWLIST = WORKSPACE / "package-allowlist.txt"

# Runtime code directories only. Tests and B1/B2 governance docs are NOT
# runtime consumers, so a file referenced only by them does not need to ship.
RUNTIME_DIRS = (
    Path("bin"),
    WORKSPACE / "scripts/runtime",
    WORKSPACE / "scripts/quality",
    WORKSPACE / "scripts/worktree",
)


def _allowlist_entries(root: Path) -> list[str]:
    path = root / ALLOWLIST
    if not path.is_file():
        raise RuntimeError(f"allowlist not found: {path}")
    return [
        line.rstrip("/")
        for raw in path.read_text(encoding="utf-8").splitlines()
        if (line := raw.strip()) and not line.startswith("#")
    ]


def _tracked_top_level_files(root: Path) -> list[str]:
    """Tracked files directly under docs/system/workspace/ (not directories).

    With git metadata use `git ls-files`; an installed state has no .git, so
    fall back to the files physically present there (all of which came from
    the allowlist in the first place).
    """
    prefix = str(WORKSPACE) + "/"
    try:
        result = subprocess.run(
            ["git", "ls-files", str(WORKSPACE)],
            cwd=str(root), capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        result = None
    if result is not None and result.returncode == 0 and result.stdout.strip():
        return sorted(
            p for p in result.stdout.splitlines()
            if p.startswith(prefix) and "/" not in p[len(prefix):]
        )
    directory = root / WORKSPACE
    if not directory.is_dir():
        return []
    return sorted(
        f"{prefix}{p.name}" for p in directory.iterdir() if p.is_file()
    )


def _runtime_text(root: Path, self_path: Path) -> str:
    chunks: list[str] = []
    for rel in RUNTIME_DIRS:
        directory = root / rel
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if not path.is_file() or "__pycache__" in str(path):
                continue
            # Never let this checker's own documentation/comment text (or a
            # copy of it in a fixture project) create a false "runtime
            # reference" for a doc-only file. Match by name as well as path:
            # --project may point at a different tree than __file__.
            if path.name == self_path.name:
                continue
            try:
                if path.resolve() == self_path.resolve():
                    continue
            except OSError:
                pass
            try:
                chunks.append(path.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                continue
    return "\n".join(chunks)


def check(root: Path) -> tuple[list[str], list[str], list[str]]:
    entries = _allowlist_entries(root)
    allow = set(entries)
    top_files = _tracked_top_level_files(root)
    text = _runtime_text(root, Path(__file__))
    referenced: list[str] = []
    undeclared: list[str] = []
    for rel in top_files:
        name = Path(rel).name
        # Accept both the full literal path and a bare filename reference,
        # but only for files that actually exist at the workspace top level.
        if name in text or rel in text:
            referenced.append(rel)
            if rel not in allow:
                undeclared.append(rel)
    return referenced, undeclared, top_files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="project root (default: cwd)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    try:
        referenced, undeclared, top_files = check(root)
    except Exception as error:
        print(f"[runtime-file-parity] ERROR: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({
            "top_level_files": top_files,
            "referenced": referenced,
            "undeclared": undeclared,
            "ok": not undeclared,
        }, ensure_ascii=False))
    if undeclared:
        for rel in undeclared:
            print(f"[runtime-file-parity] runtime-referenced file missing from package allowlist: {rel}", file=sys.stderr)
        print(f"[runtime-file-parity] {len(undeclared)} undeclared runtime file(s) - packaging aborted", file=sys.stderr)
        print("[runtime-file-parity] add the explicit file path to docs/system/workspace/package-allowlist.txt", file=sys.stderr)
        return 1
    print(f"[runtime-file-parity] OK: {len(referenced)} runtime-referenced top-level file(s) all packaged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
