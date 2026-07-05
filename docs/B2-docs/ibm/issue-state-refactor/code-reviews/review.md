- issue_id: I-20260505T1210Z-A
- issue_path: docs/B2-docs/ibm/issue-state-refactor/issues/I-20260505T1210Z-A.md

# code-review: issue state refactor

## Implementation Decision Note

- decision: 将 scan 的 TERMINAL_RAW / DONE_STATES / ACTIVE_B2 常量对齐 IBM Framework §89 定义，raw 和 I-* 统一用 phase_state 字段名
- why_this: 当前 scan 的 completed 出现在 TERMINAL_RAW 中（raw 不应有 completed），DONE_STATES 包含不在 IBM Framework 中的 done/done_ibm，issue-sync 跨层污染 status 字段
- alternatives_considered: (1) 只修 issue-sync 不修 scan 常量——拒绝，因为 scan 常量才是根源定义 (2) 两字段方案（status+phase_state）——拒绝，统一用 phase_state 更简洁
- boundary_non_goals: 不在此 scope：chat-inbox consumed 逻辑、平台 label 体系、candidate status 字段
- residual_risk: 历史 1 个 issue 使用 phase_state=done（非标准值），迁移后需手动修正为 done_b2_ibm

## Changes reviewed
- `task-lifecycle-scan.py`: constants aligned with IBM Framework §89
- `bin/migrate-issue-phase-state`: one-shot migration script

## Decision: Approve
