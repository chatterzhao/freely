#!/usr/bin/env python3
"""Tests for the harness capability probe and cache telemetry reporter."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[5]
SCRIPT = ROOT / "docs/system/workspace/scripts/runtime/harness_status.py"


def write(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_project(tmp: pathlib.Path) -> None:
    write(tmp / ".freely/config.toml", 'AGENT_AI_TOOL_ADAPTER = "acp"\nFREELY_ACP_CLAUDE_BIN = "/usr/bin/true"\nFREELY_ACP_CODEX_BIN = "/usr/bin/true"\nFREELY_ACP_CLINE_BIN = "/usr/bin/true"\n')
    write(tmp / ".freely/agent-table.toml", '''
[[agents]]
role = "manager"
manager_id = "manager_01"
manager_slot = "claude-apikey-ds-flash-auto"
pool = 1

[[agents]]
role = "worker"
worker_id = "worker_01"
worker_slot = "codex-apikey-ds-flash-auto"
pool = 4

[[agents]]
role = "reviewer"
reviewer_id = "reviewer_01"
reviewer_slot = "cline-account-free-auto"
pool = 99
''')
    log = "".join([
        "[CACHE] session_id=a launch_kind=fresh prompt_bytes=100 input=100 cache_hit=0 cache_miss=0 output=0 total=100\n",
        "[CACHE] session_id=a launch_kind=fresh prompt_bytes=100 input=100 cache_hit=0 cache_miss=0 output=0 total=100\n",
        "[CACHE] session_id=b launch_kind=resume prompt_bytes=200 input=400 cache_hit=300 cache_miss=100 output=0 total=400\n",
    ])
    write(tmp / ".freely/logs/cycle-20260101-000001.log", log)
    write(tmp / ".freely/logs/cycle-20260101-000002.debug.log", "debug only\n")


class HarnessStatusTest(unittest.TestCase):
    def run_status(self, tmp: pathlib.Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--project", str(tmp), "--json", *args],
            capture_output=True, text=True, timeout=30,
        )

    def test_roles_capabilities_and_binaries(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            make_project(tmp)
            result = self.run_status(tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            roles = {r["role"]: r for r in data["roles"]}
            self.assertEqual(roles["manager"]["tool"], "claude")
            self.assertEqual(roles["manager"]["capabilities"]["fork"], "native")
            self.assertEqual(roles["worker"]["tool"], "codex")
            self.assertEqual(roles["worker"]["capabilities"]["fork"], "degraded")
            self.assertEqual(roles["reviewer"]["tool"], "cline")
            self.assertEqual(roles["manager"]["binary_status"], "ok")

    def test_cache_aggregation_deduplicates_consecutive_lines(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            make_project(tmp)
            data = json.loads(self.run_status(tmp).stdout)
            cache = data["cache"]
            self.assertEqual(cache["lines"], 3)
            self.assertEqual(cache["entries"], 2)
            self.assertEqual(cache["hit"], 300)
            self.assertEqual(cache["miss"], 100)
            self.assertEqual(cache["hit_rate"], 0.75)
            self.assertEqual(cache["by_kind"]["resume"]["hit"], 300)
            self.assertEqual(cache["input_source"], "usage")
            self.assertEqual(cache["usage_entries"], 2)
            self.assertEqual(cache["estimated_entries"], 0)

    def test_require_fork_fails_for_codex_worker(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            make_project(tmp)
            result = self.run_status(tmp, "--require", "fork")
            self.assertEqual(result.returncode, 3)
            data = json.loads(result.stdout)
            self.assertEqual(data["required"]["status"], "fail")
            self.assertEqual([(m["role"], m["capability"], m["reason"]) for m in data["required"]["missing"]], [("worker", "fork", "degraded"), ("reviewer", "fork", "degraded")])

    def test_missing_agent_table_is_a_warning_not_a_crash(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            write(tmp / ".freely/config.toml", 'AGENT_AI_TOOL_ADAPTER = "acp"\n')
            result = self.run_status(tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["roles"], [])
            self.assertTrue(any("agent-table" in w for w in data["warnings"]))

    def test_unknown_tool_is_reported_without_capabilities(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            write(tmp / ".freely/config.toml", 'AGENT_AI_TOOL_ADAPTER = "acp"\n')
            write(tmp / ".freely/agent-table.toml", '''
[[agents]]
role = "worker"
worker_id = "worker_01"
worker_slot = "mystery-apikey-x"
pool = 1
''')
            result = self.run_status(tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            role = data["roles"][0]
            self.assertEqual(role["tool"], "mystery")
            self.assertFalse(role["known"])
            self.assertEqual(role["capabilities"], {})
            self.assertTrue(any("unknown adapter" in w for w in data["warnings"]))

    def test_strict_fails_for_unknown_adapter(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            write(tmp / ".freely/config.toml", 'AGENT_AI_TOOL_ADAPTER = "acp"\n')
            write(tmp / ".freely/agent-table.toml", """
[[agents]]
role = "worker"
worker_id = "worker_01"
worker_slot = "mystery-apikey-x"
pool = 1
""")
            result = self.run_status(tmp, "--strict")
            self.assertEqual(result.returncode, 3)
            self.assertEqual(json.loads(result.stdout)["roles"][0]["binary_status"], "not_applicable")

    def test_require_without_roles_fails_closed(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = pathlib.Path(raw)
            write(tmp / ".freely/config.toml", 'AGENT_AI_TOOL_ADAPTER = "acp"\n')
            result = self.run_status(tmp, "--require", "fork")
            self.assertEqual(result.returncode, 3)
            data = json.loads(result.stdout)
            self.assertEqual(data["required"]["missing"][0]["reason"], "no_roles")


if __name__ == "__main__":
    unittest.main()
