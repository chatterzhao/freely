"""Static + unit coverage for review follow-ups on worker launch fail-closed.

Covers:
1. freely direct-agent path: no ${_worker_agent_id:-worker_01}; empty identity/slot fail-closed
2. agent_assign after atomic assign must not swallow RPC with || true on worker launch chain
3. stats reviewer occupied uses _aw_parse_occupied (bare + session)
"""
import os
import re
import sys
import time
import unittest

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNTIME = os.path.join(PROJECT, "docs", "system", "workspace", "scripts", "runtime")
FREELY = os.path.join(RUNTIME, "freely")
sys.path.insert(0, RUNTIME)


class TestFreelyWorkerLaunchFailClosedStatic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(FREELY) as f:
            cls.src = f.read()

    def test_no_worker_agent_id_default_to_worker_01(self):
        self.assertNotIn(
            "${_worker_agent_id:-worker_01}",
            self.src,
            "direct-agent path must not default empty identity to worker_01",
        )

    def test_direct_fallback_requires_real_agent_id(self):
        # capture_worker_session_id_and_store must use $_worker_agent_id not empty default
        self.assertIn(
            'capture_worker_session_id_and_store "$manager_project" "$worker_cycle_log" "$task_id" "$target_project" "$_worker_agent_id" "$_worker_slot"',
            self.src,
        )
        self.assertNotIn(
            'capture_worker_session_id_and_store "$manager_project" "$worker_cycle_log" "$task_id" "$target_project" "${_worker_agent_id:-}"',
            self.src,
        )

    def test_empty_slot_fail_closed_not_default_claude(self):
        # Forbidden: silent default slot after empty get-slot on launch path
        self.assertNotIn(
            '[[ -z "$_aw_slot" ]] && _aw_slot="${AGENT_AI_TOOL:-claude}"',
            self.src,
        )
        self.assertNotIn(
            '|| echo "${AGENT_AI_TOOL:-claude-apikey-ds-flash-auto}"',
            self.src,
        )
        self.assertIn(
            "worker launch: no slot for assigned agent",
            self.src,
        )
        self.assertIn(
            "worker launch: agent_assign/session register failed",
            self.src,
        )

    def test_worker_raw_key_is_extracted_and_never_defaults_to_develop(self):
        sync_start = self.src.find("sync_project_tooling_from_source()")
        sync_end = self.src.find("write_project_codex_config()", sync_start)
        self.assertGreater(sync_start, 0)
        self.assertGreater(sync_end, sync_start)
        sync_region = self.src[sync_start:sync_end]
        self.assertIn('_worker_raw_key="$(printf', sync_region)
        self.assertIn("agent-table: target worktree has no issue raw_key (fail-closed)", sync_region)
        self.assertNotIn("or 'develop'", sync_region)

        launch_start = self.src.find(
            "Atomic assign FIRST — identity must exist before slot/bridge/direct launch."
        )
        launch_end = self.src.find("launching worker AI via manager bridge (fork session):", launch_start)
        self.assertGreater(launch_start, 0)
        self.assertGreater(launch_end, launch_start)
        launch_region = self.src[launch_start:launch_end]
        self.assertIn("worker launch: target worktree has no issue raw_key (fail-closed)", launch_region)
        self.assertNotIn("or 'develop'", launch_region)

    def test_worker_launch_agent_assign_not_swallowed(self):
        """Worker launch enrich path must not use agent_assign ... || true."""
        # Extract region around worker launch atomic assign
        markers = [
            "Atomic assign FIRST — identity must exist before slot/bridge/direct launch.",
            "launching worker AI via manager bridge (fork session):",
        ]
        start = self.src.find(markers[0])
        self.assertGreater(start, 0, "atomic-first marker missing")
        end = self.src.find(markers[1], start)
        self.assertGreater(end, start)
        region = self.src[start:end]
        # Must have fail-closed agent_assign
        self.assertIn("agent_assign failed", region)
        self.assertIn("agent_release_all", region)
        # No swallow of agent_assign in this region
        for line in region.splitlines():
            if "agent_assign" in line and "|| true" in line:
                self.fail(f"agent_assign swallowed with || true: {line.strip()}")

    def test_sync_path_agent_assign_not_swallowed(self):
        self.assertIn(
            "agent-table: agent_assign failed for $_next_worker (released pending, fail-closed)",
            self.src,
        )
        # One-liners that swallow agent_assign RPC — only worker-role calls are in scope.
        # discuss-*/manager_01 static bookkeeping is outside the worker launch chain.
        bad = re.findall(
            r"agent_assign\([^)]*\)\"\s*2>/dev/null \|\| true",
            self.src,
        )
        worker_bad = [
            b for b in bad
            if re.search(r"['\"]worker['\"]", b)
            or "_next_worker" in b
            or "_worker_agent_id" in b
        ]
        self.assertEqual(worker_bad, [], f"worker path still swallows assign: {worker_bad}")
        # Explicit: worker launch / sync-tooling regions must not contain || true after assign
        for marker, end_marker in (
            (
                "Atomic assign FIRST — identity must exist before slot/bridge/direct launch.",
                "launching worker AI via manager bridge (fork session):",
            ),
            (
                "Atomic assign via agent_working; use returned agent_id for slot (no second assign).",
                "agent-table: assigned $_next_worker",
            ),
        ):
            start = self.src.find(marker)
            self.assertGreater(start, 0, f"missing marker: {marker}")
            end = self.src.find(end_marker, start)
            self.assertGreater(end, start, f"missing end marker after {marker}")
            region = self.src[start:end]
            for line in region.splitlines():
                if "agent_assign" in line and "|| true" in line:
                    self.fail(f"swallowed agent_assign in worker chain: {line.strip()}")


