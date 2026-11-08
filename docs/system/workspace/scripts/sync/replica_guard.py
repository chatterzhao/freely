#!/usr/bin/env python3
"""Platform-side replica guard for issue-sync create/close (#4225).

The local ``platform_ids`` map is a CACHE: after a degraded pull (R6/#4182)
records only one readable platform, that cache can be partial even though a
canonical replica already exists on the other platform. ``create`` and
``close`` must therefore consult the platform-side identity resolver
(``platform-adapter.py discover-raw``) instead of trusting the cache, otherwise
they build a duplicate replica (→ ``ambiguous`` → reconciliation hard-blocks)
or close only a subset of the real replicas.

This module is the single source of truth for interpreting that resolver's
per-platform receipt. It is PURE: no I/O, no subprocess, no network. Callers
obtain the receipt via ``discover-raw`` and pass it in, which keeps the logic
unit-testable with synthetic receipts and mirrors the Q1/R1 pattern of a pure
helper behind a thin I/O boundary.
"""
from __future__ import annotations

import json
import sys
from typing import Any

# A unique canonical replica exists on the platform. Backfill platform_ids,
# do NOT create (creating would duplicate it).
PRESENT = "present"
# Platform-side search confirmed no replica. Safe to create.
ABSENT = "absent"
# Read failed / ambiguous / platform absent from receipt. Never fabricate a
# fact: fail closed — do NOT create and do NOT certify success (R7/#4195).
INDETERMINATE = "indeterminate"


def classify_receipt(receipt: Any, platform: str) -> tuple[str, str, str]:
    """Return ``(state, issue_id, url)`` for one platform.

    ``discover-raw`` yields ``{platform: {status, ...}}`` with statuses
    ``ok`` / ``missing`` / ``ambiguous`` / ``unknown``. Only ``ok`` with a real
    issue_id is a fact we can act on; only ``missing`` is a confirmed absence.
    Everything else (unreadable platform, two canonical matches, a platform
    missing from the receipt, malformed data) is INDETERMINATE.
    """
    if not isinstance(receipt, dict):
        return (INDETERMINATE, "", "")
    entry = receipt.get(platform)
    if not isinstance(entry, dict):
        return (INDETERMINATE, "", "")
    status = entry.get("status")
    if status == "ok":
        issue_id = str(entry.get("issue_id") or "").strip()
        url = str(entry.get("url") or "").strip()
        if issue_id:
            return (PRESENT, issue_id, url)
        return (INDETERMINATE, "", "")
    if status == "missing":
        return (ABSENT, "", "")
    return (INDETERMINATE, "", "")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: replica_guard.py <platform>  (discover-raw JSON on stdin)",
              file=sys.stderr)
        return 2
    raw = sys.stdin.read().strip()
    try:
        receipt = json.loads(raw) if raw else {}
    except (ValueError, TypeError):
        receipt = {}
    state, issue_id, url = classify_receipt(receipt, sys.argv[1])
    # tab-separated so bash `IFS=$'\t' read` can consume it losslessly.
    print(f"{state}\t{issue_id}\t{url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
