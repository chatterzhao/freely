---
local_id: raw-20260623T162226Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260623T162226Z-A
platform_ids:
  github:
    issue_id: '3392'
    url: https://github.com/chatterzhao/freely/issues/3392
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-23T16:22:44Z'
updated_at: '2026-06-23T16:22:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 背景

#3381 分析发现空循环时 `semantic_loop_signal` 未触发（Guard 10 盲区）。SSE 重构（#3388）和 A2A 状态管理修复（#3390）已做完——Manager 有了实时 Worker 状态、stop 不再改 A2A state、_restore_tasks 正确处理重启恢复。但**仍然没有兜底安全网**——如果 SSE Watchdog 挂了、Manager session 卡住了、AI 模型陷入短回复循环，系统还是会空转。

需要一套不依赖 continuity 指纹、不依赖 AI 自我判断的 supervisor 侧防护。

## 当前基础设施（SSE 重构后可用）

- SSE Watchdog（sse-watchdog.sh）：持久 SSE 连接，state_update → JSONL 队列 + ACP 注入
- `_sse_event_queue_read_unconsumed`：Manager prompt 读 SSE 事件队列
- `restart_storm`：已有 30s 滑动窗口（跟踪进程数）
- `cache_metrics`：runtime event（当前缺 token 数据，等 #3386）
- `task_mode` set/get：已有 auto/listen/wait 三种模式
- `stop_ai → listen` 降级路径（freely:15300-15328）：已存在

## 设计（基于最新实现的简化版）

四层递进，在 supervisor 主循环中 A-L042 → A-L020 之间执行。

### L0 — 频繁 fresh 启动（独立轻量窗口）
- 数据结构：`.freely/run/loop-guard-L0-window.tsv`，格式 `timestamp<TAB>launch_kind<TAB>worker_launched_count`
- 窗口：300s（5 分钟）
- 条件：窗口内 `launch_kind=fresh` 行数 > 3，且全部 `worker_launched_count=0`
- 动作：`task-mode set --task-mode wait`
- 与 `restart_storm` 的关系：独立运行，不修改 restart_storm 的 TSV 格式

### L1 — 动作指纹停滞（同 session）
- 条件：`(exit_kind, worker_launched_count)` 二元组连续 3 轮相同，且 `worker_launched=0`
- 数据源：`LAST_EXIT_REASON`（第 8021 行），`worker_launched_directly` 事件（第 12585 行）
- 动作递进：第 1 次 → runtime event + hint / 第 2 次 → 显式指令 / 第 3 次 → listen

### L2 — Token 空转（滑动窗口）
- 依赖 #3386。未完成前降级为 `prompt_bytes * 0.25` 估算
- 条件：10 分钟内 > 20000 tokens（或 prompt_bytes > 80KB），worker_launched=0，continuity 无推进
- 动作：`task-mode set --task-mode listen`

### L3 — 硬预算封顶
- 条件：单次 auto 启动总 token > 500000
- 动作：`task-mode set --task-mode wait` + stop marker

## 关键决策
- L1/L2 → `listen`（300s 轮询，自动恢复）
- L0/L3 → `wait`（人工介入）
- 不替代现有 `semantic_loop`——保留为观测信号，L0-L3 是阻断层
- 不依赖 continuity 指纹

## 与现有机制的整合

| 现有 | 在 L0-L3 中的角色 |
|------|-----------------|
| SSE Watchdog | 减少了空循环概率（实时 Worker 状态）——兜底在 SSE 挂了时生效 |
| `restart_storm` | L0 参考其滑动窗口模式，但不共用 TSV |
| `cache_metrics` | L2 数据源（需 #3386） |
| `task_mode` | L0-L3 的动作执行器 |

## 参考
- 原始分析：https://github.com/chatterzhao/freely/issues/3381
- SSE 实现：https://github.com/chatterzhao/freely/pull/3389
- 状态管理：https://github.com/chatterzhao/freely/pull/3391
- 行业模式：Costfuse/Circuit Breaker/AgentFuse 三层防护
