---
local_id: raw-20260630T085809Z09Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T085809Z-A
platform_ids:
  github:
    issue_id: '3647'
    url: https://github.com/chatterzhao/freely/issues/3647
    synced_at: ''
  gitee:
    issue_id: IJXVF2
    url: https://gitee.com/zhaoquan/freely/issues/IJXVF2
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T08:58:29Z'
updated_at: '2026-06-30T08:58:29Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## 发现的问题

freely start --task-mode auto 启动时观测到以下 bug：

### Bug 1: A2A 健康检查发送原始 HTTP GET 而非 JSON-RPC
- 位置: docs/system/workspace/scripts/runtime/freely:8620
- s.sendall(b'GET /tasks HTTP/1.1...') — 发送原始 HTTP
- A2A Server 的 / 路由是 JSON-RPC 端点，接受 POST + JSON body
- 健康检查应使用正确的端点

### Bug 2: 44,835 行 Invalid HTTP request 日志轰炸
- A2A 日志 45,870 行中 44,835 行(97.7%) 是 h11 的 WARNING
- _a2a_uvicorn_log_config() 配置了 h11: ERROR 但未生效

### Bug 3: Shell 注入
- 位置: freely:8619，s.connect('$a2a_socket') 变量直接拼接
- 与之前修复的 freely-cycle shell 注入同类问题

### Bug 4: A2A Server 启动超时 10 秒过短
- 服务器恢复历史 task 需要 >10 秒

### Bug 5: A2A Server 日志无时间戳
- uvicorn 默认日志格式不含时间戳

## 验收标准
- 健康检查使用正确的 A2A 协议端点或 socket 存在性检查
- Shell 注入修复：通过环境变量传递 socket 路径
- h11 日志抑制生效
- A2A 启动超时延长到合理值（如 30 秒）
- A2A Server 日志包含时间戳
