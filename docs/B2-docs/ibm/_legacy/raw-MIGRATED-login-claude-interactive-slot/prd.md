# PRD: login claude 交互式 slot 命名与 alias 创建

## Goal

修复 `freely ai login claude`（及 opencode/cc/cc-use-codex-cli/kiro-cli）命令：让用户在登录时能交互式选择 auth_mode 并自定义 slot 名称，自动创建带 Anthropic 官方 settings.json 骨架的 slot 目录和 shell alias。

## Why Now

- 当前 `login claude` 只创建空目录 `claude-default-1`，完全不可用
- 用户期望与 `login codex` 一致的交互体验
- 影响多个工具（claude, opencode, cc, kiro-cli），覆盖面广

## Product Surface

| 面 | 说明 |
|----|------|
| CLI 交互 | `freely ai login <tool>` 新增两步 prompt（auth_mode → slot name） |
| 文件系统 | `~/.ai-auth/{tool}-{mode}-{name}/settings.json` 含 Anthropic 完整骨架 |
| Shell | `~/.zshrc` alias 自动添加 |
| 脚本兼容 | `--name` + `--yes` 支持非交互模式 |

## Non-Goals

- 不修改 codex 登录流程
- 不修改 iflow 登录流程
- 不修改 switch/save/list/whoami/status/delete 命令
- 不涉及 ACP bridge 或 tool-registry 变更

## Non-Negotiables

- 空输入必须终止（不能默默回退默认值）
- settings.json 骨架必须是 Anthropic 最新完整格式
- 向后兼容：`--name` 标志行为不变

## Context Pack

- 源文件：`docs/system/workspace/scripts/runtime/ai-cli`（~2400 行）
- 参照实现：`codex_prompt_login_mode`（L66-78）、`_login_apikey_alias`（L1299-1410）
- 已实现：commit `dfdb41ad5`（+152/-4）
- 测试：6 场景全部通过

## Decomposition Tree

```
login claude 交互式 slot
├── 1. _prompt_generic_login_mode（auth_mode 选择）
├── 2. _login_account_slot（account 模式 slot 创建）
├── 3. cmd_login 路由修改（apikey/account 分支）
├── 4. _login_apikey_alias 交互提示（空 LOGIN_PROVIDER_NAME）
└── 5. settings.json 完整骨架替换
```

## Prototype Path

1. 修改 ai-cli → 2. 语法检查 → 3. 6 场景测试 → 4. cp 到 fix 工位 → 5. commit

## Eval Plan

| 场景 | 预期 | 状态 |
|------|------|------|
| `login claude` → account + slot name | 创建 claude-account-{name}/ + alias | ✅ pass |
| `login claude` → apikey + slot name | 创建 claude-apikey-{name}/settings.json + alias | ✅ pass |
| `login claude apikey --name foo` | 非交互创建 | ✅ pass |
| `login claude account --name foo` | 非交互创建 | ✅ pass |
| `login claude apikey` + 空输入 | exit 2 | ✅ pass |
| `login claude apikey --yes` 无 --name | 报错 exit 2 | ✅ pass |
