#!/usr/bin/env python3
"""Read-only lifecycle gate for a configured raw replica set."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SCRIPTS / "sync"))
from raw_metadata_contract import read_issue
from raw_reconciliation import reconcile
from raw_title_contract import find_local_heading


def _load_adapter():
    path = SCRIPTS / "sync" / "platform-adapter.py"
    spec = importlib.util.spec_from_file_location("platform_adapter", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _local_record(path: Path, raw_key: str) -> dict:
    metadata, body = read_issue(path)
    # #4269: only a real Markdown H1 counts. A bare `^#\s+` regex also matched
    # `# -> StateFileError: ...` comments INSIDE python code blocks, which made
    # this gate borrow a code comment as the LOCAL title and drop every line
    # before it — a healthy raw was then reported as content_diverged.
    heading = find_local_heading(body)
    title = ""
    if heading:
        title, end_offset = heading
        body = body[end_offset:].lstrip()
    declared = metadata.get("labels")
    # Labels are platform-side presentation state. A raw document only asserts
    # them when it explicitly declares a `labels` frontmatter field; deriving
    # kind/* for legacy unlabelled raws would invent a fact and diverge from
    # platform copies that predate the label pipeline (#4151 has no labels).
    labels = [str(item) for item in declared] if isinstance(declared, list) else []
    return {
        "raw_key": metadata.get("local_id", raw_key),
        "title": title,
        "body": body,
        "state": metadata.get("phase_state", ""),
        "labels": labels,
        "comments": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--raw-key", required=True)
    parser.add_argument("--require-local", action="store_true")
    parser.add_argument(
        "--allow-degraded",
        action="store_true",
        help="permit unreadable replicas, recording them as debt; facts still block",
    )
    args = parser.parse_args()
    project = Path(args.project).resolve()
    os.environ.setdefault("FREELY_PROJECT_ROOT", str(project))
    adapter = _load_adapter()
    local_path = project / "docs" / "B1-docs" / f"raw-{args.raw_key}" / "issue.md"
    local = _local_record(local_path, args.raw_key) if local_path.is_file() else None
    replicas = adapter.discover_raw_replicas(args.raw_key)
    receipt = reconcile(
        raw_key=args.raw_key,
        configured_platforms=adapter.configured_platforms(),
        replicas=replicas,
        local=local if args.require_local else None,
        allow_degraded=args.allow_degraded,
    )
    if args.require_local and local is None:
        receipt["ok"] = False
        receipt["diagnostics"].append({"scope": "local", "code": "missing_local", "detail": str(local_path)})
    elif args.require_local and not local.get("title"):
        # Fail with an actionable reason: the document has no real H1, so
        # `raw-issue-pull` (or a manual edit) must restore it. Never silently
        # fall back to a code comment and report a misleading divergence.
        receipt["ok"] = False
        receipt["diagnostics"].append({
            "scope": "local", "code": "missing_local_title",
            "detail": f"{local_path}: no H1 outside fenced code blocks; "
                      f"re-materialize with raw-issue-pull",
        })
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
