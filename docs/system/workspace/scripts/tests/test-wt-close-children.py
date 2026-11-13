#!/usr/bin/env python3
"""AT-001 (raw-20261113T115957Z): wt-close must retire ALL promoted children.

A raw is 1:N (promoted_children) but owns exactly one worktree. Deleting the
worktree therefore requires every child to be terminal, and every completed
child must have its platform replica closed. The previous implementation:
  * looked for children under docs/B1-docs/<I-id>/issue.md (they live in
    docs/B2-docs/**/issues/), so the block was dead code;
  * only read absorbed_into (one child) instead of promoted_children (a list);
  * never checked that children were terminal before deleting the worktree.

This AT extracts the REAL Phase 2.5 block plus the REAL _fm_get /
_close_platform_ids_readonly helpers from the source under test, runs them
against a sandbox project whose adapter records every call, and asserts the
closeout behaviour. Baseline (develop) must fail all three ways.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[5]
if "--source-dir" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--source-dir") + 1]).resolve()
BASE = Path(sys.argv[sys.argv.index("--baseline") + 1]) if "--baseline" in sys.argv else None

WT_CLOSE = "docs/system/workspace/scripts/worktree/wt-close"
KEY = "20261113T115957Z"
CHILD_A = f"I-{KEY}-A"
CHILD_B = f"I-{KEY}-B"

OK = 0
BAD = 0


def ok(label: str) -> None:
    global OK
    OK += 1
    print("  [ok] " + label)


def bad(label: str) -> None:
    global BAD
    BAD += 1
    print("  [FAIL] " + label)


def check(cond: bool, label: str) -> None:
    (ok if cond else bad)(label)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def fn(text: str, name: str) -> str:
    start = text.find(name + "() {")
    if start < 0:
        return ""
    end = text.find("\n}\n", start)
    return text[start:end + 3] if end > start else ""


def phase25(text: str) -> str:
    start = text.find("# ── Phase 2.5")
    if start < 0:
        return ""
    end = text.find("# ── Phase 3", start)
    return text[start:end] if end > start else ""


def raw_doc(children: list[str]) -> str:
    body = "\n".join("  - " + c for c in children)
    return f"""---
schema_version: '1'
local_id: raw-{KEY}
kind: raw
phase_state: absorbed
absorbed_into: {CHILD_A}
platform_ids:
  github:
    issue_id: '9000'
platform_state: closed
promoted_children:
{body}
---

# raw fixture
"""


def child_doc(cid: str, phase: str, platform_state: str) -> str:
    ps_line = f"platform_state: {platform_state}\n" if platform_state else ""
    return f"""---
schema_version: '1'
issue_id: {cid}
kind: linked
status: completed
phase_state: {phase}
promoted_from: raw-{KEY}
platform_ids:
  github:
    issue_id: '9001'
  gitee:
    issue_id: 'IKTEST1'
{ps_line}pre_tests_path: docs/B2-docs/x/y/raw-{KEY}/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/x/y/raw-{KEY}/code-reviews
---

