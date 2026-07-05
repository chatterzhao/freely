# Brainstorm: milestone-planning-and-state-maintenance

- source_brainstorm: `docs/B1-docs/raw-20260320/brainstorms.md`
- canonical_issue: `docs/epics/workspace-routing-foundation/milestone-planning-and-state-maintenance/issues/milestone-planning-and-state-maintenance.md`

## Key Decisions

- milestone sequencing 和状态维护应视为 standing-source scan 后的独立 worker 职责。
- 这是一条治理事务线，不是业务 worker 顺手补写的附属任务。
- worker 负责 reconcile 和 writeback，不接管顶层优先级裁决，也不直接写业务实现。
