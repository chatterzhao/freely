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

## Refactoring Plan: 12 → 1

### Before/After 对照

#### 1. freely shell — Manager session register

**Before** (`_persist_session_anchor_early`, line 4033-4055):
```bash
python3 -c "
from agent_working import agent_assign
agent_assign('${project}', '__manager__', 'manager', 'manager_01',
             worktree='${project}', branch='develop',
             session_id='${CLAUDE_SESSION_ID_CURRENT:-}')  # ← 可能空
"  # ← 缺 slot
```

**After**:
```bash
python3 -c "
from agent_working import acp_session_register
acp_session_register('${project}', '__manager__', 'manager', 'manager_01',
                     session_id='${TOOL_SESSION_ID_CURRENT:-}',
                     slot='${AGENT_AI_TOOL}',           # ← 新增
                     worktree='${project}', branch='develop')
"
```

#### 2. watchdog — _handle_needs_reviewer (reviewer session decision)

**Before** (70 行逻辑，手动判断 alive→prompt / dead→fork→new):
```python
# Step 1: Check alive session
existing = agent_list_by_raw_key(project, raw_key)
if existing and existing.get("reviewer_id"):
    sid = agent_get_session(project, raw_key, "reviewer")
    if sid:
        if _acp_session_prompt(project, sid, task_msg):
            return     # alive → prompt
        # prompt failed → return (don't allocate second reviewer)
    else:
        _create_reviewer_session(project, raw_key, rid, ...)  # dead → fork→new
    return
# Step 2: Allocate next free
reviewer_id = agent_next_free(project, "reviewer", 99)
_create_reviewer_session(project, raw_key, reviewer_id, ...)
```

**After**:
```python
sid, op = acp_session_connect(
    project, raw_key, "reviewer", reviewer_id,
    slot=reviewer_slot,           # ← 新增 slot 匹配
    message=task_msg,
    force_new=(reason == NEEDS_REVIEW_GATE)  # gate → new
)
# 内部自动决策: prompt > resume > fork(Mgr) > new
```

#### 3. watchdog — _handle_needs_worker (worker session decision)

**Before** (50 行逻辑，手动判断 prompt→fork→new→delegate):
```python
sid = agent_get_session(project, raw_key, "worker")
if sid:
    if _acp_session_prompt(project, sid, verdict_msg): return
# Try fork from Manager
session_id = _acp_session_fork(project, "manager", "worker", wid, raw_key)
if session_id:
    agent_assign(project, raw_key, "worker", f"{wid}:{session_id}")
else:
    new_sid = _acp_session_new(project, "worker", wid)
    agent_assign(project, raw_key, "worker", f"{wid}:{new_sid}")
```

**After**:
```python
sid, op = acp_session_connect(
    project, raw_key, "worker", wid,
    slot=worker_slot,
    message=verdict_msg
)
# 内部: prompt(alive) → resume(dead+slot匹配) → fork(Mgr) → new
```

#### 4. watchdog — _handle_needs_manager (manager 被唤醒)

**Before** (40 行逻辑):
```python
sid = agent_get_session(project, "__manager__", "manager")
if sid:
    if _acp_session_prompt(...): return
# No alive → session/new
new_sid = _acp_session_new(project, "manager", "manager_01")
agent_assign(project, "__manager__", "manager", f"manager_01:{new_sid}")
```

**After**:
```python
sid, op = acp_session_connect(
    project, "__manager__", "manager", "manager_01",
    slot=manager_slot,
    message=mgr_msg
)
# 内部: prompt(alive) → resume(dead+slot匹配) → new
# Manager 不 fork（它是 fork 的源）
```

#### 5. freely shell — Worker launch (line 13209)

**Before** (直接 fork，无 session 决策):
```bash
export SESSION_PARENT_ID="${CLAUDE_SESSION_ID_CURRENT:-}"
python3 run-acp-prompt.py --launch-kind fork --bridge-socket ...
# agent_assign 由 _persist_session_anchor_early 在 worker daemon 中调用
```

