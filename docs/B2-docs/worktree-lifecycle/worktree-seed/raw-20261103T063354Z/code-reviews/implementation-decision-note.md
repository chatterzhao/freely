---
issue_id: I-20261103T063354Z-A
issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261103T063354Z/issues/I-20261103T063354Z-A.md
phase_state: in_b2_ibm
---

# Implementation Decision Note
- issue_id: I-20261103T063354Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261103T063354Z/issues/I-20261103T063354Z-A.md
- decision: adapter 新增 configured-platforms 只读动作；pr-merge 收尾循环改用它。
- why_this: git remote 名与 adapter 平台名是不同概念；adapter 是配置唯一真源。
- alternatives_considered: shell 解析 config.toml（第二真源）；adapter 猜 remote（职责错位）——均排除。
- boundary_non_goals: 不改 close_pr 语义；不改平台写通道；不改 dispatcher。
- residual_risk: Gitee close_pr 当前返回 skipped；本轮只修平台名与回执，不实现 Gitee PR 关闭 API。
