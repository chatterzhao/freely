#!/usr/bin/env python3
"""AT-001 for raw-20261104T075857Z / #4161 (R30, first stage).

The Bash↔Python boundary had no machine-readable declaration, so every call
site re-invented its own error handling: a missing field silently became an
empty string, a wrong-typed field was coerced, and a hung child was reported
as a generic failure. This AT pins three things:

* `contracts/cross-process/contract.yaml` declares the state-file protocol,
  the error envelope, the exit codes and the timeout semantics;
* `quality/cross_process_boundary.py` implements that envelope for the three
  boundary classes (missing field / type error / timeout);
* a lint keeps contract and implementation from drifting apart.

Runs against `git archive develop` to prove RED.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AT_NAME = "test-cross-process-contract.py"
CONTRACT_REL = "contracts/cross-process/contract.yaml"
RUNNER_REL = "docs/system/workspace/scripts/quality/cross_process_boundary.py"
LINT_REL = "bin/check-cross-process-contract"

OK: list[str] = []
FAIL: list[str] = []


def check(name: str, fn):
    try:
        ok, detail = fn()
    except Exception as exc:  # noqa: BLE001 - report, never abort the suite
        ok, detail = False, f"exception: {type(exc).__name__}: {exc}"
    (OK if ok else FAIL).append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + ("" if ok else f" — {detail}"))


def load(src: Path) -> dict:
    return json.loads((src / CONTRACT_REL).read_text(encoding="utf-8"))


def run(src: Path, *args: str, timeout: float = 30.0) -> subprocess.CompletedProcess:
    """Run the boundary runner from `src` with the given CLI arguments."""
    return subprocess.run(
        [sys.executable, str(src / RUNNER_REL), *args],
        capture_output=True, text=True, timeout=timeout,
    )


def emit(payload: dict) -> str:
    """Build a `-- sh -c ...` producer that prints one JSON object."""
    body = json.dumps(payload)
    return f"printf '%s\\n' '{body}'"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="", help="root to inspect (RED: a develop snapshot)")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else ROOT

    print(f"source: {src}")

    # ---- static: the contract exists, parses, and declares every section ----
    def c01():
        return (src / CONTRACT_REL).is_file(), f"missing {CONTRACT_REL}"

    def c02():
        data = load(src)
        return isinstance(data, dict) and bool(data), "contract is not a JSON object"

    def c03():
        data = load(src)
        return (data.get("schema_version") == 1 and bool(data.get("owner")),
                "schema_version must be 1 and owner must be set")

    def c04():
        sf = load(src).get("state_file") or {}
        need = {"format", "encoded_line", "legacy_line", "missing_key", "key_whitelist_owner"}
        missing = sorted(need - set(sf))
        return (
            not missing and sf.get("format") == "tabulator+json",
            f"state_file missing/unexpected: {missing} or bad format",
        )

    def c05():
        em = load(src).get("error_model") or {}
        codes = em.get("exit_codes") or {}
        need_codes = {"0", "1", "2", "3", "4"}
        envelope = set(em.get("envelope_fields") or [])
        need_fields = {"ok", "error.kind", "error.message", "error.source"}
        return (
            need_codes.issubset(set(codes)) and need_fields.issubset(envelope),
            f"error_model codes={sorted(codes)} fields={sorted(envelope)}",
        )

    def c06():
        to = load(src).get("timeout") or {}
        return (
            to.get("exit_code") == 4 and to.get("distinguishable") is True
            and float(to.get("default_seconds", 0)) > 0,
            f"timeout must declare exit_code=4 and a positive default: {to}",
        )

    def c07():
        bounds = load(src).get("boundaries") or []
        bad = [
            b.get("name") for b in bounds
            if not {"name", "error_class", "producer", "consumer", "required_keys"} <= set(b)
        ]
        return len(bounds) >= 3 and not bad, f"{len(bounds)} boundaries, malformed={bad}"

    def c08():
        kinds = set((load(src).get("error_model") or {}).get("kinds") or [])
        need = {"missing_field", "type_error", "timeout"}
        return need.issubset(kinds), f"error kinds={sorted(kinds)} missing={sorted(need - kinds)}"

    def c09():
        doc = src / "contracts/cross-process/README.md"
        if not doc.is_file():
            return False, "missing contracts/cross-process/README.md"
        text = doc.read_text(encoding="utf-8")
        need = ["missing_field", "type_error", "timeout"]
        missing = [n for n in need if n not in text]
        return not missing, f"README does not document {missing}"

    def c10():
        lint = src / LINT_REL
        return lint.is_file() and bool(lint.stat().st_mode & 0o111), f"missing/executable: {LINT_REL}"

    def c11():
        runner = src / RUNNER_REL
        if not runner.is_file():
            return False, f"missing {RUNNER_REL}"
        text = runner.read_text(encoding="utf-8")
        need = ["--require-key", "--timeout", "missing_field", "type_error", "timeout"]
        missing = [n for n in need if n not in text]
        return not missing, f"runner lacks {missing}"

    def c12():
        ta = (src / "bin/test-all").read_text(encoding="utf-8")
        core = "CORE=(\n  " + AT_NAME
        ci = "CI_CORE=(\n  " + AT_NAME
        return core in ta and ci in ta, "AT not wired into both CORE and CI_CORE"

    def c13():
        svg = (src / "docs/epics-map.svg").read_text(encoding="utf-8")
        return 'id="story-cross-process-contract"' in svg, "story not registered in epics-map"

    def c14():
        """The declared codes must match the ones the gates really use."""
        pr_body = (src / "docs/system/workspace/scripts/worktree/pr_body.py").read_text(encoding="utf-8")
        codes = (load(src).get("error_model") or {}).get("exit_codes") or {}
        refuse = "REFUSE_EXIT = 3" in pr_body
        return refuse and codes.get("3") is not None and "contract" in str(codes.get("3")).lower(), \
            f"code 3 must be the refuse/contract code (pr_body REFUSE_EXIT=3: {refuse})"

    check("contract file exists", c01)
    check("contract parses as JSON", c02)
    check("schema_version and owner declared", c03)
    check("state_file protocol section complete", c04)
    check("error_model codes and envelope declared", c05)
    check("timeout semantics declared", c06)
    check(">=3 boundaries each with required keys", c07)
    check("error kinds cover the three boundary classes", c08)
    check("single-page README documents all three classes", c09)
    check("lint exists and is executable", c10)
    check("boundary runner exposes the declared CLI", c11)
    check("AT wired into CORE and CI_CORE", c12)
    check("story registered in epics-map", c13)
    check("declared exit codes match the gates", c14)

    # ---- behaviour: the three boundary classes really fail closed ----
    def b15():
        """Missing field → exit 3 + missing_field, never an empty string."""
        proc = run(src, "run", "--require-key", "LAST_TESTED_COMMIT",
                   "--", "sh", "-c", emit({"STATUS": "ok"}))
        kind = ""
        try:
            kind = json.loads(proc.stdout)["error"]["kind"]
        except Exception:  # noqa: BLE001
            kind = proc.stdout.strip()[:120]
        return proc.returncode == 3 and kind == "missing_field", \
            f"rc={proc.returncode} kind={kind} stderr={proc.stderr.strip()[:120]}"

    def b16():
        """Wrong type → exit 3 + type_error, never coerced to str()."""
        proc = run(src, "run", "--require-key", "LAST_TESTED_COMMIT", "--expect-type", "str",
                   "--", "sh", "-c", emit({"LAST_TESTED_COMMIT": 12345}))
        kind = ""
        try:
            kind = json.loads(proc.stdout)["error"]["kind"]
        except Exception:  # noqa: BLE001
            kind = proc.stdout.strip()[:120]
        return proc.returncode == 3 and kind == "type_error", \
            f"rc={proc.returncode} kind={kind} stderr={proc.stderr.strip()[:120]}"

    def b17():
        """Timeout → exit 4, distinguishable from a contract violation (3)."""
        proc = run(src, "run", "--timeout", "0.4", "--require-key", "STATUS",
                   "--", "sh", "-c", "sleep 3; " + emit({"STATUS": "ok"}))
        kind = ""
        try:
            kind = json.loads(proc.stdout)["error"]["kind"]
        except Exception:  # noqa: BLE001
            kind = proc.stdout.strip()[:120]
        return proc.returncode == 4 and kind == "timeout", \
            f"rc={proc.returncode} kind={kind} stderr={proc.stderr.strip()[:120]}"

    check("missing key fails closed with missing_field", b15)
    check("wrong type fails closed with type_error", b16)
    check("timeout is exit 4 and distinguishable", b17)

    print(f"\nSUMMARY: {len(OK)} ok, {len(FAIL)} failed")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
