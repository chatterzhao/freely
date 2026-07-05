---
issue_id: I-20260628T054513Z-A
issue_path: docs/issues/I-20260628T054513Z-A/issue.md
phase_state: completed
---

- issue_id: I-20260628T054513Z-A
- issue_path: docs/issues/I-20260628T054513Z-A/issue.md

## Implementation Decision Note

- decision: pre-commit hook 移除 --fail-on-required 和 exit 1，scope 超标仅输出诊断信息
- why_this: 文件数不等于 scope 爆炸，硬阻塞逼迫拆分同一逻辑变更
- alternatives_considered: 保留硬阻塞（拒绝：行业无先例，文件数是粗糙代理）
- boundary_non_goals: 不改 checkpoint-guard 本身的 scope 检测逻辑；不添加 git add hook
- residual_risk: 移除阻塞后可能出现真正 scope 混乱的提交，但 AGENTS.md 规范 + PR review 兜底
