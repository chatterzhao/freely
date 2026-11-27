---
issue_id: I-20261126T130151Z-A
issue_path: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261126T130151Z/issues/I-20261126T130151Z-A.md
phase_state: done_b2_ibm
---

# Implementation Decision Note

- issue_id: I-20261126T130151Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261126T130151Z/issues/I-20261126T130151Z-A.md
- decision: 在 pr-merge 的 test 工位同步点调用既有 `test-evidence.py attest-meta`。
- why_this: 证据判据归 test-evidence；封装命令只补调用，不造第二判据。
- alternatives_considered: 放宽 wt-close（否）；每轮重跑 CI（吞吐损失，否）。
- boundary_non_goals: 不改 test-evidence.py / wt-close；不掩盖真代码变更。
- residual_risk: 默认 sensitive paths 是保守列表；lane 声明真源出现后应改为读取声明。
