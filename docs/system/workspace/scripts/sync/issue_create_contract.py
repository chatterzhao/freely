#!/usr/bin/env python3
"""Single owner for the platform projection of an issue document.

Both platform-create paths used to build this projection independently:

* ``bin/issue-sync`` derived labels in shell (``_labels``) and assembled the
  body with an ``awk`` "strip" that only deleted the ``---`` markers, so the
  YAML keys were published *unfenced* as body text;
* ``bin/freely feedback`` hard-coded ``kind/raw,phase/proposed,severity/Pn``
  and pushed its own frontmatter block.

Two entry points, two bodies, two label lists. A third entry point would have
forked them again. Everything now goes through :func:`strip_frontmatter`,
:func:`platform_body` and :func:`labels_for`.

Why the body keeps a frontmatter fence: the platform issue is the durable copy
of a raw issue. ``platform-adapter.pull_raw_issue()`` re-materializes the local
``issue.md`` from it and reads ``schema_version`` to pick the strict branch, so
dropping the block would silently downgrade every materialized raw to the
legacy metadata branch.

CLI (used by the shell callers so no shell code re-implements the shape)::

    issue_create_contract.py body   --file <issue.md> --local-id <id> --title <t>
    issue_create_contract.py labels --file <issue.md>
    issue_create_contract.py labels --kind raw --phase proposed --severity P1
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

# Timestamps are contract strings, not datetime objects: the same document must
# project identically before and after a write (see frontmatter_contract_cli).
yaml.SafeLoader.yaml_implicit_resolvers.pop("tag:yaml.org,2002:timestamp", None)

VALID_SEVERITIES = ("P0", "P1", "P2")
DEFAULT_SEVERITY = "P2"
# A platform issue should stay readable; the local document keeps the full text.
BODY_MAX_LINES = 80

_WORKFLOW_KIND = re.compile(r"^workflow_kind:\s*(\S+)\s*$", re.MULTILINE)
_COMMENT_HEADING = re.compile(r"^#{3,4}\s+(?:comment|resolution)-", re.IGNORECASE)


def strip_frontmatter(text: str) -> tuple[dict, str]:
    """Split ``---`` frontmatter from the Markdown body.

    Returns ``(metadata, body)``. A document without frontmatter yields an
    empty mapping and the original text.
    """
    parts = text.split("---", 2)
    if len(parts) >= 3 and parts[0].strip() == "":
        metadata = yaml.safe_load(parts[1]) or {}
        if isinstance(metadata, dict):
            return metadata, parts[2]
    return {}, text


def split_workflow_kind(markdown_body: str) -> tuple[str, str]:
    """Separate the ``workflow_kind: fix|feature`` marker from the human body."""
    match = _WORKFLOW_KIND.search(markdown_body)
    if not match:
        return "", markdown_body.lstrip("\n")
    remaining = (markdown_body[:match.start()] + markdown_body[match.end():]).lstrip("\n")
    return match.group(1), remaining


def normalize_severity(severity: object) -> str:
    value = str(severity or "").strip()
    return value if value in VALID_SEVERITIES else DEFAULT_SEVERITY


def labels_for(kind: object = "", phase: object = "", severity: object = "") -> str:
    """The one label list for a platform issue: kind, phase, severity."""
    labels = f"kind/{kind or 'unknown'}"
    phase_value = str(phase or "").strip()
    if phase_value and phase_value != "None":
        labels += f",phase/{phase_value}"
    labels += f",severity/{normalize_severity(severity)}"
    return labels


def _governance(local_id: str) -> list[str]:
    key = local_id[4:] if local_id.startswith("raw-") else local_id
    return [
        f"> **Freely 治理**：这是 raw issue `{local_id}`。实现前请用 "
        f"`wt-create --raw-key {key}` 创建专属工位，确保代码修改在包含此 "
        "raw-key 的分支上进行。",
        "",
    ]


def drop_comment_channel(markdown_body: str) -> list[str]:
    """Remove the local comment channel from the body projection.

    Comment blocks (``### comment-<ts>``) are synced as real platform comments,
    so republishing them inside the body doubles them. The old shell projection
    only deleted the ``## Comments`` heading and shipped the block text anyway.
    """
    kept: list[str] = []
    skipping = False
    for line in markdown_body.splitlines():
        stripped = line.strip()
        if stripped == "## Comments" or _COMMENT_HEADING.match(stripped):
            skipping = True
            continue
        # A comment body may itself start with `##`/`###` headings. Ending the
        # skip there published the comment text inside the body, so the body
        # projection could never agree with the local projection (#4653).
        # Blocks therefore run until the next comment marker or the end, which
        # is exactly how raw_reconciliation._COMMENT_BLOCK cuts them.
        if skipping:
            continue
        kept.append(line)
    return kept


def strip_local_h1(markdown_body: str) -> str:
    """Drop the document's own H1 from the platform projection.

    A raw document carries a real ``# <title>`` H1 so the replica gate can read
    the local title, but the platform body already declares that title as
    ``## <title>`` plus the metadata table. Re-emitting the H1 duplicated the
    header in every pushed body; because the gate strips the local H1 before
    comparing, a healthy raw could then never match its platform copies
    (#4653).
    """
    lines = str(markdown_body or "").splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if line.startswith("# "):
            rest = lines[index + 1:]
            while rest and not rest[0].strip():
                rest.pop(0)
            return "\n".join(rest)
        return markdown_body
    return markdown_body


def strip_repeated_header(markdown_body: str, title: str) -> str:
    """Drop a previously generated header from a materialised document.

    A document pulled back from a platform copy already carries ``## <title>``,
    the metadata table, the ``---`` rule and the governance note. Emitting them
    again on the next ``issue-sync update`` doubled the header, and the replica
    gate then reported ``content_diverged`` against every platform copy
    (#4653). Projection has to be idempotent: same input meaning -> same body.
    """
    lines = str(markdown_body or "").splitlines()
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines) or lines[index].strip() != f"## {title.strip()}":
        return markdown_body
    if not any(line.strip() == "| Field | Value |" for line in lines[index:index + 14]):
        return markdown_body
    cursor = index
    while cursor < len(lines) and not lines[cursor].strip().startswith("---"):
        cursor += 1
    if cursor < len(lines):
        cursor += 1  # the horizontal rule that closes the metadata table
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1
    if cursor < len(lines) and lines[cursor].lstrip().startswith("> **Freely 治理**"):
        cursor += 1
        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
    return "\n".join(lines[cursor:]).lstrip("\n")


def platform_body(
    local_id: str,
    title: str,
    metadata: dict,
    markdown_body: str,
    max_lines: int = BODY_MAX_LINES,
) -> str:
    """Render the platform body for ``local_id`` from its local document."""
    kind = str(metadata.get("kind") or "unknown")
    phase = str(metadata.get("phase_state") or "none")
    canonical = str(metadata.get("canonical_issue_path") or "none")
    created = str(metadata.get("created_at") or "unknown")
    updated = str(metadata.get("updated_at") or "unknown")
    workflow_kind, human_body = split_workflow_kind(markdown_body)
    human_body = strip_local_h1(human_body)
    human_body = strip_repeated_header(human_body, title)

    lines: list[str] = []
    if metadata:
        dumped = yaml.safe_dump(
            metadata, default_flow_style=False, allow_unicode=True, sort_keys=False
        ).strip()
        lines += ["---", dumped, "---", ""]
    if workflow_kind:
        lines += [f"workflow_kind: {workflow_kind}", ""]

    lines += [
        f"## {title}",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| local_id | `{local_id}` |",
        f"| kind | `{kind}` |",
        f"| phase_state | `{phase}` |",
        f"| canonical | `{canonical}` |",
        f"| created | {created} |",
        f"| updated | {updated} |",
        "",
        "---",
        "",
    ]
    if kind == "raw":
        lines += _governance(local_id)

    body_lines = drop_comment_channel(human_body)
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)
    while body_lines and not body_lines[-1].strip():
        body_lines.pop()
    lines += body_lines[:max_lines]
    return "\n".join(lines).rstrip("\n") + "\n"


def _read(path: Path) -> tuple[dict, str]:
    return strip_frontmatter(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="issue create contract")
    sub = parser.add_subparsers(dest="cmd", required=True)

    body = sub.add_parser("body", help="render the platform body")
    body.add_argument("--file", required=True)
    body.add_argument("--local-id", required=True)
    body.add_argument("--title", required=True)
    body.add_argument("--max-lines", type=int, default=BODY_MAX_LINES)

    labels = sub.add_parser("labels", help="render the platform label list")
    labels.add_argument("--file")
    labels.add_argument("--kind", default="")
    labels.add_argument("--phase", default="")
    labels.add_argument("--severity", default="")

    args = parser.parse_args(argv)

    if args.cmd == "labels":
        kind, phase, severity = args.kind, args.phase, args.severity
        if args.file:
            metadata, _ = _read(Path(args.file))
            kind = kind or metadata.get("kind", "")
            phase = phase or metadata.get("phase_state", "")
            severity = severity or metadata.get("severity", "")
        print(labels_for(kind, phase, severity))
        return 0

    metadata, markdown = _read(Path(args.file))
    sys.stdout.write(platform_body(args.local_id, args.title, metadata, markdown, args.max_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
