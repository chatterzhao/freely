# Brainstorm: default-autonomy-activation-consent-and-tool-policy-governance

## Focus

把 Freely 默认高自治 posture、activation consent、runtime decision ladder、以及 tool policy materialization 上方的 posture truth 收口成一条可继续实现的产品 owner issue。

## Key Reproduced Facts

1. `tools.md` 和 runtime launcher 已把 `codex` / `cc` 的 `auto` 路径定义成免交互、自动批准。
2. `freely init` 当前生成的项目级 `.codex/config.toml` 仍写 guarded defaults。
3. 产品讨论已明确：Freely 默认不应把交互批准当主路。
4. safeguard 应是强建议与支持面，而不是默认强制前置门槛。
5. 运行中高风险处理的主路应是内部 AI 决策升级，而不是恢复用户逐步批准。

## Intended Contract

1. Freely default posture
   - unattended
   - automatic approval
   - owner-grade autonomy

2. Activation consent
   - blocking
   - explicit
   - repeatable confirmation allowed
   - records accepted boundary

3. Safeguard guidance
   - sandbox / VM / dedicated device / restricted network are strongly recommended
   - Freely should help users adopt them
   - missing safeguards do not automatically block activation

4. Tool policy layering
   - Freely canonical policy owns the product truth
   - adapter layer translates it to tool-specific args / env / prompts / project config
   - tool-local config should remain project-scoped when possible and avoid mutating user-global state by default

5. Runtime autonomy preservation
   - high-risk or high-uncertainty situations first escalate through internal AI review
   - security-focused subagent / reviewer committee can participate without restoring human step approvals
   - minimal risk state is the last resort when no credible next move remains

## Split Rationale

这条 owner 只承接产品 posture 与 mapping contract，不承接：

- supply-chain baseline implementation
- secret/artifact scanning implementation
- reusable security skill decomposition
- full decision-support capability materialization
