---
local_id: raw-20260720T044032Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '4049'
    url: https://github.com/chatterzhao/freely/issues/4049
    synced_at: ''
  gitee:
    issue_id: IK2944
    url: https://gitee.com/zhaoquan/freely/issues/IK2944
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T04:40:56Z'
updated_at: '2026-07-20T04:40:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## Root Cause

Worker supervisor recovery writes manager_worker_launch_verification_blocked when verification-contract.env has METADATA_PRESENT=false. For closeout-only workers (B1/B2 done, need only PR+merge+close), the contract lacks B2-level metadata fields and AI never starts.

## Impact

Since 2026-07-20 04:00Z, 8+ Manager patrol rounds failed because workers can't self-start. Only B1 111514Z succeeded (initial launch passed contract check, AI ran, PR created before restart blocked).

## Fix Targets

1. docs/system/workspace/scripts/runtime/freely:
   - launch_worker_from_manager_prompt_if_needed: write_worker_verification_contract_file should populate defaults when no metadata
   - recover_expected_running_workcells: allow closeout workers to skip contract check

## Reproduction

1. Manager delegates closeout worker
2. Runtime launches worker supervisor via manager_runtime_launch_workers_after_ai_cycle_if_needed
3. Supervisor starts, checks verification-contract.env → METADATA_PRESENT=false → writes manager_worker_launch_verification_blocked
4. AI never starts, task stuck forever
