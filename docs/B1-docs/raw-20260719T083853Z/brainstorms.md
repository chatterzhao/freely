---
b1_id: B1-20260719T083853Z
phase_state: completed
source_raw: raw-20260719T083853Z
source_url: https://github.com/chatterzhao/freely/issues/4008
produced_candidate: C-20260719T083853Z-A
created_at: '2026-07-19'
---

# B1_IBM: a2a task + agent_working 写入前校验——三层拦截

## 证据

Round 094 Manager 委派 Worker 时创建的 task `36fa73f1`：
```
agent_id='worker'  state='input-required'  worktree=''  branch=''  raw_key=''
```

整条写入链三层全通、零拦截：

```
Manager AI:  a2a-exit --state submitted --role worker --summary "..."
                  ↓ 没传 --worktree --branch --raw-key
argparse:     worktree=""  branch=""  raw_key=""            ← default=""
                  ↓ 无校验 → 直接 create
a2a-exit:     c.create(worktree="", branch="", raw_key="")
                  ↓
A2A Server:   h_a2a_task_insert → params.get("worktree","") → INSERT
                  ↓
SQLite:       写入成功。NOT NULL 接受 ''。无 CHECK 约束。
                  ↓
Runtime:      读到 worktree='' → worker deferred: worktree missing
```

## 每条路径的精确问题

### 写入路径

| 位置 | 代码 | 问题 |
|------|------|------|
| a2a_task.py L834 | `--worktree default=""` | 不传就是空，不报错 |
| a2a_task.py L835 | `--branch default=""` | 同上 |
| a2a_task.py L833 | `--raw-key default=""` | 同上 |
| a2a_task.py L1112 | `c.create(worktree=..., branch=..., raw_key=...)` | 无校验，空值直传 |
| freely_db_manager.py L1071 | `params.get("worktree","")` | 无校验，空值直写 |
| freely_db_manager.py L1072 | `params.get("branch","")` | 同上 |

### 拦截路径

| 位置 | 拦截存在？ | 错误消息 |
|------|----------|---------|
| a2a_task.py a2a-exit handler | ❌ 无 | 无 |
| h_a2a_task_insert | ❌ 无 | 无 |
| agent_assign | ❌ 无（worker_id=NULL 也接受） | 无 |
| SQLite CHECK | ❌ 无 | 无 |

### role vs agent_id 混淆

- a2a_tasks.agent_id 存 `"worker"`（role 字符串）——用于 Runtime 发现（LIKE 匹配）
- agent_working.worker_id 存 `"worker_03:session_id"`（实例 ID + session）——用于追踪
- 两者职责不同，不应混淆。a2a_tasks.agent_id 在 task 创建时写 role 字符串（Manager AI 不知道哪个实例空闲），Runtime 分配实例后再更新

## Brainstorm

### 三层防线设计

需要精确的错误消息让调用方知道缺了什么：

**L1: argparse 层（最早拦截）**
`--worktree`、`--branch`、`--raw-key` 改为 `required=True`（仅当 `--role worker` 时）

→ 问题：argparse 不支持条件 required。需要用 `required=False` + handler 内手动校验。

**方案**：handler 内校验，报错示例：
```
{"ok": false, "error": "worker task requires: --worktree (empty)"}
{"ok": false, "error": "worker task requires: --branch (empty)"}
{"ok": false, "error": "new worker task state must be 'submitted', got 'input-required'"}
```

**L2: DB insert 层（写入前检查）**
`h_a2a_task_insert` 在 INSERT 前检查：agent_id ∈ {worker, worker_*} 时 worktree/branch/raw_key 非空。

→ 报错示例：
```
{"error": "worker task rejected: worktree is empty"}
```

**L3: agent_assign 层（agent_working 写入检查）**
`agent_assign` 检查 role=worker 时 agent_id 非空且格式正确（`worker_NN`）。

→ 报错示例：
```
{"error": "worker agent_id invalid: 'worker', expected 'worker_NN' format"}
```

### Decision

三层全上。L1 最先拦截、报错最精确。L2/L3 兜底防止绕过 L1 的调用路径。

另外 prompt 模板也要补全 `--worktree --branch --raw-key`（双保险：AI 知道要传 + 传错了 L1 拦住）。
