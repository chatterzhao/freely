# Candidates - 20260303-0000--cli-orchestration-architecture

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260303-101
- title: CLI 编排最小闭环实现
- problem: 现有编排概念完整，但缺少最小执行落点。
- why_now: 是让 auto-loop 可运行的直接前置。
- acceptance_hint: 提供命令编排、超时重试、日志与失败回退策略。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 已由 auto-loop-orchestrator bootstrap 与现有编排真源吸收，不应再保留为独立待 materialize 候选。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/B2-docs/ibm/bootstrap-routing-foundation-artifacts/issues/auto-loop-orchestrator-bootstrap.md`
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- session_refs: []

### C-20260303-102
- title: 集成测试优先门禁落地
- problem: 验收标准存在，但门禁执行路径不稳定。
- why_now: 自治开发优先保障可运行与可回归。
- acceptance_hint: 进入提升流程前强制集成测试通过。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 集成测试优先门禁已被现行法律和分支治理真源吸收，无需再补历史 issue。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/LAWS.md`
  - `docs/system/workspace/skills/branch-management/SKILL.md`
- session_refs: []

### C-20260303-103
- title: 会话管理机制（恢复/压缩/新会话）
- problem: 自治循环缺少标准化会话生命周期管理，恢复链路不稳。
- why_now: 属于后续行动清单中的直接工程项，影响无人值守连续性。
- acceptance_hint: 定义会话恢复、上下文压缩与新会话切换策略及审计字段。
- priority: P1
- status: promoted
- decision_reason: 与恢复优先和自治持续运行目标直接对齐，应纳入主线实现。
- promoted_issue_path: `docs/B2-docs/ibm/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
- legacy_id_mapping: I-20260316-1801  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: []
