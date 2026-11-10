#!/usr/bin/env python3
import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "docs/system/workspace/scripts/lifecycle/raw_metadata_contract.py"
ISSUE_SYNC = ROOT / "bin/issue-sync"

def issue_sync_functions_source() -> str:
    """Everything bin/issue-sync defines, without running main().

    #4286: the entry point is a dispatcher; its subcommands live in
    bin/issue-sync.d/*.sh. Concatenating the modules with the entry point
    (minus the module loader and the dispatch guard) gives the test the same
    function set a sourced entry point has.
    """
    entry = ISSUE_SYNC.read_text(encoding="utf-8")
    # The entry point's loader resolves issue-sync.d next to itself; the
    # functions file lives in a sandbox, so append the modules instead.
    entry = entry.replace("\n_issue_sync_load_modules\n", "\n")
    modules = [path.read_text(encoding="utf-8")
               for path in sorted((ROOT / "bin" / "issue-sync.d").glob("*.sh"))]
    return entry + "\n" + "\n".join(modules)




def load_contract():
    spec = importlib.util.spec_from_file_location("raw_metadata_contract", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RawMetadataContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = load_contract()
        self.base = self.contract.new_raw_metadata(
            local_id="raw-20260721T223133Z",
            platform_ids={
                "github": {
                    "issue_id": "4070",
                    "url": "https://example.test/issues/4070",
                    "synced_at": "",
                }
            },
            primary_platform="github",
            created_at="2026-07-21T22:31:56Z",
            updated_at="2026-07-21T22:31:56Z",
            author="platform",
            channel="github",
        )

    def test_feedback_initializes_complete_schema_with_explicit_values(self):
        self.assertEqual(list(self.base), list(self.contract.RAW_METADATA_FIELDS))
        self.assertEqual(
            self.base,
            {
                "schema_version": self.contract.SCHEMA_VERSION,
                "local_id": "raw-20260721T223133Z",
                "kind": "raw",
                "phase_state": "proposed",
                "absorbed_into": "",
                "platform_ids": {
                    "github": {
                        "issue_id": "4070",
                        "url": "https://example.test/issues/4070",
                        "synced_at": "",
                    }
                },
                "primary_platform": "github",
                "canonical_issue_path": "",
                "last_synced_comment_at": {},
                "hash": "",
                "created_at": "2026-07-21T22:31:56Z",
                "updated_at": "2026-07-21T22:31:56Z",
                "intake_id": "",
                "author": "platform",
                "channel": "github",
                "session_refs": [],
                "platform_state": "open",
                "promoted_children": [],
                "source_candidate": "",
                "completed_at": "",
                "closeout_note": "",
            },
        )
        self.contract.validate(self.base)

    def test_worktree_created_changes_no_metadata(self):
        transitioned = self.contract.transition(self.base, "worktree_created")
        self.assertEqual(transitioned, self.base)
        self.assertEqual(list(transitioned), list(self.base))

    def test_promotion_records_child_before_final_absorption(self):
        started = self.contract.transition(
            self.base,
            "promotion_started",
            issue_id="I-20260721T223133Z-A",
            source_candidate="docs/B1-docs/raw-20260721T223133Z/candidates.md#C-A",
            at="2026-07-21T23:00:00Z",
        )
        self.assertEqual(started["phase_state"], "proposed")
        self.assertEqual(started["promoted_children"], ["I-20260721T223133Z-A"])
        with tempfile.TemporaryDirectory() as directory:
            issue_path = Path(directory) / "I-20260721T223133Z-A.md"
            issue_path.write_text("# canonical\n", encoding="utf-8")
            transitioned = self.contract.transition(
                started,
                "promotion_finalized",
                issue_id="I-20260721T223133Z-A",
                issue_path=issue_path.name,
                at="2026-07-22T00:00:00Z",
                base_dir=directory,
            )
            retried = self.contract.transition(
                transitioned,
                "promotion_finalized",
                issue_id="I-20260721T223133Z-A",
                issue_path=issue_path.name,
                at="2026-07-22T00:05:00Z",
                base_dir=directory,
            )
        self.assertEqual(list(transitioned), list(self.base))
        self.assertEqual(transitioned["phase_state"], "absorbed")
        self.assertEqual(transitioned["absorbed_into"], "I-20260721T223133Z-A")
        self.assertEqual(transitioned["canonical_issue_path"], issue_path.name)
        self.assertEqual(transitioned["updated_at"], "2026-07-22T00:00:00Z")
        self.assertEqual(retried, transitioned)

    def test_transition_issue_writes_atomically_without_reordering_or_body_loss(self):
        with tempfile.TemporaryDirectory() as directory:
            issue_file = Path(directory) / "issue.md"
            body = "\n\nworkflow_kind: fix\n\n## 问题\n保留正文。\n"
            self.contract.write_issue(issue_file, self.base, body)
            before_inode = issue_file.stat().st_ino
            updated = self.contract.transition_issue(
                issue_file,
                "promotion_started",
                issue_id="I-20260721T223133Z-A",
                at="2026-07-21T23:00:00Z",
            )
            persisted, persisted_body = self.contract.read_issue(issue_file)
            after_inode = issue_file.stat().st_ino
        self.assertEqual(persisted, updated)
        self.assertEqual(list(persisted), list(self.contract.RAW_METADATA_FIELDS))
        self.assertEqual(persisted_body, body)
        self.assertNotEqual(after_inode, before_inode)

    def test_issue_sync_promote_and_finalize_follow_two_stage_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            sandbox = Path(directory)
            raw_id = "raw-20260721T223133Z"
            child_id = "I-20260721T223133Z-A"
            raw_file = sandbox / "docs/B1-docs" / raw_id / "issue.md"
            child_file = sandbox / "docs/B2-docs/example/issues" / f"{child_id}.md"
            raw_file.parent.mkdir(parents=True)
            child_file.parent.mkdir(parents=True)
            child_file.write_text("# canonical\n", encoding="utf-8")
            self.contract.write_issue(raw_file, self.base, "\n\n## 问题\n命令级状态流。\n")

            source = issue_sync_functions_source()
            source_file = sandbox / "issue-sync-functions.sh"
            source_file.write_text(source, encoding="utf-8")
            script = r'''
set -euo pipefail
source "$SOURCE_FILE"
ROOT_DIR="$SANDBOX"
# The copied functions file lives outside docs/, so pin the single-owner CLI
# explicitly (#4148) — otherwise every _fm_* write silently no-ops here.
_FM_CLI="$CONTRACT_ROOT/docs/system/workspace/scripts/lifecycle/frontmatter_contract_cli.py"
RAW_METADATA_CONTRACT_ROOT="$CONTRACT_ROOT"
ISSUES_DIR="$SANDBOX/docs/B1-docs"
find() { printf '%s\n' "$CHILD_FILE"; }
cmd_create() { :; }
cmd_comment() { :; }
cmd_close() {
  local file="$ISSUES_DIR/$1/issue.md"
  [[ "$(_fm_get "$file" phase_state)" == "absorbed" ]]
  local at; at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  _raw_transition_if_strict "$file" platform_closed "" "" "" "$at"
}
cmd_promote "$RAW_ID" "$CHILD_ID"
[[ "$(_fm_get "$RAW_FILE" phase_state)" == "proposed" ]]
cmd_promote_finalize "$RAW_ID"
'''
            env = dict(os.environ)
            env.update(
                SOURCE_FILE=str(source_file),
                CONTRACT_ROOT=str(ROOT),
                SANDBOX=str(sandbox),
                CHILD_FILE=str(child_file),
                RAW_ID=raw_id,
                CHILD_ID=child_id,
                RAW_FILE=str(raw_file),
            )
            result = subprocess.run(
                ["bash", "-c", script], env=env, capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            metadata, body = self.contract.read_issue(raw_file)
        self.assertEqual(metadata["phase_state"], "absorbed")
        self.assertEqual(metadata["platform_state"], "closed")
        self.assertEqual(metadata["promoted_children"], [child_id])
        self.assertEqual(metadata["absorbed_into"], child_id)
        self.assertEqual(
            metadata["canonical_issue_path"],
            "docs/B2-docs/example/issues/I-20260721T223133Z-A.md",
        )
        self.assertEqual(body.count("event: promote_finalized"), 1)

    def test_issue_sync_close_commits_state_only_after_all_platforms_close(self):
        with tempfile.TemporaryDirectory() as directory:
            sandbox = Path(directory)
            raw_id = "raw-20260721T223133Z"
            raw_file = sandbox / "docs/B1-docs" / raw_id / "issue.md"
            adapter = sandbox / "docs/system/workspace/scripts/sync/platform-adapter.py"
            raw_file.parent.mkdir(parents=True)
            adapter.parent.mkdir(parents=True)
            absorbed = dict(
                self.base,
                phase_state="absorbed",
                absorbed_into="I-20260721T223133Z-A",
                completed_at="2026-07-22T00:00:00Z",
            )
            self.contract.write_issue(raw_file, absorbed, "\n\n## 问题\n平台关闭聚合。\n")
            adapter.write_text(
                # Faithful to the real adapter contract: close-multi prints
                # per-platform results, and the exit code is 0/3/1 (#4184).
                "#!/usr/bin/env python3\n"
                "import json, os\n"
                "rc = int(os.environ['FAKE_CLOSE_RC'])\n"
                "status = 'closed' if rc == 0 else 'error'\n"
                "print(json.dumps({'github': {'status': status}}))\n"
                "raise SystemExit(rc)\n",
                encoding="utf-8",
            )

            source = issue_sync_functions_source()
            source_file = sandbox / "issue-sync-functions.sh"
            source_file.write_text(source, encoding="utf-8")
            script = r'''
set -euo pipefail
source "$SOURCE_FILE"
ROOT_DIR="$SANDBOX"
# The copied functions file lives outside docs/, so pin the single-owner CLI
# explicitly (#4148) — otherwise every _fm_* write silently no-ops here.
_FM_CLI="$CONTRACT_ROOT/docs/system/workspace/scripts/lifecycle/frontmatter_contract_cli.py"
RAW_METADATA_CONTRACT_ROOT="$CONTRACT_ROOT"
ISSUES_DIR="$SANDBOX/docs/B1-docs"
cmd_close "$RAW_ID"
'''
            env = dict(os.environ)
            env.update(
                SOURCE_FILE=str(source_file),
                CONTRACT_ROOT=str(ROOT),
                SANDBOX=str(sandbox),
                RAW_ID=raw_id,
                FAKE_CLOSE_RC="1",
            )
            failed = subprocess.run(
                ["bash", "-c", script], env=env, capture_output=True, text=True
            )
            after_failure, _ = self.contract.read_issue(raw_file)
            self.assertNotEqual(failed.returncode, 0)
            self.assertEqual(after_failure["platform_state"], "open")

            env["FAKE_CLOSE_RC"] = "0"
            succeeded = subprocess.run(
                ["bash", "-c", script], env=env, capture_output=True, text=True
            )
            after_success, _ = self.contract.read_issue(raw_file)
        self.assertEqual(succeeded.returncode, 0, succeeded.stdout + succeeded.stderr)
        self.assertEqual(after_success["platform_state"], "closed")

    def test_each_stage_changes_only_its_owned_values(self):
        with tempfile.TemporaryDirectory() as directory:
            issue_path = Path(directory) / "I-20260721T223133Z-A.md"
            issue_path.write_text("# canonical\n", encoding="utf-8")
            started = self.contract.transition(
                self.base,
                "promotion_started",
                issue_id="I-20260721T223133Z-A",
                at="2026-07-21T23:00:00Z",
            )
            promoted = self.contract.transition(
                started,
                "promotion_finalized",
                issue_id="I-20260721T223133Z-A",
                issue_path=issue_path.name,
                at="2026-07-22T00:00:00Z",
                base_dir=directory,
            )
            closed = self.contract.transition(
                promoted,
                "platform_closed",
                at="2026-07-22T01:00:00Z",
                base_dir=directory,
            )
        self.assertEqual(list(promoted), list(self.base))
        self.assertEqual(list(closed), list(self.base))
        self.assertEqual(promoted["platform_state"], "open")
        self.assertEqual(closed["phase_state"], "absorbed")
        self.assertEqual(closed["absorbed_into"], "I-20260721T223133Z-A")
        self.assertEqual(closed["platform_state"], "closed")
        self.assertEqual(closed["completed_at"], "2026-07-22T00:00:00Z")
        self.assertEqual(closed["updated_at"], "2026-07-22T01:00:00Z")

    def test_drop_and_close_are_separate_valid_transitions(self):
        dropped = self.contract.transition(
            self.base,
            "dropped",
            reason="superseded by canonical scope",
            at="2026-07-22T00:00:00Z",
        )
        self.assertEqual(dropped["phase_state"], "dropped")
        self.assertEqual(dropped["platform_state"], "open")
        self.assertEqual(dropped["completed_at"], "2026-07-22T00:00:00Z")
        self.assertEqual(dropped["closeout_note"], "superseded by canonical scope")
        closed = self.contract.transition(
            dropped,
            "platform_closed",
            at="2026-07-22T01:00:00Z",
        )
        self.assertEqual(closed["phase_state"], "dropped")
        self.assertEqual(closed["platform_state"], "closed")

    def test_illegal_stage_order_fails_closed(self):
        with self.assertRaises(self.contract.MetadataValidationError):
            self.contract.transition(
                self.base,
                "platform_closed",
                at="2026-07-22T00:00:00Z",
            )

    def test_strict_schema_rejects_illegal_cross_field_combinations(self):
        cases = []
        proposed_with_target = dict(self.base, absorbed_into="I-20260721T223133Z-A")
        cases.append(proposed_with_target)
        absorbed_without_target = dict(self.base, phase_state="absorbed")
        cases.append(absorbed_without_target)
        dropped_without_closeout = dict(self.base, phase_state="dropped")
        cases.append(dropped_without_closeout)
        for metadata in cases:
            with self.subTest(metadata=metadata):
                with self.assertRaises(self.contract.MetadataValidationError):
                    self.contract.validate(metadata)

    def test_absorbed_accepts_either_verifiable_canonical_relation(self):
        by_id = dict(
            self.base,
            phase_state="absorbed",
            absorbed_into="I-20260721T223133Z-A",
            completed_at="2026-07-22T00:00:00Z",
        )
        self.contract.validate(by_id)
        with tempfile.TemporaryDirectory() as directory:
            issue_path = Path(directory) / "I-20260721T223133Z-A.md"
            issue_path.write_text("# canonical\n", encoding="utf-8")
            by_path = dict(
                self.base,
                phase_state="absorbed",
                canonical_issue_path=issue_path.name,
                completed_at="2026-07-22T00:00:00Z",
            )
            self.contract.validate(by_path, base_dir=directory)

    def test_strict_schema_rejects_missing_or_reordered_fields(self):
        missing = dict(self.base)
        missing.pop("closeout_note")
        with self.assertRaises(self.contract.MetadataValidationError):
            self.contract.validate(missing)
        reordered = {key: self.base[key] for key in reversed(self.base)}
        with self.assertRaises(self.contract.MetadataValidationError):
            self.contract.validate(reordered)

    def test_legacy_is_normalized_without_rewrite(self):
        legacy = {
            "local_id": "raw-legacy",
            "kind": "raw",
            "status": "proposed",
            "platform_ids": {},
        }
        before = yaml.safe_dump(legacy, sort_keys=False)
        normalized = self.contract.normalize(legacy)
        after = yaml.safe_dump(legacy, sort_keys=False)
        self.assertEqual(before, after)
        self.assertEqual(normalized["phase_state"], "proposed")
        self.assertFalse(normalized["strict_schema"])


if __name__ == "__main__":
    unittest.main()
