- issue_id: I-20260505T1210Z-A-C
- issue_path: docs/epics/workspace-routing-foundation/issue-state-refactor/issues/I-20260505T1210Z-A-C.md

# code-review: governance gate state consistency

## Implementation Decision Note

- decision: 在 governance-merge-gate 中新增 G1/G2/G3/S3 四条规则，检查 develop merge diff 中所有 issue 的状态一致性
- why_this: C-A 修正了 scan 常量，C-B 修正了 issue-sync 污染源，C-C 兜底拦截任何遗漏的状态不一致
- alternatives_considered: 放在 scan 中做软诊断——拒绝，scan 输出建议但 gate 才是阻断点
- boundary_non_goals: 不检查不在 merge diff 中的 issue
- residual_risk: 历史 issue 中可能仍有 phase_state 值不符合新规范（如 done），但这些不在当前 merge diff 中

## Decision: Approve
