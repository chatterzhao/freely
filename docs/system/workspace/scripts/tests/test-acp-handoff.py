#!/usr/bin/env python3
"""RED test: new/fork must prompt with the handoff message."""
import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[5]
MOD = ROOT / "docs/system/workspace/scripts/runtime/agent_working.py"


class AcpHandoffTest(unittest.TestCase):
    def test_new_and_fork_prompt(self):
        if not MOD.exists():
            self.fail(f"missing module: {MOD}")
        sys.path.insert(0, str(MOD.parent))
        spec = importlib.util.spec_from_file_location("agent_working", MOD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertTrue(hasattr(mod, "_prompt_after_connect"), "missing _prompt_after_connect helper")
        calls = []
        original = mod._acp_bridge_call
        mod._acp_bridge_call = lambda project, tool, method, params: calls.append((method, params)) or {}
        try:
            mod._prompt_after_connect("/tmp/p", "codex", "sid-1", "reviewer", "do review")
        finally:
            mod._acp_bridge_call = original
        self.assertEqual(calls[0][0], "session/prompt")
        self.assertEqual(calls[0][1]["sessionId"], "sid-1")
        self.assertIn("[role:reviewer]", calls[0][1]["prompt"])
        self.assertIn("do review", calls[0][1]["prompt"])


if __name__ == "__main__":
    unittest.main()
