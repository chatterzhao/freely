#!/usr/bin/env python3
"""RED test: Reviewer verdict contract must be identical in three places."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[5]
FILES = [
    ROOT / "docs/system/workspace/agents/reviewer-agent.md",
    ROOT / "docs/system/workspace/scripts/runtime/watchdog_sse.py",
    ROOT / "docs/system/workspace/skills/freely-tdd-review/SKILL.md",
]


class ReviewerContractTest(unittest.TestCase):
    def test_single_exit_contract(self):
        texts = [p.read_text(encoding="utf-8") for p in FILES if p.exists()]
        self.assertEqual(len(texts), 3, "reviewer contract files missing")
        needle = "a2a-exit --state completed --summary"
        for p, text in zip(FILES, texts):
            self.assertIn(needle, text, f"{p} does not use the single contract")
            self.assertNotIn("不用 a2a_task.py / a2a-exit", text, f"{p} still forbids the contract")


if __name__ == "__main__":
    unittest.main()
