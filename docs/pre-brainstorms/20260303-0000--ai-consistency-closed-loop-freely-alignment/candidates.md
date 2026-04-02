# Candidates - 20260303-0000--ai-consistency-closed-loop-freely-alignment

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260303-001
- title: Ring + SSOT 规则契约化
- problem: 一致性规则分散在讨论中，缺少统一可执行契约。
- why_now: 会直接影响后续 doc/dev skills 的稳定性。
- acceptance_hint: 输出 `Ring/SSOT` 冲突决议规则与检查点清单。
- priority: P0
- status: needs_research
- decision_reason: 方向仍有价值，但当前没有一条精确 issue 对其进行独立承接；不应伪装成已 promotion。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260306-workspace-routing-foundation
- session_refs: []

### C-20260303-002
- title: 独立监理 Gate 接入 auto-loop
- problem: 缺少独立监理放行机制，易出现自证通过。
- why_now: 自治开发阶段需先锁住质量下限。
- acceptance_hint: 增加独立审查通过前不得标记完成的门禁。
- priority: P1
- status: needs_research
- decision_reason: 方向合理但缺少与当前执行链路的最小实现边界，需补方案再晋升。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260306-workspace-routing-foundation
- session_refs: []

### C-20260303-003
- title: 验收合同 + 自包含交付检查落地
- problem: 验收边界与文档自包含规则未形成统一可执行检查。
- why_now: 会直接影响 dev-loop 进入条件与交付稳定性。
- acceptance_hint: 提供 acceptance-contract-builder 与 self-contained-delivery-checker 的最小实现规范。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 核心意图已被现有 IBM 执行与法律门禁真源吸收，不需要再单独 materialize 新 issue。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/skills/laws-enforcer/SKILL.md`
- session_refs: []
