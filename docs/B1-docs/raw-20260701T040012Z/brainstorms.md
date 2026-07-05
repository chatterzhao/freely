---
b1_id: B1-20260701T040012Z
phase_state: completed
source_raw: raw-20260701T040012Z
source_url: https://github.com/chatterzhao/freely/issues/3682
produced_candidate: C-20260701T040012Z-A
created_at: 2026-07-01
---

# B1_IBM: A2A health check unreliable

## Problem
Daemon 启动时 A2A 健康检查始终超时（socket 在 2s 已创建但 -S 检测不到）。

## Root Cause
bash `[[ -S ]]` 检测 uvicorn Unix socket 时存在未知的不一致。改用 A2A 日志中的就绪信号。

## Brainstorm
- Option A: 调大超时 — 治标
- Option B: log-based — A2A 真正绑定后才输出 "Uvicorn running"，更可靠
- Option C: HTTP health endpoint — 过度设计

## Decision: Option B — log-based health check
Grep A2A log for "Uvicorn running on unix socket". Process liveness check added. Timeout reduced 30s→15s.
