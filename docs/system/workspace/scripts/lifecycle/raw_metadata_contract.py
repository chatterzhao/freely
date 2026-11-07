#!/usr/bin/env python3
"""Raw issue metadata contract and lifecycle transitions."""
from __future__ import annotations

import os
import tempfile
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

SCHEMA_VERSION = "1"
RAW_METADATA_FIELDS = (
    "schema_version",
    "local_id",
    "kind",
    "phase_state",
    "absorbed_into",
    "platform_ids",
    "primary_platform",
    "canonical_issue_path",
    "last_synced_comment_at",
    "hash",
    "created_at",
    "updated_at",
    "intake_id",
    "author",
    "channel",
    "session_refs",
    "platform_state",
    "promoted_children",
    "source_candidate",
    "completed_at",
    "closeout_note",
)
PHASE_STATES = {"proposed", "absorbed", "dropped"}
PLATFORM_STATES = {"open", "closed"}


class MetadataValidationError(ValueError):
    pass


def _string(value: Any) -> str:
    return "" if value is None else str(value)


def new_raw_metadata(
    *,
    local_id: str,
    platform_ids: Mapping[str, Mapping[str, Any]],
    primary_platform: str,
    created_at: str,
    updated_at: str,
    author: str,
    channel: str,
    intake_id: str = "",
) -> dict[str, Any]:
    metadata = {
        "schema_version": SCHEMA_VERSION,
        "local_id": local_id,
        "kind": "raw",
        "phase_state": "proposed",
        "absorbed_into": "",
        "platform_ids": deepcopy(dict(platform_ids)),
        "primary_platform": primary_platform,
        "canonical_issue_path": "",
        "last_synced_comment_at": {},
        "hash": "",
        "created_at": created_at,
        "updated_at": updated_at,
        "intake_id": intake_id,
        "author": author,
        "channel": channel,
        "session_refs": [],
        "platform_state": "open",
        "promoted_children": [],
        "source_candidate": "",
        "completed_at": "",
        "closeout_note": "",
    }
    validate(metadata)
    return metadata


def normalize(metadata: Mapping[str, Any]) -> dict[str, Any]:
    strict = _string(metadata.get("schema_version")) == SCHEMA_VERSION
    phase = _string(metadata.get("phase_state") or metadata.get("status") or "proposed")
    normalized = {
        "schema_version": _string(metadata.get("schema_version")),
        "local_id": _string(metadata.get("local_id")),
        "kind": _string(metadata.get("kind") or "raw"),
        "phase_state": phase,
        "absorbed_into": _string(metadata.get("absorbed_into")),
        "platform_ids": deepcopy(metadata.get("platform_ids") or {}),
        "primary_platform": _string(metadata.get("primary_platform")),
        "canonical_issue_path": _string(metadata.get("canonical_issue_path")),
        "last_synced_comment_at": deepcopy(metadata.get("last_synced_comment_at") or {}),
        "hash": _string(metadata.get("hash")),
        "created_at": _string(metadata.get("created_at")),
        "updated_at": _string(metadata.get("updated_at")),
        "intake_id": _string(metadata.get("intake_id")),
        "author": _string(metadata.get("author")),
        "channel": _string(metadata.get("channel")),
        "session_refs": deepcopy(metadata.get("session_refs") or []),
        "platform_state": _string(metadata.get("platform_state") or "open"),
        "promoted_children": deepcopy(metadata.get("promoted_children") or []),
        "source_candidate": _string(metadata.get("source_candidate")),
        "completed_at": _string(metadata.get("completed_at")),
        "closeout_note": _string(metadata.get("closeout_note")),
        "force_closed_at": _string(metadata.get("force_closed_at")),
        "force_closed_reason": _string(metadata.get("force_closed_reason")),
        "strict_schema": strict,
    }
    return normalized


