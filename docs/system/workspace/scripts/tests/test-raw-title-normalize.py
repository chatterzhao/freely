#!/usr/bin/env python3
"""AT-001/AT-002 — raw-20261116T050414Z / #4657.

Title normalisation must happen at the *scan* funnel, before any local task is
derived from a platform raw issue, with pr-create-guarded as a fallback for
absorbed/CLOSED replicas that scan never sees.

Contracts pinned here
---------------------
1. `runtime/raw_title_normalize.normalize_open_raw_titles()` derives the
   authoritative raw key from ``title + body`` (never from created_at), fixes
   only non-canonical titles through the adapter, prints ``旧 → 新``, is
   idempotent and honours ``--dry-run``.
2. The scan command wires the preflight; `task-lifecycle-scan.py` and
   `pre-scan-fix.sh` themselves stay read-only.
3. The replica gate emits a structured `non_canonical_title` diagnostic and
   pr-create-guarded has a preflight that re-runs the gate.

Run:
  RED   : python3 test-raw-title-normalize.py           (module absent)
  GREEN : python3 test-raw-title-normalize.py           (after implementation)
Exit 0 iff zero failures; prints "SUMMARY: N ok, M failed".
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
ROOT = Path(os.environ.get("RAW_TITLE_NORMALIZE_SOURCE_ROOT", str(PROJECT))).resolve()
MODULE_PATH = ROOT / "docs/system/workspace/scripts/runtime/raw_title_normalize.py"

FAILURES: list[str] = []
TOTAL: list[int] = [0]


def check(condition: bool, message: str) -> None:
    TOTAL[0] += 1
    if condition:
        print(f"  ok   {message}")
    else:
        print(f"  FAIL {message}")
        FAILURES.append(message)


class FakeAdapter:
    """Minimal platform surface: reads OPEN records and records title writes."""

    def __init__(self, records: dict[str, dict], fail_platform: str = "") -> None:
        self.records = records
        self.writes: list[dict] = []
        self.fail_platform = fail_platform

    def configured_platforms(self) -> list[str]:
        return ["github", "gitee"]

    def list_open_issue_records(self) -> dict[str, dict]:
        return self.records

    def update_issue(self, local_id: str, platform_ids: dict, title: str = "", body: str = "") -> dict:
        self.writes.append({"local_id": local_id, "ids": platform_ids, "title": title, "body": body})
        platform = next(iter(platform_ids), "github")
        if platform == self.fail_platform:
            return {platform: {"status": "error", "error": "injected"}}
        return {platform: {"status": "updated"}}


def _records(noncanonical: bool = True) -> dict[str, dict]:
    title = ("fix: 标题缺前缀" if noncanonical
             else "[RAW-20260101T000000Z] fix: 标题已达标")
    body = "workflow_kind: fix\n\n| local_id | `raw-20260101T000000Z` |\n\n## 现象\n\ntext\n"
    return {
        "4657": {"platform": "github", "title": title, "body": body, "state": "OPEN"},
        "IKVLKU": {"platform": "gitee", "title": title, "body": body, "state": "OPEN"},
    }


def _load_module():
    if not MODULE_PATH.is_file():
        raise ImportError(f"normalisation module missing: {MODULE_PATH}")
    spec = importlib.util.spec_from_file_location("raw_title_normalize", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_api_present():
    print("AT-001 S1: normalisation module exposes the preflight API")
    try:
        module = _load_module()
    except Exception as exc:
        check(False, f"module importable ({type(exc).__name__}: {exc})")
        return None
    check(callable(getattr(module, "normalize_open_raw_titles", None)),
          "normalize_open_raw_titles() exists")
    return module


def test_fixes_title_and_prints_from_to(module):
    if module is None:
        return
    print("AT-001 S2: non-canonical title is fixed and from→to is printed")
    fake = FakeAdapter(_records())
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        result = module.normalize_open_raw_titles(str(PROJECT), dry_run=False, adapter_module=fake)
    check(result.get("ok") is True, "preflight reports ok")
    check(len(fake.writes) == 2, f"both platforms written (got {len(fake.writes)})")
    expected = "[RAW-20260101T000000Z] fix: 标题缺前缀"
    check(all(w["title"] == expected for w in fake.writes), "titles are canonical after write")
    check(all(w["body"] == "" for w in fake.writes), "body is never rewritten")
    text = out.getvalue()
    check("fix: 标题缺前缀" in text and "→" in text and expected in text,
          "stdout carries `旧 → 新` before/after")
    check(all(str(c.get("raw_key", "")) == "20260101T000000Z" for c in result.get("changes", [])),
          "changes record the authoritative raw key (without raw- prefix)")


def test_idempotent_and_dry_run(module):
    if module is None:
        return
    print("AT-001 S3: canonical title is a no-op; dry-run never writes")
    fake_ok = FakeAdapter(_records(noncanonical=False))
    with contextlib.redirect_stdout(io.StringIO()):
        module.normalize_open_raw_titles(str(PROJECT), adapter_module=fake_ok)
    check(fake_ok.writes == [], "already-canonical title causes zero writes")

    fake_dry = FakeAdapter(_records())
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        module.normalize_open_raw_titles(str(PROJECT), dry_run=True, adapter_module=fake_dry)
    check(fake_dry.writes == [], "dry-run causes zero writes")
    check("→" in out.getvalue(), "dry-run still prints from→to")


def test_linked_issue_is_never_normalised(module):
    if module is None:
        return
    print("AT-001 S4b: a linked I-* issue is not a raw title candidate")
    body = (
        "---\nissue_id: I-20260101T000000Z-C\nkind: linked\n"
        "promoted_from: raw-20260101T000000Z\n"
        "source_candidate: docs/B1-docs/raw-20260101T000000Z/candidates.md\n---\n\n"
        "# I-20260101T000000Z-C: 讨论入口\n"
    )
    records = {
        "42": {"platform": "github", "title": "[I-20260101T000000Z-C] 讨论入口",
               "body": body, "state": "OPEN"},
        "IKV9ZK": {"platform": "gitee", "title": "[I-20260101T000000Z-C] 讨论入口",
                   "body": body, "state": "OPEN"},
    }
    fake = FakeAdapter(records)
    with contextlib.redirect_stdout(io.StringIO()):
        result = module.normalize_open_raw_titles(str(PROJECT), adapter_module=fake)
    check(fake.writes == [], "linked issues cause zero platform writes")
    check(result.get("ok") is True, "linked-only scan is ok (skips are not failures)")


def test_partial_failure(module):
    if module is None:
        return
    print("AT-001 S4: partial platform failure is reported, never declared success")
    fake = FakeAdapter(_records(), fail_platform="gitee")
    with contextlib.redirect_stdout(io.StringIO()):
        result = module.normalize_open_raw_titles(str(PROJECT), adapter_module=fake)
    check(result.get("ok") is False, "partial failure returns ok=False")
    check(bool(result.get("errors")), "errors are surfaced")


def test_readonly_boundaries():
    print("AT-001 S5: scan analyser and pre-scan helper stay read-only")
    scan = (ROOT / "docs/system/workspace/scripts/runtime/task-lifecycle-scan.py").read_text(encoding="utf-8")
    prescan = (ROOT / "docs/system/workspace/scripts/runtime/pre-scan-fix.sh").read_text(encoding="utf-8")
    for name, text in (("task-lifecycle-scan.py", scan), ("pre-scan-fix.sh", prescan)):
        forbidden = [token for token in ("update_issue(", "create_issue(", "close_issue(") if token in text]
        check(not forbidden, f"{name} has no platform-write calls (found {forbidden})")


def test_gate_diagnostic():
    print("AT-002 S1: gate emits structured non_canonical_title diagnostic")
    gate = ROOT / "docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py"
    recon = ROOT / "docs/system/workspace/scripts/lifecycle/raw_reconciliation.py"
    check("non_canonical_title" in recon.read_text(encoding="utf-8"),
          "reconcile() knows the non_canonical_title code")
    check("suggested_command" in gate.read_text(encoding="utf-8")
          or "suggested_command" in recon.read_text(encoding="utf-8"),
          "diagnostic carries suggested_command")


def test_scan_and_prcreate_wiring():
    print("AT-002 S2: scan command and pr-create preflight call the normaliser")
    runtime = (ROOT / "docs/system/workspace/scripts/runtime/freely").read_text(encoding="utf-8")
    prcreate = (ROOT / "docs/system/workspace/scripts/worktree/pr-create-guarded").read_text(encoding="utf-8")
    check("raw_title_normalize" in runtime, "cmd_task_source_scan wires the preflight")
    check("raw_title_normalize" in prcreate or "normalize-open-raw-titles" in prcreate,
          "pr-create-guarded has a preflight")


def main() -> int:
    print(f"source: {ROOT}")
    module = test_api_present()
    test_fixes_title_and_prints_from_to(module)
    test_idempotent_and_dry_run(module)
    test_partial_failure(module)
    test_linked_issue_is_never_normalised(module)
    test_readonly_boundaries()
    test_gate_diagnostic()
    test_scan_and_prcreate_wiring()
    failed = len(FAILURES)
    ok = TOTAL[0] - failed
    print(f"SUMMARY: {ok} ok, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
