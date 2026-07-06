---
local_id: I-20260516T094405Z-A
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
promoted_from: raw-20260516T094405Z05Z
source_candidate: docs/B1-docs/raw-20260516T094405Z05Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '2605'
    url: https://github.com/chatterzhao/freely/issues/2605
    synced_at: '2026-06-13T10:46:21Z'
primary_platform: github
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T09:44:05Z'
updated_at: '2026-06-13T10:46:21Z'
intake_id: ''
author: manager
channel: direct-absorption
session_refs: []
pre_tests_path: ''
verification_artifact_dir: ''
platform_state: closed
---

# I-20260516T094405Z-A: delegate_workers 被 exclusive_fields_conflict 拒绝

Runtime bug fix absorbed directly into develop via fix/raw-20260516T014923Z* worktree.

Changes: validate_manager_exit_contract_for_project — stop_reason should only be read for exit_kind=stop_ai.
