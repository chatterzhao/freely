#!/usr/bin/env python3
"""Pure, fail-closed comparison of configured raw issue replicas."""
from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable, Mapping
from typing import Any

_RAW_PREFIX = re.compile(r"^raw-", re.IGNORECASE)
_SPACE = re.compile(r"\s+")
_COMMENT = re.compile(r"^#{3,4}\s+(?:comment|resolution)-[^\n]+$", re.IGNORECASE | re.MULTILINE)
# A comment block is its heading plus everything up to the next heading. System
# events (promote / promote_finalized) write these inline in the document body,
# so the body comparison must ignore them and the comment comparison must look at
# their content — otherwise a documented raw can never match its platform copies.
_COMMENT_BLOCK = re.compile(
    r"^#{3,4}[ \t]+(?:comment|resolution)-[^\n]*\n(.*?)(?=^#{1,4}[ \t]+|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
_META_LINE = re.compile(r"^(?:-\s+[A-Za-z_][\w-]*:.*|\{.*\})\s*$")


def normalize_raw_key(value: object) -> str:
    return _RAW_PREFIX.sub("", str(value or "").strip()).upper()


def _text(value: object) -> str:
    return _SPACE.sub(" ", str(value or "").replace("\r\n", "\n").strip())


def _strip_meta(text: str) -> str:
    """Drop the machine-readable prefix (bullets or one JSON line) of a comment."""
    lines = text.split("\n")
    while lines and (not lines[0].strip() or _META_LINE.match(lines[0].strip())):
        lines.pop(0)
    return "\n".join(lines)


def _comments(body: object, values: object = ()) -> tuple[str, ...]:
    inline = [
        _text(_strip_meta(match.group(1))).lower()
        for match in _COMMENT_BLOCK.finditer(str(body or ""))
        if _text(_strip_meta(match.group(1)))
    ]
    remote = [
        _text(item).lower()
        for item in (values or [])
        if _text(item)
    ]
    return tuple(sorted(inline + remote))


def _body(value: object) -> str:
    text = str(value or "").replace("\r\n", "\n").strip()
    if text.startswith("---") and text.count("---") >= 2:
        text = text.split("---", 2)[2]
    # Comment blocks live in the body but are compared separately, so the body
    # projection must exclude them (platform copies never inline them).
    text = _COMMENT_BLOCK.sub("", text)
    return _text(text)


def canonical_projection(record: Mapping[str, Any]) -> dict[str, Any]:
    """Remove platform transport fields and preserve only lifecycle meaning."""
    labels = record.get("labels") or []
    # Only labels whose value is determined by the local document belong in a
    # replica comparison. phase/* is a creation-time snapshot the platforms
    # never update (proposed -> absorbed -> closed), and severity/* currently
    # lives ONLY on the platform copies: wt-create materialisation does not
    # write the severity frontmatter field. Comparing either would report a
    # fake divergence for every labelled raw. kind/* stays comparable.
    labels = [
        item for item in labels
        if not _text(item).lower().startswith(("phase/", "severity/"))
    ]
    state = _text(record.get("state")).lower()
    lifecycle_state = "open" if state in {"open", "proposed"} else "closed" if state in {"closed", "absorbed", "dropped"} else state
    title = _text(record.get("title")).lower()
    title = re.sub(r"^\[raw-[^\]]+\]\s*", "", title, flags=re.IGNORECASE)
    projection = {
        "raw_key": normalize_raw_key(record.get("raw_key") or record.get("local_id")),
        "title": title,
        "body": _body(record.get("body")),
        "state": lifecycle_state,
        "labels": tuple(sorted(_text(label).lower() for label in labels if _text(label))),
        "comments": _comments(record.get("body"), record.get("comments")),
    }
    fingerprint = hashlib.sha256(repr(tuple(projection.items())).encode("utf-8")).hexdigest()
    return {**projection, "fingerprint": fingerprint}


def reconcile(
    *, raw_key: str, configured_platforms: Iterable[str], replicas: Mapping[str, Mapping[str, Any]],
    local: Mapping[str, Any] | None = None, allow_degraded: bool = False,
) -> dict[str, Any]:
    """Create a deterministic, write-free receipt for one raw key.

    Facts block: a readable platform that has no replica (`missing`), an
    ambiguous match, or two readable replicas that disagree.  Ignorance does
    not: a platform we could not read (`unknown`) is reported as `degraded`,
    and only `allow_degraded` lets a caller proceed on a partial observation.
    """
    key = normalize_raw_key(raw_key)
    platforms = tuple(dict.fromkeys(str(item).strip() for item in configured_platforms if str(item).strip()))
    diagnostics: list[dict[str, str]] = []
    degraded: list[dict[str, str]] = []
    observations: dict[str, dict[str, Any]] = {}
    baseline: dict[str, Any] | None = None

    if not platforms:
        diagnostics.append({"scope": "configuration", "code": "no_configured_platforms", "detail": "configured platform set is empty"})
    for platform in platforms:
        replica = replicas.get(platform)
        if not isinstance(replica, Mapping):
            diagnostics.append({"scope": platform, "code": "missing_replica", "detail": "configured platform has no raw replica"})
            continue
        status = str(replica.get("status", "ok")).lower()
        if status in {"unknown", "error", "unreachable"}:
            degraded.append({
                "scope": platform,
                "code": "unknown",
                "reason": str(replica.get("reason") or "unreadable"),
                "detail": str(replica.get("error") or replica.get("reason") or "platform could not be read"),
            })
            continue
        if status != "ok":
            diagnostics.append({"scope": platform, "code": status, "detail": str(replica.get("error", "unresolved replica"))})
            continue
        projection = canonical_projection(replica)
        observations[platform] = projection
        if projection["raw_key"] != key:
            diagnostics.append({"scope": platform, "code": "raw_key_mismatch", "detail": projection["raw_key"]})
        elif baseline is None:
            baseline = projection
        elif projection["fingerprint"] != baseline["fingerprint"]:
            diagnostics.append({"scope": platform, "code": "content_diverged", "detail": "canonical title/body/state/labels/comments differ"})

    if local is not None:
        local_projection = canonical_projection(local)
        observations["local"] = local_projection
        if local_projection["raw_key"] != key:
            diagnostics.append({"scope": "local", "code": "raw_key_mismatch", "detail": local_projection["raw_key"]})
        elif baseline and local_projection["fingerprint"] != baseline["fingerprint"]:
            diagnostics.append({"scope": "local", "code": "content_diverged", "detail": "local canonical content differs from platforms"})

    blocked_by_facts = bool(diagnostics)
    unreadable = bool(degraded)
    # Nothing readable means no baseline: we cannot compare, so we cannot allow.
    ok = not blocked_by_facts and baseline is not None and (allow_degraded or not unreadable)
    if blocked_by_facts or baseline is None or (unreadable and not allow_degraded):
        decision = "block"
    elif unreadable:
        decision = "allow_degraded"
    else:
        decision = "allow"
    debt = (
        [{"platform": item["scope"], "reason": item["detail"], "raw_key": key} for item in degraded]
        if decision == "allow_degraded"
        else []
    )

    return {
        "raw_key": key,
        "configured_platforms": list(platforms),
        "ok": ok,
        "decision": decision,
        "diagnostics": diagnostics,
        "degraded": degraded,
        "debt": debt,
        "observations": observations,
    }
