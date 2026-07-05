# Issue: milestone-planning-and-state-maintenance

- issue_id: `I-20260320-0512`
- title: Milestone planning and state maintenance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `milestone-planning-and-state-maintenance`
- issue-name: `milestone-planning-and-state-maintenance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/milestone-planning-and-state-maintenance/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260320/candidates.md#c-20260320-0512-a`
- source_brainstorm: `docs/B1-docs/raw-20260320/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 已经把 milestone 当成 standing source 和编排入口，但对 milestone sequencing、状态维护、写回 reconcile 的 owner 仍不清晰，导致 candidate/issue/progress/recovery/cleanup 之间的同步长期靠业务 worker 顺手维护。

本轮已经把 manager route、auto-loop、lifecycle 与专门 skill 全部补到位。现在需要把这条能力正式 materialize 成 canonical issue，让 milestone planning / state maintenance 成为 Freely 自己治理自身的一等能力。

## Scope

1. 定义 `skill:milestone-planning-state-maintenance` 作为专门 worker。
2. 明确 manager 在 standing-source scan 下何时委派此 worker。
3. 明确该 worker 负责 sequencing、queue drift、state drift、writeback reconcile。
4. 明确 `pre-brainstorm -> candidate -> milestone -> issue -> progress/recovery -> completed/cleanup` 应视为需要同步的治理事务线。
5. 明确该 worker 不做业务实现，也不取代 manager 的顶层优先级裁决。

## Acceptance

- `manager-agent.md` 明确 standing-source scan 后的 milestone planning / state maintenance 委派路径。
- `auto-loop-orchestrator/SKILL.md` 明确优先把 sequencing / queue drift / state maintenance 问题委派给专门 worker。
- `skill:milestone-planning-state-maintenance` 明确输入、职责边界、输出与不负责事项。
- `three-loop-capability-lifecycle.md` 明确这是独立 capability，而不是顺手补写行为。
- `./bin/governance-check` 通过。

## Completion

- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/milestone-planning-state-maintenance/SKILL.md`
- `docs/system/workspace/skills/README.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/B1-docs/raw-20260320/**`

## Verification

- `./bin/governance-check`

## Completion

- `docs/epics/workspace-routing-foundation/milestone-planning-and-state-maintenance/code-reviews/20260320-milestone-planning-state-maintenance-verification.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/milestone-planning-state-maintenance/SKILL.md`
- `docs/system/workspace/skills/README.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/B1-docs/raw-20260320/**`

## Completion Note

milestone planning and state maintenance 已完成物化并验证，作为 standing-source scan 下的独立治理能力收口。
