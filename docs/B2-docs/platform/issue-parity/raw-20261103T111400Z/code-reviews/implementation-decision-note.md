---
issue_id: I-20261103T111400Z-A
issue_path: docs/B2-docs/platform/issue-parity/raw-20261103T111400Z/issues/I-20261103T111400Z-A.md
phase_state: completed
---

- issue_id: I-20261103T111400Z-A
- issue_path: docs/B2-docs/platform/issue-parity/raw-20261103T111400Z/issues/I-20261103T111400Z-A.md

## Implementation Decision Note

- decision: docs-only lane + `FREELY_SKIP_IBM_GATE`（合法豁免，变更全部为治理文档）；物化用 adapter pull，回填只在标题前缀唯一匹配时进行。
- why_this: GATE 1 禁止一个工位跨 raw issue 做代码+文档混合变更；拆分保持两个 lane 各自合规。
- alternatives_considered: 等每个 issue lane 各自物化（历史编号缺口无 lane 承接，否决）。
- boundary_non_goals: 不建历史 issue、不删平台 issue、不改代码。
- residual_risk: 回填为一次性数据修复；未来新 issue 仍由 wt-create 自动物化。
