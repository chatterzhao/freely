#!/usr/bin/env python3
"""Normalise platform raw-issue titles before the scan funnel consumes them.

Functional owner of the title format is ``sync/raw_title_contract.py``; the
only platform write channel is ``sync/platform-adapter.py``. This module is
pure orchestration: it reads OPEN issue records, derives the authoritative raw
key from ``title + body`` (never from ``created_at``), and writes *only* a
title when it is not canonical.

Used by ``freely task-source-scan`` as a preflight and by ``pr-create-guarded``
as a fallback for absorbed/CLOSED replicas that scan never sees.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
_SYNC = _SCRIPTS / "sync"
sys.path.insert(0, str(_SYNC))

from raw_title_contract import canonical_raw_title, is_canonical_raw_title  # noqa: E402

_RAW_KEY = re.compile(r"(?:^|\W)raw-(\d{8}T\d{4,6}Z)", re.IGNORECASE | re.MULTILINE)
_STALE_PREFIX = re.compile(r"^\[raw-[0-9]{8}T[0-9]{4,6}Z\]\s*", re.IGNORECASE)


def extract_raw_key(text: str) -> str:
    """Return the raw key declared anywhere in ``title + body``."""
    match = _RAW_KEY.search(str(text or ""))
    return match.group(1) if match else ""


def _load_adapter():
    spec = importlib.util.spec_from_file_location("platform_adapter", _SYNC / "platform-adapter.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _platform_of(key: str, record: dict) -> str:
    declared = str(record.get("platform") or "")
    if declared:
        return declared
    return key.split(":", 1)[0] if ":" in key else ""


def _is_raw_identity(title: str, body: str, raw_key: str) -> bool:
    """Only the issue that *owns* ``raw-<key>`` may be normalised.

    A body reference is not identity: linked I-* issues carry
    ``promoted_from: raw-<key>`` and source_candidate paths, but their own
    identity is ``issue_id: I-...``. Rewriting those titles would corrupt them.
    """
    if is_canonical_raw_title(title, raw_key):
        return True
    if re.match(r"^\[I-", str(title or "").strip(), re.IGNORECASE):
        return False
    if re.search(r"^\s*(?:kind:\s*linked|issue_id:\s*I-)", str(body or ""),
                 re.IGNORECASE | re.MULTILINE):
        return False
    key = re.escape(raw_key)
    return bool(re.search(
        rf"local_id\s*[:|]\s*`?raw-{key}`?", str(body or ""), re.IGNORECASE,
    ))


def _expected_title(raw_key: str, observed: str) -> str:
    human = _STALE_PREFIX.sub("", str(observed or "").strip()).strip()
    return canonical_raw_title(raw_key, human or f"raw-{raw_key}")


def normalize_open_raw_titles(
    project: str | Path,
    dry_run: bool = False,
    adapter_module=None,
    raw_key: str = "",
) -> dict:
    """Fix non-canonical titles on OPEN raw replicas.

    Returns ``{"ok", "changes", "errors", "skipped"}``. ``changes`` entries
    carry ``platform``, ``issue_id``, ``raw_key``, ``before`` and ``after``.
    """
    adapter = adapter_module or _load_adapter()
    try:
        records = adapter.list_open_issue_records() or {}
    except Exception as exc:  # a read failure is debt, not a fabricated absence
        return {"ok": False, "changes": [], "errors": [f"open issue read failed: {exc}"], "skipped": []}

    changes: list[dict] = []
    errors: list[str] = []
    skipped: list[str] = []

    for key, record in records.items():
        if "__degraded__" in str(key):
            skipped.append(str(record.get("error") or "degraded platform read"))
            continue
        if not isinstance(record, dict):
            continue
        platform = _platform_of(str(key), record)
        issue_id = str(record.get("issue_id") or (key.split(":", 1)[1] if ":" in str(key) else key))
        observed = str(record.get("title") or "")
        body = str(record.get("body") or "")
        found_key = extract_raw_key(f"{observed}\n{body}")
        if not found_key:
            # Never guess identity from created_at; leave a diagnosable trace.
            skipped.append(f"{platform}:{issue_id}: no raw-<key> in title or body")
            continue
        if raw_key and found_key.lower() != raw_key.strip().lower():
            continue
        if not _is_raw_identity(observed, body, found_key):
            skipped.append(f"{platform}:{issue_id}: raw key is only a body reference, not this issue's identity")
            continue
        expected = _expected_title(found_key, observed)
        if is_canonical_raw_title(observed, found_key) and observed == expected:
            continue

        change = {
            "platform": platform,
            "issue_id": issue_id,
            "raw_key": found_key,
            "before": observed,
            "after": expected,
        }
        changes.append(change)
        prefix = "[dry-run] " if dry_run else ""
        print(f'{prefix}issue 标题不规范已执行规范标题命令：{platform} #{issue_id} "{observed}" → "{expected}"')
        if dry_run:
            continue

        try:
            result = adapter.update_issue(
                f"raw-{found_key}", {platform: {"issue_id": issue_id}}, expected, "",
            ) or {}
            status = (result.get(platform) or {}).get("status")
            if status not in ("updated", "skipped"):
                errors.append(f"{platform} #{issue_id}: {status or 'no status'}")
        except Exception as exc:
            errors.append(f"{platform} #{issue_id}: {exc}")

    return {"ok": not errors, "changes": changes, "errors": errors, "skipped": skipped}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--raw-key", default="", help="limit normalisation to one raw key")
    args = parser.parse_args(argv)
    result = normalize_open_raw_titles(args.project, dry_run=args.dry_run, raw_key=args.raw_key)
    for item in result["skipped"]:
        print(f"[title] skip: {item}", file=sys.stderr)
    for item in result["errors"]:
        print(f"[title] ERROR: {item}", file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
