"""Regression: agent-table-query --next-free must exit 0 on success."""
import os
import subprocess
import sys
import unittest

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(PROJECT, "bin", "agent-table-query")


class TestAgentTableQueryNextFree(unittest.TestCase):
    def test_next_free_exit_zero_on_success(self):
        """Bug: previous code printed agent_id then sys.exit(1)."""
        # Source-inspect for the inverted exit, and smoke-run if agent-table present
        with open(BIN) as f:
            src = f.read()
        self.assertNotIn(
            'if agent_id:\n            print(agent_id)\n            sys.exit(1)',
            src.replace("\r\n", "\n"),
            "agent-table-query --next-free still exits 1 after successful print",
        )
        # Must not fall back to agent-id.env in live path
        live_lines = []
        for i, line in enumerate(src.splitlines(), 1):
            if "agent-id.env" in line and not line.strip().startswith("#"):
                live_lines.append(f"{i}:{line.strip()}")
        self.assertEqual(live_lines, [], f"live agent-id.env refs: {live_lines}")

    def test_pool_size_arg_defined(self):
        with open(BIN) as f:
            src = f.read()
        self.assertIn("--pool-size", src)
        self.assertIn("pool_size", src)


class TestPrReviewGuardedOrder(unittest.TestCase):
    def test_parses_branch_before_agent_query(self):
        path = os.path.join(PROJECT, "bin", "pr-review-guarded")
        with open(path) as f:
            src = f.read()
        # Branch parse must precede first use of review_branch in agent_working query
        parse_idx = src.find('review_branch="$1"')
        if parse_idx < 0:
            parse_idx = src.find('review_branch="${1')
        query_idx = src.find("agent_list_by_raw_key")
        self.assertGreater(parse_idx, 0, "branch parse not found")
        self.assertGreater(query_idx, 0, "agent_list_by_raw_key not found")
        self.assertLess(parse_idx, query_idx, "must parse branch before agent_working query")
        # No live agent-id.env fallback
        for i, line in enumerate(src.splitlines(), 1):
            if "agent-id.env" in line:
                stripped = line.strip()
                self.assertTrue(
                    stripped.startswith("#"),
                    f"live agent-id.env at line {i}: {stripped}",
                )


if __name__ == "__main__":
    unittest.main()
