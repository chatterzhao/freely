---
issue_id: I-20260625T222357Z-A
issue_path: docs/issues/I-20260625T222357Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260625T222357Z-A
- issue_path: docs/issues/I-20260625T222357Z-A/issue.md

## Implementation Decision Note

- decision: pr-review-guarded 改为在 test-pre-merge 执行，前置检查 clean+sync+cod
- why_this: evidence 在 test-pre-merge 才可见，checking sync 防止 test-pre-merge 丢弃后丢代码
- alternatives_considered: cp evidence → 额外步骤不可靠；信 actual_output → ghost pass 温床
- boundary_non_goals: 不改 pr-merge、不改 Manager patrol
- residual_risk: ACP bridge 不可用时 fallback legacy，未执行完整三层 review
