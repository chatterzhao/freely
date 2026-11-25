#!/usr/bin/env python3
"""replica_truth — decide which platform replicas belong to a local issue id.

The issue lifecycle used to be judged from the local `platform_state` cache.
That cache is written by the same code paths it is supposed to certify, so a
partially-closed or never-mapped replica stayed OPEN while the worktree was
deleted (raw-20261125T071429Z).

This module holds the *pure* half of the fix: given a platform read (a mapping
of ``platform:issue_id`` to issue records, as returned by
``platform_adapter.list_open_issue_records``), decide which records are OPEN
replicas of ``local_id``. Keeping it pure makes the judgement testable without
network access, and keeps the adapter as the only I/O owner.

Contract
--------
``filter_open_replicas(records, local_id)`` -> ``{platform: [record, ...]}``
    * a record belongs to ``local_id`` when its title carries that id;
    * CLOSED records are never returned (the caller reads OPEN issues, but a
      mixed source must not leak a closed replica into the refusal list);
    * raw titles (``[RAW-...]``) that merely mention an I-* id are not replicas
      of that I-*;
    * the ``__degraded__`` marker is never a record.

``summarize(records, local_id)`` -> ``{"ok", "replicas", "degraded"}``
    ``ok`` means "every configured platform was readable". A read failure must
    never be reported as "no replicas" — that inversion is what let the gate
    pass while the platform was unreadable.
"""
from __future__ import annotations

from typing import Iterable

DEGRADED_KEY = "__degraded__"
_CLOSED_STATES = {"closed", "completed", "done"}


def _platform_of(key: str) -> str:
    return key.split(":", 1)[0] if ":" in key else ""


def _issue_id_of(key: str, record: dict) -> str:
    value = str(record.get("issue_id") or "")
    if value:
        return value
    return key.split(":", 1)[1] if ":" in key else key


def title_carries_local_id(title: str, local_id: str, kind: str = "linked") -> bool:
    """True when a title is a replica of ``local_id`` (not merely a mention).

    linked replicas carry the id in their canonical title:
    ``[I-<key>-A] I-<key>-A: …`` or ``[RAW-<key>] [I-<key>-A] …`` (promoted).
    A raw issue title without an ``[I-`` marker is the B1 document, not an I-*
    replica — EXCEPT when we are asking about the raw document itself
    (``kind="raw"``), where ``raw-<key>`` in the title is the identity.
    """
    if not local_id:
        return False
    if kind == "raw":
        # Document ids are lowercase (raw-<key>); the canonical title is
        # [RAW-<key>]. Compare case-insensitively or the raw is never found.
        # Promoted linked replicas carry "[RAW-<key>] [I-<key>-A] ..." — they are
        # I-* replicas, covered by their own id, not by the raw document.
        return local_id.lower() in title.lower() and "[I-" not in title
    if local_id not in title:
        return False
    return "[I-" in title


def _is_open(record: dict) -> bool:
    """Missing state means the source already filtered for OPEN issues."""
    state = str(record.get("state") or "").strip().lower()
    if not state:
        return True
    return state not in _CLOSED_STATES


def filter_open_replicas(records: dict, local_id: str,
                         kind: str = "linked") -> dict[str, list[dict]]:
    found: dict[str, list[dict]] = {}
    for key, record in (records or {}).items():
        if key == DEGRADED_KEY or not isinstance(record, dict):
            continue
        title = str(record.get("title") or "")
        if not title_carries_local_id(title, local_id, kind):
            continue
        if not _is_open(record):
            continue
        platform = _platform_of(key) or "unknown"
        found.setdefault(platform, []).append(
            {"issue_id": _issue_id_of(key, record), "title": title}
        )
    return found


def degraded_platforms(records: dict) -> list[dict]:
    marker: Iterable = ()
    if isinstance(records, dict):
        marker = records.get(DEGRADED_KEY) or ()
    if isinstance(marker, dict):
        marker = [marker]
    return [item for item in marker if isinstance(item, dict)]


def summarize(records: dict, local_id: str, kind: str = "linked") -> dict:
    replicas = filter_open_replicas(records, local_id, kind)
    degraded = degraded_platforms(records)
    return {
        "ok": not degraded,
        "local_id": local_id,
        "kind": kind,
        "replicas": replicas,
        "open_count": sum(len(items) for items in replicas.values()),
        "degraded": degraded,
    }


def has_any_replica(records: dict, local_id: str, kind: str = "linked") -> bool:
    """Any replica at all (OPEN or not) — used to refuse duplicate creation."""
    for key, record in (records or {}).items():
        if key == DEGRADED_KEY or not isinstance(record, dict):
            continue
        if title_carries_local_id(str(record.get("title") or ""), local_id, kind):
            return True
    return False
