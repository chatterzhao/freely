---
local_id: raw-20260704T234812Z12Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260704T234812Z-A
platform_ids:
  github:
    issue_id: '3732'
    url: https://github.com/chatterzhao/freely/issues/3732
    synced_at: ''
  gitee:
    issue_id: IJYTKP
    url: https://gitee.com/zhaoquan/freely/issues/IJYTKP
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-04T23:48:32Z'
updated_at: '2026-07-04T23:48:32Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景

PR #3731 (fix/raw-20260704T164337Z37Z-acp-cleanup) 清理不彻底，遗留以下问题：

## 1. freely_db_manager.py — IndentationError 阻止 DB daemon 启动

h_aw_upsert_only 中 if slot_val: 缩进多了一级，导致 Python 语法错误。

## 2. acp-bridge.py — CLI 缺少 --base-tool 参数

_pid_file/_socket_path 签名已接受 base_tool，但 argparse 无 --base-tool 参数。#3731 的修改只是把所有调用从 _pid_file(project) 改成 _pid_file(project, "")，传的都是空字符串，等于没改。

## 3. freely shell — _ensure_acp_bridge_running 不传 $base_tool

line 14035: pid_file="$(_acp_bridge_pid_file "$project")" — 不传第二个参数
line 14097: _acp_bridge_health_check "$project" 5 — 不传 base_tool
line 14196: bridge start 命令不传 --base-tool

## 4. bash/Python socket/pid 路径不一致

bash 版无条件加 - 分隔符产生 /tmp/freely-acp-{hash}-.sock，Python 版条件加产生 /tmp/freely-acp-{hash}.sock，路径不匹配。

## 5. freely shell — 5 处硬编码 socket 路径

line 18788, 18829, 18860, 18890, 18923 硬编码了 /tmp/freely-acp- 路径，未使用 _acp_bridge_socket 函数。

## 6. watchdog_sse.py — 3 个 docstring 未闭合

_handle_needs_reviewer, _handle_needs_manager, _handle_needs_worker 的 docstring 只有开头 """，没有结尾。

## 7. freely shell — 3 处 agent_assign 裸调用

_acp_session_new, _acp_session_fork, reviewer session create 中直接调 agent_assign 未传 slot 参数。

## 8. monitor-ai-acp.sh — bridge 函数不传 base_tool

_bridge_pid_file, _bridge_socket 调用不传 base_tool 参数。

## 9. pre-commit.sh hook 提示改进

拦截消息没有告知用户使用 freely feedback 命令 + freely wt-create 命令 + skill freely-workflow-guarded-execution。
