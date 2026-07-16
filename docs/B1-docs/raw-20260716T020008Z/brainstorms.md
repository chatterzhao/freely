---
b1_id: B1-20260716T020008Z
phase_state: completed
source_raw: raw-20260716T020008Z
created_at: 2026-07-16
---
# B1: capture_worker_session_id_and_store 写入 agent_working

## Problem
capture_worker_session_id_and_store (line 13055) 在 worker fork 后捕获 session_id，但只更新 A2A task (line 13077)，不写 agent_working。

agent_assign 已在 fork 前写入基本条目(worktree/worker_id/slot)，但 session_id 从未回填。agent_working 表永远只有 __manager__。

## 当前链路
1. agent_assign → UPSERT agent_working (worktree, worker_id, slot) ✅
2. run-acp-prompt.py fork → session_id 输出到 cycle log ✅
3. capture_worker_session_id_and_store → 读 log → UUID 验证 ✅
   → a2a_task.py update ✅ → acp_session_register ❌

## Decision
capture_worker_session_id_and_store 增加参数(target_project, agent_id, slot)，session 捕获后调用 acp_session_register 写入 agent_working。

同时 agent_assign 传入的 slot 应从 agent-table 读取 worker slot，而非硬编码 manager slot。

## Candidate: C-20260716T020008Z-A promoted M-20260716T020008Z-A
