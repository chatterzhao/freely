# Issue: active-lifecycle-boundary-and-dogfooding-capability-discovery

- issue_id: `I-20260321-1745`
- title: Active lifecycle boundary and dogfooding capability discovery
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `active-lifecycle-boundary-and-dogfooding-capability-discovery`
- issue-name: `active-lifecycle-boundary-and-dogfooding-capability-discovery`
- verification_artifact_dir: `docs/B2-docs/- epic-name: `workspace-routing-foundation`/- story-name: `active-lifecycle-boundary-and-dogfooding-capability-discovery`/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260321T170600Z/candidates.md#c-20260321-1745-a`
- source_brainstorm: `docs/B1-docs/raw-20260321T170600Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/B2-docs/ibm/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 当前仍缺少一条稳定的生命周期边界语义，导致团队会反复争论：

- 什么算“历史”？
- 什么算“当前仍可修改的真源”？
- Freely 在狗粮中暴露出来的问题，应视为一次性项目经验，还是优先判断为 Freely 产品能力缺口？

如果这层边界不固定，后续会不断出现两类错误：

- 把仍在活跃生命周期里的 issue/worktree 错当历史，过早冻结真源
- 把已完成且已收口的历史产物继续当当前承接面回写，破坏追溯性

同时，Freely 开发 Freely 时暴露出的共性问题也会继续停留在聊天或 continuity 里，而不是 materialize 成用户也能复用的能力。

## Scope

1. 在 `three-loop-capability-lifecycle.md` 中明确：
- `historical` 与 `active lifecycle` 以生命周期与收口状态判断，而不是创建时间
- 当前活跃生命周期内允许对应用产物做收敛重构，而不是记流水账
- 只有 `completed + worktree merge/cleanup closure` 的产物才进入历史追溯面

2. 在 `PROJECT_INTENT.md` 中明确：
- Freely 开发 Freely 时暴露的可复现共性问题，默认先判断是否应成为 Freely 能力发现
- 若可泛化到用户项目，应优先进入三层循环，而不是只保留成一次性项目经验

3. 保持边界一致：
- 不回写历史已完成 issue
- 不在旧 issue 上追加当前轮语义
- 通过当前新 issue 生命周期收敛方法论更新

## Acceptance

- `three-loop-capability-lifecycle.md` 明确：
  - `historical = 已完成且已收口`
  - `active lifecycle = 仍在活跃执行链里，即使文件较早创建`
  - 当前活跃链允许应用产物收敛重构
- `PROJECT_INTENT.md` 明确狗粮能力发现原则
- 新 wording 不与既有三层 loop / manager / worktree 治理语义冲突
- 不通过修改历史已完成 issue 来承载本轮新讨论

## Completion

- `docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/issues/active-lifecycle-boundary-and-dogfooding-capability-discovery.md`
- `docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/brainstorms/b-active-lifecycle-boundary-and-dogfooding-capability-discovery.md`
- `docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/prd.md`
- `docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/raw-20260321-1745/verification/pre-tests.md`
- `docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/tasks.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/PROJECT_INTENT.md`
- `docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/raw-20260321-1745/code-reviews/20260321-active-lifecycle-boundary-and-dogfooding-capability-discovery-verification.md`

## Verification

- `./bin/governance-check`
- wording review of lifecycle boundary and dogfooding principle for contradiction / overlap / residual ambiguity
- `docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/raw-20260321-1745/code-reviews/20260326-active-lifecycle-boundary-canonical-replay-verification.md`

## Next

- 当前文档真源收敛与 contradiction review 已完成，本 issue 正式完成。
- 若后续需要把“狗粮问题 -> 能力发现”的判断脚本化或路由化，再由新的 runtime/agent 增量承接。
