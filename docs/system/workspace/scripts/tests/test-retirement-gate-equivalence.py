#!/usr/bin/env python3
"""AT-001 for raw-20261126T120834Z / #4723.

The retirement gate must consume the SAME three-state verdict as
`test-evidence.py validate` (current/equivalent/stale), not its own HEAD
equality check.

Usage: python3 ...test-retirement-gate-equivalence.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

OK = FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global OK, FAIL
    if cond:
        OK += 1
        print(f"ok   {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def git(fixture: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(fixture), *args],
                          capture_output=True, text=True)


def commit(fixture: Path, rel: str, text: str) -> str:
    path = fixture / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    git(fixture, "add", rel)
    git(fixture, "commit", "-q", "-m", f"commit {rel}")
    return git(fixture, "rev-parse", "HEAD").stdout.strip()


def make_fixture(root: Path, with_gate: bool = True) -> tuple[Path, object]:
    td = tempfile.TemporaryDirectory(prefix="freely-retire-equiv-")
    fixture = Path(td.name)
    qdir = fixture / "docs/system/workspace/scripts/quality"
    qdir.mkdir(parents=True)
    shutil.copy(root / "docs/system/workspace/scripts/quality/pretests-retirement-gate",
                qdir / "pretests-retirement-gate")
    shutil.copy(root / "docs/system/workspace/scripts/quality/test-evidence.py",
                qdir / "test-evidence.py")
    stub = fixture / "bin/pretests-gate"
    stub.parent.mkdir(parents=True)
    stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    stub.chmod(0o755)
    git(fixture, "init", "-q")
    git(fixture, "config", "user.email", "fixture@local")
    git(fixture, "config", "user.name", "fixture")
    head = commit(fixture, "README.md", "fixture\n")
    if with_gate:
        evidence = fixture / ".freely/run/test-evidence.log"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("fixture evidence\n", encoding="utf-8")
        subprocess.run(
            ["python3", str(qdir / "test-evidence.py"), "write",
             "--gate", str(fixture / ".freely/run/test-gate.env"),
             "--status", "completed", "--command", "fixture",
             "--exit-code", "0", "--evidence", str(evidence), "--head", head],
            capture_output=True, text=True, check=True,
        )
    return fixture, td


def run_gate(fixture: Path):
    gate = fixture / "docs/system/workspace/scripts/quality/pretests-retirement-gate"
    return subprocess.run(["bash", str(gate), "--project", str(fixture),
                           "--worktree-path", str(fixture)],
                          cwd=fixture, capture_output=True, text=True)


def attest(fixture: Path, sensitive: str) -> subprocess.CompletedProcess:
    qdir = fixture / "docs/system/workspace/scripts/quality"
    return subprocess.run(
        ["python3", str(qdir / "test-evidence.py"), "attest-meta",
         "--gate", str(fixture / ".freely/run/test-gate.env"),
         "--worktree", str(fixture), "--sensitive-paths", sensitive],
        capture_output=True, text=True,
    )


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    gate_src = (root / "docs/system/workspace/scripts/quality/pretests-retirement-gate").read_text(encoding="utf-8")

    check("self-made HEAD stale check removed", "pretests_stale" not in gate_src)
    check("validate verdict consumed", "validate" in gate_src and "--json" in gate_src)
    check("not_tested guard preserved", "pretests_not_tested" in gate_src)

    fixture, td = make_fixture(root)
    try:
        check("current evidence accepted", run_gate(fixture).returncode == 0)

        commit(fixture, "docs/B2-docs/note.md", "metadata only\n")
        before = run_gate(fixture).returncode
        result = attest(fixture, "docs/system/workspace/scripts/,bin/,tests/")
        check("attest-meta accepts metadata commit", result.returncode == 0, result.stderr[:200])
        after = run_gate(fixture)
        check("equivalent evidence accepted by retirement gate", after.returncode == 0,
              f"before={before}: {after.stderr[:200]}")

        commit(fixture, "bin/new-runtime-helper", "#!/bin/sh\nexit 0\n")
        stale = run_gate(fixture)
        check("stale evidence rejected", stale.returncode == 1, stale.stderr[:200])
        refused = attest(fixture, "docs/system/workspace/scripts/,bin/,tests/")
        check("attest-meta fails closed on real code change", refused.returncode != 0)
    finally:
        td.cleanup()

    empty, td2 = make_fixture(root, with_gate=False)
    try:
        check("not_tested rejected", run_gate(empty).returncode == 1)
    finally:
        td2.cleanup()

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
