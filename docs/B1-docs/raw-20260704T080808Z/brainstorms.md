---
b1_id: B1-20260704T080808Z
phase_state: completed
source_raw: raw-20260704T080808Z08Z
source_url: https://github.com/chatterzhao/freely/issues/3727
produced_candidate: C-20260704T080808Z-A
created_at: 2026-07-04
---

# B1_IBM: 多 ACP bridge 并行 — per-agent tool/slot 支持

## Input
- raw-20260704T080808Z08Z (GitHub #3727)
- 前置依赖: raw-20260704T064539Z39Z (session 统一, 已合并到 develop)

## Problem

当前 1 个 bridge per project，所有 agent 共享 manager 的 tool。agent-table 中 worker/reviewer 即使配置了不同 slot 也无效。

需要支持:
1. 同 base_tool 不同 slot: manager=opencode-apikey-ds-flash, worker=opencode-apikey-openai-gpt
2. 不同 base_tool: manager=opencode, worker=claude

## 前置条件 (已由 #3726 完成)

- `_ensure_acp_bridge_running(project, base_tool)` ✅ 签名已预留
- `_acp_bridge_socket(project, base_tool)` ✅ 签名已预留 (base_tool 被忽略)
- `_resolve_bridge_socket(project, base_tool)` ✅ agent_working.py 已实现 (base_tool 被忽略)
- `acp_session_connect()` ✅ 所有 session 操作经统一入口
- 调用方已传入 base_tool ✅ bridge 路由参数已到位

## Brainstorm

### 设计: 为每个 agent 的 base_tool 启动独立 bridge

```
daemon start:
  agent-table.toml:
    manager_slot  = opencode-apikey-ds-flash-auto    → base_tool = opencode
    worker_slot   = opencode-apikey-openai-gpt-auto  → base_tool = opencode
    reviewer_slot = claude-apikey-ds-flash-auto      → base_tool = claude

  唯一 base_tools: {opencode, claude}
  → _ensure_acp_bridge_running(project, "opencode")
    socket: /tmp/freely-acp-{hash}-opencode.sock
  → _ensure_acp_bridge_running(project, "claude")
    socket: /tmp/freely-acp-{hash}-claude.sock

session 操作:
  acp_session_connect(slot="opencode-apikey-ds-flash-auto")
    → base_tool = "opencode"
    → socket = /tmp/freely-acp-{hash}-opencode.sock
    → session/new, fork, resume, prompt 都走这个 bridge

  acp_session_connect(slot="claude-apikey-ds-flash-auto")
    → base_tool = "claude"
    → socket = /tmp/freely-acp-{hash}-claude.sock
```

### 关键改动

**1. socket/pid 命名改为 per-tool**
```bash
# Before: /tmp/freely-acp-{hash}.sock
# After:  /tmp/freely-acp-{hash}-{base_tool}.sock

_acp_bridge_pid_file() { echo "/tmp/freely-acp-$(_acp_bridge_short_hash "$1")-${2:-}.pid"; }
_acp_bridge_socket()   { echo "/tmp/freely-acp-$(_acp_bridge_short_hash "$1")-${2:-}.sock"; }
```

**2. daemon start: 扫描 agent-table 启动所有 bridge**
```bash
# 获取所有唯一的 base_tool
local _tools=()
while IFS= read -r slot; do
    local bt="${slot%%-*}"
    [[ " ${_tools[*]} " != *" $bt "* ]] && _tools+=("$bt")
done < <("$BIN/agent-table-query" --list-slots 2>/dev/null)

for bt in "${_tools[@]}"; do
    if ! _tool_is_registered "$bt"; then
        log_error "agent-table slot base_tool '$bt' not in tool-registry. Aborting."
        exit 1
    fi
    _ensure_acp_bridge_running "$project" "$bt" || exit 1
done
```

**3. base_tool 不可解析 → 硬报错**
```bash
# slot 截取的 base_tool 必须在 tool-registry 有注册
# 必须在 config.toml 能找到 FREELY_ACP_{TOOL}_BIN
# 任一不满足 → 立即报错退出，不 fallback
```

**4. daemon stop: 停止所有 bridge**
```bash
for bt in "${_tools[@]}"; do
    _stop_acp_bridge "$project" "$bt"
done
```

**5. _resolve_bridge_socket 启用 base_tool**
```python
def _resolve_bridge_socket(project, base_tool=""):
    h = hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]
    return f"/tmp/freely-acp-{h}-{base_tool}.sock"
```

### fork 跨 slot 策略

| 场景 | base_tool | bridge | fork? |
|------|:---:|------|:---:|
| Mgr(opencode-ds)→Worker(opencode-ds) | 同 | 同 | ✅ |
| Mgr(opencode-ds)→Worker(opencode-gpt) | 同 | 同 | ✅ (同 bridge, 不同 settings.json) |
| Mgr(opencode)→Worker(claude) | 不同 | 不同 | ❌ → session/new |

**同 bridge 不同 slot 的 fork**: 本期尝试 fork——如果 opencode bridge 能处理不同 session 用不同 settings，fork 成功 (缓存命中)。如果失败，自然回退 new + log。

## Decision

核心改动:
1. socket/pid 命名 per-tool: `-{base_tool}` 后缀
2. daemon start 扫描 agent-table 所有唯一 base_tool → 各启一个 bridge
3. base_tool 不可解析 → 硬报错退出
4. daemon stop 清理所有 bridge
5. `_resolve_bridge_socket` 启用 base_tool
6. cleanup 模式更新 (多 bridge pid/socket 文件清理)

## Candidate
- candidate_id: C-20260704T080808Z-A
- status: promoted
- milestone: M-20260704T080808Z-A

## 切号与多 bridge 交互

### 当前切号逻辑

```
failure → tool_select_ready_slot → _stop_acp_bridge → load_config → next cycle
          扫描可用 slot, 测试        杀当前 bridge      更新 AGENT_AI_TOOL   重启 bridge
```

问题: `_stop_acp_bridge "$project"` 会杀死所有 bridge（如果已实现多 bridge）。Manager 切号不应影响 Worker 的 bridge。

### 多 bridge 下的切号行为

```
Manager 切号 (opencode → claude):
  1. _stop_acp_bridge "$project" "opencode"  ← 只停 Manager 的旧 bridge
  2. load_config → AGENT_AI_TOOL=claude-apikey-xxx
  3. next cycle → _ensure_acp_bridge_running "$project" "claude" ← 启动新 bridge
  4. Worker 的 opencode bridge 不受影响 ✅

所有 tool 不可用 → fallback:
  1. 每个 bridge 尝试恢复 → 都不可用 → 报错等待
  2. _stop_acp_bridge 改为接受 base_tool 参数 (默认全停)
```

### base_tool 解析验证点

必须在以下时机验证 base_tool 可解析:

| 时机 | 验证 | 失败处理 |
|------|------|:---:|
| daemon start | 扫描 agent-table 所有 slot → 每个 base_tool 必须在 registry + config | 硬报错退出 |
| 切号 | 新 slot 的 base_tool 必须在 registry + config | 硬报错, 不切 |
| acp_session_connect | slot → base_tool → bridge_socket 解析 | 报错 + 不创建 session |

### _stop_acp_bridge 参数化

```bash
# Before: _stop_acp_bridge "$project"  (杀所有 bridge)
# After:
_stop_acp_bridge() {
  local project="$1" base_tool="${2:-}"  # 空 = 全停, 有值 = 只停指定 tool
  if [[ -n "$base_tool" ]]; then
    _stop_one_bridge "$project" "$base_tool"
  else
    for bt in "${_all_running_tools[@]}"; do
      _stop_one_bridge "$project" "$bt"
    done
  fi
}
```
