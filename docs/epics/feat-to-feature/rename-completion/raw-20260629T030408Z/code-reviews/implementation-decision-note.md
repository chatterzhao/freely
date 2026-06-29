---
issue_id: I-20260629T030408Z-A
issue_path: docs/epics/feat-to-feature/rename-completion/raw-20260629T030408Z/issues/I-20260629T030408Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260629T030408Z-A
- issue_path: docs/epics/feat-to-feature/rename-completion/raw-20260629T030408Z/issues/I-20260629T030408Z-A.md

## Implementation Decision Note

- decision: 全局字符串替换 freely-feat-execution → freely-feature-execution，AGENTS.md 中 feat: → feature:
- why_this: 纯字符串替换，sed 一行完成，无逻辑变更，零风险
- alternatives_considered: 逐个文件手工编辑 — 但 sed 更高效且不易遗漏
- boundary_non_goals: 不改历史文档（docs/issues/、docs/pre-brainstorms/、docs/epics/ 中的历史记录保持原样）；不改 ~/.claude/skills/ 下的 skill 副本（由 deploy-skills 负责同步）
- residual_risk: 无。sed 替换前后均可 grep 验证，无歧义
