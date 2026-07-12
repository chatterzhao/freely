# B1: daemon stop rc=143 与意外崩溃区分

## Problem
freely daemon stop 发送 SIGTERM → AI 进程 rc=143 (128+15)。
monitor-ai-acp.sh 无法区分这是 intentional stop 还是 crash → stopReason=unknown → exit 1。
下次启动时 resume session 被标记失败 → fresh session → 丢失上下文。

## Brainstorm
### Option A: stop_marker 文件检查
monitor 在 stop_reason=unknown 时检查 stop_marker 文件是否存在。
daemon stop 命令在发 SIGTERM 前写入 stop_marker。
- 文件存在 → stop_requested → exit 0 (clean)
- 文件不存在 → 原逻辑 (crash → exit 1)
✅ 简单、可靠、无侵入

### Option B: PID 追踪
记录 AI 进程 PID，stop 时对比。但 PID 可能被复用。

## Decision: Option A
在 monitor-ai-acp.sh completion 逻辑中增加 stop_marker 检查，仅约 12 行代码。
