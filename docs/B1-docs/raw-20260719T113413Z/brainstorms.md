---
b1_id: B1-20260719T113413Z
phase_state: completed
source_raw: raw-20260719T113413Z
source_url: https://github.com/chatterzhao/freely/issues/4012
produced_candidate: C-20260719T113413Z-A
created_at: '2026-07-19'
---

# B1: agent_working 写入时 slot 和 agent_id 从 agent-table 正确解析

## 证据

自由重启后 agent_working 表实际数据：

```
raw_key=20260719T070107Z  worker_id=NULL  slot=claude-apikey-ds-flash-auto
raw_key=20260719T070409Z  worker_id=NULL  slot=claude-apikey-ds-flash-auto
```

agent-table.toml 配置：
- worker slot = opencode-apikey-ds-flash-auto, worker_id = worker_01 (pool=10)

**写入的 slot 是 claude（Manager的tool），不是 opencode。worker_id 是 NULL。**

## 全仓追踪

### L13110 (fork 路径) — ❌ slot 硬编码 + agent_id 可能为空

```bash
acp_session_register('${manager_project}', '${_raw_key:-${agent_id}}', 'worker',
  '${agent_id}', session_id='${_session_id}',
  slot='${slot:-claude}',    # ← $slot 未设置→默认"claude"!
  worktree='${target_project}')
```

问题：
1. `slot='${slot:-claude}'` — $slot shell变量从未设置 → 永远fallback到"claude"
2. `${agent_id}` — 可能是"worker"(role string),不是"worker_01"(instance ID)
3. L13109 guard `[[ -n "$agent_id" ]]` — agent_id="worker"会通过,但L3拒绝
4. `|| true` 吞掉L3错误 → worker_id写入失败无感知

### L6064 (旧 launch 路径) — ❌ 无 slot 参数

```bash
agent_assign('${PROJECT_ROOT}', '${_worker_raw_key:-develop}', 'worker',
  '$_next_worker', worktree='${target_project}')
# ↑ 没有 slot= 参数!
```

`$_next_worker` 来自 agent_next_free → "worker_01" ✅ 格式正确。
但缺 slot，agent_working.slot 不会被更新。

### L13328 (新 launch 路径) — ✅ 已正确

```bash
agent_assign('${PROJECT_ROOT}', '${_worker_raw_key:-develop}', 'worker',
  '${_worker_agent_id}', worktree='${target_project}', slot='${_worker_slot}')
```

slot 和 agent_id 都已正确传入。这是我们的跨 tool fix 添加的路径。

## agent-table.toml 参考

```toml
[[agents]]
role = "manager"     manager_id = "manager_01"  manager_slot = "claude-apikey-ds-flash-auto"  pool = 1
role = "worker"      worker_id  = "worker_01"   worker_slot  = "opencode-apikey-ds-flash-auto" pool = 10
role = "reviewer"    reviewer_id= "reviewer_01" reviewer_slot= "cline-account-ds-flash-free-auto" pool = 99
```

每个 role 的 slot 从 `agent-table-query --get-slot {role}_01` 获取。
pool > 1 时 agent_id 通过 agent_next_free 获取空闲实例。

## Fix

三条 agent_assign 调用路径统一：
1. slot: agent-table-query --get-slot ${role}_01
2. agent_id: Manager="manager_01", Worker=agent_next_free, Reviewer=类似
3. 错误处理: `|| log_warn "agent_assign failed"` 替代 `|| true`
