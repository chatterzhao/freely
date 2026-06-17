---
local_id: raw-20260615T001626Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2691'
    url: https://github.com/chatterzhao/freely/issues/2691
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-15T00:16:42Z'
updated_at: '2026-06-17T00:24:09Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 目标
消除双路径（a2a-exit + 文本JSON解析），只保留标准 A2A 协议路径。

## 6 Phase 计划

### Phase 1: 修复信号文件 WORKERS 字段
a2a_task.py a2a-exit 写入 WORKERS 到 last-exit-task.env

### Phase 2: 更新所有 Prompt
- manager-agent.md: 改为 a2a-exit 指令
- worker-agent.md: 同上
- WORKER_STATE_INJECT: 移除 JSON block 指令
- 系统 prompt: 改为 a2a-exit
- repair prompt: 同上
- delta prompt: 同上

### Phase 3: 移除文本解析 fallback
- parse_a2a_task_json_reply: 删除 tail+regex 路径
- 删除 last-workers-csv.txt/last-exit-kind.txt 持久化

### Phase 4: 移除持久化文件 fallback
- manager_exit_contract_kind: 移除文件读取
- delegate_workers handler: 移除文件读取

### Phase 5: 废弃 a2a_task_parser.py
- process_ai_reply/read_state_only: 加 env guard
- parse/extract CLI 子命令: 移除

### Phase 6: Worker handoff 改用 DB 查询
- supervisor loop: 用 DB get 替代 text extract

## 回退
每 Phase 独立可回退。FREELY_A2A_TEXT_PARSING_FALLBACK=1 恢复旧行为。
