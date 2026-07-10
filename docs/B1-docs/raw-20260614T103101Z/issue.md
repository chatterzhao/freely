---
local_id: raw-20260614T103101Z01Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2655'
    url: https://github.com/chatterzhao/freely/issues/2655
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-14T10:31:17Z'
updated_at: '2026-06-14T10:31:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题

a2a-exit 当前每次调用都创建新 Task (POST /tasks)，而非更新现有 Task (PATCH /tasks/{id})。
Worker 的 3 次调用 (submitted→working→completed) 产生 3 条独立记录，破坏 A2A Task 生命周期。

DB CHECK constraint 不接受 pending-input，worker_handoff_needed 映射不一致。

缺少 a2a-task-update 工具，Worker 无法中期汇报进度。

## 修复

1. a2a-exit: --task-id 参数 (首次 POST 创建，后续 PATCH 更新)
2. a2a-task-update 子命令 (--task-id --state --progress --message --artifact)
3. DB: ALTER TABLE 添加 pending-input 到 CHECK constraint
4. worker_handoff_needed → pending-input (统一 a2a_client.py + freely_db_manager.py)
5. 信号文件 last-exit-task.env 消除监督者轮询延迟
6. launched_at / completed_at 自动填充逻辑

Closes #2651 (部分)
