# Code Review: manager-owner-stance-and-source-patrol-governance
- issue_id: `I-20260326-1835`

## Scope

- `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/prd.md`
- `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/pre-tests.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/skills/human-interruption-manager-triage/SKILL.md`
- `docs/system/workspace/skills/signal-intent-understanding/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/system/workspace/skills/context-source-skill/references/continuation-recovery-routing.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`

## Findings

- `manager-agent` 现在明确把自己定义为运行期产品能力真源，并写清主管是项目主人、全局裁决者与 source-patrol 补账责任人，而不是默认等待人类澄清的代理。
- `worker-agent` 现在明确只负责核实 / 执行 / 回证，不接管 interruption / milestone / progress / pre-brainstorm 的项目级 completeness 裁决。
- interruption 相关 skill 现在把 human interruption 统一收紧为 advisory signal，并要求主管先判断它与当前主线的关系，而不是把用户原话直接当成调度方案。
- patrol / routing 真源现在把 standing-source completeness 明确扩到 interruption、milestone、progress、pre-brainstorm，并写清 drift 时默认走补账、核实、重排、委派。
- 本 issue 自身的 `PRD/pre-tests` 现在已从弱 wording review 型验收升级为可恢复的 acceptance contract，显式写出 post-merge integration、application-native real-environment 与 end-to-end dogfood 场景。
- 新 wording 保持在现有 issue 边界内，没有重新定义 dual-entry patrol、delegation threshold 或 active-lifecycle boundary，只把这些 issue 之上的 owner stance / completeness contract 写清。

## Verification

- `./bin/governance-check`
- wording review:
  - dogfooding governance inputs and capability truth are no longer conflated
  - manager / worker / interruption / patrol wording remains consistent with adjacent truth sources
