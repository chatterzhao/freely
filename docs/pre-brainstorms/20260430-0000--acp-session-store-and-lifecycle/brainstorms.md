# Brainstorms — ACP Session Store & Lifecycle

## Context

2026-04-30 调试 `freely start` 启动异常，追踪到一条 session ID 污染 + 恢复链路断裂的 bug 链：

1. `run-acp-prompt.py` 向 stdout 输出 `session id: <uuid> (resumed)` — 注解混入 ID
2. `monitor-ai-acp.sh` sed 提取时未 strip 注解 → `LAST_TOOL_SESSION_ID="<uuid> (resumed)"`（非合法 UUID）
3. `select_launch_kind` fallback 到 `_find_recent_session_from_tool_dir` — `find | sort` 字母序而非 mtime 序，反复恢复到同一"坏"session
4. 坏 session resume 失败 → 标记 auth_or_rate_limit → 停 runtime → 重启 → 循环

此外，session 恢复链路上还有更本质的问题：
- ACP bridge 重启后 session 丢失（session 在 claude-agent-acp 内存中，非持久）
- 恢复依赖 cycle log 文本解析（不可靠）和工具目录 `~/.claude/projects/{slug}/` 扫描（多 session 混杂，认错 session）
- session 的权威来源应该是 ACP 协议 `session/new` 或 `session/resume` 的返回值，而不是任何文件系统扫描

## 决定

吸收业界 ACP session 管理的最佳实践，以 CLI-first + SQLite 方式重构 session 身份存储和生命周期管理，修复当前 bug 链的同时不打折现有功能。

## 边界

- 只改 session 身份层（存储、读写、恢复），不动 ACP bridge 的 transport 层
- 不动 `session-state.env` 中的运行时计数器（rate limit tracking、restart storm、checkpoint drift 等）
- 不动 `cc` / `codex` / `iflow` 等非 ACP 工具适配器
- 保持 CLI-first：所有操作通过 `python3 session-store.py <subcommand>` 完成，freely 调用 CLI 而非直接操作 DB
- 保持项目隔离：`.freely/freely.db` per-project，SQLite WAL 模式
- 代码中不出现外部项目名称

## 功能面

### P0 — Session 身份权威存储（修复 bug 链）

**目标：** Session ID 永远 clean，来源单一，不依赖任何文本解析或文件系统扫描。

| 功能 | 描述 | 映射到 freely |
|---|---|---|
| 权威 ID 源 | ACP `session/new` / `session/resume` 返回的 UUID | `run-acp-prompt.py` 第 1 行 stdout 输出 clean UUID（机器可读），第 2 行输出带注解的人类可读行 |
| 结构化存储 | session 身份存入 SQLite | `session-store.py upsert` 写入 `freely.db` sessions 表 |
| 主动读取 | 启动时从 DB 读 session ID 决定 resume/fresh | `session-store.py get-active` 返回 clean UUID，`select_launch_kind` 调用 |
| 生命周期标记 | session 完成/失败后更新状态 | `session-store.py complete --status completed|failed` |

**删除项：**
- `_find_recent_session_from_tool_dir` 在 ACP 路径的调用
- `extract_tool_session_id_from_log` 的 ACP 分支
- `select_launch_kind` 中 cycle log 文本解析 fallback
- `_write_acp_session_state`（用 session-store.py 替代）

### P1 — Session 恢复链路（双模式 resume）

**目标：** 根据场景选择最优的 resume 策略，最大化 cache hit 率。

**核心映射：freely 已经实现了两种 resume，对照如下：**

| 模式 | 描述 | ACP RPC | 使用场景 |
|---|---|---|---|
| **native resume** | 直接恢复到已知 session，provider 侧 cache hit | `session/resume <session_id>` | session 仍在 bridge 内存中，上次正常结束 |
| **recreated** | session 丢失后重建新 session，通过 prompt/handoff 恢复上下文 | `session/new`（resume 失败后 fallback） | bridge 重启、session 过期、resume 失败 |

