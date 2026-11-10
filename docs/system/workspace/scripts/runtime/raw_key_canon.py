"""Canonical raw_key normalization for agent_working assign/scan/review/close.

All production entry points that touch agent_working must use canonicalize_raw_key
so the same logical issue always maps to the same DB row.
"""
from __future__ import annotations

import re
import sys
from typing import Optional

# Bare timestamp: 20260720T171146Z
_BARE_TS = re.compile(r"^(\d{8}T\d{6}Z)$")
# Legacy format: 20261103-1326 / 20261103-132645 (optionally raw- prefixed).
# #4154: wt-create accepted this form but only warned, then embedded
# `raw-20261103-1326` into branch names where every downstream T...Z extractor
# returned an empty raw_key. Normalize it here, at the single owner.
_LEGACY = re.compile(r"^(?:raw-)?(\d{8})-(\d{4}|\d{6})$", re.IGNORECASE)
# Full raw key or with optional suffix after timestamp
_RAW_PREFIXED = re.compile(r"^(raw-)?(\d{8}T\d{6}Z)(?:[-_].*)?$", re.IGNORECASE)
# Extract first bare timestamp from branch/path/string
_EXTRACT_TS = re.compile(r"(\d{8}T\d{6}Z)")
# Legacy timestamp embedded in a branch/path (fix/raw-20261103-1326-slug)
_EXTRACT_LEGACY = re.compile(r"(\d{8})-(\d{4}|\d{6})(?![0-9])")


def canonicalize_raw_key(value: Optional[str]) -> str:
    """Normalize any raw-key-like string to a stable canonical form.

    Timestamp-bearing values become raw-YYYYMMDDTHHMMSSZ.
    Reserved keys (__manager__) and opaque keys (develop, e2e-*, discuss-*)
    pass through unchanged so assign/scan/review/close share one boundary.
    """
    if value is None:
        raise ValueError("raw_key is required")
    s = str(value).strip()
    if not s:
        raise ValueError("raw_key is empty")
    # Reserved synthetic keys used by runtime (manager global row, etc.)
    if s.startswith("__") and s.endswith("__"):
        return s

    legacy = _LEGACY.match(s)
    if legacy:
        date, hhmm = legacy.group(1), legacy.group(2)
        if len(hhmm) == 4:
            hhmm += "00"
        return f"raw-{date}T{hhmm}Z"

    m = _RAW_PREFIXED.match(s)
    if m:
        return f"raw-{m.group(2)}"

    if _BARE_TS.match(s):
        return f"raw-{s}"

    found = _EXTRACT_TS.search(s)
    if found:
        return f"raw-{found.group(1)}"

    legacy_found = _EXTRACT_LEGACY.search(s)
    if legacy_found:
        date, hhmm = legacy_found.group(1), legacy_found.group(2)
        if len(hhmm) == 4:
            hhmm += "00"
        return f"raw-{date}T{hhmm}Z"

    # Opaque / non-timestamp keys: stable identity (develop, e2e-*, discuss-*)
    return s


def try_canonicalize_raw_key(value: Optional[str], default: str = "") -> str:
    """Like canonicalize_raw_key but returns default on failure instead of raising."""
    try:
        return canonicalize_raw_key(value)
    except ValueError:
        return default


def extract_raw_key_from_branch(branch: str) -> str:
    """Extract canonical raw_key from a git branch name. Raises if not found."""
    return canonicalize_raw_key(branch)


def _main(argv: list[str]) -> int:
    """CLI used by shell entry points (wt-create) so none of them re-implement
    the format table. Prints the canonical raw key on success."""
    if len(argv) != 1 or not argv[0].strip():
        print("usage: raw_key_canon.py <raw-key-or-branch>", file=sys.stderr)
        return 2
    try:
        print(canonicalize_raw_key(argv[0]))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
