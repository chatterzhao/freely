#!/usr/bin/env python3
"""Unit tests for raw replica identity resolution (title-prefix first)."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PA_PATH = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"

_spec = importlib.util.spec_from_file_location("platform_adapter", PA_PATH)
pa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pa)


class RawIdentityTests(unittest.TestCase):
    def test_title_prefix_wins_over_body_reference(self):
        matches = [
            {"issue_number": "4107", "title": "[RAW-20260807T114900Z] scan fix"},
            {"issue_number": "4108", "title": "[RAW-20260807T120649Z] a2a"},
        ]
        match, error = pa._resolve_raw_identity(matches, "20260807T114900Z")
        self.assertEqual(error, "")
        self.assertEqual(match["issue_number"], "4107")

    def test_multiple_title_prefix_matches_remain_ambiguous(self):
        matches = [
            {"issue_number": "1", "title": "[RAW-20260807T114900Z] a"},
            {"issue_number": "2", "title": "[RAW-20260807T114900Z] b"},
        ]
        match, error = pa._resolve_raw_identity(matches, "20260807T114900Z")
        self.assertIsNone(match)
        self.assertIn("ambiguous", error)

    def test_fallback_single_body_match(self):
        matches = [{"issue_number": "9", "title": "legacy issue without prefix"}]
        match, error = pa._resolve_raw_identity(matches, "20260807T114900Z")
        self.assertEqual(error, "")
        self.assertEqual(match["issue_number"], "9")

    def test_no_match(self):
        match, error = pa._resolve_raw_identity([], "20260807T114900Z")
        self.assertIsNone(match)
        self.assertIn("not found", error)


if __name__ == "__main__":
    unittest.main()
