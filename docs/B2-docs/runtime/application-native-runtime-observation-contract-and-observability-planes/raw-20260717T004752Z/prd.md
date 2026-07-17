# PRD: 监督面观测真源对齐
- issue_id: I-20260717T004752Z-A

## Goal
读文档即可正确理解监督面现行为；trace §11 与实际打点零漂移；L240 缺口闭合。

## 实现方案
b-I 清单。顺序：L240 打点 → trace-contract → capability-lifecycle → SKILL → AGENTS → deploy-skills。

## Dev-Loop Handoff
RED 4 项 → 实现 → GREEN（AT-003 E2E 在 test 工位）。