**run-acp-prompt.py 已实现的 fallback 逻辑（L334-352）：**
```python
if launch_kind == "resume" and resume_target:
    try:
        session_result = client.request("session/resume", ...)  # native
        # success → cache hit
    except:
        session_result = client.request("session/new", ...)      # recreated
        # fallback → new session, context via prompt
```

**session-store 的职责：** 正确记录哪种模式成功了，下次启动据此决策。

| 上次结果 | session-store 状态 | 下次启动 |
|---|---|---|
| native resume 成功 | status=active, resume_mode=native | `get-active` → 有 → 下次继续 native resume |
| recreated（resume失败后fallback new） | status=active, resume_mode=recreated | `get-active` → 有 → 下次 native resume（新 session 已在 bridge 中） |
| 严重错误（auth/rate_limit） | status=failed, error_reason=auth_or_rate_limit | `get-active` → 无（跳过 failed）→ fresh |
| bridge 重启导致 session 丢失 | status=failed, error_reason=bridge_session_lost | `get-active` → 无 → fresh |

**关键洞察：** `get-active` 返回 status=active 的 session → 用 native resume（大概率 cache hit）。如果 native resume 又失败了（bridge 又重启了），`run-acp-prompt.py` 的 try/except 再次 fallback 到 recreated → session-store 更新为新 session ID。这个自愈循环不依赖 cycle log 解析。

| 功能 | 描述 | 映射到 freely |
|---|---|---|
| 双模式 resume | native resume（session/resume） + recreated（session/new fallback） | `run-acp-prompt.py` **已实现**，session-store 记录结果 |
| 场景决策 | 有 active session → native；无 → fresh；resume 失败 → recreated | `select_launch_kind` 读 `get-active` 决定 |
| 错误分类 | auth/rate_limit → failed 不续接；network → 保留 active 等恢复 | `complete --status failed --error-reason <reason>` |

### P2 — 多 Agent 协调层

**目标：** 在 supervisor + worker 场景下正确追踪父子 session 关系。

| 功能 | 描述 | 映射到 freely |
|---|---|---|
| 父子关系 | `parent_session_id` 字段建立继承链 | upsert 时传 `--parent-session-id` |
| 子 session 查询 | 给定 parent 找到所有 child | `list-children --parent-session-id <uuid>` |
| Worker fork | worker 从 parent fork | `upsert --role worker --parent-session-id <parent> --launch-kind fork` |

### 现有功能保持清单

以下功能不受影响，不改动：

- `session-state.env` 的 45 个运行时计数器字段
- `_persist_session_anchor_early` — 保留，同时写 session-store.py
- `SESSION_PARENT_ID` — 保留 shell 变量，同时写入 DB
- `is_valid_uuid` — 保留，`LAST_TOOL_SESSION_ID` 取值前加校验
- ACP bridge（acp-bridge.py）— 不动 transport 层
- codex / kiro-cli / iflow 适配器 — 不动

## sessions 表设计

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL UNIQUE,
    project TEXT NOT NULL,
    tool TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'manager',
    parent_session_id TEXT DEFAULT '',
    launch_kind TEXT NOT NULL DEFAULT 'fresh',
    tool_adapter TEXT NOT NULL DEFAULT 'direct',
    resume_mode TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    error_reason TEXT DEFAULT '',
    metadata_json TEXT DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT ''
);
```

## session-store.py CLI 命令

```
# P0 — 已实现
init             创建表
upsert           插入/更新 session 记录
get-active       查当前活跃 session（按 project + role）
get-parent       查父 session
show             查看 session 详情
complete         标记完成/失败
list             列出 sessions
list-children    查子 sessions
count-active     计数活跃 sessions
```

## 集成点

### 1. run-acp-prompt.py — stdout 输出格式

```python
# 当前（有问题）:
print(f"session id: {session_id} (resumed)", flush=True)

