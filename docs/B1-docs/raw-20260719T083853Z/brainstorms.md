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

## 关键区分

### 新建 task vs 更新已有 task

a2a-exit 有两种调用模式：

| 场景 | 参数 | worktree/branch/raw-key |
|------|------|------------------------|
| Manager 委派 Worker（新建） | `--state submitted --role worker --worktree ...` | **必须填** |
| Worker 退出（更新已有 task） | `--task-id <id> --state completed --role worker` | **不需要**（已有 task 继承原有值） |
| Manager 自身状态 | `--state submitted --role manager` | 不需要 |

校验仅针对**新建 worker task**（`--role worker` + 无 `--task-id`）。

### role vs agent_id（不要混淆）

- `role` = 角色类型：`"worker"`（字符串，用于 Runtime LIKE 发现）
- `agent_id` = 具体实例：`"worker_03"`（格式 `{role}_\d{2}`，如 `worker_01`~`worker_10`）
- a2a_tasks.agent_id：创建时写 role 字符串（Manager AI 不知道哪个实例空闲），Runtime 分配后更新为实例 ID
- agent_working.worker_id：写 `"worker_03:session_xxx"` 格式（实例+session）

## Brainstorm

### 三层防线设计

**L1: a2a_task.py handler（最早拦截，报错最精确）**

`a2a-exit` handler (L1092-1125) 在 `c.create()` 前校验：

```python
if args.role == "worker" and not existing_task_id:
    # 新 worker task 必须填
    if not worktree.strip():   error "--worktree required for new worker task"
    if not branch.strip():     error "--branch required for new worker task"
    if not raw_key.strip():    error "--raw-key required for new worker task"
    if not summary.strip():    error "--summary required for new worker task"
    if state != "submitted":   error "state must be 'submitted', got '{state}'"
```

错误消息精确指到缺失的字段名。

**L2: DB insert 层（兜底，防止绕过 L1 的调用路径）**

`h_a2a_task_insert` (L1048-1083) 在 INSERT 前检查：

```python
agent_id = params.get("agent_id","")
if agent_id.startswith("worker"):
    if not params.get("worktree","").strip():   return error
    if not params.get("branch","").strip():     return error
    if not params.get("raw_key","").strip():    return error
    if not params.get("message","").strip():    return error
```

**L3: agent_assign 层（agent_working 写入检查）**

`agent_assign` (agent_working.py L39-67) 检查：

```python
if role == "worker":
    if not agent_id:  return error "agent_id required for worker"
    if not re.match(r'^worker_\d{2}$', agent_id):
        return error f"agent_id '{agent_id}' invalid, expected 'worker_NN' format"
```

`worker_NN` 格式：两位数字，`worker_01`~`worker_10`（与 `h_aw_next_free` 的 `{prefix}{i:02d}` 一致）。

### 不在此 scope 的

- DB schema migration（agent_working.worker_id → NOT NULL）——独立 issue，需要处理 `__manager__` 行的兼容
- 清理历史僵尸 task（55 个空 message worker task）——独立 cleanup issue
- Runtime `worker deferred` 错误消息改进——独立 issue

### Decision

L1+L2+L3 三层全部实现，加 prompt 模板补全。L1 对新建 worker task 做校验（不拦更新已有 task），L2 做 DB 层兜底，L3 做 agent_id 格式校验。
