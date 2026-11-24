---
issue_id: I-20261124T072402Z-A
issue_path: docs/B2-docs/gate/ci-merge-protection/raw-20261124T072402Z/issues/I-20261124T072402Z-A.md
phase_state: completed
---

- issue_id: I-20261124T072402Z-A
- issue_path: docs/B2-docs/gate/ci-merge-protection/raw-20261124T072402Z/issues/I-20261124T072402Z-A.md

## Implementation Decision Note

- decision: 只改文档断言——更正 workflow 注释中错误的「pr-merge-guarded 置 check success」，明确 check 恒 in_progress 是拦截网页合并的设计态；不改任何运行时代码。
- why_this: 原 P0 功能断言经实测证伪（保护可安全启用、本地合并不受 check 影响）；真正问题是过时的注释会诱导重复误判。
- alternatives_considered: 在 pr-merge-guarded 接线置 success（会让网页按钮可用、破坏「NEVER merge button」目标，否决）；什么都不改（误导持续，否决）。
- boundary_non_goals: 不改 workflow jobs/permissions/triggers、不改合并逻辑、不改分支保护配置、不触碰平台 issue 生命周期。
- residual_risk: 若未来设计改为 CI/App 置 success 并保留网页拦截，需重新评估；AT 会锁定当前契约，届时一并更新。
