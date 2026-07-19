---
b1_id: B1-20260719T074532Z
phase_state: completed
source_raw: raw-20260719T074532Z
source_url: https://github.com/chatterzhao/freely/issues/4006
produced_candidate: C-20260719T074532Z-A
created_at: '2026-07-19'
---

# B1_IBM: a2a task 和 agent_working 使用真实 agent 实例 ID

## Input

- raw issue: raw-20260719T074532Z
- 症状: agent_working.worker_id 始终 NULL，a2a_tasks.agent_id 存 "worker" 而非 "worker_03"
- agent-table.toml 设计意图: worker_id="worker_01" 为基名，pool=10 → worker_01~10 共10实例

## 逐层追踪

### 第1层：agent-table.toml 解析 ✅ 已正确实现

```toml
[[agents]]
role = "worker"
worker_id = "worker_01"     # 基名，NN 从 01 开始
worker_slot = "opencode-apikey-ds-flash-auto"
pool = 10                   # 实例数: worker_01 ~ worker_10
```

### 第2层：DB (freely_db_manager.py) ✅ 已正确实现

`h_aw_next_free` (L1445-1465): 计算空闲实例
```python
all_ids = {f"{prefix}{i:02d}" for i in range(1, pool_size + 1)}
free = sorted(all_ids - occupied)
return {"agent_id": free[0] if free else None}
```
- 生成 worker_01~10，减去 agent_working 中已占用的，返回第一个空闲
- 逻辑正确，已实现

`h_aw_next_free_and_assign` (L1468+): 原子分配
- 消除 agent_next_free 和 agent_assign 之间的 TOCTOU 窗口
- 逻辑正确，已实现

`h_aw_upsert` (L1312-1355): 写入 agent_working
- 将 `{agent_id}:{session_id}` 写入对应 role 列
- 逻辑正确，已实现

### 第3层：Python agent_working.py ✅ 已正确实现

- `agent_next_free(project, role, pool_size)` → DB RPC → 返回 "worker_03"
- `agent_assign(project, raw_key, role, agent_id, ...)` → DB RPC → 写入
- `acp_session_register` → 统一入口，ACP session/new|fork 时调用
- 全部正确，已实现

### 第4层：Shell (freely runtime) ❌ 两处断点

**断点 A: raw_key 硬编码** (freely L6064)
```bash
python3 -c "... agent_assign('${PROJECT_ROOT}', 'develop', 'worker', '$_next_worker', ...)"
                                                      ^^^^^^^
```
传给 agent_assign 的 raw_key 是硬编码的 `'develop'`，不是实际 raw issue key。
→ agent_working 的 worker_id 写入了 `__manager__` 行或不存在行，而不是 raw_key 对应行

**断点 B: agent_next_free 结果未被 a2a-exit 使用** (freely L6034-6037)
```bash
_next_worker=$(python3 -c "from agent_working import agent_next_free;
  print(agent_next_free('${PROJECT_ROOT}', 'worker', 10) or '')")
```
`_next_worker` 已经正确计算（如 "worker_03"），但这个值只用于 agent_assign，没有传给 a2a-exit。
a2a-exit 的 agent_id 仍然是 `args.role`（字符串 "worker"）。

### 第5层：a2a-exit (a2a_task.py) ❌ agent_id 用 role 字符串

```python
# L1112: 当前（刚修复的 --role required）
agent_id=args.role,   # "worker" — 是 role，不是实例 ID
```

a2a-exit 没有 `--agent-instance` 参数来接收具体实例 ID（如 "worker_03"）。
`--role` 是路由类型，"worker" 应该传给 Runtime 发现层，但 agent_id 字段应该是 "worker_03"。

### 第6层：Runtime worker 发现 (freely) ❌ 查询条件过窄

```bash
# Runtime: list --role worker --status submitted
# SQL: WHERE agent_id = 'worker' AND state = 'submitted'
```

当 agent_id 改为 "worker_03" 后，这个查询就查不到了。
需要改为 `WHERE agent_id LIKE 'worker_%'`。

### 第7层：Manager prompt 模板 ❌ 无实例分配指令

Manager AI 的 prompt 中没有"委派前先调用 agent_next_free 获取空闲 worker 实例"的指令。
AI 不知道需要分配具体实例。

## 完整断点清单

| 层 | 功能 | 实现状态 | 问题 |
|---|------|---------|------|
| agent-table.toml | 声明实例 | ✅ | - |
| DB next_free | 计算空闲实例 | ✅ | - |
| DB upsert | 写入分配 | ✅ | - |
| Python agent_working | 封装 RPC | ✅ | - |
| Shell _next_worker | 调用 next_free | ✅ | 结果未被 a2a-exit 使用 |
| Shell agent_assign | raw_key 参数 | ❌ | 硬编码 'develop' |
| a2a_task.py | agent_id 值 | ❌ | 用 role 字符串，无实例参数 |
| Runtime 发现 | 查询条件 | ❌ | 等值匹配，不支持 LIKE |
| Manager prompt | 实例分配指令 | ❌ | 无相关指令 |

## Brainstorm

### Option A: 最小修复 — shell 层接上断点

修复 L6064 raw_key + 让 a2a-exit 接收 `--agent-instance` 参数 + Runtime LIKE 查询。
优点: 改动集中在 shell 层
风险: Manager AI 不知道要传 --agent-instance（prompt 模板没教）

### Option B: shell + prompt + a2a_task 全线修复（采纳）

1. freely L6064: raw_key 从 hardcoded 'develop' 改为实际变量
2. a2a_task.py: 新增 `--agent-instance` 参数，存为 agent_id
3. freely Runtime: worker 发现用 LIKE 'worker_%'
4. Manager prompt 模板: 加 agent_next_free 调用 + a2a-exit --agent-instance worker_NN

### Decision

**采纳 Option B**。5 个断点分布在 3 个文件，需要全线接上才能形成完整链路。

## 改动范围

1. `freely` L6064: `'develop'` → `"$raw_key"`（需确认调用上下文有 raw_key 变量）
2. `a2a_task.py`: 新增 `--agent-instance` 参数，L1112 `agent_id=args.agent_instance or args.role`
3. `freely` Runtime worker 发现: `WHERE agent_id = 'worker'` → `WHERE agent_id LIKE 'worker_%'`
4. `freely` Manager prompt 模板 L15528+: 加 agent_next_free 调用指令和 --agent-instance 参数

## 验证方式

修复后重启 daemon → Manager 委派 → 检查:
- agent_working.worker_id = "worker_03:session_xxx" (非 NULL)
- a2a_tasks.agent_id = "worker_03" (非 "worker")
- Runtime 能发现 worker task → worker_prompts_csv 非空 → worker bridge 启动
