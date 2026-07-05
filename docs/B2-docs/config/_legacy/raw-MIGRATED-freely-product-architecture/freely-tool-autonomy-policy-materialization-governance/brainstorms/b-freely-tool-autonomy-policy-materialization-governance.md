# Brainstorm: freely-tool-autonomy-policy-materialization-governance

## Context

`I-20260401-1303-A` 已经冻结了 Freely 默认高自治 posture、activation consent、以及“阻塞知情同意而不是阻塞 safeguard completeness”的产品真相。

当前剩下的产品架构缺口不是“Freely 到底要不要默认高自治”，而是“这个默认姿势如何被具体工具消费”。

## Reproduced Fact

当前至少存在一组明确 split：

1. `docs/system/workspace/tools.md` 把 `codex` / `cc` 的 `auto` 路径定义为免交互、自动批准。
2. runtime launcher 在 `mode=auto` 下也实际注入：
   - Codex: `--dangerously-bypass-approvals-and-sandbox`
   - Claude Code: `--permission-mode bypassPermissions`
3. 本条 issue 最初 materialize 时，`freely init` 生成的项目级 `.codex/config.toml` 仍保持 guarded posture：
   - `approval_policy = "on-request"`
   - `sandbox_mode = "workspace-write"`
   - `network_access = false`
4. 当前第一条实现切片已落地：
   - `auto` 模式的项目级 `.codex/config.toml` 现在写 `approval_policy = "never"`
   - `sandbox_mode = "workspace-write"` 与 `network_access = false` 仍保持 project-local recommended baseline
   - `cc` / `cc-use-codex-cli` 目前仍主要依赖 launch-time materialization，而不是 project-local config file

## Questions To Freeze

1. 哪些 posture truth 应由 Freely canonical policy 保存？
2. 哪些应直接写入项目级工具配置？
3. 哪些应仅在 launch-time 动态注入？
4. 哪些只能给 manual hint，不能自动写用户 home config？
5. ACP 将来若接入，应该消费哪一层 truth，而不是重新发明 owner？

## Working Direction

- Freely canonical policy 是上位真源。
- tool adapter injection 负责把 canonical policy 翻译成具体工具可消费的 flags / env / prompt contract。
- tool-local config materialization 只负责能项目级落盘的那一层，不应与 launch-time injection 混在一起。
- user-global config 默认只给 manual-only guidance。
- ACP 若接入，应消费 canonical policy / adapter contract，而不是成为本条前置 blocker。
