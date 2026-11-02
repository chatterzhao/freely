#!/usr/bin/env python3
"""RED/GREEN contract for owner-lane identity claim.

An owner-created worktree has no `agent_working` row, so the daemon cannot
resolve which agent it is and refuses to start.  The claim is deliberately
narrow: it only fills a *missing* row, only for the single configured manager,
and only for a real worktree of this project.
"""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "docs/system/workspace/scripts/runtime/owner_lane.py"
PATH = "/repo/freely-worktrees/fix-raw-20261102T103231Z-owner-lane-daemon-identity"
BRANCH = "fix/raw-20261102T103231Z-owner-lane-daemon-identity"


def load():
    spec = importlib.util.spec_from_file_location("owner_lane", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OwnerLaneClaimTests(unittest.TestCase):
    def setUp(self):
        self.subject = load()
        self.writes = []

    def _write(self, *args, **kwargs):
        self.writes.append((args, kwargs))
        return {"ok": True}

    def test_existing_binding_is_returned_untouched(self):
        result = self.subject.claim(
            project="/repo",
            path=PATH,
            rows=[{"raw_key": "20261102T103231Z", "worktree": PATH, "worker_id": "worker_03:ses_x"}],
            managers=["manager_01"],
            worktrees={PATH: BRANCH},
            write=self._write,
        )
        self.assertEqual(result["agent_id"], "worker_03")
        self.assertFalse(result["created"])
        self.assertEqual(self.writes, [])

    def test_zero_row_claims_the_single_manager(self):
        result = self.subject.claim(
            project="/repo",
            path=PATH,
            rows=[],
            managers=["manager_01"],
            worktrees={PATH: BRANCH},
            write=self._write,
        )
        self.assertTrue(result["created"])
        self.assertEqual(result["agent_id"], "manager_01")
        self.assertEqual(result["raw_key"], "20261102T103231Z")
        self.assertEqual(len(self.writes), 1)
        args, kwargs = self.writes[0]
        self.assertEqual(args[2], "manager")
        self.assertEqual(args[3], "manager_01")

    def test_ambiguous_manager_configuration_stays_closed(self):
        result = self.subject.claim(
            project="/repo",
            path=PATH,
            rows=[],
            managers=["manager_01", "manager_02"],
            worktrees={PATH: BRANCH},
            write=self._write,
        )
        self.assertIsNone(result["agent_id"])
        self.assertEqual(result["reason"], "manager_not_unique")
        self.assertEqual(self.writes, [])

    def test_path_outside_project_worktrees_is_rejected(self):
        result = self.subject.claim(
            project="/repo",
            path="/tmp/not-a-worktree",
            rows=[],
            managers=["manager_01"],
            worktrees={PATH: BRANCH},
            write=self._write,
        )
        self.assertIsNone(result["agent_id"])
        self.assertEqual(result["reason"], "not_a_worktree")
        self.assertEqual(self.writes, [])

    def test_test_lane_branch_without_raw_prefix_still_resolves(self):
        result = self.subject.claim(
            project="/repo",
            path=PATH,
            rows=[],
            managers=["manager_01"],
            worktrees={PATH: "test-pre-merge-20261102T103231Z-owner-lane-daemon-identity"},
            write=self._write,
        )
        self.assertTrue(result["created"], result)
        self.assertEqual(result["raw_key"], "20261102T103231Z")

    def test_branch_without_raw_key_is_not_guessed(self):
        result = self.subject.claim(
            project="/repo",
            path=PATH,
            rows=[],
            managers=["manager_01"],
            worktrees={PATH: "scratch/whatever"},
            write=self._write,
        )
        self.assertIsNone(result["agent_id"])
        self.assertEqual(result["reason"], "raw_key_unresolved")
        self.assertEqual(self.writes, [])

    def test_agent_table_is_read_from_freely_home(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            worktree = Path(root) / "wt"
            (worktree / ".freely").mkdir(parents=True)
            (worktree / ".freely" / "config.toml").write_text('FREELY_HOME = "/repo/main"\n')
            self.assertEqual(self.subject._home(str(worktree)), "/repo/main")
            self.assertEqual(self.subject._home("/nonexistent/project"), "/nonexistent/project")


if __name__ == "__main__":
    unittest.main()