def validate(
    metadata: Mapping[str, Any],
    *,
    require_canonical_file: bool = True,
    base_dir: str | Path | None = None,
) -> None:
    if _string(metadata.get("schema_version")) != SCHEMA_VERSION:
        raise MetadataValidationError("strict raw metadata requires current schema_version")
    if tuple(metadata.keys()) != RAW_METADATA_FIELDS:
        raise MetadataValidationError("raw metadata fields are missing, extra, or reordered")
    if metadata.get("kind") != "raw" or not _string(metadata.get("local_id")).startswith("raw-"):
        raise MetadataValidationError("raw identity is invalid")

    phase = metadata.get("phase_state")
    platform_state = metadata.get("platform_state")
    target = _string(metadata.get("absorbed_into"))
    canonical = _string(metadata.get("canonical_issue_path"))
    completed_at = _string(metadata.get("completed_at"))
    closeout_note = _string(metadata.get("closeout_note"))

    if phase not in PHASE_STATES:
        raise MetadataValidationError(f"invalid phase_state: {phase}")
    if platform_state not in PLATFORM_STATES:
        raise MetadataValidationError(f"invalid platform_state: {platform_state}")
    if phase == "absorbed":
        if not target and not canonical:
            raise MetadataValidationError("absorbed requires a canonical id or path")
        if target and not target.startswith("I-"):
            raise MetadataValidationError("absorbed_into must be an I-* id")
        if canonical:
            canonical_path = Path(canonical)
            if canonical_path.is_absolute() or ".." in canonical_path.parts:
                raise MetadataValidationError("canonical issue path must be project-relative")
            canonical_root = Path(base_dir) if base_dir is not None else Path.cwd()
            if require_canonical_file and not (canonical_root / canonical_path).is_file():
                raise MetadataValidationError("canonical issue path does not exist")
        if not completed_at:
            raise MetadataValidationError("absorbed requires completed_at")
    elif target or canonical:
        raise MetadataValidationError(f"{phase} cannot have absorption target")
    if phase == "dropped":
        if not completed_at or not closeout_note:
            raise MetadataValidationError("dropped requires completed_at and closeout_note")
    elif phase == "proposed" and (completed_at or closeout_note):
        raise MetadataValidationError("proposed cannot have closeout values")
    if not isinstance(metadata.get("platform_ids"), dict):
        raise MetadataValidationError("platform_ids must be a mapping")
    if not isinstance(metadata.get("promoted_children"), list):
        raise MetadataValidationError("promoted_children must be a list")
    if any(not _string(child).startswith("I-") for child in metadata["promoted_children"]):
        raise MetadataValidationError("promoted_children entries must be I-* ids")
    for platform, reference in metadata["platform_ids"].items():
        if not platform or not isinstance(reference, dict):
            raise MetadataValidationError("platform reference is invalid")
        if not _string(reference.get("issue_id")) or not _string(reference.get("url")):
            raise MetadataValidationError(f"platform reference is incomplete: {platform}")
        if set(reference) != {"issue_id", "url", "synced_at"}:
            raise MetadataValidationError(f"platform reference fields are invalid: {platform}")


def transition(
    metadata: Mapping[str, Any],
    event: str,
    *,
    base_dir: str | Path | None = None,
    **payload: Any,
) -> dict[str, Any]:
    current = deepcopy(dict(metadata))
    validate(current, base_dir=base_dir)
    if event == "worktree_created":
        return current

    at = _string(payload.get("at"))
    if not at:
        raise MetadataValidationError(f"{event} requires at")
    if event == "promotion_started":
        if current["phase_state"] != "proposed":
            raise MetadataValidationError("only proposed raw can record promoted children")
        issue_id = _string(payload.get("issue_id"))
        if not issue_id.startswith("I-"):
            raise MetadataValidationError("promotion_started requires I-* issue_id")
        if issue_id not in current["promoted_children"]:
            current["promoted_children"].append(issue_id)
        candidate = _string(payload.get("source_candidate"))
        if candidate:
            current["source_candidate"] = candidate
    elif event == "promotion_finalized":
        issue_id = _string(payload.get("issue_id"))
        issue_path = _string(payload.get("issue_path"))
        if current["phase_state"] == "absorbed":
            if current["absorbed_into"] == issue_id and current["canonical_issue_path"] == issue_path:
                return current
            raise MetadataValidationError("absorbed raw cannot be finalized to a different child")
        if current["phase_state"] != "proposed":
            raise MetadataValidationError("only proposed raw can be absorbed")
        if issue_id not in current["promoted_children"]:
            raise MetadataValidationError("promotion_finalized requires recorded child")
        if not issue_path:
            raise MetadataValidationError("promotion_finalized requires issue_path")
        current["phase_state"] = "absorbed"
        current["absorbed_into"] = issue_id
        current["canonical_issue_path"] = issue_path
        current["completed_at"] = at
        current["closeout_note"] = _string(payload.get("note"))
    elif event == "dropped":
        if current["phase_state"] != "proposed":
            raise MetadataValidationError("only proposed raw can be dropped")
        reason = _string(payload.get("reason"))
        if not reason:
            raise MetadataValidationError("dropped requires reason")
        current["phase_state"] = "dropped"
        current["completed_at"] = at
        current["closeout_note"] = reason
    elif event == "platform_closed":
        if current["phase_state"] not in {"absorbed", "dropped"}:
            raise MetadataValidationError(
                "platform close requires terminal raw phase "
                f"(current: {current['phase_state']}, need: absorbed|dropped)"
            )
        current["platform_state"] = "closed"
    else:
        raise MetadataValidationError(f"unknown raw metadata event: {event}")
    current["updated_at"] = at
    validate(current, base_dir=base_dir)
    return current


def read_issue(path: str | Path) -> tuple[dict[str, Any], str]:
    text = Path(path).read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise MetadataValidationError("issue file has no YAML frontmatter")
    metadata = yaml.safe_load(parts[1]) or {}
    if not isinstance(metadata, dict):
        raise MetadataValidationError("issue frontmatter must be a mapping")
    return metadata, parts[2]


def write_issue(
    path: str | Path,
    metadata: Mapping[str, Any],
    body: str,
    *,
    base_dir: str | Path | None = None,
) -> None:
    validate(metadata, base_dir=base_dir)
    destination = Path(path)
    rendered = yaml.safe_dump(
        dict(metadata), default_flow_style=False, allow_unicode=True, sort_keys=False
    ).strip()
    content = f"---\n{rendered}\n---{body}"
    fd, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def transition_issue(
    path: str | Path,
    event: str,
    *,
    base_dir: str | Path | None = None,
    **payload: Any,
) -> dict[str, Any]:
    metadata, body = read_issue(path)
    updated = transition(metadata, event, base_dir=base_dir, **payload)
    write_issue(path, updated, body, base_dir=base_dir)
    return updated
