---
local_id: raw-20260617T095105Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260617T095105Z-B
platform_ids:
  github:
    issue_id: '2913'
    url: https://github.com/chatterzhao/freely/issues/2913
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T09:51:22Z'
updated_at: '2026-06-21T01:40:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 目标

消除 Manager-Worker 委派中的 CSV 文件和 prompt 文件路径中转，改用 A2A 协议原生的 Task.message 承载完整任务内容。

## 当前架构（CSV 中转）

```
Manager → 写 worker prompt 文件到 .freely/run/worker-prompts/
       → a2a-exit --workers=path1,path2 (CSV 路径)
       → worker_prompts_csv 存入 A2A Task
       → freely runtime 读 CSV → 打开文件 → 启动 Worker

问题:
1. CSV 路径依赖文件系统，工作区/工位下路径不一致
2. worker_prompts_csv 字段不兼容 A2A 标准
3. 两层存储: prompt 文件内容 + A2A Task 元数据，不同步
```

## 目标架构（A2A 原生）

```
Manager → a2a-exit --state=submitted --agent-id=worker \
            --skill=freely-fix-execution \
            --worktree=/path --branch=fix/xxx \
            --message="完整 worker prompt 指令内容"
       → A2A Task 包含完整委派内容
       → freely runtime: tasks/list --state=submitted --agent=worker
       → 每个 Task: 读 message → 生成 prompt file → 启动 Worker ACP session
       → Worker 完成: a2a-exit --state=completed (SSE 推送状态)

对标 Routa:
- Routa Coordinator: createTask(message=story_yaml) → A2A
- Routa Crafter: listTasks(state=todo) → 获取任务 → 执行
- Routa Gate: updateTaskStatus → 验收
- 全程无 CSV，无文件路径依赖
```

## 具体改动

### Phase 1: A2A Task 承载完整委派信息
- a2a_task.py a2a-exit: message 字段承载完整 prompt 内容
- a2a_server.py POST /tasks: 确保 message/skill/worktree/branch/raw_key 全部持久化
- 移除 --workers / worker_prompts_csv 参数

### Phase 2: Runtime 从 A2A Task 读取委派
- manager_exit_contract_kind(): 改查 tasks/list --state=submitted
- manager_runtime_launch_workers(): 读 task.message → 生成 prompt file
- 移除所有 worker_prompts_csv / _worker_csv 相关代码
- 移除 _db_exit_contract_field manager worker_prompts_csv

### Phase 3: Manager prompt 更新
- Agent 指令: a2a-exit 直接传 message（不再写 prompt 文件再用 CSV）
- Worker prompt 内容嵌入 A2A Task.message

## 影响文件
- docs/system/workspace/scripts/runtime/freely
- docs/system/workspace/scripts/runtime/a2a/a2a_server.py
- docs/system/workspace/scripts/runtime/a2a_task.py
- docs/system/workspace/agents/manager-agent.md (prompt 模板)
