---
schema_version: '1'
local_id: raw-20260807T120649Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4108'
    url: https://github.com/chatterzhao/freely/issues/4108
    synced_at: ''
  gitee:
    issue_id: IK7894
    url: https://gitee.com/zhaoquan/freely/issues/IK7894
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T12:06:49Z'
updated_at: '2026-08-07T12:07:22Z'
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

## Symptom
Manager delegations via a2a-exit --state submitted --role worker with full verification metadata still result in the worktree being marked manager_worker_launch_verification_blocked. The worker DOES launch and runs correctly (run-acp-prompt.py process active, B1/B2/dev commits produced), but:
- .freely/run/worker-verification-contract.env is written as a stub (VERIFICATION_METADATA_PRESENT=false, all fields empty)
- workcell-state.env ends with DESIRED_RUNTIME_STATE=stopped + LAST_EXIT_REASON=manager_worker_launch_verification_blocked
- watchdog_sse.py then false-flags the worker as DEAD and clears its session binding in agent_working

## Root cause
docs/system/workspace/scripts/runtime/consume_worker_tasks.py flattens the task message:
    msg = msg.replace('\n', ' ').replace('\r', '')
The worker prompt verification metadata parser (worker_prompt_dispatch_metadata_value / worker_prompt_dispatch_metadata_csv in runtime/freely) is line-oriented: it does split(line, parts, ':') and normalizes parts[1] as the key. When the whole summary (including Owner-Issue:/Pre-Tests-Path:/Required-Test-Lanes:/Closeout-*:) is collapsed onto ONE line, the first colon belongs to the prose preamble, so no metadata key is ever matched -> missing_fields_csv = all 12 -> contract written as stub -> launch marked blocked.

Verified 2026-08-07: delegation summary with all 12 fields parses clean (missing=[]) when read from the DB message (newlines preserved), but parses as ALL missing when read from the materialized prompt file (flattened).

## Impact
- Verification contract always a stub for a2a-exit delegations -> crash recovery will not relaunch a blocked worktree; closeout gates may fail.
- workcell-state mislabels healthy running workers as blocked -> patrol confusion, risk of premature wt-close.
- watchdog pgrep -f <session_id> cannot match run-acp-prompt.py command lines (session_id not present) -> false DEAD flags clear agent_working session bindings.

## Expected fix (pick one)
1. Preserve newlines in the message when consuming worker tasks (e.g. base64/json-encode the message field, or use a separator that survives tab output and restore newlines before writing the prompt file).
2. Make worker_prompt_* metadata parser resilient to flattened single-line summaries (e.g. tokenize on 'Key:' boundaries regardless of line breaks).
3. At minimum: do not mark workcell blocked when metadata is incomplete IF the worker launch itself succeeds (the launch path already continues on incomplete metadata).

## Evidence
- .freely/run/manager-continuity-20260807T1159Z.md
- worker prompt: fix-raw-20260807T114900Z/.freely/run/a2a-prompts/task-cabd8c06...txt (flattened)
- verification contract stub: fix-raw-20260807T114900Z/.freely/run/worker-verification-contract.env
