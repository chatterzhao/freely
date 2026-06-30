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

### 全链路标准化，不留 `blocked`

当前 exit kind `worker_blocked` → 映射层 → A2A state `input-required`。留 `worker_blocked` 造成理解摩擦：
- 开发者看到 `worker_blocked` 要想"这是 A2A 的 input-required 吗？"
- `failed`/`canceled` 也可能被理解为"session blocked 了"
- 映射层增加认知负担

**全改**：

```
之前:
  a2a-exit --kind worker_blocked → 映射 'blocked': 'input-required' → state=input-required

之后:
  a2a-exit --kind input_required → 直接 → state=input-required
```

| 维度 | 之前 | 之后 |
|------|------|------|
| exit kind | `worker_blocked` | `input_required` |
| 映射层 | `'blocked': 'input-required'` | 删除，exit kind 直接当 state 用 |
| A2A state | `input-required` | 不变 |
| `failed` | exit kind: `worker_failed` | exit kind: `failed` |
| `canceled` | 不存在 | exit kind: `canceled`（新增） |
| `completed` | exit kind: `completed` | 不变 |

### 改动面（全量）

| 文件 | 改动 |
|------|------|
| `a2a_task.py` State class | `BLOCKED="blocked"` → `INPUT_REQUIRED="input-required"`；新增 `CANCELED="canceled"`；`FAILED` 值不变（已是 `"failed"`） |
| `a2a_task.py` 映射表 (line 661,827) | 删除 `'blocked': 'input-required'` 等映射；exit kind 直接当 state |
| `a2a_task.py` SQLite CHECK | 更新合法 state 列表 |
| `a2a/exit-kind-mapping.md` | `worker_blocked` → `input_required`；新增 `canceled`；删除旧映射表 |
| `a2a/protocol-design.md` | `worker_blocked` → `input_required` |
| `a2a/agent-card-schema.md` | `worker_blocked` → `input_required` |
| `wt-close` 注释 | `blocked` → `input-required` |
| `worker-agent.md` | 状态列表更新 |
| `a2a-exit` 调用处（agent prompt 模板、shell 脚本等） | `--kind worker_blocked` → `--kind input_required` |
| 所有 grep/awk 匹配 `blocked` state 的逻辑 | 更新为 `input-required`

## Decision: 直接用标准状态名

- `blocked` → `input-required`（内部 state 值直接改，不经过映射）
- 新增 `canceled`（manager_01 主动取消时使用）
- exit kind `worker_blocked` 保留不变（内部口令）
- 映射表保留但加注释说明是历史兼容

## Candidate
- candidate_id: C-20260630T021946Z-A
- status: promoted
- milestone: M-20260630T021946Z-A
