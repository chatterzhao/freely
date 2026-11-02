#!/usr/bin/env python3
"""Declarative worktree seeds.

`git worktree add` checks out tracked files only, so anything gitignored but
required to run (agent table, local env, certificates) is missing in a fresh
worktree.  The list of such paths is project data, not script logic: it lives
in `docs/system/workspace/worktree-seed.toml` and travels with the repository.

When the manifest is absent we fall back to a single builtin entry
(`.freely/agent-table.toml`), which is what wt-create used to hardcode.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

MANIFEST = Path("docs") / "system" / "workspace" / "worktree-seed.toml"
DEFAULT_SEEDS = [{"path": ".freely/agent-table.toml", "mode": "copy", "required": False}]


class SeedError(RuntimeError):
    """A seed entry cannot be applied; the caller must abort the worktree."""


def _mini_parse(text: str) -> dict:
    """Fallback for Python without tomllib: only the [[seed]] surface we ship."""
    data: dict = {"version": 1, "seed": []}
    current: dict | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line == "[[seed]]":
            current = {}
            data["seed"].append(current)
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.lower() in {"true", "false"}:
            parsed: object = value.lower() == "true"
        elif value.isdigit():
            parsed = int(value)
        else:
            parsed = value
        if current is None:
            data[key] = parsed
        else:
            current[key] = parsed
    return data


def _parse(text: str) -> dict:
    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:
        return _mini_parse(text)
    try:
        return tomllib.loads(text)
    except Exception as error:
        raise SeedError(f"invalid worktree-seed manifest: {error}") from error


def _normalize(raw: dict) -> list:
    entries = []
    for item in raw.get("seed") or []:
        if not isinstance(item, dict):
            raise SeedError("each [[seed]] entry must be a table")
        path = str(item.get("path") or "").strip()
        if not path:
            raise SeedError("seed entry without path")
        mode = str(item.get("mode") or "copy").strip().lower()
        if mode not in {"copy", "link"}:
            raise SeedError(f"unsupported seed mode '{mode}' for {path}")
        entries.append({"path": path, "mode": mode, "required": bool(item.get("required", False))})
    return entries


def load(project: str | os.PathLike) -> tuple[list, str]:
    """Return (entries, source) where source is 'manifest' or 'builtin'."""
    manifest = Path(project) / MANIFEST
    if manifest.is_file():
        entries = _normalize(_parse(manifest.read_text()))
        if entries:
            return entries, "manifest"
    return [dict(item) for item in DEFAULT_SEEDS], "builtin"


def _check_path(root: Path, relative: str) -> Path:
    if os.path.isabs(relative):
        raise SeedError(f"seed path must be relative: {relative}")
    source = (root / relative).resolve()
    if source != root and root not in source.parents:
        raise SeedError(f"seed path escapes the project: {relative}")
    return source


def apply(project: str | os.PathLike, target: str | os.PathLike, entries: list | None = None) -> dict:
    """Copy/link each seed into `target`. Idempotent; never overwrites."""
    root = Path(project).resolve()
    destination_root = Path(target).resolve()
    if entries is None:
        entries, _ = load(root)
    report = {"copied": [], "linked": [], "skipped": [], "missing": []}
    for entry in entries:
        relative = str(entry.get("path") or "").strip()
        source = _check_path(root, relative)
        destination = destination_root / relative
        if destination.exists() or destination.is_symlink():
            report["skipped"].append(relative)
            continue
        if not source.exists():
            if entry.get("required"):
                raise SeedError(f"required seed missing: {relative}")
            report["missing"].append(relative)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if str(entry.get("mode", "copy")).lower() == "link":
            destination.symlink_to(source)
            report["linked"].append(relative)
        elif source.is_dir():
            shutil.copytree(source, destination)
            report["copied"].append(relative)
        else:
            shutil.copy2(source, destination)
            report["copied"].append(relative)
    return report


def _print_report(report: dict, source: str, as_json: bool) -> None:
    if as_json:
        print(json.dumps({**report, "source": source}, ensure_ascii=False))
        return
    print(f"[wt-seed] source={source}")
    for label in ("copied", "linked", "skipped", "missing"):
        for item in report.get(label, []):
            print(f"[wt-seed] {label}: {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="apply declarative worktree seeds")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("apply", "list"):
        command = sub.add_parser(name)
        command.add_argument("--project", required=True)
        command.add_argument("--target", default="")
        command.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        entries, source = load(args.project)
        if args.command == "list":
            if args.json:
                print(json.dumps({"source": source, "entries": entries}, ensure_ascii=False, indent=2))
            else:
                print(f"[wt-seed] source={source}")
                for entry in entries:
                    print(f"[wt-seed] {entry['mode']:<4} required={str(entry['required']):<5} {entry['path']}")
            return 0
        if not args.target:
            raise SeedError("--target is required for apply")
        report = apply(args.project, args.target, entries)
    except SeedError as error:
        print(f"[wt-seed] {error}", file=sys.stderr)
        return 1
    _print_report(report, source, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
