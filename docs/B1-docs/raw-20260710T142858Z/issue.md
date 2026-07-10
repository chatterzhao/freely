---
local_id: raw-20260710T142858Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260710T142858Z-A
platform_ids:
  github:
    issue_id: '3874'
    url: https://github.com/chatterzhao/freely/issues/3874
    synced_at: ''
  gitee:
    issue_id: IK09X6
    url: https://gitee.com/zhaoquan/freely/issues/IK09X6
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T14:29:24Z'
updated_at: '2026-07-10T14:29:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

Manager 通过 a2a-exit 委派 Worker 后，A2A Task (state=submitted) 被创建，但 Runtime 不查询也不启动 Worker ACP session。Worker launch 仍走旧的 CSV/continuity prompt file 系统。

## 设计 vs 实现差距

acp-a2a-architecture.md 定义了正确流程:
1. Manager → a2a-exit → Task.message (A2A)
2. Runtime → tasks/list --state=submitted --role=worker → 获取待处理任务
3. Runtime → Task.message → prompt file → Worker ACP session (fork from Manager)
4. Worker → a2a-exit completed → SSE → Manager 感知

当前实现:
- 步骤 1 已实现 (Manager 正确创建 A2A Task)
- 步骤 2-3 未实现 (Runtime 仍用 CSV/continuity)
- 步骤 4 部分实现 (SSE 已就绪，Worker 从未启动所以无法触发)

## 根因

manager_runtime_launch_workers_from_latest_task() 只读 continuity 文件和 CSV prompt 列表，不查询 a2a_tasks 表。

## 修复

1. manager_runtime_launch_workers_from_latest_task() 增加 A2A 路径: 查询 tasks/list --state=submitted --role=worker
2. 对每个 submitted task: 从 Task.message 生成临时 prompt file
3. 启动 Worker ACP session (session/fork from Manager 或 session/new)
4. Worker 启动后更新 task state: submitted → working

## 验收

- Manager 委派后，Worker ACP session 在 30s 内启动
- Worker 完成后，Manager 通过 SSE 收到通知
- 旧 CSV/continuity 系统保留作为 fallback
