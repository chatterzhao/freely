---
local_id: raw-20260516T121409Z
kind: raw
priority: P2
phase_state: absorbed
source: chat-inbox
created_at: '2026-05-16T12:14:09Z'
title: manager-agent.md 缺少巡逻模式行为规范，导致 Manager 面对 scan 数据只输出 stop_ai
platform_ids:
  github:
    issue_id: '368'
    url: https://github.com/chatterzhao/freely/issues/368
    synced_at: '2026-05-16T12:14:17Z'
updated_at: '2026-06-03T10:50:01Z'
primary_platform: github
platform_state: closed
force_closed_at: '2026-05-16T12:59:11Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
absorbed_into: infra-githooks
---

## 根因

`manager-agent.md` 当前只有"首跳路由"（新 intake → route to B1/B2），缺少**巡逻委派**模式的行为规范。

Manager 每轮收到含 scan 数据的 prompt（131 条 ready 条目），但不知道怎么处理：
- 不知道 `local_only` 条目应该用 `issue-sync` 推送到平台
- 不知道 `branch_deleted` 应该批量更新 phase_state
- 不知道 `platform_create` 应该 `wt-create` 开工位
- 不知道 `raw_created` 应该路由到 B1
- 不知道什么时候该 `delegate_workers`、什么时候该 `resume_manager`、什么时候该 `stop_ai`

结果：每次巡逻看到同样的 scan → 不知道怎么处理 → `stop_ai` → 下一轮又来 → 死循环。

## 需要补充的内容

### 1. 巡逻模式的 step-by-step 工作流

```
巡逻模式（prompt 含 scan 数据时）：
1. 读 scan 数据，分类条目
2. 对每种 stage 采取对应的 action（见下方表格）
3. 决策：自己处理还是委派 worker
4. 输出对应的 exit_kind
```

### 2. Scan stage → action 映射表

| stage | action | exit_kind |
|-------|--------|-----------|
| local_only (ready) | 用 ./bin/issue-sync push | delegate_workers（批量） |
| local_needs_closeout (ready) | 更新 phase_state → completed | delegate_workers（批量） |
| branch_deleted (ready) | 更新 phase_state → absorbed | delegate_workers（批量） |
| platform_create (ready) | wt-create 开工位 | delegate_workers |
| raw_created | 路由到 B1 | resume_manager（自己处理）或 delegate_workers |
| chat_waiting_worktree | 评估价值 → wt-create | resume_manager |
| b1_candidate | 评估 promote/absorb/drop | resume_manager |

### 3. exit_kind 使用指南

| exit_kind | 何时使用 |
|-----------|---------|
| delegate_workers | 有可委派的具体任务（有 worker prompt 文件路径） |
| resume_manager | 需要自己继续分析/处理（如 B1 决策、评估） |
| stop_ai | 真的无事可做：scan total_incomplete=0、无新 intake、handoff DB 无未消费 worker |

### 4. stop_ai 循环防护

如果连续 3 次 stop_ai 且 scan 数据中的 ready 条目未减少，必修：
- 检查 prompt 中的 scan 条目是否可操作
- 如果可操作但之前未处理 → 说明之前的 stop_ai 是误判 → 本轮必须 delegate 或 resume
- 如果确实不可操作 → 在 reason 中说明具体为什么每个 stage 都不可操作

## 范围

只改 `docs/system/workspace/agents/manager-agent.md`。
