---
local_id: raw-20260616T023944Z44Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2792'
    url: https://github.com/chatterzhao/freely/issues/2792
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T02:40:00Z'
updated_at: '2026-06-16T02:40:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem

scan 在 task-lifecycle-scan.py line 474-485 发现 local ↔ platform state 不一致时，
无条件生成 state_mismatch → platform_sync_batch 任务。不区分"一边已 terminal"还是
"两边都活跃"。

结果：121 个本地 file 的 GitHub 已关闭，但 scan 生成 315 个 sync 任务消耗所有 AI 周期。

## Current logic (line 471-485)
```python
if plat_state:
    if local_platform_state and local_platform_state != plat_state:
        # ANY difference → state_mismatch → sync task
        items.append({"stage": "state_mismatch", ...})
```

## Correct logic

### Phase 1: Terminal resolution (trivial — one side already done)
```
local terminal (absorbed/dropped) + platform OPEN  → close_platform
platform CLOSED/MERGED + local proposed           → close_local (mark dropped)
platform CLOSED/MERGED + local absorbed/dropped   → consistent (skip)
```

### Phase 2: Real mismatch (both active, needs sync)
```
local OPEN + platform OPEN + states differ → state_mismatch (real sync)
```

### Phase 3: Missing counterpart (existing logic)
```
local exists + no platform counterpart → local_only → push to platform
platform exists + no local counterpart → platform_only → pull from platform
```

## Implementation

In task-lifecycle-scan.py, add a `_resolve_terminal_mismatch()` check before
the state_mismatch branch. If either side is terminal/closed:
- Set stage to "close_platform" or "close_local"  
- next_action includes the specific close command
- Don't count as incomplete for sync batch purposes

For close_local: next_action should be "更新 phase_state 为 dropped，理由：平台 issue 已关闭"
For close_platform: next_action should be "关闭平台 issue #{num}，本地已 terminal"

## Acceptance
- [ ] Local proposed + GitHub CLOSED → close_local (not state_mismatch)
- [ ] Local absorbed + GitHub OPEN → close_platform (not state_mismatch)
- [ ] Local proposed + GitHub OPEN (diff states) → state_mismatch (real sync)
- [ ] 315 sync items → ~10 real mismatches after fix
