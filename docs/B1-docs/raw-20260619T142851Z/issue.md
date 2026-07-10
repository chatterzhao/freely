---
local_id: raw-20260619T142851Z51Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T142851Z-A
platform_ids:
  github:
    issue_id: '3088'
    url: https://github.com/chatterzhao/freely/issues/3088
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T14:29:08Z'
updated_at: '2026-06-19T14:29:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## Root cause

parse_a2a_task_json_reply line 14548-14553: state=submitted only returns delegate_workers
when worker_prompts_csv is non-empty. But the Manager creates individual A2A worker tasks
(not CSV prompt files). worker_prompts_csv is always empty → _exit_kind defaults to
resume_manager → supervisor loop never enters the worker launch block.

manager_exit_contract_kind uses a different check (list --role worker --status pending)
and correctly returns delegate_workers.

## Fix

In parse_a2a_task_json_reply, add a fallback check for submitted worker tasks when
worker_prompts_csv is empty, mirroring manager_exit_contract_kind logic.
