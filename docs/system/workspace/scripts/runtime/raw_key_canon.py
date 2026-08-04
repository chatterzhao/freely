"""Canonical raw_key normalization for agent_working assign/scan/review/close.

All production entry points that touch agent_working must use canonicalize_raw_key
so the same logical issue always maps to the same DB row.
"""
from __future__ import annotations

import re
from typing import Optional

# Bare timestamp: 20260720T171146Z
_BARE_TS = re.compile(r"^(\d{8}T\d{6}Z)$")
# Full raw key or with optional suffix after timestamp
_RAW_PREFIXED = re.compile(r"^(raw-)?(\d{8}T\d{6}Z)(?:[-_].*)?$", re.IGNORECASE)
# Extract first bare timestamp from branch/path/string
_EXTRACT_TS = re.compile(r"(\d{8}T\d{6}Z)")


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

    m = _RAW_PREFIXED.match(s)
    if m:
        return f"raw-{m.group(2)}"

    if _BARE_TS.match(s):
        return f"raw-{s}"

    found = _EXTRACT_TS.search(s)
    if found:
        return f"raw-{found.group(1)}"

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
