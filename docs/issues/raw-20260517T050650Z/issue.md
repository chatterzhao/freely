---
local_id: raw-20260517T050650Z
kind: raw
priority: P2
source: chat-inbox
created_at: '2026-05-17T05:06:50Z'
title: 'worker 使用非标准 exit_kind: completed，应为 worker_done'
platform_ids:
  github:
    issue_id: '417'
    url: https://github.com/chatterzhao/freely/issues/417
    synced_at: '2026-05-17T05:06:57Z'
updated_at: '2026-06-15T06:10:00Z'
primary_platform: github
phase_state: absorbed
absorbed_into: I-20260413-0420-A
platform_state: closed
---

## 问题

Worker 完成委派任务后输出 `"exit_kind": "completed"`，但 worker-agent.md 定义的标准值是 `worker_done`。

观察到的 cycle log：
```json
{
  "exit_kind": "completed",
  "summary": "batch-closeout 和 lifecycle-closeout-round2 均已合入 develop",
  ...
}
```

`completed` 不是 `VALID_EXIT_KINDS` 中定义的合法值：
```python
VALID_EXIT_KINDS = {
    'delegate_workers', 'resume_manager', 'stop_ai',
    'worker_done', 'worker_blocked', 'worker_handoff_needed',
}
```

## 影响

Runtime 的 `parse_handoff_json` → `validate_handoff_json` 会将 `completed` 视为非法值，handoff 解析失败，Manager 收不到 Worker 的完成汇报。

## 原因

worker-agent.md 的交接章节（行 111+）使用 `worker_done`，但 AI 有时输出 `completed`。可能在 agent doc 的某些地方用词不一致，或 AI 自发选择了 `completed`。

## 修复

1. 在 worker-agent.md 的退出交接章节中 **强调只能使用三种 exit_kind：worker_done、worker_blocked、worker_handoff_needed**
2. 在 handoff.py `validate_handoff_json` 中，对 worker 角色的非法 exit_kind 给出更明确的错误提示
