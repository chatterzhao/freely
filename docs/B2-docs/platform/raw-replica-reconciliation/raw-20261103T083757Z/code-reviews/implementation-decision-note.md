---
issue_id: I-20261103T083757Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T083757Z/issues/I-20261103T083757Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261103T083757Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T083757Z/issues/I-20261103T083757Z-A.md
- decision: 把 repo_path_branch 改为 Gitee v5 的 /branches/ 端点。
- why_this: GitHub git-ref 路径在 Gitee 恒 404，fallback 掩盖真实失败并产生误导性告警。
- alternatives_considered: 直接删除 fallback——会牺牲网络异常时的可恢复性；在 wt-close 侧特判——会把平台适配知识扩散到调用方。
- boundary_non_goals: 不改 fallback；不改其他 Gitee 命令。
- residual_risk: 分支名含特殊字符时未做 URL 编码，沿用既有行为（调用方控制分支名）。
