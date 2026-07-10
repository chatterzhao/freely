---
local_id: raw-20260701T040012Z12Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260701T040012Z-A
platform_ids:
  github:
    issue_id: '3682'
    url: https://github.com/chatterzhao/freely/issues/3682
    synced_at: ''
  gitee:
    issue_id: IJY15F
    url: https://gitee.com/zhaoquan/freely/issues/IJY15F
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T04:00:33Z'
updated_at: '2026-07-01T04:00:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n
## 问题

Daemon 启动时 A2A server 健康检查始终超时（先 30s，优化为 10s 仍然超时）。实测 socket 在 2s 内已创建，但 bash -S 检测无法发现。

## 根因

健康检查用 `[[ -S "$a2a_socket" ]]` + Python socket connect 检测 A2A 是否就绪。但 A2A server 实际在 2s 内就已绑定 socket 并输出 "Uvicorn running on unix socket" 到日志。bash 的 -S 检测与 uvicorn 的 socket 创建之间存在未知的不一致。

## 修复

将健康检查从 socket 轮询改为读取 A2A 日志文件中的就绪信号：
- 检查 A2A 进程是否存活（`kill -0`）
- grep 日志文件中的 "Uvicorn running on unix socket"
- 超时从 30s 降到 15s

这样更可靠——因为 "Uvicorn running" 是 uvicorn 真正完成绑定后才打印的。
