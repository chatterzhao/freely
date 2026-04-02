# PRD: default-autonomy-activation-consent-and-tool-policy-governance

## Goal

冻结 Freely 作为高自治宿主的默认产品姿势，并把 activation consent、runtime decision ladder、以及产品级 posture truth 写成统一、可实现、可观察的 contract。

## Why Now

Freely 当前已经在 `tools.md` 与 launcher 中表现出明显的自动批准姿势，但项目级 Codex config、产品级知情同意 contract、以及“高风险时自治如何继续推进”的 runtime contract 仍未统一。若不先把这层 product truth 冻结下来，后续 security baseline、ACP adapter、tool-specific wiring 都会继续漂。

## Product Surface

- `freely init`
- `freely doctor`
- runtime decision / escalation path
- `freely baseline-status`
- `freely live-status`
- project-level posture / consent artifacts

## Non-Goals

- 不一次解决所有 security baseline domains
- 不把运行时主路改回人工逐步批准
- 不把 sandbox/VM/隔离设备变成默认 hard prerequisite
- 不直接实现 reusable security skills

## Non-Negotiables

- Freely 默认姿势是高自治、免交互、自动批准
- activation consent 必须阻塞，但阻塞的是知情同意，不是 safeguard completeness
- safeguard 必须被清楚提示、建议、尽量支持
- Freely canonical policy 必须是上位真源
- autonomous escalation ladder、reviewer committee、minimal risk state 必须被定义成产品 contract
- 具体 tool adapter 和 tool-local config materialization 由 sibling owner 承接，不在本条里混成一个实现大伞

## Context Pack

- `tools.md` / launcher 已定义 auto posture
- `.codex/config.toml` project bootstrap 仍偏 guarded posture
- 既有 `interactive-init-bootstrap-and-force-governance` 已经证明 project-local config 优先、避免污染用户 home 是正确方向
- ACP 仍是可选 adapter boundary，不是这条 product truth 的 owner

## Decomposition Tree

1. Freeze default autonomy posture
2. Define activation consent contract
3. Define safeguard guidance semantics
4. Define runtime decision ladder and minimal-risk semantics
5. Define canonical-policy ownership boundary above tool materialization
6. Define observable posture fields for init/doctor/runtime/status

## Prototype Path

最小原型不是直接改 runtime 行为，而是先把 issue、PRD、pre-tests、tasks 和 issue-bound brainstorm 写清，使后续实现不再反复争论 Freely 默认是否应高自治、是否该把 safeguard 变成默认阻塞，以及哪些实现细节应交给 sibling materialization owner。

## Eval Plan

成功：
- 阅读 issue artifacts 后，默认 posture、blocking consent、non-blocking safeguards、tool policy layering 一目了然
- 阅读 issue artifacts 后，可以明确知道 runtime 在高风险场景下先升级内部 AI 评审，何时才进入 minimal risk state
- 读者不会再把 sandbox 缺失误解成“默认不能启用 Freely”
- 读者不会再把产品级 posture truth 与下游工具配置物化 owner 混成一层

失败：
- 仍然看不清 Freely 默认是否高自治
- activation consent 与 runtime approval 混淆
- safeguard 建议被写成默认强制门禁
- autonomous escalation ladder / minimal risk semantics 仍然只留在口头讨论里
- ACP 被误写成这条 contract 的 owner

## Execution Slices

1. default posture wording
2. activation consent contract
3. safeguard guidance contract
4. runtime escalation and minimal risk contract
5. sibling owner boundary for tool policy materialization
6. status-surface visibility contract

## Revisit Triggers

- 若后续 capability lane 发现默认 posture 还需进一步拆成多个 owner
- 若 ACP/adapters 暴露出新的 translation boundary conflict
- 若 runtime implementation 表明 init/doctor/runtime/status responsibilities need another owner split

## Dev-Loop Handoff

本 issue 的下一跳应优先实现文档和 contract writeback，再决定是否同轮推进 `freely init` / launcher / status surface 的最小 code changes。
