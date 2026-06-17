---
local_id: raw-20260617T103956Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2916'
    url: https://github.com/chatterzhao/freely/issues/2916
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T10:40:13Z'
updated_at: '2026-06-17T14:28:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-06-17T14:28:31Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
absorbed_into: 'I-20260617T103956Z-A'
---

## 目标
彻底消除 worker_prompts_csv 和 prompt 文件路径的所有残留，改为 A2A 协议标准委派模式。

## A2A 标准对标(官方 proto)
- Task.metadata = 标准扩展点(Freely 字段: skill/worktree/branch/raw_key/session_id)
- Message.parts[0].text = Worker 指令内容
- TaskStatus.state = submitted→working→completed
- SSE: SubscribeToTask / TaskStatusUpdateEvent

## 改动

### Phase 1: 消除所有 CSV 残留
- freely: 移除所有 worker_prompts_csv 引用(~28处)
- freely: 移除 manager_exit_contract_has_launchable_worker_prompt
- freely: 移除 latest_manager_worker_prompt_csv_from_continuity
- events: 不再输出 worker_prompts_csv=none

### Phase 2: Runtime 从 Task 生成 prompt
- manager_runtime_launch_workers(): 读 task.message → 写 prompt file → 启动 Worker
- 不再依赖 worker prompt 文件预存在

### Phase 3: Manager prompt 更新  
- manager-agent.md: 委派指令改为 A2A 标准模式
- 移除写 prompt 文件+CSV 的指令
- 改为: a2a-exit --state=submitted --agent-id=worker --message=完整指令 --skill=... --worktree=...

## 对标
- A2A official: Task.metadata 承载自定义字段, SendMessage.message 承载任务
- Routa: createTask(message=story_yaml), 不用 CSV
- JiuwenSwarm: Leader Task → Teammate 查询+执行
