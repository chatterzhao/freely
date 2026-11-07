#!/usr/bin/env python3
"""AT-001 — raw-20261105T122053Z / #4195

A platform READ FAILURE must never be flattened into an empty open-issue list.
An empty dict is indistinguishable from "this platform has no open issues",
which made 57 GitHub issues vanish from the lifecycle scan.

Contract:
  - healthy: list_open_issue_records() returns the plain merged dict (57+50),
    no extra keys, no caller changes (PRE-EXISTING capability, must stay green)
  - read failure: each handler records ok/error/partial; the module-level
    aggregator emits a "__degraded__" marker that the existing scan consumer
    (task-lifecycle-scan.py:773) already understands
  - REST fallback is preserved
  - parity check skips (with a retry hint) instead of reporting fake divergence
"""
import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[5]
ADAPTER = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"
SCAN = ROOT / "docs/system/workspace/scripts/runtime/task-lifecycle-scan.py"
PARITY = ROOT / "docs/system/workspace/scripts/tests/test-platform-open-parity.py"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _record(platform, number):
    return {"platform": platform,
            "title": f"[RAW-20261105T122053Z] fixture {platform} #{number}",
            "body": "fixture", "state": "OPEN"}


class _FakeHandler:
    """Minimal stand-in exposing the read contract under test."""
    def __init__(self, name, records=None, raise_exc=False, health=None):
        self.name = name
        self.records = records or {}
        self.raise_exc = raise_exc
        self.read_health = health or {"ok": True, "error": "", "partial": False}

    def list_open_issue_records(self):
        if self.raise_exc:
            raise RuntimeError("502 Bad Gateway")
        return dict(self.records)


class AggregatorTests(unittest.TestCase):
    def setUp(self):
        self.pa = _load("pa_r7_under_test", ADAPTER)

    def _run(self, handlers):
        with mock.patch.object(self.pa, "_handlers", return_value=handlers):
            try:
                return self.pa.list_open_issue_records()
            except TypeError as error:
                # Before the fix, _safe() returns {'status': 'error', ...} and
                # the aggregator does **record on a string -> TypeError. That
                # is the same silent-failure defect, just one step later.
                self.fail(f"aggregator treated an error object as issue records: {error}")

    def test_healthy_merge_unchanged_preexisting(self):
        """PRE-EXISTING: both platforms healthy -> plain 107-record dict."""
        gh = _FakeHandler("github", {str(n): _record("github", n) for n in range(1, 58)})
        gt = _FakeHandler("gitee", {f"I{n}": _record("gitee", n) for n in range(1, 51)})
        result = self._run([gh, gt])
        self.assertEqual(len(result), 107, result.keys())
        self.assertNotIn("__degraded__", result)
        self.assertIn("github:1", result)
        self.assertEqual(result["gitee:I1"]["issue_id"], "I1")
        self.assertEqual(set(result["github:1"]), {"issue_id", "platform", "title", "body", "state"})

    def test_single_platform_failure_emits_degraded_marker(self):
        """RED: one platform unreadable -> result must carry a failure marker."""
        gh = _FakeHandler("github", health={"ok": False, "error": "GraphQL 502 / REST 502",
                                            "partial": True})
        gt = _FakeHandler("gitee", {f"I{n}": _record("gitee", n) for n in range(1, 51)})
        result = self._run([gh, gt])
        self.assertTrue("__degraded__" in result, "read failure was silently flattened to a plain list")
        marker = result["__degraded__"]
        self.assertIn("github", str(marker))
        self.assertIn("502", str(marker))
        self.assertEqual(len([k for k in result if k != "__degraded__"]), 50)

    def test_exception_from_handler_is_degraded_not_fake_records(self):
        """RED: _safe() used to return {'status':'error'} which the aggregator
        then iterated as issue ids, fabricating records."""
        gh = _FakeHandler("github", raise_exc=True)
        gt = _FakeHandler("gitee", {"I1": _record("gitee", 1)})
        result = self._run([gh, gt])
        self.assertIn("__degraded__", result)
        self.assertNotIn("github:status", result)
        self.assertNotIn("github:error", result)
        self.assertIn("gitee:I1", result)

    def test_all_platforms_failed_still_marks_degraded(self):
        """RED: total read failure must be explicit, never a clean empty dict."""
        handlers = [
            _FakeHandler("github", health={"ok": False, "error": "502", "partial": True}),
            _FakeHandler("gitee", health={"ok": False, "error": "timeout", "partial": True}),
        ]
        result = self._run(handlers)
        self.assertTrue("__degraded__" in result, "total read failure returned a clean empty dict")
        self.assertNotEqual(result, {})

    def test_handlers_expose_read_health(self):
        """RED: each configured handler must report ok/error/partial."""
        src = ADAPTER.read_text(encoding="utf-8")
        self.assertTrue("read_health" in src, "handlers have no read-health state")


class ScanTests(unittest.TestCase):
    def test_scan_get_platform_open_issues_produces_degraded(self):
        """RED: scan must see __degraded__ when a platform read failed."""
        self.scan = _load("scan_r7_under_test", SCAN)
        fake_pa = mock.Mock()
        fake_pa.list_open_issue_records.return_value = {
            "gitee:I1": {"issue_id": "I1", "platform": "gitee", "title": "x", "body": "", "state": "OPEN"},
            "__degraded__": {"platform": "github", "error": "502", "ok": False, "partial": True},
        }
        with mock.patch.object(self.scan, "_get_pa", return_value=fake_pa):
            result = self.scan.get_platform_open_issues(ROOT)
        self.assertIn("__degraded__", result)

    def test_scan_degraded_consumer_still_exists_preexisting(self):
        """PRE-EXISTING: scan already pops the marker into platform_health."""
        src = SCAN.read_text(encoding="utf-8")
        self.assertIn('if "__degraded__" in platform_issues', src)
        self.assertIn('platform_health = "degraded"', src)


class ParityTests(unittest.TestCase):
    def test_parity_skips_with_retry_hint_on_degraded(self):
        """RED: parity must not report fake gitee-only divergence on read failure."""
        self.parity = _load("parity_r7_under_test", PARITY)
        gh = _FakeHandler("github", health={"ok": False, "error": "502", "partial": True})
        gt = _FakeHandler("gitee", {"I1": _record("gitee", 1)})
        with mock.patch.object(self.parity.pa, "_handlers", return_value=[gh, gt]):
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                rc = self.parity.main()
        text = out.getvalue() + err.getvalue()
        self.assertEqual(rc, 0, text)
        self.assertNotIn("gitee-only", text)
        self.assertIn("retry", text.lower(), text)

    def test_parity_healthy_still_compares_preexisting(self):
        """PRE-EXISTING: healthy parity check still works."""
        self.parity = _load("parity_r7_healthy", PARITY)
        src = PARITY.read_text(encoding="utf-8")
        self.assertIn("collect_open_issues", src)


if __name__ == "__main__":
    unittest.main(verbosity=2)
