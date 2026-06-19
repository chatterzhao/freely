---
local_id: raw-20260619T033758Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T033758Z-A
platform_ids:
  github:
    issue_id: '3015'
    url: https://github.com/chatterzhao/freely/issues/3015
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T03:38:14Z'
updated_at: '2026-06-19T03:41:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 触发命令

```bash
freely ai login claude
freely ai login opencode
freely ai login cc
freely ai login cc-use-codex-cli
freely ai login kiro-cli
```

（统称"非 codex 工具"，不带 `apikey` 模式参数）

## 问题

执行 `freely ai login claude` 后，完整调用链最终落在 `tool_login_generic`（ai-cli L1260-1261），这个函数：
- ❌ 没有任何交互提示（不询问 auth_mode、不询问 slot name）
- ❌ 硬编码自动生成 `claude-default-1` 作为 slot 名
- ❌ 只创建空目录 `~/.ai-auth/claude-default-1/`，不写配置模板（settings.json）
- ❌ 不加 shell alias 到 `~/.zshrc`

对比 `login codex` 的完整流程（L1200-1254：55行登录+保存+alias 逻辑），claude 分支只有一行 `tool_login_generic "$tool"`。

## 根因

`tool_login_generic` 设计意图是"轻量容器创建"（适合 iflow 这种 auth 来自环境变量、slot 仅调度器兼容的场景），但被错误地复用到 claude/opencode 等需要完整配置+alias 的工具。

## 设计方案

参照 `login codex` 的交互模式：

```
freely ai login claude
  → 1. 提示: "Claude auth mode (account/apikey) [account]"
       ├─ apikey → 提示输入 slot name（空=退出）
       │            → 创建 ~/.ai-auth/claude-apikey-{name}/settings.json
       │            → alias claude-apikey-{name}="claude --settings ..."
       └─ account → 提示输入 slot name（空=退出）
                     → 创建 ~/.ai-auth/claude-account-{name}/
                     → alias claude-account-{name}="claude"
```

### 需要改的函数（均在 `docs/system/workspace/scripts/runtime/ai-cli`）

1. **`cmd_login` L1260-1261** — 替换 `tool_login_generic`，增加 auth_mode 交互提示 + account/apikey 分支
2. **`_login_apikey_alias` L1276** — `LOGIN_PROVIDER_NAME` 为空时改为交互提示，不再默默回退 `"default"`
3. **新增 `_prompt_claude_login_mode`** — 类似 `codex_prompt_login_mode` (L66-78)，为 claude/opencode 等非 codex 工具提供 account/apikey 选择
4. **新增 `_login_account_slot`** — account 模式的 slot 创建（交互式 slot name + alias）

### 不影响

- `iflow` — 保持现状（auth 来自环境变量，slot 仅调度器兼容）
- `codex` — 保持现有 account/apikey 流程

### 附注：`codex_prompt_login_mode` 的潜在 bug

`cmd_login` 中 L1201-1207：`codex_prompt_login_mode` 允许用户选 apikey，但走到 L1204 会因为 `$auth_mode != "account"` 而报错退出（因为统一 apikey 路径 L1191-1196 在 prompt 之前就检查过了）。建议 prompt 只提供 `account` 选项，让用户想要 apikey 时显式传参。
