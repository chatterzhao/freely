---
local_id: I-20260617T110109Z-A
kind: linked
status: in_dev
phase_state: completed
source_candidate: docs/B1-docs/raw-20260617T110109Z/candidates.md
promoted_from: raw-20260617T110109Z
verification_artifact_dir: docs/epics/remove-prompt-file/code-reviews
platform_ids:
  github:
    issue_id: '2940'
    url: https://github.com/chatterzhao/freely/issues/2940
    synced_at: '2026-06-17T16:53:37Z'
updated_at: '2026-06-17T16:53:37Z'
primary_platform: github
created_at: '2026-06-17T16:53:37Z'
platform_state: closed
---
# I-20260617T110109Z-A: Remove prompt_file from A2A
A2A needs Message, not files. prompt_file path now derived from task_id at Runtime.
