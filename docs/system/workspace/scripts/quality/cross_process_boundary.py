#!/usr/bin/env python3
"""Boundary runner for the Bash↔Python data contract (#4161).

One place implements the error envelope declared in
`contracts/cross-process/contract.yaml`, so a Bash caller no longer has to
guess whether an empty string meant "absent", or whether a non-zero exit meant
"wrong answer" or "took too long".

Three boundary classes, three distinct outcomes:

    missing field  -> exit 3, {"ok": false, "error": {"kind": "missing_field"}}
    wrong type     -> exit 3, {"ok": false, "error": {"kind": "type_error"}}
    timeout        -> exit 4, {"ok": false, "error": {"kind": "timeout"}}

On success the child's stdout is passed through unchanged (see `success_shape`
in the contract); the envelope is never invented for a healthy call.

CLI:
    cross_process_boundary.py run [--require-key KEY]... [--expect-type TYPE]
                                  [--timeout SECONDS] [--source NAME] -- CMD...
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_CONTRACT = 3
EXIT_TIMEOUT = 4

TYPE_CHECKS = {
    "str": lambda v: isinstance(v, str),
    "int": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "list": lambda v: isinstance(v, list),
    "dict": lambda v: isinstance(v, dict),
}


def envelope(kind: str, message: str, source: str) -> str:
    return json.dumps(
        {"ok": False, "error": {"kind": kind, "message": message, "source": source}},
        ensure_ascii=False,
    )


def fail(kind: str, message: str, source: str, code: int) -> int:
    print(envelope(kind, message, source))
    print(f"[cross-process] {kind}: {message}", file=sys.stderr)
    return code


def parse_args(argv: list[str]) -> tuple[argparse.Namespace, list[str]] | None:
    if "--" not in argv:
        return None
    split = argv.index("--")
    own, child = argv[:split], argv[split + 1:]
    ap = argparse.ArgumentParser(prog="cross_process_boundary")
    sub = ap.add_subparsers(dest="command", required=True)
    p_run = sub.add_parser("run", help="run a producer and validate its output")
    p_run.add_argument("--require-key", action="append", default=[],
                       help="key the caller cannot work without (repeatable)")
    p_run.add_argument("--expect-type", default="", choices=sorted(TYPE_CHECKS))
    p_run.add_argument("--timeout", type=float, default=30.0)
    p_run.add_argument("--source", default="boundary", help="name used in the envelope")
    try:
        ns = ap.parse_args(own)
    except SystemExit:
        return None
    return ns, child


def main(argv: list[str] | None = None) -> int:
    parsed = parse_args(sys.argv[1:] if argv is None else argv)
    if parsed is None:
        print(__doc__ or "", file=sys.stderr)
        return EXIT_USAGE
    args, child = parsed
    if not child:
        print("[cross-process] no child command after --", file=sys.stderr)
        return EXIT_USAGE

    try:
        proc = subprocess.run(child, capture_output=True, text=True, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        # 4, never 1 or 3: "took too long" must stay distinguishable.
        return fail("timeout", f"child exceeded {args.timeout:g}s", args.source, EXIT_TIMEOUT)
    except FileNotFoundError as exc:
        return fail("missing_field", f"child not found: {exc.filename}", args.source, EXIT_CONTRACT)

    if proc.returncode != 0:
        detail = (proc.stderr or "").strip().splitlines()
        return fail("invalid_json", f"child exited {proc.returncode}: "
                    f"{detail[-1] if detail else 'no stderr'}", args.source, EXIT_CONTRACT)

    raw = (proc.stdout or "").strip()
    try:
        payload: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        return fail("invalid_json", f"stdout is not JSON: {exc}", args.source, EXIT_CONTRACT)
    if not isinstance(payload, dict):
        return fail("type_error", f"expected a JSON object, got {type(payload).__name__}",
                    args.source, EXIT_CONTRACT)

    for key in args.require_key:
        if key not in payload:
            return fail("missing_field", f"{key} is required but absent", args.source, EXIT_CONTRACT)
        if args.expect_type:
            value = payload[key]
            if not TYPE_CHECKS[args.expect_type](value):
                return fail(
                    "type_error",
                    f"{key} must be {args.expect_type}, got {type(value).__name__}",
                    args.source, EXIT_CONTRACT,
                )

    sys.stdout.write(proc.stdout)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
