# PRD: agent_working + a2a_tasks 使用真实 agent 实例 ID

- issue_id: I-20260719T074532Z-A
- epic: a2a
- story: agent-instance-id

## Goal

agent-table.toml 中声明的 pool 实例（worker_01~10）真正被分配和追踪。Worker 委派时写 agent_working.worker_id 为 "worker_03:session_xxx"，a2a_tasks.agent_id 为 "worker_03"，Runtime 用 LIKE 'worker_%' 发现。

## 实现方案

### 修改 1: freely L6064 — raw_key 正确传入（路径 A）

改前: `agent_assign('${PROJECT_ROOT}', 'develop', 'worker', '$_next_worker', ...)`
改后: `agent_assign('${PROJECT_ROOT}', '${_worker_raw_key:-develop}', 'worker', '$_next_worker', ...)`

与 L13309 一致，从 target_project 提取 raw_key。

### 修改 2: freely L13306 — agent_next_free 替代硬编码（路径 B）

改前: `_worker_agent_id="worker_01"`
改后: 调用 `agent_next_free` 获取实际空闲实例

### 修改 3: a2a_task.py — 新增 --agent-instance 参数

新增参数，允许调用方传入具体实例 ID（如 "worker_03"）。
L1112: `agent_id=args.agent_instance or args.role`

### 修改 4: freely Runtime — worker 发现用 LIKE

改前: `WHERE agent_id = 'worker'`
改后: `WHERE agent_id LIKE 'worker_%'`

### 修改 5: freely prompt 模板 L15537 — 加 --agent-instance

改前: `a2a-exit --state submitted --role worker --summary "..."`
改后: `a2a-exit --state submitted --role worker --agent-instance worker_NN --summary "..."`

## Dev-Loop Handoff

- 修改文件: freely (4处) + a2a_task.py (1处)
- 改动: ~20 行
