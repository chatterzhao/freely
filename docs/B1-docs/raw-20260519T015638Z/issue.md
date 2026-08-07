---
local_id: raw-20260519T015638Z38Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '601'
    url: https://github.com/chatterzhao/freely/issues/601
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-19T01:56:56Z'
updated_at: '2026-06-21T20:12:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260519T015638Z38Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260519T015638Z38Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-05-19T01:56:38Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260519T015638Z38Z`。实现前请用 `wt-create --raw-key 20260519T015638Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P1
- phase_state: dropped
source: feedback
created_at: "2026-05-19T01:56:38Z"
title: "systematic: worker process consistently exits with stale_pid before producing handoff"

## Observation
21 consecutive worker launches (2026-05-18T23:49 to 2026-05-19T01:45) have exited with stale_pid (worker process no longer alive) before producing a completion handoff.

## Evidence
- Handoff DB shows 21 blocked workers, all exit_kind=stale_pid
- Workers live 2-10 minutes then die without completion_summary
- No completed workers in recent rounds
- Affects all worktrees: fix-batch-closeout-raw, feature-chat-conversation, 20260519-fix-cleanup-sync, etc.

## Impact
- Manager delegations are ineffective — no closeout work progresses
- 30 state_mismatch items cannot be closed
- 4 ready worktrees cannot be merged
- Fleet cleanup is stalled

## Suspected Root Cause
- Worker ACP session times out before task completes
- OR worker produces handoff but runtime fails to persist it
- OR worker launch pipeline has a race condition

## Suggested Action
1. Investigate worker launch/handoff pipeline in runtime scripts
2. Add worker lifecycle timeout/respawn governance
3. Consider direct execution fallback for simple tasks
