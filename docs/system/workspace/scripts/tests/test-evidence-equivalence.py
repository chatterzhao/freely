#!/usr/bin/env python3
"""AT-001 for raw-20261125T094413Z / I-20261125T094413Z-A.

Machine-verifiable test evidence must distinguish 'tests are current' from
'tests are equivalent through metadata-only commits'.  A commit that only
changes governance metadata (not a test dependency, not the test definition)
must be able to carry evidence forward; a commit touching a sensitive path or
a test definition must invalidate it.

Structural checks on test-evidence.py + behavioural checks in an isolated git
repo. RED on develop: no attest-meta subcommand, validate only exact-HEAD.

Usage: python3 ...test-evidence-equivalence.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

OK = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global OK, FAIL
    if cond:
        OK += 1
        print(f"ok   {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def run_helper(helper: Path, *args: str) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(helper), *map(str, args)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout.strip() or r.stderr.strip()


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def make_repo(tmp: Path, helper: Path, name: str = "repo",
              fingerprint: str = "") -> tuple[Path, Path]:
    repo = tmp / name; repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "t@b.c")
    git(repo, "config", "user.name", "repro")
    (repo / "test-evidence.py").write_bytes(helper.read_bytes())
    (repo / "evidence.log").write_text("test ok\n")
    (repo / "gate.env").write_text("")
    (repo / "docs").mkdir(); (repo / "docs" / "issue.md").write_text("phase: proposed\n")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "init")
    head = git(repo, "rev-parse", "HEAD")
    args = ["--gate", repo / "gate.env", "--status", "completed", "--command", "true",
            "--exit-code", "0", "--evidence", repo / "evidence.log", "--head", head]
    rc, _ = run_helper(repo / "test-evidence.py", "write", *args,
                       *(["--test-definition-fingerprint", fingerprint] if fingerprint else []))
    if rc != 0 and fingerprint:
        # RED baseline: helper predates fingerprint support. Fall back so the
        # later fingerprint assertions fail on their own merit, not on setup.
        rc, _ = run_helper(repo / "test-evidence.py", "write", *args)
    assert rc == 0, "baseline write failed"
    return repo, Path(head)


def main() -> int:
    global OK, FAIL
    ap = argparse.ArgumentParser(); ap.add_argument("--source-dir", default="")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else Path(__file__).resolve().parents[5]
    helper = src / "docs/system/workspace/scripts/quality/test-evidence.py"
    text = helper.read_text(encoding="utf-8")
    check("helper readable", bool(text))

    # Structural
    check("attest-meta subcommand present", "attest-meta" in text)
    check("validate emits three-state verdict", "equivalent" in text and "verdict" in text)
    check("hard-excluded paths present", "pre-tests.md" in text and "projection.lock" in text)
    check("fingerprint is persisted, not compared in memory",
          "TEST_DEFINITION_FINGERPRINT" in text and '"TEST_DEFINITION_FINGERPRINT"' in text)

    with tempfile.TemporaryDirectory(prefix="freely-equiv-") as td:
        tmp = Path(td)
        repo, tested = make_repo(tmp, helper)
        h = repo / "test-evidence.py"

        # baseline: exact HEAD validates
        rc, out = run_helper(h, "validate", "--gate", repo / "gate.env", "--worktree", repo, "--json")
        check("baseline exact HEAD validates", rc == 0 and json.loads(out).get("ok") is True, out[:100])

        # metadata-only commit
        (repo / "docs" / "issue.md").write_text("phase: absorbed\n")
        git(repo, "add", "-A"); git(repo, "commit", "-qm", "metadata only")

        rc, out = run_helper(h, "validate", "--gate", repo / "gate.env", "--worktree", repo, "--json")
        check("metadata commit goes stale without attestation", rc != 0 and json.loads(out).get("ok") is False, out[:100])

        # attest with non-sensitive path
        rc, out = run_helper(h, "attest-meta", "--gate", repo / "gate.env", "--worktree", repo,
                             "--sensitive-paths", "src/**,tests/**")
        check("attest-meta succeeds for non-sensitive diff", rc == 0, out[:120])

        rc, out = run_helper(h, "validate", "--gate", repo / "gate.env", "--worktree", repo, "--json")
        verdict = json.loads(out) if out.startswith("{") else {}
        check("validated as equivalent", rc == 0 and verdict.get("verdict") == "equivalent", out[:120])

        # sensitive path must be rejected
        (repo / "src").mkdir(); (repo / "src" / "app.py").write_text("x=1\n")
        git(repo, "add", "-A"); git(repo, "commit", "-qm", "code change")
        rc, out = run_helper(h, "attest-meta", "--gate", repo / "gate.env", "--worktree", repo,
                             "--sensitive-paths", "src/**,tests/**")
        check("attest-meta rejects sensitive diff with reason",
              rc != 0 and ("sensitive" in out.lower() or "re-run" in out.lower()), out[:160])

        # Test-definition fingerprint: changed definition must invalidate,
        # and a missing stored fingerprint must never be silently accepted.
        fp_repo, _ = make_repo(tmp, helper, name="fp-repo", fingerprint="fp-v1")
        fph = fp_repo / "test-evidence.py"
        (fp_repo / "docs" / "issue.md").write_text("phase: absorbed\n")
        git(fp_repo, "add", "-A"); git(fp_repo, "commit", "-qm", "metadata only")
        rc, out = run_helper(fph, "attest-meta", "--gate", fp_repo / "gate.env",
                             "--worktree", fp_repo, "--sensitive-paths", "src/**",
                             "--test-definition-fingerprint", "fp-v2")
        check("changed test-definition fingerprint rejected",
              rc != 0 and "fingerprint" in out.lower(), out[:160])
        rc, out = run_helper(fph, "attest-meta", "--gate", fp_repo / "gate.env",
                             "--worktree", fp_repo, "--sensitive-paths", "src/**",
                             "--test-definition-fingerprint", "fp-v1")
        check("matching fingerprint attests", rc == 0, out[:160])
        rc, out = run_helper(fph, "validate", "--gate", fp_repo / "gate.env",
                             "--worktree", fp_repo, "--json")
        verdict = json.loads(out) if out.startswith("{") else {}
        check("fingerprint attestation validates as equivalent",
              rc == 0 and verdict.get("verdict") == "equivalent", out[:120])

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
