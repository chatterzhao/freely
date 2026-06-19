# Implementation Decision Note

- owner_issue: `docs/issues/I-20260619T033758Z-A/issue.md`
- source_candidate: `docs/pre-brainstorms/20260619T033758Z--login-claude-interactive-slot/candidates.md`

## decision

修改 `docs/system/workspace/scripts/runtime/ai-cli`：新增 `_prompt_generic_login_mode` 和 `_login_account_slot` 两个函数，修改 `cmd_login` 的 claude/opencode/cc/kiro-cli 分支和 `_login_apikey_alias` 的 slot 命名逻辑，替换 settings.json 骨架。

## why_this

1. **最小改动原则**：修改局限在 1 个文件，+152/-4 行
2. **参照既有模式**：`_prompt_generic_login_mode` 与 `codex_prompt_login_mode` 同构，`_login_account_slot` 与 `_login_apikey_alias` 同构
3. **职责分离**：account 和 apikey 两路径行为不同（前者无 settings override，后者有完整模板），分组为独立函数
4. **向后兼容**：`--name` + `--yes` 标志行为不变

## alternatives_considered

| 方案 | 拒绝原因 |
|------|---------|
| 修改 `tool_login_generic` 增加交互 | 影响 iflow 的轻量容器语义，职责串味 |
| 创建统一 `_login_interactive_slot` | account/apikey 配置差异大，统一接口反而增加复杂度 |
| 仅修改 apikey 路径，不管 account | 用户需要两种模式都可用 |

## boundary_non_goals

- 不修改 codex 登录流程（保持现有行为）
- 不修改 iflow 登录流程（保持 `tool_login_generic`）
- 不修改 switch/save/list/whoami/status/delete 命令
- 不涉及 ACP bridge、tool-registry 或 scheduler

## residual_risk

- **低风险**：修改完全自包含，不依赖外部服务或配置
- settings.json 骨架可能与未来 Claude Code 版本不兼容（需随官方更新同步维护）
- `--yes` 模式强制要求 `--name`，可能影响极少数脚本（之前 `--yes` 无 `--name` 会静默创建 `default`，现在报错）。这是一个有意的改进——静默创建无意义的默认 slot 是更差的行为。
