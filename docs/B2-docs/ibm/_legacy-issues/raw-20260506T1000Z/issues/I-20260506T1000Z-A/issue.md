---
local_id: I-20260506T1000Z-A
kind: i_issue
phase_state: completed
milestone: M-20260506T1000Z-A
candidate: C-20260506T1000Z-A
title: supervisor 主循环 select_launch_kind 前添加 task_mode=wait 门禁
created_at: '2026-05-19T16:32:43Z'
updated_at: '2026-05-19T18:34:00Z'
source_candidate: docs/B1-docs/raw-20260506T010000Z/candidates.md#C-20260506T1000Z-A
---

## I-20260506T1000Z-A

| Field | Value |
|-------|-------|
| local_id | `I-20260506T1000Z-A` |
| kind | `i_issue` |
| phase_state | `in_dev` |
| milestone | `M-20260506T1000Z-A` |
| candidate | `C-20260506T1000Z-A` |
| created | 2026-05-19 16:32:43+00:00 |
| updated | 2026-05-19 16:32:43+00:00 |

### Acceptance Criteria

1. task_mode=wait 时 supervisor 不 build prompt、不 launch AI
2. wait 模式 supervisor 仅轮询 task_mode_gate，sleep CHECK_INTERVAL 后 continue
3. 修改点在 select_launch_kind 之前，不破坏已有 stop_ai handler 逻辑
4. task_mode=auto 或 id:<scan-id> 时行为不变
