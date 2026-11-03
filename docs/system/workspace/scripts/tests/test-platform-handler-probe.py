#!/usr/bin/env python3
"""Unit tests for platform handler probing: cache, retry, structured failure."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PA_PATH = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"

_spec = importlib.util.spec_from_file_location("platform_adapter", PA_PATH)
pa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pa)


class FakeHandler:
    def __init__(self, name, detections):
        self._name = name
        self._detections = list(detections)
        self.calls = 0

    @property
    def name(self):
        return self._name

    def detect(self):
        self.calls += 1
        index = min(self.calls - 1, len(self._detections) - 1)
        return self._detections[index]


class HandlerProbeTests(unittest.TestCase):
    def setUp(self):
        pa._registry.clear()
        pa._HANDLER_PROBE_CACHE.clear()
        pa._READ_BACKOFF = (0, 0)

    def tearDown(self):
        pa._registry.clear()
        pa._HANDLER_PROBE_CACHE.clear()

    def test_successful_probe_is_cached(self):
        handler = FakeHandler("fake", [True])
        pa._registry.append(handler)
        for _ in range(10):
            self.assertIs(pa._handler_for("fake"), handler)
        self.assertEqual(handler.calls, 1)

    def test_probe_retries_transient_failure(self):
        handler = FakeHandler("fake-retry", [False, True])
        pa._registry.append(handler)
        self.assertIs(pa._handler_for("fake-retry"), handler)
        self.assertEqual(handler.calls, 2)

    def test_unavailable_handler_returns_structured_error(self):
        handler, error = pa._ensure_handler("github")
        self.assertIsNone(handler)
        self.assertEqual(error.get("status"), "error")
        self.assertEqual(error.get("stage"), "execute")
        self.assertIn("platform handler unavailable", error.get("error", ""))

    def test_available_handler_passes_guard(self):
        handler = FakeHandler("fake-ok", [True])
        pa._registry.append(handler)
        resolved, error = pa._ensure_handler("fake-ok")
        self.assertIs(resolved, handler)
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()
