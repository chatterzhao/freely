# Candidates - 20260320-0605--agent-state-time-machine-and-shared-continuity

## Context
- Source brainstorm: `./brainstorms.md`
- Status: `active`

## Candidates

### C-20260320-0605-A: legacy issue
- title: Agent state time-machine and shared continuity control plane
- problem: Freely 当前已经治理了 worktree、checkpoint、continuity、handoff、recovery，但这些能力仍分散在多个 artifact 与 loop 中，尚未形成“哪些状态需要统一 snapshot / fork / rollback / shared continuity”的明确能力边界；一旦进入多 agent、多设备或更强恢复场景，单靠 Git/worktree 不足以完整恢复自治运行上下文。
- why_now: 2026-03-20 的微信文章《把 Agent 的状态放进数据库》把问题提炼得很清楚：真正值得吸收的不是 PGFS 本身，而是 `time machine` 与 `shared brain` 这两个产品能力。Freely 现在正处于多 worktree 监督、interruption、handoff 与恢复治理收敛期，适合把这条能力先收敛成 pre-brainstorm 边界。
- acceptance_hint:
  - 明确 Freely 当前哪些关键状态不在 Git/worktree 治理内
  - 明确哪些状态需要一起 snapshot / rollback，哪些可以重算
  - 明确共享连续性控制面与 worker 私有状态的边界
  - 明确这条能力是 `state-snapshot-fork-and-shared-continuity-governance`，而不是默认 `PGFS integration`
  - 给出最小实现顺序：本地 snapshot index / continuity metadata 优先，数据库 backing 作为后续选项
- priority: `P1`
- status: `needs_research`
- decision_reason: 这条能力方向对 Freely 的长期自治恢复和多 agent 协作很重要，但当前仍应先做边界收敛，而不是直接做基础设施绑定。
- next_action: 继续 pre-brainstorm，优先冻结 snapshot / fork / rollback / shared continuity 的边界，再决定是否 materialize 为独立 issue。
- revisit_trigger: 当 Freely 的多设备或多人协作场景需要统一共享连续性控制面，且本地 snapshot index 方案边界稳定后，再进入 IBM。
- promoted_issue_path: `pending://state-snapshot-fork-and-shared-continuity-materialization`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: `codex`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://codex-thread-only`
  - role: `author`
  - external_source: `https://mp.weixin.qq.com/s/t5nNOS39jtzLsGJr-kcXvw`
