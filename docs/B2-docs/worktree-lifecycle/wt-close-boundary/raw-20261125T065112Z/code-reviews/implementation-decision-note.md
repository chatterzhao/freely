---
issue_id: I-20261125T065112Z-A
issue_path: docs/B2-docs/worktree-lifecycle/wt-close-boundary/raw-20261125T065112Z/issues/I-20261125T065112Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261125T065112Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/wt-close-boundary/raw-20261125T065112Z/issues/I-20261125T065112Z-A.md
- decision: 同步三份文档为 write-free 单入口；对 touched linked I-* 加 strict YAML frontmatter 门禁；AT 锁住文档与提示。
- why_this: 实现方向已正确，故障来自执行者按过时文档操作与解析空字段；改说明与判据比改运行时更安全。
- alternatives_considered: 全仓 322 个 linked 文档批量补 schema——230 个历史文档无实际改动需求，噪声过大；恢复 wt-close 写平台——违背 #4699 的单一平台写通道。
- boundary_non_goals: 不改 wt-close 运行时写权；Phase 7 死代码与 dev↔test 双实现统一列为长期架构债（本轮不夹带）。
- residual_risk: schema 门禁只覆盖本分支触及的 linked 文档；历史文档在被修改时才会被要求补 schema。
