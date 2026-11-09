#!/usr/bin/env python3
"""AT-001 for raw-20261103T132548Z — test evidence must be machine-verifiable.

A hand-written three-line test-gate.env used to make the real retirement gate
return 0. This suite drives the REAL gate in an isolated git fixture, plus the
single-source evidence helper, the aggregate runner and the CI files. Nothing
here touches the real ~/.freely or .freely/run of the project.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

OK = 0
BAD = 0
PROJECT = Path(__file__).resolve().parents[5]


def ok(label):
    global OK
    OK += 1
    print(f"  [ok] {label}")


def bad(label):
    global BAD
    BAD += 1
    print(f"  [FAIL] {label}")


def expect(cond, label):
    (ok if cond else bad)(label)


def helper(project: Path) -> Path:
    return project / "docs/system/workspace/scripts/quality/test-evidence.py"


def make_fixture(root: Path):
    (root / "bin").mkdir(parents=True)
    stub = root / "bin/pretests-gate"
    stub.write_text("#!/bin/sh\nexit 0\n")
    stub.chmod(0o755)
    (root / ".freely/run").mkdir(parents=True)
    (root / "README").write_text("fixture\n")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "README"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "init"], check=True)
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()


def static_checks(project: Path):
    print("=== STATIC: evidence chain wiring ===")
    q = project / "docs/system/workspace/scripts/quality"
    gate = q / "pretests-retirement-gate"
    runtime = project / "docs/system/workspace/scripts/runtime/freely"
    # Guards: these already exist on develop.
    expect(gate.is_file(), "pretests-retirement-gate exists (pre-existing)")
    expect(runtime.is_file() and "_test_gate_write()" in runtime.read_text(),
           "test-gate writer exists (pre-existing)")
    expect((project / ".gitee-ci.yml").is_file(), ".gitee-ci.yml exists (pre-existing)")
    expect((project / ".github/workflows/pr-merge-guard.yml").is_file(),
           "GitHub workflow exists (pre-existing)")

    expect(helper(project).is_file(), "test-evidence single-source helper exists")
    gate_text = gate.read_text()
    expect("test-evidence.py" in gate_text and "pretests_evidence_invalid" in gate_text,
           "retirement gate validates machine evidence and fails closed")
    runtime_text = runtime.read_text()
    expect("cmd_test_gate_run()" in runtime_text and "run) cmd_test_gate_run" in runtime_text,
           "freely test-gate run is wired into the dispatcher")
    expect("cmd_evidence_add()" in runtime_text,
           "freely evidence add is wired")
    expect((project / "bin/test-all").is_file(), "aggregate runner bin/test-all exists")
    gitee = (project / ".gitee-ci.yml").read_text()
    expect('echo "CI OK"' not in gitee, "Gitee CI no longer prints CI OK")
    expect("fix/*" in gitee and "bin/test-all" in gitee,
           "Gitee CI covers fix/* and runs the real test suite")
    workflow = (project / ".github/workflows/pr-merge-guard.yml").read_text()
    expect("run:" in workflow and "bin/test-all" in workflow,
           "GitHub workflow has a real run: step")


def behavior_checks(project: Path):
    print("=== BEHAVIOR: real gate + evidence helper ===")
    hp = helper(project)
    gate_script = project / "docs/system/workspace/scripts/quality/pretests-retirement-gate"
    tmp = Path(tempfile.mkdtemp(prefix="evidence-chain-"))
    try:
        fixture = tmp / "fixture"
        head = make_fixture(fixture)
        gate_env = fixture / ".freely/run/test-gate.env"
        evidence_file = fixture / ".freely/run/test-evidence.log"
        evidence_file.write_text("test output\n")

        # 1) hand-written three-line env must be REJECTED by the real gate
        gate_env.write_text(
            'TEST_STATUS="completed"\n'
            'LAST_TESTED_AT="2026-11-09T00:00:00Z"\n'
            f'LAST_TESTED_COMMIT="{head}"\n'
        )
        result = subprocess.run(
            ["bash", str(gate_script), "--project", str(fixture),
             "--worktree-path", str(fixture)],
            capture_output=True, text=True,
        )
        combined = result.stdout + result.stderr
        expect(result.returncode != 0 and "pretests_evidence_invalid" in combined,
               f"hand-written 3-line test-gate.env is rejected by the real gate (rc={result.returncode})")

        if not hp.is_file():
            for label in (
                "failed test run is refused (exit_code=1)", "successful real run is accepted",
                "tampered evidence is rejected (sha256 mismatch)", "stale HEAD evidence is rejected",
                "real gate accepts runner-produced evidence",
                "bin/test-all --ci passes with an explicit known-broken list",
                "evidence add records the file sha256 in a manifest",
            ):
                bad(f"{label} (helper missing)")
            return

        def run_helper(*args):
            return subprocess.run([sys.executable, str(hp), *map(str, args)],
                                  capture_output=True, text=True)

        # 2) failed run
        run_helper("write", "--gate", gate_env, "--status", "failed",
                   "--command", "false", "--exit-code", "1",
                   "--evidence", evidence_file, "--head", head)
        verdict = run_helper("validate", "--gate", gate_env,
                             "--worktree", fixture, "--json")
        expect(verdict.returncode != 0, "failed test run (exit_code=1) is refused")

        # 3) successful run
        run_helper("write", "--gate", gate_env, "--status", "completed",
                   "--command", "true", "--exit-code", "0",
                   "--evidence", evidence_file, "--head", head)
        verdict = run_helper("validate", "--gate", gate_env,
                             "--worktree", fixture, "--json")
        expect(verdict.returncode == 0,
               f"successful real run is accepted ({verdict.stdout.strip()[:120]})")

        # 4) tampered evidence
        evidence_file.write_text("test output TAMPERED\n")
        verdict = run_helper("validate", "--gate", gate_env,
                             "--worktree", fixture, "--json")
        expect(verdict.returncode != 0 and "hash" in verdict.stdout.lower(),
               "tampered evidence is rejected (sha256 mismatch)")

        # 5) stale HEAD
        evidence_file.write_text("test output\n")
        run_helper("write", "--gate", gate_env, "--status", "completed",
                   "--command", "true", "--exit-code", "0",
                   "--evidence", evidence_file, "--head", "deadbeef")
        verdict = run_helper("validate", "--gate", gate_env,
                             "--worktree", fixture, "--json")
        expect(verdict.returncode != 0, "stale HEAD evidence is rejected")

        # 6) the real retirement gate accepts a runner-produced verdict
        run_helper("write", "--gate", gate_env, "--status", "completed",
                   "--command", "true", "--exit-code", "0",
                   "--evidence", evidence_file, "--head", head)
        result = subprocess.run(
            ["bash", str(gate_script), "--project", str(fixture),
             "--worktree-path", str(fixture)],
            capture_output=True, text=True,
        )
        expect(result.returncode == 0,
               f"real gate accepts runner-produced evidence (rc={result.returncode}, {(result.stdout+result.stderr)[:160]})")

        # 7) aggregate runner
        runner = project / "bin/test-all"
        if runner.is_file():
            agg = subprocess.run(["bash", str(runner), "--ci"],
                                 capture_output=True, text=True, cwd=str(project))
            expect(agg.returncode == 0 and "known-broken" in (agg.stdout + agg.stderr).lower(),
                   f"bin/test-all --ci passes with an explicit known-broken list (rc={agg.returncode})")
        else:
            bad("bin/test-all --ci passes with an explicit known-broken list (runner missing)")

        # 8) evidence add records a hash (isolated git repo)
        manifest_cmd = run_helper("manifest-add", "--project", fixture,
                                  "--file", evidence_file)
        manifest = fixture / ".freely/run/evidence-manifest.json"
        payload = json.loads(manifest.read_text()) if manifest.is_file() else {}
        expect(manifest_cmd.returncode == 0 and payload.get("files"),
               "evidence add records the file sha256 in a manifest")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=None)
    ap.add_argument("mode", nargs="?", default="all")
    args = ap.parse_args()
    project = Path(args.source_dir).resolve() if args.source_dir else PROJECT
    if args.mode in ("static", "all"):
        static_checks(project)
    if args.mode in ("behavior", "all"):
        behavior_checks(project)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
