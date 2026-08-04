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
from raw_metadata_contract import read_issue
from raw_reconciliation import reconcile


def _load_adapter():
    path = SCRIPTS / "sync" / "platform-adapter.py"
    spec = importlib.util.spec_from_file_location("platform_adapter", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _local_record(path: Path, raw_key: str) -> dict:
    metadata, body = read_issue(path)
    title = ""
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        body = body[match.end():].lstrip()
    return {
        "raw_key": metadata.get("local_id", raw_key),
        "title": title,
        "body": body,
        "state": metadata.get("phase_state", ""),
        "labels": [],
        "comments": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--raw-key", required=True)
    parser.add_argument("--require-local", action="store_true")
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
    )
    if args.require_local and local is None:
        receipt["ok"] = False
        receipt["diagnostics"].append({"scope": "local", "code": "missing_local", "detail": str(local_path)})
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
