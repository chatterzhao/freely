---
b1_id: B1-20260630T021946Z
phase_state: completed
source_raw: raw-20260630T021946Z
source_url: https://github.com/chatterzhao/freely/issues/3639
produced_candidate: C-20260630T021946Z-A
created_at: 2026-06-30
---

# B1_IBM: a2a_tasks 状态对齐 Google A2A 标准

## Input
- 来源：GitHub #3639 raw-20260630T021946Z
- kind：fix
- 触发：supervisor-cycle B1 预研中发现 Freely 使用自定义状态名 `blocked`，Google A2A 标准对应态是 `input-required`，且缺少 `canceled`

## Discovery

### 当前状态实现

a2a_task.py 已有一层映射（line 661, 827）：

```python
# a2a_task.py line 661 — exit_kind → A2A state 映射（已有）
'blocked': 'input-required', 'block': 'input-required',

# line 827 — state 标准化映射（已有）
'blocked': 'input-required', 'rejected': 'failed', 'consumed': 'completed'
```

**已有映射层**：内部 `worker_blocked` exit kind → A2A state `input-required`。但映射之前的内部状态值仍然是 `blocked`，没有被标准化。

### 改动面扫描

| 文件 | 影响 | 改动类型 |
|------|------|---------|
| `a2a_task.py` State class | `BLOCKED = "blocked"` | → `INPUT_REQUIRED = "input-required"`；新增 `CANCELED = "canceled"` |
| `a2a_task.py` SQLite CHECK | `CHECK (state IN (...))` | 更新列表 |
| `a2a_task.py` 映射表 (line 661,827) | `'blocked': 'input-required'` | 反向：`'input-required': 'input-required'`（自身映射，无变化语义） |
| `a2a/exit-kind-mapping.md` | `worker_blocked` → `input-required` 映射 | exit kind 名不需要改（`worker_blocked` 是内部 exit kind，不等于 A2A state），但文档需澄清 |
| `a2a/protocol-design.md` | `worker_blocked` 引用 | 更新为 `worker_input_required` 或保留并加注释 |
| `a2a/agent-card-schema.md` | `worker_blocked` 引用 | 同上 |
| `wt-close` line 980 注释 | `completed/blocked` | → `completed/input-required` |
| `worker-agent.md` | 状态说明 | 更新可用 state 列表 |
| SQLite DB schema (freely.db) | 已有数据 | 不迁移历史数据；新 task 用新 state |

### 关于 `worker_blocked` exit kind

exit kind 是 **Freely 内部约定**（Worker 的 `a2a-exit --kind worker_blocked`），A2A state 是 **A2A 协议标准**（`input-required`）。映射关系：

```
Worker 执行: a2a-exit --kind worker_blocked
  → a2a_task.py 映射: 'worker_blocked' → 'input-required'
  → a2a_tasks 表写入: state = 'input-required'
  → A2A Server 对外暴露: Task.state = 'input-required'  ← 对齐标准
```

**exit kind 不需要改**。`worker_blocked` 是给 Worker agent 的口令（"我阻塞了"），`input-required` 是 A2A 协议标准状态名。内部映射层保持不变。

### 改什么 vs 不改什么

**改**：
- `a2a_task.py`: State class 常量名，SQLite CHECK，state 值
- `a2a/protocol-design.md`: 状态说明中的 `blocked` → `input-required`
- `wt-close`: 注释中的 `blocked` → `input-required`
- 新增 `canceled` state + 对应 exit kind

**不改**：
- `worker_blocked` exit kind 名（内部口令，不对外）
- 映射表逻辑（已有 `'blocked': 'input-required'` 映射，保持不变）
- wt-close UI 消息中的 "blocked"（那是英文动词 "被阻塞"，不是状态名）

## Problem

`blocked` 是非标准状态名。Google A2A 标准对应态是 `input-required`。Freely 在内部使用 `blocked` 然后在映射层转 `input-required`——绕了一圈。应该直接使用标准名。

缺少 `canceled` 终止态。当前只有 `completed` 和 `failed`，manager_01 主动取消时只能复用 `failed` 或 `completed`，语义不清。

## Decision: 直接用标准状态名

- `blocked` → `input-required`（内部 state 值直接改，不经过映射）
- 新增 `canceled`（manager_01 主动取消时使用）
- exit kind `worker_blocked` 保留不变（内部口令）
- 映射表保留但加注释说明是历史兼容

## Candidate
- candidate_id: C-20260630T021946Z-A
- status: promoted
- milestone: M-20260630T021946Z-A
