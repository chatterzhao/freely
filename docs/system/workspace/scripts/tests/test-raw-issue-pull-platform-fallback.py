#!/usr/bin/env python3
"""AT-001 — raw-issue-pull must survive an unreadable platform.

RED contract (issue #4182):
  - pull_raw_issue() currently FATALs unless EVERY configured replica is ok
  - there is no --platform / --source-platform selection
  - unreadable platforms are not recorded as sync debt
  - partial success has no distinct exit code (3)

Pre-existing capabilities that MUST stay green in RED:
  - all replicas ok -> identical behaviour (primary = first configured platform)
  - all replicas unreadable -> still FATAL
  - materialization still carries an H1 and the caller's raw-key identity
"""
import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[5]
ADAPTER = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"
PULL_CLI = ROOT / "bin/raw-issue-pull"
WT_CREATE = ROOT / "docs/system/workspace/scripts/worktree/wt-create"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


KEY = "20261104T082549Z"

BODY = """---
schema_version: '1'
local_id: raw-20261104T082549Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids: {}
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-04T08:25:49Z'
updated_at: '2026-11-04T08:25:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

workflow_kind: fix

## Root cause

platform fallback fixture body.
"""


def _ok(platform, issue_id):
    return {
        "status": "ok", "raw_key": f"raw-{KEY}", "issue_id": issue_id,
        "url": f"https://example/{platform}/{issue_id}",
        "title": f"[RAW-{KEY}] fix: platform fallback fixture",
        "body": BODY, "state": "OPEN", "labels": [],
        "created_at": "2026-11-04T08:25:49Z", "updated_at": "2026-11-04T08:25:49Z",
    }


def _unknown(reason="transport_unavailable", error="502 proxy"):
    return {"status": "unknown", "reason": reason, "error": error}


