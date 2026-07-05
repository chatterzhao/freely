# Issue: three-loops-sibling-relationship-and-terminal-governance

- issue_id: `I-20260324-0405`
- title: 三个 loop 的并列关系与 terminal governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `three-loops-sibling-relationship-and-terminal-governance`
- issue-name: `three-loops-sibling-relationship-and-terminal-governance`
- verification_artifact_dir: `docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/code-reviews`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260319/candidates.md#c-20260319-1105-a`
- additional_source_candidates:
  - `docs/B1-docs/raw-20260323/candidates.md#c-20260323-0241-a`
- source_brainstorm: `docs/B1-docs/raw-20260319/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/PROJECT_INTENT.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

## Why

Freely 当前已经把 `auto-loop`、`doc-loop`、`dev-loop` 写进多个 active truth，但中文口径和部分图示仍把它们渲染成“`三层`”或近似包含关系，结果带来三个持续误解：

- `doc-loop` 被误读成 `dev-loop` 的上层或前置层，而不是 sibling execution loop
- verification / cleanup / recovery 被误写成新增 loop，而不是 route / phase / governance path
- 局部 loop 收口被误判成 terminal completion，worktree lifecycle 与 outer governance 的结束条件因此持续漂移

这不是单个 wording bug，而是 Freely 自举与未来对外开发都会反复踩到的高层治理缺口。必须把“**三个 loop**”的关系、跳出条件和 terminal closure 真源统一收敛，再继续扩 runtime / skills / product surfaces。

## Scope

1. 在 active truth 中统一把“`三层`”纠偏成“`三个 loop`”。
2. 明确：
   - `auto-loop` 是 orchestration / governance outer loop
   - `doc-loop` 与 `dev-loop` 是 sibling execution loops
   - verification / recovery / cleanup 是 route、phase 或 governance path，不是额外 loop
3. 明确 loop exit / re-entry / terminal semantics：
   - `doc-loop` 跳出只表示文档边界已收敛到下一跳
   - `dev-loop` 跳出只表示 issue 实现/验证到达下一门
   - completion / verification / cleanup 的最终裁决属于 `auto-loop`
   - 只有 outer governance 看到 cleanup / retirement 闭环，当前主题才退出 active lifecycle
   - watchdog 发现的 restart storm / process churn 属于 `auto-loop` supervision signal，由主管裁决 dead-loop / thrash，而不是让 worker 或 watchdog 自行宣布 terminal judgement
4. 明确 active truth、active lifecycle、historical evidence 的改写边界，避免全仓盲替。
5. 只改 active truth，不回写历史已完成 issue 的历史语义。

## Acceptance

- `CONSTITUTION.md`、`PROJECT_INTENT.md`、`three-loop-capability-lifecycle.md`、`manager-agent.md`、`auto-loop-orchestrator/SKILL.md` 在高层关系上保持一致：
  - “三个 loop”而非“三层”
  - `auto-loop` outer
  - `doc-loop` / `dev-loop` sibling
  - verification / cleanup / recovery 非新增 loop
- `three-loop-capability-lifecycle.md` 明确区分：
  - loop
  - route_kind
  - phase / lifecycle state
  - terminal cleanup / retirement
- `three-loop-capability-lifecycle.md`、`manager-agent.md`、`auto-loop-orchestrator/SKILL.md` 明确一致：
  - worker 负责在 `doc-loop` / `dev-loop` 中产出文档、实现、测试与 verification evidence
  - `auto-loop` 负责完成判定、验证裁决、cleanup / retirement 路由
  - restart storm / process churn 由 watchdog 暴露为 signal，再由主管在 `auto-loop` 中判断是否 dead-loop / thrash
- `PROJECT_INTENT.md` 的图和路由表不再暗示 `doc-loop` 包含 `dev-loop`
- 本 issue 的 dev 改动只覆盖 active truth，不试图重写历史 evidence

## Completion

- `docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/issues/three-loops-sibling-relationship-and-terminal-governance.md`
- `docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/brainstorms/b-three-loops-sibling-relationship-and-terminal-governance.md`
- `docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/prd.md`
- `docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/pre-tests.md`
- `docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-three-loops-sibling-relationship-and-terminal-governance.md`
- `docs/CONSTITUTION.md`
- `docs/PROJECT_INTENT.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`

## Verification

- `./bin/governance-check`
- `rg -n "三层循环|三层 loop|三层职责边界" docs/CONSTITUTION.md docs/PROJECT_INTENT.md docs/system/workspace/three-loop-capability-lifecycle.md docs/system/workspace/agents/manager-agent.md docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md docs/LAWS.md`
- read the updated active truth set together and confirm no file still implies `doc-loop` contains `dev-loop`
- confirm verification / cleanup are described as route / phase / governance path rather than extra loop

## Code Review

- `docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/code-reviews/20260324-three-loops-sibling-relationship-verification.md`

## Verification Summary

- active truth、runtime-facing contract、脚本提示词真源已统一到“`auto-loop` outer + `doc-loop` / `dev-loop` sibling”的模型，不再把它们描述成包含式“三层”。
- verification / cleanup / recovery 已统一收束为 route / phase / governance path，不再伪装成额外 loop。
- worker 负责在 `doc-loop` / `dev-loop` 内产出文档、实现、测试和 verification evidence；completion / cleanup / retirement judgement 明确回到 `auto-loop`。
- watchdog 发现 restart storm / process churn 时只暴露 supervision signal；dead-loop / thrash 结论仍由主管在 `auto-loop` 中裁决。
- 本 issue 的 pre-merge 验收已完成，但 worktree 仍需后续 merge / cleanup / retirement 才能进入 delete-eligible。
