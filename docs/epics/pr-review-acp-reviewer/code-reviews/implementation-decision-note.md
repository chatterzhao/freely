---
issue_id: I-20260625T152446Z-A
issue_path: docs/issues/I-20260625T152446Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260625T152446Z-A
- issue_path: docs/issues/I-20260625T152446Z-A/issue.md

## Implementation Decision Note

- decision: pr-review-guarded 从 bash 6-dimension 自审改为 ACP 启动独立 TDD Reviewer session
- why_this: 独立 session 确保他检；TDD 四问覆盖 RED/GREEN/ADEQUACY/REFACTOR 比 6-dimension 更深
- alternatives_considered: 保留 bash 检查 + ACP 增强 → 两套逻辑维护成本高；完全 ACP → 需要 fallback
- boundary_non_goals: 不改 pr-merge-guarded；不改 Manager patrol 调度
- residual_risk: ACP bridge 不可用时 fallback 到 legacy 检查（当前 fallback 未完整实现，待后续 PR）
