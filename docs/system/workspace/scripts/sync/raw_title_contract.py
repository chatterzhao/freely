#!/usr/bin/env python3
"""Single source of truth for canonical raw-issue platform titles.

Consumed by:
  - ``platform-adapter.pull_raw_issue()`` — normalize a platform-created title
  - ``bin/issue-sync._platform_title()`` — create/update title projection
  - ``runtime/freely.cmd_feedback`` edit — keep operator edits conformant

Pure stdlib, no platform I/O: safe to load from any worktree and from isolated
regression tests.  Historical issues are never rewritten by this module; it
only shapes a title when an explicit create/update/materialize action occurs.
"""
from __future__ import annotations

import re

MAX_TITLE_LEN = 100
_STALE_PREFIX = re.compile(r"^\[raw-[0-9]{8}T[0-9]{4,6}Z\]\s*", re.IGNORECASE)


def canonical_raw_title(raw_key: str, title: str, max_len: int = MAX_TITLE_LEN) -> str:
    """Return ``[RAW-<key>] <human title>``.

    Any pre-existing (possibly stale) ``[RAW-...]`` prefix is removed so the
    platform identity cannot disagree with the caller-supplied key.  Only the
    human part is truncated, so the identity prefix always survives the cap.
    """
    key = str(raw_key or "").strip()
    human = _STALE_PREFIX.sub("", str(title or "").strip()).strip()
    if not human:
        human = f"raw-{key}"
    prefix = f"[RAW-{key}] "
    budget = max(1, max_len - len(prefix))
    if len(human) > budget:
        human = human[:budget].rstrip()
    return prefix + human


def is_canonical_raw_title(title: str, raw_key: str) -> bool:
    """True when the title already declares this exact canonical identity."""
    return str(title or "").startswith(f"[RAW-{str(raw_key or '').strip()}] ")


def platform_title(local_id: str, kind: str, title: str,
                   max_len: int = MAX_TITLE_LEN) -> str:
    """Contract behind issue-sync's ``_platform_title()``.

    ``raw`` uses the canonical contract; ``linked`` and other kinds keep their
    historical ``[<local_id>] <title>`` projection unchanged.
    """
    lid = str(local_id or "").strip()
    if kind == "raw":
        key = lid[4:] if lid.startswith("raw-") else lid
        return canonical_raw_title(key, title, max_len)
    return f"[{lid}] {title}"
