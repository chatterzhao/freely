---
issue_id: I-20261124T054201Z-A
issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261124T054201Z/issues/I-20261124T054201Z-A.md
phase_state: completed
---

- issue_id: I-20261124T054201Z-A
- issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261124T054201Z/issues/I-20261124T054201Z-A.md

## Implementation Decision Note
- decision: test-all 每个测试输出到独立日志，成功保留摘要、失败打印断言尾部并留完整日志；SUMMARY 与退出码不变。
- why_this: CI 失败现状（只有 [FAIL] 行）让 AI 无法自诊断，直接损害项目自举目标；成功摘要不变避免日志爆炸。
- alternatives_considered: 失败输出直接打 stdout（日志混杂、无 artifact，否决）；CI 层 upload-artifact 包装（本地无诊断，治标，否决）。
- boundary_non_goals: 不改被测测试、不改 gate 判据、不改 SUMMARY 格式与 known-broken 清单。
- residual_risk: 失败日志尾部截断可能漏掉更早的断言（用可配置尾部行数 + 完整日志落盘兜底）。
