# Tasks: wt-close 复用单一评论扫描
- issue_id: I-20261107T133328Z-A
- pre_tests_path: docs/B2-docs/gate/governance/raw-20261107T133328Z/verification/pre-tests.md

## 任务分解

- [x] T1: 真机复现 wt-close 阻塞与破损文案，定位两份实现。
- [x] T2: 写 AT-001（5 静态 + 5 行为），基线快照确认 RED。
- [x] T3: `wt-close` 改调单一扫描实现。
- [x] T4: 跑 GREEN + 回归基线对比。
- [x] T5: 用修好的 wt-close 收口 R13 与本轮。
