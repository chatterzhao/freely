---
issue_id: I-20260706T023422Z-A
issue_path: docs/B2-docs/ibm/b2-governance/raw-20260706T023422Z/issues/I-20260706T023422Z-A.md
phase_state: done_b2_ibm
---
- issue_id: I-20260706T023422Z-A
- issue_path: docs/B2-docs/ibm/b2-governance/raw-20260706T023422Z/issues/I-20260706T023422Z-A.md

## Implementation Decision Note
- decision: 分 4 阶段修复 docs-structure-refactor 遗漏。P1 直接替换生产代码，P2/P3 替换内容路径，P4 移动文件位置。全部用脚本从文档元数据字段提取 raw key。
- why_this: 脚本方法保证一致性，从 issue_id/local_id/promoted_from 字段提取 raw key 比路径推断准确。分阶段独立 commit 便于 review。
- alternatives_considered: (1) 手动逐文件修改 — 1400+ 文件不可行；(2) 重新运行原始迁移脚本 — 会覆盖已有修复；(3) 只修新文件不改历史 — 目录不一致持续导致门禁问题
- boundary_non_goals: 不修改 _legacy-issues/_legacy-progress 文件位置（原始 B1 设计不修改历史文件）；不修改全局 skill (~/.claude/skills/) 路径
- residual_risk: ~70 文件在多 raw key 的 story 下无法自动归属（如 a2a/handoff/prd.md 有两个 raw key），需后续人工判断