# 目标:
print(session_id, flush=True)                           # line 1: clean UUID
print(f"session id: {session_id} (resumed)", flush=True) # line 2: human log
```

### 2. monitor-ai-acp.sh — session 写入

```bash
# 当前: _write_acp_session_state 写 session-state.env
# 目标: 读 line 1 clean UUID → session-store.py upsert
local session_id_clean
session_id_clean=$(head -1 "$log_file")
python3 "$session_store_py" upsert \
    --db "$project/.freely/freely.db" \
    --session-id "$session_id_clean" \
    --project "$project" --tool "$tool" \
    --launch-kind "$launch_kind" --tool-adapter acp \
    --role "${FREELY_ROLE_HINT:-manager}"
```

### 3. freely select_launch_kind — 恢复决策

```bash
if [[ "${AI_TOOL_ADAPTER:-direct}" == "acp" ]]; then
    local sid
    sid=$(python3 "$session_store_py" get-active \
        --db "$PROJECT_ROOT/.freely/freely.db" \
        --project "$PROJECT_ROOT" \
        --role "${FREELY_ROLE_HINT:-manager}" 2>/dev/null || true)
    if [[ -n "$sid" ]] && is_valid_uuid "$sid"; then
        CLAUDE_SESSION_ID_CURRENT="$sid"
        LAUNCH_KIND_SELECTED="resume"
        LAUNCH_ROTATION_REASON="acp_session_persists"
        return 0
    fi
    LAUNCH_KIND_SELECTED="fresh"
    LAUNCH_ROTATION_REASON="acp_first_launch"
    return 0
fi
```

## 补充设计 — ACP Bridge 重启恢复

Bridge 死亡 → `claude-agent-acp` 子进程死亡 → session 从内存丢失。但 `run-acp-prompt.py` L334-352 已实现自愈 fallback：`session/resume` 失败 → catch → `session/new`（recreated 模式）。

**P0 策略（不改 bridge，靠 session-store + run-acp-prompt.py 自愈）：**

```
上次结束: session-store 有 status=active 的 session S1
    │
    ▼
freely start → get-active → 返回 S1（clean UUID）
    │
    ▼
run-acp-prompt.py: session/resume S1
    │
    ├─ 成功 → 继续用 S1（cache hit，零 token 浪费）
    │
    └─ 失败（bridge 重启 / session 丢失）
        → catch → session/new → 得 S2（recreated）
        → stdout line 1: S2（clean UUID）
        │
        ▼
monitor-ai-acp.sh: session-store.py upsert S2（覆盖 S1 的 active 状态）
    → S1 status=failed（bridge_session_lost）
    → S2 status=active（新 session）
```

下一次 `freely start` → `get-active` 返回 S2 → `session/resume S2` → 成功。不依赖 cycle log 文本解析，不依赖工具目录扫描。

**P1 可加 bridge 世代号**避免一次失败 RPC 往返：`get-active` 时对比世代号，不同则直接 fresh。

## 补充设计 — ACP 错误分类增强

当前 `_detect_acp_failure` 只有一个分类：auth_or_rate_limit。需要细化为三类，避免误判。

| 错误类别 | 检测模式 | session 处理 |
|---|---|---|
| `auth_or_rate_limit` | 401/403/429/quota exceeded/InsufficientBalance | complete --status failed，下次 fresh |
| `network_failure` | Connection refused/reset/timeout/DNS | 保留 active，下次 resume（网络可能恢复） |
| `bridge_session_lost` | "session not found" / "unknown session" | complete --status failed，下次 fresh |

关键改进：**network_failure 不标记 session 为 failed**，保留为 active 以便网络恢复后续接。

## 补充设计 — Session 状态机

```
                 session/new
                     │
                     ▼
                 ┌───────┐
          ┌─────│ active │─────┐
          │     └───┬───┘     │
          │         │         │
     resume成功   turn结束  resume失败
     (保持active)  │    (auth/bridge_lost)
          │     complete      │
          │    --status       ▼
          │    completed   ┌──────┐
          └────▶          │failed│
                          └──┬───┘
                             │
                       下次 start 时
                       get-active 跳过 failed
                       → 自动 fresh
