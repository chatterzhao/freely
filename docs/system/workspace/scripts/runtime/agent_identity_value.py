"""Codec for agent_working identity columns.

Wire format:
- bare reservation: agent_NN
- established session: agent_NN:session_id
- multi-agent field: comma-separated entries
"""
from __future__ import annotations

from typing import Optional


def parse_agent_entries(value: object) -> dict[str, Optional[str]]:
    entries: dict[str, Optional[str]] = {}
    for raw_entry in str(value or "").split(","):
        entry = raw_entry.strip()
        if not entry:
            continue
        agent_id, separator, session_id = entry.partition(":")
        if agent_id:
            entries[agent_id] = session_id if separator and session_id else None
    return entries


def format_agent_entry(agent_id: str, session_id: str = "") -> str:
    if not agent_id:
        raise ValueError("agent_id must not be empty")
    return f"{agent_id}:{session_id}" if session_id else agent_id


def format_agent_entries(entries: dict[str, Optional[str]]) -> Optional[str]:
    if not entries:
        return None
    return ",".join(
        format_agent_entry(agent_id, session_id or "")
        for agent_id, session_id in entries.items()
    )


def agent_ids(value: object) -> set[str]:
    return set(parse_agent_entries(value))


def first_agent_id(value: object) -> Optional[str]:
    return next(iter(parse_agent_entries(value)), None)


def session_for_agent(value: object, agent_id: str) -> Optional[str]:
    return parse_agent_entries(value).get(agent_id)


def session_entry(value: object, agent_id: str = "") -> Optional[tuple[str, str]]:
    """Return one exact agent/session pair; bare reservations are not sessions."""
    entries = parse_agent_entries(value)
    if agent_id:
        session_id = entries.get(agent_id)
        return (agent_id, session_id) if session_id else None
    return next(
        ((entry_id, session_id) for entry_id, session_id in entries.items() if session_id),
        None,
    )


def bare_agent_ids(value: object) -> list[str]:
    return [
        agent_id
        for agent_id, session_id in parse_agent_entries(value).items()
        if session_id is None
    ]
