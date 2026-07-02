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
    _acp_bridge_socket, _acp_rpc, _acp_session_resume, _acp_session_new,
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
            'data: {"statusUpdate":{"status":{"state":"input-required"},"metadata":{"reason":"needs-review:b2","raw_key":"raw-20260701T000000Z","from_agent":"worker_01"}}}\n'
        )
        with patch('watchdog_sse._handle_needs_reviewer') as mock_handler:
            _handle_sse_event(TEST_PROJECT, event_text)
            mock_handler.assert_called_once()

    def test_parse_input_required_needs_manager(self):
        """SSE event routes to manager handler."""
        event_text = (
            'event: state_update\n'
            'data: {"statusUpdate":{"status":{"state":"input-required"},"metadata":{"reason":"needs-manager-decision","raw_key":"raw-20260701T000000Z","from_agent":"worker_01"}}}\n'
        )
        with patch('watchdog_sse._handle_needs_manager') as mock_handler:
            _handle_sse_event(TEST_PROJECT, event_text)
            mock_handler.assert_called_once()

    def test_parse_input_required_needs_worker(self):
        """SSE event routes to worker handler."""
        event_text = (
            'event: state_update\n'
            'data: {"statusUpdate":{"status":{"state":"input-required"},"metadata":{"reason":"needs-worker-retry","raw_key":"raw-20260701T000000Z","from_agent":"reviewer_01"}}}\n'
        )
        with patch('watchdog_sse._handle_needs_worker') as mock_handler:
            _handle_sse_event(TEST_PROJECT, event_text)
            mock_handler.assert_called_once()

    def test_skip_non_input_required(self):
        """SSE events with other states are ignored."""
        event_text = 'event: state_update\ndata: {"statusUpdate":{"status":{"state":"working"}}}\n'
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

    def test_acp_session_resume_no_socket(self):
        """_acp_session_resume returns False when no bridge."""
        result = _acp_session_resume("/nonexistent/project", "fake-session-id")
        self.assertFalse(result)

    def test_acp_session_new_no_socket(self):
        """_acp_session_new returns None when no bridge."""
        result = _acp_session_new("/nonexistent/project", "worker", "worker_01")
        self.assertIsNone(result)


class TestAgentHandlers(unittest.TestCase):
    """C14d: Agent handler routing with mocked agent_working."""

    @patch('watchdog_sse.agent_list_by_raw_key')
    @patch('watchdog_sse.agent_next_free')
    @patch('watchdog_sse.agent_assign')
    @patch('watchdog_sse._acp_session_new')
    def test_handle_needs_reviewer_new(self, mock_new, mock_assign, mock_next, mock_list):
        """_handle_needs_reviewer creates new reviewer when none exists."""
        mock_list.return_value = {}
        mock_next.return_value = "reviewer_99"
        mock_new.return_value = "session-abc"

        from watchdog_sse import _handle_needs_reviewer
        _handle_needs_reviewer("/fake/project", {
            "raw_key": "raw-20260701T000000Z",
            "from_agent": "worker_01"
        }, InputRequiredReason.NEEDS_REVIEW_B1)

        mock_next.assert_called_once()
        mock_new.assert_called_once_with("/fake/project", "reviewer", "reviewer_99")
        mock_assign.assert_called_once()

    @patch('watchdog_sse.agent_list_by_raw_key')
    @patch('watchdog_sse.agent_assign')
    @patch('watchdog_sse.agent_get_session')
    @patch('watchdog_sse._acp_session_resume')
    def test_handle_needs_reviewer_duplicate(self, mock_resume, mock_session, mock_assign, mock_list):
        """_handle_needs_reviewer skips new assignment when reviewer already assigned."""
        mock_list.return_value = {"reviewer_id": "reviewer_05:existing-session"}
        mock_session.return_value = None  # no session, so it won't try to resume

        from watchdog_sse import _handle_needs_reviewer
        _handle_needs_reviewer("/fake/project", {
            "raw_key": "raw-20260701T000000Z"
        }, InputRequiredReason.NEEDS_REVIEW_GATE)

        mock_assign.assert_not_called()

    @patch('watchdog_sse.agent_list_by_raw_key')
    @patch('watchdog_sse.agent_next_free')
    def test_handle_needs_reviewer_no_slots(self, mock_next, mock_list):
        """_handle_needs_reviewer handles no free slots gracefully."""
        mock_list.return_value = {}
        mock_next.return_value = None

        from watchdog_sse import _handle_needs_reviewer
        _handle_needs_reviewer("/fake/project", {
            "raw_key": "raw-20260701T000000Z"
        }, InputRequiredReason.NEEDS_REVIEW_DEV)
        # Should not raise

    @patch('watchdog_sse.agent_get_session')
    @patch('watchdog_sse._acp_session_resume')
    @patch('watchdog_sse.agent_list_by_raw_key')
    def test_handle_needs_manager_resume(self, mock_list, mock_resume, mock_session):
        """_handle_needs_manager resumes existing manager session."""
        mock_session.return_value = "manager-session-id"
        mock_resume.return_value = True

        from watchdog_sse import _handle_needs_manager
        _handle_needs_manager("/fake/project", {
            "raw_key": "raw-20260701T000000Z",
            "from_agent": "worker_01"
        }, InputRequiredReason.NEEDS_MANAGER_DECISION)

        mock_resume.assert_called_once()

    @patch('watchdog_sse.agent_get_session')
    @patch('watchdog_sse._acp_session_resume')
    @patch('watchdog_sse.agent_list_by_raw_key')
    def test_handle_needs_worker_resume(self, mock_list, mock_resume, mock_session):
        """_handle_needs_worker resumes existing worker session."""
        mock_session.return_value = "worker-session-id"
        mock_resume.return_value = True

        from watchdog_sse import _handle_needs_worker
        _handle_needs_worker("/fake/project", {
            "raw_key": "raw-20260701T000000Z",
            "from_agent": "reviewer_01"
        }, InputRequiredReason.NEEDS_WORKER_RETRY)

        mock_resume.assert_called_once()


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
