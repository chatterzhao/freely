#!/usr/bin/env python3
"""Unit test: merge-guard issue sync must be scoped to the lane's own raw key."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HELPER = ROOT / "docs/system/workspace/scripts/worktree/issue-sync-scope.py"


def load_helper():
    spec = importlib.util.spec_from_file_location("issue_sync_scope", HELPER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class IssueSyncScopeTests(unittest.TestCase):
    def test_raw_key_filters_out_other_raw_docs(self):
        mod = load_helper()
        changed = [
            "raw-20261103T121047Z",
            "I-20261103T121047Z-A",
            "raw-20260714T012901Z",
            "raw-20261103T083757Z",
            "I-20260719T200726Z-A",
        ]
        kept = mod.filter_issue_ids(changed, "20261103T121047Z")
        self.assertEqual(kept, ["raw-20261103T121047Z", "I-20261103T121047Z-A"])

    def test_no_raw_key_preserves_legacy_behaviour(self):
        mod = load_helper()
        changed = ["raw-20261103T121047Z", "raw-20260714T012901Z"]
        self.assertEqual(mod.filter_issue_ids(changed, ""), changed)

    def test_cli_mode_prints_filtered_ids(self):
        import subprocess
        import sys
        proc = subprocess.run(
            [sys.executable, str(HELPER), "--raw-key", "20261103T121047Z"],
            input="raw-20261103T121047Z\nraw-20260714T012901Z\nI-20261103T121047Z-A\n",
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.split(), ["raw-20261103T121047Z", "I-20261103T121047Z-A"])


if __name__ == "__main__":
    unittest.main()
