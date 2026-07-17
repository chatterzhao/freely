---
b1_id: B1-20260717T084757Z
phase_state: completed
source_raw: raw-20260717T084757Z
produced_candidate: C-20260717T084757Z-A
created_at: 2026-07-17
---

# B1_IBM: watchdog_sse 路由死定义

## Input
多 agent 设计链核验实抓：`routing to manager` 后 `SSE error: name '_get_agent_slot' is not defined`。

## Problem
watchdog_sse.py L462 `if __name__` 块含 watchdog_run 阻塞死循环；L474 `def _get_agent_slot` 在其后永不执行 → 路由三调用点（L220/253/282）触发即 NameError → SSE 断连,本次路由丢失。df5161415（07-04）引入——**A2A SSE 三角色路由自 07-04 起每次实际触发都失败**（worker 靠 runtime fallback 兜底；且 fallback worker 被观察到违规直写 develop、无产出移除工位——两次事故素材已录）。

## Brainstorm
- Option A（选定）：def 搬至 main 前 + AST 静态断言防复发 + 日志时间戳（本次排查因无时间戳无法定位实例归属）
- Option B：三处内联（重复，否）

## Decision: Option A

## 边界
只搬定义 + 时间戳 helper；不改路由逻辑/InputRequiredReason/ACP 调用。

## Candidate
- candidate_id: C-20260717T084757Z-A
- status: promoted
- milestone: M-20260717T084757Z-A
