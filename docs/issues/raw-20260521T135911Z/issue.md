---
local_id: raw-20260521T135911Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2065'
    url: https://github.com/chatterzhao/freely/issues/2065
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-21T13:59:22Z'
updated_at: '2026-05-21T15:27:20Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-05-21T15:27:20Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## 问题

权限参数散布在三个地方，互相冲突：

1. **alias**: `--dangerously-skip-permissions`（已废弃，官方推荐 `permissions.defaultMode`）
2. **bridge**: 硬编码 `--permission-mode bypassPermissions` + `session/set_mode bypassPermissions`
3. **JSON**: Claude 有 `permissions.deny` 但缺 `defaultMode`；OpenCode 有 `permission: allow`

桥的 `bypassPermissions` 对 Claude 冗余、对 OpenCode 报 Internal error。

## 统一方案

权限全部放入各家 JSON 配置文件，alias 只传工具+配置路径，bridge 完全不管权限。

### Claude Code
```json
// settings.json
{
  "permissions": {
    "defaultMode": "bypassPermissions",
    "deny": ["Bash(git push --force ...)"]
  }
}
```
alias: `claude --settings path.json`

### OpenCode
```json
// config.json
{
  "permission": "allow"
}
```
alias: `OPENCODE_CONFIG=path.json opencode` (不变)

### Codex CLI
用 `--dangerously-bypass-approvals-and-sandbox`（CLI flag），或无头模式下默认行为。

## 需要重构的位置

### 1. ~/.zshrc alias (3处)
```
cc-acp-ai98pro-0045-auto: 去掉 --dangerously-skip-permissions
cc-acp-ds-flash-auto:      去掉 --dangerously-skip-permissions
cc-direct-ds-auto:         去掉 --dangerously-skip-permissions
```
命名规范: `{tool}-{adapter}-{model}-{mode}` 如 `cc-acp-ai98pro-0045-auto`

### 2. Claude settings JSON (2个文件)
```
~/.claude/settings_ai98pro_0045.json:  permissions 加 "defaultMode": "bypassPermissions"
~/.claude/settings_deepseek_flash.json: 同上
~/.claude/settings_deepseek.json:      同上
```

### 3. acp-bridge.py (8处)
```
88:   --permission-mode bypassPermissions  → 删除
140:  --permission-mode bypassPermissions  → 删除
198:  --permission-mode bypassPermissions  → 删除
364:  session/set_mode bypassPermissions   → 删除
377:  session/set_mode bypassPermissions   → 删除
484-494: session/set_mode bypassPermissions → 删除3处
```
方法 `_ensure_bypass_permissions` 整体删除。

### 4. tool-launchers.sh (2处)
```
398:  d.get("permissionMode") → 增加 d.get("permissions",{}).get("defaultMode") 读嵌套
658:  --permission-mode bypassPermissions (cc/claude direct模式) → 删除
707:  --dangerously-skip-permissions (opencode direct模式) → 删除
```

### 5. freely (1处)
```
12527: d.get("permissionMode") → 同上，增加读 permissions.defaultMode
```

### 6. _apply_tool_alias_settings (1处)
```
增加: 读取 permissions.defaultMode 并 export CLAUDE_CODE_PERMISSION_MODE
```

## 关于分支名的附注

Worker prompt 的 `Branch:` 字段中，AI 有时生成 `Branch: xxx (to create)`，`(to create)` 被 runtime 当作分支名字面值，导致 git 拒绝。

修复:
1. manager-agent.md: 说明 Branch 字段只写分支名，不加注释
2. worker_prompt_target_branch(): 提取后 sanitize，去掉 (xxx) 尾注
