"""C14: SSE + ACP integration tests for watchdog_sse.py.

Tests the watchdog's ACP bridge helpers, SSE event parsing,
and agent handler routing without requiring a running system.
"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Add project root for imports
TEST_PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(TEST_PROJECT, "docs", "system", "workspace", "scripts", "runtime"))
sys.path.insert(0, os.path.join(TEST_PROJECT, "docs", "system", "workspace", "agents"))

# Import watchdog helpers (does not start the main loop)
from watchdog_sse import (
    _acp_bridge_socket, _acp_rpc,
    _handle_sse_event, _check_agent_liveness, _check_session_staleness,
)
from input_required_reason import InputRequiredReason


class TestAcpBridgeSocket(unittest.TestCase):
    """C14a: ACP bridge socket discovery."""

    def test_returns_none_when_no_socket(self):
        """_acp_bridge_socket returns None when socket doesn't exist."""
        result = _acp_bridge_socket("/nonexistent/project/path")
        self.assertIsNone(result)

    def test_consistent_hash_same_project(self):
        """Same project path produces same socket path."""
        r1 = _acp_bridge_socket("/tmp/fake-project")
        r2 = _acp_bridge_socket("/tmp/fake-project")
        self.assertIsNone(r1)
        self.assertEqual(r1, r2)


class TestSseEventParsing(unittest.TestCase):
    """C14b: SSE event parsing and routing."""

    def test_parse_input_required_reviewer(self):
        """SSE event with needs-review triggers reviewer handler."""
        event_text = (
            'event: state_update\n'
            'data: {"task_id":"task-123","state":"input-required","reason":"needs-review:b2","raw_key":"raw-20260701T000000Z","from_agent":"worker_01","needs_role":"reviewer"}\n'
        )
        with patch('watchdog_sse._handle_needs_reviewer') as mock_handler:
            _handle_sse_event(TEST_PROJECT, event_text)
            mock_handler.assert_called_once()

    def test_parse_input_required_needs_manager(self):
        """SSE event routes to manager handler."""
        event_text = (
            'event: state_update\n'
            'data: {"task_id":"task-456","state":"input-required","reason":"needs-manager-decision","raw_key":"raw-20260701T000000Z","from_agent":"worker_01","needs_role":"manager"}\n'
        )
        with patch('watchdog_sse._handle_needs_manager') as mock_handler:
            _handle_sse_event(TEST_PROJECT, event_text)
            mock_handler.assert_called_once()

    def test_parse_input_required_needs_worker(self):
        """SSE event routes to worker handler."""
        event_text = (
            'event: state_update\n'
            'data: {"task_id":"task-789","state":"input-required","reason":"needs-worker-retry","raw_key":"raw-20260701T000000Z","from_agent":"reviewer_01","needs_role":"worker"}\n'
        )
        with patch('watchdog_sse._handle_needs_worker') as mock_handler:
            _handle_sse_event(TEST_PROJECT, event_text)
            mock_handler.assert_called_once()

    def test_skip_non_input_required(self):
        """SSE events with other states are ignored."""
        event_text = 'event: state_update\ndata: {"task_id":"task-skip","state":"working"}\n'
        with patch('watchdog_sse._handle_needs_reviewer') as m1, \
             patch('watchdog_sse._handle_needs_manager') as m2, \
             patch('watchdog_sse._handle_needs_worker') as m3:
            _handle_sse_event(TEST_PROJECT, event_text)
            m1.assert_not_called()
            m2.assert_not_called()
            m3.assert_not_called()

    def test_parse_invalid_json(self):
        """Malformed SSE data is handled gracefully."""
        event_text = 'data: {invalid json!!!}\n'
        _handle_sse_event(TEST_PROJECT, event_text)

    def test_parse_empty_event(self):
        """Empty SSE event text is handled."""
        _handle_sse_event(TEST_PROJECT, "")


class TestAcpRpc(unittest.TestCase):
    """C14c: ACP RPC communication helpers."""

    def test_acp_rpc_no_socket_returns_none(self):
        """_acp_rpc returns None when no bridge socket exists."""
        result = _acp_rpc("/nonexistent/project", "session/new", {"role": "worker"})
        self.assertIsNone(result)

