---
local_id: raw-20260716T031047Z
kind: raw
phase_state: absorbed
absorbed_into: docs/B2-docs/runtime/daemon/raw-20260716T031047Z/issues/I-20260716T031047Z-A.md
platform_ids:
  github:
    issue_id: '3929'
    url: https://github.com/chatterzhao/freely/issues/3929
    synced_at: ''
  gitee:
    issue_id: IK1DQM
    url: https://gitee.com/zhaoquan/freely/issues/IK1DQM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T03:11:10Z'
updated_at: '2026-07-16T03:11:10Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Root Cause

capture_worker_session_id_and_store() has two bugs:

1. Wrong raw_key: passes agent_id (e.g. worker_01) instead of actual raw_key (e.g. 20260716T025126Z). Function lacks raw_key parameter.

2. Pre-launch agent_assign at L13275 uses hardcoded raw_key=develop.

## Impact

Without session_id in agent_working:
- Reviewer cannot session/prompt to inject review findings
- Manager cannot correct worker mid-task
- Daemon restart loses worker sessions
- Cross-tool detection broken

## Fix

1. Add raw_key param to capture_worker_session_id_and_store
2. Extract raw_key from branch name at call sites
3. Pass raw_key to acp_session_register
4. Fix agent_assign pre-launch call