**After**:
```bash
python3 -c "
from agent_working import acp_session_connect
sid, op = acp_session_connect(
    '${target_project}', '${raw_key}', 'worker', '${worker_id}',
    slot='${worker_slot}',
    message='${prompt_file}'  # task prompt as message
)
# run-acp-prompt.py 不再自己选 session 操作，传 launch_kind=connect
"
```

#### 6. freely shell — _ensure_reviewer_agent (line 18764)

**Before** (直接 session/new via bridge socket):
```python
req = json.dumps({'method':'session/new','params':{'sessionId':...,'cwd':...}})
# 之后 agent_assign(reviewer, session_id=sid) — 缺 worktree/branch/slot
```

**After**:
```python
sid, op = acp_session_connect(
    project, raw_key, "reviewer", reviewer_id,
    slot=reviewer_slot,
    worktree=worktree, branch=branch
)
```

#### 7. run-acp-prompt.py — session dispatch (line 420-495)

**Before** (80 行 if/elif 分发 fresh/resume/fork/prompt):
```python
if launch_kind == "resume":
    session_result = client.request("session/resume", ...)
elif launch_kind == "prompt":
    session_id = resume_target
elif launch_kind == "fork":
    session_result = client.request("session/fork", ...)
else:  # fresh
    session_result = client.request("session/new", ...)
```

**After** (新增 `launch_kind=connect` 模式):
```python
if launch_kind == "connect":
    # Session 操作由上游 acp_session_connect 决策
    # run-acp-prompt.py 只需执行指定的操作
    session_result = _execute_given_operation(args.operation, args.session_id, ...)
else:
    # 兼容旧 launch_kind (fresh/resume/fork/prompt) 逐步迁移
    ...
```

### 删除的代码

| 删除 | 文件 | 行数 |
|------|------|------|
| `_should_use_fork()` | watchdog_sse.py | ~25 行 |
| `_create_reviewer_session()` | watchdog_sse.py | ~50 行 |
| `_acp_session_new()` | watchdog_sse.py | ~12 行 |
| `_acp_session_fork()` | watchdog_sse.py | ~30 行 |
| `_acp_session_resume()` | watchdog_sse.py | ~15 行 |
| `_acp_session_prompt()` | watchdog_sse.py | ~10 行 |
| session 分发 if/elif | watchdog `_handle_needs_*` | ~100 行 |
| agent_assign 裸调用 | watchdog + freely | ~8 处 |

### 新增的代码

| 新增 | 文件 | 行数 |
|------|------|------|
| `acp_session_connect()` | agent_working.py | ~80 行 |
| `acp_session_register()` | agent_working.py | ~15 行 |
| slot 列 | freely_db_manager.py | 1 行 ALTER |
| 命名替换 | 3 文件 | 11 处 |

## 关联 Issue: raw-20260704T080808Z (多 bridge 并行)

两个 issue 协同设计，本期预留扩展点:

### 本期 (raw-20260704T064539Z) 的设计预留

`acp_session_connect()` 的 `slot` 参数即为后续 bridge 路由的 key:
- 单 bridge (本期): slot → base_tool → 唯一的 bridge (忽略 base_tool 差异)
- 多 bridge (下期): slot → base_tool → 对应的 bridge socket

```python
def acp_session_connect(project, raw_key, role, agent_id, slot, ...):
    base_tool = _extract_base_tool(slot)  # opencode-apikey-xxx → opencode
    bridge_socket = _resolve_bridge_socket(project, base_tool)  # 本期: 返回唯一 socket
    # 下期: _resolve_bridge_socket 根据 base_tool 返回不同 socket
```

### 下期 (raw-20260704T080808Z) 需解决

1. daemon 启动时扫描 agent-table，为每个不同 base_tool 启动独立 bridge
2. bridge socket 命名为 `/tmp/freely-acp-{project_hash}-{base_tool}.sock`
3. fork 跨 slot 策略: 同 bridge 内跨 slot fork? 还是必须同 slot?
4. bridge 生命周期: 与 manager bridge 一致（随 daemon 启停）

## 多 Bridge 协作分析

