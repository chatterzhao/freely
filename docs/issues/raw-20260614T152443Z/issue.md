---
local_id: raw-20260614T152443Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2674'
    url: https://github.com/chatterzhao/freely/issues/2674
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-14T15:25:00Z'
updated_at: '2026-06-14T15:25:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

1. acp-bridge.py SDK v2 不接受 'start' 子命令（旧调用方传 start），导致 ACP bridge 无法启动
2. a2a_task_parser.py extract_state_block 返回 m.group(1) 而非 m.group(2)，JSON 内容被丢弃
3. bash --reply-text 传多行文本被 shell 破坏，需改用 --reply-file + temp file
4. _platform_configs 只按 remote 名称检测平台，Gitee enterprise (origin) 检测不到

## 修复

1. acp-bridge.py: 接受 'start' 作为可选位置参数（向后兼容）
2. a2a_task_parser.py: m.group(1) → m.group(2)
3. a2a_task.py: 添加 --reply-file 选项；bash 用 temp file 传递
4. pr-create-guarded: _platform_configs 按 URL 检测平台
