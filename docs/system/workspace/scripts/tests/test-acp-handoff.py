#!/usr/bin/env python3
"""RED test: new/fork must prompt with the handoff message."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[5]
MOD = ROOT / "docs/system/workspace/scripts/runtime/agent_working.py"


class AcpHandoffTest(unittest.TestCase):
    def test_new_and_fork_prompt(self):
        if not MOD.exists():
            self.fail(f"missing module: {MOD}")
        spec = importlib.util.spec_from_file_location("agent_working", MOD)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertTrue(hasattr(mod, "_prompt_after_connect"), "missing _prompt_after_connect helper")


if __name__ == "__main__":
    unittest.main()