### 当前 vs 重构后

```
当前 (1 bridge per project):
  /tmp/freely-acp-{hash}.sock  ← 所有 agent 共用

重构后 (1 bridge per base_tool):
  /tmp/freely-acp-{hash}-opencode.sock  ← manager/worker/reviewer 用 opencode 的走这个
  /tmp/freely-acp-{hash}-claude.sock    ← 有 agent 用 claude 才启动
  /tmp/freely-acp-{hash}-codex.sock     ← 同上
```

### daemon 启动流程

```
1. load_config → 读 agent-table.toml
   获取所有 role 的 slot:
     manager_slot  = opencode-apikey-ds-flash-auto
     worker_slot   = opencode-apikey-openai-gpt-auto
     reviewer_slot = claude-apikey-ds-flash-auto

2. 提取所有唯一 base_tool: {opencode, claude}

3. 为每个 base_tool 调用 _ensure_acp_bridge_running(base_tool):
     → opencode bridge: binary=opencode, args=acp, config=...
     → claude bridge:   binary=claude-agent-acp, config=...

4. bridge 注册表 (内存或 agent_working):
     opencode → /tmp/freely-acp-{hash}-opencode.sock
     claude   → /tmp/freely-acp-{hash}-claude.sock
```

### acp_session_connect 的 bridge 路由

```python
def acp_session_connect(project, raw_key, role, agent_id, slot, ...):
    base_tool = _extract_base_tool(slot)  # slot → opencode / claude
    bridge = _resolve_bridge_socket(project, base_tool)
    
    # 后续所有操作 (new/fork/resume/prompt) 都走这个 bridge
    
    # fork 约束:
    #   同 bridge + 同 slot → fork ✅ (最佳: 完全同配)
    #   同 bridge + 不同 slot → new ⚠️ (不同 settings.json, fork 可能继承错配置)
    #   不同 bridge → new ❌ (不同二进制, 不可能 fork)
```

### fork 策略细化

| parent slot | child slot | base_tool | bridge | fork? | 理由 |
|------|------|------|------|:---:|------|
| opencode-ds-flash | opencode-ds-flash | 同 | 同 | ✅ fork | 完全相同, 最佳 |
| opencode-ds-flash | opencode-openai-gpt | 同 | 同 | ❌ new | 不同 settings.json |
| opencode-* | claude-* | 不同 | 不同 | ❌ new | 不同二进制 |

### start-lead-agent.sh 的变化

当前 worker prompt 不传 slot → agent-table 查询得到 slot → 但 bridge 已定。

重构后:
```
start-lead-agent.sh
  1. 从 worker worktree 的 agent-table 查该 role 的 slot
  2. slot → base_tool → bridge socket
  3. acp_session_connect(slot=..., base_tool=...)
     → 内部用正确的 bridge 创建 session
```

### 本期 (raw-20260704T064539Z) 要做的

- `_resolve_bridge_socket(project, base_tool)` 签名预留 base_tool 参数
- 本期 base_tool 参数被忽略，始终返回唯一 bridge
- `acp_session_connect` 所有 session 操作通过 `_resolve_bridge_socket` 获取 bridge

### 下期 (raw-20260704T080808Z) 要做的

- daemon start 时扫描 agent-table 所有 base_tool
- `_ensure_acp_bridge_running` 改为 per-base_tool 调用
- bridge socket 命名改为 `/tmp/freely-acp-{hash}-{base_tool}.sock`
- `_resolve_bridge_socket` 实现 base_tool → socket 映射
- fork 跨 slot 检测

### 两个 issue 的关系

```
raw-20260704T064539Z (本期): 统一 session 管理
  ↓ 前提
raw-20260704T080808Z (下期): 多 bridge 并行

本期不依赖下期，但需预留扩展点。
下期依赖本期 — acp_session_connect 已抽象好，只需改 bridge 路由。
```

### 是否需要并行开工位？

不需要。本期是前提——先统一 session 管理，再在统一的基础上做多 bridge。两个 issue 串行，本期设计预留足够。