class TestStatsReviewerOccupied(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from freely_db_manager import DbDaemon
        cls.daemon = DbDaemon(PROJECT)
        cls.daemon._open_db()
        cls.daemon._ensure_tables()
        cls.daemon.running = True

    @classmethod
    def tearDownClass(cls):
        cls.daemon.conn.close()

    def setUp(self):
        self.prefix = f"stats-rev-{int(time.time()*1000)}"
        self.daemon.conn.execute(
            "DELETE FROM agent_working WHERE raw_key LIKE ?", (f"{self.prefix}%",)
        )
        self.daemon.conn.commit()

    def tearDown(self):
        self.daemon.conn.execute(
            "DELETE FROM agent_working WHERE raw_key LIKE ?", (f"{self.prefix}%",)
        )
        self.daemon.conn.commit()

    def test_bare_and_session_reviewer_count_equal(self):
        d = self.daemon.dispatch
        # bare reviewer_id
        self.daemon.conn.execute(
            "INSERT INTO agent_working (raw_key, reviewer_id, updated_at) VALUES (?,?,datetime('now'))",
            (f"{self.prefix}-bare", "reviewer_03"),
        )
        # agent_id:session
        self.daemon.conn.execute(
            "INSERT INTO agent_working (raw_key, reviewer_id, updated_at) VALUES (?,?,datetime('now'))",
            (f"{self.prefix}-sess", "reviewer_04:sess-xyz"),
        )
        # multi CSV with one bare + one session
        self.daemon.conn.execute(
            "INSERT INTO agent_working (raw_key, reviewer_id, updated_at) VALUES (?,?,datetime('now'))",
            (f"{self.prefix}-multi", "reviewer_05,reviewer_06:sess-a"),
        )
        self.daemon.conn.commit()

        from freely_db_manager import _aw_parse_occupied
        self.assertEqual(_aw_parse_occupied("reviewer", "reviewer_03"), {"reviewer_03"})
        self.assertEqual(_aw_parse_occupied("reviewer", "reviewer_04:sess-xyz"), {"reviewer_04"})
        self.assertEqual(
            _aw_parse_occupied("reviewer", "reviewer_05,reviewer_06:sess-a"),
            {"reviewer_05", "reviewer_06"},
        )

        stats = d("agent_working.stats", {})
        occ = stats["reviewer"]["occupied"]
        # At least the 4 distinct reviewers we inserted (global table may have others)
        # Verify our four are counted by re-parsing rows with same helper
        rows = self.daemon.conn.execute(
            "SELECT reviewer_id FROM agent_working WHERE raw_key LIKE ?",
            (f"{self.prefix}%",),
        ).fetchall()
        ids = set()
        for r in rows:
            ids |= _aw_parse_occupied("reviewer", r["reviewer_id"] or "")
        self.assertEqual(ids, {"reviewer_03", "reviewer_04", "reviewer_05", "reviewer_06"})
        self.assertGreaterEqual(occ, 4)

    def test_stats_matches_parse_occupied_length(self):
        """stats.occupied for reviewer equals union size via _aw_parse_occupied."""
        d = self.daemon.dispatch
        self.daemon.conn.execute(
            "INSERT INTO agent_working (raw_key, reviewer_id, updated_at) VALUES (?,?,datetime('now'))",
            (f"{self.prefix}-only", "reviewer_07"),
        )
        self.daemon.conn.commit()
        from freely_db_manager import _aw_parse_occupied
        all_rows = self.daemon.conn.execute(
            "SELECT reviewer_id FROM agent_working WHERE reviewer_id IS NOT NULL"
        ).fetchall()
        expected = set()
        for r in all_rows:
            expected |= _aw_parse_occupied("reviewer", r["reviewer_id"] or "")
        stats = d("agent_working.stats", {})
        self.assertEqual(stats["reviewer"]["occupied"], len(expected))


class TestScanAgentWorkingFailClosed(unittest.TestCase):
    def test_scan_does_not_redelegate_when_identity_store_unavailable(self):
        scan_path = os.path.join(RUNTIME, "task-lifecycle-scan.py")
        with open(scan_path) as f:
            source = f.read()
        self.assertIn("agent_binding_error", source)
        self.assertIn('"3_binding_unavailable"', source)
        self.assertIn("do not re-delegate", source)
        self.assertNotIn(
            "except Exception:\n                pass\n\n            # agent_working is the sole source of truth.",
            source,
        )


if __name__ == "__main__":
    unittest.main()
