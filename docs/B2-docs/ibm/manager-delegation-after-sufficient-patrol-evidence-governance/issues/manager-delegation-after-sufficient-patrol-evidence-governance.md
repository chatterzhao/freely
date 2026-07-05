# Issue: manager-delegation-after-sufficient-patrol-evidence-governance

- issue_id: `I-20260322-0228`
- title: Manager delegation after sufficient patrol evidence governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-delegation-after-sufficient-patrol-evidence-governance`
- issue-name: `manager-delegation-after-sufficient-patrol-evidence-governance`
- verification_artifact_dir: `docs/B2-docs/ibm/manager-delegation-after-sufficient-patrol-evidence-governance/code-reviews`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260322T071500Z/candidates.md#c-20260322-0228-a`
- source_brainstorm: `docs/B1-docs/raw-20260322T071500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md`
  - `docs/B2-docs/ibm/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`
  - `docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/issues/cli-first-entrypoint-and-observability-surface-unification.md`

## Why

真实 Freely dogfood 已经证明主管能够：

- 接住 `freely chat` 的项目级监督请求
- patrol 全部剩余 worktree
- 正确判断 disposition，如 `retire-only` / `retire-now` / `continue-dev`
- 并行调用 subagent 收集证据
- 写出新的 manager continuity

但这次也暴露出新的 gap：

- 当证据已经足够支持下一步执行时，主管仍继续做更多只读核查
- 没有及时切换到具体 worker handoff / cleanup execution

因此这条 issue 的目标不是增强 patrol，而是为主管补上：

- `sufficient patrol evidence`
- `delegation threshold`
- `stop patrolling and delegate`

的硬性治理语义。

## Scope

1. 在 `manager-agent` 中定义：当 worktree disposition 与 next action 已经稳定时，主管必须停止继续补充 patrol 证据并切换到具体 worker handoff。
2. 在 `auto-loop-orchestrator` 中定义：`auto-loop` 对项目级 patrol 的完成条件不只是写 continuity，而是把 stable disposition 转成下一跳 execution routing。
3. 在 `multi-worktree-supervision` 中补充项目级监督规则：当 `retire-only / retire-now / continue-dev` 已稳定时，主管应优先启动具体 cleanup / continue-dev worker，而不是继续 manager-only 巡检。
4. 这条 issue 只收敛真源语义，不新增新的平行 skill，不实现新的 runtime 机制。

## Acceptance

- `manager-agent` 明确要求：
  - 若 disposition 已稳定，主管必须优先输出 worker-specific handoff
  - 继续 patrol 只能在缺少关键事实或存在 blocker 时发生
- `auto-loop-orchestrator` 明确要求：
  - patrol 完成后要进入 concrete execution routing
  - 不能只停在 manager continuity
- `multi-worktree-supervision` 明确要求：
  - `retire-only / retire-now / continue-dev` 应转成具体 worker next step
- 本 issue 的 verification evidence 记录这次真实 dogfood 现象，并说明为什么这条语义收敛是必要的

## Completion

- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/progress/workspace-routing-foundation/p-manager-delegation-after-sufficient-patrol-evidence-governance.md`
- `docs/B2-docs/ibm/manager-delegation-after-sufficient-patrol-evidence-governance/code-reviews/20260322-manager-delegation-after-sufficient-patrol-evidence-governance-verification.md`

## Verification

- `./bin/governance-check`
- real dogfood observation captured in this lifecycle:
  - manager can patrol and classify remaining feature worktrees
  - but needed an additional governance refinement to force timely worker delegation after evidence is sufficient

## Next

- 当前批次已完成 truth-source 收敛。
- 若后续仍观察到主管在证据充分后迟迟不进入 worker execution，则应通过新 lifecycle 进入 runtime / prompt / delegation mechanism 层修复。
