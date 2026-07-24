#!/usr/bin/env python3
import importlib.util
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "docs/system/workspace/scripts/sync/pr_lifecycle.py"
ADAPTER = ROOT / "docs/system/workspace/scripts/sync/platform-adapter.py"


def load_lifecycle():
    spec = importlib.util.spec_from_file_location("pr_lifecycle", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_adapter():
    spec = importlib.util.spec_from_file_location("platform_adapter", ADAPTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeHandler:
    def __init__(self, name, remote_head):
        self.name = name
        self.remote_head = remote_head
        self.effects = []

    def remote_name(self):
        return self.name

    def fetch_branch_head(self, _branch):
        return self.remote_head

    def push_branch(self, _branch):
        self.effects.append("push")
        self.remote_head = "local"
        return {"status": "pushed", "remote": self.name}

    def ensure_pr(self, *_args):
        self.effects.append("ensure_pr")
        return {"status": "reused", "number": "1"}


class PrLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.lifecycle = load_lifecycle()

    def test_classifies_all_remote_relations(self):
        ancestor_pairs = {
            ("remote-behind", "local"): True,
            ("local", "remote-ahead"): True,
        }

        def is_ancestor(left, right):
            return ancestor_pairs.get((left, right), False)

        cases = [
            ("local", None, "absent"),
            ("local", "remote-behind", "behind"),
            ("local", "local", "equal"),
            ("local", "remote-ahead", "ahead"),
            ("local", "remote-diverged", "diverged"),
        ]
        for local, remote, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(
                    self.lifecycle.classify_branch(local, remote, is_ancestor), expected
                )

    def test_plan_requires_all_configured_platforms_safe_before_push(self):
        observations = {
            "github": {"branch_state": "behind"},
            "gitee": {"branch_state": "diverged"},
        }
        plan = self.lifecycle.plan_platform_updates(
            configured_platforms=["github", "gitee"],
            observations=observations,
        )
        self.assertFalse(plan["safe_to_execute"])
        self.assertEqual(plan["actions"], [])
        self.assertEqual(plan["platforms"]["github"]["action"], "blocked_by_aggregate")
        self.assertEqual(plan["platforms"]["gitee"]["action"], "fail_closed")

    def test_plan_maps_safe_states_to_deterministic_actions(self):
        plan = self.lifecycle.plan_platform_updates(
            configured_platforms=["github", "gitee", "gitlab"],
            observations={
                "github": {"branch_state": "absent"},
                "gitee": {"branch_state": "behind"},
                "gitlab": {"branch_state": "equal"},
            },
        )
        self.assertTrue(plan["safe_to_execute"])
        self.assertEqual(
            plan["actions"],
            [
                {"platform": "github", "action": "push_then_ensure_pr"},
                {"platform": "gitee", "action": "push_then_ensure_pr"},
                {"platform": "gitlab", "action": "ensure_pr"},
            ],
        )

    def test_pr_create_updates_platforms_before_merge_dry_run(self):
        script = (
            ROOT
            / "docs/system/workspace/scripts/worktree/pr-create-guarded"
        ).read_text(encoding="utf-8")
        adapter_update = script.index('guarded-pr-update "$current_branch"')
        merge_dry_run = script.index(
            'pr-merge-guarded" --dry-run "$base" "$current_branch"'
        )
        self.assertLess(adapter_update, merge_dry_run)

    def test_configured_platforms_come_from_project_config_without_registry_fallback(self):
        adapter = load_adapter()
        with patch.dict(os.environ, {}, clear=True), patch.object(
            adapter, "read_config", return_value={"FREELY_REPO_PLATFORMS": "gitee,github,gitee"}
        ), patch.object(
            adapter.subprocess,
            "run",
            return_value=SimpleNamespace(returncode=0, stdout=str(ROOT), stderr=""),
        ):
            self.assertEqual(adapter.configured_platforms(), ["gitee", "github"])
        with patch.dict(os.environ, {}, clear=True), patch.object(
            adapter, "read_config", return_value={}
        ), patch.object(
            adapter.subprocess,
            "run",
            return_value=SimpleNamespace(returncode=0, stdout=str(ROOT), stderr=""),
        ):
            self.assertEqual(adapter.configured_platforms(), [])

    def test_issue_mutations_report_every_configured_platform(self):
        adapter = load_adapter()
        github = SimpleNamespace(
            create_issue=lambda *_: {"status": "created", "issue_id": "1"},
            update_issue=lambda *_: {"status": "updated"},
        )

        def handler_for(platform):
            return github if platform == "github" else None

        with patch.object(
            adapter, "configured_platforms", return_value=["github", "gitee"]
        ), patch.object(adapter, "_handler_for", side_effect=handler_for):
            created = adapter.create_issue("raw-key", "title", "body")
            updated = adapter.update_issue(
                "raw-key",
                {"github": {"issue_id": "1"}, "gitee": {"issue_id": "2"}},
                title="title",
            )
        self.assertEqual(created["github"]["status"], "created")
        self.assertEqual(created["gitee"]["status"], "error")
        self.assertEqual(updated["github"]["status"], "updated")
        self.assertEqual(updated["gitee"]["status"], "error")

    def test_guarded_update_has_no_effect_when_any_platform_is_unsafe(self):
        adapter = load_adapter()
        handlers = {
            "github": FakeHandler("github", "remote-behind"),
            "gitee": FakeHandler("gitee", "remote-diverged"),
        }

        def run(args, **_kwargs):
            if args[:2] == ["git", "rev-parse"]:
                return SimpleNamespace(returncode=0, stdout="local\n", stderr="")
            if args[:3] == ["git", "merge-base", "--is-ancestor"]:
                pair = tuple(args[3:])
                return SimpleNamespace(
                    returncode=0 if pair == ("remote-behind", "local") else 1,
                    stdout="",
                    stderr="",
                )
            raise AssertionError(args)

        with patch.object(adapter, "configured_platforms", return_value=list(handlers)), patch.object(
            adapter, "_handler_for", side_effect=handlers.get
        ), patch.object(adapter.subprocess, "run", side_effect=run):
            result = adapter.guarded_pr_update("branch", title="title", body="body")
        self.assertFalse(result["success"])
        self.assertEqual(handlers["github"].effects, [])
        self.assertEqual(handlers["gitee"].effects, [])

    def test_guarded_update_pushes_behind_then_reuses_existing_pr(self):
        adapter = load_adapter()
        handler = FakeHandler("github", "remote-behind")

        def run(args, **_kwargs):
            if args[:2] == ["git", "rev-parse"]:
                return SimpleNamespace(returncode=0, stdout="local\n", stderr="")
            if args[:3] == ["git", "merge-base", "--is-ancestor"]:
                return SimpleNamespace(
                    returncode=0
                    if tuple(args[3:]) == ("remote-behind", "local")
                    else 1,
                    stdout="",
                    stderr="",
                )
            raise AssertionError(args)

        with patch.object(adapter, "configured_platforms", return_value=["github"]), patch.object(
            adapter, "_handler_for", return_value=handler
        ), patch.object(adapter.subprocess, "run", side_effect=run):
            result = adapter.guarded_pr_update("branch", title="title", body="body")
        self.assertTrue(result["success"])
        self.assertEqual(handler.effects, ["push", "ensure_pr"])
        self.assertEqual(result["platforms"]["github"]["branch_state"], "equal")
        self.assertEqual(result["platforms"]["github"]["pr_state"], "reused")

    def test_aggregate_accepts_only_equal_branch_and_pr_success(self):
        success = self.lifecycle.aggregate_results(
            ["github", "gitee"],
            {
                "github": {"branch_state": "equal", "pr_state": "reused"},
                "gitee": {"branch_state": "equal", "pr_state": "updated"},
            },
        )
        self.assertTrue(success["success"])
        for bad_state in ("skipped", "error", "unsupported"):
            with self.subTest(bad_state=bad_state):
                failed = self.lifecycle.aggregate_results(
                    ["github", "gitee"],
                    {
                        "github": {"branch_state": "equal", "pr_state": "created"},
                        "gitee": {"branch_state": "equal", "pr_state": bad_state},
                    },
                )
                self.assertFalse(failed["success"])


if __name__ == "__main__":
    unittest.main()
