#!/usr/bin/env python3
import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[5]
SCANNER = ROOT / "docs/system/workspace/scripts/runtime/task-lifecycle-scan.py"
MIGRATE = ROOT / "bin/migrate-issue-phase-state"
BATCH = ROOT / "bin/batch-closeout-raw-issues"
PRE_SCAN = ROOT / "docs/system/workspace/scripts/runtime/pre-scan-fix.sh"
GATE = ROOT / "docs/system/workspace/scripts/quality/governance-merge-gate"


def load_scanner():
    spec = importlib.util.spec_from_file_location("task_lifecycle_scan", SCANNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LifecycleConsumerBoundaryTests(unittest.TestCase):
    def test_raw_and_linked_terminal_domains_are_separate(self):
        scanner = load_scanner()
        self.assertEqual(scanner.RAW_TERMINAL_PHASES, {"absorbed", "dropped"})
        self.assertIn("completed", scanner.LINKED_TERMINAL_PHASES)
        self.assertNotIn("completed", scanner.RAW_TERMINAL_PHASES)

    def test_scanner_rejects_legacy_absorbed_without_relationship(self):
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            issue_file = project / "docs/B1-docs/raw-20260721T223133Z/issue.md"
            issue_file.parent.mkdir(parents=True)
            issue_file.write_text(
                "---\nlocal_id: raw-20260721T223133Z\nkind: raw\n"
                "phase_state: absorbed\nplatform_ids: {}\n---\n",
                encoding="utf-8",
            )
            issues = scanner.read_issues_dir(project)
        self.assertEqual(len(issues), 1)
        self.assertIn("canonical id or path", issues[0]["metadata_validation_error"])

    def test_scanner_accepts_legacy_absorbed_with_project_relative_path(self):
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            canonical = project / "docs/B2-docs/example/issues/I-20260721T223133Z-A.md"
            canonical.parent.mkdir(parents=True)
            canonical.write_text("# issue\n", encoding="utf-8")
            issue_file = project / "docs/B1-docs/raw-20260721T223133Z/issue.md"
            issue_file.parent.mkdir(parents=True)
            issue_file.write_text(
                "---\nlocal_id: raw-20260721T223133Z\nkind: raw\n"
                "phase_state: absorbed\nabsorbed_into: ''\n"
                "canonical_issue_path: docs/B2-docs/example/issues/I-20260721T223133Z-A.md\n"
                "platform_ids: {}\n---\n",
                encoding="utf-8",
            )
            issues = scanner.read_issues_dir(project)
        self.assertEqual(issues[0]["metadata_validation_error"], "")

    def test_legacy_migration_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            lifecycle = project / "docs/system/workspace/scripts/lifecycle"
            lifecycle.mkdir(parents=True)
            lifecycle.joinpath("raw_metadata_contract.py").write_bytes(
                (ROOT / "docs/system/workspace/scripts/lifecycle/raw_metadata_contract.py").read_bytes()
            )
            issue_file = project / "docs/B1-docs/raw-legacy/issue.md"
            issue_file.parent.mkdir(parents=True)
            issue_file.write_text(
                "---\nlocal_id: raw-legacy\nkind: raw\nstatus: proposed\nplatform_ids: {}\n---\n",
                encoding="utf-8",
            )
            before = digest(issue_file)
            result = subprocess.run(
                ["python3", str(MIGRATE), str(project)],
                capture_output=True,
                text=True,
                check=True,
            )
            after = digest(issue_file)
        self.assertEqual(before, after)
        self.assertIn("0 files changed", result.stdout)

    def test_audit_entries_contain_no_lifecycle_mutation_or_platform_cli(self):
        for path in (BATCH, PRE_SCAN, MIGRATE):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn("gh issue", text)
                self.assertNotIn("git commit", text)
                self.assertNotIn("pr-create-guarded", text)
                self.assertNotIn("write_text(", text)

    def test_merge_gate_accepts_either_canonical_relationship(self):
        text = GATE.read_text(encoding="utf-8")
        self.assertIn('raw_grab("absorbed_into")', text)
        self.assertIn('raw_grab("canonical_issue_path")', text)
        self.assertIn("if not target_valid and not canonical_valid", text)

    def test_adapter_failure_is_degraded_not_empty_platform_list(self):
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            with mock.patch.dict(sys.modules, {"platform_adapter": None}):
                platform_issues = scanner.get_platform_open_issues(project)
        self.assertNotEqual(platform_issues, {})
        self.assertIn("__degraded__", platform_issues)


if __name__ == "__main__":
    unittest.main()
