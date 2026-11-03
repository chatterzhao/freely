#!/usr/bin/env python3
"""Wiring regression guard for owner-lane claim.

The defect this locks: `_resolve_current_agent_id` called `owner_lane.py claim`
inside `if [[ -z "$_my_id" && "$_current_path" != "$project" ]]`.  When the
daemon runs *inside* a worktree, `pwd` and the project argument are the same
path, so the condition was always false and the claim never ran -- while the
failure message stayed identical to the pre-fix behaviour, which is why it was
mistaken for "already fixed".

`owner_lane.claim` already refuses every unsafe case (existing binding, no raw
key in the branch, several managers, foreign path, unreadable DB), so the bash
side must not re-implement that decision as a path comparison.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUNTIME = ROOT / "docs/system/workspace/scripts/runtime/freely"


def claim_block() -> str:
    source = RUNTIME.read_text()
    start = source.index("_resolve_current_agent_id() {")
    end = source.index("\n}\n", start)
    return source[start:end]


class ClaimWiringTests(unittest.TestCase):
    def test_claim_is_actually_called(self):
        block = claim_block()
        self.assertIn("owner_lane.py", block)
        self.assertIn("claim --project", block)

    def test_no_path_inequality_guard_hides_the_claim(self):
        block = claim_block()
        patterns = [
            r'_current_path"?\s*!=\s*"?\$project',
            r'\$project"?\s*!=\s*"?\$_current_path',
            r"_current_path'\s*!=\s*'\$project",
        ]
        for pattern in patterns:
            self.assertIsNone(
                re.search(pattern, block),
                "path-inequality guard is back; it is always false inside a worktree",
            )

    def test_claim_failure_reason_is_not_swallowed(self):
        block = claim_block()
        claim_lines = [line for line in block.splitlines() if "claim --project" in line]
        self.assertTrue(claim_lines, block)
        self.assertFalse(
            any("2>/dev/null" in line for line in claim_lines),
            "claim stderr must stay visible so failures carry a reason",
        )


if __name__ == "__main__":
    unittest.main()
