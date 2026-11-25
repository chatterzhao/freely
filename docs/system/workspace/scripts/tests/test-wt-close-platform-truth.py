#!/usr/bin/env python3
"""AT-001 for raw-20261125T071429Z / I-20261125T071429Z-A.

The gate that deletes a worktree must judge "is this I-* closed" from PLATFORM
truth, not from the local `platform_state` cache. This AT checks both halves:

  behavioural  — the pure filter that decides which OPEN replicas belong to a
                 local id (must ignore CLOSED records, other I-* ids, and raw
                 titles; must never turn a read failure into "no replicas").
  structural   — wt-close / issue-sync / pr-merge-guarded actually wire that
                 truth in, and no longer swallow close failures with `|| true`.

RED on develop: the module and every structural expectation are absent.
GREEN after the fix.

Usage:
  python3 docs/system/workspace/scripts/tests/test-wt-close-platform-truth.py [--source-dir DIR]
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
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


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("replica_truth_under_test", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001 - reported as a failed check
        print(f"FAIL import {path} — {exc}")
        return None
    return module


def read(root: Path, rel: str) -> str:
    try:
        return (root / rel).read_text(encoding="utf-8")
    except OSError:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", default=str(Path(__file__).resolve().parents[5]))
    args = parser.parse_args()
    root = Path(args.source_dir).resolve()

    # ── behavioural: pure replica filter ────────────────────────────────
    module_path = root / "docs/system/workspace/scripts/lifecycle/replica_truth.py"
    check("replica_truth module exists", module_path.is_file(), str(module_path))
    module = load_module(module_path) if module_path.is_file() else None
    check("replica_truth exposes filter_open_replicas",
          module is not None and hasattr(module, "filter_open_replicas"))

    if module is not None and hasattr(module, "filter_open_replicas"):
        records = {
            "github:1": {"issue_id": "1", "title": "[I-20260101T000000Z-A] I-20260101T000000Z-A: mine"},
            "github:2": {"issue_id": "2", "title": "[I-20260101T000000Z-A] duplicate", "state": "OPEN"},
            "github:3": {"issue_id": "3", "title": "[I-20260101T000000Z-B] sibling", "state": "OPEN"},
            "gitee:IK1": {"issue_id": "IK1", "title": "[RAW-20260101T000000Z] unrelated raw", "state": "open"},
            "gitee:IK2": {"issue_id": "IK2", "title": "[I-20260101T000000Z-A] gitee replica", "state": "closed"},
        }
        found = module.filter_open_replicas(records, "I-20260101T000000Z-A")
        flat = {f"{p}:{item['issue_id']}" for p, items in found.items() for item in items}
        check("includes OPEN replica for the local id", "github:1" in flat and "github:2" in flat, str(flat))
        check("excludes sibling I-* ids", "github:3" not in flat, str(flat))
        check("excludes raw titles", "gitee:IK1" not in flat, str(flat))
        check("excludes CLOSED replicas", "gitee:IK2" not in flat, str(flat))
        check("empty when local id absent",
              module.filter_open_replicas(records, "I-20990101T000000Z-Z") == {})

        degraded = dict(records)
        degraded["__degraded__"] = {"platform": "github", "error": "read failed"}
        summary = module.summarize(degraded, "I-20260101T000000Z-A")
        check("read failure is not reported as clean", summary.get("ok") is False, str(summary))

    # ── structural: the gate must consult platform truth ────────────────
    wt = read(root, "docs/system/workspace/scripts/worktree/wt-close")
    check("wt-close consults verify-local-id", "verify-local-id" in wt)
    check("wt-close refuses when a replica is still open",
          "_wt_platform_open" in wt and "平台仍有 OPEN 副本" in wt)
    check("wt-close requires --reason for --skip-platform",
          "--skip-platform" in wt and "SKIP_PLATFORM" in wt and "requires --reason" in wt or
          "skip-platform requires --reason" in wt)

    batch = read(root, "bin/issue-sync.d/cmd-batch.sh")
    check("batch does not swallow linked close failures",
          'cmd_close_linked "$local_id" || true' not in batch)
    check("batch reconciles through close-local-id", "close-local-id" in batch or "close-linked-all" in batch)
    check("batch verifies platform presence before create",
          "_platform_has_open_replica" in batch)

    merge = read(root, "docs/system/workspace/scripts/worktree/pr-merge-guarded")
    check("pr-merge does not swallow batch failures",
          'batch "$_raw_key" || true' not in merge)
    check("pr-merge aborts when batch fails",
          "issue-sync batch $_raw_key failed" in merge or "_sync_rc" in merge)

    effects = read(root, "docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py")
    check("close_linked reconciles by local id", "close-local-id" in effects)

    state = read(root, "bin/issue-sync.d/lib-state.sh")
    check("_already_on_platform consults the platform",
          "verify-local-id" in state or "_platform_has_local_id" in state)

    print(f"SUMMARY: {OK} ok, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
