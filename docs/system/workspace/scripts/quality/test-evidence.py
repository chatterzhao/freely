#!/usr/bin/env python3
"""Single source of truth for machine-verifiable test evidence (#4151).

`test-gate.env` used to be three hand-writable lines: TEST_STATUS,
LAST_TESTED_AT, LAST_TESTED_COMMIT. Anyone could `printf` those and the
retirement gate would happily say "tests passed". This module owns the format
and the validation so `freely test-gate run` (which really executes a command)
is the only writer the gate trusts:

    write     atomically record command + real exit code + evidence sha256 + HEAD
    validate  prove the verdict is complete, successful, untampered and current
    manifest-add  record a version-controlled evidence file and its hash
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

FIELDS = (
    "TEST_STATUS", "LAST_TESTED_AT", "LAST_TESTED_COMMIT",
    "TEST_COMMAND", "TEST_EXIT_CODE", "EVIDENCE_FILE", "EVIDENCE_SHA256", "EVIDENCE_HEAD",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_env(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return data
    for raw in lines:
        line = raw.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def _atomic_env(path: Path, values: dict[str, str]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".test-evidence.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            for key in FIELDS:
                handle.write(f'{key}="{values.get(key, "")}"\n')
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def head_of(worktree: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(worktree), "rev-parse", "HEAD"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def write_evidence(gate: Path, *, status: str, command: str, exit_code: int,
                   evidence: Path, head: str) -> dict[str, str]:
    evidence = Path(evidence).resolve()
    if not evidence.is_file():
        raise ValueError(f"evidence file is missing: {evidence}")
    values = {
        "TEST_STATUS": status,
        "LAST_TESTED_AT": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "LAST_TESTED_COMMIT": head,
        "TEST_COMMAND": command,
        "TEST_EXIT_CODE": str(exit_code),
        "EVIDENCE_FILE": str(evidence),
        "EVIDENCE_SHA256": sha256(evidence),
        "EVIDENCE_HEAD": head,
    }
    _atomic_env(gate, values)
    return values


def validate(gate: Path, worktree: Path) -> dict:
    gate = Path(gate)
    errors: list[str] = []
    values = parse_env(gate)
    if not gate.is_file():
        return {"ok": False, "errors": [f"missing test-gate file: {gate}"]}

    missing = [field for field in FIELDS if not values.get(field)]
    if missing:
        errors.append("missing machine-evidence fields: " + ", ".join(missing))
    if values.get("TEST_STATUS") != "completed":
        errors.append(f"TEST_STATUS is {values.get('TEST_STATUS') or '<empty>'}, not completed")
    if values.get("TEST_EXIT_CODE") != "0":
        errors.append(f"TEST_EXIT_CODE is {values.get('TEST_EXIT_CODE') or '<empty>'}, not 0")
    timestamp = values.get("LAST_TESTED_AT", "")
    if not timestamp or timestamp.startswith("1970"):
        errors.append("LAST_TESTED_AT is missing or the 1970 sentinel")

    evidence = Path(values.get("EVIDENCE_FILE", ""))
    if not values.get("EVIDENCE_SHA256"):
        errors.append("EVIDENCE_SHA256 is missing")
    elif not evidence.is_file():
        errors.append(f"hash binding failed: evidence file is missing: {evidence}")
    elif sha256(evidence) != values["EVIDENCE_SHA256"]:
        errors.append("hash binding failed: evidence sha256 mismatch (tampered or stale)")

    head = head_of(worktree)
    if not head:
        errors.append("cannot resolve worktree HEAD")
    else:
        if values.get("LAST_TESTED_COMMIT") != head:
            errors.append("LAST_TESTED_COMMIT does not match worktree HEAD")
        if values.get("EVIDENCE_HEAD") != head:
            errors.append("EVIDENCE_HEAD does not match worktree HEAD")

    return {"ok": not errors, "errors": errors,
            "details": {k: values.get(k, "") for k in FIELDS}}


def manifest_add(project: Path, file: Path) -> dict:
    project, file = Path(project).resolve(), Path(file).resolve()
    if not file.is_file():
        raise ValueError(f"evidence file is missing: {file}")
    try:
        rel = file.relative_to(project).as_posix()
    except ValueError:
        rel = str(file)
    manifest = project / ".freely/run/evidence-manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        payload = {"files": []}
    files = [item for item in payload.get("files", []) if item.get("path") != rel]
    files.append({"path": rel, "sha256": sha256(file)})
    payload["files"] = sorted(files, key=lambda item: item["path"])
    tmp = manifest.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, manifest)
    return {"path": rel, "sha256": sha256(file), "manifest": str(manifest)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Freely machine-verifiable test evidence")
    sub = ap.add_subparsers(dest="action", required=True)

    w = sub.add_parser("write")
    w.add_argument("--gate", required=True)
    w.add_argument("--status", required=True)
    w.add_argument("--command", required=True)
    w.add_argument("--exit-code", required=True, type=int)
    w.add_argument("--evidence", required=True)
    w.add_argument("--head", required=True)

    v = sub.add_parser("validate")
    v.add_argument("--gate", required=True)
    v.add_argument("--worktree", required=True)
    v.add_argument("--json", action="store_true")

    m = sub.add_parser("manifest-add")
    m.add_argument("--project", required=True)
    m.add_argument("--file", required=True)

    args = ap.parse_args(argv)
    if args.action == "write":
        try:
            payload = write_evidence(
                args.gate, status=args.status, command=args.command,
                exit_code=args.exit_code, evidence=args.evidence, head=args.head,
            )
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print(json.dumps({"ok": True, "recorded": payload}, ensure_ascii=False))
        return 0
    if args.action == "validate":
        payload = validate(args.gate, args.worktree)
        if args.json:
            print(json.dumps(payload, ensure_ascii=False))
        else:
            for err in payload["errors"]:
                print(f"  - {err}", file=sys.stderr)
        return 0 if payload["ok"] else 1
    try:
        payload = manifest_add(args.project, args.file)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, **payload}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
