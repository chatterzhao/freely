#!/usr/bin/env python3
"""Test a2a_task.insert SQL column/value alignment.

This test directly exercises h_a2a_task_insert to verify:
1. INSERT succeeds (no SQL error about column/value count mismatch)
2. All Freely-specific fields (agent_id, skill, worktree, branch,
   prompt_file, raw_key, etc.) are stored correctly
3. Values map to the correct columns (no off-by-one shifts)

Run: python3 tests/test_a2a_task_insert.py
"""

import os
import sys
import sqlite3
import tempfile
import uuid
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestA2ATaskInsert(unittest.TestCase):
    """Verify a2a_tasks INSERT column/value alignment."""

    def setUp(self):
        """Create a fresh in-memory DB with the a2a_tasks schema."""
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        # Replicate the full production schema
        self.db.executescript("""
            CREATE TABLE a2a_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL DEFAULT '',
                description TEXT NOT NULL DEFAULT '',
                state TEXT NOT NULL DEFAULT 'submitted'
                    CHECK(state IN ('submitted','working','input-required',
                         'pending-input','completed','failed','canceled')),
                agent_id TEXT NOT NULL DEFAULT '',
                skill TEXT NOT NULL DEFAULT '',
                session_id TEXT NOT NULL DEFAULT '',
                message TEXT NOT NULL DEFAULT '',
                raw_key TEXT NOT NULL DEFAULT '',
                prompt_file TEXT NOT NULL DEFAULT '',
                worktree TEXT NOT NULL DEFAULT '',
                branch TEXT NOT NULL DEFAULT '',
                exit_kind TEXT NOT NULL DEFAULT '',
                reason TEXT NOT NULL DEFAULT '',
                progress TEXT NOT NULL DEFAULT '',
                next_action TEXT NOT NULL DEFAULT '',
                completion_summary TEXT NOT NULL DEFAULT '',
                evidence_paths TEXT NOT NULL DEFAULT '',
                worker_prompts_csv TEXT NOT NULL DEFAULT '',
                error TEXT NOT NULL DEFAULT '',
                worker_pid TEXT NOT NULL DEFAULT '',
                delivery_status TEXT NOT NULL DEFAULT 'pending'
                    CHECK(delivery_status IN ('pending','delivered','failed')),
                messages_json TEXT NOT NULL DEFAULT '[]',
                launched_at TEXT NOT NULL DEFAULT '',
                completed_at TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT ''
            )
        """)
        # Mock Daemon object with our in-memory DB
        self.daemon = MagicMock()
        self.daemon.conn = self.db

    def tearDown(self):
        self.db.close()

    def _insert(self, **overrides):
        """Call h_a2a_task_insert with optional field overrides."""
        from docs.system.workspace.scripts.runtime.freely_db_manager import (
            h_a2a_task_insert,
        )
        params = {
            "task_id": str(uuid.uuid4()),
            "name": "test-worker",
            "agent_id": "worker",
            "state": "submitted",
            "skill": "freely-fix-execution",
            "message": "test worker task summary",
            "raw_key": "raw-20260619T000000Z",
            "prompt_file": "/tmp/prompts/task-001.txt",
            "worktree": "/tmp/test-worktree",
            "branch": "fix/raw-20260619T000000Z-test",
            "exit_kind": "submitted",
            "session_id": "ses_test123",
            "reason": "",
            "progress": "",
            "next_action": "issue-sync create",
            "completion_summary": "",
            "evidence_paths": "",
            "error": "",
        }
        params.update(overrides)
        return h_a2a_task_insert(self.daemon, params)

    # ── Core fix verification ──

    def test_insert_succeeds(self):
        """INSERT must succeed — no SQL error about column/value count."""
        result = self._insert()
        self.assertIn("task_id", result)
        self.assertEqual(result.get("affected"), 1)
        task_id = result["task_id"]

        row = self.db.execute(
            "SELECT * FROM a2a_tasks WHERE task_id = ?", (task_id,)
        ).fetchone()
        self.assertIsNotNone(row, "Task was not persisted after insert")

    def test_agent_id_is_worker(self):
        """agent_id must be 'worker' when worker task is created."""
        result = self._insert(agent_id="worker")
        row = self.db.execute(
            "SELECT agent_id FROM a2a_tasks WHERE task_id = ?",
            (result["task_id"],),
        ).fetchone()
        self.assertEqual(row["agent_id"], "worker")

    def test_skill_field_preserved(self):
        """skill field must map to the correct column."""
        result = self._insert(skill="freely-dev-loop-execution")
        row = self.db.execute(
            "SELECT skill FROM a2a_tasks WHERE task_id = ?",
            (result["task_id"],),
        ).fetchone()
        self.assertEqual(row["skill"], "freely-dev-loop-execution")

    # ── Column alignment verification (caught the misalignment bug) ──

    def test_prompt_file_column_not_shifted_to_worktree(self):
        """prompt_file value must NOT leak into the worktree column."""
        result = self._insert(
            prompt_file="/p/test.txt",
            worktree="/wt/test",
        )
        row = self.db.execute(
            "SELECT prompt_file, worktree FROM a2a_tasks WHERE task_id = ?",
            (result["task_id"],),
        ).fetchone()
        self.assertEqual(row["prompt_file"], "/p/test.txt",
                         "prompt_file leaked into wrong column")
        self.assertEqual(row["worktree"], "/wt/test",
                         "worktree leaked into wrong column")

    def test_branch_and_exit_kind_not_swapped(self):
        """branch must not receive exit_kind's value."""
        result = self._insert(
            branch="fix/test-branch",
            exit_kind="submitted",
        )
        row = self.db.execute(
            "SELECT branch, exit_kind FROM a2a_tasks WHERE task_id = ?",
            (result["task_id"],),
        ).fetchone()
        self.assertEqual(row["branch"], "fix/test-branch")
        self.assertEqual(row["exit_kind"], "submitted")

    def test_completion_summary_not_shifted_to_evidence(self):
        """completion_summary must not receive evidence_paths value."""
        result = self._insert(
            completion_summary="done",
            evidence_paths="/ev/path",
        )
        row = self.db.execute(
            "SELECT completion_summary, evidence_paths FROM a2a_tasks WHERE task_id = ?",
            (result["task_id"],),
        ).fetchone()
        self.assertEqual(row["completion_summary"], "done")
        self.assertEqual(row["evidence_paths"], "/ev/path")

    def test_error_column_at_correct_position(self):
        """error must be the last inserted column value."""
        result = self._insert(error="test-error-msg")
        row = self.db.execute(
            "SELECT error FROM a2a_tasks WHERE task_id = ?",
            (result["task_id"],),
        ).fetchone()
        self.assertEqual(row["error"], "test-error-msg")

    # ── Full round-trip: simulate the A2A create + update flow ──

    def test_full_worker_task_round_trip(self):
        """Simulate A2A Server's save() + update() flow."""
        # Step 1: INSERT (save)
        result = self._insert(agent_id="worker", state="submitted")
        task_id = result["task_id"]

        # Step 2: UPDATE with Freely-specific fields (raw_rpc("a2a_task.update"))
        from docs.system.workspace.scripts.runtime.freely_db_manager import (
            h_a2a_task_update,
        )
        update_result = h_a2a_task_update(self.daemon, {
            "task_id": task_id,
            "agent_id": "worker",
            "skill": "freely-fix-execution",
            "worktree": "/wt/test",
            "branch": "fix/test",
            "raw_key": "raw-20260619T000000Z",
            "completion_summary": "worker completed task",
            "message": "full task message",
            "state": "submitted",
        })
        self.assertGreater(update_result.get("affected", 0), 0,
                           "UPDATE did not affect any rows")

        # Step 3: Verify task is queryable as a worker task
        row = self.db.execute(
            "SELECT task_id, agent_id, state, worktree, branch, "
            "completion_summary FROM a2a_tasks WHERE task_id = ?",
            (task_id,),
        ).fetchone()
        self.assertEqual(row["agent_id"], "worker")
        self.assertEqual(row["state"], "submitted")
        self.assertEqual(row["worktree"], "/wt/test")
        self.assertEqual(row["completion_summary"], "worker completed task")

    # ── Regression: ensure old broken 21-value INSERT no longer exists ──

    def test_no_21_placeholder_insert(self):
        """Verify the VALUES clause has exactly 20 placeholders."""
        import inspect
        from docs.system.workspace.scripts.runtime.freely_db_manager import (
            h_a2a_task_insert,
        )
        src = inspect.getsource(h_a2a_task_insert)
        # Count ? in the VALUES line
        for line in src.split("\n"):
            if "VALUES" in line:
                count = line.count("?")
                self.assertEqual(
                    count, 20,
                    f"VALUES has {count} placeholders, expected 20"
                )
                break
        else:
            self.fail("VALUES line not found in h_a2a_task_insert source")


if __name__ == "__main__":
    unittest.main()
