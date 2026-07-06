# PRD: manager-owner-stance-and-source-patrol-governance

## Goal

把 Freely 产品能力真源中的 manager / worker / interruption / standing-source patrol 边界写成独立、可恢复的运行期 contract，让主管明确以项目主人姿态处理插话与 source drift，而不再依赖开发治理文档的暗示语义。

## Why Now

Freely 当前已经有 manager / worker / interruption / patrol 的分散真源，但仍缺少一条更高层的一致表达：

- 开发 Freely 的治理输入不能直接充当产品化后的运行期角色真源
- 产品能力真源里还没有把 manager owner stance、advisory interruption semantics 与 source-patrol completeness 一起写清

结果是 AI 容易把开发期治理文档误读成运行期角色合同，或在面对插话和 source drift 时回退成“继续问人”而不是主管自己做项目级判断。

## Product Surface

- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/skills/human-interruption-manager-triage/SKILL.md`
- `docs/system/workspace/skills/signal-intent-understanding/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/system/workspace/skills/context-source-skill/references/continuation-recovery-routing.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`

## Non-Goals

- 不改写开发 Freely 的治理输入来充当运行期角色真源
- 不新增第四层 loop
- 不实现新的 runtime / watchdog / dispatcher 机制
- 不重复定义已有的 restart-point routing 或 delegation threshold

## Non-Negotiables

- `docs/PROJECT_INTENT.md`、`docs/CONSTITUTION.md`、`docs/LAWS.md` 不能被当成这条能力的运行期角色真源替代品
- manager 必须被表达成项目主人，而不是等待用户澄清的客服代理
- human interruption 必须被表达成 advisory signal，而不是自带调度权的命令
- worker 不接管项目级方向裁决

## Context Pack

- 这条能力只改产品能力真源，不改开发治理输入
- 邻近 issue 已分别覆盖 manager trigger、delegation threshold、active lifecycle boundary；本 issue 只负责把这些之上的 owner stance / completeness contract 写清
- Freely 自举过程中已经暴露出把开发治理文档误读成运行期角色合同，以及把 source drift 默认回抛给用户澄清的偏差

## Decomposition Tree

1. 在 `manager-agent` 写清主人姿态与默认全局判断
2. 在 `worker-agent` 写清受委派执行者边界
3. 在 interruption skill 写清 advisory signal semantics
4. 在 patrol / routing 真源写清 standing-source completeness
5. 在各文件间统一 wording，避免再靠读者拼接

## Prototype Path

最小原型就是把上述真源改成一致口径，并通过治理检查与回读验证“不能再自然误解为开发治理输入就是运行期角色真源”。

## Eval Plan

成功：
- 单独阅读相关产品能力真源时，能明确区分开发治理输入与运行期能力真源
- manager / worker / interruption / patrol 的新边界在相邻真源里保持一致
- `pre-tests.md` 能恢复：
  - pre-merge focused regression / wording consistency checks
  - post-merge integration acceptance
  - post-merge application-native real-environment acceptance
  - post-merge end-to-end dogfood acceptance

失败：
- 仍能从真源里读出“主管默认应回去问用户澄清”
- 仍能把 `PROJECT_INTENT / CONSTITUTION / LAWS` 当作直接运行期角色真源
- standing-source patrol 仍容易被理解成只盯单一 source

## Execution Slices

1. `manager-agent`
2. `worker-agent`
3. interruption skills
4. patrol / routing references
5. lifecycle writeback

## Revisit Triggers

- 若后续要把 source completeness 扩成 machine-readable runtime transaction
- 若后续要把 interruption / patrol 决策写入更强的 runtime consumption contract
- 若开发治理输入与产品能力真源仍继续在其他角色真源里混淆

## Dev-Loop Handoff

本 issue 的实现就是产品能力真源改写本身，不需要新增 runtime 代码。
