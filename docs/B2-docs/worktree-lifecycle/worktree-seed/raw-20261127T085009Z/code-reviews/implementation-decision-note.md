---
issue_id: I-20261127T085009Z-A
issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T085009Z/issues/I-20261127T085009Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261127T085009Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T085009Z/issues/I-20261127T085009Z-A.md
- decision: 显式 --source-platform 跳过全副本前置校验，物化后由 issue-sync create 补齐缺失副本。
- why_this: 参数已存在却未接入判据，导致单平台 legacy raw 无法开工位；补判据比放宽全局 gate 更安全。
- alternatives_considered: 全局允许缺副本——会让双平台原子性失去前置保障；手工 git worktree——被 reference-transaction hook 正确拦截。
- boundary_non_goals: 不改 adapter、不改 raw-reconciliation 判据、不实现 R59。
- residual_risk: 显式参数必须由调用方确认来源可靠；所有补副本动作仍经 issue-sync 双平台汇总。
