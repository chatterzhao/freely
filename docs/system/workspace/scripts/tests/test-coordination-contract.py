#!/usr/bin/env python3
"""AT-001 for raw-20261104T075903Z / #4162 (R29, first stage).

Coordination semantics get a machine-readable contract; the input-required
reason enum moves out of agents/ so watchdog_sse.py no longer needs a
sys.path.insert hack; a lint guards enum/contract parity and the import graph.

Runs against `git archive develop` to prove RED.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AT_NAME = "test-coordination-contract.py"
RUNTIME_REL = "docs/system/workspace/scripts/runtime"

OK: list[str] = []
FAIL: list[str] = []


def check(name: str, fn):
    try:
        ok, detail = fn()
    except Exception as exc:
        ok, detail = False, f"exception: {type(exc).__name__}: {exc}"
    (OK if ok else FAIL).append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}" + ("" if ok else f" — {detail}"))


def contract(src: Path) -> Path:
    return src / "contracts/coordination/contract.yaml"


def load(src: Path):
    return json.loads(contract(src).read_text(encoding="utf-8"))


def enum_values(src: Path) -> set[str]:
    p = src / RUNTIME_REL / "coordination/input_required_reason.py"
    return set(re.findall(r'=\s*"([a-z][a-z0-9:\-]+)"', p.read_text(encoding="utf-8")))


def lint_fixture(src: Path, mismatch: bool) -> int:
    lint = src / "bin/check-coordination-contract"
    if not lint.is_file():
        raise FileNotFoundError(f"missing lint: {lint}")
    with tempfile.TemporaryDirectory(prefix="coord-") as td:
        d = Path(td)
        (d / "contracts/coordination").mkdir(parents=True)
        reasons = ["needs-review:b1", "unknown"]
        (d / "contracts/coordination/contract.yaml").write_text(json.dumps({
            "schema_version": 1,
            "task_states": ["submitted", "working", "input-required", "completed", "failed", "canceled"],
            "input_required_reasons": reasons,
            "sse_topics": ["task_state_update"],
            "exit_contracts": {"delegate_workers": "delegate"},
        }), encoding="utf-8")
        cod = d / RUNTIME_REL / "coordination"
        cod.mkdir(parents=True)
        values = reasons[:-1] if mismatch else reasons
        body = "\n".join(f'    R{i} = "{v}"' for i, v in enumerate(values))
        (cod / "input_required_reason.py").write_text(
            "from enum import Enum\n\nclass InputRequiredReason(Enum):\n" + body + "\n", encoding="utf-8")
        (cod / "__init__.py").write_text("", encoding="utf-8")
        (d / RUNTIME_REL / "watchdog_sse.py").write_text(
            "from coordination.input_required_reason import InputRequiredReason\n", encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(lint), "--root", str(d)], capture_output=True, text=True).returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=str(ROOT))
    src = Path(ap.parse_args().source_dir).resolve()
    runtime = src / RUNTIME_REL

    print("=== STATIC: coordination contract ===")

    def c1():
        return contract(src).is_file(), f"missing {contract(src)}"

    check("coordination contract exists", c1)

    def c2():
        load(src)
        return True, ""

    check("contract is stdlib-parseable JSON/YAML subset", c2)

    def c3():
        m = load(src)
        missing = [k for k in ("task_states", "input_required_reasons", "sse_topics", "exit_contracts")
                   if not m.get(k)]
        return not missing, f"missing sections: {missing}"

    check("contract declares states/reasons/topics/exit-contracts", c3)

    def c4():
        cod = runtime / "coordination"
        return (cod / "__init__.py").is_file() and (cod / "input_required_reason.py").is_file(), "coordination package incomplete"

    check("coordination package owns the reason enum", c4)

    def c5():
        text = (runtime / "watchdog_sse.py").read_text(encoding="utf-8")
        bad = [l for l in text.splitlines() if "sys.path.insert" in l and "agents" in l]
        return not bad, f"agents sys.path hack: {bad}"

    check("watchdog_sse.py has no agents sys.path hack", c5)

    def c6():
        hits = []
        for p in runtime.rglob("*.py"):
            for i, l in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if "sys.path.insert" in l and "agents" in l:
                    hits.append(f"{p.relative_to(src)}:{i}")
        return not hits, f"hits: {hits[:3]}"

    check("no runtime file injects agents/ into sys.path", c6)

    def c7():
        text = (runtime / "watchdog_sse.py").read_text(encoding="utf-8")
        return "from coordination.input_required_reason import" in text, "watchdog still uses bare import"

    check("watchdog imports from the coordination package", c7)

    def c8():
        p = src / "docs/system/workspace/agents/input_required_reason.py"
        return not p.is_file(), "legacy agents/input_required_reason.py still present"

    check("reason enum moved out of agents/", c8)

    def c9():
        want = set(load(src).get("input_required_reasons", []))
        got = enum_values(src)
        return bool(want) and want == got, f"contract={sorted(want)[:4]} enum={sorted(got)[:4]}"

    check("contract reasons match the runtime enum", c9)

    def c10():
        p = src / "contracts/coordination/README.md"
        if not p.is_file():
            return False, "missing single-page doc"
        t = p.read_text(encoding="utf-8")
        states = load(src).get("task_states", [])
        exits = load(src).get("exit_contracts", {})
        return all(s in t for s in states) and all(k in t for k in exits), "doc does not list legal values"

    check("single-page doc lists state machine and exit contracts", c10)

    def c11():
        return (src / "bin/check-coordination-contract").is_file(), "missing lint"

    check("coordination lint exists", c11)

    print("=== BEHAVIOR: lint parity + import graph ===")

    def c12():
        rc = lint_fixture(src, mismatch=True)
        return rc != 0, f"lint returned {rc} for a contract/enum mismatch"

    check("lint refuses contract/enum drift", c12)

    def c13():
        rc = lint_fixture(src, mismatch=False)
        return rc == 0, f"lint returned {rc} for a compliant fixture"

    check("lint accepts a compliant fixture", c13)

    def c14():
        cod = runtime / "coordination"
        bad = [str(p.relative_to(src)) for p in cod.rglob("*.py")
               if re.search(r"import\s+runtime\.freely|from\s+runtime\s+import\s+freely", p.read_text(encoding="utf-8"))]
        return not bad, f"reverse dependencies: {bad}"

    check("coordination package has no reverse dependency on runtime/freely", c14)

    def c15():
        text = (src / "bin/test-all").read_text(encoding="utf-8")
        core = re.search(r"CORE=\((.*?)\)", text, re.S)
        ci = re.search(r"CI_CORE=\((.*?)\)", text, re.S)
        return bool(core and ci and AT_NAME in core.group(1) and AT_NAME in ci.group(1)), "AT not in both suites"

    check("AT wired into test-all CORE and CI_CORE", c15)

    def c16():
        text = (src / "docs/epics-map.svg").read_text(encoding="utf-8")
        return 'id="story-coordination-contract"' in text, "story not registered"

    check("B2 story registered in epics-map.svg", c16)

    print(f"SUMMARY: {len(OK)} ok, {len(FAIL)} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
