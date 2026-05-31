---
issue_id: raw-20260516T234331Z
kind: raw
priority: P2
source: chat-inbox
created_at: '2026-05-16T23:43:31Z'
title: 统一反馈机制：Runtime/Worker 都通过 handoff 记录向 Manager 汇报，Manager 消费 unconsumed 记录形成闭环
platform_ids:
  github:
    issue_id: '380'
    url: https://github.com/chatterzhao/freely/issues/380
    synced_at: '2026-05-16T23:43:36Z'
updated_at: '2026-05-31T00:38:01Z'
primary_platform: github
phase_state: absorbed
absorbed_into: I-20260413-0420-A
platform_state: closed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
---

## 设计

一切反馈都走 handoffs 表。Manager 已有的"未消费"查询自动拾取所有需要处理的事件。不需要 prompt 注入、不需要 per-raw-key 搜索、不需要新的通信协议。

### 写入者与记录类型

| 写入者 | 场景 | handoff 记录 |
|--------|------|-------------|
| Runtime | Worker launch 失败（工位不存在） | `role=runtime, status=blocked, exit_kind=launch_blocked, reason=worktree_missing, next_action=请用 wt-create 创建工位后重新委派` |
| Runtime | Worker 进程僵死（stale_pid） | `role=runtime, status=blocked, exit_kind=stale_pid, reason=worker_process_no_longer_alive` |
| Runtime | Worker launch 成功 | `role=runtime, status=launched`（Manager 可查但不必须消费） |
| Worker | 完成任务 | `role=worker, status=completed, exit_kind=worker_done, completion_summary=...` |
| Worker | 需要主管决策 | `role=worker, status=blocked, exit_kind=worker_handoff_needed, reason=..., next_action=...` |
| Worker | 遇到阻塞 | `role=worker, status=blocked, exit_kind=worker_blocked, reason=..., next_action=...` |
| Manager | 自己需要记录决策 | `role=manager, exit_kind=stop_ai/delegate_workers/resume_manager` |

### Manager 消费流程（已有，无需改动）

```
每轮 patrol:
1. 查 handoffs WHERE consumed_by="" AND role IN ('worker', 'runtime')
2. 逐条处理：读 reason/next_action → 决策 → 标记 consumed
3. 全部消费完后再看 scan 找新任务
```

### 关键改动

1. **`materialize_worker_prompt_worktree_if_needed` 失败时**：不再只写 runtime event，改为 INSERT handoff（`role=runtime, status=blocked, exit_kind=launch_blocked`）
2. **Worker launch 成功时**：已有 `worker_launched_directly` event → 也写一条 handoff（`role=runtime, status=launched`）
3. **Worker 僵死检测**：已有 `stale_pid` 逻辑 → 改为写 handoff（`role=runtime, status=blocked, exit_kind=stale_pid`）

### 不需要的

- ~~prompt 注入 worker launch 结果~~
- ~~per-raw-key 历史搜索~~
- ~~新的反馈协议~~
- ~~`append_manager_handoff_context_if_needed` 增强~~

## 范围

- `docs/system/workspace/scripts/runtime/freely`：runtime 失败点改为 INSERT handoff
- `docs/system/workspace/scripts/runtime/handoff.py`：支持 `role=runtime` 的 handoff INSERT