```

**`get-active` 查询逻辑：**
```sql
SELECT session_id FROM sessions
WHERE project = ? AND role = ? AND status = 'active'
ORDER BY updated_at DESC LIMIT 1
```

`status != 'active'` 的 session 对 resume 不可见，自动退回 fresh。

## 补充设计 — 数据流全景

```
freely start
  │
  ├─[1]─ acp-bridge.py start ─── 启动 claude-agent-acp ──→ bridge 监听 socket
  │                                                         bridge_generation = N
  │
  ├─[2]─ select_launch_kind ─── session-store.py get-active
  │        │                      │
  │        │                      ├─ 返回 clean UUID → resume 路径
  │        │                      └─ 返回空 → fresh 路径
  │        │
  │        ▼
  ├─[3]─ monitor-ai-acp.sh 启动
  │        │
  │        └─ run-acp-prompt.py ─── 通过 bridge socket 发 ACP RPC
  │              │                   session/new 或 session/resume
  │              │                   ← 返回 clean session_id (UUID)
  │              │
  │              ├─ stdout line 1: <clean UUID>        ← 机器读
  │              ├─ stdout line 2: session id: ...     ← 人类日志
  │              └─ stdout: AI 的工具调用和输出
  │
  ├─[4]─ monitor-ai-acp.sh 读 line 1 clean UUID
  │        │
  │        └─ session-store.py upsert
  │             --session-id <clean UUID>
  │             --launch-kind resume --tool-adapter acp
  │             --role manager
  │
  ├─[5]─ AI cycle 结束
  │        │
  │        ├─ 正常结束 → session-store.py complete --status completed
  │        └─ 异常结束 → _detect_acp_failure 分类错误
  │                         ├─ auth/bridge_lost → complete --status failed
  │                         └─ network → 保持 active（等恢复）
  │
  └─[6]─ 下次 freely start → 回到 [2]
```

## 补充设计 — 完整集成点清单

不只是 3 个集成点，实际需要改 6 个地方：

| # | 文件 | 函数/位置 | 改动 |
|---|---|---|---|
| 1 | `run-acp-prompt.py` | ~L344 | stdout line 1 = clean UUID |
| 2 | `monitor-ai-acp.sh` | ~L217-226 | 读 line 1 clean UUID → upsert，替代 `_write_acp_session_state` |
| 3 | `monitor-ai-acp.sh` | ~L95-97 | `_detect_acp_failure` 增加 `bridge_session_lost` 分类 |
| 4 | `freely` | `select_launch_kind` ~L14402-14461 | ACP 模式：`get-active` → 有则 resume，无则 fresh |
| 5 | `freely` | `extract_tool_session_id_from_log` ~L4935-4949 | 删除 ACP 分支 |
| 6 | `freely` | `_find_recent_session_from_tool_dir` ~L3360-3376 | ACP 路径不再调用 |
| 7 | `freely` | `ensure_runtime_tool_session_anchor` ~L3378-3435 | ACP 模式优先从 session-store 取值 |
| 8 | `freely` | `_persist_session_anchor_early` ~L3284-3331 | 保留写 session-state.env，**增加**写 session-store.py（同一时机，双写） |
| 9 | `freely` | init ~L16474 | 已改：`freely.db` 初始化 session-store |

## 补充设计 — 与 session-state.env 的双写策略

**原则：** session-store.py（SQLite）是 session 身份的**权威源**。session-state.env 继续持有运行时计数器。

**双写时机：**

```
_persist_session_anchor_early  ← 写 session-state.env（保留）
                               ← 同时写 session-store.py upsert（新增）

write_session_state            ← 写 session-state.env 全部 45 字段（保留）
                               ← 不写 session-store.py（session 身份已在 anchor_early 写入）
```

**读取优先级：**
```
CLAUDE_SESSION_ID_CURRENT = session-store.py get-active（权威）
                          ↓ 如果为空（DB 不存在等极端情况）
                          session-state.env 的 CLAUDE_SESSION_ID_CURRENT（降级）
                          ↓ 如果也无效
                          走 fresh
