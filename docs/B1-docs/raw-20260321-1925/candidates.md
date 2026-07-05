# Candidates - 20260321-1925--manager-chat-reentry-and-cleanup-misrouting

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260321-1925-A: legacy issue
- title: Route broad supervisor chat reentry away from cleanup misrouting
- problem: 当前 `freely chat -> interruption dispatcher` 在广义主管巡检任务上，容易把新 signal 错误归到 `cleanup://merged-worktree-followthrough`，导致它没有回到主管主循环做新的 patrol / restart-point routing。
- why_now: 这已在真实 `develop` 工位集成测试中复现。若不修复，Freely “只能通过 chat 插话驱动自己开发自己”这条 dogfooding 路线就会持续失真。
- acceptance_hint:
  - 区分纯 cleanup 请求与广义主管巡检请求
  - 前者保留 `cleanup + worker`
  - 后者改为 `continuation + manager`
  - 补真实 runtime 路径回归，不只改文档 prompt
- priority: P0
- status: promoted
- decision_reason: 这是当前 Freely 自举集成测试直接暴露的运行时缺口，边界和最小修复面都已清晰，适合立即 materialize 为 issue。
- next_action: 创建 issue，修正 interruption manager handler 对 supervisor-level chat 的默认路由，并补 handler/runtime 回归测试。
- revisit_trigger: 当 supervisor-level chat reentry 能通过真实 dispatcher 路径稳定回到 manager continuation，而不是被 cleanup 过早吸收时。
- promoted_issue_path: `docs/B2-docs/ibm/manager-chat-reentry-and-cleanup-misrouting-governance/issues/manager-chat-reentry-and-cleanup-misrouting-governance.md`
- legacy_id_mapping: I-20260321-1925  # 历史遗留的 issue id
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
