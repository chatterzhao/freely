#!/usr/bin/env python3
"""Compose the PR body, with a mandatory RED-evidence section (#4165).

Before this module the body was `See commits for details.` — a PR could change
the 27k-line core runtime without a single line saying which test was red
before the fix. The body now always carries a `## RED 证据` section:

* evidence found in the owner pre-tests → the command, the RED output, the
  GREEN output and the artifact paths;
* diff does not touch the core runtime → the section says so explicitly
  ("不适用"), so a reviewer can tell "not needed" from "forgotten";
* diff touches the core runtime and no evidence exists → exit 3. The caller
  (pr-create-guarded) fails closed instead of opening a PR that cannot be
  reviewed for TDD fidelity.

CLI:
    pr_body.py render --project <path> --raw-key <key> [--base-body <text>]
                      [--touches-runtime 0|1]
    pr_body.py evidence --project <path> --raw-key <key>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RUNTIME_PATH_PREFIXES = (
    "docs/system/workspace/scripts/runtime/",
)
RUNTIME_EXACT = ("bin/freely",)
RED_HEADER = "## RED 证据"
# Distinct from 1 (hard failure): the caller can tell "needs evidence" apart.
REFUSE_EXIT = 3
DEFAULT_BODY = "See commits for details."


def normalize_raw_key(raw_key: str) -> str:
    key = (raw_key or "").strip()
    if key.startswith("raw-"):
        return key[4:]
    return key


def pre_tests_path(project: Path, raw_key: str) -> Path | None:
    """Find `docs/B2-docs/**/raw-<key>/verification/pre-tests.md`."""
    key = normalize_raw_key(raw_key)
    if not key:
        return None
    root = project / "docs" / "B2-docs"
    if not root.is_dir():
        return None
    matches = sorted(root.glob(f"**/raw-{key}/verification/pre-tests.md"))
    return matches[0] if matches else None


def _acceptance_blocks(text: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        if line.startswith("### "):
            if current is not None:
                blocks.append(current)
            current = {}
            continue
        if current is None:
            continue
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        body = stripped[2:]
        if ":" not in body:
            continue
        key, _, value = body.partition(":")
        current[key.strip()] = value.strip()
    if current is not None:
        blocks.append(current)
    return blocks


def read_evidence(project: Path, raw_key: str) -> list[dict[str, str]]:
    """Return acceptance items that carry RED evidence, most complete first."""
    path = pre_tests_path(project, raw_key)
    if path is None or not path.is_file():
        return []
    items = []
    for block in _acceptance_blocks(path.read_text(encoding="utf-8", errors="replace")):
        if not block.get("actual_RED_output"):
            continue
        block.setdefault("acceptance_id", block.get("id", "AT-?"))
        block["_pre_tests_path"] = str(path.relative_to(project))
        items.append(block)
    items.sort(key=lambda item: (item.get("red-green-status", "") != "green",))
    return items


def _first_line(text: str, limit: int = 160) -> str:
    for line in (text or "").splitlines():
        if line.strip():
            return line.strip()[:limit]
    return ""


def _existing_artifacts(project: Path, item: dict[str, str]) -> list[str]:
    kept = []
    for raw in (item.get("evidence_file") or "").split(","):
        rel = raw.strip()
        if rel and (project / rel).is_file():
            kept.append(rel)
    return kept


def render_body(
    base_body: str,
    evidence: list[dict[str, str]],
    touches_runtime: bool,
    project: Path,
) -> str:
    body = (base_body or "").strip()
    if not body:
        body = DEFAULT_BODY

    if evidence:
        item = evidence[0]
        artifacts = _existing_artifacts(project, item)
        lines = [
            body,
            "",
            RED_HEADER,
            f"- 验收项: {item.get('acceptance_id', 'AT-?')}（red-green-status: {item.get('red-green-status', 'unknown')}）",
            f"- 命令: `{item.get('test_command', 'n/a')}`",
            f"- RED: {_first_line(item.get('actual_RED_output', ''))}",
            f"- GREEN: {_first_line(item.get('actual_output', ''))}",
            f"- 证据: {', '.join(artifacts) if artifacts else (item.get('evidence_file') or 'n/a')}",
            f"- pre-tests: {item.get('_pre_tests_path', 'n/a')}",
        ]
        if len(evidence) > 1:
            extra = ", ".join(item.get("acceptance_id", "AT-?") for item in evidence[1:])
            lines.append(f"- 其他有 RED 记录的验收项: {extra}")
        return "\n".join(lines) + "\n"

    if touches_runtime:
        print(
            "RED evidence missing: this diff touches the core runtime "
            f"({', '.join(RUNTIME_PATH_PREFIXES + RUNTIME_EXACT)}) but the owner "
            "pre-tests has no acceptance item with actual_RED_output. "
            "Record the failing test first (skill:freely-test-RED-execution), "
            "then re-run freely pr-create-guarded.",
            file=sys.stderr,
        )
        raise SystemExit(REFUSE_EXIT)

    return "\n".join([
        body,
        "",
        RED_HEADER,
        "- 不适用：本次 diff 未触及 `docs/system/workspace/scripts/runtime/**` 或 `bin/freely`。",
    ]) + "\n"


def touches_runtime(paths: list[str]) -> bool:
    for path in paths:
        if path in RUNTIME_EXACT:
            return True
        if any(path.startswith(prefix) for prefix in RUNTIME_PATH_PREFIXES):
            return True
    return False


def _read_changed_files(project: Path) -> list[str]:
    import subprocess

    for ref in ("origin/develop", "develop", "origin/main", "main"):
        proc = subprocess.run(
            ["git", "-C", str(project), "diff", "--name-only", f"{ref}...HEAD"],
            capture_output=True, text=True,
        )
        if proc.returncode == 0:
            return [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PR body with RED evidence")
    sub = parser.add_subparsers(dest="cmd", required=True)

    render = sub.add_parser("render")
    render.add_argument("--project", required=True)
    render.add_argument("--raw-key", required=True)
    render.add_argument("--base-body", default="")
    render.add_argument("--touches-runtime", choices=("0", "1"), default=None)

    evidence = sub.add_parser("evidence")
    evidence.add_argument("--project", required=True)
    evidence.add_argument("--raw-key", required=True)

    args = parser.parse_args(argv)
    project = Path(args.project).resolve()

    if args.cmd == "evidence":
        print(json.dumps(read_evidence(project, args.raw_key), indent=2, ensure_ascii=False))
        return 0

    touches = touches_runtime(_read_changed_files(project))
    if args.touches_runtime is not None:
        touches = args.touches_runtime == "1"
    body = render_body(args.base_body, read_evidence(project, args.raw_key), touches, project)
    sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
