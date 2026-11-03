#!/usr/bin/env python3
"""RED/GREEN tests: handoff first-message delivery and liveness tri-state."""
import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[5]
RUNTIME = ROOT / "docs/system/workspace/scripts/runtime"
AGENTS = ROOT / "docs/system/workspace/scripts/agents"
AW = RUNTIME / "agent_working.py"
WD = RUNTIME / "watchdog_sse.py"


def load(name: str, path: pathlib.Path):
    # agent_working is shared so watchdog's `from agent_working import ...`
    # sees the same patched instance; other modules load fresh per test.
    if name == "agent_working" and name in sys.modules:
        return sys.modules[name]
    if not path.exists():
        raise AssertionError(f"missing module: {path}")
    sys.path.insert(0, str(RUNTIME))
    sys.path.insert(0, str(AGENTS))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class HandoffRuntimeTest(unittest.TestCase):
    def test_new_session_prompts_first_message(self):
        mod = load("agent_working", AW)
        calls = []

        def fake_bridge(project, base_tool, method, params):
            calls.append((method, params))
            if method == "session/new":
                return {"sessionId": "ses_new"}
            return {"ok": True}

        def fake_db(project, method, params, timeout=5.0):
            if method == "agent_working.get_session":
                return {"session_id": ""}
            if method == "agent_working.upsert":
                return {"ok": True}
            return {"row": {}}

        mod._acp_bridge_call = fake_bridge
        mod._db_rpc = fake_db
        sid, op = mod.acp_session_connect(
            "/tmp/handoff-test", "raw-test", "worker", "worker_01",
            "opencode-apikey-test", message="do the work",
        )
        self.assertEqual(op, "new")
        self.assertEqual([c[0] for c in calls], ["session/new", "session/prompt"])
        prompt = calls[1][1]["prompt"]
        self.assertIn("[role:worker]", prompt)
        self.assertIn("do the work", prompt)

    def test_session_state_alive_dead_unknown(self):
        mod = load("watchdog_sse", WD)
        mod._get_agent_slot = lambda project, role, agent_id: "opencode-apikey-test"
        sid = "ses_live"

        mod._acp_rpc = lambda project, method, params, base_tool="": {"result": {"ok": True}}
        self.assertEqual(mod._session_state("/tmp/p", "worker", "worker_01", sid), "alive")

        mod._acp_rpc = lambda project, method, params, base_tool="": {
            "error": {"code": -32000, "message": "session not found"}
        }
        self.assertEqual(mod._session_state("/tmp/p", "worker", "worker_01", sid), "dead")

        mod._acp_rpc = lambda project, method, params, base_tool="": None
        self.assertEqual(mod._session_state("/tmp/p", "worker", "worker_01", sid), "unknown")

    def test_liveness_keeps_alive_binding(self):
        aw = load("agent_working", AW)
        wd = load("watchdog_sse", WD)
        upserts = []

        def fake_db(project, method, params, timeout=5.0):
            if method == "agent_working.get_all":
                return {"rows": [{
                    "raw_key": "raw-test",
                    "worker_id": "worker_01:ses_live",
                    "reviewer_id": "",
                    "manager_id": "",
                }]}
            if method == "agent_working.upsert":
                upserts.append(params)
                return {"ok": True}
            return {"row": {}}

        aw._db_rpc = fake_db
        wd._session_state = lambda project, role, agent_id, session_id: "alive"
        wd._check_agent_liveness("/tmp/p")
        self.assertEqual(upserts, [], "alive session must not be cleared")

        upserts.clear()
        wd._session_state = lambda project, role, agent_id, session_id: "dead"
        wd._check_agent_liveness("/tmp/p")
        self.assertEqual(len(upserts), 1, "dead session must be cleared once")
        self.assertEqual(upserts[0]["val"], "worker_01")


if __name__ == "__main__":
    unittest.main()
