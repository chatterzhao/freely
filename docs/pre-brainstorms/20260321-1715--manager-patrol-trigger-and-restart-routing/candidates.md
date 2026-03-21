# Candidates - 20260321-1715--manager-patrol-trigger-and-restart-routing

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260321-1715-A
- title: Clarify manager patrol triggers and restart-point routing in three-loop governance
- problem: 当前真源已经分别写了 `event source / standing source`、主管巡检、restart point 与委派，但还没有把它们收束成一条清晰语义：主管既应周期巡检，也应被事件唤醒；并且始终只做判断/解释/委派，把下一跳动态路由到三层 loop 的任意正确起点。
- why_now: 随着三层 loop、主管治理、worktree 收口和外部 drift 讨论增多，团队持续把 verification/writeback/cleanup 误说成第四层，或默认主管只在最前面路由一次。这个歧义已经开始影响 Freely 自举时的能力设计。
- acceptance_hint:
  - 不新增第四层 loop
  - 不新增平行大 skill
  - 明确 `auto-loop` 同时包含 patrol-driven 与 event-driven 两类入口
  - 明确主管只判断/解释/委派/监督完成，不直接施工
  - 明确 worker 或 runtime owner 返回结果后，主管继续决定下一跳 restart point
  - 明确 restart point 可落在 auto/doc/dev 三层的任意正确位置
- priority: P0
- status: proposed
- decision_reason: 现有真源已具备大部分组成件，当前最需要的是把它们收束成一致的主管 watchdog 语义，再回写到三层 loop 真源与相关 agent/skill/reference，而不是再造新能力。
- next_action: 将本条提升为对 `three-loop-capability-lifecycle`、`manager-agent`、`auto-loop-orchestrator` 与 `manager-reactivation-patrol` 的一致性增强 issue。
- revisit_trigger: 当需要把 patrol-driven/event-driven、委派回流 contract 和动态 restart-point routing 正式写入现有真源时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
