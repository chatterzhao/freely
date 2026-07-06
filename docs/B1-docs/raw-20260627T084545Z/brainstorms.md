---
b1_id: B1-20260627T084545Z
phase_state: completed
source_raw: raw-20260627T084545Z
produced_candidate: C-20260627T084545Z-A
---
# B1: a2a_tasks agent_id 具体化 + set_assignee fix
## Problem
a2a_tasks 用通用 role 名 (worker/manager) 而非具体 agent_id (worker_03)
set_assignee 用不存在的 _input 参数导致崩溃
## Fix
1. agent_id fallback: --agent-id → role name → 默认值
2. worker 查询 LIKE 'worker_%' 替代 == 'worker'
3. set_assignee 用 subprocess stdin pipe
