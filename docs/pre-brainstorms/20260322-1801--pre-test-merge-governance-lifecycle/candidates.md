# Candidates - 20260322-1801--pre-test-merge-governance-lifecycle

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260322-1801-A
- title: pre-test-merge responsibility, usage, and lifecycle governance
- problem: `pre-test-merge` 现在同时被用作临时预集成验证批次、真实验收环境的比较基线，以及旧实现回收的中间站，但职责边界、允许操作、失效条件和退休条件都没有被明确收束。
- why_now: 这次分叉直接暴露出 `pre-test-merge` 的生命周期管理不足。如果不先收口，它会继续把“验证批次”和“事实主线”混在一起，造成有效实现难以判断该保留还是该回收。
- acceptance_hint:
  - 明确 `pre-test-merge` 只是临时预集成验证批次，而不是长期开发父分支
  - 明确哪些动作允许、哪些动作禁止、哪些情况必须退役当前批次
  - 明确 stale batch 的判定信号，以及 `develop` 前进后是否需要重建批次
  - 明确 promote 语义是保留批次快照，还是 replay 来源 feature
  - 明确这套判断能被 Freely 自己消费，而不是只靠人工记忆
- priority: P0
- status: promoted
- decision_reason: 这是治理定义问题，不是 runtime 修补问题。它决定 Freely 后续如何使用 `pre-test-merge`，而不是单次如何合并。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author

### C-20260322-1801-B
- title: pre-test-merge lifecycle management capability for Freely
- problem: 即使治理规则写清了，Freely 仍缺少能够自动识别 `pre-test-merge` 是否 stale、是否需要 retire、是否能 promote、以及是否必须 replay 来源 feature 的能力。
- why_now: 这次问题已经证明“只靠人记住规则”不够。Freely 作为未来的开发工具，需要把这套判断 materialize 成可执行能力，才能避免下一次再次手工误用。
- acceptance_hint:
  - runtime 或 status surface 能暴露当前 `pre-test-merge` 批次状态
  - branch-management 相关能力能识别 `pre-test-merge` 的角色和失效边界
  - patrol / promotion 判断能提示 stale batch、replay requirement 和 cleanup requirement
  - 该能力不改变现有实现语义，只补判定与可见性
- priority: P1
- status: proposed
- decision_reason: 这是治理规则落成工具能力的下一步，不应和职责定义混在同一个 issue 中。
- promoted_issue_path: `pending://pre-test-merge-lifecycle-management-capability`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: `C-20260322-1801-A` 已 materialize 成正式 issue；当前保持在 pre-brainstorm，等职责定义 issue 写稳后，再决定 stale-batch detection、batch retirement、replay requirement 和 promote visibility 应落在 runtime/status、branch-management、manager patrol 还是组合能力中
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