```

这样 session-state.env 降级为备份，DB 是主源。

## 补充设计 — Worker fork 场景

当 supervisor 需要创建 worker 时：

```
[supervisor AI 决定创建 worker]
    │
    ├─ freely runtime 设置 SESSION_PARENT_ID=<supervisor_session_id>
    ├─ AI_TOOL_ADAPTER=acp（继承）
    ├─ FREELY_ROLE_HINT=worker
    │
    ├─ select_launch_kind
    │     └─ session-store.py get-active --role worker
    │         → 空（worker 没有自己的 active session）
    │         → SESSION_PARENT_ID 非空 → LAUNCH_KIND_SELECTED="fork"
    │
    ├─ run-acp-prompt.py
    │     └─ launch_kind=fork → session/new（创建新 session）
    │         → stdout line 1: new clean UUID
    │
    ├─ monitor-ai-acp.sh
    │     └─ session-store.py upsert
    │           --session-id <new UUID>
    │           --role worker
    │           --parent-session-id <supervisor_session_id>
    │           --launch-kind fork
    │
    └─ supervisor cleanup 时
          └─ session-store.py list-children --parent-session-id <supervisor>
              → 检查子 session 是否都 completed/failed
```

## 不吸收的功能（有意识排除）

- SSE/HTTP 推送 — freely 是 shell CLI，不需要浏览器端事件流
- serverless cold-start 恢复 — freely 是本地 daemon
- 多实例租约 — 目前单机单实例
- 多后端 DB hydrate — 单一 SQLite 足够
- 进程适配器工厂模式 — freely 通过 shell alias 解析已实现多工具切换

## P0 成功标准

实施完成后，以下每条必须为 true：

1. **Session ID 永远是 clean UUID**：`LAST_TOOL_SESSION_ID` 不包含 "(resumed)" 等注解，`is_valid_uuid` 校验通过
2. **ACP 模式不扫描文件系统**：`select_launch_kind` ACP 分支只调 `session-store.py get-active`，不读 cycle log 文本，不调 `_find_recent_session_from_tool_dir`
3. **AI cycle 结束后 session 入 DB**：`monitor-ai-acp.sh` 读 line 1 clean UUID → `session-store.py upsert`，替代 `_write_acp_session_state`
4. **不可恢复错误标记 failed**：auth/rate_limit 错误 → `complete --status failed`，下次 `get-active` 不可见
5. **网络错误保留 active**：network_failure 不标记 failed，保留续接可能
6. **非 ACP 工具无回归**：codex/kiro-cli/iflow 的 session 管理行为不变
7. **`session-state.env` 运行时计数器不变**：rate limit tracking、restart storm、resume streak 等字段继续工作

## 实施清单

| # | 文件 | 改动 | 状态 |
|---|---|---|---|
| 1 | `run-acp-prompt.py` | stdout line 1 = clean UUID | ⬜ |
| 2 | `monitor-ai-acp.sh` L217-226 | 读 line 1 UUID → session-store.py upsert | ⬜ |
| 3 | `monitor-ai-acp.sh` L87-98 | `_detect_acp_failure` 增加 bridge_session_lost 分类 | ⬜ |
| 4 | `freely` L14402-14461 | ACP 模式 `select_launch_kind` 调用 session-store | ⬜ |
| 5 | `freely` L4935-4949 | 删除 `extract_tool_session_id_from_log` ACP 分支 | ⬜ |
| 6 | `freely` L3360-3376 | `_find_recent_session_from_tool_dir` ACP 路径不再调用 | ⬜ |
| 7 | `freely` L3378-3435 | `ensure_runtime_tool_session_anchor` ACP 模式优先 DB | ⬜ |
| 8 | `freely` L3284-3331 | `_persist_session_anchor_early` 同时写 session-store | ⬜ |
| 9 | `freely` L16474 | init 时调 session-store.py init（已做 ✅） | ✅ |

## 参考资料

- `20260401-1545--acp-client-agent-protocol-runtime-adoption`
- `20260419-2245--runtime-claude-launch-and-session-evidence`
- `20260316-1800--session-lifecycle-rotation-and-handoff`
- `chat-inbox.py` — CLI + SQLite 模式参考
