#!/usr/bin/env python3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
WT_CREATE = ROOT / "docs/system/workspace/scripts/worktree/wt-create"


class WorktreeLifecycleBoundaryTests(unittest.TestCase):
    def test_worktree_creation_does_not_mark_raw_absorbed(self):
        source = WT_CREATE.read_text(encoding="utf-8")
        self.assertNotIn("_mark_raw_issue_absorbed", source)
        self.assertNotIn("fm['phase_state'] = 'absorbed'", source)


if __name__ == "__main__":
    unittest.main()
