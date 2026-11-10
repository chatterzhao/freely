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
_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_H1 = re.compile(r"^#[ \t]+(\S.*)$")


def find_local_heading(body: str):
    """Return ``(title, end_offset)`` for the first H1 OUTSIDE fenced code.

    Both the materializer (`platform-adapter.pull_raw_issue`) and the replica
    gate (`raw-reconciliation-gate._local_record`) used a bare ``^#\\s+``
    regex over the whole body. A bug report containing a python code block
    with ``# -> StateFileError: ...`` comments therefore looked like it
    already had an H1: materialization skipped injecting one, and the gate
    borrowed the comment as the LOCAL title and discarded the body before it
    (#4269). Fenced blocks are skipped so only real Markdown headings count.

    ``end_offset`` is the character offset just after the heading line, which
    lets callers slice the remaining body the same way the old regex match
    did. Returns ``None`` when no real H1 exists.
    """
    text = str(body or "")
    fence_char = ""
    fence_len = 0
    offset = 0
    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        fence = _FENCE.match(stripped)
        if fence:
            marker = fence.group(1)
            char = marker[0]
            if not fence_char:
                fence_char, fence_len = char, len(marker)
            elif char == fence_char and len(marker) >= fence_len:
                fence_char, fence_len = "", 0
            offset += len(line)
            continue
        if not fence_char:
            heading = _H1.match(stripped)
            if heading:
                return heading.group(1).strip(), offset + len(line)
        offset += len(line)
    return None


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


def local_heading_title(raw_key: str, title: str, max_len: int = MAX_TITLE_LEN) -> str:
    """Return the H1 text for a materialized ``docs/B1-docs/raw-*/issue.md``.

    ``raw-reconciliation-gate._local_record()`` extracts the first ``# `` line
    as the LOCAL title, while ``canonical_projection()`` strips the
    ``[RAW-<key>] `` prefix from the PLATFORM title.  To keep both fingerprints
    identical the H1 must therefore be the human part only — no identity prefix.

    Derived through ``canonical_raw_title()`` so the same de-duplication,
    identity anchoring and length cap that shape the platform title also shape
    the local H1: a hand-edited or prefix-less platform title is normalized to
    the same human text on both sides of the comparison.

    Empty/whitespace-only titles fall back to ``raw-<key>`` via the canonical
    contract, so the H1 is never blank.
    """
    key = str(raw_key or "").strip()
    # Strip any identity prefix BEFORE delegating. _STALE_PREFIX (used inside
    # canonical_raw_title) only matches timestamp-shaped keys, so handing it a
    # historical/non-standard key ('20260501', 'MIGRATED', ...) would produce
    # a doubled '[RAW-...] [RAW-...]' prefix. Removing the exact-key prefix
    # first keeps canonical_raw_title() itself untouched (no Q2 regression).
    exact = re.compile(r"^\[raw-" + re.escape(key) + r"\]\s*", re.IGNORECASE)
    human = exact.sub("", str(title or "").strip()).strip()
    human = _STALE_PREFIX.sub("", human).strip()
    canonical = canonical_raw_title(key, human, max_len)
    prefix = f"[RAW-{key}] "
    human = canonical[len(prefix):].strip() if canonical.startswith(prefix) else _STALE_PREFIX.sub("", canonical).strip()
    # An H1 is one line. canonical_projection() collapses whitespace and
    # lowercases the platform title, so this keeps both sides identical.
    human = re.sub(r"\s+", " ", human)
    return human or f"raw-{key}"


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
