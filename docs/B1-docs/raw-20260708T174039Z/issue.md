---
local_id: raw-20260708T174039Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260708T174039Z-A
platform_ids:
  github:
    issue_id: '3822'
    url: https://github.com/chatterzhao/freely/issues/3822
    synced_at: ''
  gitee:
    issue_id: IJZRZB
    url: https://gitee.com/zhaoquan/freely/issues/IJZRZB
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T17:41:01Z'
updated_at: '2026-07-08T17:41:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## 问题

commit 191afb82c (multi ACP bridge per-agent tool/slot) 更新了 5 个文件的 socket/path 逻辑加入 base_tool 后缀，但遗漏了 tool-launchers.sh。

tool_run_acp_from_prompt_file() 调用 _bridge_socket "$project" 不传 base_tool，导致计算出的 socket 路径无后缀（/tmp/freely-acp-<hash>.sock），而 acp-bridge.py 监听的是带后缀的路径（/tmp/freely-acp-<hash>-claude.sock）。

socket 路径不匹配 → run-acp-prompt.py 连接失败 → cycle log 空 → Manager AI session 47分钟零输出。

## 修复

在 tool-launchers.sh 的 tool_run_acp_from_prompt_file() 中，将 _bridge_socket "$project" 改为 _bridge_socket "$project" "$tool"。

## 验证

手动用正确的 socket path 测试了完整 Manager prompt (32KB)，AI 在 114 秒内产出 526 chunks 并正常 stopReason=end_turn。
