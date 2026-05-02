# PRD: agent-execution-safety-review-and-security-decision-support

## Goal

定义一条可复用 capability owner，使 Freely runtime 能在保持高自治的前提下，复核真实执行边界，并在单 agent 不应独断时引入内部安全决策委员。

## Why Now

Freely 的产品 owner 已开始冻结默认高自治 posture，但没有配套 capability 的话，runtime 仍容易在高风险场景里落回两种差路径：

- 单 agent 硬判
- 重新把用户拉回逐步批准

execution-boundary review 和 security decision support 正好承接中间层：让 runtime 先更会判断、更会复核、更会继续推进。

## Product Surface

- future `docs/system/workspace/skills/**` security capabilities
- runtime review helpers
- reviewer evidence writeback surfaces

## Non-Goals

- 不接管 Freely-self product consent owner
- 不定义默认强制 sandbox
- 不把全部安全能力一次收口
- 不直接实现 full incident remediation

## Non-Negotiables

- capability 必须可复用，不是某个单次会话脚本
- reviewer / committee 是内部 AI 决策增强，不是用户审批替身
- safeguard recommendation 必须允许输出，但默认不构成 blocker
- contract 必须能对比 tool flags、project config、launch-time injection、observed posture

## Context Pack

- product owner 正在冻结默认 autonomy posture
- 现有 repo 已有 skill-based capability landing pattern
- 现有 runtime 已具备 tool adapter / launch-time injection 现实基础

## Decomposition Tree

1. execution-boundary review
2. reviewer / committee support
3. recommendation and evidence writeback
4. product-owner boundary enforcement

## Prototype Path

先冻结 IBM issue artifacts，说明 capability contract 应如何被后续 skill / reference / runtime helper materialize。

当前 advisory-only implementation slice 维持：

- project-local `security review policy` / `scope` truth
- `baseline-status` / `live-status` / `doctor` introspection
- workspace skill entry for execution-boundary review and reviewer-backed guidance
- `security-review-brief` machine-readable output for follow-on orchestration
- no launch blocking, no approval posture rewrite, no forced committee runtime

## Eval Plan

成功：
- issue artifacts 清楚区分 product consent owner 与 capability review owner
- reviewer / committee semantics 清楚
- safeguard recommendation 是支持面，不是默认阻断面

失败：
- capability 被写成 product UI/consent owner
- 又把人类逐步批准带回主路
- 仍然没有清楚的 execution-boundary comparison model

## Execution Slices

1. execution-boundary review contract
2. reviewer/committee contract
3. evidence writeback contract
4. follow-on skill split proposal
5. advisory-only runtime brief

## Revisit Triggers

- 若后续 capability 实现表明 execution review 与 decision support 应进一步拆 owner
- 若后续 product implementation 暴露新的 boundary conflict

## Dev-Loop Handoff

下一跳应优先把这条 owner 映射到最小 skill/reference/runtime-helper 组合，而不是继续在对话里泛讲“用 subagent 评审”。