class PullFallbackTests(unittest.TestCase):
    def setUp(self):
        self.adapter = _load("pa_fallback_under_test", ADAPTER)
        self.tmp = tempfile.TemporaryDirectory(prefix="freely-r6-")
        self.target = Path(self.tmp.name) / f"raw-{KEY}"
        self.patches = [
            mock.patch.object(self.adapter, "check_and_claim_assignee",
                              return_value=(True, "fixture: claimed")),
            mock.patch.object(self.adapter, "_update_issue_title", return_value=True),
            mock.patch.object(self.adapter, "configured_platforms",
                              return_value=["github", "gitee"]),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def _pull(self, replicas, **kwargs):
        # The legacy implementation prints the whole replica dict on FATAL;
        # keep the evidence log readable by capturing diagnostics.
        with mock.patch.object(self.adapter, "discover_raw_replicas", return_value=replicas), \
             contextlib.redirect_stderr(io.StringIO()):
            try:
                return self.adapter.pull_raw_issue(KEY, self.target, **kwargs)
            except TypeError as error:
                if "preferred_platform" in str(error):
                    self.fail(f"pull_raw_issue does not accept a platform selector: {error}")
                raise

    def test_all_ok_unchanged_preexisting(self):
        """PRE-EXISTING: both platforms readable -> primary stays github."""
        result = self._pull({"github": _ok("github", "4182"),
                             "gitee": _ok("gitee", "IKSWR9")})
        self.assertIsNotNone(result)
        self.assertEqual(result["platform"], "github")
        self.assertEqual(set(result["platform_ids"]), {"github", "gitee"})

    def test_all_unreadable_still_fatal_preexisting(self):
        """PRE-EXISTING: nothing readable -> must still fail closed."""
        result = self._pull({"github": _unknown(), "gitee": _unknown()})
        self.assertIsNone(result)

    def test_materialization_keeps_h1_and_identity_preexisting(self):
        """PRE-EXISTING (R2): the materialized file carries an H1."""
        result = self._pull({"github": _ok("github", "4182"),
                             "gitee": _ok("gitee", "IKSWR9")})
        self.assertIsNotNone(result)
        text = (self.target / "issue.md").read_text(encoding="utf-8")
        self.assertIn(f"raw-{KEY}", text)
        parts = text.split("---", 2)
        body = parts[2] if len(parts) >= 3 else text
        self.assertRegex(body, r"(?m)^#\s+\S")

    def test_partial_replica_still_materializes(self):
        """RED: github unreadable, gitee ok -> pull must still succeed."""
        result = self._pull({"github": _unknown(), "gitee": _ok("gitee", "IKSWR9")})
        self.assertIsNotNone(result, "pull FATALed on a single unreadable platform")
        self.assertTrue((self.target / "issue.md").is_file())

    def test_explicit_platform_selects_source(self):
        """RED: --platform gitee must read from gitee and write it back."""
        result = self._pull({"github": _ok("github", "4182"),
                             "gitee": _ok("gitee", "IKSWR9")},
                            preferred_platform="gitee")
        self.assertIsNotNone(result)
        self.assertEqual(result["platform"], "gitee")
        text = (self.target / "issue.md").read_text(encoding="utf-8")
        self.assertIn("primary_platform: gitee", text)

    def test_partial_platform_ids_exclude_unreadable(self):
        """RED: an unreadable replica has no issue_id -> must not poison platform_ids."""
        result = self._pull({"github": _unknown(), "gitee": _ok("gitee", "IKSWR9")})
        self.assertIsNotNone(result)
        self.assertNotIn("github", result["platform_ids"], result)
        self.assertEqual(result["platform_ids"]["gitee"]["issue_id"], "IKSWR9")

    def test_degraded_platforms_reported_for_sync_debt(self):
        """RED: caller must be able to record the unreadable platform as debt."""
        result = self._pull({"github": _unknown(), "gitee": _ok("gitee", "IKSWR9")})
        self.assertIsNotNone(result)
        self.assertEqual(result.get("degraded_platforms"), ["github"], result)

    def test_explicit_unreadable_platform_fails_closed(self):
        """RED: an explicitly requested but unreadable platform must not silently fall back."""
        result = self._pull({"github": _ok("github", "4182"), "gitee": _unknown()},
                            preferred_platform="gitee")
        self.assertIsNone(result)

    def test_cli_supports_platform_argument(self):
        """RED: bin/raw-issue-pull must accept --platform."""
        text = PULL_CLI.read_text(encoding="utf-8")
        self.assertIn("--platform", text)

    def test_wt_create_supports_source_platform_passthrough(self):
        """RED: wt-create must accept --source-platform and pass it through."""
        text = WT_CREATE.read_text(encoding="utf-8")
        self.assertIn("--source-platform", text)
        self.assertIn("source_platform", text)

    def test_partial_success_has_distinct_exit_code_3(self):
        """RED: partial success must be exit 3, not 1 (behaviour, not a string)."""
        import json
        import subprocess
        import shutil
        import textwrap

        with tempfile.TemporaryDirectory(prefix="freely-r6-cli-") as tmp:
            root = Path(tmp)
            cli = root / "bin" / "raw-issue-pull"
            adapter = root / "docs/system/workspace/scripts/sync/platform-adapter.py"
            debt = root / "docs/system/workspace/scripts/lifecycle/sync-debt.py"
            for path in (cli, adapter, debt):
                path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(PULL_CLI, cli)
            cli.chmod(0o755)
            # Fake adapter emits a partial-success document and exit 3.
            adapter.write_text(textwrap.dedent('''\
                import json, sys
                print(json.dumps({
                    "local_id": "raw-20261104T082549Z",
                    "platform": "gitee",
                    "degraded_platforms": ["github"],
                    "partial": True,
                }))
                raise SystemExit(3)
            '''), encoding="utf-8")
            shutil.copy(ROOT / "docs/system/workspace/scripts/lifecycle/sync-debt.py", debt)
            # No issue-sync binary: keep the fixture free of platform writes.
            target = root / "docs/B1-docs/raw-20261104T082549Z"
            target.mkdir(parents=True)
            subprocess.run(["git", "init", "-q", "-b", "develop"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "t@t"], cwd=root, check=True)
            (root / "seed").write_text("x", encoding="utf-8")
            subprocess.run(["git", "add", "seed"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)
            subprocess.run(["git", "checkout", "-q", "-b",
                            "fix/raw-20261104T082549Z-cli"], cwd=root, check=True)
            proc = subprocess.run(
                ["bash", str(cli), "--raw-key", KEY, "--target", str(target)],
                cwd=root, capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 3, proc.stderr)
            # STDOUT must be exactly one JSON document for wt-create.
            doc = json.loads(proc.stdout)
            self.assertEqual(doc["local_id"], f"raw-{KEY}")
            ledger = root / ".freely" / "state" / "sync-debt.json"
            self.assertTrue(ledger.is_file(), proc.stderr)
            entries = json.loads(ledger.read_text())["entries"]
            self.assertIn(f"{KEY}::github", entries, entries)
        adapter_text = ADAPTER.read_text(encoding="utf-8")
        self.assertIn("SystemExit(3)", adapter_text)

    def test_sync_debt_reuses_existing_ledger(self):
        """RED: pull must record debt in the existing sync-debt ledger."""
        text = PULL_CLI.read_text(encoding="utf-8")
        self.assertIn("sync-debt.py", text)
        self.assertIn("record", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
