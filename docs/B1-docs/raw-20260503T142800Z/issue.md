---
local_id: raw-20260503T142800Z00Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
priority: P1
source: platform
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: "187"
    owner: chatterzhao
    repo: freely
created_at: "2026-05-03T21:29:35Z"
title: "fix: run-acp-prompt.py disconnects before bridge finishes"
platform_state: closed
---

## Root Cause

run-acp-prompt.py disconnects from the bridge socket immediately after receiving stopReason=end_turn, before the bridge finishes sending all follow-up session/update notifications. The bridge then gets [Errno 32] Broken pipe → treated as an error → AI cycle marked rc=1 → process churn → restart storm.

### Timing evidence
```
21:20:03  bridge: session/prompt id=5 sent
21:22:31  bridge: send response error: [Errno 32] Broken pipe
21:22:41  daemon: ai process exited rc=1 → restart storm triggered
```

### Fix Options
1. run-acp-prompt.py: wait for final response before disconnect (2s grace after end_turn)
2. daemon: don't treat Broken pipe as failure if valid output exists
3. process churn threshold: increase RESTART_STORM_COUNT from 3 to 10

### Status
Root cause confirmed. OPEN — needs implementation.
