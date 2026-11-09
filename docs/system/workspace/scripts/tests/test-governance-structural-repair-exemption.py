#!/usr/bin/env python3
"""AT-001 — raw-20261109T070744Z / #4236.

GATE 1 treats every issue document touched by the branch as an owner of this
merge and demands its key match the branch key. A branch that repairs 23
historically damaged documents therefore matches none of them, so damaged
documents can never be repaired: a discipline check became a deadlock.

Fix: a document whose pre-merge copy was not parseable had no readable lifecycle
state, so repairing it cannot change anyone's governance state. Such paths are
dropped from the owner set (warning) instead of failing every downstream check.

Runs against two roots:
  RED   : --source-dir /tmp/<develop-baseline>   (no exemption -> FAIL)
  GREEN : --source-dir <this worktree>
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
SRC = Path(os.environ.get("GATE_SOURCE_ROOT", str(PROJECT))).resolve()

GLUED = ("---\nlocal_id: raw-20260101T000000Z\nkind: raw\nphase_state: proposed\n"
         "platform_state: closed---\n\n# t\n")
CONFLICT = ("---\nlocal_id: raw-20260101T000000Z\nkind: raw\n<<<<<<< HEAD\n"
            "phase_state: dropped\n=======\nphase_state: proposed\n>>>>>>> x\n---\n\n# t\n")
BULLET_IN_YAML = ("---\nlocal_id: I-20260101T000000Z-A\nkind: linked\n"
                  "- phase_state: dropped\npromoted_from: raw-20260101T000000Z\n---\n\n# t\n")
GLUED_FIELDS = ("---\nlocal_id: I-20260101T000000Z-A\nkind: linked\n"
                "canonical_issue_path: docs/B2-docs/x/issues/20260101- pre_tests_path: docs/p.md\n"
                "---\n\n# t\n")
VALID = "---\nlocal_id: raw-20260101T000000Z\nkind: raw\nphase_state: proposed\n---\n\n# t\n"
LEGACY_BULLETS = "# I-20260101T000000Z-A: legacy\n\n- issue_id: I-20260101T000000Z-A\n- phase_state: completed\n"

OK = 0
BAD = 0


def ok(label: str) -> None:
    global OK
    OK += 1
    print(f"  [ok] {label}")


def bad(label: str) -> None:
    global BAD
    BAD += 1
    print(f"  [FAIL] {label}")


def expect(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


def load_gate(src: Path):
    from importlib.machinery import SourceFileLoader

    path = src / "docs/system/workspace/scripts/quality/governance-merge-gate"
    sys.path.insert(0, str(src / "docs/system/workspace/scripts/lifecycle"))
    # The gate is an extensionless executable, so it needs an explicit loader.
    loader = SourceFileLoader("gate_probe", str(path))
    spec = importlib.util.spec_from_loader("gate_probe", loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["gate_probe"] = module
    loader.exec_module(module)
    return module


def fixture_checks(gate) -> None:
    print("=== FIXTURE: damage classification ===")
    cases = (
        ("glued closing delimiter", GLUED, True),
        ("unresolved conflict markers", CONFLICT, True),
        ("bullet line inside the YAML block", BULLET_IN_YAML, True),
        ("field glued to the previous value", GLUED_FIELDS, True),
        ("valid YAML frontmatter", VALID, False),
        ("legacy bullet-only document (supported format)", LEGACY_BULLETS, False),
    )
    for label, text, want in cases:
        got = gate.legacy_frontmatter_damaged(text)
        expect(got == want, f"{label} -> damaged={want} (got {got})")


def _run_git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def repo_checks(gate) -> None:
    print("=== REPO: baseline resolution + owner-set selection ===")
    tmp = Path(tempfile.mkdtemp(prefix="gate-repair."))
    damaged_rel = "docs/B1-docs/raw-20260101T000000Z/issue.md"
    clean_rel = "docs/B1-docs/raw-20260102T000000Z/issue.md"
    try:
        _run_git(tmp, "init", "-q")
        _run_git(tmp, "config", "user.email", "t@example.test")
        _run_git(tmp, "config", "user.name", "t")
        for rel, text in ((damaged_rel, GLUED), (clean_rel, VALID)):
            path = tmp / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        _run_git(tmp, "add", "-A")
        _run_git(tmp, "commit", "-qm", "baseline")

        # Working tree: repair the damaged one, leave the clean one untouched.
        (tmp / damaged_rel).write_text(
            GLUED.replace("platform_state: closed---", "platform_state: closed"),
            encoding="utf-8")

        old_root = gate.ROOT_DIR
        gate.ROOT_DIR = str(tmp)
        try:
            staged = argparse.Namespace(staged=True, range=None)
            ranged = argparse.Namespace(staged=False, range="HEAD..HEAD")

            expect("platform_state: closed---" in gate.baseline_text(damaged_rel, staged),
                   "staged mode reads the pre-merge copy from HEAD")
            expect(gate.legacy_frontmatter_damaged(gate.baseline_text(damaged_rel, staged)),
                   "staged mode flags the damaged baseline")
            expect(not gate.legacy_frontmatter_damaged(gate.baseline_text(clean_rel, staged)),
                   "staged mode leaves a clean baseline alone")

            selected = gate.select_repair_only_paths({damaged_rel, clean_rel}, staged)
            expect(selected == {damaged_rel},
                   f"only the damaged path is treated as a structural repair (got {sorted(selected)})")

            expect(gate.legacy_frontmatter_damaged(gate.baseline_text(damaged_rel, ranged)),
                   "range mode resolves the left side of the range")
            expect(gate.select_repair_only_paths({clean_rel}, ranged) == set(),
                   "range mode keeps a clean baseline in the owner set")
        finally:
            gate.ROOT_DIR = old_root
    finally:
        subprocess.run(["rm", "-rf", str(tmp)], check=False)


def reverse_guard_checks(gate) -> None:
    """A parseable baseline with a foreign key must still be rejected."""
    print("=== REVERSE GUARD: parseable foreign key is still an error ===")
    text = VALID.replace("raw-20260101T000000Z", "raw-20990101T000000Z")
    expect(not gate.legacy_frontmatter_damaged(text),
           "parseable baseline of a foreign key is NOT exempted")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=None)
    ap.add_argument("mode", nargs="?", default="all")
    args = ap.parse_args()
    src = Path(args.source_dir).resolve() if args.source_dir else SRC
    try:
        gate = load_gate(src)
        if not hasattr(gate, "select_repair_only_paths"):
            raise AttributeError("select_repair_only_paths (exemption missing)")
    except Exception as exc:
        # Baseline has no exemption at all. Keep every assertion running against
        # a "no capability" stub so RED reports one line per missing behaviour
        # instead of collapsing into a single import error.
        print(f"  [info] gate module unusable ({type(exc).__name__}); "
              f"running against a no-capability stub")

        class _NoCapability:
            ROOT_DIR = ""

            @staticmethod
            def legacy_frontmatter_damaged(text: str) -> bool:
                return False

            @staticmethod
            def baseline_text(rel_path: str, ns) -> str:
                return ""

            @staticmethod
            def select_repair_only_paths(paths, ns):
                return set()

        gate = _NoCapability()
    if args.mode in ("fixture", "all"):
        fixture_checks(gate)
    if args.mode in ("repo", "all"):
        repo_checks(gate)
        reverse_guard_checks(gate)
    print(f"SUMMARY: {OK} ok, {BAD} failed")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main())