class TestAgentHandlers(unittest.TestCase):
    """C14d: handlers delegate session policy to the unified connector."""

    @patch("watchdog_sse._get_agent_slot", return_value="cline-slot-01")
    @patch("watchdog_sse.acp_session_connect", return_value=("session-abc", "new"))
    @patch("watchdog_sse.agent_next_free", return_value="reviewer_99")
    @patch("watchdog_sse.agent_list_by_raw_key", return_value={})
    def test_handle_needs_reviewer_new(self, _list, next_free, connect, _slot):
        from watchdog_sse import _handle_needs_reviewer

        _handle_needs_reviewer("/fake/project", {
            "raw_key": "raw-20260701T000000Z",
            "from_agent": "worker_01",
        }, InputRequiredReason.NEEDS_REVIEW_B1)

        next_free.assert_called_once()
        self.assertEqual(connect.call_args.args[:4], (
            "/fake/project", "raw-20260701T000000Z", "reviewer", "reviewer_99",
        ))
        self.assertFalse(connect.call_args.kwargs["force_new"])

    @patch("watchdog_sse._get_agent_slot", return_value="cline-slot-01")
    @patch("watchdog_sse.acp_session_connect", return_value=("session-live", "prompt"))
    @patch("watchdog_sse.agent_list_by_raw_key", return_value={
        "reviewer_id": "reviewer_05:session-live,reviewer_06:session-other"
    })
    def test_handle_needs_reviewer_preserves_exact_identity(self, _list, connect, _slot):
        from watchdog_sse import _handle_needs_reviewer

        _handle_needs_reviewer("/fake/project", {
            "raw_key": "raw-20260701T000000Z",
        }, InputRequiredReason.NEEDS_REVIEW_B2)

        self.assertEqual(connect.call_args.args[:4], (
            "/fake/project", "raw-20260701T000000Z", "reviewer", "reviewer_05",
        ))

    @patch("watchdog_sse._get_agent_slot", return_value="cline-slot-01")
    @patch("watchdog_sse.acp_session_connect", return_value=("session-gate", "new"))
    @patch("watchdog_sse.agent_next_free", return_value="reviewer_99")
    @patch("watchdog_sse.agent_list_by_raw_key", return_value={})
    def test_handle_needs_reviewer_gate_forces_new(self, _list, _next, connect, _slot):
        from watchdog_sse import _handle_needs_reviewer

        _handle_needs_reviewer("/fake/project", {
            "raw_key": "raw-20260701T000000Z",
        }, InputRequiredReason.NEEDS_REVIEW_GATE)

        self.assertTrue(connect.call_args.kwargs["force_new"])

    @patch("watchdog_sse.agent_next_free", return_value=None)
    @patch("watchdog_sse.agent_list_by_raw_key", return_value={})
    def test_handle_needs_reviewer_no_slots(self, _list, _next):
        from watchdog_sse import _handle_needs_reviewer

        _handle_needs_reviewer("/fake/project", {
            "raw_key": "raw-20260701T000000Z",
        }, InputRequiredReason.NEEDS_REVIEW_DEV)


class TestSessionPrompt(unittest.TestCase):
    """Phase 1-2: session/prompt message delivery and handler decision tree."""

    def test_build_review_task_message(self):
        """_build_review_task_message contains key context fields."""
        from watchdog_sse import _build_review_task_message
        msg = _build_review_task_message("raw-20260701T000000Z", "worker_03",
                                          InputRequiredReason.NEEDS_REVIEW_B1)
        self.assertIn("raw-20260701T000000Z", msg)
        self.assertIn("worker_03", msg)
        self.assertIn("b1", msg)  # review stage from reason value

    def test_build_worker_verdict_message(self):
        """_build_worker_verdict_message contains key context fields."""
        from watchdog_sse import _build_worker_verdict_message
        msg = _build_worker_verdict_message("raw-20260701T000000Z", "reviewer_05",
                                             InputRequiredReason.NEEDS_WORKER_RETRY,
                                             {"verdict": "fail"})
        self.assertIn("raw-20260701T000000Z", msg)
        self.assertIn("reviewer_05", msg)
        self.assertIn("needs-worker-retry", msg)

    @patch("watchdog_sse._get_agent_slot", return_value="cline-slot-03")
    @patch("watchdog_sse.acp_session_connect", return_value=("ses_wrk", "prompt"))
    @patch("watchdog_sse.agent_list_by_raw_key", return_value={"worker_id": "worker_03:ses_wrk"})
    def test_worker_route_uses_unified_connector(self, _list, connect, _slot):
        from watchdog_sse import _handle_needs_worker

        _handle_needs_worker("/fake/project", {
            "raw_key": "raw-20260701T000000Z",
            "from_agent": "reviewer_05",
        }, InputRequiredReason.NEEDS_WORKER_RETRY)

        self.assertEqual(connect.call_args.args[:4], (
            "/fake/project", "raw-20260701T000000Z", "worker", "worker_03",
        ))
        self.assertIn("reviewer_05", connect.call_args.kwargs["message"])

    @patch("watchdog_sse._get_agent_slot", return_value="claude-slot-01")
    @patch("watchdog_sse.acp_session_connect", return_value=("ses_mgr", "prompt"))
    @patch("watchdog_sse.agent_next_free", return_value="manager_01")
    def test_manager_route_uses_unified_connector(self, _next, connect, _slot):
        from watchdog_sse import _handle_needs_manager

        _handle_needs_manager("/fake/project", {
            "raw_key": "raw-20260701T000000Z",
            "from_agent": "worker_03",
        }, InputRequiredReason.NEEDS_MANAGER_DECISION)

        self.assertEqual(connect.call_args.args[:4], (
            "/fake/project", "__manager__", "manager", "manager_01",
        ))
        self.assertIn("worker_03", connect.call_args.kwargs["message"])


class TestLivenessAndStaleness(unittest.TestCase):
    """C14e: Agent crash detection and staleness checks."""

    @patch('agent_working._db_rpc')
    def test_check_liveness_empty(self, mock_rpc):
        """_check_agent_liveness handles empty agent_working table."""
        mock_rpc.return_value = {"rows": []}
        _check_agent_liveness("/fake/project")

    @patch('agent_working._db_rpc')
    @patch('subprocess.run')
    def test_check_liveness_dead_process(self, mock_run, mock_rpc):
        """_check_agent_liveness detects dead processes."""
        mock_rpc.return_value = {
            "rows": [{
                "raw_key": "raw-20260701T000000Z",
                "worker_id": "worker_01:dead-session-123",
                "reviewer_id": "",
                "manager_id": ""
            }]
        }
        mock_result = MagicMock()
        mock_result.returncode = 1  # pgrep failed = process dead
        mock_run.return_value = mock_result
        _check_agent_liveness("/fake/project")

    def test_check_staleness_skips_recent(self):
        """_check_session_staleness rate-limits itself (300s interval)."""
        import watchdog_sse
        watchdog_sse._last_staleness_check = 1e12
        _check_session_staleness("/fake/project")


if __name__ == "__main__":
    unittest.main()
