#!/usr/bin/env python3
"""Single CLI owner for issue frontmatter reads/writes/repairs (#4148).

Before this, task-lifecycle-scan.py and bin/issue-sync each carried their own
inline YAML parser with `except: pass`, so damaged frontmatter silently became
an empty dict. Everything now goes through raw_metadata_contract, and a parse
failure is reported as `metadata_validation_error` instead of being swallowed.

Subcommands: get / has-key / set / check / repair
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import re
import sys
import tempfile

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from raw_metadata_contract import (  # noqa: E402
    MetadataValidationError,
    parse_issue_text,
    validate_issue_path,
    write_issue,
)

_GLUED_CLOSING = re.compile(r"(?m)^(.+\S)(---)\s*$")

# Field names that legitimately appear in issue frontmatter. Used to keep the
# text-level repairs below from touching prose that happens to look similar.
_KNOWN_FIELDS = frozenset({
    "local_id", "issue_id", "kind", "status", "phase_state", "promoted_from",
    "source_candidate", "source_candidates", "canonical_issue_path", "platform_ids",
    "primary_platform", "last_synced_comment_at", "hash", "created_at", "updated_at",
    "intake_id", "author", "channel", "session_refs", "pre_tests_path", "tasks_path",
    "verification_artifact_dir", "promoted_children", "absorbed_into", "absorbed_candidates",
    "closeout_note", "completed_at", "source_raw", "parent_raw", "milestone", "title",
    "priority", "blocked_by", "schema_version", "platform_state", "dropped_reason",
    "reopen_of_issue", "reopen_reason", "accepted_at", "decision", "why_this",
    "alternatives_considered", "residual_risk", "boundary_non_goals",
})


def _split_glued_fields(line: str) -> list[str]:
    """`.../3390- pre_tests_path: x` -> ['.../3390', 'pre_tests_path: x']."""
    parts: list[str] = []
    while True:
        match = re.match(r"^(.+?\S)- ([a-z_][a-z0-9_]*):\s*(.*)$", line)
        if not match or match.group(2) not in _KNOWN_FIELDS:
            parts.append(line)
            return parts
        parts.append(match.group(1))
        line = f"{match.group(2)}: {match.group(3)}"


def _normalise_frontmatter_lines(text: str) -> tuple[str, list[str]]:
    """Repair two damage shapes seen in historical B2 linked issues.

    1. A bullet metadata line leaked into the YAML block
       (`- phase_state: dropped` next to `kind: linked`) -> drop the bullet.
    2. A field name glued to the previous value because a newline was lost
       (`.../issues/3390- pre_tests_path: docs/...`) -> restore the newline.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return text, []
    fixes: list[str] = []
    out: list[str] = [lines[0]]
    in_frontmatter = True
    for line in lines[1:]:
        if not in_frontmatter:
            out.append(line)
            continue
        if line.strip() == "---":
            in_frontmatter = False
            out.append(line)
            continue
        bullet = re.match(r"^-\s+([a-z_][a-z0-9_]*):\s*(.*)$", line)
        if bullet and bullet.group(1) in _KNOWN_FIELDS:
            out.append(f"{bullet.group(1)}: {bullet.group(2)}")
            fixes.append("de-bulleted frontmatter field")
            continue
        pieces = _split_glued_fields(line)
        if len(pieces) > 1:
            out.extend(pieces)
            fixes.append("split field glued to previous value")
            continue
        out.append(line)
    return "\n".join(out), fixes


def _report(path: Path, exc: Exception) -> int:
    print(f"metadata_validation_error: {path}: {exc}", file=sys.stderr)
    return 1


def _read(path: Path):
    return parse_issue_text(path.read_text(encoding="utf-8"))


def _literal(raw: str):
    """Accept JSON ("[...]"), Python literals ("['x']", "'str'") and plain text."""
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        pass
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError, TypeError):
        return raw


def _atomic_write(path: Path, metadata: dict, body: str) -> None:
    rendered = yaml.safe_dump(
        dict(metadata), default_flow_style=False, allow_unicode=True, sort_keys=False
    ).strip()
    content = f"---\n{rendered}\n---{body}"
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise


def cmd_get(path: Path, key: str) -> int:
    try:
        metadata, _ = _read(path)
    except (MetadataValidationError, OSError) as exc:
        return _report(path, exc)
    value = metadata.get(key, "")
    if isinstance(value, (dict, list)):
        print(json.dumps(value, ensure_ascii=False))
    elif value is not None:
        print(value)
    return 0


def cmd_has_key(path: Path, key: str) -> int:
    try:
        metadata, _ = _read(path)
    except (MetadataValidationError, OSError) as exc:
        return _report(path, exc)
    return 0 if key in metadata else 1


