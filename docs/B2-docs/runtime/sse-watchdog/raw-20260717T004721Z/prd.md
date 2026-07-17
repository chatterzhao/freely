# PRD: sse pid 校验参数顺序修复
- issue_id: I-20260717T004721Z-A

## Goal
活着的 sse-watchdog 不再被误判 invalid/误清/误杀；控制面 sse 状态真源恢复可见。

## 实现方案
runtime/freely `valid_sse_watchdog_pid_for_project` 声明行参数顺序修复（唯一改动）。

## Dev-Loop Handoff
RED（3 项确认失败）→ 单行修复 → GREEN → test 工位全量。