# {cid} fixture
"""


ADAPTER = (
    "import sys, json, os\n"
    "with open(os.environ['ADAPTER_LOG'], 'a') as f: f.write(sys.argv[1] + '\\n')\n"
    "print(json.dumps({'github': {'status': 'closed'}, 'gitee': {'status': 'closed'}}))\n"
    "sys.exit(0)\n"
)


def run(source: Path, child_a_phase="completed", child_b_phase="completed",
        child_a_state="open", child_b_state="open", dry=False, skip=False) -> tuple:
    text = read(source / WT_CLOSE)
    fmg, closeh, block = fn(text, "_fm_get"), fn(text, "_close_platform_ids_readonly"), phase25(text)
    if not fmg or not closeh or not block:
        return subprocess.CompletedProcess([], 99, "", "helpers/block not found"), 0
    with tempfile.TemporaryDirectory(prefix="at-children-") as td:
        root = Path(td)
        raw_dir = root / "docs/B1-docs" / f"raw-{KEY}"
        raw_dir.mkdir(parents=True)
        (raw_dir / "issue.md").write_text(raw_doc([CHILD_A, CHILD_B]), encoding="utf-8")
        for cid, phase, state in ((CHILD_A, child_a_phase, child_a_state),
                                  (CHILD_B, child_b_phase, child_b_state)):
            d = root / "docs/B2-docs/epic/story" / f"raw-{KEY}" / "issues"
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{cid}.md").write_text(child_doc(cid, phase, state), encoding="utf-8")
        sync_dir = root / "docs/system/workspace/scripts/sync"
        sync_dir.mkdir(parents=True)
        (sync_dir / "platform-adapter.py").write_text(ADAPTER, encoding="utf-8")
        log = root / "adapter.log"
        probe = root / "probe.sh"
        probe.write_text(
            "set -uo pipefail\n"
            + fmg + "\n" + closeh + "\n"
            + "_dry() { printf '[DRY-RUN] %s\\n' \"$*\"; }\n"
            + f"PROJECT_ROOT='{root}'\n"
            + f"issue_file='{raw_dir / 'issue.md'}'\n"
            + f"wt_path='{root / 'fake-wt'}'\n"
            + "FORCE=false\n"
            + f"DRY_RUN={'true' if dry else 'false'}\n"
            + f"SKIP_PLATFORM={'true' if skip else 'false'}\n"
            + block,
            encoding="utf-8",
        )
        env = dict(os.environ, ADAPTER_LOG=str(log))
        proc = subprocess.run(["bash", str(probe)], capture_output=True, text=True,
                              timeout=120, env=env, cwd=str(root))
        calls = len([x for x in read(log).splitlines() if x.strip()])
        return proc, calls


def static_checks() -> None:
    print("=== STATIC: the block uses promoted_children and B2 paths ===")
    text = read(SRC / WT_CLOSE)
    block = phase25(text)
    check(bool(block), "S1 Phase 2.5 block exists")
    check("promoted_children" in block, "S2 block reads promoted_children")
    check("absorbed_into" in block, "S3 block keeps absorbed_into as a fallback")
    check("docs/B2-docs" in block, "S4 block resolves children under docs/B2-docs")
    check("wt_path/docs/B1-docs" not in block and "PROJECT_ROOT/docs/B1-docs" not in block,
          "S5 block no longer builds the old docs/B1-docs path")
    check("phase_state=" in block and "completed|dropped" in block,
          "S6 block gates deletion on terminal phase_state")
    check("_close_platform_ids_readonly" in block, "S7 block reuses the single close helper")
    check("_dry " in block, "S8 dry-run path present")


def behaviour_checks() -> None:
    print("=== BEHAVIOUR: real block against a sandbox project ===")
    p, calls = run(SRC)
    check(p.returncode == 0 and calls == 2,
          f"B1 both completed children are closed (rc={p.returncode}, calls={calls})")
    check(CHILD_A in p.stdout and CHILD_B in p.stdout,
          "B2 both child ids appear in the closeout output")

    p, calls = run(SRC, child_b_phase="in_dev")
    check(p.returncode != 0 and "尚未完成" in (p.stdout + p.stderr) and calls == 0,
          "B3 an unfinished child blocks the closeout with zero platform writes")
    check(CHILD_B in p.stdout + p.stderr, "B4 the blocking child is named")

    p, calls = run(SRC, dry=True)
    check(p.returncode == 0 and calls == 0 and "[DRY-RUN]" in p.stdout,
          "B5 dry-run plans the closes without calling the adapter")

    p, calls = run(SRC, skip=True)
    check(p.returncode == 0 and calls == 0,
          "B6 --skip-platform keeps the children open")

    p, calls = run(SRC, child_a_state="closed", child_b_state="closed")
    check(p.returncode == 0 and calls == 0,
          "B7 already-closed children are not re-closed")

    # Empty platform_state is the REAL shape left by promote-finalize. An empty
    # TSV column makes bash IFS collapse tabs and shifts the path away.
    p, calls = run(SRC, child_a_state="", child_b_state="")
    check(p.returncode == 0 and calls == 2,
          "B8 empty platform_state still closes both children (no TSV collapse)")


def baseline_checks() -> None:
    if BASE is None:
        return
    print("=== BASELINE CONTROL: develop block ===")
    base_text = read(BASE / WT_CLOSE)
    check("# ── Phase 2.5" in base_text,
          "R1 develop already carries R33.15's children-closeout phase")
    check('or "-"' not in base_text,
          "R2 develop still emits empty TSV columns (no placeholder yet)")
    p, calls = run(BASE, child_a_state="", child_b_state="")
    check(p.returncode != 0 or calls != 2,
          "R3 develop really fails on missing platform_state (RED is real)")


def main() -> None:
    print("AT-001 source: " + str(SRC))
    static_checks()
    behaviour_checks()
    baseline_checks()
    print("SUMMARY: " + str(OK) + " ok, " + str(BAD) + " failed")
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
