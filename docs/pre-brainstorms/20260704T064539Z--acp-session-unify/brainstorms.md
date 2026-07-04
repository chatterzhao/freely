---
b1_id: B1-20260704T064539Z
phase_state: completed
source_raw: raw-20260704T064539Z
source_url: https://github.com/chatterzhao/freely/issues/3726
produced_candidate: C-20260704T064539Z-A
created_at: 2026-07-04
---

# B1_IBM: 统一 ACP session 管理方法

## Input
- raw-20260704T064539Z (GitHub #3726)

## Problem

12 个分散的 session 操作调用点，无统一决策逻辑。agent_working 无 slot 列，无法安全 resume。每个 agent 都需要 prompt/resume/fork/new 全路径。

## Brainstorm: 穷举场景矩阵

### 决策树

```
acp_session_connect(project, raw_key, role, agent_id, slot,
                    message=None, force_new=False)
  → (session_id, operation_used)

  # ── 0. 明确要求 new ──
  if force_new:
      → session/new (调用方显式要求，如 gate review、跨 tool)
      return

  # ── 1. 查 agent_working ──
  existing = agent_working.get(raw_key, role)
  if existing and existing.session_id and existing.slot:
      slot_ok = (existing.slot == slot)
      # ── 2. slot 变了？ ──
      if not slot_ok:
          → session/new  (安全: 不同配置不能 resume/fork)
          return
      # ── 3. session alive? ──
      is_alive = _acp_bridge.ping(existing.session_id)
      if is_alive:
          if message:
              → session/prompt(message)  【最快: alive + 有消息】
          else:
              → return existing.session_id  【已连接】
      else:
          if message:
              → session/resume + session/prompt(message)  【恢复上下文 + 投递】
          else:
              → session/resume  【仅恢复，保留上下文】
      return

  # ── 4. 无 session，尝试 fork ──
  same_tool = (_base_tool(slot) == _base_tool(mgr_slot))
  if same_tool and mgr_session_exists():
      if role == "reviewer" and parent_role == "worker":
          # 禁止: 不能 fork Worker（自评自审）
          → session/new + log("fork from worker forbidden, using new")
      else:
          → session/fork(from=manager)  【缓存命中 + 独立公正】
  else:
      → session/new  【跨 tool 或 mgr 无 session，必须 new】
```

### 穷举场景表

| # | agent_working 有记录 | slot 匹配 | session alive | 同 tool | message | force_new | role 特殊 | 操作 | 缓存 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|------|------|:---:|
| 1 | ✓ | ✓ | ✓ | - | ✓ | - | - | **session/prompt** | ✅ |
| 2 | ✓ | ✓ | ✓ | - | ✗ | - | - | 直接返回 session_id | - |
| 3 | ✓ | ✓ | ✗ | - | ✓ | - | - | **session/resume** + prompt | ✅ |
| 4 | ✓ | ✓ | ✗ | - | ✗ | - | - | **session/resume** | ✅ |
| 5 | ✓ | ✗ | - | - | - | - | - | **session/new** | ❌ 安全 |
| 6 | ✗ | - | - | ✓ | - | - | non-gate | **session/fork**(Mgr) | ✅ |
| 7 | ✗ | - | - | ✗ | - | - | - | **session/new** | ❌ 跨 tool |
| 8 | - | - | - | - | - | ✓ | - | **session/new** | ❌ 显式 |
| 9 | - | - | - | - | - | - | reviewer gate | **session/new** | ❌ 中立 |
| 10 | ✓ | ✓ | ✓ | - | ✓ | - | reviewer fork Worker | **session/new** + 日志 | ❌ 防作弊 |

### 回退 new 的场景

```
明确意图 new (正常路径):
  #5   — slot 变了，必须 new
  #7   — 跨 tool，无法 fork
  #8   — force_new=True，调用方显式要求
  #9   — reviewer gate review，强制独立

未知/异常回退 (需打日志):
  #10  — reviewer 尝试 fork Worker，被拦截
  #11  — prompt 失败 (session 意外死亡) → 降级 resume → 再失败 → new
  #12  — resume 失败 (bridge 问题/session 损坏) → 降级 new
  #13  — fork 失败 (mgr session 不可用/bridge 问题) → 降级 new
  #14  — 任何未预见的组合 → 降级 new + 日志
```

### 回退日志格式

```python
# 异常回退 (session 操作失败，非预期)
log_warn(f"[acp-session] {operation} failed for {role}/{agent_id} "
         f"(session={sid[:16]}...), falling back to session/new: {error}")

# 未知场景回退 (决策树未覆盖的组合)
log_warn(f"[acp-session] no optimal path: role={role} slot={slot} "
         f"has_session={has_session} slot_match={slot_match} "
         f"alive={is_alive} same_tool={same_tool} force_new={force_new}, "
         f"falling back to session/new")
```

### 三个角色的典型路径

**Manager:**
```
freely start (首次)    → 场景 #7 (无记录) → session/new
freely restart (不变)  → 场景 #4 (有记录+slot匹配+dead) → session/resume ✅缓存
freely restart (换slot)→ 场景 #5 (slot不匹配) → session/new
```

**Worker:**
```
Manager 委派 (首次)    → 场景 #6 (同tool) → session/fork(Mgr) ✅缓存
Manager 委派 (跨tool)  → 场景 #7 (跨tool) → session/new
watchdog 发任务 (活)   → 场景 #1 (alive+message) → session/prompt ✅最快
watchdog 发任务 (死)   → 场景 #3 (dead+message) → session/resume+prompt ✅恢复
```

**Reviewer:**
```
Worker 请求 review (首次) → 场景 #6 (fork Mgr) → session/fork(Mgr) ✅独立
Worker 请求 review (gate) → 场景 #9 (gate强制) → session/new ✅中立
watchdog 发任务 (活)      → 场景 #1 (alive+message) → session/prompt
watchdog 发任务 (死)      → 场景 #3 (dead+message) → session/resume+prompt
```

### 补充发现

1. agent_working 需要 `slot` 列 (schema 变更)
2. `CLAUDE_SESSION_ID_CURRENT` → `TOOL_SESSION_ID_CURRENT`
3. DB upsert UPDATE 时也应更新 worktree/branch/test_*

## Decision

核心交付:
1. `acp_session_connect()` — 穷举场景的决策树
2. 明确路径: prompt(1/2) > resume(3/4) > fork(6) > new(5/7/8/9)
3. 回退路径: 所有异常降级到 new + 日志
4. agent_working + slot 列
5. Reviewer 防 fork Worker

## Candidate
- candidate_id: C-20260704T064539Z-A
- status: promoted
- milestone: M-20260704T064539Z-A
