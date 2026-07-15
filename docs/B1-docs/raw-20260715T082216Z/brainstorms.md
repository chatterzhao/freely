---
b1_id: B1-20260715T082216Z
phase_state: completed
source_raw: raw-20260715T082216Z
created_at: 2026-07-15
---

# B1: _bridge_ensure_running 缺少 registry-driven slot 凭证注入

## Input
- raw-20260715T082216Z: monitor-ai-acp.sh 启动 ACP bridge 时不传凭证 env vars

## Problem

### 启动时序

```
freely daemon start
  → start_project_runtime → main loop
    → _ensure_acp_bridge_running (L22552)
      → ai_cli_tool_with_auth_assemble work → 读 ~/.ai-auth/<slot>/<config>
      → env KEY=VALUE python3 acp-bridge.py ← 凭证正确传入 ✅

    → L040 AI launch → monitor-ai-acp.sh
      → _bridge_ensure_running (L372)
        → bridge 已在运行 → 直接返回 (L86-87) ✅
```

这个路径是正确的——当 daemon 首次启动时，`_ensure_acp_bridge_running` 先于 `monitor-ai-acp.sh` 运行，bridge 被正确启动。

### 但是：bridge 首次启动可能在 monitor-ai-acp.sh 的 context 中

**关键问题**：`_ensure_acp_bridge_running` 和 `monitor-ai-acp.sh` 中的 `_bridge_ensure_running` 谁先运行，取决于启动时序。

`_ensure_acp_bridge_running` 在主循环的 L040 之前调用。但 `monitor-ai-acp.sh` 是在 `start_project_runtime` 的主循环中被 `launch_manager_supervisor` → `daemon-run` → 新的 supervisor → main loop → L040 调用的。

如果在旧 supervisor 退出、新 supervisor 启动之间的窗口期，`monitor-ai-acp.sh` 的 `_bridge_ensure_running` 先触发了 bridge 启动（无凭证），然后 `_ensure_acp_bridge_running` 看到 bridge 已运行就跳过了。

### 本质问题

`_bridge_ensure_running` (monitor-ai-acp.sh L147) 启动 bridge 时**没有注入 slot 凭证**：
```bash
python3 "$bridge_script" start ... --foreground >/dev/null 2>&1
```

而 `_ensure_acp_bridge_running` (freely L14338) 有：
```bash
env "${_bridge_env[@]}" python3 "$bridge_script" start ... &
```

### 通用性要求

本修复必须对**所有注册的 AI CLI tool** 生效，不限于 Claude：

| Tool | 配置格式 | config_file (registry) | is_dir | 凭证位置 |
|------|---------|----------------------|--------|---------|
| Claude | JSON | settings.json | false | `~/.ai-auth/<slot>/settings.json` → `env` section |
| Codex | TOML | (空，is_dir=true) | true | `~/.ai-auth/<slot>/config.toml` + `auth.json` |
| OpenCode | JSON | settings.json | false | `~/.ai-auth/<slot>/settings.json` → `env` section |
| Cline | JSON | data/settings/providers.json | true | `~/.ai-auth/<slot>/data/settings/providers.json` |

## Decision

### 方案：在 tool-launchers.sh 新增 `_load_slot_env_vars`

在 `tool-launchers.sh` 新增函数 `_load_slot_env_vars`，直接通过 registry 读取 slot 凭证，不依赖 alias：

```bash
_load_slot_env_vars() {
  local tool="$1"
  local base_tool="${tool%%-*}"
  
  # 从 registry 读取 config_file 和 is_dir
  local cfg_file; cfg_file="$(_tool_registry_get "$base_tool" "slot.config_file" 2>/dev/null || echo "settings.json")"
  local is_dir; is_dir="$(_tool_registry_get "$base_tool" "slot.is_dir" 2>/dev/null || echo "false")"
  local fmt; fmt="$(_tool_registry_get "$base_tool" "config_schema.file_format" 2>/dev/null || echo "json")"
  
  # 解析 slot 目录
  local slot_dir="$HOME/.ai-auth/$tool"
  [[ -d "$slot_dir" ]] || return 1
  
  local config_path
  if [[ "$is_dir" == "true" && -n "$cfg_file" ]]; then
    config_path="$slot_dir/$cfg_file"
  else
    config_path="$slot_dir/${cfg_file:-settings.json}"
  fi
  [[ -f "$config_path" ]] || return 1
  
  # 读取凭证 env vars + permission mode
  python3 -c "
import json, os
# JSON format (claude, opencode, cline)
if '${fmt}' == 'json':
    with open('${config_path}') as f:
        d = json.load(f)
    for k, v in d.get('env', {}).items():
        print(f'{k}={v}')
    pm = d.get('permissionMode') or (d.get('permissions', {}) or {}).get('defaultMode', '')
    if pm: print(f'CLAUDE_CODE_PERMISSION_MODE={pm}')
# TOML format (codex)
elif '${fmt}' == 'toml':
    import tomllib
    with open('${config_path}', 'rb') as f:
        d = tomllib.load(f)
    # codex 的 config.toml 可能没有 env section，凭证在 auth.json 中
    # 暂时输出空，让 codex 使用 CODEX_HOME env var (bridge_config_env)
    pass
" 2>/dev/null
  
  return 0
}
```

然后在 `_bridge_ensure_running` (monitor-ai-acp.sh) 中调用：
```bash
while IFS='=' read -r key value; do
  [[ -n "$key" ]] && _bridge_env_vars+=("$key=$value")
done < <(_load_slot_env_vars "$tool" 2>/dev/null)

# 用 env vars 启动 bridge
env "${_bridge_env_vars[@]}" python3 "$bridge_script" start ...
```

### 为什么选这个方案
- tool-launchers.sh 已有 `_tool_registry_get`，无需额外依赖
- `monitor-ai-acp.sh` 已 source tool-launchers.sh
- 新函数对 Claude/OpenCode/Cline 的 JSON 格式通用
- Codex 的 TOML 格式暂不需要额外凭证注入（通过 `CODEX_HOME` env var 处理）
- 不破坏 `_apply_tool_alias_settings` 的 alias 路径（保留作为可选的补充）

## Candidate
- candidate_id: C-20260715T082216Z-A
- status: promoted
- milestone: M-20260715T082216Z-A
