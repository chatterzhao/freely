#!/usr/bin/env python3
"""Review gate: a core-runtime change must ship function-level RED evidence (#4165).

`pr-review-guarded` reviewed documents and PR receipts but never asked whether
a change to the 27k-line runtime had a failing test first. This gate answers
exactly that, and only that:

* diff does not touch the runtime  → SKIP (exit 2), review continues as before;
* touches runtime, unit test added/modified, owner pre-tests has an acceptance
  item with red-green-status=green + actual_RED_output + existing artifact
  → PASS (exit 0);
* otherwise → REFUSE (exit 1) with the missing pieces spelled out.

Exit codes are distinct so the caller can tell "not applicable" from "failed".

CLI:
    runtime_red_gate.py --project <path> [--changed-files <file>] [--raw-key <key>]
    runtime_red_gate.py --project <path> --changed-files <file> --json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "worktree"))
from pr_body import (  # noqa: E402  (sibling contract module)
    RUNTIME_EXACT,
    RUNTIME_PATH_PREFIXES,
    normalize_raw_key,
    pre_tests_path,
    read_evidence,
)

UNIT_TEST_PREFIX = "docs/system/workspace/scripts/tests/unit/"

SKIP = 2
PASS = 0
REFUSE = 1


def runtime_files(paths: list[str]) -> list[str]:
    hit = []
    for path in paths:
        if path in RUNTIME_EXACT or any(path.startswith(p) for p in RUNTIME_PATH_PREFIXES):
            hit.append(path)
    return hit


def unit_test_files(paths: list[str]) -> list[str]:
    return [p for p in paths if p.startswith(UNIT_TEST_PREFIX)]


def changed_files(project: Path, base_ref: str = "") -> list[str]:
    refs = [base_ref] if base_ref else []
    refs += ["origin/develop", "develop", "origin/main", "main"]
    for ref in refs:
        if not ref:
            continue
        proc = subprocess.run(
            ["git", "-C", str(project), "diff", "--name-only", f"{ref}...HEAD"],
            capture_output=True, text=True,
        )
        if proc.returncode == 0:
            return [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return []


def resolve_raw_key(project: Path, explicit: str) -> str:
    if explicit:
        return normalize_raw_key(explicit)
    proc = subprocess.run(
        ["git", "-C", str(project), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True,
    )
    branch = proc.stdout.strip()
    import re
    match = re.search(r"(\d{8}T\d{6}Z)", branch)
    return match.group(1) if match else ""


def evaluate(project: Path, files: list[str], raw_key: str) -> dict:
    runtime_hits = runtime_files(files)
    if not runtime_hits:
        return {"verdict": "skip", "reason": "diff does not touch the core runtime",
                "runtime_files": [], "unit_test_files": [], "evidence": []}

    unit_hits = unit_test_files(files)
    evidence = [
        item for item in read_evidence(project, raw_key)
        if item.get("red-green-status") == "green" and item.get("actual_RED_output")
    ]
    artifacts_ok = []
    for item in evidence:
        listed = [p.strip() for p in (item.get("evidence_file") or "").split(",") if p.strip()]
        if listed and all((project / p).is_file() for p in listed):
            artifacts_ok.append(item)

    reasons = []
    if not unit_hits:
        reasons.append(
            f"no function-level test added or changed under {UNIT_TEST_PREFIX}"
        )
    if not evidence:
        reasons.append(
            "owner pre-tests has no acceptance item with red-green-status=green "
            "and actual_RED_output"
        )
    elif not artifacts_ok:
        reasons.append(
            "the RED evidence lists artifact paths that do not exist on disk"
        )

    verdict = "pass" if not reasons else "refuse"
    return {
        "verdict": verdict,
        "reason": "; ".join(reasons),
        "raw_key": raw_key,
        "runtime_files": runtime_hits,
        "unit_test_files": unit_hits,
        "evidence": [
            {"acceptance_id": item.get("acceptance_id"), "evidence_file": item.get("evidence_file")}
            for item in evidence
        ],
        "pre_tests": str(pre_tests_path(project, raw_key) or ""),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="core-runtime RED evidence gate")
    parser.add_argument("--project", required=True)
    parser.add_argument("--changed-files", default="")
    parser.add_argument("--raw-key", default="")
    parser.add_argument("--base-ref", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    project = Path(args.project).resolve()
    if args.changed_files == "-":
        files = [line.strip() for line in sys.stdin if line.strip()]
    elif args.changed_files:
        files = [line.strip() for line in Path(args.changed_files).read_text().splitlines() if line.strip()]
    else:
        files = changed_files(project, args.base_ref)

    raw_key = resolve_raw_key(project, args.raw_key)
    result = evaluate(project, files, raw_key)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif result["verdict"] == "skip":
        print(f"[runtime-red-gate] skip: {result['reason']}")
    elif result["verdict"] == "pass":
        print(f"[runtime-red-gate] pass: {len(result['runtime_files'])} runtime file(s), "
              f"{len(result['unit_test_files'])} unit test(s), evidence={result['evidence']}")
    else:
        print(f"[runtime-red-gate] refuse: {result['reason']}", file=sys.stderr)

    return {"skip": SKIP, "pass": PASS, "refuse": REFUSE}[result["verdict"]]


if __name__ == "__main__":
    raise SystemExit(main())
