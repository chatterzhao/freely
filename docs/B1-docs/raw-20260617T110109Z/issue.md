---
local_id: raw-20260617T110109Z09Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2918'
    url: https://github.com/chatterzhao/freely/issues/2918
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T11:01:26Z'
updated_at: '2026-06-17T14:28:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-06-17T14:28:44Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
absorbed_into: I-20260617T110109Z-A
platform_state: closed
---

## 问题
A2A 协议完全不使用文件。Message.parts[{text}] 就是内容载体。但 Freely 的 A2A Task 仍存储 prompt_file 字段——这是 ACP 层的实现细节泄漏到了 A2A 层。

ACP session/prompt 确实需要文件作为输入，但文件路径应由 Runtime 从 task_id 派生（临时文件），不应作为 A2A Task 的持久化字段。

## 评审结论(subagent)
APPROVE WITH CHANGES — 影响 6 个文件，需修复 1 个 _task_id ordering bug + 1 个 _raw_key extraction bug。

## 改动清单

### a2a_types.py — 类型层
- 移除 Task dataclass 的 prompt_file 字段
- 移除 to_dict/from_dict 中的 prompt_file

### a2a_server.py — A2A 服务端
- execute(): 移除 prompt_file metadata 写入
- _tasks_endpoint POST: 移除 prompt_file

### a2a_task.py — CLI 客户端
- 移除 --prompt-file 参数(create/insert/parse/a2a-exit 共 4 处)
- 移除所有 handler 中的 prompt_file=getattr(...)

### freely-db-cli — DB CLI
- 移除 task.upsert/update 中的 prompt_file 参数

### freely_db_manager.py — DB Schema (向后兼容)
- 保留 prompt_file 列(已有数据)，但停止写入
- 从 migration list 移除

### freely runtime — 核心重构
- Worker launch loop: 不读 prompt_file，直接从 task_id 派生文件路径
- 路径: {worktree}/.freely/run/a2a-prompts/task-{task_id}.txt  
- 从 task 记录提取 raw_key(不是从文件名)
- 修复 _task_id ordering bug(先取值再用)
- Worker 完成后清理临时文件
- parse_a2a_task_json_reply: 移除未使用的 prompt_file 参数
