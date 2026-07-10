---
kind: raw
priority: P2
phase_state: absorbed
source: feedback
created_at: '2026-05-18T03:28:31Z'
title: freely ai config 命令：统一管理各 AI Tool 配置 + 向下生成 + alias 生成
platform_ids:
  github:
    issue_id: '551'
    url: https://github.com/chatterzhao/freely/issues/551
    synced_at: '2026-05-18T03:28:37Z'
updated_at: '2026-06-17T00:23:42Z'
primary_platform: github
platform_state: closed
local_id: raw-20260518T032831Z
---

## 现状

- `freely set-tool` 只改 config.env 的 AI_TOOL 值
- 各工具配置散落在不同位置（opencode config.toml, claude settings.json, shell alias）
- `_apply_tool_alias_settings` 从 alias 的 --settings 参数读 JSON，临时导出 env vars
- `bypassPermissions` 通过 session/set_mode RPC 透传时 OpenCode 不支持，报错

## 设计

### 新增命令

```
freely ai config new     --tool <name> --file toml|json  [--interactive]
freely ai config update  --tool <name> --key <jsonpath> --value <val>
freely ai config remove  --tool <name> --key <jsonpath>
freely ai config show    --tool <name>  [--json]
freely ai config alias   --tool <name>  [--dry-run]
```

- 默认非交互式（给 AI 用），`--interactive` 给人用
- UI 保存时直接拼 CLI 参数调用，一份实现

### 存储：自管理 + 向下生成

```
~/.freely/tools/
├── oc-acp-ds-flash-auto/
│   ├── settings.json          # freely 自己的规范格式（唯一真相源）
│   └── generated/             # 向下生成（可重建）
│       ├── config.toml        # → opencode 格式
│       ├── settings.json      # → claude code 格式
│       └── alias.sh           # → shell alias snippet
```

### 向下生成流程

```
freely ai config alias --tool oc-acp-ds-flash-auto
  → 1. 读 settings.json
  → 2. 生成 generated/config.toml (TOML)
  → 3. 生成 generated/settings.json (Claude Code)
  → 4. 写入 alias 到 .zshrc
  → 5. source
```

### 权限透传修复

目前: acp-bridge --permission-mode ✅ + session/set_mode ❌(opencode 不支持)
改成: acp-bridge --permission-mode ✅ + alias → settings.json → _apply_tool_alias_settings 读 permissionMode → export 到 agent 环境变量。去掉了对 session/set_mode RPC 的依赖。

## 涉及文件

- `docs/system/workspace/scripts/runtime/freely` — 新增 `cmd_ai_config` + 5 个子命令
- `docs/system/workspace/scripts/runtime/tool-launchers.sh` — `_apply_tool_alias_settings` 适配新路径
- 现有 `freely set-tool` 可复用内部逻辑

## 参考

- `freely daemon start|stop|status` 子命令模式
- `freely task-mode set` 参数模式
- `_apply_tool_alias_settings` 当前 alias → settings 读取逻辑