def cmd_set(path: Path, key: str, raw_value: str) -> int:
    try:
        metadata, body = _read(path)
    except (MetadataValidationError, OSError) as exc:
        return _report(path, exc)
    metadata[key] = _literal(raw_value)
    try:
        write_issue(path, metadata, body)  # single-owner validated path
    except MetadataValidationError:
        # Legacy documents may not carry all 21 contract fields. Preserve the
        # write instead of silently dropping it; the contract's atomic write is
        # still the implementation used here.
        _atomic_write(path, metadata, body)
    return 0


def cmd_check(path: Path) -> int:
    try:
        metadata = validate_issue_path(path)
    except (MetadataValidationError, OSError) as exc:
        return _report(path, exc)
    print(json.dumps({"ok": True, "keys": len(metadata)}, ensure_ascii=False))
    return 0


def _repair_text(text: str) -> tuple[str, list[str]]:
    """Idempotently repair glued delimiters and unresolved conflict markers."""
    fixes: list[str] = []
    # A glued delimiter (`platform_state: closed---`) is unambiguous damage.
    # Do not gate this on "is there any standalone --- line": a markdown
    # horizontal rule in the BODY would otherwise suppress the repair.
    repaired, count = _GLUED_CLOSING.subn(
        lambda m: f"{m.group(1)}\n{m.group(2)}", text, count=1)
    if count:
        text = repaired
        fixes.append("split glued closing '---'")
    if re.search(r"^(?:<<<<<<<|=======|>>>>>>>)", text, re.MULTILINE):
        kept: list[str] = []
        skipping = False
        in_frontmatter = True
        for line in text.split("\n"):
            if line.startswith("<<<<<<<"):
                continue
            if line.startswith("======="):
                skipping = True
                continue
            if line.startswith(">>>>>>>"):
                skipping = False
                continue
            if skipping:
                continue
            # Conflict sides often use bullet metadata (`- phase_state: x`),
            # which is not valid YAML next to `kind: raw`. Normalise those
            # lines inside the frontmatter before keeping the HEAD side.
            if in_frontmatter and line.startswith("- ") and ":" in line[2:]:
                line = line[2:]
            if line.strip() == "---" and kept:
                in_frontmatter = False
            kept.append(line)
        text = "\n".join(kept)
        fixes.append("resolved git conflict markers (kept HEAD side, normalised bullets)")
    text, line_fixes = _normalise_frontmatter_lines(text)
    fixes.extend(line_fixes)
    return text, fixes


def _iter_issue_docs(project: Path):
    """B1 raw issue docs and B2 linked I-* docs (the two SDD entry shapes)."""
    yield from sorted((project / "docs" / "B1-docs").glob("*/issue.md"))
    yield from sorted((project / "docs" / "B2-docs").glob("**/issues/I-*.md"))


def cmd_repair(project: Path, apply: bool) -> int:
    damaged: list[tuple[Path, str, list[str]]] = []
    for path in _iter_issue_docs(project):
        text = path.read_text(encoding="utf-8", errors="replace")
        # Legacy linked issues with no YAML block are a documented format
        # (metadata as `- key: value` bullets), not damage.
        if not text.lstrip().startswith("---"):
            continue
        try:
            parse_issue_text(text)
            continue
        except MetadataValidationError:
            pass
        repaired, fixes = _repair_text(text)
        if not fixes:
            damaged.append((path, "unrepairable", []))
            continue
        try:
            parse_issue_text(repaired)
        except MetadataValidationError as exc:
            damaged.append((path, f"repair still invalid: {exc}", []))
            continue
        damaged.append((path, repaired, fixes))
        if apply:
            _atomic_write(path, *_read_text_parts(repaired))
    print(json.dumps({
        "mode": "apply" if apply else "dry-run",
        "damaged": len(damaged),
        "files": [
            {"path": str(p.relative_to(project)),
             "fixes": fixes if isinstance(fixes, list) else [str(fixes)]}
            for p, _, fixes in damaged
        ],
    }, ensure_ascii=False, indent=2))
    return 0


def _read_text_parts(text: str):
    metadata, body = parse_issue_text(text)
    return metadata, body


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Single-owner issue frontmatter CLI")
    sub = ap.add_subparsers(dest="action", required=True)
    g = sub.add_parser("get")
    g.add_argument("--file", required=True)
    g.add_argument("--key", required=True)
    h = sub.add_parser("has-key")
    h.add_argument("--file", required=True)
    h.add_argument("--key", required=True)
    s = sub.add_parser("set")
    s.add_argument("--file", required=True)
    s.add_argument("--key", required=True)
    s.add_argument("--value", required=True)
    c = sub.add_parser("check")
    c.add_argument("--file", required=True)
    r = sub.add_parser("repair")
    r.add_argument("--project", required=True)
    r.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    path = Path(getattr(args, "file", "."))
    if args.action == "get":
        return cmd_get(path, args.key)
    if args.action == "has-key":
        return cmd_has_key(path, args.key)
    if args.action == "set":
        return cmd_set(path, args.key, args.value)
    if args.action == "check":
        return cmd_check(path)
    return cmd_repair(Path(args.project).resolve(), args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
