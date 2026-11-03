#!/usr/bin/env python3
"""Durable ledger of platform replicas we could not verify.

A `unknown` replica is not a fact about the platform, so it must not block work
forever -- but it must not disappear either.  Every time a caller proceeds on a
partial observation, the unreadable platform is recorded here with its reason,
age and attempt count, so `issue-sync reconcile` (or a human) can settle it
later.

The ledger lives under `.freely/state/` (machine-local, gitignored): it describes
*this machine's* view of the network, not the repository's content.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_NAME = "sync-debt.json"


def _path(root: str | None, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    base = Path(root or os.environ.get("FREELY_PROJECT_ROOT") or os.getcwd())
    return base / ".freely" / "state" / DEFAULT_NAME


def _load(path: Path) -> dict:
    if not path.is_file():
        return {"version": 1, "entries": {}}
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {"version": 1, "entries": {}}
    if not isinstance(data, dict):
        return {"version": 1, "entries": {}}
    data.setdefault("version", 1)
    data.setdefault("entries", {})
    return data


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=str(path.parent), prefix=".sync-debt.")
    with os.fdopen(handle, "w") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")
    os.replace(temporary, path)


def _key(raw_key: str, platform: str) -> str:
    return f"{raw_key.strip()}::{platform.strip()}"


def record(entries: list[dict], path: Path) -> dict:
    data = _load(path)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for item in entries:
        raw_key = str(item.get("raw_key") or "").strip()
        platform = str(item.get("platform") or "").strip()
        if not raw_key or not platform:
            continue
        key = _key(raw_key, platform)
        existing = data["entries"].get(key) or {}
        data["entries"][key] = {
            "raw_key": raw_key,
            "platform": platform,
            "reason": str(item.get("reason") or "unreadable")[:300],
            "since": existing.get("since") or now,
            "last_seen": now,
            "attempts": int(existing.get("attempts") or 0) + 1,
        }
    _save(path, data)
    return data


def clear(raw_key: str, platform: str | None, path: Path) -> dict:
    data = _load(path)
    for key in list(data["entries"]):
        item = data["entries"][key]
        if item.get("raw_key") != raw_key:
            continue
        if platform and item.get("platform") != platform:
            continue
        data["entries"].pop(key, None)
    _save(path, data)
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="record / list / clear raw replica sync debt")
    parser.add_argument("--root", default="")
    parser.add_argument("--file", default="")
    sub = parser.add_subparsers(dest="command", required=True)

    record_cmd = sub.add_parser("record")
    record_cmd.add_argument("--receipt", default="", help="gate receipt JSON; reads its debt list")
    record_cmd.add_argument("--raw-key", default="")
    record_cmd.add_argument("--platform", default="")
    record_cmd.add_argument("--reason", default="")

    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--json", action="store_true")

    clear_cmd = sub.add_parser("clear")
    clear_cmd.add_argument("--raw-key", required=True)
    clear_cmd.add_argument("--platform", default="")

    args = parser.parse_args()
    path = _path(args.root, args.file)

    if args.command == "record":
        entries: list[dict] = []
        if args.receipt:
            try:
                receipt = json.loads(Path(args.receipt).read_text())
            except (OSError, json.JSONDecodeError):
                receipt = {}
            entries = [item for item in (receipt.get("debt") or []) if isinstance(item, dict)]
        if args.raw_key and args.platform:
            entries.append({"raw_key": args.raw_key, "platform": args.platform, "reason": args.reason})
        data = record(entries, path)
        print(json.dumps({"file": str(path), "recorded": len(entries), "total": len(data["entries"])}, ensure_ascii=False))
        return 0 if entries else 1

    if args.command == "clear":
        data = clear(args.raw_key, args.platform or None, path)
        print(json.dumps({"file": str(path), "total": len(data["entries"])}, ensure_ascii=False))
        return 0

    data = _load(path)
    entries = sorted(data["entries"].values(), key=lambda item: item.get("since", ""))
    if args.json:
        print(json.dumps({"file": str(path), "entries": entries}, ensure_ascii=False, indent=2))
        return 0
    if not entries:
        print(f"sync-debt: no outstanding replicas ({path})")
        return 0
    for item in entries:
        print(
            f"{item.get('since','?')}  {item.get('raw_key')}  {item.get('platform')}  "
            f"attempts={item.get('attempts')}  {item.get('reason')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
